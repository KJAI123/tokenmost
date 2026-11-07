#!/usr/bin/env python3
"""freecloud 挖矿器 v2 (freecloud_expand.py) —— 目标 3000+ 免费云信源池

三段递归挖矿（「源里挖源」）：
  W1 直挖聚合页/聚合仓（free-for-dev、LowEndBox 站点图、中文聚合…）
  W2 GitHub 搜索 API 找更多聚合仓 → 挖 README
  W3 递归：池内所有疑似聚合仓的 github 链接 → 挖其 README（深度放大）
  全部候选并发探活（HEAD→GET 兜底），累积进 freecloud_candidates.json（旧候选永不丢失）
- 候选只是候选，不自动入盯防表；分类 official/doc/repo/article 供人工挑选
- 零 LLM token

用法:
    python3 data-research/freecloud/freecloud_expand.py [--target 3000]
"""
from __future__ import annotations

import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCES = HERE / "freecloud_sources.json"
POOL = HERE / "freecloud_candidates.json"
UA = "tokenmost-freecloud-expand/0.2 (+https://tokenmost.com; free-tier research)"
THREADS = 16

CLOUD_HINTS = re.compile(
    r"(?i)(vps|vds|dedicated|hosting|cloud|server|virtual machine|\bvm\b|gpu|sandbox|compute|"
    r"\bide\b|paas|faas|serverless|docker|container|kubernetes|k8s|firecracker|microvm|shell|"
    r"workspace|notebook|colab|trial|free[- ]?tier|always[- ]?free|database|\bdb\b|storage|"
    r"\bcdn\b|\bdns\b|\bci\b|\bcd\b|devops|domain|ssl|certificate|uptime|monitor|"
    r"database|klient|云服务器|云主机|免费|试用|虚拟主机|建站|域名|弹性云)")

EXCLUDE = re.compile(
    r"(?i)(twitter\.com|x\.com/|youtube|facebook|instagram|tiktok|discord\.gg|t\.me/|reddit\.com/r/|"
    r"openai\.com|anthropic\.com|claude\.ai|chatgpt|"
    r"casino|bet\b|porn|nsfw|xxx|onlyfans|"
    r"spotify|netflix|coupon|sample|freebie|giveaway(?!.*vps)|steam|game\b|"
    r"shields\.io|badgen\.net|badge|img\.shields|simpleicons|travis-ci\.org|circleci\.com|"
    r"\.png$|\.jpg$|\.jpeg$|\.gif$|\.svg$|\.webp$|\.ico$|\.zip$|\.pdf$)")

# 明确允许（即使文字不带 cloud 词）
FORCE_HINTS = re.compile(r"(?i)(free|gratis|kostenlos|darmowy|免费|试用|赠)")

LINK_RE = re.compile(r"\[([^\]]{2,140})\]\((https?://[^)\s]+?)\)")
HTML_LINK_RE = re.compile(r'<a[^>]+href="(https?://[^"]+)"[^>]*>(.*?)</a>', re.S | re.I)
TAG_STRIP = re.compile(r"<[^>]+>")
REPO_RE = re.compile(r"https://github\.com/([\w.-]+)/([\w.-]+)/?$")
SITEMAP_LOC = re.compile(r"<loc>([^<]+)</loc>")

MINING = [
    {"name": "free-for-dev 总表", "url": "https://raw.githubusercontent.com/ripienaar/free-for-dev/master/README.md"},
    {"name": "LowEndBox 首页+免费分类", "url": "https://lowendbox.com/"},
    {"name": "LowEndBox 免费VPS分类", "url": "https://lowendbox.com/category/free-vps/"},
    {"name": "LowEndTalk freevps 版", "url": "https://www.lowendtalk.com/categories/freevps"},
    {"name": "vpsbros 免费清单", "url": "https://www.vpsbros.com/%E5%85%8D%E8%B4%B9vps"},
    {"name": "free-for-bots", "url": "https://raw.githubusercontent.com/lingonslask/free-for-bots/master/README.md"},
    {"name": "itsfree.dev（聚合站）", "url": "https://itsfree.dev/"},
    {"name": "cloudcredits.io（云试用金聚合站）", "url": "https://cloudcredits.io/"},
    {"name": "free-for.dev（站点版）", "url": "https://free-for.dev/"},
    {"name": "cloud-gpus.com（GPU 云对比雷达·爬取战果反哺）", "url": "https://cloud-gpus.com"},
    {"name": "cheapvpsfinder.com（低价 VPS 雷达·爬取战果反哺）", "url": "https://cheapvpsfinder.com"},
    {"name": "vps234 免费VPS（中文测评站）", "url": "https://www.vps234.com/free-vps/"},
]

