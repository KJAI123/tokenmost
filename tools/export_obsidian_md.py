#!/usr/bin/env python3
"""把 tokenmost 免费情报聚合导出为 Obsidian 笔记（纯标准库）。
每轮 15 分钟找源巡检自动执行：deals.json 变了，Obsidian 里的笔记就自动更新。
输出：~/Documents/Obsidian Vault/Token羊毛情报站/ 下两个笔记。"""
from __future__ import annotations
import json, datetime, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT = Path.home() / "Documents" / "Obsidian Vault" / "Token羊毛情报站"
LAYER = {"official_cn":"大模型官方(国内)","agent":"Agent 平台","compute":"算力平台",
         "reseller":"Token 中间商","official_global":"大模型官方(海外)"}
TYPE = {"signup_bonus":"注册赠送","free_tier":"长期免费","coupon":"折扣码","student":"学生通道",
        "limited_promo":"限时活动","price_low":"长期低价"}

def main() -> int:
    deals = json.loads((ROOT/"deals.json").read_text(encoding="utf-8"))
    live = [d for d in deals if d.get("published") and d.get("verify_status")=="verified"]
    VAULT.mkdir(parents=True, exist_ok=True)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # 笔记1：免费 Token 总览
    lines = ["---","tags: [token羊毛, AI, 白嫖, tokenmost]","更新: " + now,
             f"来源: tokenmost.com 工作区（{len(live)} 条已验证在架）","---","",
             f"# 免费 Token 总览（自动聚合于 {now}）","",
             f"> 由 tokenmost 找源巡检自动维护，共 **{len(live)}** 条已验证在架情报。"
             "优惠以各平台官方页面为准。",""]
    for cat in ["official_cn","official_global","agent","compute","reseller"]:
        rows = [d for d in live if d.get("category")==cat]
        if not rows: continue
        lines += [f"## {LAYER.get(cat,cat)}（{len(rows)}）","",
                  "| 平台 | 内容 | 规则/门槛 | 核实 | 链接 |","|---|---|---|---|---|"]
        for d in rows:
            val = (d.get("value","") or "").replace("|","／")[:60]
            rule = (d.get("rule","") or "").replace("|","／")[:50]
            vtime = (d.get("verified_at","") or "")[:10]
            lines.append(f"| {d.get('provider','')} | {val} | {rule} | {vtime} | [官网]({d.get('url','')}) |")
        lines.append("")
    lines += ["## 薅羊毛纪律","",
              "- 只薅官方/官方授权渠道；多号、群控、伪造邀请=黑名单","- 每条情报注意「核实」日期，过期以官网为准",
              "- 完整情报流与一键接入工具见 tokenmost.com（本地: tokenmost/index.html）"]
    (VAULT/"免费Token总览.md").write_text("\n".join(lines), encoding="utf-8")

    # 笔记2：信源监控看板
    hb = ROOT/"data-research"/"harvest"/"heartbeat.txt"
    hb_line = hb.read_text().strip().splitlines()[-1] if hb.exists() else "尚无心跳"
    try:
        cfg = json.loads((ROOT/"tools"/"harvest_sources.json").read_text(encoding="utf-8"))
        n_src = len(cfg["sources"])
    except Exception:
        n_src = "?"
    q = ROOT/"data-research"/"discovery-queue.md"
    pending = sum(1 for l in q.read_text(encoding="utf-8").splitlines() if l.strip().startswith("- [ ]")) if q.exists() else 0
    (VAULT/"信源监控看板.md").write_text("\n".join([
        "---","tags: [token羊毛, 信源, 监控]","更新: " + now,"---","",
        "# 信源监控看板（自动聚合于 " + now + "）","",
        f"- 采集器现役信源：**{n_src}** 个（15 分钟一轮自动盯防）",
        f"- 找源队列待办：**{pending}** 条（data-research/discovery-queue.md）",
        f"- 最近心跳：{hb_line}",
        "- 全量信源表：tokenmost/data-research/信息源总表-全量版.xlsx",
        "- 交接/合并素材：tokenmost/data-research/HANDOFF.md","",
        "## 监控归属","",
        "| 归属 | 方式 |","|---|---|",
        "| ZCode 找源巡检(15分钟) | harvest 脚本 + diff 告警 + 队列搜索 |",
        "| 主会话 sync.py | 结构化 API 直更 + 页面哈希监控 |",
        "| 爬虫主管(主会话) | 平台深挖 data-deep |",
        "| 老板人工 | 公众号矩阵 + 客户端活动卡片(ZCode/豆包) |"]), encoding="utf-8")
    print(f"Obsidian 导出完成: {VAULT}/（免费Token总览.md {len(live)} 条 / 信源监控看板.md）")
    return 0

if __name__ == "__main__":
    sys.exit(main())
