#!/usr/bin/env python3
"""tokenmost 自动数据流水线 —— 零 token：纯规则抓取，无任何 LLM 参与。

用法：
    python3 tools/sync.py            # 实跑，直接更新数据文件
    python3 tools/sync.py --dry-run  # 只打印将要发生的变化，不写文件

流程：
  1. 按 tools/sources.json 逐源抓取（json API / watch 页面 / rss）
     - json  : 结构化 API → 按 action 更新 deal 文案 / 比价行，成功即续验证戳（verify_by=auto）
     - watch : 官方页面哈希监控 → 哈希不变=内容仍成立=自动续验证戳；
               变了=内容可能过期 → 相关 deal 降级「待复核」+ 写入 review-queue.md
     - rss   : linux.do 等社区源 → 关键词白/黑名单过滤 → 只生成 published:false 草稿
  2. 规则引擎：deadline 已过 → 自动标「已失效」；verified_at 超 stale_days → 自动降级待复核
  3. 写回 deals.json / prices.json / .sync-state.json / review-queue.md
  4. 调 tools/check.py 校验并重生成 rss.xml（失败则以非零码退出，CI 不提交坏数据）

设计约束：GitHub Actions 公共仓免费额度内运行；对目标站点礼貌抓取（每日 2 次、单线程、带 UA）。
"""
import json
import sys
import re
import hashlib
import html as htmlmod
import datetime
import subprocess
import urllib.request
import urllib.error
from urllib.parse import urljoin
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "Mozilla/5.0 (compatible; tokenmost-sync/1.0; +https://tokenmost.com)"}
NOW = datetime.datetime.now(datetime.timezone.utc)
NOW_ISO = NOW.strftime("%Y-%m-%dT%H:%M:%SZ")
TODAY = NOW.date()
DRY = "--dry-run" in sys.argv


def fetch(url: str, timeout: int = 25, ua=None) -> str:
    for _ in range(5):  # 手动跟随重定向（urllib 不处理 308）
        req = urllib.request.Request(url, headers={"User-Agent": ua or UA["User-Agent"]})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            loc = e.headers.get("Location") if e.headers else None
            if e.code in (301, 302, 303, 307, 308) and loc:
                url = urljoin(url, loc)
                continue
            raise
    raise RuntimeError(f"重定向超过 5 跳: {url}")


def content_hash(text: str) -> str:
    """归一化后哈希：剥离 script/style/注释/nonce/CSRF/长随机串，只对可见内容变化敏感。
    （React 态、CSRF token、资源哈希等每次请求都不同，直接哈希原始 HTML 会永远误报「有变」。）"""
    t = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", text)
    t = re.sub(r"(?s)<!--.*?-->", " ", t)
    t = re.sub(r'(?i)\s(?:nonce|csrf[\w-]*|integrity|data-[\w-]*hash)="[^"]*"', " ", t)
    t = re.sub(r"[A-Za-z0-9_\-/+=]{24,}", " ", t)  # 残留的长随机串/资产指纹/内联 token
    t = re.sub(r"\s+", " ", t)
    return hashlib.sha256(t.encode("utf-8", errors="replace")).hexdigest()[:16]


def dump_lines(path: Path, arr: list):
    """一行一条的 JSON 数组，git diff 友好。"""
    path.write_text("[\n" + ",\n".join("  " + json.dumps(x, ensure_ascii=False) for x in arr) + "\n]\n", encoding="utf-8")


