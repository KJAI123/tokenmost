const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {spawnSync} = require('node:child_process');
const root = path.resolve(__dirname, '..');
const math = require('../assets/token-math.js');
const deals = JSON.parse(fs.readFileSync(path.join(root,'deals.json')));
// Formula examples are evaluated as of the snapshot below. Automated expiry or
// archival must not break publishing; the parity pass uses the actual live states.
const byId = Object.fromEntries(deals.map(d=>[d.id,{...d,verify_status:'verified',published:true}]));
const now = new Date('2026-11-18T03:00:00Z');
const near = (a,b) => assert.ok(Math.abs(a-b)<1e-6, `${a} != ${b}`);
const quota = rows => ({token_quota:rows});

near(math.quota(byId['kimi-voucher'],now).total,15/1.75*100);
near(math.quota(byId['vercel-ai-gateway-free-credits'],now).monthly,5/.2625*100);
near(math.quota(byId['vercel-ai-gateway-free-credits'],now).daily,0);
near(math.quota(byId['edgeone-makers-50w'],now).monthly,50);
near(math.quota(byId['edgeone-makers-50w'],now).once,0);
near(math.quota(byId['deep-zhipu-trialplan-r7'],now).total,(300*13/1.75+500*1.3/1.75)*5);
near(math.quota(byId['autoclaw-m11w3-login'],now).total,10000);
near(math.rawTokens(math.entries(byId['deep-zhipu-trial-card'])[0]),2000*10000/11.175);
near(math.quota(byId['llm7-free-token'],now).total,300);
near(math.quota(byId['qiniu-conatus-1e8'],now).total,10000*13);
near(math.quota(byId['fiimeopc-token'],now).once,10000); // not 16亿 plus another month's tasks
near(math.quota(byId['aliyun-yungongkaiwu-student'],now).total,300/1.75*100); // cloud coupon not counted again
near(math.quota(quota([{amount:100,unit:'USD',period:'once'}]),now).total,100/.2625*100);
near(math.quota({tokens_wan:300,eq_wan:999999,token_quota:[]},now).total,0); // explicit empty wins
near(math.quota({daily_wan:5,deadline:'2026-11-17'},now).total,0);
for(const id of ['ace-music-daily-20','groq-free','modelscope-amd-gpu-100h','openrouter-free','sensenova-lite']) near(math.quota(byId[id],now).total,0);
for(const id of ['openai-pro-api-credits','opendesign-reset-card-invite','fiimeopc-token','deep-zhipu-trial-card']) assert.equal(math.free(byId[id]),false);
assert.match(math.cell(byId['ant-bailing-monthly-10']),/¥10/);
assert.match(math.explain(byId['kimi-voucher']),/1.75/);
assert.equal(math.allowance([byId['kimi-voucher']],{provider:'Kimi 开放平台',model:'kimi-k3'},now).cny,0);
near(math.allowance([byId['xiaomi-mimo-free5']],{provider:'小米 MiMo',model:'mimo-intl'},now).cny,5);
assert.equal(math.allowance([byId['autoclaw-m11w3-login']],{provider:'智谱 BigModel',model:'GLM-5.3'},now).tokens,0);
const expired={...byId['xiaomi-mimo-free5'],verify_status:'expired'};
assert.equal(math.allowance([expired],{provider:'小米 MiMo',model:'mimo-intl'},now).cny,0);
const q=math.sum([byId['kimi-voucher'],byId['ant-bailing-monthly-10']],now);
near(q.total,25/1.75*100); // amount and equivalent are counted once
// Daily scenarios never mutate official quotas or become model-billing allowances.
const requests=math.estimate(byId['openrouter-free'],now);
near(requests.daily.low,5);
near(requests.daily.typical,20);
near(requests.daily.high,40);
near(requests.month.typical,600);
near(math.estimate(byId['modelscope-free-infer'],now).daily.typical,800);
near(math.estimate(byId['deep-qoder-daily-credits'],now).daily.typical,100*(20/2000)/.2625*100);
near(math.estimate(byId['workbuddy-intl-free'],now).daily.typical,30*.01/.2625*100);
near(math.estimate(byId['cloudflare-workers-ai-free'],now).daily.typical,10000/(13778*.75+26128*.25)*100);
near(math.estimate(byId['tencent-ima-daily'],now).daily.typical,5);
near(math.estimate(byId['wps-lingxi-daily'],now).month.typical,540);
near(math.estimate(byId['wps-lingxi-daily'],now).daily.high,40);
near(math.estimate(byId['modelscope-free-infer'],now,{requestTokens:8000,pointTokens:1000}).daily.typical,1600);
near(math.estimate(byId['tencent-ima-daily'],now,{requestTokens:4000,pointTokens:2000}).daily.typical,10);
assert.equal(math.quota(byId['openrouter-free'],now).total,0);
assert.equal(math.estimate(byId['ace-music-daily-20'],now),null); // music isn't language tokens
assert.equal(math.estimate({...byId['tencent-ima-daily'],deadline:'2026-11-17'},now),null);
assert.equal(math.estimateMany([byId['openrouter-free'],byId['ernie-5.5-flash-free']],now).count,1);
near(math.estimateMany([byId['openrouter-free'],byId['ernie-5.5-flash-free']],now).daily.typical,20);
near(math.estimateMany([byId['modelscope-free-infer'],byId['modelscope-gpu-free']],now).daily.typical,800);
const capped={...byId['openrouter-free'],daily_estimate:{...byId['openrouter-free'].daily_estimate,token_cap_daily:100000}};
near(math.estimate(capped,now).daily.high,10);
assert.match(math.estimateExplain(byId['tencent-ima-daily']),/非官方/);
const eq=JSON.parse(fs.readFileSync(path.join(root,'tools/eq.json')));
near(math.rates.CNY,eq.base_cn.weighted_cny_per_m);
near(math.rates.USD,eq.base_global.weighted_usd_per_m);
const plans=JSON.parse(fs.readFileSync(path.join(root,'plans.json')));
near(plans.find(p=>p.provider==='小米 MiMo').tokens_wan,4.1e9/125/10000);
near(plans.find(p=>p.provider==='国家超算互联网 SCNet').tokens_wan,60000/(.75*60000/7200000+.25*60000/1700000)/10000);
for(const p of plans.filter(p=>p.provider==='智谱 BigModel')) {
 const weekly={'GLM Coding Lite':10000,'GLM Coding Pro':60000,'GLM Coding Max':140000}[p.plan];
 assert.ok(Math.abs(p.tokens_wan-weekly/11.175*30/7)<.0001);
}
const staticRun=spawnSync('python3',['-c',
  "import sys,json,datetime;sys.path.insert(0,'tools');from token_math import quota,free,estimate;print(json.dumps({d['id']:{**quota(d,datetime.date(2026,11,18)),'free':free(d),'estimated':estimate(d,datetime.date(2026,11,18))} for d in json.load(open('deals.json'))}))"
],{cwd:root,encoding:'utf8'});
assert.equal(staticRun.status,0,staticRun.stderr);
const staticQuotas=JSON.parse(staticRun.stdout);
for(const d of deals) {
 const dynamic=math.quota(d,now),rendered=staticQuotas[d.id];
 for(const key of ['once','daily','monthly','dailyMonth','total']) near(dynamic[key],rendered[key]);
 assert.equal(math.free(d),rendered.free,d.id);
 const estimated=math.estimate(d,now),staticEstimate=rendered.estimated;
 assert.equal(Boolean(estimated),Boolean(staticEstimate),d.id);
 if(estimated) for(const period of ['daily','month']) for(const key of ['low','typical','high']) near(estimated[period][key],staticEstimate[period][key]);
}
console.log('Token conversion and daily-estimate checks passed: formulas, scenarios, settings, pool deduplication, billing separation and JS/Python parity.');
