const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const liveCatalogue=JSON.parse(fs.readFileSync(path.join(root,'deals.json')));
const liveDeal=liveCatalogue.find(d=>d.id==='zcode-weekend-5yi-1120');
// Historical time-travel cases use their verified snapshot state; current
// automation may already have expired the pack or marked a promotion stale.
const deal={...liveDeal,verify_status:'verified'};
const actualMath=require('../assets/token-math.js');
if(new Date(liveDeal.deadline).getTime()<=Date.now()){
 assert.equal(actualMath.quota(liveDeal,new Date()).total,0);
 assert.equal(actualMath.phase(liveDeal,new Date()),'expired');
}
assert.equal(deal.claim_status,'window_unconfirmed');
assert.equal(deal.api_via,'client_only');
assert.equal(deal.token_quota[0].model,'GLM-5.3-Flash');
assert.equal(deal.quota_conditional,true);
const scripts=['assets/token-math.js','assets/workbench.js'].map(p=>fs.readFileSync(path.join(root,p),'utf8')).join('\n');
for(const lang of ['zh-CN','en']){
 let clock='2026-11-23T08:59:00+08:00',rendered=0,newsRefreshes=0;
 const timers=[];
 const makeNode=()=>({dataset:{},style:{},classList:{contains:()=>false},querySelector(){return this;},querySelectorAll:()=>[],addEventListener(){},setAttribute(){},append(){},replaceChildren(){},contains:()=>false});
 const ticker=makeNode(),newsItems=makeNode();
 const DateAt=class extends Date {constructor(...args){super(...(args.length?args:[clock]));}static now(){return new Date(clock).getTime();}};
 const sandbox={module:{exports:{}},Date:DateAt,Intl,URL,console,DEALS:[deal],esc:x=>String(x),
  document:{documentElement:{lang},getElementById:id=>id==='newsTicker'?ticker:id==='ntkItems'?newsItems:null,querySelector:()=>null,addEventListener(){},createElement:makeNode,hidden:false,activeElement:null},
  window:{matchMedia:()=>({matches:true,addEventListener(){}}),render(){rendered++;},calcGlobalBanner(){},refreshWorkbenchNews(){newsRefreshes++;wb.refreshNews([deal],false);}},
  setInterval:(fn,ms)=>{timers.push({fn,ms});return timers.length;},clearTimeout(){},setTimeout:()=>0};
 vm.runInNewContext(scripts+'\nmodule.exports={math:TokenMath,workbench:Workbench};',sandbox);
 const {math,workbench:wb}=sandbox.module.exports;
 const historicFeaturedIds=new Set(['opendesign-reset-card-invite','opencode-go-deepseek','cline-pass-deepseek']);
 const catalogue=liveCatalogue.map(d=>{
  if(!historicFeaturedIds.has(d.id))return d;
  const historical=d.id==='opencode-go-deepseek'
    ? d.offer_history?.find(entry=>entry.previous?.featured_until==='2026-11-22')?.previous
    : undefined;
  return {...d,...historical,verify_status:'verified'};
 });
 const currentFeatured=wb.featuredDeals(liveCatalogue,new Date());
 assert.ok(currentFeatured.every(d=>d.verify_status==='verified'&&wb.isFeatured(d,new Date())),'Current recommendations never restore stale or expired data.');
 const later=clock;clock='2026-11-22T12:00:00+08:00';
 const featured=wb.featuredDeals(catalogue,new Date(clock));
 assert.deepEqual(Array.from(featured,d=>d.id),['opendesign-reset-card-invite','opencode-go-deepseek','cline-pass-deepseek']);
 const extra={...featured[0],id:'fourth-paid-plan',provider:'Fourth',group:'Fourth',featured_rank:4};
 const duplicate={...featured[0],id:'duplicate-plan',featured_rank:5};
 assert.deepEqual(Array.from(wb.featuredDeals([extra,duplicate,...catalogue],new Date(clock)),d=>d.id),Array.from(featured,d=>d.id),'Pin at most three distinct platforms, in editorial order.');
 assert.equal(wb.isFeatured({...featured[0],verify_status:'stale'},new Date(clock)),false);
 assert.equal(wb.isFeatured({...featured[0],quota_paid:false},new Date(clock)),false);
 assert.deepEqual(Array.from(wb.featuredDeals(catalogue,new Date('2026-11-23T00:00:00+08:00')),d=>d.id),['opendesign-reset-card-invite','cline-pass-deepseek'],'Expired boost leaves the recommendations.');
 assert.deepEqual(Array.from(wb.featuredDeals(catalogue,new Date('2026-11-30T00:00:00+08:00')),d=>d.id),['opendesign-reset-card-invite']);
 assert.equal(wb.featuredDeals(catalogue,new Date('2026-12-06T00:00:00+08:00')).length,0);
 const pinnedBefore=wb.pinnedInvites(liveCatalogue,new Date('2026-11-29T23:59:59+08:00'));
 const pinnedAfter=wb.pinnedInvites(liveCatalogue,new Date('2026-11-30T00:00:00+08:00'));
 assert.match(pinnedBefore,/QPBS8AX98ZQM/);
 assert.doesNotMatch(pinnedAfter,/QPBS8AX98ZQM/);
 assert.match(pinnedAfter,/s\.qiniu\.com\/EnYbIb/);
 assert.equal(math.catalogue(featured).total.typical,0,'Paid recommendations do not enter the free ledger.');
 assert.match(wb.subscriptionCell(featured[0]),lang==='en'?/\$8 first mo/:/\$8 首月/);
 assert.match(wb.subscriptionCell(featured[0]),/\$10/);
 assert.match(wb.subscriptionCell(featured[2]),/2–5/);
 assert.equal(featured[2].subscription_offer.monthly_usage_limit,undefined,'A multiplier is not an invented dollar cap.');
 assert.doesNotMatch(wb.timing(featured[0]),/2026-11-29/,'Editorial review date is not an offer expiry.');
 clock=later;
 assert.equal(math.quota(deal).total,50000);
 assert.match(math.cell(deal),lang==='en'?/Claimed pack total/:/已领礼包总量/);
 const grouped=math.cell(deal,{...math.quota(deal),total:999999});
 assert.match(grouped,lang==='en'?/Claimed pack total/:/已领礼包总量/);
 assert.match(grouped,lang==='en'?/500.00M/:/5.00 亿/,'The group header shows the tested pack, not mixed trial/card capacity.');
 assert.doesNotMatch(grouped,/999999/);
 assert.equal(wb.claimLabel(deal),lang==='en'?'View entry':'查看入口');
 assert.match(wb.claimNotice(deal),lang==='en'?/New claims unconfirmed/:/新领取待核/);
 assert.match(wb.freshness(deal),lang==='en'?/Claim tested/:/已领实测/);
 assert.equal(math.free(deal),false);
 assert.equal(math.catalogue([deal]).total.typical,0,'A single claimed account does not add guaranteed free grants.');
 assert.equal(math.allowance([deal],{provider:deal.provider,model:'GLM-5.3-Flash'}).tokens,0,'Client pack is not API credit.');
 const phaseTimer=timers.find(t=>t.ms===1000);assert.ok(phaseTimer);phaseTimer.fn();
 clock='2026-11-23T09:00:00+08:00';phaseTimer.fn();
 assert.equal(math.quota(deal).total,0);assert.equal(math.phase(deal),'expired');
 assert.equal(wb.claimLabel(deal),lang==='en'?'View history':'查看历史');
 assert.equal(wb.claimNotice(deal),'');assert.match(wb.freshness(deal),lang==='en'?/Expired/:/已失效/);
 assert.equal(rendered,1,'Deadline transition refreshes existing open pages.');
 assert.equal(newsRefreshes,1);assert.equal(newsItems.textContent,lang==='en'?'No updates yet':'暂无更新','Expired pack leaves fallback news.');
}
console.log('Claim-window and featured checks passed: scope labels, paid isolation, capped ordering, expiry and both languages.');