GH_SEARCH_QUERIES = [
    "awesome+free+tier+cloud",
    "free+vps+list",
    "awesome+free+hosting",
    "free+cloud+trial+list",
    "free+shell+account+list",
    "awesome+paas",
    "free+kubernetes+sandbox",
    "awesome+cloud+credits",
    "awesome+student+developer+pack",
    "free+serverless+hosting",
    "free+database+hosting+list",
    "free+tier+tracking",
    "free+vps+2026",
    "cheap+vps+deals+list",
    "awesome+vagrant+boxes",
    "free+docker+hosting",
    "free+cloud+vps",
    "awesome+free+paas",
    "free+hosting+2026",
    "aws+activate+credits+list",
    "free+server+hosting",
    "awesome+free+services",
]
GH_TOPICS = ["free-tier", "free-cloud", "free-vps", "free-hosting", "student-pack",
             "free-resources", "awesome-free", "cloud-credits", "freebies", "paas",
             "free-shell", "trial-credits", "serverless", "aws-credits", "free-credits"]


def gitee_repos() -> list[str]:
    """Gitee 搜索：中文免费云聚合仓。"""
    repos: list[str] = []
    for q in ["免费云", "免费vps", "白嫖云服务器", "免费主机", "免费服务器", "云电脑", "免费算力"]:
        try:
            req = urllib.request.Request(
                f"https://gitee.com/api/v5/search/repositories?q={urllib.parse.quote(q)}&sort=stars_count&per_page=10",
                headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode("utf-8"))
            for it in data:
                full = it.get("full_name") or it.get("path_with_namespace") or ""
                if full and (it.get("stargazers_count") or 0) >= 5:
                    repos.append(f"https://gitee.com/{full}/raw/master/README.md")
            print(f"[gt]  {q} → 累计 {len(repos)}")
        except Exception as e:
            print(f"[gt!] {q} {type(e).__name__}")
    return sorted(set(repos))


def crawl_hot(cap: int = 150) -> list[str]:
    """W6：从爬取战果里挑高信号页反哺挖矿（聚合文章里挖源）。"""
    files = sorted((HERE / "freecloud_crawl").glob("crawl-*.jsonl"))
    if not files:
        return []
    urls: list[tuple[int, str]] = []
    for f in files:
        for line in f.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("n_signal", 0) >= 8 and r.get("cat") in ("article", "official"):
                urls.append((r["n_signal"], r["url"]))
    urls = sorted(set(urls), reverse=True)
    return [u for _, u in urls[:cap]]


def fetch(url: str, timeout: int = 20) -> str:
    """urllib 直抓，被挡（403/000）时 fallback pagesift 浏览器内核。"""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", "ignore")
    except Exception as e:
        if isinstance(e, urllib.error.HTTPError) and e.code in (403, 405, 429):
            raise
        try:
            import pagesift
            d = pagesift.scrape(url, pagesift.ScrapeOptions(timeout=25000))
            if d.success and d.markdown:
                return d.markdown
        except Exception:
            pass
        raise


def norm(url: str) -> str:
    u = url.strip().rstrip("/")
    p = urllib.parse.urlsplit(u)
    q = [(k, v) for k, v in urllib.parse.parse_qsl(p.query) if not k.lower().startswith(("utm_", "ref", "fbclid"))]
    return urllib.parse.urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path, urllib.parse.urlencode(q), ""))


