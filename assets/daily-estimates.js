/* Editable allowance scenarios, kept separate from verified allowances and API billing. */
const DailyEstimateUI = (() => {
  const zh = document.documentElement.lang.startsWith('zh');
  const msg = (cn,en) => zh ? cn : en;
  const esc = value => String(value ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const f = TokenMath.format;
  const range = value => value.low===value.high?f(value.low):f(value.low)+'–'+f(value.high);
  const dialog = document.createElement('dialog');
  dialog.id = 'dailyEstimateDialog';
  dialog.setAttribute('aria-labelledby','dailyEstimateTitle');
  dialog.innerHTML = `<div class="estimate-dialog-head"><h3 id="dailyEstimateTitle">${msg('额度换算与估计','Allowance conversions & estimates')}</h3><button type="button" data-close-estimates aria-label="${msg('关闭','Close')}">✕</button></div>
    <p class="estimate-intro">${msg('一次性计一次，月额计一期，日额按有效天数（最多30天），周额按有效天数÷7。低 / 参考 / 高是用量情景；积分售价仅估购买力，原始额度和领取条件始终保留。','One-time grants and monthly allowances count once; daily grants use active days (up to 30), weekly grants use active days ÷ 7. Low / reference / high are usage scenarios. Credit prices estimate purchasing power; native allowances and eligibility stay visible.')}</p>
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
    const deals = data().filter(d=>d.published!==false && d.verify_status!=='expired');
    const total = TokenMath.estimateMany(deals);
    const candidates = deals.flatMap(d=>TokenMath.estimates(d)).sort((a,b)=>{
      if (a.deal.id===selected) return -1;
      if (b.deal.id===selected) return 1;
      return b.month.typical-a.month.typical;
    });
    const counted = new Set(total.rows.map(e=>e.basis));
    const kinds = {requests:msg('次数情景','Request scenario'),credit_value:msg('售价购买力','Price-based value'),neurons:msg('模型价格情景','Model-rate scenario'),model_examples:msg('官方模型示例','Official model examples'),scenario:msg('可调假设','Editable assumption')};
    document.getElementById('dailyEstimateBody').innerHTML = `<div class="estimate-totals">
      <div><span>${msg('独立额度池','Independent pools')}</span><b>${total.count}</b><small>${msg('共享额度只加一次','Shared allowances counted once')}</small></div>
      <div><span>${msg('其中日额度部分 / 天','Daily allowance component / day')}</span><b>${range(total.daily)}</b><small>${msg('参考情景 ','Reference scenario ')}${f(total.daily.typical)}</small></div>
      <div><span>${msg('首月情景估计','First-month scenario')}</span><b>${range(total.month)}</b><small>${msg('按实际活动天数，最多30天','Remaining active days, up to 30')}</small></div>
    </div><p class="estimate-scope">${msg('合计仅含常规免费权益，含待复核记录；付费、邀请等额外条件项单列。情景估计独立展示，不充当已核验 Token，也不直接抵扣 API 月费。','Totals cover standard free offers, including pending records. Paid and conditional offers are shown separately. Scenarios are distinct from verified tokens and never directly offset API bills.')}</p>
    <div class="estimate-list">${candidates.map(e=>{
      const d=e.deal;
      const basis=e.basis, source=basis.source_url;
      const periodLabel={once:msg('本次领取估计','This grant estimate'),daily:msg('估计 Tokens/天','Estimated tokens/day'),weekly:msg('估计 Tokens/周','Estimated tokens/week'),monthly:msg('估计 Tokens/月','Estimated tokens/month')}[e.period];
      return `<article class="estimate-item${d.id===selected?' selected':''}" data-estimate-row="${esc(d.id)}">
        <header><strong>${esc(d.provider)}</strong><span class="estimate-kind">${kinds[e.method]}</span>${Workbench.freshness(d)}</header>
        <div class="estimate-metrics"><div><span>${msg('原始额度','Native allowance')}</span><b>${esc(TokenMath.native(e.quota))}</b></div><div><span>${periodLabel}</span><b>${range(e.periodTokens)}</b><small>${msg('参考 ','Reference ')}${f(e.periodTokens.typical)}</small></div><div><span>${msg('首月参考','First-month estimate')}</span><b>${range(e.month)}</b><small>${e.period==='daily'?e.days+msg(' 天',' days'):e.period==='weekly'?e.days+msg('天 ÷ 7',' days ÷ 7'):msg('只计一次，不乘30','Counted once, never ×30')}</small></div></div>
        ${!counted.has(basis)?`<p class="estimate-shared">${TokenMath.free(d)?msg('共享额度视图，合计中已去重','Shared-pool view, deduplicated in the total'):msg('付费或额外条件权益，不计入免费合计','Paid or conditional offer, excluded from free totals')}</p>`:''}
        <details><summary>${msg('假设与依据','Assumptions and sources')}</summary><p>${esc(TokenMath.estimateExplain(d,e))}</p>${e.method==='neurons'?'<p>'+esc(Object.values(basis.models).map(model=>model.name+': '+model.input+'/'+model.output+' Neurons/M input/output').join(' · '))+'</p>':''}${source&&/^https?:\/\//.test(source)?`<a href="${esc(source)}" target="_blank" rel="noopener">${msg('公开价格 / 额度依据','Published rate / quota source')}</a>`:''}<p>${msg('参数整理日期：','Parameters reviewed: ')}${esc(basis.reviewed_at)} · ${msg('原始领取规则与更多信源见列表条目。','See the offer row for claim rules and additional sources.')}</p></details>
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
    if (typeof window.calcGlobalBanner==='function') window.calcGlobalBanner();
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
  function editSetting(event) {
    const key={estimateRequestTokens:'requestTokens',estimatePointTokens:'pointTokens'}[event.target.id];
    if (!key) return;
    const value=Number(event.target.value);
    if (Number.isFinite(value) && value>=1 && value<=1000000) apply({[key]:value});
    else if (event.type==='change') apply({});
  }
  dialog.addEventListener('input',editSetting);
  dialog.addEventListener('change',editSetting);
  dialog.addEventListener('close',()=>{
    const button = selected ? [...document.querySelectorAll('[data-estimate-id]')].find(b=>b.dataset.estimateId===selected)
      : document.querySelector('[data-open-daily-estimates]');
    button?.focus({preventScroll:true});
  });
  return {open,refresh};
})();
