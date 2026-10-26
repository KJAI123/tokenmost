#!/usr/bin/env python3
"""tokenmost 快照 diff 告警 (harvest_diff.py)

v3 关键件：对比最新快照 latest.json 与上一份快照对应的历史状态（prev.json 基线），
识别各源状态 / 命中数 / 命中内容的变化。
- 页面没变 → 打印 no change，全程无人值守
- 有变化 → 写 data-research/harvest/alert-YYYY-MM-DD.md，列出变化源与上下文摘录，
  此时才需要人/LLM 介入判读
- 纯 Python 标准库、兼容 Python 3.9、--selftest 离线自检不发网络请求

基线说明：harvest.py 同日重跑会覆盖 latest.json 与 harvest-*.md，因此「上一份快照」
的结构化状态由本脚本落盘为 prev.json（与上一份 harvest-*.md 一一对应），并在每轮
对比完成后滚动更新为最新状态。

用法:
    python3 tools/harvest_diff.py             # 对比并按需写告警
    python3 tools/harvest_diff.py --selftest  # 离线自检
"""
from __future__ import annotations  # 兼容 Python 3.9 的类型注解（PEP 604 / 内置泛型）

import argparse
import hashlib
import json
import sys
import tempfile
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "data-research" / "harvest"
LATEST = OUTDIR / "latest.json"   # harvest.py 每轮覆盖写
BASELINE = OUTDIR / "prev.json"   # 上一份快照状态，由本脚本维护与滚动
MAX_EXCERPTS = 3                  # 告警里每源最多摘录几条新增上下文
MAX_REMOVED = 5                   # 告警里每源最多列几条消失命中


def fingerprint(entry: dict) -> str:
    """命中内容的指纹：任一 match/context 变了指纹就变。"""
    parts = ["{}|{}".format(h.get("match", ""), h.get("context", ""))
             for h in entry.get("findings", [])]
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()


def index_results(state: dict) -> dict:
    """把 latest.json 的 results 转成 {id: entry} 索引。"""
    return {r["id"]: r for r in state.get("results", [])}


def diff_states(prev: dict, cur: dict) -> list[dict]:
    """对比两份快照，返回变化源列表（按 id 排序）。"""
    p, c = index_results(prev), index_results(cur)
    changes = []
    for sid in sorted(set(p) | set(c)):
        pe, ce = p.get(sid), c.get(sid)
        if ce is None:
            changes.append({"id": sid, "kind": "removed", "prev": pe})
            continue
        if pe is None:
            changes.append({"id": sid, "kind": "added", "cur": ce})
            continue
        fields = []
        if pe.get("status") != ce.get("status"):
            fields.append("状态 {} → {}".format(pe.get("status"), ce.get("status")))
        ph, ch = len(pe.get("findings", [])), len(ce.get("findings", []))
        if ph != ch:
            fields.append("命中数 {} → {}".format(ph, ch))
        if ce.get("status") == "error" and pe.get("error") != ce.get("error"):
            fields.append("错误信息变化")
        if fingerprint(pe) != fingerprint(ce):
            fields.append("命中内容变化")
        if fields:
            changes.append({"id": sid, "kind": "changed", "detail": "；".join(fields),
                            "prev": pe, "cur": ce})
    return changes