def main() -> int:
    cfg = json.loads((ROOT / "tools" / "sources.json").read_text())
    state_path = ROOT / ".sync-state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {"sources": {}}
    src_state = state.setdefault("sources", {})

    deals = json.loads((ROOT / "deals.json").read_text())
    prices = json.loads((ROOT / "prices.json").read_text())
    by_id = {d["id"]: d for d in deals}
    summary = []        # 运行摘要
    deals_dirty = False
    prices_dirty = False

    def bump(deal_ids, src_id):
        """自动续验证戳。只处理仍为 verified 的已发布条目——
        被降级（stale）的条目必须人工核实后才能恢复，页面恢复稳定不算数。"""
        nonlocal deals_dirty
        for did in deal_ids:
            d = by_id.get(did)
            if not d:
                summary.append(f"WARN 源 {src_id} 引用的 deal {did} 不存在")
                continue
            if not d.get("published", True) or d.get("verify_status") != "verified":
                continue
            d["verified_at"] = NOW_ISO
            d["verify_by"] = "auto"
            deals_dirty = True

    for src in cfg["sources"]:
        sid, url, styp = src["id"], src["url"], src["type"]
        st = src_state.setdefault(sid, {})
        try:
            text = fetch(url, ua=src.get("ua"))
        except Exception as e:
            st["fail_streak"] = st.get("fail_streak", 0) + 1
            st["last_error"] = f"{type(e).__name__}: {e}"[:200]
            summary.append(f"FAIL {sid}: {st['last_error']}")
            continue
        st["fail_streak"] = 0
        st["last_ok"] = NOW_ISO
        h = content_hash(text)
        min_len = src.get("min_len", 200)
        if len(text) < min_len:
            summary.append(f"SKIP {sid}: 响应过短（{len(text)}B < {min_len}B），疑似 JS 渲染页或反爬，记为基线不参与续期")
            st["hash"], st["len"] = h, len(text)
            continue

        # ---- 结构化 JSON 源：内容级自动更新 ----
        if styp == "json":
            try:
                data = json.loads(text)
            except json.JSONDecodeError as e:
                summary.append(f"FAIL {sid}: JSON 解析失败 {e}")
                continue
            models = [m.get("id", "?") for m in data.get("data", [])]
            free = [m["id"] for m in data.get("data", []) if str(m.get("id", "")).endswith(":free")]
            ctx = {
                "n_models": len(models), "n_free": len(free),
                "top_models": "、".join(models[:3]), "free_top": "、".join(free[:3]),
            }
            for act in src.get("actions", []):
                if act["do"] == "update_deal":
                    d = by_id.get(act["deal"])
                    if not d:
                        summary.append(f"WARN {sid}: deal {act['deal']} 不存在")
                        continue
                    new_val = act["template"].format(**ctx)
                    if d.get("value") != new_val:
                        summary.append(f"UPDATE {sid} → {act['deal']}: 文案已随 API 更新")
                    d["value"] = new_val
                    bump([act["deal"]], sid)
                elif act["do"] == "sync_prices":
                    tag = f"auto:{sid}"
                    keep = [p for p in prices if p.get("source") != tag]
                    for m in free[: act.get("free_top", 3)]:
                        keep.append({"model": m, "provider": act["provider"], "layer": act["layer"],
                                     "currency": act["currency"], "input": 0, "output": 0, "free": True,
                                     "note": ":free 自动同步", "verified_at": str(TODAY), "source": tag})
                    if keep != prices:
                        prices = keep
                        prices_dirty = True
                        summary.append(f"UPDATE {sid} → prices.json: 免费模型行已同步（{min(act.get('free_top',3), len(free))} 行）")
            st["hash"], st["len"] = h, len(text)
            continue

        # ---- 哈希监控源：两次观测确认制 ----
        # 页面「每次请求都在变」（计数器/轮换 banner/时间戳）会永远误报；只有同一新哈希
        # 连续出现 confirm_runs 次才认定为真实变更。确认前的观测仍续验证戳（抖动≠过期）。
        if styp == "watch":
            prev = st.get("hash")
            st["len"] = len(text)
            confirm_runs = src.get("confirm_runs", 2)
            if prev is None:
                st["hash"] = h
                summary.append(f"BASE  {sid}: 首次抓取，建立基线")
                bump(src.get("deals", []), sid)
                continue
            if h == prev:
                st.pop("pending", None)
                bump(src.get("deals", []), sid)
                summary.append(f"OK    {sid}: 未变化，{len(src.get('deals', []))} 条已自动续期")
                continue
            pend = st.get("pending") or {}
            if pend.get("hash") == h:
                pend["seen"] = pend.get("seen", 1) + 1
                if pend["seen"] >= confirm_runs:
                    # 确认真的变了：降级相关 deal（写明原因）+ 重设基线；复核队列会自动展示它们
                    st["hash"] = h
                    st.pop("pending", None)
                    for did in src.get("deals", []):
                        d = by_id.get(did)
                        if d and d.get("published", True) and d.get("verify_status") != "expired":
                            d["verify_status"] = "stale"
                            d["stale_reason"] = f"源 {sid} 页面于 {TODAY} 变更（连续 {pend['seen']} 次观测一致）"
                            deals_dirty = True
                    summary.append(f"CHANGED {sid}: 连续 {pend['seen']} 次观测到新内容，{len(src.get('deals', []))} 条降级待复核")
                else:
                    st["pending"] = pend
                    bump(src.get("deals", []), sid)
                    summary.append(f"WAIT  {sid}: 新哈希首次复现（{pend['seen']}/{confirm_runs}），待下次确认")
            else:
                st["pending"] = {"hash": h, "seen": 1}
                bump(src.get("deals", []), sid)
                summary.append(f"WAIT  {sid}: 内容与基线不同（可能抖动），进入待确认")
            continue

        # ---- RSS 源：关键词过滤 → 只进草稿 ----
        if styp == "rss":
            inc, exc = src.get("include", []), src.get("exclude", [])
            items = re.findall(r"<item>(.*?)</item>", text, re.S)
            added = 0
            for it in items:
                title_m = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", it, re.S)
                link_m = re.search(r"<link>(.*?)</link>", it, re.S)
                if not (title_m and link_m):
                    continue
                title = htmlmod.unescape(title_m.group(1).strip())
                link = link_m.group(1).strip()
                tid_m = re.search(r"/t/[^/]+/(\d+)", link)
                if not tid_m:
                    continue
                did = f"ld-{tid_m.group(1)}"
                if any(x in title for x in exc) or not any(x in title.lower() for x in inc):
                    continue
                if did in by_id:
                    continue
                deals.append({
                    "id": did, "provider": "Linux.do 线索", "category": "reseller", "type": "limited_promo",
                    "value": title[:90], "region": "cn", "url": link,
                    "verify_status": "stale", "verified_at": NOW_ISO, "difficulty": 2, "published": False,
                    "notes": "🤖 RSS 自动抓取草稿：人工核实官方来源后再发布；命中黑名单的多号/合租类已过滤",
                })
                by_id[did] = deals[-1]
                added += 1
            if added:
                deals_dirty = True
                summary.append(f"DRAFT {sid}: 新增 {added} 条草稿（黑名单已过滤 {len(exc)} 类风险词）")
            st["hash"], st["len"] = h, len(text)
            continue

    # ---- 规则引擎 1：截止日自动失效 ----
    for d in deals:
        dl = d.get("deadline")
        if dl and d.get("verify_status") != "expired":
            try:
                if datetime.date.fromisoformat(dl) < TODAY:
                    d["verify_status"] = "expired"
                    d["stale_reason"] = f"截止 {dl} 已过（{TODAY} 自动标失效）"
                    deals_dirty = True
                    summary.append(f"EXPIRE {d['id']}: deadline {dl} 已过")
            except ValueError:
                pass

    # ---- 规则引擎 2：超期未复核自动降级 ----
    stale_days = cfg.get("stale_days", 14)
    for d in deals:
        if d.get("verify_status") != "verified" or not d.get("published", True):
            continue
        try:
            age = (NOW - datetime.datetime.fromisoformat(d["verified_at"].replace("Z", "+00:00"))).days
        except Exception:
            continue
        if age > stale_days:
            d["verify_status"] = "stale"
            d["stale_reason"] = f"超过 {stale_days} 天未被任何数据源自动续期（源失联或未配置监控）"
            deals_dirty = True
            summary.append(f"STALE {d['id']}: {age} 天未复核")

    # ---- 复核队列 = 当前状态的实时视图（从 deals + 源健康推导，人工修复即自动出队）----
    queue = []
    for d in deals:
        if d.get("published", True) and d.get("verify_status") == "stale":
            queue.append(f"- **待复核** `{d['id']}`（{d['provider']}）：{d.get('stale_reason', '原因见 sync 运行摘要')} → 核实后更新 value/notes 并改 `verify_status:\"verified\"`")
        elif not d.get("published", True) and str(d.get("notes", "")).startswith("🤖"):
            queue.append(f"- **RSS 草稿** `{d['id']}`：{d.get('value', '')[:60]} <{d.get('url', '')}> → 核实官方来源后改 `published:true` 并补 category/provider；不实就删条目")
    for sid, st in sorted(src_state.items()):
        if st.get("fail_streak", 0) >= 3:
            queue.append(f"- **源失联** `{sid}`：连续 {st['fail_streak']} 次失败（{st.get('last_error', '')}）→ 检查 URL 是否失效，或从 tools/sources.json 移除")

    # ---- 写回 ----
    if DRY:
        print("== DRY RUN，不写文件 ==")
    else:
        if deals_dirty:
            dump_lines(ROOT / "deals.json", deals)
        if prices_dirty:
            dump_lines(ROOT / "prices.json", prices)
        state["generated_at"] = NOW_ISO
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (ROOT / "review-queue.md").write_text(
            "# 人工复核队列（sync.py 每次运行自动重算；人工修复对应条目后自动消失）\n\n"
            "机器不能判断的事都在这里：官方页面有变、来源失联、超期未复核、RSS 草稿。\n"
            "处理方式：改 deals.json 对应条目（核实→更新 value→verify_status:\"verified\"；不实→删）。\n\n"
            + ("\n".join(queue) if queue else "✅ 当前为空 —— 没有待人工处理的事项") + "\n",
            encoding="utf-8")
        rc = subprocess.run([sys.executable, str(ROOT / "tools" / "check.py")]).returncode
        if rc != 0:
            print("!! check.py 校验失败，数据未提交（回滚请看 git diff）")
            return rc

    print(f"== sync {NOW_ISO} ==")
    pub = sum(1 for d in deals if d.get("published", True))
    ver = sum(1 for d in deals if d.get("published", True) and d.get("verify_status") == "verified")
    auto = sum(1 for d in deals if d.get("verify_by") == "auto")
    print(f"deals {len(deals)}（发布 {pub} / 验证 {ver} / 自动核验 {auto}）| prices {len(prices)} | 源 {len(cfg['sources'])} | 待复核事项 {len(queue)}")
    for s in summary:
        print(" ", s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
