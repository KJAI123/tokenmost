const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const deal=JSON.parse(fs.readFileSync(path.join(root,'deals.json'))).find(d=>d.id==='zcode-weekend-5yi-1120');
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
console.log('Claim-window checks passed: scope labels, totals/API separation, exact cutoff and open-page/news refresh in both languages.');
