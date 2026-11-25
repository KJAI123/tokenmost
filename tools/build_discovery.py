"""Build public browsing and subscription entry points from the catalogue used by build_seo."""
import html
from collections import defaultdict
from datetime import datetime, timezone
from email.utils import format_datetime
from urllib.parse import quote
from xml.etree import ElementTree as ET
from token_math import entries, free, _active_days

HOST = 'https://tokenmost.com'
esc = html.escape
NAV = '<nav aria-label="主导航"><a class="brand" href="/">TokenMost</a><a href="/free-ai-api.html">免费 API 对比</a><a href="/platform/">平台目录</a><a href="/guides/">领取攻略</a></nav>'


def page(title, desc, url, body, surface, *, verified_feed='/verified.xml'):
    canonical = HOST + url
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · TokenMost</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{canonical}">
<meta property="og:title" content="{esc(title)} · TokenMost"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}"><meta property="og:type" content="website"><meta property="og:image" content="{HOST}/og-image.png">
<meta name="twitter:card" content="summary_large_image"><link rel="alternate" type="application/rss+xml" title="已核验免费权益" href="{verified_feed}">
<link rel="stylesheet" href="/assets/discovery.css"><script defer src="/assets/engagement.js"></script></head>
<body data-surface="{surface}"><header>{NAV}</header><main><h1>{esc(title)}</h1><p class="intro">{esc(desc)}</p>{body}</main>
<footer><a href="{verified_feed}">订阅免费权益 RSS</a><button type="button" data-share-page hidden>分享本页</button><span role="status" data-share-status></span></footer></body></html>
'''


def write_discovery(root, pages, guides, deals, slugify, layers):
    by_layer = defaultdict(list)
    for p in sorted(pages, key=lambda v:v['name'].casefold()):
        by_layer[p['category']].append(p)
    sections = []
    for layer, members in by_layer.items():
        items = ''.join(f'<li><a href="/platform/{quote(m["slug"])}.html">{esc(m["name"])}</a><small>{m["verified"]} 条已核验 / 共 {m["n"]} 条</small></li>' for m in members)
        sections.append(f'<section><h2>{esc(layers.get(layer,"云服务与工具"))}</h2><ul class="grid">{items}</ul></section>')
    (root/'platform/index.html').write_text(page('AI 平台免费额度目录','按平台查当前额度、核验日期和官方领取入口。','/platform/','<p><a href="/free-cloud-servers.html">免费云服务器与开发资源</a></p>'+''.join(sections),'directory'))
    links = ''.join(f'<li><a href="{quote(g["id"])}.html">{esc(g["title"])}</a></li>' for g in guides)
    (root/'guides/index.html').write_text(page('AI 免费额度领取攻略','从注册、接入到检查用量，按你正在使用的平台选择教程。','/guides/',f'<ul class="guides">{links}</ul>','directory'))

    eligible = [d for d in deals if free(d) and d.get('verify_status')=='verified' and _active_days(d)
                and d.get('gate')!='student' and d.get('type') not in ('student','paid_discount')]
    def detail(d):
        return '/platform/'+quote(slugify(d.get('group') or d['provider']))+'.html#deal-'+quote(d['id'])
    native, others = [], []
    for d in eligible:
        for q in entries(d):
            if q.get('period') not in ('daily','weekly','monthly') or q.get('starts_after_days'): continue
            unit = q['unit']
            if unit=='tokens': dest=native
            elif unit in ('requests','neurons') and d.get('api_via') in ('api','gateway') and d.get('sources'): dest=others
            else: continue
            quantity = f'{q["amount"]:,}' + {'tokens':' Token','requests':' 次','neurons':' Neurons'}[unit]
            period = {'daily':'天','weekly':'周','monthly':'月'}[q['period']]
            note = d.get('rule') or d.get('value','')
            dest.append((d['provider'],f'<article><h3><a href="{esc(detail(d))}">{esc(d["provider"])}</a></h3>'
                         f'<p class="quota">{quantity} / {period}</p><p>{esc(q.get("model",""))}</p>'
                         f'<p>{esc(note)}</p><small>核验 {esc(d["verified_at"][:10])}'+(f' · 截止 {esc(d["deadline"][:10])}' if d.get('deadline') else '')+'</small>'
                         f'<p><a class="claim" data-claim href="{esc(d["url"])}" rel="noopener nofollow">查看领取入口 ↗</a></p></article>'))
    def cards(rows):
        return '<div class="cards">'+''.join(card for _,card in sorted(rows))+'</div>'
    body = f'<section><h2>按 Token 发放</h2>{cards(native)}</section><section><h2>按调用次数或算力发放</h2>{cards(others)}</section>'
    (root/'free-ai-api.html').write_text(page(
        '免费 AI API 额度对比',
        '按平台比较每日或每月刷新的免费上限、适用模型和账号条件。EdgeOne 单列内置模型权益。',
        '/free-ai-api.html', body, 'comparison', verified_feed=f'{HOST}/verified.xml',
    ))

    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss,'channel')
    for name,value in [('title','TokenMost · 已核验免费权益'),('link',HOST+'/free-ai-api.html'),('description','按最近核验时间排序，保留原始额度与官方领取入口。'),('language','zh-CN')]:
        ET.SubElement(channel,name).text=value
    for d in sorted((d for d in eligible if d.get('type') not in ('info','tool_integration') and entries(d)),key=lambda row:(row['verified_at'],row['id']),reverse=True)[:40]:
        item=ET.SubElement(channel,'item')
        ET.SubElement(item,'title').text=d['provider']+' · '+d['value']
        ET.SubElement(item,'link').text=HOST+detail(d).replace('#','?utm_source=verified_rss#',1)
        ET.SubElement(item,'guid',isPermaLink='false').text='tokenmost:'+d['id']
        timestamp=datetime.fromisoformat(d['verified_at'].replace('Z','+00:00'))
        ET.SubElement(item,'pubDate').text=format_datetime(timestamp.replace(tzinfo=timestamp.tzinfo or timezone.utc))
        ET.SubElement(item,'description').text=esc(d.get('rule') or d['value'])+' · <a href="'+esc(d['url'])+'">官方入口</a>'
    (root/'verified.xml').write_bytes(ET.tostring(rss,encoding='utf-8',xml_declaration=True))