def render_alert(changes: list[dict], prev: dict, cur: dict) -> str:
    """把变化列表渲染成 alert-*.md 的正文。"""
    lines = ["# 采集变化告警 {}".format(date.today().isoformat()), "",
             "- 生成时间: {}（harvest_diff 自动生成）".format(
                 datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")),
             "- 基线快照: {}（prev.json，对应上一份 harvest-*.md）".format(prev.get("harvested_at", "?")),
             "- 当前快照: {}（latest.json）".format(cur.get("harvested_at", "?")),
             "- 变化源: {} / {}".format(len(changes), len(index_results(cur))),
             "", "> 仅列变化源；未列出的源视为无变化。", ""]
    for ch in changes:
        if ch["kind"] == "added":
            e = ch["cur"]
            lines.append("## 新增源 {}（{}）".format(e.get("name", "?"), ch["id"]))
            lines.append("- 状态: {}，来源: {}".format(e.get("status"), e.get("url", "?")))
            for h in e.get("findings", [])[:MAX_EXCERPTS]:
                lines.append("- 🔎 `…{}…`".format(h.get("context", "")))
            lines.append("")
            continue
        if ch["kind"] == "removed":
            e = ch["prev"]
            lines.append("## 移除源 {}（{}）".format(e.get("name", "?"), ch["id"]))
            lines.append("- 原状态: {}，来源: {}".format(e.get("status"), e.get("url", "?")))
            lines.append("")
            continue
        pe, ce = ch["prev"], ch["cur"]
        lines.append("## {}（{}）".format(ce.get("name", pe.get("name", "?")), ch["id"]))
        lines.append("- 变化: {}".format(ch["detail"]))
        if ce.get("error"):
            lines.append("- 错误: {}".format(ce["error"]))
        pm = {h.get("match", "") for h in pe.get("findings", [])}
        cm = {h.get("match", "") for h in ce.get("findings", [])}
        gone = sorted(pm - cm)
        if gone:
            lines.append("- 消失命中({}): {}".format(len(gone), "、".join(gone[:MAX_REMOVED])))
        for h in [h for h in ce.get("findings", []) if h.get("match", "") not in pm][:MAX_EXCERPTS]:
            lines.append("- 🔎 新增 `…{}…`".format(h.get("context", "")))
        lines.append("")
    return "\n".join(lines)


def run_diff(outdir: Path) -> tuple:
    """对 outdir 下的 latest.json 与 prev.json 做对比；返回 (退出码, 摘要消息)。"""
    latest, baseline = outdir / "latest.json", outdir / "prev.json"
    if not latest.exists():
        return 1, "latest.json 不存在，请先运行 tools/harvest.py 采集一轮"
    raw = latest.read_text(encoding="utf-8")
    if not baseline.exists():
        baseline.write_text(raw, encoding="utf-8")
        return 0, "首次运行：已建立基线 prev.json，下轮开始对比（本轮 no change）"
    prev, cur = json.loads(baseline.read_text(encoding="utf-8")), json.loads(raw)
    changes = diff_states(prev, cur)
    baseline.write_text(raw, encoding="utf-8")  # 基线滚动到本轮
    if not changes:
        return 0, "no change（{} 个源全部无变化）".format(len(index_results(cur)))
    out = outdir / "alert-{}.md".format(date.today().isoformat())
    out.write_text(render_alert(changes, prev, cur), encoding="utf-8")
    return 0, "检测到 {} 个源有变化，告警已写入 {}".format(len(changes), out)


def selftest() -> int:
    # 单元：五类变化（无变化 / 数量+内容 / 状态+错误 / 源移除 / 源新增）
    base = [{"id": "a", "name": "源A", "status": "ok",
             "findings": [{"match": "m1", "context": "c1"}]},
            {"id": "b", "name": "源B", "status": "ok",
             "findings": [{"match": "m2", "context": "c2"}]},
            {"id": "c", "name": "源C", "status": "ok", "findings": []},
            {"id": "d", "name": "源D", "status": "error", "error": "boom", "findings": []}]
    cur = [{"id": "a", "name": "源A", "status": "ok",
            "findings": [{"match": "m1", "context": "c1"}]},
           {"id": "b", "name": "源B", "status": "ok",
            "findings": [{"match": "m2-new", "context": "c2-new"},
                         {"match": "m3", "context": "c3"}]},
           {"id": "c", "name": "源C", "status": "error", "error": "timeout", "findings": []},
           {"id": "e", "name": "源E", "status": "ok", "findings": []}]
    by = {c["id"]: c for c in diff_states({"results": base}, {"results": cur})}
    assert "a" not in by, "无变化源不应出现在告警里"
    assert by["b"]["kind"] == "changed" and "命中数 1 → 2" in by["b"]["detail"]
    assert by["c"]["kind"] == "changed" and "状态" in by["c"]["detail"]
    assert by["d"]["kind"] == "removed" and by["e"]["kind"] == "added"
    # 端到端：临时目录里跑完整流程（建基线 → 有变化写告警 → 基线滚动后 no change）
    with tempfile.TemporaryDirectory() as td:
        out = Path(td)
        (out / "prev.json").write_text(
            json.dumps({"harvested_at": "T0", "results": base}, ensure_ascii=False), encoding="utf-8")
        (out / "latest.json").write_text(
            json.dumps({"harvested_at": "T1", "results": cur}, ensure_ascii=False), encoding="utf-8")
        code, msg = run_diff(out)
        assert code == 0 and "告警已写入" in msg, msg
        alerts = list(out.glob("alert-*.md"))
        assert len(alerts) == 1 and "命中数 1 → 2" in alerts[0].read_text(encoding="utf-8")
        code2, msg2 = run_diff(out)
        assert code2 == 0 and "no change" in msg2, msg2
        assert len(list(out.glob("alert-*.md"))) == 1, "无变化不应新增告警文件"
        (out / "prev.json").unlink()
        code3, msg3 = run_diff(out)
        assert code3 == 0 and "基线" in msg3, msg3  # 基线丢失时可自愈重建
    print("selftest OK: 数量/内容/状态/增删源五类变化均识别，告警落盘与基线滚动正常")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true", help="离线自检，不发请求")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    code, msg = run_diff(OUTDIR)
    print(msg)
    return code


if __name__ == "__main__":
    sys.exit(main())
