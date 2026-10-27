#!/usr/bin/env python3
"""tokenmost 零 token 采集器 (harvest.py)

目标：日常盯防各平台官方页面的价格/额度关键词变化，全程不消耗任何 LLM token。
- 纯 Python 标准库（无需安装依赖）
- 遵守 robots.txt、限速抓取、15s 超时
- 输出：data-research/harvest/harvest-YYYY-MM-DD.md + latest.json
- --selftest 用内置样本自检提取逻辑，不发网络请求

用法:
    python3 tools/harvest.py                # 全量抓取
    python3 tools/harvest.py --only volc    # 只抓 id 含 volc 的源
    python3 tools/harvest.py --selftest     # 离线自检
"""
from __future__ import annotations  # 兼容 Python 3.9 的类型注解（PEP 604 / 内置泛型）

import argparse
import json
import re
import sys
import time
import urllib.request
import urllib.robotparser
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "tools" / "harvest_sources.json"
OUTDIR = ROOT / "data-research" / "harvest"
UA = "tokenmost-harvest/0.1 (+https://tokenmost.com; deal-verification research bot)"
DELAY = 1.0  # 抓取间隔秒数（60+ 源规模下保证 15 分钟内跑完）
TIMEOUT = 10

# 通用关键词：命中即记录上下文
DEFAULT_PATTERNS = [
    r"免费[^。]{0,40}(额度|tokens?|token|次)",
    r"(赠送|注册即送|注册送|新用户)[^。]{0,50}",
    r"\d+\s*万\s*[Tt]okens?",
    r"[¥￥$]\s?[\d.]+[^。]{0,30}(百万|/M|/1M)?",
    r"每[日天][^。]{0,40}(万|tokens?|次)",
    r"\b(RPM|RPD|requests? per (minute|day))\b[^。]{0,40}",
]

TAG_RE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.S | re.I)
HTML_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"[ \t\r\f\v]+")


def load_text(html: str) -> str:
    """剥掉 script/style 与标签，压平成纯文本。"""
    html = TAG_RE.sub(" ", html)
    text = HTML_RE.sub(" ", html)
    text = (text.replace("&nbsp;", " ").replace("&amp;", "&")
                .replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&#39;", "'"))
    return WS_RE.sub(" ", text).replace("\n", " ")


def extract(text: str, patterns: list[str]) -> list[dict]:
    """跑关键词，返回命中与前后各 120 字符的上下文窗口。"""
    hits, seen = [], set()
    for pat in patterns:
        for m in re.finditer(pat, text, re.I):
            a, b = max(0, m.start() - 120), min(len(text), m.end() + 120)
            window = text[a:b].strip()
            key = window[:60]
            if key in seen:
                continue
            seen.add(key)
            hits.append({"match": m.group(0)[:80], "context": window})
            if len(hits) >= 30:  # 每源最多记 30 条，防刷屏
                return hits
    return hits


def robots_allows(url: str, cache: dict) -> bool:
    host = "/".join(url.split("/")[:3])
    if host not in cache:
        rp = urllib.robotparser.RobotFileParser()
        try:
            with urllib.request.urlopen(urllib.request.Request(host + "/robots.txt", headers={"User-Agent": UA}), timeout=TIMEOUT) as r:
                rp.parse(r.read().decode("utf-8", "ignore").splitlines())
        except Exception:
            rp = None  # 拿不到 robots.txt 时按允许处理
        cache[host] = rp
    rp = cache[host]
    return True if rp is None else rp.can_fetch(UA, url)


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", "ignore")


def run(only: str | None = None) -> int:
    cfg = json.loads(SOURCES.read_text(encoding="utf-8"))
    robots_cache: dict = {}
    results, errors = [], []
    for src in cfg["sources"]:
        sid, url = src["id"], src["url"]
        if only and only not in sid:
            continue
        if src.get("disabled"):
            results.append({"id": sid, "name": src["name"], "url": url, "status": "disabled"})
            continue
        entry = {"id": sid, "name": src["name"], "url": url}
        try:
            if not robots_allows(url, robots_cache):
                entry["status"] = "robots_disallowed"
                results.append(entry)
                print(f"[skip] {sid}: robots.txt 不允许，尊重站点选择")
                continue
            raw = fetch(url)
            hits = extract(load_text(raw), DEFAULT_PATTERNS + src.get("patterns", []))
            entry.update(status="ok", hits=len(hits), findings=hits)
            results.append(entry)
            print(f"[ok]   {sid}: {len(hits)} 处命中（{url}）")
        except Exception as e:  # 网络失败不中断整体
            entry.update(status="error", error=f"{type(e).__name__}: {e}")
            errors.append(sid)
            results.append(entry)
            print(f"[err]  {sid}: {type(e).__name__}: {e}")
        time.sleep(DELAY)
    return results, errors


def save(results: list[dict]) -> Path:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    (OUTDIR / "latest.json").write_text(
        json.dumps({"harvested_at": now, "results": results}, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [f"# 采集快照 {today}", "", f"- 采集时间: {now}（零 LLM 参与）",
             f"- 源数: {len(results)}，命中源: {sum(1 for r in results if r.get('hits'))}", ""]
    for r in results:
        lines.append(f"## {r['name']}（{r['id']}）")
        lines.append(f"- 状态: {r['status']}，来源: {r['url']}")
        if r["status"] == "ok" and r.get("findings"):
            for h in r["findings"][:12]:
                lines.append(f"- 🔎 `…{h['context']}…`")
        elif r["status"] == "ok":
            lines.append("- ⚠️ 0 命中——页面可能已改版或为 JS 渲染，需人工核查 pattern")
        lines.append("")
    out = OUTDIR / f"harvest-{today}.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def selftest() -> int:
    sample = ("新用户注册即送 2000 万 Tokens，GLM-4-Flash 模型免费。定价 ¥2 /百万 tokens。"
              "免费层每天 500 万 Tokens，限 30 RPM 与 1000 RPD。充 $10 解锁更多。")
    hits = extract(sample, DEFAULT_PATTERNS)
    assert any("2000 万" in h["context"] for h in hits), "应命中 2000万 Tokens"
    assert any("500 万" in h["context"] for h in hits), "应命中每日额度"
    assert any("RPM" in h["context"] for h in hits), "应命中 RPM/RPD"
    assert any("$10" in h["context"] for h in hits), "应命中美元价"
    print(f"selftest OK: {len(hits)} 处命中，提取逻辑正常")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="只抓 id 含该子串的源")
    ap.add_argument("--selftest", action="store_true", help="离线自检，不发请求")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    results, errors = run(args.only)
    out = save(results)
    print(f"\n快照已写入: {out}")
    if errors:
        print(f"注意: {len(errors)} 个源失败（{', '.join(errors)}），可稍后重试或人工核查")
    return 0


if __name__ == "__main__":
    sys.exit(main())
