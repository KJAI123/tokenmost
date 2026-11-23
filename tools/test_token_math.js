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
near(math.quota(byId['deep-zhipu-trialplan-r7'],now).total,0); // Official trial pages conflict; no fixed amount selected.
near(math.quota(byId['autoclaw-m11w3-login'],now).total,10000);
near(math.rawTokens(math.entries(byId['deep-zhipu-trial-card'])[0]),2000*10000/11.175);
near(math.quota(byId['llm7-free-token'],now).total,0); // Legacy quota has no current policy evidence.
near(math.quota(quota([{amount:100000,unit:'tokens',period:'daily'}]),now).total,300);
near(math.quota(byId['electronhub-free-weekly'],now).monthly,.25/.2625*100*30/7);
assert.equal(math.free(byId['deep-qoder-daily-credits']),false); // Pro trial or paid-plan eligibility is required.
assert.equal(math.estimateMany([byId['deep-qoder-daily-credits']],now).count,0);
near(math.quota(byId['qiniu-conatus-1e8'],now).total,10000*13);
near(math.quota(byId['fiimeopc-token'],now).once,10000); // not 16亿 plus another month's tasks
near(math.quota(byId['aliyun-yungongkaiwu-student'],now).total,300/1.75*100); // cloud coupon not counted again
near(math.quota(quota([{amount:100,unit:'USD',period:'once'}]),now).total,100/.2625*100);
near(math.quota({tokens_wan:300,eq_wan:999999,token_quota:[]},now).total,0); // explicit empty wins
near(math.quota({daily_wan:5,deadline:'2026-11-17'},now).total,0);
for(const id of ['ace-music-daily-20','modelscope-amd-gpu-100h','openrouter-free','sensenova-lite']) near(math.quota(byId[id],now).total,0);
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
// Different refresh periods must not all become daily grants.
const mixedFixture={id:'mixed-periods',deadline:'2026-11-20',token_quota:[
 {amount:100,unit:'credits',period:'once'}, {amount:10,unit:'credits',period:'daily'},
 {amount:50,unit:'credits',period:'monthly'}, {amount:20,unit:'credits',period:'weekly'}
],quota_estimates:[0,1,2,3].map(quota_index=>({quota_index,method:'scenario'}))};
const mixed=math.estimate(mixedFixture,now,{requestTokens:4000,pointTokens:1000});
near(mixed.daily.typical,1);
near(mixed.month.typical,10+3+5+2*3/7);
assert.equal(math.estimateMany([mixedFixture],now).count,4);
assert.match(math.cell(byId['openrouter-free'],math.sum([byId['openrouter-free']],now)),/50/); // A single-estimate provider group still carries its native quota.
assert.match(math.cell(byId['trae-free-tier'],math.sum([byId['trae-free-tier']],now)),/3 项独立额度/);
near(math.quota({deadline:'2026-11-20',token_quota:[{amount:7,unit:'USD',period:'weekly'}]},now).total,3/.2625*100);
near(math.estimate(byId['trae-free-tier'],now).month.typical,(500+1500+100*30)*(49/2000)/1.75*100);
near(math.estimate(byId['clixad-free'],now).daily.typical,60000*21500/585/10000);
near(math.estimate(byId['cohere-trial'],now).month.typical,400);
near(math.estimate(byId['cohere-trial'],now).daily.typical,0);
near(math.estimate(byId['github-copilot-free'],now).month.typical,40); // 2K short completions, not 2K full chat requests.
near(math.estimate(byId['deep-qoder-cn-free'],now).month.typical,300*(169/6000)/1.75*100);
assert.equal(math.estimate(byId['clixad-free'],now).method,'model_examples');
// Model tables produce alternate scenarios for a single pool, never three grants.
const meoo=math.estimate(byId['miao-wu-daily-2000'],now);
near(meoo.daily.typical,2000*1000/(2*.75+8*.25)/10000);
near(meoo.month.typical,(5000+2000*30)*1000/3.5/10000);
near(meoo.month.low,65000*1000/40/10000);
near(meoo.month.high,65000*1000/.65/10000);
assert.equal(math.estimateMany([byId['miao-wu-daily-2000']],now).count,2);
near(math.quota(byId['miao-wu-daily-2000'],now).total,0);
const drex=byId['drex-monthly-5usd'];
near(math.estimate(drex,now).month.typical,5/.03*100);
near(math.quota(drex,now).total,0); // Same $5 is not also a DS buying-power reference.
assert.equal(math.estimateMany([drex],now).count,1);
assert.match(math.cell(drex),/输入预算/);
const drexStaticPage=fs.readFileSync(path.join(root,'platform/drex.html'),'utf8');
assert.match(drexStaticPage,/首月仅输入预算/);
assert.match(drexStaticPage,/延后发放，首月按规则排除/);
assert.doesNotMatch(drexStaticPage,/金额只作 DS Flash 购买力参考/);
assert.equal(math.estimate({...drex,quota_estimates:[{...drex.quota_estimates[0],quota_index:1}]},now),null);
const delayedFixture={id:'delayed',token_quota:[{amount:5,unit:'USD',period:'once'},{amount:5,unit:'USD',period:'monthly',starts_after_days:30},{amount:1,unit:'USD',period:'daily',starts_after_days:20}]};
near(math.quota(delayedFixture,now).monthly,0);
near(math.quota(delayedFixture,now).dailyMonth,10/.2625*100);
near(math.quota(delayedFixture,now).total,15/.2625*100);
near(math.estimate(byId['fastgpt-free'],now).month.typical,100*(99/4000)/1.75*100);
near(math.estimate(byId['tencent-adp-15k'],now).month.typical,15/1.75*100);
near(math.quota(byId['tencent-adp-15k'],now).total,0); // PU value is a separate scenario, never a native token grant.
assert.match(math.cell(byId['tencent-adp-15k']),/购买力估计/);
assert.equal(math.estimate(byId['fastgpt-free'],now).daily.typical,0);
assert.equal(math.entries(byId['deep-windsurf-devin']).length,0);
const sharedBuddy=math.estimateMany([byId['workbuddy-free'],byId['deep-codebuddy-free-kimi']],now);
assert.equal(sharedBuddy.rows.filter(e=>e.pool==='buddy-cn-monthly').length,1);
assert.equal(sharedBuddy.rows.find(e=>e.pool==='buddy-cn-monthly').deal.id,'deep-codebuddy-free-kimi');
for(const id of ['workbuddy-intl-pro','atlassian-rovo-dev-free','trae-code-fission','freepi-terminal-free']) {
 assert.ok(math.estimate(byId[id],now),id+' has a displayable scenario');
 assert.equal(math.estimateMany([byId[id]],now).count,0,id+' excluded from standard free totals');
}
for(const id of ['rime-monthly-50usd','elevenlabs-free-10k','agentscope-qwenpaw-free','replit-free-mode','azure-free-trial','vultr-trial-250']) {
 near(math.quota(byId[id],now).total,0);
 assert.equal(math.estimate(byId[id],now),null,id+' is not a text-token allowance');
}
// The broader catalogue must expose its verified, pending and scenario parts.
// Student/paid/conditional offers stay outside it and unknown quotas aren't zero-value grants.
const verifiedFixture={id:'verified',verify_status:'verified',token_quota:[{amount:1000000,unit:'tokens',period:'once'}]};
const pendingFixture={id:'pending',verify_status:'stale',token_quota:[{amount:2000000,unit:'tokens',period:'once'}]};
const unknownFixture={id:'unlimited',verify_status:'verified',token_quota:[]};
const catalogue=math.catalogue([verifiedFixture,pendingFixture,unknownFixture,byId['openrouter-free'],
  {...verifiedFixture,id:'student',gate:'student'}, {...verifiedFixture,id:'paid',quota_paid:true},
  {...verifiedFixture,id:'conditional',quota_conditional:true}],now);
