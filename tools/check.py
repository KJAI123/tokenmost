#!/usr/bin/env python3
"""tokenmost 数据校验 + rss.xml 同步生成。用法：python3 tools/check.py"""
import json, sys, datetime, html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAYERS = {"official_cn": "大模型官方（国内）", "agent": "Agent 平台", "compute": "算力平台",
          "reseller": "Token 中间商", "official_global": "大模型官方（海外）", "intel_source": "情报源"}
TYPES = {"signup_bonus": "注册赠送", "free_tier": "长期免费", "coupon": "折扣码",
         "student": "学生通道", "limited_promo": "限时活动", "price_low": "长期低价",
         "free_model": "免费模型", "pricing_plan": "套餐订阅", "recurring_promo": "长期活动",
         "warning": "避雷", "tool_integration": "工具接入", "invite_bonus": "邀请奖励",
         "subscription_bonus": "订阅赠送", "info": "情报"}

deals = json.loads((ROOT / "deals.json").read_text())
sites = json.loads((ROOT / "sites.json").read_text())
prices = json.loads((ROOT / "prices.json").read_text())
errors, warns = [], []

# --- deals 校验 ---
ids = [d["id"] for d in deals]
if len(ids) != len(set(ids)):
    errors.append("deal id 重复: " + str([i for i in ids if ids.count(i) > 1]))
all_sites = [s for g in sites for s in g["sites"]]
site_first = {s["name"].split()[0]: s for s in all_sites}
for d in deals:
    for k in ("id", "provider", "category", "type", "value", "url", "verify_status", "verified_at", "difficulty", "published"):
        if k not in d:
            errors.append(f"{d.get('id','?')} 缺字段 {k}")
    if d.get("category") not in LAYERS: errors.append(f"{d['id']} category 非法: {d['category']}")
    # type/via 为自由标识符（主管产线可扩展），只校验格式
    if not re.match(r"^[a-z_]{2,30}$", str(d.get("type", ""))): errors.append(f"{d['id']} type 格式非法: {d['type']}")
    if d.get("via") and not re.match(r"^[a-z_]{2,30}$", str(d["via"])): errors.append(f"{d['id']} via 格式非法: {d['via']}")
    if not re.match(r"^https?://", d.get("url", "")): errors.append(f"{d['id']} url 非 http(s): {d['url']}")
    if d.get("coupon") and not d.get("published", True) and not d.get("placeholder"):
        warns.append(f"{d['id']} 有 coupon 且未发布但无 placeholder 标记")
    for k in ("tokens_wan", "cny", "usd"):
        if k in d and (not isinstance(d[k], (int, float)) or d[k] < 0):
            errors.append(f"{d['id']} 收益字段 {k} 非法: {d[k]}")
    first = d["provider"].split()[0]
    if d["provider"].split()[0] not in site_first:
        warns.append(f"{d['id']} provider「{d['provider']}」无对应导航站点（无 ⚡接入 按钮）")

# --- sites 校验 ---
for g in sites:
    if g["layer"] not in LAYERS: errors.append(f"sites layer 非法: {g['layer']}")
for s in all_sites:
    if not re.match(r"^https?://", s["url"]): errors.append(f"site {s['name']} url 非法")
    api = s.get("api")
    if api:
        for k in ("base_url", "model", "env"):
            if not api.get(k): errors.append(f"site {s['name']} api 缺 {k}")
        if not re.match(r"^https?://", api["base_url"]): errors.append(f"site {s['name']} api.base_url 非法")

# --- prices 校验 ---
for p in prices:
    if p["currency"] not in ("CNY", "USD"): errors.append(f"price {p['model']} currency 非法")
    for k in ("input", "output"):
        if not isinstance(p.get(k), (int, float)) or p[k] < 0: errors.append(f"price {p['model']} {k} 非法")

# --- rss 生成（与 published:true 一一对应）---
def rfc822(iso):
    dt = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return dt.strftime("%a, %d %b %Y 00:00:00 GMT")

items = []
for d in deals:
    if not d.get("published", True): continue
    desc = TYPES.get(d["type"], d["type"])
    if d.get("rule"): desc += " · 规则：" + d["rule"]
    if d.get("deadline"): desc += f" · 截止 {d['deadline']}"
    if d.get("coupon") and not d.get("placeholder"): desc += " · 折扣码见站内卡片"
    desc += "（优惠以官方页面为准）"
    items.append(f"""    <item>
      <title>{html.escape(d['provider'] + "：" + d['value'].split("；")[0].split("——")[0][:60])}</title>
      <link>{html.escape(d['url'])}</link>
      <guid isPermaLink="false">{d['id']}</guid>
      <pubDate>{rfc822(d['verified_at'])}</pubDate>
      <description>{html.escape(desc)}</description>
    </item>""")

latest = max(d["verified_at"] for d in deals if d.get("published", True))
rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>tokenmost.com — AI token 折扣情报</title>
    <link>https://tokenmost.com/</link>
    <description>五层来源 AI token 折扣码与免费额度情报，每日人工核验</description>
    <language>zh-CN</language>
    <lastBuildDate>{rfc822(latest)}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
"""
(ROOT / "rss.xml").write_text(rss)

# 攻略页构建（guides/*.md 存在时）
import subprocess as _sp
_g = ROOT / "tools" / "build_guides.py"
if _g.exists():
    _sp.run([sys.executable, str(_g)])

pub = sum(1 for d in deals if d.get("published", True))
verified_pub = sum(1 for d in deals if d.get("published", True) and d["verify_status"] == "verified")
api_n = sum(1 for s in all_sites if s.get("api"))
print(f"deals {len(deals)} 条（published {pub}，其中 verified {verified_pub}）| sites {len(all_sites)} 个（api 端点 {api_n}）| prices {len(prices)} 行 | rss items {len(items)}")
for e in errors: print("ERROR:", e)
for w in warns: print("WARN:", w)
sys.exit(1 if errors else 0)
