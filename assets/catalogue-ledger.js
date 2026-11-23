/* A catalogue scenario is not the verified allowance ledger or an API balance. */
const CatalogueUI = (() => {
  const m = Workbench.msg, f = TokenMath.format;
  const esc = value => String(value ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const nativeAmount = wan => {
    if (document.documentElement.lang.startsWith('zh') && wan>=10000) return (wan/10000).toLocaleString('zh-CN',{maximumFractionDigits:4})+' 亿';
    if (document.documentElement.lang==='en' && wan>=100000) return (wan/100000).toLocaleString('en-US',{maximumFractionDigits:5})+'B';
    return f(wan);
  };
  const range = value => value.low===value.high?f(value.low):f(value.low)+'–'+f(value.high);
  const monthName = month => m(Number(month.slice(5))+' 月',new Intl.DateTimeFormat('en',{month:'long',timeZone:'UTC'}).format(new Date(month+'-01T00:00:00Z')));
  function banner(deals) {
    const monthly = TokenMath.monthlyLedger(deals);
    const calendar = TokenMath.calendarLedger(deals);
    const dated = calendar.rows.length>0;
    document.querySelector('#globalBanner .gb-label').textContent = dated
      ? monthName(calendar.month)+m('有据活动 · 全月上限',' dated offers · full month')
      : m('未来 30 天 · 含首领与试用','Next 30 days · incl. first claims');
    document.getElementById('gbNum').textContent = nativeAmount(dated?calendar.total:monthly.firstMonth);
    const parts = dated ? [
      [m('余期 · 有据活动','Remaining dated offers'),calendar.remaining],
      [m('未来 30 天 · 含首领','Next 30 days incl. trials'),monthly.firstMonth]
    ] : [
      [m('周期额度','Recurring caps'),monthly.total],
      [m('首领及试用','First claims & trials'),monthly.firstClaim]
    ];
    document.getElementById('gbBreakdown').innerHTML = parts.map(([label,value])=>'<span>'+label+' <strong>'+nativeAmount(value)+'</strong></span>').join('');
    document.getElementById('gbEstimate').textContent = dated ? m('含已结束活动，按平台分别用满','Includes past offers at full eligible use') : m('按各平台分别用满估算','Assumes full eligible use per platform');
    document.getElementById('globalBanner').title = m('查看活动日期、领取条件与计算明细','View offer dates, eligibility and calculations');
  }
  function calendarSection(deals,calendar) {
    const amount=nativeAmount;
    const rows = calendar.rows.map(({deal,q,term,value,remaining,days})=>{
      const end = term.observed_through || deal.deadline.slice(0,10);
      const note = m(term.note || deal.rule,term.note_en || deal.rule_en || deal.rule);
      const dates = term.start.slice(0,10)+' → '+end+(term.observed_through ? m('（末次核见）',' (last observed)') : '');
      const needsReview = term.observed_through && TokenMath.today()>term.observed_through && calendar.month===TokenMath.today().slice(0,7);
      const remainingText = needsReview ? m('余期待复核','Availability unconfirmed') : m('余期 ','Remaining ')+amount(remaining);
      const formula = q.period==='daily' ? amount(TokenMath.rawTokens(q)/10000)+m('/天 × ','/day × ')+days+m(' 天',' days') : m('单次领取','One claim');
      return '<li><div><a href="'+esc(term.source || deal.url)+'" target="_blank" rel="noopener">'+esc(deal.group || deal.provider)+' ↗</a><small>'+esc(dates+' · '+formula)+'</small><small>'+esc(note)+'</small></div><strong>'+amount(value)+'<small>'+remainingText+'</small></strong></li>';
    });
    const tiers = [];
    for (const deal of deals.filter(d=>d.conditional_tiers && d.published!==false)) {
      for (const tier of deal.conditional_tiers) {
        const promotion = tier.window==='campaign';
        const window = calendar.rows.find(r=>r.deal===deal);
        if (promotion && !window) continue;
        const daily = tier.daily_groups.reduce((a,b)=>a+b,0)/10000;
        const period = promotion?window.days:30;
        const note = m(tier.note || deal.rule,tier.note_en || deal.rule_en || deal.rule);
        tiers.push('<li><div><a href="'+esc(deal.url)+'" target="_blank" rel="noopener">'+esc(deal.group || deal.provider)+' · '+esc(m(tier.label,tier.label_en))+' ↗</a><small>'+tier.daily_groups.map(v=>amount(v/10000)).join(' + ')+m(' / 天',' / day')+' · '+esc(note)+'</small></div><strong>'+amount(daily*period)+'<small>'+ (promotion?m('全月条件档','Full-month tier'):m('按现行规则 × 30 天','Current terms × 30 days'))+'</small></strong></li>');
      }
    }
    const personal = calendar.personal.map(({deal,term,value})=>'<li><div><a href="'+esc(term.source)+'">'+esc(deal.group || deal.provider)+' ↗</a><small>'+esc(m(term.note,term.note_en))+'</small></div><strong>'+amount(value)+'</strong></li>');
    return '<section class="catalogue-overview" aria-label="'+m('自然月账本','Calendar month ledger')+'"><div class="catalogue-title"><div><h3>'+calendar.month+' · '+m('自然月活动账本','Calendar-month offers')+'</h3><p>'+m('北京时间。全月包含已过窗口，余期假设今日额度和可领礼包均未用。只收有日期证据的活动，常规额度另见滚动账本。','Beijing time. Full month includes elapsed windows. Remaining assumes today’s caps and available grants are unused. Dated offers only. Standing allowances appear in the rolling ledger.')+'</p></div><b>'+ (rows.length?amount(calendar.total):m('待核','No dated offers'))+'</b></div>'
      +(calendar.carryIn ? '<p class="calc-note">'+m('其中 '+amount(calendar.carryIn)+' 来自上月开启、当时尚未领取的礼包。若上月已领，本月合计 '+amount(calendar.total-calendar.carryIn)+'。',amount(calendar.carryIn)+' carried over in unclaimed packs. If previously claimed, the full-month subtotal is '+amount(calendar.total-calendar.carryIn)+'.')+'</p>' : '')
      +(rows.length?'<details class="catalogue-detail" open><summary>'+m('本月逐项明细','Itemized offers')+' · '+m('余期 ','Remaining ')+amount(calendar.remaining)+'</summary><ul>'+rows.join('')+'</ul></details>':'')
      +(tiers.length?'<details class="catalogue-detail"><summary>'+m('有条件的额度 · 档位互斥','Conditional allowances · alternative tiers')+'</summary><ul>'+tiers.join('')+'</ul></details>':'')
      +(personal.length?'<details class="catalogue-detail"><summary>'+m('单账号实领记录','Observed on one account')+'</summary><ul>'+personal.join('')+'</ul></details>':'')+'</section>';
  }
  function ledger(deals) {
    const c = TokenMath.catalogue(deals);
    const rows = [...c.rows].sort((a,b)=>b.quota.total-a.quota.total);
    const estimates = [...c.estimates.rows].sort((a,b)=>b.month.typical-a.month.typical);
    const item = (d,value,basis) => '<li><div><a href="'+esc(d.url)+'" target="_blank" rel="noopener">'+esc(d.provider)+' ↗</a>'
      +Workbench.freshness(d)+'<small>'+esc(basis)+'</small></div><strong>'+value+'</strong></li>';
    const monthly = TokenMath.monthlyLedger(deals);
    const firstByDeal = new Map();
    for (const row of monthly.firstClaimRows) {
      const group = firstByDeal.get(row.deal.id) || [];
      group.push(row);
      firstByDeal.set(row.deal.id,group);
    }
    const termsRow = ({deal,q,days,value},group) => {
      const source = deal.sources?.find(s=>s.kind==='official');
      const rules = document.documentElement.lang.startsWith('zh') ? deal.rule : deal.rule_en || deal.rule;
      const multi = group.length>1;
      const amount = multi ? group.reduce((sum,row)=>sum+row.value,0) : value;
      const terms = multi ? group.map(row=>row.q.model+' '+TokenMath.native(row.q)).join(' · ') : [TokenMath.native(q),q.model].filter(Boolean).join(' · ');
      const basis = [terms, q.period==='daily' ? days+m(' 天',' days') : '', rules].filter(Boolean).join(' · ');
      return item({...deal,url:deal.quota_source_url || source?.url || deal.url},nativeAmount(amount),basis);
    };
    const calendar = TokenMath.calendarLedger(deals);
    const archives = [...new Set(deals.filter(d=>d.calendar_window).map(d=>(d.calendar_window.observed_through || d.deadline).slice(0,7)))].filter(month=>month<calendar.month).sort().reverse();
    const archive = archives.map(month=>'<details class="catalogue-detail"><summary>'+month+' · '+m('历史活动账本','Archived offers')+'</summary>'+calendarSection(deals,TokenMath.calendarLedger(deals,new Date(),month))+'</details>').join('');
    return calendarSection(deals,calendar)+archive+`<section class="catalogue-overview" aria-labelledby="monthlyTitle">
      <div class="catalogue-title"><div><h3 id="monthlyTitle">${m('从今天起 30 天 · 含首领与试用','Next 30 days · including first claims and trials')}</h3><p>${m('假设今天开始、各平台和模型分别用满，且首领和试用尚未使用。含端内专用额度。','Assumes full use from today across separate platforms and models, with all first claims and trials unused. Includes in-app tokens.')}</p></div><b>${nativeAmount(monthly.firstMonth)}</b></div>
      <div class="catalogue-parts">
        <div><span>${m('常规 · 每 30 天','Recurring · per 30 days')}</span><b>${nativeAmount(monthly.standing)}</b></div>
        <div><span>${m('限时 · 剩余有效日','Promotions · remaining days')}</span><b>${nativeAmount(monthly.limited)}</b></div>
        <div><span>${m('首次领取及新户试用','First claims & new trials')}</span><b>${nativeAmount(monthly.firstClaim)}</b></div>
      </div>
      <details class="catalogue-detail" open><summary>${m('未来 30 天周期额度','Recurring caps over the next 30 days')} · ${nativeAmount(monthly.total)}</summary><ul>${monthly.rows.map(row=>termsRow(row,[row])).join('')}</ul></details>
      <details class="catalogue-detail"><summary>${m('首领与试用明细','First claims and trial terms')} · ${nativeAmount(monthly.firstClaim)}</summary><ul>${[...firstByDeal.values()].map(group=>termsRow(group[0],group)).join('')}</ul></details>
      <details class="catalogue-detail"><summary>${m('其他免费用量 · 单独估算','Other free usage · separate estimate')} ≈ ${f(monthly.usage.month.typical)}</summary>
      <p class="calc-note">${m('已核验的周期性请求、积分和算力按当前用量假设折算。估计区间','Verified recurring requests, credits and compute converted under the current usage assumptions. Range')} ${range(monthly.usage.month)}。</p>
      <ul>${monthly.usage.rows.map(e=>item(e.deal,f(e.month.typical),TokenMath.estimateExplain(e.deal,e))).join('')}</ul></details>
      </section><section class="catalogue-overview" aria-labelledby="catalogueTitle">
      <div class="catalogue-title"><div><h3 id="catalogueTitle">${m('全站收录 · 首月情景参考','Catalogue · first-month scenario')}</h3><p>${m('含待复核与可调估计；各平台分别领取，不是保证到账量。','Includes pending offers and editable estimates; claimed separately, not guaranteed grants.')}</p></div><b id="catalogueTotal">≈ ${f(c.total.typical)}</b></div>
      <div class="catalogue-parts">
        <div><span>${m('已核验额度参考','Verified allowance reference')}</span><b>${f(c.verified.total)}</b><small>${m('可直接折算的常规权益','Convertible standard offers')}</small></div>
        <div><span>${m('待复核额度参考','Pending allowance reference')}</span><b>${f(c.pending.total)}</b><small>${m('旧记录或尚欠现行证据','Stale or awaiting current evidence')}</small></div>
        <div><span>${m('额度首月估计','Allowance scenarios: first month')}</span><b>${f(c.estimates.month.typical)}</b><small>${c.estimates.count} ${m('个独立池，按活动有效天数','independent pools, active days only')}</small></div>
      </div>
      <p class="catalogue-range">${m('情景区间','Scenario range')} <strong>${range(c.total)}</strong> · <button type="button" data-open-daily-estimates>${m('调整用量估计','Adjust usage estimates')} ↗</button></p>
      <p class="calc-note">${m('参考值 = 已核验 + 待复核 + 情景估计。原始 Token 与 DS Flash 购买力参考混合汇总，不代表同一模型余额；待复核项可能已调整或失效。学生、申请制、付费及随机上限另列。','Reference = verified + pending + allowance scenarios. Mixes native tokens and DS Flash purchasing-power references, not a single-model balance. Pending offers may have changed or ended. Student, application-based, paid and random maximum offers stay separate.')}</p>
      <details class="catalogue-detail"><summary>${m('逐项核对：额度与状态','Itemized allowances and status')} · ${rows.length}</summary><ul>${rows.map(({deal,quota})=>item(deal,f(quota.total),TokenMath.nativeSummary(deal))).join('')}</ul></details>
      <details class="catalogue-detail"><summary>${m('额度估计明细（不与上方重复）','Additional allowance scenarios (no overlap above)')} · ${estimates.length}</summary><ul>${estimates.map(e=>item(e.deal,f(e.month.typical),TokenMath.native(e.quota)+' · '+m('首月估计 ','Month estimate ')+range(e.month))).join('')}</ul></details>
      <details class="catalogue-detail"><summary>${m('尚未计入：不限量、未定额或不适合折算','Not quantified: unlimited, unspecified or non-token offers')} · ${c.unquantified.length}</summary><p class="calc-note">${m('未计入数字不等于没有价值；未公布上限不能当作零或随意补一个 Token 数。音频、生图、工具与算力保留原单位。','Unquantified does not mean valueless. An unpublished cap is neither zero nor a made-up token amount. Audio, images, tools and compute keep native units.')}</p><ul>${c.unquantified.map(d=>item(d,m('另列','Separate'),TokenMath.entries(d).map(TokenMath.native).join(' + ') || (d.value_en && document.documentElement.lang==='en' ? d.value_en : d.summary || d.value))).join('')}</ul></details>
    </section><h3 class="verified-ledger-title">${m('已核验总账 · 常规领取口径','Verified ledger · standard eligibility')}</h3>`;
  }
  return {banner,ledger};
})();