near(catalogue.verified.total,100);
near(catalogue.pending.total,200);
near(catalogue.total.low,450); // 1M + 2M + 50/day × 1K/request × 30 days
near(catalogue.total.typical,900);
near(catalogue.total.high,1500);
assert.deepEqual(catalogue.unquantified.map(d=>d.id),['unlimited']);
near(math.catalogue([verifiedFixture,pendingFixture,byId['openrouter-free']],now,{requestTokens:8000,pointTokens:1000}).total.typical,1500);
assert.equal(math.catalogue([{...pendingFixture,verify_status:'expired'},{...verifiedFixture,published:false}],now).total.typical,0);
// Rolling native caps and separate usage scenarios. One-time, gated and shared grants cannot inflate either sum.
const current = new Date('2026-11-23T08:00:00Z');
const dailyDeal = {...verifiedFixture,token_quota:[{amount:200000,unit:'tokens',period:'daily',pool:'shared-models'}]};
const scenario = {...mixedFixture,deadline:undefined,verify_status:'verified'};
const month = math.monthlyLedger([dailyDeal,{...dailyDeal,id:'other-model'},verifiedFixture,pendingFixture,
  {...dailyDeal,id:'conditional',quota_conditional:true}, {...dailyDeal,id:'paid',quota_paid:true},
  {...dailyDeal,id:'student',gate:'student'},byId['qiniu-conatus-1e8'],scenario],current);