def classify(url: str, text: str) -> str:
    if "github.com" in url or "gitlab.com" in url or "gitee.com" in url:
        return "repo"
    if "docs." in urllib.parse.urlsplit(url).netloc or "/docs" in url:
        return "doc"
    if re.search(r"(?i)(pricing|free|trial|promo|tier|plans?|signup|register|gratis|kostenlos)", url) \
            or re.search(r"免费|试用|白嫖", text):
        return "official"
    return "article"


def mine_text(md: str, found_in: str, existing: set[str], seen: set[str]) -> list[dict]:
    out: list[dict] = []

    def add(text: str, url: str) -> None:
        url = norm(url)
        if url in seen or url in existing:
            return
        if EXCLUDE.search(url) or EXCLUDE.search(text):
            return
        if not (CLOUD_HINTS.search(text) or CLOUD_HINTS.search(url) or FORCE_HINTS.search(text)):
            return
        seen.add(url)
        out.append({"url": url, "text": re.sub(r"\s+", " ", text.strip())[:120],
                    "cat": classify(url, text), "found_in": found_in})

    for text, url in LINK_RE.findall(md):
        add(text, url)
    for url, raw_text in HTML_LINK_RE.findall(md):
        text = TAG_STRIP.sub(" ", raw_text)
        if len(text.strip()) >= 2:
            add(text, url)
    return out


def mine_urls(urls: list[str], label: str, existing: set[str], seen: set[str]) -> list[dict]:
    """并发抓一批页面/README 抽链接。"""
    def one(u: str):
        try:
            return u, fetch(u)
        except Exception:
            return u, None

    cands: list[dict] = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        for u, body in ex.map(one, urls):
            if body:
                n = mine_text(body, label, existing, seen)
                cands.extend(n)
                print(f"[ok]  {u[:80]} → {len(n)} 新候选")
    return cands


def gh_repos() -> list[str]:
    """GitHub 搜索 API：聚合仓发现。"""
    repos: dict[str, str] = {}
    headers = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    queries = [f"search/repositories?q={q}&sort=stars&per_page=15" for q in GH_SEARCH_QUERIES]
    queries += [f"search/repositories?q=topic:{t}&sort=stars&per_page=15" for t in GH_TOPICS]
    for q in queries:
        try:
            req = urllib.request.Request(f"https://api.github.com/{q}", headers=headers)
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode("utf-8"))
            for it in data.get("items", []):
                full = it.get("full_name", "")
                stars = it.get("stargazers_count", 0)
                if it.get("fork") or stars < 30:
                    continue
                repos[full] = f"{stars}"
            print(f"[gh]  {q[:60]} → 累计 {len(repos)} 仓")
        except Exception as e:
            print(f"[gh!] {q[:60]} {type(e).__name__}")
    return [f"https://raw.githubusercontent.com/{full}/HEAD/README.md" for full in repos]


def lowendbox_sitemap(parts_max: int = 8, cap: int = 1200) -> list[str]:
    """LowEndBox 文章站点图（免费/低价 VPS 文章=情报源）。"""
    urls: list[str] = []
    try:
        idx = fetch("https://lowendbox.com/wp-sitemap.xml")
        parts = [u for u in SITEMAP_LOC.findall(idx) if "posts-post" in u][:parts_max]
        for p in parts:
            body = fetch(p)
            for u in SITEMAP_LOC.findall(body):
                if "lowendbox.com/blog/" in u:
                    urls.append(u)
                if len(urls) >= cap:
                    return urls
    except Exception as e:
        print(f"[leb!] sitemap {type(e).__name__}")
    return urls


def probe(items: list[dict]) -> None:
    def one(c: dict) -> None:
        for method in ("HEAD", "GET"):
            try:
                req = urllib.request.Request(c["url"], headers={"User-Agent": UA}, method=method)
                with urllib.request.urlopen(req, timeout=12) as r:
                    c["status"] = r.status
                    return
            except Exception as e:
                code = getattr(e, "code", None)
                if method == "GET":
                    c["status"] = code if code else f"{type(e).__name__}"
                elif code not in (405, 403, 429):
                    c["status"] = code if code else f"{type(e).__name__}"
                    return

    with ThreadPoolExecutor(max_workers=THREADS) as ex:
        list(ex.map(one, items))


