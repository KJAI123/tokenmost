#!/usr/bin/env python3
"""freecloud 挖矿器 (freecloud_expand.py) —— 聚合仓/聚合页里挖免费云服务器信源

套路沿用主管线 expand_sources.py（信源千人计划）：源里挖源 → 去重 → 并发探测 → 累积候选池。
- 候选池 freecloud_candidates.json 为累积基准，旧候选永不丢失
- 不自动入盯防表：候选只是候选，人工/主会话挑选高价值并入 freecloud_sources.json
- 零 LLM token

用法:
    python3 data-research/freecloud/freecloud_expand.py            # 全量挖+探
    python3 data-research/freecloud/freecloud_expand.py --no-probe # 只挖不探（快）
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCES = HERE / "freecloud_sources.json"
POOL = HERE / "freecloud_candidates.json"
UA = "tokenmost-freecloud-expand/0.1 (+https://tokenmost.com; free-tier research)"

# 挖矿源：raw markdown 聚合仓（新仓往这里加）
MINING = [
    {"name": "free-for-dev（ripienaar，73k+ star 免费开发者资源总表）",
     "url": "https://raw.githubusercontent.com/ripienaar/free-for-dev/master/README.md",
     "fallback": "https://raw.githubusercontent.com/ripienaar/free-for-dev/main/README.md"},
]

# 相关性提示词：命中才算 freecloud 候选
CLOUD_HINTS = re.compile(
    r"(?i)(vps|vds|dedicated|hosting|cloud|server|vm|virtual machine|gpu|sandbox|compute|"
    r"ide|paas|faas|serverless|docker|container|kubernetes|firecracker|microvm|shell|"
    r"workspace|notebook|colab|trial|free tier|always.?free|数据库|云服务器|云主机|试用)")
# 明确排除：社交/视频/纯LLM API 类（LLM API 归主管线管）
EXCLUDE = re.compile(
    r"(?i)(twitter|x\.com|youtube|facebook|instagram|tiktok|discord\.gg|t\.me|"
    r"openai\.com|anthropic\.com|"
    r"^#|anchor$|/blob/|twitter\.com)")

LINK_RE = re.compile(r"\[([^\]]{2,120})\]\((https?://[^)\s]+)\)")


def fetch(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")


def load_pool() -> dict:
    if POOL.exists():
        try:
            return json.loads(POOL.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"updated_at": None, "items": {}}


def mine() -> list[dict]:
    """抓聚合仓 README，抽相关外链候选。"""
    existing = {s["url"].rstrip("/") for s in json.loads(SOURCES.read_text(encoding="utf-8"))["sources"]}
    existing |= {c["url"].rstrip("/") for c in load_pool()["items"].values()}
    out: list[dict] = []
    seen: set[str] = set()
    for src in MINING:
        try:
            try:
                md = fetch(src["url"])
            except Exception:
                md = fetch(src["fallback"])
        except Exception as e:
            print(f"[err] 挖矿源不可达 {src['name']}: {type(e).__name__}")
            continue
        print(f"[ok]  {src['name']}: {len(md) // 1024}KB")
        cur = src["url"]
        for text, url in LINK_RE.findall(md):
            url = url.rstrip("/")
            if url in seen or url.rstrip("/") in existing:
                continue
            if EXCLUDE.search(url) or EXCLUDE.search(text):
                continue
            blob = f"{text} {url}"
            if not CLOUD_HINTS.search(blob):
                continue
            seen.add(url)
            out.append({"url": url, "text": text.strip()[:120], "found_in": src["name"]})
    return out


def probe(cands: list[dict]) -> None:
    def one(c: dict) -> None:
        try:
            req = urllib.request.Request(c["url"], headers={"User-Agent": UA}, method="HEAD")
            with urllib.request.urlopen(req, timeout=12) as r:
                c["status"] = r.status
        except Exception as e:
            code = getattr(e, "code", None)
            c["status"] = code if code else f"{type(e).__name__}"

    with ThreadPoolExecutor(max_workers=10) as ex:
        list(ex.map(one, cands))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-probe", action="store_true")
    a = ap.parse_args()

    pool = load_pool()
    cands = mine()
    if not cands:
        print("无新候选（池可能已吃干，往 MINING 里加新仓）")
        return 0
    print(f"新候选 {len(cands)} 条")
    if not a.no_probe:
        probe(cands)
        ok = sum(1 for c in cands if c.get("status") == 200)
        print(f"探测完成: 200×{ok} / 非200×{len(cands) - ok}")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for c in cands:
        c["added_at"] = now
        pool["items"][c["url"]] = c
    pool["updated_at"] = now
    POOL.write_text(json.dumps(pool, ensure_ascii=False, indent=2), encoding="utf-8")
    ok_n = sum(1 for c in pool["items"].values() if c.get("status") == 200)
    print(f"候选池累计: {len(pool['items'])} 条（200 可达 {ok_n}）→ {POOL.name}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
