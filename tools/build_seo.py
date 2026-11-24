#!/usr/bin/env python3
"""程序化 SEO（pSEO）：deals.json 按平台聚合生成静态落地页 + llms.txt。
被 check.py 末尾调用；pages.yml 需复制 platform/ 目录。纯标准库。
产出：
  platform/<slug>.html —— 每平台一页（title/desc/JSON-LD/FAQ/h1 全套，承接长尾词）
  llms.txt / llms-full.txt —— AI 搜索（ChatGPT/Perplexity）站点地图
日期口径（诚实性）：页面/FAQ 的核验日期只取自 deals.json 各条 verified_at
证据字段——全页一致写单日期、有效日期混合明示“各条不一”、有效性混合
（有效+缺失/无效）明示“部分未知/无效”、全无有效证据明示“未知/无效”，
绝不用生成时钟冒充核验时间；生成时钟只作“页面生成”展示并用于排除未来
日期证据。verified_at 必须是完整 ISO 日期或带合法 Z/偏移的完整时间戳，
尾随垃圾/畸形时间一律拒绝。sitemap lastmod 只在本次生成对已部署产物有
字节级修改证据（新旧内容不同）时给出=本次运行日，否则按 sitemaps.org
可选语义省略——lastmod 是页面最后修改日期，不是生成日期、也不是信源
核验日期。
"""
from urllib.parse import quote
import json, html, re
from pathlib import Path
from datetime import datetime, timezone, timedelta, date
from build_discovery import write_discovery
from token_math import entries as quota_entries, quota as token_quota, free as free_quota, estimate as daily_estimate, estimate_assumption

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "platform"
GDIR = ROOT / "guides"

LAYER = {"official_cn": "大模型官方（国内）", "agent": "Agent 平台", "compute": "算力平台",
         "reseller": "Token 中间商", "official_global": "大模型官方（海外）", "maas": "MaaS 平台（云上托管）"}
TYPE = {"paid_discount": "付费折扣", "signup_bonus": "注册赠送", "free_tier": "长期免费", "limited_promo": "限时活动",
        "recurring_promo": "长期活动", "free_model": "免费模型", "student": "学生通道", "invite_bonus": "邀请奖励", "pricing_plan": "套餐订阅", "info": "情报", "tool_integration": "工具接入"}