def load_pool() -> dict:
    if POOL.exists():
        try:
            return json.loads(POOL.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"updated_at": None, "items": {}}


def save_pool(pool: dict) -> None:
    pool["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    POOL.write_text(json.dumps(pool, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    pool = load_pool()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def flush(cands: list[dict]) -> int:
        added = 0
        for c in cands:
            if c["url"] in pool["items"]:
                continue
            c["added_at"] = now
            pool["items"][c["url"]] = c
            added += 1
        return added

    existing = {s["url"].rstrip("/") for s in json.loads(SOURCES.read_text(encoding="utf-8"))["sources"]}
    existing |= {u.rstrip("/") for u in pool["items"]}
    seen: set[str] = set()

    # W1 直挖聚合页
    print("== W1 直挖聚合页 ==")
    cands = mine_urls([m["url"] for m in MINING], "W1-aggregate", existing, seen)
    leb = lowendbox_sitemap(parts_max=45, cap=6000)
    print(f"[leb] 站点图文章 {len(leb)} 篇")
    for u in leb:
        if u not in seen and u.rstrip("/") not in existing:
            seen.add(u)
            cands.append({"url": u, "text": "LowEndBox 文章", "cat": "article", "found_in": "W1-leb-sitemap"})
    added = flush(cands)
    print(f"W1 +{added}（池 {len(pool['items'])}）")
    save_pool(pool)

    # W2 GitHub 搜索仓 README
    print("== W2 GitHub 聚合仓 ==")
    gh = gh_repos()
    gt = gitee_repos()
    added = flush(mine_urls(gh + gt, "W2-github", existing, seen))
    print(f"W2 +{added}（池 {len(pool['items'])}）")
    save_pool(pool)

    # W3 递归挖池内全部 github 仓（放宽过滤，cap 400）
    print("== W3 递归挖仓 ==")
    repos: list[str] = []
    for c in pool["items"].values():
        m = REPO_RE.match(c["url"])
        if m and not c["url"].lower().endswith(("/readme", "/readme.md")):
            repos.append(f"https://raw.githubusercontent.com/{m.group(1)}/{m.group(2)}/HEAD/README.md")
    repos = sorted(set(repos))[:400]
    print(f"递归目标仓 {len(repos)} 个")
    added = flush(mine_urls(repos, "W3-recursive", existing, seen))
    print(f"W3 +{added}（池 {len(pool['items'])}）")
    save_pool(pool)

    # W6 爬取战果反哺：高信号聚合页再挖一层
    print("== W6 高信号页反哺挖矿 ==")
    hot = crawl_hot()
    print(f"高信号页 {len(hot)} 个")
    added = flush(mine_urls(hot, "W6-crawl-hot", existing, seen))
    print(f"W6 +{added}（池 {len(pool['items'])}）")
    save_pool(pool)

    # 池优化：'?' 分类回填
    for c in pool["items"].values():
        if "cat" not in c:
            c["cat"] = classify(c["url"], c.get("text", ""))
    save_pool(pool)

    # 探活（只探新条目）
    fresh = [c for c in pool["items"].values() if "status" not in c]
    print(f"== 探活 {len(fresh)} 条 ==")
    probe(fresh)
    ok = sum(1 for c in fresh if c.get("status") == 200)
    save_pool(pool)

    total = len(pool["items"])
    ok_all = sum(1 for c in pool["items"].values() if c.get("status") == 200)
    cats = {}
    for c in pool["items"].values():
        cats[c.get("cat", "?")] = cats.get(c.get("cat", "?"), 0) + 1
    print(f"\n== 池总量 {total}（200 可达 {ok_all}）分类 {cats}")
    print(f"本轮新探活: {len(fresh)}，200×{ok}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
