#!/usr/bin/env python3
"""公众号信源发现器（零 token）：搜狗微信搜索 + 文章页滚雪球。
搜狗 robots 仅限制其自家蜘蛛；本工具低频查询（每关键词 1 请求 + 限量重定向解析）。
产出：data-research/weixin_articles.json（文章/账号发现记录）。"""
from __future__ import annotations
import json, re, sys, time, urllib.request, http.cookiejar
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data-research" / "weixin_articles.json"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
# 发现用查询词（按周轮换，可在队尾追加）
# 按周轮换：第2周批次（每周巡检时更换以避开搜狗缓存）
# 按周轮换：第3周批次
# 按周轮换：第4周批次
# 按周轮换：第5周批次
QUERIES = ["模型 免费 送", "agent 免费 额度", "算力 白嫖", " inference 免费"]
SNOWBALL_SEEDS = [  # 已知文章：从文内互链滚雪球
    "https://mp.weixin.qq.com/s/7mSCNv7ZumV8urTr37eKrg",
]

# 带 cookie 的会话级 opener（搜狗 /link 解析必需：SUID/ABTEST 预热）
_CJ = http.cookiejar.CookieJar()
_OP = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_CJ))
_OP.addheaders = [("User-Agent", UA)]

def fetch(url: str, referer: str = "") -> tuple[int, str]:
    try:
        h = {"User-Agent": UA}
        if referer:
            h["Referer"] = referer
        req = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, r.read(800_000).decode("utf-8", "ignore")
    except Exception:
        return 0, ""

def txt(h: str) -> str:
    t = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"\s+", " ", t)

def sogou(query: str) -> list[dict]:
    try:
        r = _OP.open("https://weixin.sogou.com/weixin?type=2&query=" + urllib.request.quote(query), timeout=12)
        st, h = r.status, r.read().decode("utf-8", "ignore")
    except Exception:
        st, h = 0, ""
    out = []
    if st != 200 or "antispider" in h.lower():
        print(f"[warn] 搜狗查询受限或失败: {query} (HTTP {st})")
        return out
    # 结果块：标题 + 公众号名 + /link 重定向
    for m in re.finditer(r'<h3>[\s\S]*?<a[^>]*href="(/link\?url=[^"]+)"[^>]*>([\s\S]*?)</a>[\s\S]*?</h3>([\s\S]*?)(?=<h3>|$)', h):
        link, title_html, block = m.group(1), m.group(2), m.group(3)
        title = re.sub(r"<[^>]+>", "", title_html).strip()
        acc = re.search(r"click_under[\s\S]*?>([^<]+)<", block) or re.search(r"公众号[^>]*>[\s\S]*?>([^<]{2,20})<", block)
        out.append({"query": query, "title": title[:60], "account": (acc.group(1).strip() if acc else ""),
                    "sogou_link": "https://weixin.sogou.com" + link.replace("&amp;", "&")})
    return out[:10]

def resolve(sogou_link: str) -> str:
    """解析搜狗 /link 加密跳转：cookie 预热 + Referer + JS 片段拼装（2026-10-28 实测 3/3）。"""
    try:
        clean = "".join(sogou_link.split()).replace("&amp;", "&")
        req = urllib.request.Request("https://weixin.sogou.com" + clean,
                                     headers={"Referer": "https://weixin.sogou.com/"})
        body = _OP.open(req, timeout=12).read().decode("utf-8", "ignore")
    except Exception:
        return ""
    frag = "".join(re.findall(r"url \+= '([^']*)'", body)).replace("@", "")
    if frag.startswith("http"):
        return frag
    m = re.search(r'window\.location\.replace\("([^"]+)"\)', body)
    return m.group(1) if m else ""

def snowball(seed: str) -> dict:
    st, h = fetch(seed)
    info = {"seed": seed, "status": st, "account": "", "inner_links": [], "titles": []}
    if st != 200:
        return info
    m = re.search(r'var nickname[^=]*=\s*[\"\x27]([^\"\x27]+)', h) or re.search(r'js_name[^>]*>\s*([^<]+)', h)
    if m:
        info["account"] = m.group(1).strip()
    info["inner_links"] = list(dict.fromkeys(re.findall(r'mp\.weixin\.qq\.com/s/[A-Za-z0-9_-]{10,}', h)))[:10]
    info["titles"] = [t[:50] for t in re.findall(r"title:\s*'([^']{6,60})'", h)][:6]
    return info

def main() -> int:
    try:
        _OP.open("https://weixin.sogou.com/", timeout=10)  # cookie 预热（SUID/ABTEST）
    except Exception:
        pass
    articles: list[dict] = []
    for q in QUERIES:
        res = sogou(q)
        articles += res
        print(f"[sogou] {q}: {len(res)} 条结果")
        time.sleep(2.5)
    # 解析 1 条真实地址（多查询连发触发搜狗反爬，每轮限 1 条）
    if articles:
        articles[0]["wx_url"] = resolve(articles[0]["sogou_link"])
        print(f"[resolve] {'✅ ' + articles[0]['wx_url'][:60] if articles[0]['wx_url'] else '未解析（反爬或无结果）'}")
    # 滚雪球
    snowballs = []
    for s in SNOWBALL_SEEDS:
        sb = snowball(s)
        snowballs.append(sb)
        print(f"[snowball] {sb.get('account')} : 文内互链 {len(sb['inner_links'])} / 标题 {len(sb['titles'])}")
        time.sleep(2.0)
    data = {"generated_at": datetime_utc(), "sogou_results": articles, "snowballs": snowballs}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    accounts = sorted({a["account"] for a in articles if a["account"]})
    print(f"\n发现账号 {len(accounts)} 个: {accounts[:12]}")
    print(f"记录 {len(articles)} 篇文章 → {OUT.name}")
    return 0

def datetime_utc() -> str:
    import datetime as _d
    return _d.datetime.now(_d.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

if __name__ == "__main__":
    sys.exit(main())