TPL = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://tokenmost.com/platform/{slug_enc}.html">
<meta property="og:title" content="{title} — tokenmost">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://tokenmost.com/platform/{slug_enc}.html">
{robots}<meta property="og:image" content="https://tokenmost.com/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://tokenmost.com/og-image.png">
<script type="application/ld+json">{ld_web}</script>
<script type="application/ld+json">{ld_faq}</script>
<style>
:root{{--bg:#f8f9fb;--card:#fff;--border:#e5e8ee;--text:#171b26;--muted:#5f6b7a;--accent:#059669;--green:#16a34a;--red:#dc2626;--link:#2563eb}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font:15px/1.75 -apple-system,"PingFang SC","Microsoft YaHei",sans-serif;max-width:780px;margin:0 auto;padding:28px 18px 80px}}
a{{color:var(--link);text-decoration:none}}
h1{{font-size:1.5rem;margin-bottom:4px}} h1 b{{color:var(--accent)}}
.sub{{color:var(--muted);font-size:.85rem;margin-bottom:18px}}
h2{{font-size:1.1rem;margin:22px 0 8px;color:var(--accent)}}
.deal{{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:12px 14px;margin:10px 0}}
.deal b{{font-size:.95rem}} .deal .tag{{display:inline-block;font-size:.72rem;color:var(--accent);border:1px solid var(--accent);border-radius:5px;padding:0 6px;margin-left:6px;vertical-align:1px}}
.deal p{{color:var(--muted);font-size:.88rem;margin-top:4px}}
.deal .go{{display:inline-block;margin-top:6px;background:var(--accent);color:#fff;border-radius:7px;padding:5px 14px;font-size:.82rem;font-weight:600}}
details{{border:1px solid var(--border);border-radius:10px;background:var(--card);padding:10px 14px;margin:8px 0}}
summary{{font-weight:700;cursor:pointer}}
details p{{color:var(--muted);font-size:.9rem;margin-top:8px}}
.back{{display:inline-block;margin-bottom:16px;color:var(--muted);font-size:.85rem}}
.rel{{margin-top:26px;padding-top:12px;border-top:1px solid var(--border);color:var(--muted);font-size:.85rem}}
.rel a{{margin-right:14px}}
</style><script defer src="/assets/engagement.js"></script></head><body data-surface="platform">
<a class="back" href="/">← 回 tokenmost 情报流</a>
<h1>{h1}</h1>
<p class="sub">信源核验：{updated} · 页面生成：{gen} · {layer} · 共 {n} 条信源 · {metric}</p>
<p>{intro}</p>
<h2>{offers_heading}</h2>
{deals}
<h2>{faq_heading}</h2>
{faq}
<div class="rel">继续看：<a href="/platform/">平台目录</a><a href="/free-ai-api.html">免费 API 对比</a><a href="/guides/">领取攻略</a><a href="/verified.xml">已核验权益 RSS</a><button type="button" data-share-page hidden>分享本页</button> <span role="status" data-share-status></span></div>
</body></html>"""

FAQ_GEN = [
    ("{name}现在有什么免费额度？",
     "本页信源核验日期：{updated}。{name}在 tokenmost 收录的权益共 {n} 条：{brief}。原始额度与折算依据分开显示，金额只作 DS Flash 购买力参考。"),
    ("{name}免费额度怎么领取？",
     "点击本页各条「立即领取」直达官方页面，按官方规则注册/实名/激活即可；限时活动请留意截止日期。tokenmost 每日核验各条状态，失效信息自动清洗。"),
    ("{name}的免费额度能用多少 token？",
     "首月参考为一次性额度、有效活动天数内的日额度（最多 30 天）与月额度之和。模型积分有官方公式才折算，金额按 DS Flash 空闲价作购买力参考。未核验、付费与无固定比例的权益不计入已核验总额。"),
]

INPUT_BUDGET_FAQ = [
    ("{name}当前有哪些免费余额？",
     "本页信源核验日期：{updated}。本页收录 {n} 条权益，原始余额、发放周期与特定模型的输入预算单列。延后到账的月赠是否计入首月，以各条规则为准。"),
    FAQ_GEN[1],
    ("{name}的输入预算如何计算？",
     "用原始余额除以对应模型的官方每百万输入 Token 价格，仅计算输入、不估输出。其他共享余额的资源消耗会降低预算。同笔金额不重复折算 DS 购买力；模型输入预算不是跨模型通用 Token 或保证到账量。"),
]

APPLICATION_GATES = {"startup", "audit", "oss"}
APPLICATION_FAQ = [
    ("有哪些申请制计划？", "本站收录 {n} 项计划，包括 {brief}。"),
    ("如何申请？", "点击「查看申请」进入官方页面，核对适用对象、审核材料和额度有效期。"),
    ("额度如何计算？", "各计划按其官方条款和原单位发放额度。"),
]


def slugify(p: str) -> str:
    s = re.sub(r"\s+", "-", p.strip())
    s = re.sub(r"[^\w\u4e00-\u9fff.-]", "", s, flags=re.UNICODE)
    return s.lower() or "p"


def fmt_wan(w):
    return f"{w/10000:.2f} 亿".replace(".00 亿", " 亿") if w >= 10000 else f"{round(w)} 万"


def deal_value(d):
    if d.get("unit") == "tool":
        return "免费工具，无独立 Token 赠额"
    if "token_quota" in d:
        parts = []
        for q in quota_entries(d):
            amount = f"{q['amount']:,.2f}".rstrip("0").rstrip(".")
            unit = q["unit"]
            text = (f"{fmt_wan(q['amount']/10000)} tokens" if unit == "tokens"
                    else ("¥" if unit == "CNY" else "$")+amount if unit in ("CNY", "USD")
                    else amount+{"credits":" 积分", "points":" 算力", "hours":" 小时", "requests":" 次"}.get(unit, unit))
            text += {"daily":"/天", "monthly":"/月", "weekly":"/周"}.get(q.get("period"), "")
            if q.get("starts_after_days"):
                text += "（延后发放，首月按规则排除）"
            parts.append(text)
        value = token_quota(d)["total"]
        if value:
            parts.append("已领礼包总量（新领取待核）" if d.get("quota_basis") == "claimed_pack" else f"首月 ≈ {fmt_wan(value)} Token 参考")
        estimated = daily_estimate(d)
        if estimated:
            period = "daily" if estimated["period"] == "daily" else "month"
            label = "日用量" if period == "daily" else "首月"
            if estimated.get("basis", {}).get("method") == "model_budget":
                value_range = fmt_wan(estimated[period]['low'])
                if estimated[period]['low'] != estimated[period]['high']:
                    value_range += "–"+fmt_wan(estimated[period]['high'])
                parts.append(f"{label}仅输入预算 ≈ {value_range} Token（非通用赠额）")
            else:
                parts.append(f"{label}情景估计 ≈ {fmt_wan(estimated[period]['low'])}–{fmt_wan(estimated[period]['high'])} Token（非保证额度）")
        return "；".join(parts) or "Token 数量以官方页为准"
    parts = []
    if d.get("daily_wan"): parts.append(f"日均 ~{fmt_wan(d['daily_wan'])} tokens")
    if d.get("tokens_wan") or d.get("eq_wan"):
        parts.append(f"一次性 {fmt_wan(d.get('eq_wan') or d.get('tokens_wan'))} 等效")
    if d.get("cny"): parts.append(f"¥{d['cny']} 额度")
    if d.get("usd"): parts.append(f"${d['usd']} credits")
    return "；".join(parts) or "额度以官方页为准"


def esc_quote(s):
    return html.escape(str(s or ""), quote=True)


EVIDENCE_MISSING = "核验日期未知"
EVIDENCE_INVALID = "核验日期无效"
_ISO_RE = re.compile(
    r"(\d{4})-(\d{2})-(\d{2})"
    r"(?:T(\d{2}):(\d{2}):(\d{2})(\.\d+)?(Z|[+-]\d{2}:\d{2})?)?\Z")
# 自指生成戳：它的变化不是内容修改。lastmod 的修改证据比较必须剔除它，
# 否则“页面生成”日期每天一换就等于每日再生伪造全站修改（本任务点名缺陷）。
_GEN_STAMP_RE = re.compile(r"页面生成：\d{4}-\d{2}-\d{2}")


def _content_key(text: str) -> str:
    """内容修改比较键：剔除自指的“页面生成”戳，只看真实内容差异。"""
    return _GEN_STAMP_RE.sub("页面生成：\u200d", text)


def evidence_date(rec, gen_day):
    """从记录的 verified_at 证据字段取核验日期；绝不从生成时间推断。
    返回 (date|None, status)，status ∈ {"valid","missing","invalid"}。
    严格校验：仅接受完整 ISO 日期（YYYY-MM-DD）或完整 ISO 时间戳
    （YYYY-MM-DDTHH:MM:SS[.frac][Z|±HH:MM]）；尾随垃圾（如 2026-11-22garbage）、
    畸形时间（如 T99:99:99Z）、非法偏移（+99:00）、非法日历日期一律 invalid。
    未来日期不是可信核验证据（不假装支持未来时间）。"""
    raw = rec.get("verified_at")
    if raw in (None, ""):
        return None, "missing"
    m = _ISO_RE.match(str(raw))
    if not m:
        return None, "invalid"
    try:
        d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None, "invalid"
    if m.group(4) is not None:
        if int(m.group(4)) > 23 or int(m.group(5)) > 59 or int(m.group(6)) > 59:
            return None, "invalid"
        off = m.group(8)
        if off not in (None, "Z"):
            oh, om = off[1:].split(":")
            if int(oh) > 23 or int(om) > 59:
                return None, "invalid"
    if d > gen_day:
        return None, "invalid"
    return d, "valid"


def evidence_tag(rec, gen_day):
    """逐条信源的核验日期标签（页内“逐条见下”的落点）。"""
    d, status = evidence_date(rec, gen_day)
    if d:
        return f"核验 {d.isoformat()}"
    return EVIDENCE_MISSING if status == "missing" else EVIDENCE_INVALID


def verify_label(records, gen_day):
    """页面级核验标签（诚实口径，不掩盖任何记录）：
      全部有效且同日 -> 单日期；全部有效但日期不同 -> 各条不一（最早~最新）；
      有效 + 缺失/无效 -> 部分未知/无效（n/N 条有核验时间）；
      全无有效证据 -> 未知（全缺失）/ 无效（含无效）/ 未知/无效（混合缺失与无效）。
    绝不把含缺失/无效记录的页面标成全页一致日期。"""
    dated = []
    n_missing = n_invalid = 0
    for r in records:
        d, status = evidence_date(r, gen_day)
        if status == "valid":
            dated.append(d)
        elif status == "missing":
            n_missing += 1
        else:
            n_invalid += 1
    n = len(records)
    if not dated:
        if n_missing and n_invalid:
            return "未知/无效（核验时间缺失或无效）"
        if n_invalid:
            return "无效（核验时间字段无效）"
        return "未知（缺有效核验时间）"
    if n_missing or n_invalid:
        prefix = ("部分未知/无效" if n_missing and n_invalid
                  else "部分未知" if n_missing else "部分无效")
        return f"{prefix}（{len(dated)}/{n} 条有核验时间）"
    lo, hi = min(dated), max(dated)
    return lo.isoformat() if lo == hi else f"各条不一（{lo.isoformat()}~{hi.isoformat()}）"


def verify_short(label):
    """title 括注用的短标签（同一证据口径的紧凑表述）。"""
    for pre in ("未知/无效", "部分未知/无效"):
        if label.startswith(pre):
            return f"信源核验日期{pre}"
    for pre in ("未知", "无效", "部分未知", "部分无效"):
        if label.startswith(pre):
            return f"信源核验日期{pre}"
    if label.startswith("各条不一"):
        return "信源核验日期不一"
    return f"信源核验 {label}"


COLL_TPL = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://tokenmost.com/{slug_enc}.html">
<meta property="og:title" content="{title} — tokenmost">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://tokenmost.com/{slug_enc}.html">
<meta property="og:image" content="https://tokenmost.com/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://tokenmost.com/og-image.png">
<script type="application/ld+json">{ld_item}</script>
<script type="application/ld+json">{ld_faq}</script>
<style>body{{font-family:-apple-system,"PingFang SC",sans-serif;max-width:900px;margin:0 auto;padding:24px 16px;line-height:1.7;color:#1a2b22}}h1{{color:#059669;font-size:1.5rem}}h2{{font-size:1.15rem;margin-top:28px;border-left:4px solid #059669;padding-left:10px}}table{{border-collapse:collapse;width:100%;font-size:.9rem}}td,th{{border:1px solid #d8e4dd;padding:8px 10px;text-align:left}}th{{background:#ecfdf5}}a{{color:#059669}}.up{{font-size:.78rem;color:#6b7280}}.faq h3{{font-size:1rem;margin:18px 0 6px}}</style>
</head><body>
<p class="up"><a href="/">← tokenmost 免费羊毛情报站</a> · 数据每日核验 · 信源核验：{updated} · 页面生成：{gen}</p>
<h1>{h1}</h1>
<p>{intro}</p>
<h2>一图看懂：{n} 个平台怎么选</h2>
<table><tr><th>平台</th><th>免费给什么</th><th>关键限制</th><th>详情</th></tr>{rows}</table>
<h2>常见问题</h2>
<div class="faq">{faq}</div>
<p>更多品类：<a href="/guides/cloud-mail-email.html">0 元搭无限邮箱</a> · <a href="/guides/free-tier-survival.html">海外免费层生存指南</a> · <a href="/">每日 token 羊毛情报流</a>（RSS 可订阅）</p>
</body></html>"""

def main():
    deals = json.load(open(ROOT / "deals.json", encoding="utf-8"))
    guides = json.load(open(GDIR / "index.json", encoding="utf-8")) if (GDIR / "index.json").exists() else []
    today = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")  # 生成时钟：仅作“页面生成”展示，不作核验声明
    gen_day = date(*map(int, today.split("-")))
    groups = {}
    for d in deals:
        if not d.get("published") or d.get("category") == "intel_source":
            continue
        g = d.get("group") or d["provider"]
        groups.setdefault(g, []).append(d)

    OUT.mkdir(exist_ok=True)
    # 页面实际内容修改证据：写盘前先读当前已部署产物（之后才清空重建）。
    # 内容比较剔除自指“页面生成”戳（_content_key）：新旧内容键不同 =
    # 本次生成真实修改了该页内容 -> lastmod=本次运行日；相同 = 未修改 ->
    # 省略 lastmod（sitemaps.org 可选语义，不伪造，也不把再生日当修改日）。
    old_pages = {f.stem: f.read_text(encoding="utf-8") for f in OUT.glob("*.html")}
    for f in OUT.glob("*.html"):
        f.unlink()
    _coll_path = ROOT / "free-cloud-servers.html"
    old_coll = _coll_path.read_text(encoding="utf-8") if _coll_path.exists() else None
    old_llms = (ROOT / "llms.txt").read_text(encoding="utf-8") if (ROOT / "llms.txt").exists() else None
    old_llms_full = (ROOT / "llms-full.txt").read_text(encoding="utf-8") if (ROOT / "llms-full.txt").exists() else None
    pages = []
    for g, ds in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        name = g.split("（")[0].strip()
        slug = slugify(g)
        layer = LAYER.get(ds[0]["category"], "")
        vlabel = verify_label(ds, gen_day)
        vshort = verify_short(vlabel)
        verified = sum(1 for d in ds if d.get("verify_status") == "verified")
        available = [d for d in ds if d.get("gate") not in APPLICATION_GATES]
        application_only = not available
        input_budget = any(e.get("method") == "model_budget" for d in ds for e in d.get("quota_estimates", []))
        amounts = [token_quota(d) for d in available if free_quota(d) and d.get("verify_status") == "verified"]
        once = sum(q["once"] for q in amounts)
        daily = sum(q["daily"] for q in amounts)
        monthly = sum(q["monthly"] for q in amounts)
        total = sum(q["total"] for q in amounts)
        total_s = fmt_wan(total) if total else "暂无可折算总额"
        brief = "、".join(d["provider"] for d in ds[:3])
        title = f"{name}额度领取攻略：{total_s} 已核验首月参考（{vshort}）"
        desc = f"{name}免费 token 额度大全：{len(ds)} 条信源（{verified} 条已验证），{deal_value(ds[0])}。附适用条件、逐条核验日期与官方入口。"
        h1 = f"{name}额度大全：已核验首月参考 {total_s}"
        intro = (f"本页聚合 {name}（{layer}）全部 {len(ds)} 条额度与折扣情报，其中 {verified} 条已验证。"
                 f"已核验首月参考约 <b>{total_s}</b>（一次性、活动有效期内日额度及月额度；金额仅作 DS Flash 购买力比较，实际额度见下方原单位）。"
                 f"tokenmost 每日核验，过期自动清洗。")
        if application_only:
            title = f"{name}申请指南（{vshort}）"
            h1 = f"{name}申请指南"
            desc = f"收录 {len(ds)} 项申请制权益，附官方资格、额度和申请入口。"
            intro = f"本页收录 {len(ds)} 项申请制权益，其中 {verified} 项已核验。请按各计划的官方条件申请。"
        elif input_budget:
            title = f"{name}额度领取攻略：免费余额与模型输入预算（{vshort}）"
            h1 = f"{name}免费余额与模型输入预算"
            intro = f"本页收录 {name} 的 {len(ds)} 条权益，其中 {verified} 条已核验。原始余额、发放周期与特定模型的输入预算分开展示；输入预算不含输出，同笔余额不重复折算 DS 购买力。"
        elif not total:
            if all(d.get("verify_status") == "expired" for d in ds):
                subject = "历史活动与截止日期"
            elif not verified:
                subject = "额度线索与核验进度"
            elif all(d.get("quota_paid") or d.get("type") in ("pricing_plan","paid_discount","price_low") for d in ds):
                subject = "套餐价格与使用条件"
            else:
                subject = "额度规则、使用限制与入口"
            h1 = f"{name} · {subject}"
            title = f"{h1} | TokenMost"
            primary = next((d for d in ds if d.get("verify_status") == "verified"), ds[0])
            status = "已核验" if primary.get("verify_status") == "verified" else "历史记录" if primary.get("verify_status") == "expired" else "待复核"
            desc = f"{status} · {primary['value'][:100]}。查看对应来源和核验日期。"
            intro = f"本站收录 {len(ds)} 条 {esc_quote(name)} 记录。下方列出每条记录的原始单位、适用条件和核验状态。"
        blocks = []
        for d in sorted(ds, key=lambda x: -token_quota(x)["total"]-(daily_estimate(x) or {"month":{"typical":0}})["month"]["typical"]):
            tag = TYPE.get(d.get("type"), d.get("type", ""))
            badge = "已失效" if d.get("verify_status") == "expired" else "✅ 已领实测 · 新领取待核" if d.get("quota_basis") == "claimed_pack" else "✅ 已验证" if d.get("verify_status") == "verified" else "⚠️ 待复核"
            vtag = evidence_tag(d, gen_day)
            dl = f' <span style="color:var(--red)">📅 {esc_quote(d["deadline"])}</span>' if d.get("deadline") else ""
            action = "查看历史条款" if d.get("verify_status") == "expired" else "查看入口" if d.get("claim_status") == "window_unconfirmed" else "获取工具" if d.get("unit") == "tool" else "查看活动" if d.get("starts_at") else "查看申请" if d.get("gate") in APPLICATION_GATES else "查看套餐" if d.get("quota_paid") or d.get("type") == "pricing_plan" else "立即领取"
            definitions = d.get("quota_estimates", [d["daily_estimate"]] if d.get("daily_estimate") else [])
            estimate_note = (f'<p>估算假设：{esc_quote(estimate_assumption(d))} {esc_quote("；".join(e["note"] for e in definitions))} '
                             f'<a href="/?q={esc_quote(d["id"])}">调整假设 / 查看完整估计 →</a></p>') if daily_estimate(d) else ""
            blocks.append(
                f'<div class="deal" id="deal-{esc_quote(d["id"])}"><b>{esc_quote(d["value"][:80])}{"…" if len(d["value"])>80 else ""}</b>'
                f'<span class="tag">{esc_quote(tag)}</span><span class="tag">{badge}</span><span class="tag">{esc_quote(vtag)}</span>{dl}'
                f'<p>💰 {esc_quote(deal_value(d))} ｜ 📐 {esc_quote(d.get("rule","以官方页为准")[:90])}</p>'
                + estimate_note +
                f'<a class="go" href="{esc_quote(d["url"])}" target="_blank" rel="noopener nofollow">{action} →</a>'
                + ('<p><a href="../guides/kimi-guide.html">查看 Kimi API 15 元券领取攻略 →</a></p>'
                   if d["id"] == "kimi-voucher" else "")
                + '</div>')
        faq_blocks = []
        faq_items = []
        for q_t, a_t in APPLICATION_FAQ if application_only else INPUT_BUDGET_FAQ if input_budget else FAQ_GEN:
            q = q_t.format(name=name, updated=vlabel, n=len(ds), brief=brief)
            a = a_t.format(name=name, updated=vlabel, n=len(ds), brief=brief, total=total_s)
            faq_blocks.append(f"<details><summary>{esc_quote(q)}</summary><p>{esc_quote(a)}</p></details>")
            faq_items.append({"q": q, "a": a})
        ld_web = json.dumps({"@context": "https://schema.org", "@type": "WebPage", "name": title,
                             "url": f"https://tokenmost.com/platform/{slug}.html", "inLanguage": "zh-CN",
                             "isPartOf": {"@type": "WebSite", "name": "tokenmost.com", "url": "https://tokenmost.com/"}},
                            ensure_ascii=False)
        ld_faq = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                             "mainEntity": [{"@type": "Question", "name": it["q"],
                                             "acceptedAnswer": {"@type": "Answer", "text": it["a"]}} for it in faq_items]},
                            ensure_ascii=False)
        robots_meta = '<meta name="robots" content="noindex,follow">\n' if (verified == 0 and len(ds) < 3) else ''
        page = TPL.format(title=esc_quote(title), desc=esc_quote(desc), slug=slug, slug_enc=quote(slug), h1=h1, robots=robots_meta,
                          updated=vlabel, gen=today, layer=layer, n=len(ds), intro=intro,
                          metric="额度按官方单位列出" if application_only else "原始余额 + 仅输入预算" if input_budget else "原始额度 + 有依据的 Token 折算 / 购买力参考",
                          offers_heading="申请计划" if application_only else "🎁 当前可领额度与羊毛",
                          faq_heading="申请常见问题" if application_only else f"❓ {esc_quote(name)}免费额度常见问题",
                          deals="\n".join(blocks), faq="\n".join(faq_blocks),
                          ld_web=ld_web, ld_faq=ld_faq)
        (OUT / f"{slug}.html").write_text(page, encoding="utf-8")
        old_page = old_pages.get(slug)
        page_lm = gen_day.isoformat() if old_page is None or _content_key(old_page) != _content_key(page) else None
        pages.append({"slug": slug, "name": name, "category": ds[0]["category"], "has_total": bool(total), "n": len(ds), "verified": verified, "total": total_s,
                      "url": f"https://tokenmost.com/platform/{slug}.html",
                      "title": title, "desc": desc, "application_only": application_only,"input_budget": input_budget,
                      "lastmod": page_lm})

    write_discovery(ROOT, pages, guides, deals, slugify, LAYER)

    # llms.txt（AI 搜索站点地图）
    lines = ["# tokenmost.com", "",
             "> AI 大模型额度与折扣情报站：原始额度、有官方公式的 Token 折算与 DS Flash 金额购买力参考分开显示。已核验首月参考排除付费订阅、申请制和无固定比例的权益。", "",
             "## Entity", "",
             "- Name: TokenMost",
             "- URL: https://tokenmost.com/",
             "- Type: AI token deals intelligence site",
             "- Data freshness: per-offer verification status and dates; historical and pending records are retained",
             "- Metric: native tokens, requests, credits, and purchasing-power scenarios reported separately",
             "- Open data: deals.json / llms-full.txt / rss.xml / verified.xml",
             "- Free API comparison: https://tokenmost.com/free-ai-api.html",
             "- Platform directory: https://tokenmost.com/platform/",
             "- Contact: no signup required, site is fully public", ""]
    lines += ["## 平台免费额度页", ""]
    for p in sorted(pages, key=lambda x: -x["n"]):
        label = (f"{p['name']}申请指南（{p['n']} 项）" if p["application_only"]
                 else f"{p['name']}免费余额与输入预算（{p['n']} 条信源）" if p["input_budget"]
                 else f"{p['name']}首月额度参考（{p['total']}）" if p["has_total"] else p["name"]+"额度规则与来源")
        lines.append(f"- [{label}]({p['url']}): {p['desc'][:80].rstrip()}")
    lines += ["", "## 领取攻略", ""]
    for g in guides:
        lines.append(f"- [{g['title']}](https://tokenmost.com/guides/{g['id']}.html): {g.get('desc','')[:80]}")
    lines += ["", "## 动态情报", "", "- [RSS 情报流](https://tokenmost.com/rss.xml): 每日更新的全部平台羊毛情报"]
    llms_content = "\n".join(lines) + "\n"
    (ROOT / "llms.txt").write_text(llms_content, encoding="utf-8")
    llms_lm = gen_day.isoformat() if old_llms != llms_content else None
    full = ["# tokenmost.com — 全量情报（Markdown 版）", ""]
    for d in deals:
        if not d.get("published"):
            continue
        full.append(f"## {d['provider']}｜{TYPE.get(d.get('type'), d.get('type',''))}")
        full.append(f"- 内容：{d['value']}")
        if d.get("rule"): full.append(f"- 规则：{d['rule']}")
        if d.get("daily_note"): full.append(f"- 日均：{d['daily_note']}")
        full.append(f"- 链接：{d['url']}")
        full.append(f"- 状态：{'已验证' if d.get('verify_status')=='verified' else '待复核'}（核验时间 {d.get('verified_at','—')}）\n")
    llms_full_content = "\n".join(full) + "\n"
    (ROOT / "llms-full.txt").write_text(llms_full_content, encoding="utf-8")
    llms_full_lm = gen_day.isoformat() if old_llms_full != llms_full_content else None


    # ===== 品类聚合页（长尾词 landing）：免费云服务器/域名/GPU =====
    coll_specs = [
        ("free-cloud-servers", "免费云服务器大全 2026：{n} 个平台可白嫖（长期免费+注册赠送）",
         "免费云服务器怎么选？本文聚合 {n} 个真实可领的平台：Oracle/Azure/GCP/AWS 大厂免费层、免卡 VPS、免费域名、AI 云电脑与 192G 显存 GPU，全部标注限制与续期规则，每日核验。",
         "freecloud"),
    ]
    coll_lm = None
    for slug, t_tpl, d_tpl, cat in coll_specs:
        cd = [d for d in deals if d.get("category") == cat and d.get("published", True) and d.get("verify_status") != "expired"]
        if len(cd) < 5:
            continue
        n = len(cd)
        cvlabel = verify_label(cd, gen_day)
        title = t_tpl.format(n=n); desc = d_tpl.format(n=n)
        h1 = "免费云服务器与免费域名大全（2026 实测 " + str(n) + " 平台）"
        intro = "免费云服务器真正的门槛不是能不能领，而是能不能稳定用。本文只收录当前仍可申请的平台，统一标注配置、续期规则与隐藏成本；数据每日核验，失效自动下架。搭配 <a href='/guides/cloud-mail-email.html'>0 元无限邮箱</a> 与 <a href='/guides/free-tier-survival.html'>海外免费层生存指南</a> 使用效果最佳。"
        rows = ""
        for d in sorted(cd, key=lambda x: -(x.get("eq_wan") or x.get("tokens_wan") or 0)):
            lim = (d.get("rule") or "详见平台")[:60].replace("|", "·")
            u = d.get("url", "#"); nm = d.get("provider", "")
            rows += "<tr><td><a href='" + u + "' rel='nofollow noopener' target='_blank'>" + html.escape(str(nm)) + "</a></td><td>" + html.escape(str(d.get("value", ""))[:80]) + "</td><td>" + html.escape(lim) + "</td><td><a href='https://tokenmost.com/platform/" + html.escape(slugify(str(d.get('group') or d.get('provider','')))) + ".html'>详情</a></td></tr>"
        faq = (
            "<h3>免费云服务器真的永久免费吗？</h3><p>Oracle Always Free、Azure 12 个月免费服务等「Always Free/长期免费」档在账号存续期有效，但 Oracle 2026 年已把 A1 配额砍半（4核24G→2核12G），且纯免费账号有闲置回收（7 天利用率低于 20% 会被停）——不要把重要数据只存一份在免费机上。</p>"
            "<h3>免绑卡的免费 VPS 靠谱吗？</h3><p>免卡、免费、长期可用是三个独立条件。纯 IPv6/NAT 小鸡适合练手，注册商随时可能改规则（deSEC 2026-10 已停新注册）；正经业务请上大厂免费层或付费。</p>"
            "<h3>怎么把免费服务器用出价值？</h3><p>推荐 0 元链路：免费域名托管 Cloudflare（免费 DNS/CDN/证书）→ 服务跑 InstaBox/Oracle 免费机 → 邮箱用 <a href='/guides/cloud-mail-email.html'>cloud-mail 无限邮箱</a>（Cloudflare Email Routing 免费收信）→ 监控走免费额度。全链路 0 元。</p>")
        ld_item = json.dumps({"@context": "https://schema.org", "@type": "ItemList",
                              "name": title, "itemListElement": [
                                  {"@type": "ListItem", "position": i + 1, "name": html.escape(str(d.get("provider", ""))),
                                   "description": html.escape(str(d.get("value", ""))[:100])}
                                  for i, d in enumerate(sorted(cd, key=lambda x: -(x.get("eq_wan") or x.get("tokens_wan") or 0)))]},
                             ensure_ascii=False)
        ld_faq = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q.split("？")[0] + "？", "acceptedAnswer": {"@type": "Answer", "text": a[:200]}}
            for q, a in [("免费云服务器真的永久免费吗？", "Oracle Always Free 等长期档在账号存续期有效，但 2026 年配额已砍半且有闲置回收规则。"),
                          ("免绑卡的免费 VPS 靠谱吗？", "免卡/免费/长期可用是三个独立条件，适合练手不适合业务。"),
                          ("怎么 0 元搭一套服务？", "免费域名+Cloudflare+免费算力机+cloud-mail 邮箱，全链路 0 元。")]]},
                           ensure_ascii=False)
        page = COLL_TPL.format(title=esc_quote(title), desc=esc_quote(desc), slug=slug, slug_enc=quote(slug),
                               h1=esc_quote(h1), intro=intro, n=n, rows=rows, faq=faq,
                               ld_item=ld_item, ld_faq=ld_faq, updated=cvlabel, gen=today)
        (ROOT / (slug + ".html")).write_text(page, encoding="utf-8")
        coll_lm = gen_day.isoformat() if old_coll is None or _content_key(old_coll) != _content_key(page) else None
        print(f"品类聚合页: {slug}.html（{n} 平台）")

    # sitemap 并入 platform 页
    sm = ['<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    # lastmod 只写有“页面内容被本次生成真实修改”证据的 URL（sitemaps.org：
    # lastmod 应为链接页面最后被修改的日期，而非 sitemap 生成日，更不是信源核验日）：
    #   platform/聚合页 —— 内容键（剔除自指“页面生成”戳）不同 -> 本次运行日；相同 -> 省略；
    #   llms.txt/llms-full.txt —— 无自指戳，直接字节比较，不同 -> 本次运行日；
    #   首页/en.html/guides/rss.xml —— 本生成器从不写这些文件，永无修改证据 -> 省略。
    urls = [("https://tokenmost.com/", None, "daily", "1.0"),
            ("https://tokenmost.com/en.html", None, "daily", "0.9"),
            ("https://tokenmost.com/free-cloud-servers.html", coll_lm, "daily", "0.9")]
    urls += [("https://tokenmost.com/"+path,None,"daily","0.9") for path in ("free-ai-api.html","platform/","guides/")]
    sm_pages = [p for p in pages if not (p["verified"] == 0 and p["n"] < 3)]
    urls += [(p["url"], p["lastmod"], "daily", "0.9") for p in sorted(sm_pages, key=lambda x: -x["n"])]
    urls += [(f"https://tokenmost.com/guides/{g['id']}.html", None, "weekly", "0.8") for g in guides]
    urls += [("https://tokenmost.com/llms.txt", llms_lm, "daily", "0.5"),
             ("https://tokenmost.com/llms-full.txt", llms_full_lm, "daily", "0.5"),
             ("https://tokenmost.com/rss.xml", None, "daily", "0.6")]
    _SAFE = ':/?&='
    n_lm = 0
    for loc, mod, freq, pri in urls:
        lm = f"\n    <lastmod>{mod}</lastmod>" if mod else ""
        n_lm += bool(mod)
        sm.append(f"  <url>\n    <loc>{quote(loc, safe=_SAFE)}</loc>{lm}\n    <changefreq>{freq}</changefreq>\n    <priority>{pri}</priority>\n  </url>")
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")

    print(f"pSEO: platform/ {len(pages)} 页 + llms.txt + llms-full.txt + sitemap {len(urls)} URL（{n_lm} 个带证据 lastmod）")


if __name__ == "__main__":
    main()
