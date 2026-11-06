#!/usr/bin/env python3
"""freecloud 采集器 —— 薅免费云服务器管线 (freecloud_harvest.py)

盯防对象：免费云服务器/云电脑/Agent 沙盒的官方免费档（vCPU/GiB/快照/流量/试用金）。
- 采集内核 = pagesift（Rust，自动遵守 robots.txt + 每站限速 + 干净 Markdown 抽取）
- 全程零 LLM token；指纹 diff（命中上下文集合 sha256），变化才告警，首跑建基线
- 输出：freecloud/harvest/freecloud-YYYY-MM-DD.md + latest.json + state.json
- --selftest 离线自检；--only ID 过滤；PAGESIFT_CONCURRENCY 可调并发（默认 4）

用法:
    python3 data-research/freecloud/freecloud_harvest.py              # 全量
    python3 data-research/freecloud/freecloud_harvest.py --only instabox
    python3 data-research/freecloud/freecloud_harvest.py --selftest   # 离线自检
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCES = HERE / "freecloud_sources.json"
OUTDIR = HERE / "harvest"
STATE = HERE / "state.json"

# 数额类关键词：只抓「数字+单位/配额词」的上下文，营销措辞漂移不误报
DEFAULT_PATTERNS = [
    r"(?i)\b\d+(?:\.\d+)?\s*(?:vCPUs?|GiBs?|MiBs?|GBs?|TBs?|OCPUs?)\b[^.\n]{0,60}",
    r"(?i)(?:always[- ]free|forever[- ]free|永久免费|长期免费)[^.\n]{0,50}",
    r"(?i)\bfree\s+(?:tier|plan|trial|credits?|month|year)[^.\n]{0,60}",
    r"免费(?:试用|额度|套餐|赠送)[^。\n]{0,50}",
    r"(?i)(?:credits?|试用金|赠金|赠送)[^.\n]{0,60}",
    r"(?i)(?:egress|transfer|traffic|流量|出网)[^.\n]{0,60}",
    r"(?i)(?:idle|suspend|pause|闲置|暂停)[^.\n]{0,50}",
    r"(?i)(?:per month|/month|/mo|每月)[^.\n]{0,50}",
]

WS_RE = re.compile(r"\s+")


def extract(text: str, patterns: list[str]) -> list[dict]:
    """跑关键词，返回 [{m: 命中词, ctx: 上下文窗口}]（去重按上下文）。"""
    hits: list[dict] = []
    seen: set[str] = set()
    for pat in patterns:
        try:
            rx = re.compile(pat)
        except re.error:
            continue
        for m in rx.finditer(text):
            s = max(0, m.start() - 100)
            ctx = WS_RE.sub(" ", text[s:m.end() + 100]).strip()
            if len(ctx) > 8 and ctx not in seen:
                seen.add(ctx)
                hits.append({"m": m.group(0), "ctx": ctx})
    return hits


def fingerprint(hits: list[str]) -> str:
    """命中集合指纹：排序后整体 sha256（沿用 harvest_diff 口径）。"""
    return hashlib.sha256("\n".join(sorted(hits)).encode("utf-8")).hexdigest()


def load_state() -> dict:
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"baseline": {}}


def save_state(st: dict) -> None:
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")


def scrape_all(sources: list[dict]) -> tuple[list[dict], list[str]]:
    """pagesift 批量抓取，返回 results（与 sources 对齐）与失败 id 列表。"""
    import pagesift

    conc = int(os.environ.get("PAGESIFT_CONCURRENCY", "4"))
    opts = pagesift.ScrapeOptions(timeout=30000)  # 毫秒
    active = [s for s in sources if not s.get("disabled")]
    for s in sources:
        if s.get("disabled"):
            print(f"[skip] {s['id']}: {s.get('disabled_reason', 'disabled')}")
    urls = [s["url"] for s in active]
    results: list[dict] = [None] * len(urls)  # type: ignore
    errors: list[str] = []
    with pagesift.Scraper() as scraper:
        for doc in scraper.scrape_iter(urls, options=opts, concurrency=conc):
            src = active[doc.index]
            entry = {"id": src["id"], "name": src["name"], "url": src["url"]}
            if doc.success and doc.markdown:
                md = doc.markdown
                hits = extract(md, DEFAULT_PATTERNS + src.get("patterns", []))
                entry.update(status="ok", md_len=len(md), hits=hits)
                print(f"[ok]   {src['id']}: {len(hits)} 处命中 (md {len(md)}B)")
            else:
                code = getattr(doc, "error_code", None) or "error"
                entry.update(status="error", error=f"{code}: {getattr(doc, 'error_message', '')}")
                errors.append(src["id"])
                print(f"[err]  {src['id']}: {code}")
            results[doc.index] = entry
    return results, errors


def run(only: str | None) -> int:
    cfg = json.loads(SOURCES.read_text(encoding="utf-8"))
    sources = cfg["sources"]
    if only:
        sources = [s for s in sources if only in s["id"]]
    if not sources:
        print("no sources matched --only", only)
        return 2

    results, errors = scrape_all(sources)
    OUTDIR.mkdir(parents=True, exist_ok=True)

    st = load_state()
    changed: list[str] = []
    baseline_new: list[str] = []
    watching: list[str] = []
    pending = st.setdefault("pending", {})
    for r in results:
        if r["status"] != "ok":
            continue
        fp = fingerprint([h["ctx"] for h in r["hits"]])
        prev = st["baseline"].get(r["id"])
        if prev is None:
            baseline_new.append(r["id"])
            st["baseline"][r["id"]] = {"fp": fp, "ts": _now(), "n_hits": len(r["hits"])}
        elif prev["fp"] == fp:
            pending.pop(r["id"], None)  # 回到基线：抖动，撤销观察
        else:
            # 与基线不同：连续 2 轮同一新指纹才确认变化（防动态页漂移误报）
            p = pending.get(r["id"])
            if p and p["fp"] == fp:
                p["count"] += 1
                if p["count"] >= 2:
                    changed.append(r["id"])
                    st["baseline"][r["id"]] = {"fp": fp, "ts": _now(), "n_hits": len(r["hits"])}
                    pending.pop(r["id"], None)
            else:
                pending[r["id"]] = {"fp": fp, "ts": _now(), "count": 1}
                watching.append(r["id"])
    st["pending"] = {k: v for k, v in pending.items()}
    save_state(st)

    out = OUTDIR / f"freecloud-{date.today().isoformat()}.md"
    write_report(out, results, changed, baseline_new, watching, errors)
    (OUTDIR / "latest.json").write_text(
        json.dumps({"harvested_at": _now(), "changed": changed, "watching": watching,
                    "new_baseline": baseline_new, "errors": errors, "results": results},
                   ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n== 汇总: {len(results)} 源 | 变化 {len(changed)} | 观察中 {len(watching)} | 新基线 {len(baseline_new)} | 失败 {len(errors)}")
    if changed:
        print("!! 变化源:", ", ".join(changed))
    if watching:
        print("👀 首次偏离基线待二次确认:", ", ".join(watching))
    print("报告:", out)
    return 0


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_report(out: Path, results: list[dict], changed: list[str],
                 baseline_new: list[str], watching: list[str], errors: list[str]) -> None:
    lines = [
        f"# freecloud 采集快照 {date.today().isoformat()}",
        "",
        f"- 采集时间: {_now()}（pagesift 内核·零 LLM 参与·遵守 robots.txt·两次观测确认制）",
        f"- 源数: {len(results)} | 🔔变化: {', '.join(changed) or '无'} | 👀观察中: {', '.join(watching) or '无'} | 🌱首跑基线: {len(baseline_new)} | 失败: {', '.join(errors) or '无'}",
        "",
    ]
    for r in results:
        flag = "🔔" if r["id"] in changed else ("👀" if r["id"] in watching else ("🌱" if r["id"] in baseline_new else "  "))
        lines.append(f"## {flag} {r['name']}（{r['id']}）")
        lines.append(f"- 状态: {r['status']} | {r['url']}")
        if r["status"] == "ok":
            for h in r["hits"][:10]:
                lines.append(f"- 🔎 **{h['m']}** `{h['ctx']}`")
            if not r["hits"]:
                lines.append("- ⚠️ 0 命中——页面可能 JS 渲染或改版，需人工核 pattern")
        else:
            lines.append(f"- ❌ {r.get('error', '')}")
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")


def selftest() -> int:
    sample = """
    Free plan includes 4 vCPUs / 8 GiB per machine. Plan limits: Free 1 machine, 5 snapshots,
    idle pause fixed at 30 min. Egress 100 GiB per month included. 新用户免费试用 3 个月。
    Oracle Always Free includes Arm-based Ampere A1: 4 OCPUs and 24 GB of memory.
    Marketing copy changes all the time — none of it should trip the fingerprint.
    """
    hits = extract(sample, DEFAULT_PATTERNS)
    matched = " | ".join(h["m"] for h in hits)
    assert "4 vCPUs / 8 GiB" in matched, "数额抽取失败"
    assert "Always Free" in matched, "Always Free 抽取失败"
    assert "免费试用" in matched, "中文试用抽取失败"
    # 营销句任何词都不能成为命中锚点（上下文窗口扫到邻句不算误报）
    for word in ("Marketing", "copy", "changes", "fingerprint"):
        for h in hits:
            assert word.lower() not in h["m"].lower(), f"误报：营销词 {word} 被命中"
    fp1 = fingerprint([h["ctx"] for h in hits])
    hits2 = hits[:-1] if len(hits) > 1 else hits + [{"m": "x", "ctx": "x"}]
    assert fingerprint([h["ctx"] for h in hits2]) != fp1, "指纹应随命中集变化"
    print(f"selftest OK: {len(hits)} 命中, 指纹稳定/敏感")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="只抓 id 含该子串的源")
    ap.add_argument("--selftest", action="store_true", help="离线自检")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    try:
        return run(a.only)
    except ImportError:
        print("缺 pagesift：pip3 install --user pagesift（或用容器跑 tools/docker_cycle.sh）")
        return 1


if __name__ == "__main__":
    sys.exit(main())
