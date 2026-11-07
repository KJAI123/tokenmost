#!/usr/bin/env python3
"""freecloud 全池爬取器 (freecloud_crawl.py) —— 对候选池实爬抽情报

- 输入：freecloud_candidates.json 里 status==200 的候选 + 盯防表活跃源
- 内核：pagesift（robots.txt/限速自动），并发 PAGESIFT_CONCURRENCY（默认 12）
- 每页抽取：标题、正文长度、免费/云关键词计数、Top 5 情报片段（±80 字符）
- 输出：freecloud_crawl/crawl-YYYYMMDD.jsonl（增量可续爬）+ report md（Top 命中）
- 零 LLM token

用法:
    python3 data-research/freecloud/freecloud_crawl.py                # 全量（断点续爬）
    python3 data-research/freecloud/freecloud_crawl.py --limit 500    # 本轮只爬 500 条
    python3 data-research/freecloud/freecloud_crawl.py --cat official # 只爬某分类
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
POOL = HERE / "freecloud_candidates.json"
SOURCES = HERE / "freecloud_sources.json"
OUTDIR = HERE / "freecloud_crawl"

FREE_KW = re.compile(r"(?i)(free|gratis|kostenlos|darmowy|gratuit|免费|试用|白嫖|赠)")
CLOUD_KW = re.compile(
    r"(?i)(vps|vds|dedicated|hosting|cloud|server|\bvm\b|gpu|sandbox|compute|\bide\b|paas|faas|"
    r"serverless|docker|container|kubernetes|microvm|shell|workspace|notebook|colab|database|"
    r"\bcdn\b|\bdns\b|storage|k8s|free[- ]?tier|always[- ]?free|云服务器|云主机|虚拟主机|建站)")
SIGNAL_KW = re.compile(
    r"(?i)(free tier|free plan|always[- ]?free|forever[- ]?free|free trial|\$\d+|€\d+|"
    r"\d+\s*(?:vCPUs?|GiBs?|GBs?|MB|TB)|credits?\b|\d+\s*(?:hours?|months?|years?)\b|"
    r"免费(?:试用|额度|套餐|赠送)|永久免费|长期免费|试用金|赠金)")
SNIP = 80


def extract_intel(md: str) -> dict:
    hits = []
    seen: set[str] = set()
    for m in SIGNAL_KW.finditer(md):
        s = max(0, m.start() - SNIP)
        ctx = re.sub(r"\s+", " ", md[s:m.end() + SNIP]).strip()
        if len(ctx) > 10 and ctx not in seen:
            seen.add(ctx)
            hits.append(ctx)
    return {
        "n_free": len(FREE_KW.findall(md)),
        "n_cloud": len(CLOUD_KW.findall(md)),
        "n_signal": len(hits),
        "snippets": hits[:5],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--cat", help="只爬某分类（official/doc/repo/article）")
    a = ap.parse_args()

    pool = json.loads(POOL.read_text(encoding="utf-8"))["items"]
    watch = {s["url"].rstrip("/"): s["id"] for s in json.loads(SOURCES.read_text(encoding="utf-8"))["sources"]}

    todo: list[tuple[str, str, str]] = []  # (url, cat, label)
    for u, c in pool.items():
        if c.get("status") != 200:
            continue
        if a.cat and c.get("cat") != a.cat:
            continue
        todo.append((u, c.get("cat", "?"), c.get("text", "")[:60]))
    for u, sid in watch.items():
        todo.append((u, "watch", sid))
    todo = sorted(set(todo))

    OUTDIR.mkdir(parents=True, exist_ok=True)
    out = OUTDIR / f"crawl-{date.today().isoformat()}.jsonl"
    done: set[str] = set()
    for prev in sorted(OUTDIR.glob("crawl-*.jsonl")):  # 断点缓存跨天累计（修复：原先只认当天文件）
        for line in prev.read_text(encoding="utf-8").splitlines():
            try:
                done.add(json.loads(line)["url"])
            except Exception:
                pass
    todo = [t for t in todo if t[0] not in done]
    if a.limit:
        todo = todo[:a.limit]

    print(f"待爬 {len(todo)}（已完成 {len(done)} 缓存于 {out.name}）")
    if not todo:
        return 0

    import pagesift

    conc = int(os.environ.get("PAGESIFT_CONCURRENCY", "12"))
    opts = pagesift.ScrapeOptions(timeout=25000)
    n_ok = n_err = 0
    t0 = datetime.now(timezone.utc)
    with pagesift.Scraper() as scraper, out.open("a", encoding="utf-8") as fh:
        urls = [t[0] for t in todo]
        for i, doc in enumerate(scraper.scrape_iter(urls, options=opts, concurrency=conc)):
            url, cat, label = todo[doc.index]
            if doc.success and doc.markdown:
                md = doc.markdown
                rec = {"url": url, "cat": cat, "label": label, "status_code": doc.status_code,
                       "title": (doc.metadata or {}).get("title", "")[:160],
                       "md_len": len(md), "ts": _now(), **extract_intel(md)}
                n_ok += 1
            else:
                rec = {"url": url, "cat": cat, "label": label, "error_code": getattr(doc, "error_code", None),
                       "error": (getattr(doc, "error_message", "") or "")[:120], "ts": _now()}
                n_err += 1
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if (i + 1) % 100 == 0:
                fh.flush()
                el = (datetime.now(timezone.utc) - t0).total_seconds()
                print(f"进度 {i + 1}/{len(todo)} | ok {n_ok} err {n_err} | {el:.0f}s", flush=True)

    write_report(n_ok, n_err)
    print(f"\n== 爬取完成: ok {n_ok} / err {n_err} → {out.name}")
    return 0


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_report(n_ok: int, n_err: int) -> None:
    recs = []
    for prev in sorted(OUTDIR.glob("crawl-*.jsonl")):
        for line in prev.read_text(encoding="utf-8").splitlines():
            try:
                recs.append(json.loads(line))
            except Exception:
                pass
    # 跨天去重：同 URL 保留最新一条
    by_url: dict[str, dict] = {}
    for r in recs:
        by_url[r["url"]] = r  # 后写覆盖先写=最新
    recs = list(by_url.values())
    out_path = sorted(OUTDIR.glob("crawl-*.jsonl"))[-1]
    good = [r for r in recs if "md_len" in r]
    errs = [r for r in recs if "error_code" in r]
    top = sorted(good, key=lambda r: (r["n_signal"], r["n_free"]), reverse=True)[:40]
    errc = {}
    for r in errs:
        errc[r.get("error_code") or "?"] = errc.get(r.get("error_code") or "?", 0) + 1
    cats = {}
    for r in good:
        cats[r["cat"]] = cats.get(r["cat"], 0) + 1

    lines = [
        f"# freecloud 全池爬取报告 {date.today().isoformat()}",
        "",
        f"- 累计 {len(recs)} | 成功 {len(good)} | 失败 {len(errs)}（{errc}）",
        f"- 成功分类分布: {cats}",
        f"- 情报信号页（n_signal≥3）: {sum(1 for r in good if r['n_signal'] >= 3)}",
        "",
        "## Top 40 情报信号页（按免费/数额关键词密度）",
        "",
    ]
    for r in top:
        lines.append(f"### [{r['cat']}] {r['label'] or r['title']}")
        lines.append(f"- {r['url']}")
        lines.append(f"- title: {r['title']} | md {r['md_len']}B | free×{r['n_free']} cloud×{r['n_cloud']} signal×{r['n_signal']}")
        for s in r["snippets"][:3]:
            lines.append(f"- 🔎 `{s}`")
        lines.append("")
    (OUTDIR / f"report-{date.today().isoformat()}.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
