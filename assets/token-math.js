/* Quotas use native units. Money is a purchasing-power reference, never delivered tokens. */
const TokenMath = (() => {
  const rates = Object.freeze({CNY: 1.75, USD: .2625});
  const sources = Object.freeze({CNY: 'https://api-docs.deepseek.com/zh-cn/quick_start/pricing/', USD: 'https://api-docs.deepseek.com/quick_start/pricing/'});
  const zh = typeof document === 'undefined' || document.documentElement.lang.startsWith('zh');
  const msg = (cn, en) => zh ? cn : en;
  const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const positive = value => Number.isFinite(value) && value > 0 ? value : 0;
  const format = wan => zh ? (wan >= 10000 ? (wan/10000).toFixed(2)+' 亿' : Number(wan.toFixed(1))+' 万')
    : wan >= 100000 ? (wan/100000).toFixed(2)+'B' : wan >= 100 ? (wan/100).toFixed(2)+'M' : Math.round(wan*10000).toLocaleString('en-US');
  function today(now = new Date()) {
    return new Intl.DateTimeFormat('en-CA', {timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit'}).format(now);
  }
  function activeDays(d, now) {
    let days = Math.min(30, positive(d.quota_days) || 30);
    if (/^\d{4}-\d{2}-\d{2}/.test(d.deadline || '')) {
      days = Math.min(days, Math.max(0, Math.floor((Date.parse(d.deadline.slice(0,10)+'T00:00:00Z')-Date.parse(today(now)+'T00:00:00Z'))/864e5)+1));
    }
    return days;
  }
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
    return (q.unit === 'tokens' ? format(q.amount/10000)+' tokens' : q.unit === 'CNY' ? '¥'+amount : q.unit === 'USD' ? '$'+amount : amount+(units[q.unit]||' '+q.unit))+suffix;
  }
  function quota(d, now) {
    const result = {once:0,daily:0,monthly:0,dailyMonth:0,total:0,converted:false,rows:entries(d),days:activeDays(d,now)};
    for (const q of result.rows) {
      const value = equivalent(q);
      const period = q.period || 'once';
      if (period === 'daily') result.daily += value;
      else if (period === 'monthly') result.monthly += value;
      else if (period === 'weekly') result.monthly += value*30/7;
      else result.once += value;
      if (value && (q.unit !== 'tokens' || q.equivalent_factor)) result.converted = true;
    }
    result.dailyMonth = result.daily*result.days;
    result.total = result.once+result.dailyMonth+result.monthly;
    if (d.verify_status === 'expired' || result.days === 0) {
      for (const key of ['once','daily','monthly','dailyMonth','total']) result[key] = 0;
    }
    return result;
  }
  function sum(deals, now) {
    return deals.reduce((s,d) => {
      const q = quota(d,now);
      for (const key of ['once','daily','monthly','dailyMonth','total']) s[key] += q[key];
      s.converted ||= q.converted;
      return s;
    }, {once:0,daily:0,monthly:0,dailyMonth:0,total:0,converted:false});
  }
  function free(d) {
    return d.published !== false && d.verify_status !== 'expired' && !['freecloud','intel_source'].includes(d.category)
      && !['warning','price_low','pricing_plan','subscription_bonus','status'].includes(d.type)
      && !['subscribe','subscription'].includes(d.via) && !d.quota_paid && !d.quota_upper_bound && !d.quota_conditional
      && !['startup','audit','oss'].includes(d.gate);
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
    const q = aggregate || quota(d);
    if (d.verify_status === 'expired') return '<span class="num">'+msg('已失效','Expired')+'</span>';
    if (q.total > 0) {
      const nativeText = aggregate ? (q.once ? msg('一次性 ','One-time ')+format(q.once) : '')
        + (q.monthly+q.dailyMonth ? (q.once?' + ':'')+msg('周期 ','Recurring ')+format(q.monthly+q.dailyMonth) : '')
        : entries(d).map(native).join(' + ');
      const label = d.quota_paid ? msg('付费额度参考','Paid quota reference') : d.quota_upper_bound ? msg('首月上限','First-month maximum') : msg('首月参考','First-month reference');
      return '<span class="quota-value" title="'+escape(explain(d)||nativeText)+'"><span class="num">'+(q.converted?'≈ ':'')+format(q.total)+'</span><span class="unit">'+label+'</span><span class="unit quota-native">'+escape(nativeText)+'</span></span>';
    }
    const rows = entries(d);
    if (rows.length) return '<span class="quota-value" title="'+escape(explain(d))+'"><span class="quota-original">'+escape(native(rows[0]))+'</span><span class="unit">'+msg('保留原单位','Native units')+'</span></span>';
    if (d.unit === 'tool') return '<span class="quota-original">'+msg('免费工具','Free tool')+'</span>';
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
        const times = q.period==='daily' ? activeDays(d,now) : q.period==='weekly' ? 30/7 : 1;
        tokens += rawTokens(q)*times/1e6;
        if (rates[q.unit]) cny += q.amount*times*(q.unit==='USD'?7.2:1);
      }
    }
    return {tokens,cny};
  }
  return {rates,sources,format,entries,rawTokens,equivalent,native,quota,sum,free,explain,cell,allowance};
})();
if (typeof module !== 'undefined') module.exports = TokenMath;
