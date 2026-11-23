/* A catalogue scenario is not the verified allowance ledger or an API balance. */
const CatalogueUI = (() => {
  const m = Workbench.msg, f = TokenMath.format;
  const esc = value => String(value ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const nativeAmount = wan => wan>=10000 && document.documentElement.lang.startsWith('zh')
    ? (wan/10000).toLocaleString('zh-CN',{maximumFractionDigits:4})+' 亿' : f(wan);
  const range = value => value.low===value.high?f(value.low):f(value.low)+'–'+f(value.high);
  function banner(deals) {
    const monthly = TokenMath.monthlyLedger(deals);
    document.getElementById('gbNum').textContent = nativeAmount(monthly.total);
    document.getElementById('gbBreakdown').innerHTML = [
      [m('常规','Recurring'),monthly.standing], [m('限时','Limited'),monthly.limited]
    ].map(([label,value])=>'<span>'+label+' <strong>'+f(value)+'</strong></span>').join('');
    document.getElementById('globalBanner').title = m('按各平台免费规则分别用满；点击查看模型、限制与有效天数。','Assumes full use on each platform. Open for models, limits and active days.');
  }
  function ledger(deals) {
    const c = TokenMath.catalogue(deals);
    const rows = [...c.rows].sort((a,b)=>b.quota.total-a.quota.total);
    const estimates = [...c.estimates.rows].sort((a,b)=>b.month.typical-a.month.typical);
    const item = (d,value,basis) => '<li><div><a href="'+esc(d.url)+'" target="_blank" rel="noopener">'+esc(d.provider)+' ↗</a>'
      +Workbench.freshness(d)+'<small>'+esc(basis)+'</small></div><strong>'+value+'</strong></li>';
    const monthly = TokenMath.monthlyLedger(deals);
    const nativeRows = monthly.rows.map(({deal,q,days,value,limited}) => {
      const source = deal.sources?.find(s=>s.kind==='official');
      const basis = [TokenMath.native(q), q.model, limited ? days+m(' 个有效日',' active days') : ''].filter(Boolean).join(' · ');
      return item({...deal,url:source?.url || deal.url},f(value),basis);
    }).join('');
    return `<section class="catalogue-overview" aria-labelledby="monthlyTitle">
      <div class="catalogue-title"><div><h3 id="monthlyTitle">${m('未来 30 天可用的免费 Token','Free tokens available over the next 30 days')}</h3><p>${m('从北京时间今天起，按每个平台的免费上限分别用满。日额按有效日累计，月额计一个周期。','From today in Beijing time, assuming full use on each platform. Daily caps count active days, monthly caps count one cycle.')}</p></div><b>${nativeAmount(monthly.total)}</b></div>
      <div class="catalogue-parts"><div><span>${m('常规额度 · 每 30 天','Recurring · per 30 days')}</span><b>${f(monthly.standing)}</b></div><div><span>${m('限时活动 · 只计剩余天数','Promotions · remaining days only')}</span><b>${f(monthly.limited)}</b></div></div>
      <details class="catalogue-detail" open><summary>${m('逐项额度与官方规则','Allowances and official terms')} · ${monthly.rows.length}</summary><ul>${nativeRows}</ul></details>
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
      <details class="catalogue-detail"><summary>${m('逐项核对：额度与状态','Itemized allowances and status')} · ${rows.length}</summary><ul>${rows.map(({deal,quota})=>item(deal,f(quota.total),TokenMath.entries(deal).map(TokenMath.native).join(' + '))).join('')}</ul></details>
      <details class="catalogue-detail"><summary>${m('额度估计明细（不与上方重复）','Additional allowance scenarios (no overlap above)')} · ${estimates.length}</summary><ul>${estimates.map(e=>item(e.deal,f(e.month.typical),TokenMath.native(e.quota)+' · '+m('首月估计 ','Month estimate ')+range(e.month))).join('')}</ul></details>
      <details class="catalogue-detail"><summary>${m('尚未计入：不限量、未定额或不适合折算','Not quantified: unlimited, unspecified or non-token offers')} · ${c.unquantified.length}</summary><p class="calc-note">${m('未计入数字不等于没有价值；未公布上限不能当作零或随意补一个 Token 数。音频、生图、工具与算力保留原单位。','Unquantified does not mean valueless. An unpublished cap is neither zero nor a made-up token amount. Audio, images, tools and compute keep native units.')}</p><ul>${c.unquantified.map(d=>item(d,m('另列','Separate'),TokenMath.entries(d).map(TokenMath.native).join(' + ') || (d.value_en && document.documentElement.lang==='en' ? d.value_en : d.summary || d.value))).join('')}</ul></details>
    </section><h3 class="verified-ledger-title">${m('已核验总账 · 常规领取口径','Verified ledger · standard eligibility')}</h3>`;
  }
  return {banner,ledger};
})();
