#!/usr/bin/env python3
"""信源扩展器（零 token）：源里挖源。
从 GitHub 聚合仓库 README、社区攻略帖出链中批量提取候选信源 URL，
探测可达性并分类打分，落 data-research/source_candidates.json。
全程纯标准库 + 多线程探测，不消耗任何 LLM token。"""
from __future__ import annotations
import concurrent.futures as cf
import json, re, sys, time, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data-research" / "source_candidates.json"
UA = "tokenmost-harvest/0.1 (+https://tokenmost.com; source-discovery research bot)"
TIMEOUT = 10

# 种子聚合仓库（README 里全是信源）
SEED_REPOS = [
    "mnfst/awesome-free-llm-apis",
    "guihuashaoxiang/FreeLLM-API-KeyHub",
    "yacuo/ai-coding-plan",
]
# GitHub 仓库搜索（找更多聚合仓库；未认证 10 次/分钟，够用）
GH_SEARCHES = [
    "awesome free llm api",
    "free llm api list",
    "免费 大模型 API 汇总",
    "free token llm 额度",
]
# 社区攻略帖（提取出链）
PAGE_SOURCES = [
    "https://zhuanlan.zhihu.com/p/2014053076936438015",
    "https://www.cnblogs.com/nkds/p/21203036",
    "https://developer.cloud.tencent.com/article/2712136",
    "https://blog.csdn.net/2402_84764726/article/details/158284048",
    "https://blog.liurb.org/posts/2026/01/06/free_api",
    "https://openrouter.ai/blog/tutorials/free-llm-apis-compared",
    "https://www.reddit.com/r/LocalLLaMA/comments/1sigg35/",
]
BLOCK_DOMAINS = ("twitter.com", "x.com", "youtube.com", "facebook.com", "linkedin.com",
                 "discord", "t.me", "wikipedia.org", "bilibili.com", "douyin.com",
                 "zhihu.com/career", "appstore", "play.google", "itunes")
OFFICIAL_PAT = re.compile(r"(docs?\.|/docs|/pricing|api-docs|developer\.|platform\.|console\.|/doc/|/help|open\.\w+\.com|cloud\.|\.md$)", re.I)
URL_RE = re.compile(r"https?://[^\s\"'<>\)\]\\，。；]+")

def fetch(url: str) -> tuple[int, str]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status, r.read(600_000).decode("utf-8", "ignore")
    except Exception:
        return 0, ""

def extract_urls(text: str) -> set[str]:
    out = set()
    for u in URL_RE.findall(text):
        u = u.rstrip(".,;:！？")
        low = u.lower()
        if any(b in low for b in BLOCK_DOMAINS):
            continue
        if low.startswith("https://github.com/") and low.count("/") <= 4 and "/blob/" not in low:
            out.add(u.rstrip("/"))  # 仓库主页=聚合源
            continue
        if low.startswith(("http://localhost", "https://example")):
            continue
        if len(u) < 12 or low.endswith((".png", ".jpg", ".svg", ".ico", ".gif", ".webp", ".css", ".woff2")):
            continue
        if any(ch in u for ch in "[]{}<>\"'\\ "):
            continue
        out.add(u)
    return out

def gh_api(path: str) -> dict | list | None:
    st, body = fetch("https://api.github.com" + path)
    if st != 200:
        return None
    return json.loads(body)

def collect() -> dict[str, dict]:
    pool: dict[str, dict] = {}
    def add(url: str, origin: str, kind_hint: str = ""):
        url = url.strip()
        if not url or url in pool:
            return
        kind = "repo" if url.lower().startswith("https://github.com/") and url.count("/") == 4 else \
               ("official" if OFFICIAL_PAT.search(url) else "article")
        pool[url] = {"url": url, "origin": origin, "kind": kind_hint or kind, "title": "", "status": 0}

    # 1) 种子仓库 README
    readmes: list[tuple[str, str]] = []
    for repo in SEED_REPOS:
        for br in ("main", "master"):
            st, body = fetch(f"https://raw.githubusercontent.com/{repo}/{br}/README.md")
            if st == 200 and body:
                readmes.append((f"github:{repo}", body))
                for u in extract_urls(body):
                    add(u, f"github:{repo}")
                break
    print(f"种子 README: {len(readmes)} 个")

    # 2) GitHub 搜索更多聚合仓库 → 取 README
    seen_repos = set(SEED_REPOS)
    for q in GH_SEARCHES:
        data = gh_api("/search/repositories?q=" + urllib.request.quote(q) + "&sort=stars&per_page=8")
        if not data or not data.get("items"):
            continue
        for it in data["items"][:8]:
            full = it.get("full_name", "")
            stars = it.get("stargazers_count", 0)
            if not full or full.lower() in seen_repos or stars < 5:
                continue
            seen_repos.add(full.lower())
            for br in ("main", "master"):
                st, body = fetch(f"https://raw.githubusercontent.com/{full}/{br}/README.md")
                if st == 200 and body:
                    for u in extract_urls(body):
                        add(u, f"github:{full}")
                    add(f"https://github.com/{full}", f"github:{full}", "repo")
                    break
            time.sleep(1.2)
    print(f"池中候选(仓库轮后): {len(pool)}")

    # 3) 社区攻略帖出链
    for page in PAGE_SOURCES:
        st, body = fetch(page)
        if st == 200 and body:
            for u in extract_urls(body):
                add(u, page)
        time.sleep(1.0)
    print(f"池中候选(社区帖轮后): {len(pool)}")

    # 4) reddit 帖 JSON（自出链）
    for page in [p for p in PAGE_SOURCES if "reddit.com" in p]:
        st, body = fetch(page.rstrip("/") + ".json?limit=100")
        if st == 200 and body:
            try:
                data = json.loads(body)
                for child in data[0]["data"]["children"][:40]:
                    for u in extract_urls(json.dumps(child.get("data", {}).get("selftext", ""))):
                        add(u, "reddit:" + page)
            except Exception:
                pass
    print(f"池中候选(reddit轮后): {len(pool)}")
    return pool

def probe(pool: dict[str, dict], workers: int = 6) -> None:
    def one(item):
        url, meta = item
        try:
            st, body = fetch(url)
            meta["status"] = st
            m = re.search(r"<title[^>]*>([^<]{2,120})", body)
            if m:
                meta["title"] = m.group(1).strip()[:100]
        except Exception:
            meta["status"] = 0
        time.sleep(0.2)
    items = list(pool.items())
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        for i, _ in enumerate(ex.map(one, items), 1):
            if i % 100 == 0:
                print(f"探测进度 {i}/{len(items)}")

def main() -> int:
    pool = collect()
    probe(pool)
    for m in pool.values():
        ok = m["status"] == 200
        m["score"] = (3 if m["kind"] == "official" else 2 if m["kind"] == "repo" else 1) \
                     + (2 if ok else -3) + (1 if m["title"] else 0)
    data = {"generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "total": len(pool), "candidates": list(pool.values())}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    by = {}
    for m in pool.values():
        by[m["kind"]] = by.get(m["kind"], 0) + 1
    ok200 = sum(1 for m in pool.values() if m["status"] == 200)
    print(f"\n完成: {len(pool)} 候选 | 分类 {by} | 可达(200): {ok200}")
    print(f"已写 {OUT}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