near(month.standing,600); near(month.limited,80000); near(month.total,80600);
assert.equal(month.rows.length,2);
assert.equal(month.usage.count,3); // daily, weekly, monthly, no signup grant
near(math.monthlyLedger([byId['qiniu-conatus-1e8']],new Date('2026-11-30T15:59:00Z')).total,0);
near(math.monthlyLedger([byId['groq-free'],byId['sambanova-free'],byId['vikasit-nova-free'],byId['edgeone-makers-50w']],current).standing,7250);
// First-use grants join the first-month view only. Conflicting versions of one pool count once.
const trialFixture = {...dailyDeal,id:'trial',quota_introductory:true,quota_days:30,
  token_quota:[{amount:1000000,unit:'tokens',period:'daily',pool:'trial-core'}]};
const fixedCredit = {...verifiedFixture,id:'official-ratio',token_quota:[{amount:5000,unit:'credits',period:'once',tokens_per_unit:10000}]};
const sharedFirst = {...verifiedFixture,id:'same-pool',token_quota:[{amount:30000000,unit:'tokens',period:'once',pool:'shared-models'}]};
for (const candidates of [[dailyDeal,sharedFirst],[sharedFirst,dailyDeal]]) {
  const ledger = math.monthlyLedger([...candidates,trialFixture,verifiedFixture,fixedCredit,pendingFixture,
    {...verifiedFixture,id:'gated',quota_conditional:true},{...fixedCredit,id:'old',deadline:'2026-11-22'}],current);
  near(ledger.total,600);
  near(ledger.firstClaim,8100);
  near(ledger.firstMonth,8700);
}
const regolo = byId['regolo-core-trial'];
near(math.monthlyLedger([regolo],current).standing,0);
near(math.monthlyLedger([regolo],current).firstClaim,3000);
const bailian = byId['deep-bailian-newuser-quota'];
assert.equal(new Set(bailian.token_quota.map(q=>q.pool)).size,bailian.token_quota.length);
assert.ok(bailian.token_quota.every(q=>q.model && q.period==='once'));
for (const id of ['wx-miniprogram-growth-1b','agentrouter-signup','aimlapi-startup-10m','siliconflow-referral']) assert.equal(math.free(byId[id]),false,id);
const actualCatalogue=math.catalogue(deals,now);
for (const d of deals) assert.equal(typeof math.cell(d),'string',d.id);
const providerGroups=new Map();
for (const d of deals) {const key=d.group||d.provider;if(!providerGroups.has(key))providerGroups.set(key,[]);providerGroups.get(key).push(d);}
for (const rows of providerGroups.values()) assert.equal(typeof math.cell(rows[0],math.sum(rows,now)),'string',rows[0].provider+' group rendering');
near(actualCatalogue.verified.total,math.sum(deals.filter(d=>math.free(d)&&d.verify_status==='verified'&&d.gate!=='student'&&d.type!=='student'),now).total);
near(actualCatalogue.total.typical,actualCatalogue.verified.total+actualCatalogue.pending.total+actualCatalogue.estimates.month.typical);
assert.ok(actualCatalogue.total.low<=actualCatalogue.total.typical&&actualCatalogue.total.typical<=actualCatalogue.total.high);
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
const delayedStatic=spawnSync('python3',['-c',"import sys,json,datetime;sys.path.insert(0,'tools');from token_math import quota;print(json.dumps(quota(json.loads(sys.argv[1]),datetime.date(2026,11,18))))",JSON.stringify(delayedFixture)],{cwd:root,encoding:'utf8'});
assert.equal(delayedStatic.status,0,delayedStatic.stderr);
const delayedRendered=JSON.parse(delayedStatic.stdout);
for(const key of ['once','daily','monthly','dailyMonth','total']) near(math.quota(delayedFixture,now)[key],delayedRendered[key]);
const staticQuotas=JSON.parse(staticRun.stdout);
// Timezone-aware deadlines expire at the exact instant (Nov 23, 09:00 GMT+8).
const tzDeal={id:'tz-boundary',verify_status:'verified',published:true,deadline:'2026-11-23T09:00:00+08:00',token_quota:[{amount:100,unit:'tokens',period:'daily'}]};
const stillClaimable=new Date('2026-11-22T23:30:00Z'); // 07:30 GMT+8 on Nov 23
const justExpired=new Date('2026-11-23T01:30:00Z');    // 09:30 GMT+8 on Nov 23
assert.ok(math.quota(tzDeal,stillClaimable).total>0,'08:59 GMT+8 must still be claimable');
assert.equal(math.quota(tzDeal,justExpired).total,0,'09:00 GMT+8 must be expired');
// Pure dates keep the end-of-day semantics on both sides of the same instants.
assert.ok(math.quota({...tzDeal,deadline:'2026-11-23'},stillClaimable).total>0);
assert.ok(math.quota({...tzDeal,deadline:'2026-11-23'},justExpired).total>0);
// JS/Python parity at the exact boundary.
const tzPy=spawnSync('python3',['-c',"import sys,datetime;sys.path.insert(0,'tools');from token_math import _deadline_days;print(_deadline_days({'deadline':'2026-11-23T09:00:00+08:00'},datetime.date(2026,11,23),datetime.datetime.fromisoformat('2026-11-23T08:59:00+08:00')))"],{cwd:root,encoding:'utf8'});
assert.equal(tzPy.status,0,tzPy.stderr);
assert.equal(parseInt(tzPy.stdout.trim(),10),1,'Python must also keep Nov 23 claimable until 09:00 GMT+8');
const tzPyAfter=spawnSync('python3',['-c',"import sys,datetime;sys.path.insert(0,'tools');from token_math import _deadline_days;print(_deadline_days({'deadline':'2026-11-23T09:00:00+08:00'},datetime.date(2026,11,24)))"],{cwd:root,encoding:'utf8'});
assert.equal(parseInt(tzPyAfter.stdout.trim(),10),0,'Python must treat 09:00 GMT+8 Nov 23 as expired on Nov 24');
const tzPyBoundary=spawnSync('python3',['-c',"import sys,datetime;sys.path.insert(0,'tools');from token_math import _deadline_days;print(_deadline_days({'deadline':'2026-11-23T09:00:00+08:00'},datetime.date(2026,11,23),datetime.datetime.fromisoformat('2026-11-23T08:59:00+08:00')));print(_deadline_days({'deadline':'2026-11-23T09:00:00+08:00'},datetime.date(2026,11,23),datetime.datetime.fromisoformat('2026-11-23T09:30:00+08:00')))"],{cwd:root,encoding:'utf8'});
assert.equal(tzPyBoundary.status,0,tzPyBoundary.stderr);
const tzPyRows=tzPyBoundary.stdout.trim().split('\n').map(Number);
assert.deepEqual(tzPyRows,[1,0],'Python 08:59 claimable / 09:30 expired');
// Exact 09:00 GMT+8 boundary on both ends.
assert.equal(math.quota(tzDeal,new Date('2026-11-23T01:00:00Z')).total,0,'JS 09:00 GMT+8 exact boundary expired');
const tzPyExact=spawnSync('python3',['-c',"import sys,datetime;sys.path.insert(0,'tools');from token_math import _deadline_days;print(_deadline_days({'deadline':'2026-11-23T09:00:00+08:00'},datetime.date(2026,11,23),datetime.datetime.fromisoformat('2026-11-23T09:00:00+08:00')))"],{cwd:root,encoding:'utf8'});
assert.equal(parseInt(tzPyExact.stdout.trim(),10),0,'Python 09:00 GMT+8 exact boundary expired');
// Real hourly instants (not just date-level): 08:59 claimable, 09:00 and 09:01 expired.
const hourDeal={id:'tz-hour',verify_status:'verified',published:true,deadline:'2026-11-23T09:00:00+08:00',token_quota:[{amount:1000000,unit:'tokens',period:'once'}]};
for(const [t,expect] of [['2026-11-22T20:00:00+08:00',1000000/10000],['2026-11-23T00:59:00+08:00',1000000/10000],['2026-11-23T08:59:00+08:00',1000000/10000],['2026-11-23T09:00:00+08:00',0],['2026-11-23T09:01:00+08:00',0]]){
  near(math.quota(hourDeal,new Date(t)).total,expect,'hour '+t);
}
for(const d of deals) {
 const dynamic=math.quota(d,now),rendered=staticQuotas[d.id];
 for(const key of ['once','daily','monthly','dailyMonth','total']) near(dynamic[key],rendered[key]);
 assert.equal(math.free(d),rendered.free,d.id);
 const estimated=math.estimate(d,now),staticEstimate=rendered.estimated;
 assert.equal(Boolean(estimated),Boolean(staticEstimate),d.id);
 if(estimated) for(const period of ['daily','month']) for(const key of ['low','typical','high']) near(estimated[period][key],staticEstimate[period][key]);
}
const clockRun=spawnSync('python3',['tools/test_quota_clock.py'],{cwd:root,encoding:'utf8'});
assert.equal(clockRun.status,0,clockRun.stderr||clockRun.stdout);
const claimRun=spawnSync(process.execPath,['tools/test_claim_window.js'],{cwd:root,encoding:'utf8'});
assert.equal(claimRun.status,0,claimRun.stderr||claimRun.stdout);
console.log('Token conversion and daily-estimate checks passed: formulas, scenarios, settings, pool deduplication, billing separation, JS/Python parity and timestamp boundaries.');

