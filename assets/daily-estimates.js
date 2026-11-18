/* Editable daily-usage scenarios, kept separate from verified allowances and API billing. */
const DailyEstimateUI = (() => {
  const zh = document.documentElement.lang.startsWith('zh');
  const msg = (cn,en) => zh ? cn : en;
  const esc = value => String(value ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const f = TokenMath.format;
  const range = value => f(value.low)+'–'+f(value.high);
  const dialog = document.createElement('dialog');
  dialog.id = 'dailyEstimateDialog';
  dialog.setAttribute('aria-labelledby','dailyEstimateTitle');
  dialog.innerHTML = `<div class="estimate-dialog-head"><h3 id="dailyEstimateTitle">${msg('每日免费额度估计','Daily free allowance estimates')}</h3><button type="button" data-close-estimates aria-label="${msg('关闭','Close')}">✕</button></div>
    <p class="estimate-intro">${msg('看大致量级：低用量 / 参考 / 高用量是情景假设，实际随模型、上下文、缓存和任务变化。积分售价折的是购买力；原始日额度始终保留。','Compare approximate scale: low / reference / high are scenarios, not confidence bounds. Actual usage depends on models, context, caching and tasks. Credit prices estimate purchasing power; native daily quotas stay visible.')}</p>
    <form class="estimate-settings" onsubmit="return false">
      <label>${msg('每次请求参考 Tokens','Reference tokens/request')}<input id="estimateRequestTokens" type="number" min="1" max="1000000" step="100" inputmode="numeric"></label>
      <label>${msg('未知积分的参考 Tokens/积分','Unpriced points: reference tokens/point')}<input id="estimatePointTokens" type="number" min="1" max="1000000" step="100" inputmode="numeric"></label>
      <button type="button" data-reset-estimates>${msg('恢复默认','Reset')}</button>
      <small>${msg('次数按参考值的 ¼–2 倍；未知积分按 ½–2 倍作示意，部分平台有独立倍率。不是官方积分兑换率，可按自己的实测修改。','Requests use ¼–2× the reference; unpriced points use an illustrative ½–2×, with platform-specific scales where noted. These are not official credit conversion rates; adjust to your own measurements.')}</small>
    </form>
    <div id="dailyEstimateBody"></div>`;
  document.body.append(dialog);
  let selected = '';
  const data = () => typeof DEALS === 'undefined' ? [] : DEALS;
  function render() {
    const deals = data().filter(d=>TokenMath.free(d));
    const total = TokenMath.estimateMany(deals);
    const candidates = deals.map(d=>TokenMath.estimate(d)).filter(Boolean).sort((a,b)=>{
      if (a.deal.id===selected) return -1;
      if (b.deal.id===selected) return 1;
      return b.daily.typical-a.daily.typical;
    });
    const counted = new Set(total.rows.map(e=>e.deal.id));
    const kinds = {requests:msg('次数情景','Request scenario'),credit_value:msg('售价购买力','Price-based value'),neurons:msg('模型价格情景','Model-rate scenario'),scenario:msg('可调假设','Editable assumption')};
    document.getElementById('dailyEstimateBody').innerHTML = `<div class="estimate-totals">
      <div><span>${msg('独立额度池','Independent pools')}</span><b>${total.count}</b><small>${msg('共享额度只加一次','Shared allowances counted once')}</small></div>
      <div><span>${msg('日估计（含购买力参考）','Daily estimate, including value references')}</span><b>${range(total.daily)}</b><small>${msg('参考情景 ','Reference scenario ')}${f(total.daily.typical)}</small></div>
      <div><span>${msg('首月情景估计','First-month scenario')}</span><b>${range(total.month)}</b><small>${msg('按实际活动天数，最多30天','Remaining active days, up to 30')}</small></div>
    </div><p class="estimate-scope">${msg('以下含待复核日额度；来源状态与估算假设分别列出。情景估计独立展示，不充当已核验 Token，也不直接抵扣 API 月费。','Includes pending-review daily quotas. Source status and estimation assumptions are separate. Scenarios stay distinct from verified token allowances and never directly offset API bills.')}</p>
    <div class="estimate-list">${candidates.map(e=>{
      const d=e.deal;
      const source=d.daily_estimate.source_url;
      return `<article class="estimate-item${d.id===selected?' selected':''}" data-estimate-row="${esc(d.id)}">
        <header><strong>${esc(d.provider)}</strong><span class="estimate-kind">${kinds[e.method]}</span>${Workbench.freshness(d)}</header>
        <div class="estimate-metrics"><div><span>${msg('原始日额','Native daily quota')}</span><b>${esc(TokenMath.native(e.quota))}</b></div><div><span>${msg('估计 Tokens/天','Estimated tokens/day')}</span><b>${range(e.daily)}</b><small>${msg('参考 ','Reference ')}${f(e.daily.typical)}</small></div><div><span>${msg('首月参考','First-month estimate')}</span><b>${range(e.month)}</b><small>${e.days}${msg(' 天',' days')}</small></div></div>
        ${!counted.has(d.id)?`<p class="estimate-shared">${msg('共享额度视图，合计中已去重','Shared-pool view, deduplicated in the total')}</p>`:''}
        <details><summary>${msg('假设与依据','Assumptions and sources')}</summary><p>${esc(TokenMath.estimateExplain(d))}</p>${e.method==='neurons'?'<p>'+esc(Object.values(d.daily_estimate.models).map(model=>model.name+': '+model.input+'/'+model.output+' Neurons/M input/output').join(' · '))+'</p>':''}${source&&/^https?:\/\//.test(source)?`<a href="${esc(source)}" target="_blank" rel="noopener">${msg('公开价格 / 额度依据','Published rate / quota source')} ↗</a>`:''}<p>${msg('参数整理日期：','Parameters reviewed: ')}${esc(d.daily_estimate.reviewed_at)} · ${msg('原始领取规则与更多信源见列表条目。','See the offer row for claim rules and additional sources.')}</p></details>
      </article>`;
    }).join('')}</div>`;
  }
  function open(id = '') {
    selected = id;
    const settings = TokenMath.getEstimateSettings();
    document.getElementById('estimateRequestTokens').value=settings.requestTokens;
    document.getElementById('estimatePointTokens').value=settings.pointTokens;
    render();
    if (!dialog.open) dialog.showModal();
    dialog.scrollTop=0;
  }
  function refresh() { if(dialog.open) render(); }
  function apply(settings) {
    const next=TokenMath.setEstimateSettings(settings);
    document.getElementById('estimateRequestTokens').value=next.requestTokens;
    document.getElementById('estimatePointTokens').value=next.pointTokens;
    if (typeof window.render==='function') window.render();
    if (document.getElementById('sumPanel')?.classList.contains('open')) sumRender();
    render();
  }
  document.addEventListener('click', event=>{
    const target=event.target.closest('[data-open-daily-estimates],[data-estimate-id]');
    if (target) { event.preventDefault();open(target.dataset.estimateId || ''); }
    if (event.target.closest('[data-close-estimates]')) dialog.close();
    if (event.target.closest('[data-reset-estimates]')) apply(TokenMath.estimateDefaults);
  });
  dialog.addEventListener('click', event=>{if(event.target===dialog){const box=dialog.getBoundingClientRect();if(event.clientX<box.left||event.clientX>box.right||event.clientY<box.top||event.clientY>box.bottom)dialog.close();}});
  dialog.addEventListener('change',event=>{
    if(event.target.id==='estimateRequestTokens') apply({requestTokens:event.target.value});
    if(event.target.id==='estimatePointTokens') apply({pointTokens:event.target.value});
  });
  dialog.addEventListener('close',()=>{
    const button = selected ? [...document.querySelectorAll('[data-estimate-id]')].find(b=>b.dataset.estimateId===selected)
      : document.querySelector('[data-open-daily-estimates]');
    button?.focus({preventScroll:true});
  });
  return {open,refresh};
})();
