#!/usr/bin/env python3
"""Telegram 频道监视器（零 token）——X 的合规替代管线。
X 站内直抓不可行（登录墙+robots 禁爬+API 收费，且不绕反爬）；
Telegram 公开频道预览页（t.me/s/<频道>）静态可抓，大量 AI 羊毛频道镜像 X 情报。

每轮：抓频道列表 → 消息提取 → 关键词过滤（token/免费/credit/羊毛/AI）→ 去重 → 新消息写告警。
频道列表：data-research/tg_channels.json（可随时增删，老板补充自己关注的频道）。
状态：data-research/tg_state.json（seen 去重）。
"""
from __future__ import annotations
import json, re, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DR = ROOT / "data-research"
CHANNELS = DR / "tg_channels.json"
STATE = DR / "tg_state.json"
ALERTS = DR / "tg_alerts.md"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"
KW = re.compile(r"免费|额度|羊毛|白嫖|token|credit|free tier|赠送|折扣|coupon|promo", re.I)
MSG_RE = re.compile(r'class="tgme_widget_message_text[^"]*"[^>]*>([\s\S]*?)</div>')
LINK_RE = re.compile(r'href="([^"]*?)"')  # 消息内 t.me 深链

def fetch(url: str) -> str:
    try:
        return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}),
                                      timeout=12).read(500_000).decode("utf-8", "ignore")
    except Exception:
        return ""

def strip_tags(h: str) -> str:
    t = re.sub(r"<br/?>", "\n", h)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"[ \t]+", " ", t).strip()

def main() -> int:
    if CHANNELS.exists():
        channels = json.loads(CHANNELS.read_text(encoding="utf-8"))
    else:
        channels = ["v2ex_notice"]
        CHANNELS.write_text(json.dumps(channels, ensure_ascii=False, indent=1), encoding="utf-8")
    try:
        state = json.loads(STATE.read_text(encoding="utf-8"))
    except Exception:
        state = {"seen": {}}
    seen = state.setdefault("seen", {})
    new_alerts = []
    for ch in channels:
        html = fetch(f"https://t.me/s/{ch}")
        if not html:
            print(f"[err] {ch}: 抓取失败")
            continue
        blocks = re.findall(r'(<div class="tgme_widget_message[\s\S]*?class="tgme_widget_message_footer[\s\S]*?)</div>\s*</div>', html)
        texts = MSG_RE.findall(html)
        n_new = 0
        for raw in texts[:15]:
            t = strip_tags(raw)
            if len(t) < 10:
                continue
            key = f"{ch}:{t[:60]}"
            if key in seen:
                continue
            seen[key] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
            if KW.search(t):
                new_alerts.append(f"🆕 [{ch}] {t[:150]}")
                n_new += 1
        print(f"[ok] {ch}: {len(texts)} 条消息，新命中 {n_new}")
    if new_alerts:
        with ALERTS.open("a", encoding="utf-8") as f:
            f.write(f"\n## {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n" +
                    "\n".join(f"- {a}" for a in new_alerts) + "\n")
    state["seen"] = dict(list(seen.items())[-2000:])  # 状态瘦身
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"NEW_TG_ALERTS={len(new_alerts)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
