/* Quotas use native units. Money is a purchasing-power reference, never delivered tokens. */
const TokenMath = (() => {
  const rates = Object.freeze({CNY: 1.75, USD: .2625});
  const sources = Object.freeze({CNY: 'https://api-docs.deepseek.com/zh-cn/quick_start/pricing/', USD: 'https://api-docs.deepseek.com/quick_start/pricing/'});
  const zh = typeof document === 'undefined' || document.documentElement.lang.startsWith('zh');
  const msg = (cn, en) => zh ? cn : en;
  const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const positive = value => Number.isFinite(value) && value > 0 ? value : 0;
  const estimateDefaults = Object.freeze({requestTokens:4000,pointTokens:1000});
  let estimateSettings = {...estimateDefaults};
  try {
    const saved = JSON.parse(localStorage.getItem('tm_daily_estimates_v1') || 'null');
    if (saved) setEstimateSettings(saved, false);
  } catch (_) { /* The default scenario also works without local storage. */ }
  const format = wan => zh ? (wan >= 10000 ? (wan/10000).toFixed(2)+' 亿' : Number(wan.toFixed(1))+' 万')
    : wan >= 100000 ? (wan/100000).toFixed(2)+'B' : wan >= 100 ? (wan/100).toFixed(2)+'M' : Math.round(wan*10000).toLocaleString('en-US');
  function today(now = new Date()) {
    return new Intl.DateTimeFormat('en-CA', {timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit'}).format(now);
  }
  function phase(d, now = new Date()) {
    const at = now instanceof Date ? now : new Date(now);
    const end = /^\d{4}-\d{2}-\d{2}T/.test(d.deadline || '') ? Date.parse(d.deadline)
      : /^\d{4}-\d{2}-\d{2}$/.test(d.deadline || '') ? Date.parse(d.deadline+'T00:00:00+08:00')+864e5 : NaN;
    if (d.verify_status === 'expired' || Number.isFinite(end) && at.getTime() >= end) return 'expired';
    const start = Date.parse(d.starts_at);
    return Number.isFinite(start) && at.getTime() < start ? 'upcoming' : 'active';
  }
  function activeDays(d, now = new Date()) {
    if (phase(d,now) !== 'active') return 0;
    let days = Math.min(30, positive(d.quota_days) || 30);
    const endAt = Date.parse(d.deadline);
    const date = /^\d{4}-\d{2}-\d{2}T/.test(d.deadline || '') && Number.isFinite(endAt) ? today(new Date(endAt-1)) : d.deadline;
    if (/^\d{4}-\d{2}-\d{2}$/.test(date || '')) {
      days = Math.min(days, Math.max(0, Math.round((Date.parse(date+'T00:00:00Z')-Date.parse(today(now)+'T00:00:00Z'))/864e5)+1));
    }
    return days;
  }
  const rowDays = (d,q,now) => Math.max(0,activeDays(d,now)-(positive(q.starts_after_days)||0));
  function entries(d) {
    if (Array.isArray(d.token_quota)) return d.token_quota;
    // Legacy numeric token fields only. Currency and subscription prices need explicit quota records.
    const rows = [];
    if (d.tokens_wan) rows.push({amount:d.tokens_wan*10000,unit:'tokens',period:d.cadence === 'monthly' ? 'monthly' : 'once'});
    if (d.daily_wan) rows.push({amount:d.daily_wan*10000,unit:'tokens',period:'daily'});
    return rows;
  }
  function rawTokens(q) {
    return q.unit === 'tokens' ? positive(q.amount) : positive(q.amount)*positive(q.tokens_per_unit);
  }
  function equivalent(q) {
    if (q.convert === false) return 0;
    if (rates[q.unit]) return positive(q.amount)/rates[q.unit]*100;
    return rawTokens(q)/10000*(positive(q.equivalent_factor)||1);
  }
  function native(q) {
    const suffix = q.period === 'daily' ? msg('/天','/day') : q.period === 'monthly' ? msg('/月','/mo') : q.period === 'weekly' ? msg('/周','/week') : '';
    const amount = Number(q.amount.toFixed(2)).toLocaleString(zh?'zh-CN':'en-US');
    const units = {credits:msg(' 积分',' credits'),requests:msg(' 次',' requests'),hours:msg(' 小时',' hours'),points:msg(' 算力',' points')};
    return (q.unit === 'tokens' ? format(q.amount/10000)+' tokens' : q.unit === 'CNY' ? '¥'+amount : q.unit === 'USD' ? '$'+amount : amount+(units[q.unit]||' '+q.unit))+suffix+(q.starts_after_days ? msg('（延后发放）',' (deferred)') : '');
  }
  function quota(d, now) {
    const result = {once:0,daily:0,monthly:0,dailyMonth:0,total:0,converted:false,rows:entries(d),days:activeDays(d,now)};
    for (const q of result.rows) {
      const days = rowDays(d,q,now);
      if (!days) continue;
      const value = equivalent(q);
      const period = q.period || 'once';
      if (period === 'daily') {result.daily += value; result.dailyMonth += value*days;}
      else if (period === 'monthly') result.monthly += value;
      else if (period === 'weekly') result.monthly += value*days/7;
      else result.once += value;
      if (value && (q.unit !== 'tokens' || q.equivalent_factor)) result.converted = true;
    }
    result.total = result.once+result.dailyMonth+result.monthly;
    if (d.verify_status === 'expired' || result.days === 0) {
      for (const key of ['once','daily','monthly','dailyMonth','total']) result[key] = 0;
    }
    return result;
  }
  function sum(deals, now) {
    const result = deals.reduce((s,d) => {
      const q = quota(d,now);
      for (const key of ['once','daily','monthly','dailyMonth','total']) s[key] += q[key];
      s.converted ||= q.converted;
      return s;
    }, {once:0,daily:0,monthly:0,dailyMonth:0,total:0,converted:false});
    result.estimates = estimateMany(deals, now);
    return result;
  }
  function free(d) {
    return d.published !== false && d.verify_status !== 'expired' && !['freecloud','intel_source'].includes(d.category)
      && !['warning','price_low','pricing_plan','subscription_bonus','status'].includes(d.type)
      && !['subscribe','subscription'].includes(d.via) && !d.quota_paid && !d.quota_upper_bound && !d.quota_conditional
      && !['startup','audit','oss'].includes(d.gate);
  }
  function setEstimateSettings(settings, save = true) {
    for (const key of Object.keys(estimateDefaults)) {
      const value = Number(settings[key]);
      if (Number.isFinite(value) && value >= 1 && value <= 1000000) estimateSettings[key] = value;
    }
    if (save) try { localStorage.setItem('tm_daily_estimates_v1', JSON.stringify(estimateSettings)); } catch (_) {}
    return {...estimateSettings};
  }
  function estimateQuota(d, e, now, settings = estimateSettings) {
    const q = e && entries(d)[e.quota_index];
    if (!e || !q || !['once','daily','weekly','monthly'].includes(q.period) || equivalent(q) || d.verify_status === 'expired' || !rowDays(d,q,now)) return null;
    let factors;
    if (e.method === 'requests') {
      const perRequest = (positive(settings.requestTokens) || estimateDefaults.requestTokens)*(e.scale || 1);
      factors = {low:perRequest/4,typical:perRequest,high:perRequest*2};
    } else if (e.method === 'credit_value') {
      factors = Object.fromEntries(['low','typical','high'].map(key=>[key,e.unit_value[key]/rates[e.currency]*1e6]));
    } else if (e.method === 'neurons') {
      factors = Object.fromEntries(['low','typical','high'].map(key=>{
        const model = e.models[key];
        return [key,1e6/(model.input*.75+model.output*.25)];
      }));
    } else if (e.method === 'model_examples') {
      factors = Object.fromEntries(['low','typical','high'].map(key=>{
        const model = e.models[key];
        return [key,(model.input_tokens+model.output_tokens)/model.credits];
      }));
    } else if (e.method === 'model_rates') {
      factors = Object.fromEntries(['low','typical','high'].map(key=>{
        const model=e.models[key];
        return [key,1000/(model.input*.75+model.output*.25)];
      }));
    } else if (e.method === 'model_budget') {
      factors = Object.fromEntries(['low','typical','high'].map(key=>[key,1e6/e.models[key].price]));
    } else if (e.method === 'scenario') {
      const perPoint = positive(settings.pointTokens) || estimateDefaults.pointTokens;
      const scale = e.scale || 1;
      factors = {low:perPoint*.5*scale,typical:perPoint*scale,high:perPoint*2*scale};
    } else return null;
    const days = rowDays(d,q,now);
    const quantities = e.quantity_range || {low:q.amount,typical:q.amount,high:q.amount};
    const monthUnits = e.schedule
      ? e.schedule.reduce((s,step,index)=>{
          const before=e.schedule.slice(0,index).reduce((n,item)=>n+item.days,0);
          return s+Math.max(0,Math.min(step.days,days-before))*step.amount;
        },0)
      : null;
    const daily = {}, periodTokens = {}, month = {};
    const cycles = q.period === 'daily' ? days : q.period === 'weekly' ? days/7 : 1;
    for (const key of ['low','typical','high']) {
      const cap = positive(e.token_cap_daily) || Infinity;
      periodTokens[key] = Math.min(cap,quantities[key]*factors[key])/10000;
      daily[key] = q.period === 'daily' ? periodTokens[key] : 0;
      month[key] = monthUnits === null ? periodTokens[key]*cycles : Math.min(cap*days,monthUnits*factors[key])/10000;
    }
    return {daily,month,periodTokens,period:q.period,days,method:e.method,pool:e.pool || d.id+':'+e.quota_index,priority:e.priority || 0,deal:d,quota:q,basis:e};
  }
  function estimates(d, now, settings = estimateSettings) {
    const definitions = Array.isArray(d.quota_estimates) ? d.quota_estimates : d.daily_estimate ? [d.daily_estimate] : [];
    return definitions.map(e=>estimateQuota(d,e,now,settings)).filter(Boolean);
  }
  function estimate(d, now, settings = estimateSettings) {
    const rows = estimates(d,now,settings);
    if (!rows.length) return null;
    if (rows.length === 1) return rows[0];
    const result = {rows,days:rows[0].days,period:'mixed',deal:d,daily:{low:0,typical:0,high:0},month:{low:0,typical:0,high:0}};
    for (const e of rows) for (const period of ['daily','month']) for (const key of ['low','typical','high']) result[period][key] += e[period][key];
    return result;
  }
  function estimateMany(deals, now, settings = estimateSettings, include = () => true) {
    const pools = new Map();
    for (const d of deals) {
      if (!free(d)) continue;
      for (const e of estimates(d,now,settings)) {
        if (!include(e)) continue;
        if (!pools.has(e.pool) || pools.get(e.pool).priority < e.priority) pools.set(e.pool,e);
      }
    }
    const rows = [...pools.values()];
    const result = {daily:{low:0,typical:0,high:0},month:{low:0,typical:0,high:0},count:rows.length,rows};
    for (const e of rows) for (const period of ['daily','month']) for (const key of ['low','typical','high']) result[period][key] += e[period][key];
    return result;
  }
  // Catalogue scale is broader than the verified ledger. Keep its three
  // components visible; estimates never promote an offer's source status.
  function catalogue(deals, now, settings = estimateSettings) {
    const regular = deals.filter(d=>free(d) && d.gate !== 'student' && d.type !== 'student' && phase(d,now) === 'active');
    const verified = sum(regular.filter(d=>d.verify_status === 'verified'),now);
    const pending = sum(regular.filter(d=>d.verify_status !== 'verified'),now);
    const estimates = estimateMany(regular,now,settings);
    const total = Object.fromEntries(['low','typical','high'].map(key=>[key,verified.total+pending.total+estimates.month[key]]));
    const unquantified = regular.filter(d=>!quota(d,now).total && !estimate(d,now,settings));
    const rows = regular.map(deal=>({deal,quota:quota(deal,now)})).filter(row=>row.quota.total>0);
    return {verified,pending,estimates,total,unquantified,rows};
  }
  // All internal totals use ten-thousand tokens, just like quota() and format().
  function monthlyLedger(deals, now = new Date(), settings = estimateSettings) {
    const eligible = deals.filter(d => free(d) && d.verify_status === 'verified'
      && d.gate !== 'student' && d.type !== 'student' && d.type !== 'paid_discount'
      && phase(d,now) === 'active');
    const pools = new Map();
    for (const deal of eligible) {
      entries(deal).forEach((q,index) => {
        const period = q.period || 'once';
        if (q.convert === false || !rawTokens(q) || !['once','daily','weekly','monthly'].includes(period)) return;
        const days = rowDays(deal,q,now);
        if (!days || !positive(q.amount)) return;
        const cycles = q.period === 'daily' ? days : q.period === 'weekly' ? days/7 : 1;
        const value = rawTokens(q) * cycles / 10000;
        const pool = q.pool || deal.id+':'+index;
        const limited = Boolean(deal.deadline || deal.quota_days || deal.type === 'limited_promo');
        const firstClaim = period === 'once' || deal.quota_introductory === true;
        const previous = pools.get(pool);
        // A repeatable entitlement takes precedence over another listing of the same pool.
        if (!previous || (previous.firstClaim && !firstClaim)
            || (previous.firstClaim === firstClaim && value > previous.value)) {
          pools.set(pool,{deal,q,days,value,limited,firstClaim});
        }
      });
    }
    const sorted = [...pools.values()].sort((a,b)=>b.value-a.value);
    const rows = sorted.filter(row=>!row.firstClaim);
    const firstClaimRows = sorted.filter(row=>row.firstClaim);
    const firstClaim = firstClaimRows.reduce((total,row)=>total+row.value,0);
    const standing = rows.reduce((n,r)=>n+(r.limited?0:r.value),0);
    const limited = rows.reduce((n,r)=>n+(r.limited?r.value:0),0);
    const nativePools = new Set(pools.keys());
    const recurring = eligible.filter(d=>!d.quota_introductory);
    const usage = estimateMany(recurring, now, settings, e => e.period !== 'once'
      && !nativePools.has(e.pool) && ['requests','neurons','model_rates','model_examples','scenario'].includes(e.method));
    return {standing,limited,total:standing+limited,firstClaim,firstMonth:standing+limited+firstClaim,rows,firstClaimRows,usage};
  }
  function estimateExplain(d, selected) {
    if (!selected) return estimates(d).map(e=>estimateExplain(d,e)).join('；');
    const e = selected;
    if (!e) return '';
    const basis = e.basis;
    const suffix = {once:msg(' tokens/次领取',' tokens/grant'),daily:msg(' tokens/天',' tokens/day'),weekly:msg(' tokens/周',' tokens/week'),monthly:msg(' tokens/月',' tokens/month')}[e.period];
    let text = native(e.quota)+' · '+msg('估计 ','Estimated ')+format(e.periodTokens.low)+'–'+format(e.periodTokens.high)+suffix;
    if (e.method === 'requests') text += msg('；每次请求假设含输入和输出 ','; assumed input + output per request ')+estimateSettings.requestTokens/4*(basis.scale||1)+' / '+estimateSettings.requestTokens*(basis.scale||1)+' / '+estimateSettings.requestTokens*2*(basis.scale||1)+' tokens';
    if (e.method === 'scenario') text += msg('；每积分假设 ','; assumed tokens per point ')+estimateSettings.pointTokens*.5*(basis.scale||1)+' / '+estimateSettings.pointTokens*(basis.scale||1)+' / '+estimateSettings.pointTokens*2*(basis.scale||1)+msg(' tokens，非官方扣费比例',' tokens; not an official billing ratio');
    if (e.method === 'credit_value') text += msg('；每积分售价参考 ','; price reference per credit ')+['low','typical','high'].map(key=>Number(basis.unit_value[key].toPrecision(6))).join(' / ')+' '+basis.currency+' ÷ '+rates[basis.currency]+' '+basis.currency+msg('/百万（DS Flash空闲价，输入:输出3:1、无缓存），估购买力，不代表实际 Token','/M (DS Flash off-peak, uncached 3:1 input/output); purchasing-power estimate, not delivered tokens');
    if (e.method === 'neurons') text += msg('；按三款可用模型的 Neurons 价格、输入:输出 3:1、无缓存估算','; three eligible model neuron rates, uncached 3:1 input/output');
    if (e.method === 'model_examples') text += msg('；按官方模型示例估算：','; based on official model examples: ')+['low','typical','high'].map(key=>{
      const m=basis.models[key];return m.name+' '+(m.input_tokens+m.output_tokens).toLocaleString(zh?'zh-CN':'en-US')+' tokens / '+m.credits+' credits';
    }).join(' · ');
    if (e.method === 'model_rates') text += msg('；官方积分/千Token价格，假设输入:输出=3:1、无缓存：','; official credits/1K tokens, assumed uncached 3:1 input/output: ')+['low','typical','high'].map(key=>{const m=basis.models[key];return m.name+' '+m.input+'/'+m.output;}).join(' · ');
    if (e.method === 'model_budget') text += msg('；原余额除以该模型每百万输入Token的价格，不估输出、不重复计DS购买力：','; balance divided by the model price per million INPUT tokens; output is not estimated, and DS purchasing power is not counted again: ')+basis.models.typical.name+' '+basis.models.typical.price+' '+e.quota.unit+'/M';
    text += ' · '+(zh?basis.note:basis.note_en||basis.note);
    return text;
  }
  function estimateCell(d, e) {
    if (!e || !e.month.high) return '';
    const first = e.rows?.[0] || e;
    const method = first.method;
    const mixed = e.rows?.length > 1;
    const dailyOnly = mixed ? e.rows.every(row=>row.period==='daily') : first.period==='daily';
    const label = method === 'model_budget' && !mixed ? msg('首月输入预算','First-month INPUT budget') : dailyOnly ? (method === 'credit_value' ? msg('购买力估计/天','Value estimate/day') : msg('用量估计/天','Usage estimate/day')) : method === 'credit_value' && !mixed ? msg('首月购买力估计','First-month value estimate') : msg('首月情景估计','First-month scenario');
    const value = dailyOnly ? e.daily : e.month;
    const range = format(value.low)+(value.low===value.high?'':'–'+format(value.high));
    const nativeText = mixed ? e.rows.length+msg(' 项独立额度',' independent allowances') : native(first.quota);
    return '<span class="quota-value quota-estimated" title="'+escape(mixed?nativeText:estimateExplain(d))+'"><span class="num">≈ '+range+'</span><span class="unit">'+label+'</span><span class="unit quota-native">'+escape(nativeText)+'</span><button type="button" class="estimate-link" data-estimate-id="'+escape(d.id)+'">'+msg('估算依据','Estimate basis')+'</button></span>';
  }
  function nativeSummary(d) {
    const rows = entries(d);
    if (rows.length > 3 && rows.every(q=>q.model && q.period==='once' && q.unit==='tokens' && q.amount===rows[0].amount)) {
      return msg(rows.length+' 款模型，各 ',' '+rows.length+' model pools, each ')+native(rows[0]);
    }
    return rows.map(native).join(' + ');
  }
  function rank(d) {
    return quota(d).total + (estimate(d)?.month.typical || 0);
  }
  function explain(d) {
    return entries(d).map(q => {
      let text = native(q);
      if (rates[q.unit] && q.convert !== false) text += ' ÷ '+(q.unit==='CNY'?'¥':'$')+rates[q.unit]+msg('/百万 = ≈','/M = ≈')+format(equivalent(q))+msg(' DS Flash 购买力参考',' DS Flash value reference');
      else if (q.tokens_per_unit) text += ' × '+Number(q.tokens_per_unit.toFixed(2))+msg(' tokens/积分 = ≈',' tokens/credit = ≈')+format(rawTokens(q)/10000)+msg(' 原始 tokens',' native tokens');
      if (q.equivalent_factor) text += ' × '+q.equivalent_factor.toFixed(4)+msg(' 价格比',' price ratio');
      if (q.convert === false || !equivalent(q)) text += msg(' · 暂无固定 Token 比例',' · no fixed token conversion');
      if (q.model) text += ' · '+q.model;
      if (q.note || q.note_en) text += ' · '+(zh?q.note:q.note_en||q.note);
      return text;
    }).join('；');
  }
  function cell(d, aggregate) {
    // An account-tested pack must not be presented as a mixed pool with trial/card offers.
    if (d.quota_basis === 'claimed_pack') aggregate = undefined;
    const q = aggregate || quota(d);
    if (phase(d) === 'expired') return '<span class="num">'+msg('已失效','Expired')+'</span>';
    if (phase(d) === 'upcoming' && !q.total) return '<span class="quota-value"><span class="quota-original">'+msg('即将开始','Upcoming')+'</span><span class="unit quota-native">'+escape(entries(d).map(native).join(' + '))+'</span></span>';
    if (q.total > 0) {
      const nativeText = aggregate ? (q.once ? msg('一次性 ','One-time ')+format(q.once) : '')
        + (q.monthly+q.dailyMonth ? (q.once?' + ':'')+msg('周期 ','Recurring ')+format(q.monthly+q.dailyMonth) : '')
        : nativeSummary(d);
      const label = d.quota_basis === 'claimed_pack' && !aggregate ? msg('已领礼包总量','Claimed pack total') : d.quota_paid ? msg('付费额度参考','Paid quota reference') : d.quota_upper_bound ? msg('首月上限','First-month maximum') : msg('首月参考','First-month reference');
      const extraEstimate = aggregate?.estimates?.count ? aggregate.estimates : estimate(d);
      const extraId = extraEstimate?.rows?.[0]?.deal.id || d.id;
      const extra = extraEstimate?.month.high ? '<button type="button" class="estimate-link" data-estimate-id="'+escape(extraId)+'">'+msg('另有额度估计','Additional allowance estimate')+'</button>' : '';
      return '<span class="quota-value" title="'+escape(explain(d)||nativeText)+'"><span class="num">'+(q.converted?'≈ ':'')+format(q.total)+'</span><span class="unit">'+label+'</span><span class="unit quota-native">'+escape(nativeText)+'</span>'+extra+'</span>';
    }
    const estimated = aggregate?.estimates?.count ? aggregate.estimates : null;
    if (estimated) return estimateCell(estimated.rows[0].deal,estimated);
    const individual = estimate(d);
    if (individual) return estimateCell(d,individual);
    const rows = entries(d);
    if (rows.length) return '<span class="quota-value" title="'+escape(explain(d))+'"><span class="quota-original">'+escape(native(rows[0]))+'</span><span class="unit">'+msg('保留原单位','Native units')+'</span></span>';
    if (d.unit === 'tool') return '<span class="quota-original">'+msg('免费工具','Free tool')+'</span>';
    if (d.category === 'freecloud') return '<span class="quota-original">'+(d.id==='amd-token-factory'?msg('按账号限额','Account limits'):msg('云与工具权益','Cloud & tool perks'))+'</span><span class="unit">'+msg('保留原单位','Native units')+'</span>';
    if (['price_low','pricing_plan','paid_discount','info','status','warning'].includes(d.type)) return '<span class="quota-original">'+msg('价格 / 规则','Pricing / terms')+'</span><span class="unit">'+msg('无独立赠额','No separate grant')+'</span>';
    if (d.free_models?.length) return '<span class="quota-original">'+msg('免费模型','Free models')+'</span><span class="unit">'+msg('未定额 / 动态限流','Unspecified / rate-limited')+'</span>';
    return '<span class="quota-original">'+msg('未公布','Not specified')+'</span><span class="unit">'+msg('Token 额度','Token quota')+'</span>';
  }
  // Only compatible, verified native API allowances offset a model's bill. DS value references never do.
  function allowance(deals, price, now) {
    let tokens = 0, cny = 0;
    for (const d of deals) {
      if (!free(d) || d.verify_status !== 'verified' || d.api_via !== 'api') continue;
      for (const q of entries(d)) {
        if (q.provider !== price.provider || (q.models && !q.models.includes(price.model)) || (q.excluded_models || []).includes(price.model)) continue;
        if (!q.models && !q.all_models) continue;
        const days=rowDays(d,q,now);
        if (!days) continue;
        const times = q.period==='daily' ? days : q.period==='weekly' ? days/7 : 1;
        tokens += rawTokens(q)*times/1e6;
        if (rates[q.unit]) cny += q.amount*times*(q.unit==='USD'?7.2:1);
      }
    }
    return {tokens,cny};
  }
  return {rates,sources,format,entries,nativeSummary,rawTokens,equivalent,native,phase,quota,sum,free,explain,cell,allowance,
    estimate,estimates,estimateMany,catalogue,monthlyLedger,estimateExplain,rank,estimateDefaults,setEstimateSettings,getEstimateSettings:()=>({...estimateSettings})};
})();
if (typeof module !== 'undefined') module.exports = TokenMath;
