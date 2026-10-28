#!/usr/bin/env python3
"""公众号羊毛专属管线（零 token）——独立于通用找源，专注盯防公众号。

每轮动作（反爬友好：单查询、低频、cookie 会话）：
1. 轮换查询词（状态文件记轮次）→ 搜狗微信搜索
2. 新文章检测（状态文件去重）→ 新文章写告警 data-research/weixin_alerts.md
3. 滚雪球：抓种子文章页，提取账号名/文内互链 → 种子库自增长
4. 账号名册：data-research/weixin_accounts.json（发现的羊毛号台账）

状态文件：data-research/weixin_state.json（seen 集合/轮次/种子库）
"""
from __future__ import annotations
import json, re, sys, time, urllib.request, http.cookiejar
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DR = ROOT / "data-research"
STATE = DR / "weixin_state.json"
ALERTS = DR / "weixin_alerts.md"
ACCOUNTS = DR / "weixin_accounts.json"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"

QUERIES = ["token 免费额度", "AI 羊毛 折扣码", "大模型 领额度", "白嫖 API",
           "GLM 免费", "Coding Plan 折扣", "AI 编程 白嫖", "注册送 tokens",
           "大模型 体验卡", "Claude Code 折扣", "免费 claude", "API 中转 折扣",
           "模型 免费 送", "agent 免费 额度", "算力 白嫖", "inference 免费"]
SEEDS_MIN = ["https://mp.weixin.qq.com/s/7mSCNv7ZumV8urTr37eKrg"]  # 神秘喵星人

_CJ = http.cookiejar.CookieJar()
_OP = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_CJ))
_OP.addheaders = [("User-Agent", UA)]

def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

def fetch(url: str, referer: str = "") -> str:
    try:
        h = {"User-Agent": UA}
        if referer: h["Referer"] = referer
        return _OP.open(urllib.request.Request(url, headers=h), timeout=12).read(600_000).decode("utf-8", "ignore")
    except Exception:
        return ""

def load_state() -> dict:
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except Exception:
        return {"turn": 0, "seen": {}, "seeds": SEEDS_MIN, "accounts": {}}

def save_state(s: dict):
    STATE.write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")

def article_meta(html: str) -> tuple[str, str]:
    m = re.search(r'var msg_title = \'([^\']+)\'', html) or re.search(r"<title>([^<]+)", html)
    title = (m.group(1).strip() if m else "")[:80]
    n = re.search(r'var nickname = \'([^\']+)\'', html) or re.search(r'js_name[^>]*>\s*([^<]+)', html)
    return title, (n.group(1).strip() if n else "")

def sogou_search(query: str) -> list[dict]:
    h = fetch("https://weixin.sogou.com/weixin?type=2&query=" + urllib.request.quote(query))
    if not h or "antispider" in h.lower():
        return []
    out = []
    for m in re.finditer(r'<h3>[\s\S]*?<a[^>]*href="(/link\?url=[^"]+)"[^>]*>([\s\S]*?)</a>', h):
        out.append({"sogou_link": "https://weixin.sogou.com" + "".join(m.group(1).split()).replace("&amp;", "&"),
                    "title": re.sub(r"<[^>]+>", "", m.group(2)).strip()[:80]})
    return out[:8]

def resolve(link: str) -> str:
    try:
        body = _OP.open(urllib.request.Request(link, headers={"Referer": "https://weixin.sogou.com/"}),
                        timeout=12).read().decode("utf-8", "ignore")
    except Exception:
        return ""
    frag = "".join(re.findall(r"url \+= '([^']*)'", body)).replace("@", "")
    if frag.startswith("http"):
        return frag
    m = re.search(r'window\.location\.replace\("([^"]+)"\)', body)
    return m.group(1) if m else ""

def main() -> int:
    s = load_state()
    s["turn"] = s.get("turn", 0) + 1
    new_alerts: list[str] = []
    seen = s.setdefault("seen", {})

    # A) 滚雪球：抓一个种子，长新种子+账号
    seed = s["seeds"][s["turn"] % len(s["seeds"])]
    html = fetch(seed)
    if html:
        title, account = article_meta(html)
        if account:
            acc = s.setdefault("accounts", {})
            acc[account] = {"last_title": title, "last_seen": now()}
            ACCOUNTS.write_text(json.dumps(acc, ensure_ascii=False, indent=1), encoding="utf-8")
        inner = list(dict.fromkeys(re.findall(r'mp\.weixin\.qq\.com/s/[A-Za-z0-9_-]{10,}', html)))
        for u in inner:
            if u not in s["seeds"] and len(s["seeds"]) < 60:
                s["seeds"].append(u)
        if title and title not in seen:
            seen[title] = {"account": account, "first_seen": now(), "via": "snowball"}
            new_alerts.append(f"🌱 种子更新 [{account or '未知号'}] {title}")

    # B) 轮换查询（内置节流：每 4 轮才敲一次搜狗——15 分钟节奏下≈每小时 1 查询，反爬安全）
    results = []
    resolved = ""
    q = ""
    do_search = (s["turn"] % 4 == 1)
    if do_search:
        q = QUERIES[s["turn"] % len(QUERIES)]
        results = sogou_search(q)  # 搜狗查询
        time.sleep(2)
        resolved = ""
        if results:
            resolved = resolve(results[0]["sogou_link"])
            time.sleep(2)
        if results and resolved:
            art = fetch(resolved)
            if art:
                t2, acc2 = article_meta(art)
                if acc2:
                    acc = s.setdefault("accounts", {})
                    acc[acc2] = {"last_title": t2, "last_seen": now()}
                r0 = results[0]
                if r0["title"] and r0["title"] not in seen:
                    seen[r0["title"]] = {"account": acc2 or r0.get("account", ""), "first_seen": now(), "via": f"搜狗:{q}"}
                    new_alerts.append(f"🆕 公众号新文 [{acc2 or '?'}] {r0['title']} → {resolved[:60]}")
    # C) 搜狗结果标题层去重告警
    for r in results[1:5]:
        if r["title"] and r["title"] not in seen:
            seen[r["title"]] = {"account": "", "first_seen": now(), "via": f"搜狗标题:{q}"}
            new_alerts.append(f"📰 标题雷达 [{q}] {r['title']}")

    # D) 告警落盘
    if new_alerts:
        with ALERTS.open("a", encoding="utf-8") as f:
            f.write(f"\n## {now()}（轮 {s['turn']}，查询：{q}）\n" + "\n".join(f"- {a}" for a in new_alerts) + "\n")
        print(f"⚠️ {len(new_alerts)} 条新告警已写入 weixin_alerts.md")
    else:
        print("本轮无新文章（搜狗缓存或已见）")
    save_state(s)
    accs = s.get("accounts", {})
    print(f"轮 {s['turn']} | 种子 {len(s['seeds'])} | 名册 {len(accs)} 号: {list(accs)[-5:]}")
    print(f"NEW_ALERTS={len(new_alerts)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