// Calendar records survive expiry, while the current-month remainder loses each elapsed day.
const iFlytek=byId['xfyun-spark-x26-nov17'];
// Replay the Nov 24 observation independently of later source reviews.
const datedGrant={...iFlytek,calendar_window:{...iFlytek.calendar_window,observed_through:'2026-11-24'}};
const novemberDeals=deals.map(d=>d.id===iFlytek.id?datedGrant:d);
const november = at => math.calendarLedger(novemberDeals,new Date('2026-11-'+at+'+08:00'));
for (const [time,remaining] of [['01T12:00:00',443000],['23T21:00:00',185000],['24T00:00:00',175000],['25T00:00:00',65000],['29T23:59:00',20000],['30T23:58:59',10000],['30T23:59:00',0]]) {
  const c=november(time);
  near(c.total,443000); near(c.remaining,remaining); near(c.carryIn,8000);
  assert.deepEqual(c.personal.map(r=>r.value),[50000]);
  assert(c.personal.every(r=>!r.remaining));
}
const december=new Date('2026-11-30T16:00:00Z');
near(math.calendarLedger(deals,december).total,0);
near(math.calendarLedger(deals,december,'2026-11').total,443000);
near(math.calendarLedger(deals,december,'2026-11').remaining,0);
near(math.monthlyLedger([datedGrant],new Date('2026-11-24T23:59:59+08:00')).firstClaim,100000);
near(math.monthlyLedger([datedGrant],new Date('2026-11-25T00:00:00+08:00')).firstClaim,0);
const duplicate={...iFlytek,id:'alternate-source'};
near(math.calendarLedger([iFlytek,duplicate],current).total,100000);
assert.equal(math.calendarLedger([byId['openai-api-data-sharing-tokens']],current).total,0);
assert.equal(bailian.token_quota.length,56);
