#!/usr/bin/env python3
"""程序化 SEO（pSEO）：deals.json 按平台聚合生成静态落地页 + llms.txt。
被 check.py 末尾调用；pages.yml 需复制 platform/ 目录。纯标准库。
产出：
  platform/<slug>.html —— 每平台一页（title/desc/JSON-LD/FAQ/h1 全套，承接长尾词）
  llms.txt / llms-full.txt —— AI 搜索（ChatGPT/Perplexity）站点地图
"""
import json, html, re
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "platform"
GDIR = ROOT / "guides"

LAYER = {"official_cn": "大模型官方（国内）", "agent": "Agent 平台", "compute": "算力平台",
         "reseller": "Token 中间商", "official_global": "大模型官方（海外）", "maas": "MaaS 平台（云上托管）"}
TYPE = {"signup_bonus": "注册赠送", "free_tier": "长期免费", "limited_promo": "限时活动",
        "recurring_promo": "长期活动", "free_model": "免费模型", "student": "学生通道", "invite_bonus": "邀请奖励"}

TPL = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://tokenmost.com/platform/{slug}.html">
<meta property="og:title" content="{title} — tokenmost">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://tokenmost.com/platform/{slug}.html">
<meta name="twitter:card" content="summary">
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
</style></head><body>
<a class="back" href="/">← 回 tokenmost 情报流</a>
<h1>{h1}</h1>
<p class="sub">更新于 {updated} · {layer} · 共 {n} 条信源 · 全站计量基准：DeepSeek V4.1 Flash 等效</p>
<p>{intro}</p>
<h2>🎁 当前可领额度与羊毛</h2>
{deals}
<h2>❓ {name}免费额度常见问题</h2>
{faq}
<div class="rel">继续看：<a href="/">全部平台情报流</a><a href="/guides/coding-plan-guide.html">Coding Plan 选购攻略</a><a href="/guides/free-tier-survival.html">海外免费层生存指南</a><a href="/rss.xml">RSS 订阅</a></div>
</body></html>"""

FAQ_GEN = [
    ("{name}现在有什么免费额度？",
     "截至 {updated}，{name}在 tokenmost 收录的免费羊毛共 {n} 条：{brief}。所有额度统一折算 DeepSeek V4.1 Flash 等效 token，可在本页与全平台横向比较。"),
    ("{name}免费额度怎么领取？",
     "点击本页各条「立即领取」直达官方页面，按官方规则注册/实名/激活即可；限时活动请留意截止日期。tokenmost 每日核验各条状态，失效信息自动清洗。"),
    ("{name}的免费额度能用多少 token？",
     "tokenmost 按 DS Flash 等效统一计量：一次性额度与每日刷新额度分开标注，「首月可薅总量 = 一次性 + 日均 × 30 天」。本页各条收益列即等效 token 数。"),
]


def slugify(p: str) -> str:
    s = re.sub(r"\s+", "-", p.strip())
    s = re.sub(r"[^\w\u4e00-\u9fff.-]", "", s, flags=re.UNICODE)
    return s.lower() or "p"


def fmt_wan(w):
    return f"{w/10000:.2f} 亿".replace(".00 亿", " 亿") if w >= 10000 else f"{round(w)} 万"


def deal_value(d):
    parts = []
    if d.get("daily_wan"): parts.append(f"日均 ~{fmt_wan(d['daily_wan'])} tokens")
    if d.get("tokens_wan") or d.get("eq_wan"):
        parts.append(f"一次性 {fmt_wan(d.get('eq_wan') or d.get('tokens_wan'))} 等效")
    if d.get("cny"): parts.append(f"¥{d['cny']} 额度")
    if d.get("usd"): parts.append(f"${d['usd']} credits")
    return "；".join(parts) or "额度以官方页为准"


def esc_quote(s):
    return html.escape(str(s or ""), quote=True)


COLL_TPL = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://tokenmost.com/{slug}.html">
<meta property="og:title" content="{title} — tokenmost">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<script type="application/ld+json">{ld_item}</script>
<script type="application/ld+json">{ld_faq}</script>
<style>body{{font-family:-apple-system,"PingFang SC",sans-serif;max-width:900px;margin:0 auto;padding:24px 16px;line-height:1.7;color:#1a2b22}}h1{{color:#059669;font-size:1.5rem}}h2{{font-size:1.15rem;margin-top:28px;border-left:4px solid #059669;padding-left:10px}}table{{border-collapse:collapse;width:100%;font-size:.9rem}}td,th{{border:1px solid #d8e4dd;padding:8px 10px;text-align:left}}th{{background:#ecfdf5}}a{{color:#059669}}.up{{font-size:.78rem;color:#6b7280}}.faq h3{{font-size:1rem;margin:18px 0 6px}}</style>
</head><body>
<p class="up"><a href="/">← tokenmost 免费羊毛情报站</a> · 数据每日核验 · {updated} 更新</p>
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
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    groups = {}
    for d in deals:
        if not d.get("published") or d.get("category") == "intel_source":
            continue
        g = d.get("group") or d["provider"]
        groups.setdefault(g, []).append(d)

    OUT.mkdir(exist_ok=True)
    for f in OUT.glob("*.html"):
        f.unlink()
    pages = []
    for g, ds in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        name = g.split("（")[0].strip()
        slug = slugify(g)
        layer = LAYER.get(ds[0]["category"], "")
        verified = sum(1 for d in ds if d.get("verify_status") == "verified")
        once = sum(d.get("eq_wan") or d.get("tokens_wan") or 0 for d in ds)
        daily = sum(d.get("daily_wan") or 0 for d in ds)
        total = once + daily * 30
        total_s = fmt_wan(total) if total else "待公布"
        brief = "、".join(d["provider"] for d in ds[:3])
        title = f"{name}免费额度领取攻略：{total_s} DS Flash 等效可薅（{today} 核验）"
        desc = f"{name}免费 token 额度大全：{len(ds)} 条信源（{verified} 条已验证），{deal_value(ds[0])}。每日核验、失效即清，附领取步骤与常见问题。"
        h1 = f"{name}免费额度大全：首月可薅 {total_s} DS Flash 等效"
        intro = (f"本页聚合 {name}（{layer}）全部 {len(ds)} 条免费额度情报，其中 {verified} 条已验证。"
                 f"首月可薅总量约 <b>{total_s}</b> DS Flash 等效 token（一次性 {fmt_wan(once) if once else '—'} ＋ 日均 {fmt_wan(daily) if daily else '—'} × 30 天）。"
                 f"tokenmost 每日核验，过期自动清洗。")
        blocks = []
        for d in sorted(ds, key=lambda x: -(x.get("eq_wan") or x.get("tokens_wan") or 0) - (x.get("daily_wan") or 0) * 30):
            tag = TYPE.get(d.get("type"), d.get("type", ""))
            badge = "✅ 已验证" if d.get("verify_status") == "verified" else "⚠️ 待复核"
            dl = f' <span style="color:var(--red)">📅 {esc_quote(d["deadline"])}</span>' if d.get("deadline") else ""
            blocks.append(
                f'<div class="deal"><b>{esc_quote(d["value"][:80])}{"…" if len(d["value"])>80 else ""}</b>'
                f'<span class="tag">{esc_quote(tag)}</span><span class="tag">{badge}</span>{dl}'
                f'<p>💰 {esc_quote(deal_value(d))} ｜ 📐 {esc_quote(d.get("rule","以官方页为准")[:90])}</p>'
                f'<a class="go" href="{esc_quote(d["url"])}" target="_blank" rel="noopener nofollow">立即领取 →</a></div>')
        faq_blocks = []
        faq_items = []
        for q_t, a_t in FAQ_GEN:
            q = q_t.format(name=name, updated=today, n=len(ds), brief=brief)
            a = a_t.format(name=name, updated=today, n=len(ds), brief=brief, total=total_s)
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
        page = TPL.format(title=esc_quote(title), desc=esc_quote(desc), slug=slug, h1=h1,
                          updated=today, layer=layer, n=len(ds), intro=intro,
                          deals="\n".join(blocks), faq="\n".join(faq_blocks),
                          name=esc_quote(name), ld_web=ld_web, ld_faq=ld_faq)
        (OUT / f"{slug}.html").write_text(page, encoding="utf-8")
        pages.append({"slug": slug, "name": name, "n": len(ds), "total": total_s,
                      "url": f"https://tokenmost.com/platform/{slug}.html",
                      "title": title, "desc": desc})

    # llms.txt（AI 搜索站点地图）
    lines = ["# tokenmost.com", "",
             "> AI 大模型免费额度与折扣码情报站：聚合大模型官方、Agent 平台、MaaS 云、算力中心与 token 中间商的免费额度情报，每日核验，统一折算 DeepSeek V4.1 Flash 等效 token。", ""]
    lines += ["## 平台免费额度页", ""]
    for p in sorted(pages, key=lambda x: -x["n"]):
        lines.append(f"- [{p['name']}免费额度（{p['total']}可薅，{p['n']} 条信源）]({p['url']}): {p['desc'][:80]}")
    lines += ["", "## 领取攻略", ""]
    for g in guides:
        lines.append(f"- [{g['title']}](https://tokenmost.com/guides/{g['id']}.html): {g.get('desc','')[:80]}")
    lines += ["", "## 动态情报", "", "- [RSS 情报流](https://tokenmost.com/rss.xml): 每日更新的全部平台羊毛情报"]
    (ROOT / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
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
    (ROOT / "llms-full.txt").write_text("\n".join(full) + "\n", encoding="utf-8")


    # ===== 品类聚合页（长尾词 landing）：免费云服务器/域名/GPU =====
    coll_specs = [
        ("free-cloud-servers", "免费云服务器大全 2026：{n} 个平台可白嫖（长期免费+注册赠送）",
         "免费云服务器怎么选？本文聚合 {n} 个真实可领的平台：Oracle/Azure/GCP/AWS 大厂免费层、免卡 VPS、免费域名、AI 云电脑与 192G 显存 GPU，全部标注限制与续期规则，每日核验。",
         "freecloud"),
    ]
    for slug, t_tpl, d_tpl, cat in coll_specs:
        cd = [d for d in deals if d.get("category") == cat and d.get("published", True) and d.get("verify_status") != "expired"]
        if len(cd) < 5:
            continue
        n = len(cd)
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
        page = COLL_TPL.format(title=esc_quote(title), desc=esc_quote(desc), slug=slug,
                               h1=esc_quote(h1), intro=intro, n=n, rows=rows, faq=faq,
                               ld_item=ld_item, ld_faq=ld_faq, updated=today)
        (ROOT / (slug + ".html")).write_text(page, encoding="utf-8")
        print(f"品类聚合页: {slug}.html（{n} 平台）")

    # sitemap 并入 platform 页
    sm = ['<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    urls = [("https://tokenmost.com/", today, "daily", "1.0"),
            ("https://tokenmost.com/en.html", today, "daily", "0.9"),
            ("https://tokenmost.com/free-cloud-servers.html", today, "daily", "0.9")]
    urls += [(p["url"], today, "daily", "0.9") for p in sorted(pages, key=lambda x: -x["n"])]
    urls += [(f"https://tokenmost.com/guides/{g['id']}.html", today, "weekly", "0.8") for g in guides]
    urls += [("https://tokenmost.com/llms.txt", today, "daily", "0.5"),
             ("https://tokenmost.com/llms-full.txt", today, "daily", "0.5"),
             ("https://tokenmost.com/rss.xml", today, "daily", "0.6")]
    for loc, mod, freq, pri in urls:
        sm.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{mod}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{pri}</priority>\n  </url>")
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")

    print(f"pSEO: platform/ {len(pages)} 页 + llms.txt + llms-full.txt + sitemap {len(urls)} URL")


if __name__ == "__main__":
    main()
