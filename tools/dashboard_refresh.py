# -*- coding: utf-8 -*-
"""dashboard_refresh.py — 运营中台看板刷新入口
用法:
  python3 tools/dashboard_refresh.py                    # 用 dashboard-data.json 刷新 dashboard.html
  python3 tools/dashboard_refresh.py <data.json> <out>  # 指定数据与输出（隔离测试用）
依赖: 仅标准库。数据与渲染分离——日常只改 dashboard-data.json 后运行本脚本。
"""
import json, sys, os
from datetime import datetime
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
data_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "dashboard-data.json")
out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "dashboard.html")

data = json.load(open(data_path, encoding="utf-8"))
D = json.dumps(data, ensure_ascii=False)

html = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>TokenMost 运营中台</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#0a0e1a; color:#e0e6f0; font-family:-apple-system,'PingFang SC',sans-serif; padding:24px; }
h1 { font-size:22px; margin-bottom:4px; }
.sub { color:#7a8699; font-size:12px; margin-bottom:20px; }
.grid { display:grid; grid-template-columns:repeat(6,1fr); gap:12px; margin-bottom:20px; }
.kpi { background:#121826; border:1px solid #1e2a42; border-radius:10px; padding:14px; }
.kpi .v { font-size:26px; font-weight:700; color:#4ade80; }
.kpi .l { font-size:11px; color:#7a8699; margin-top:2px; }
h2 { font-size:15px; margin:20px 0 10px; color:#9db4d0; border-left:3px solid #3b82f6; padding-left:8px; }
.two { display:grid; grid-template-columns:1fr 1fr; gap:14px; }
.card { background:#121826; border:1px solid #1e2a42; border-radius:10px; padding:14px; }
table { width:100%; border-collapse:collapse; font-size:12.5px; }
td, th { padding:6px 8px; border-bottom:1px solid #1a2338; text-align:left; }
th { color:#7a8699; font-weight:500; }
.st-ok { color:#4ade80; } .st-warn { color:#fbbf24; } .st-banned { color:#f87171; } .st-todo { color:#7a8699; }
.delta-up { color:#4ade80; } .delta-rej { color:#f87171; }
.timeline li { list-style:none; padding:4px 0; font-size:12.5px; color:#b8c4d8; border-left:2px solid #3b82f6; padding-left:10px; margin-left:4px; }
.pill { display:inline-block; padding:2px 8px; border-radius:10px; font-size:11px; margin:2px; }
.pill.b { background:#1e3a5f; color:#7cc4ff; } .pill.g { background:#14532d; color:#4ade80; } .pill.y { background:#713f12; color:#fbbf24; }
.note { font-size:11.5px; color:#7a8699; margin-top:8px; line-height:1.5; }
</style>
</head>
<body>
<h1>🚀 TokenMost 运营中台</h1>
<div class="sub"></div>
<div class="grid">
  <div class="kpi"><div class="v" id="k-pub"></div><div class="l">累计发布(4天)</div></div>
  <div class="kpi"><div class="v" id="k-reads"></div><div class="l">CSDN 总阅读</div></div>
  <div class="kpi"><div class="v" id="k-ammo"></div><div class="l">弹药库(人味化)</div></div>
  <div class="kpi"><div class="v" id="k-bl"></div><div class="l">外链管道</div></div>
  <div class="kpi"><div class="v" id="k-ore"></div><div class="l">掘金矿石</div></div>
  <div class="kpi"><div class="v" id="k-geo"></div><div class="l">GEO 矩阵有号</div></div>
</div>
<h2>平台矩阵状态</h2>
<div class="card"><table id="acc"></table>
<div class="note">状态: <span class="st-ok">■</span> 正常运转 · <span class="st-warn">■</span> 待动作(扫码/迁移/审核) · <span class="st-banned">■</span> 禁言/受限 · <span class="st-todo">■</span> 待注册</div></div>
<div class="two">
<div>
<h2>CSDN · AI 案例分享系列</h2>
<div class="card"><table id="art"></table>
<div class="note" id="coupon-note"></div></div>
<h2>知乎事件线</h2>
<div class="card"><ul class="timeline" id="tl"></ul></div>
</div>
<div>
<h2>外链管道 (GitHub)</h2>
<div class="card">
<span class="pill g" id="bl-merged"></span><span class="pill b" id="bl-open"></span>
<div class="note" id="bl-note" style="margin-top:8px;white-space:pre-line"></div></div>
<h2>弹药库</h2>
<div class="card"><div class="note" id="ammo-note" style="white-space:pre-line"></div></div>
<h2>⏳ 待老板配合</h2>
<div class="card"><div class="note" id="boss"></div></div>
</div>
</div>
<script>
const D = __DATA__;
document.querySelector('.sub').textContent = '数据快照: ' + D.updated + ' · 刷新: python3 tools/dashboard_refresh.py';
document.getElementById('k-pub').textContent = D.kpis.total_published;
document.getElementById('k-reads').textContent = D.kpis.reads_total.toLocaleString();
document.getElementById('k-ammo').textContent = D.ammo.total;
document.getElementById('k-bl').textContent = D.backlinks.total;
document.getElementById('k-ore').textContent = D.kpis.ore.toLocaleString();
document.getElementById('k-geo').textContent = D.kpis.geo_accounts;
document.getElementById('coupon-note').textContent = D.coupons.total + ' coupons, ' + D.coupons.active + ' active; ' + D.coupons.faceValue + '; ' + D.coupons.note + '; ' + D.coupons.policyNote;
document.getElementById('bl-merged').textContent = D.backlinks.merged + ' merged';
document.getElementById('bl-open').textContent = D.backlinks.open + ' open';
document.getElementById('bl-note').textContent = 'Merged: ' + D.backlinks.mergedName + '\\nPending: ' + D.backlinks.top.join(' · ') + '\\n' + D.backlinks.pendingNote;
document.getElementById('ammo-note').textContent = D.ammo.total + ' articles, ' + D.ammo.humanized + ' humanized. ' + D.ammo.note + '\\n' + D.ammo.breakdown + '\\n' + D.ammo.schedule;

const cls = {ok:'st-ok', warn:'st-warn', banned:'st-banned', todo:'st-todo'};
document.getElementById('acc').innerHTML = '<tr><th>平台</th><th>状态</th><th>备注</th></tr>' +
  D.accounts.map(a => `<tr><td>${a.platform}</td><td class="${cls[a.status]||''}">${a.statusText}</td><td style="color:#7a8699">${a.note}</td></tr>`).join('');
document.getElementById('art').innerHTML = '<tr><th>文章</th><th>阅读</th><th>赞/收</th><th>趋势</th></tr>' +
  D.csdn_articles.map(a => `<tr><td>${a.title}</td><td>${a.reads}</td><td>${a.likes}/${a.collects}</td><td class="${a.delta.includes('❌')?'delta-rej':'delta-up'}">${a.delta}</td></tr>`).join('');
document.getElementById('tl').innerHTML = D.zhihu_timeline.map(x => `<li><b>${x.date}</b> — ${x.event}</li>`).join('');
document.getElementById('boss').innerHTML = D.pending_boss.map(x => '• ' + x).join('<br>');
</script>
</body>
</html>"""

html = html.replace("__DATA__", D)
open(out_path, "w", encoding="utf-8").write(html)
print(f"refreshed: {out_path} ({os.path.getsize(out_path)} bytes) from {data_path} (updated={data.get('updated')})")
