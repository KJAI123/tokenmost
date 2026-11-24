/* Shared interactions for the two homepages. */
const Workbench = (() => {
  const zh = document.documentElement.lang.startsWith('zh');
  const msg = (cn, en) => zh ? cn : en;
  const locale = msg('zh-CN', 'en-US');
  const el = id => document.getElementById(id);
  const layers = {
    L0: ['clock', msg('限时与折扣', 'Promotions & discounts'), msg('留意活动截止日期和名额', 'Check deadlines and availability')],
    L1: ['repeat', msg('每日可领', 'Daily refresh'), msg('每天重置的额度与权益', 'Credits and perks that reset daily')],
    L2: ['infinity', msg('长期免费', 'Always free'), msg('常设免费档和注册权益', 'Standing free tiers and signup offers')],
    L3: ['stack', msg('其他权益', 'Other perks'), msg('邀请奖励、订阅加成和工具', 'Invites, subscription bonuses and tools')],
    L4: ['stack', msg('申请制权益', 'Application-based offers'), msg('需企业资质、项目审核或开源维护者资格', 'Startup, project review or open-source eligibility required')]
  };
  const expanded = new Set();
  const icon = key => '<svg class="ui-icon" aria-hidden="true"><use href="#tm-' + key + '"/></svg>';

  function groupRows(box) {
    const rows = Object.fromEntries(Object.keys(layers).map(key => [key, []]));
    for (const row of box.querySelectorAll(':scope > article[data-layer]')) {
      const next = row.nextElementSibling;
      rows[row.dataset.layer].push([row, next?.classList.contains('agg-detail') ? next : null]);
    }
    const batch = document.createDocumentFragment();
    for (const [key, [glyph, title, description]] of Object.entries(layers)) {
      if (!rows[key].length) continue;
      const heading = document.createElement('div');
      heading.className = 'layer-head ' + key;
      heading.innerHTML = icon(glyph) + '<h3>' + title + '</h3><p>' + description
        + '</p><span class="layer-count">' + msg(rows[key].length + ' 个平台', rows[key].length + ' platforms') + '</span>';
      batch.append(heading);
      for (const [row, detail] of rows[key]) {
        batch.append(row);
        if (detail) batch.append(detail);
      }
    }
    box.replaceChildren(batch);
  }

  const editorialHosts = new Set(['github.com', 'npmjs.com', 't.me', 'post.smzdm.com', 'aihot.news', 'mp.weixin.qq.com']);

  function logoHostname(value) {
    try {
      const url = new URL(value);
      if (url.protocol === 'https:' || url.protocol === 'http:') return url.hostname.replace(/^www\./, '');
    } catch (_) {
      // The local monogram covers entries without a provider website.
    }
    return '';
  }

  function providerLogo(name, url, variant, alternateUrl, alternateName) {
    const logos = window.LOGOS || {};
    const hostname = logoHostname(url);
    const alternateHost = logoHostname(alternateUrl);
    const hostLogo = host => {
      if (editorialHosts.has(host)) return '';
      const parts=host.split('.');
      while(parts.length>1) {
        const candidate=parts.join('.');
        if (editorialHosts.has(candidate)) return '';
        if (logos[candidate]) return logos[candidate];
        parts.shift();
      }
      return '';
    };
    const local = logos['provider:' + name] || logos['provider:' + alternateName]
      || hostLogo(hostname) || hostLogo(alternateHost);
    const path = typeof local === 'string' && /^assets\/logos\/[\w.-]+\.(?:png|svg|ico|webp)$/i.test(local) ? local : '';
    const initial = name.match(/[\p{L}\p{N}]/u)?.[0]?.toUpperCase() || '·';
    return '<span class="provider-icon provider-icon--' + variant + '" aria-hidden="true">'
      + (path ? '<img src="' + esc(path) + '" alt="" loading="lazy" decoding="async" onload="this.dataset.loaded=\'true\'" onerror="this.remove()">' : '')
      + '<span class="provider-initial" data-initial="' + esc(initial) + '"></span></span>';
  }

  function offerLogo(deal, site, name = deal.provider) {
    if (name === '初创额度') return providerLogo(name, '', 'row');
    return providerLogo(name, site?.url, 'row', deal.url, deal.provider);
  }

  function couponLink(deal) {
    if (deal.placeholder || !deal.url || (!deal.coupon && deal.type !== 'coupon')) return '';
    const code = deal.coupon;
    const label = code ? msg('🎁 券领', 'Coupon') : msg('🔗 折扣链接', 'Get offer');
    const title = code ? msg('查看折扣码与领取方式', 'View coupon and redemption options')
      : msg('打开折扣链接', 'Open discount link');
    const codeAttribute = code ? ' data-redeem-code="' + esc(code) + '"' : '';
    return `<a class="go cgo" href="${esc(safeUrl(deal.url))}" target="_blank" rel="noopener nofollow"${codeAttribute} title="${title}">${label}</a>`;
  }

  function sourceLinks(deal) {
    const explicit = Array.isArray(deal.sources) ? deal.sources : [];
    const links = new Map();
    for (const source of [...explicit, ...TokenMath.entries(deal).filter(q=>TokenMath.rates[q.unit]&&q.convert!==false).map(q=>({url:TokenMath.sources[q.unit],title:msg('折算价格依据','Conversion pricing basis')})), { url: deal.url, title: msg('条目入口', 'Offer page') }]) {
      try {
        const url = new URL(source.url);
        if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password) continue;
        if (!links.has(url.href)) links.set(url.href, source.title || url.hostname);
      } catch (_) { /* Keep the offer readable when an older link is malformed. */ }
    }
    if (!links.size) return '';
    return '<details class="source-links"><summary class="chip">'
      + msg('信源 ', 'Sources ') + links.size
      + '</summary><ul>' + Array.from(links, ([url, label]) =>
        '<li><a href="' + esc(url) + '" target="_blank" rel="noopener nofollow">' + esc(label) + '</a></li>'
      ).join('') + '</ul><p>' + esc(offerValue(deal)) + '</p>'
      + (TokenMath.estimateExplain(deal) ? '<p class="quota-explanation">' + esc(TokenMath.estimateExplain(deal)) + '</p>' : '')
      + (TokenMath.explain(deal) ? '<p class="quota-explanation">' + esc(TokenMath.explain(deal)) + '</p>' : '')
      + (offerNotes(deal) ? '<p>' + esc(offerNotes(deal)) + '</p>' : '') + '</details>';
  }

  function cleanCopy(value) {
    return String(value || '').replace(/\*\*|`/g, '').replace(/\s+/g, ' ').trim();
  }

  function offerValue(deal) {
    return cleanCopy(zh ? deal.value : deal.value_en || deal.value);
  }

  function shortCopy(value, limit) {
    const text = cleanCopy(value).replace(/^【[^】]+】\s*/, '');
    const parts = text.split(/[；;。]|\s+\|\s+|\s+——\s*/);
    const lead = parts[0].trim();
    if (!lead) return '';
    if (Array.from(lead).length <= limit) return lead;
    const clipped = Array.from(lead).slice(0, limit).join('');
    const wordEnd = clipped.lastIndexOf(' ');
    return (wordEnd > limit * .7 ? clipped.slice(0, wordEnd) : clipped).trimEnd() + '…';
  }

  function headline(deal) {
    return shortCopy(offerValue(deal), msg(67, 108));
  }

  function summary(deal) {
    const rule = zh ? deal.rule : deal.rule_en || deal.rule;
    const notes = zh ? deal.notes : deal.notes_en || deal.notes;
    const editorial = zh ? deal.summary : deal.summary_en;
    return shortCopy(editorial || rule || (notes && !/^(TODO|⚠️)/.test(notes) ? notes : ''), msg(48, 90));
  }

  function groupSummary(best, deals) {
    const lead = summary(best);
    return lead || deals.filter(deal => deal !== best).slice(0, 2)
      .map(deal => shortCopy(offerValue(deal), msg(21, 34))).filter(Boolean).join(' · ');
  }

  function offerNotes(d) {
    const rule = zh ? d.rule : d.rule_en || d.rule;
    const notes = zh ? d.notes : d.notes_en || d.notes;
    return [
      rule && msg('规则：', 'Rules: ') + cleanCopy(rule),
      notes && !/^(TODO|⚠️)/.test(notes) && msg('备注：', 'Notes: ') + cleanCopy(notes),
    ].filter(Boolean).join(' · ');
  }

  function gateLabel(deal) {
    const labels = {
      verify: msg('需实名', 'ID verification'),
      card: msg('需验卡', 'Card verification'),
      student: msg('学生认证', 'Student verification'),
      startup: msg('初创资质', 'Startup eligibility'),
      audit: msg('需审核', 'Application review'),
      oss: msg('开源维护者', 'Open-source maintainers'),
      subscription: msg('需订阅', 'Subscription required'),
    };
    return labels[deal.gate] || deal.gate_label || deal.gate;
  }

  function requiresApplication(deal) {
    return ['startup', 'audit', 'oss'].includes(deal.gate);
  }

  const beijingDay = now => new Date(now.getTime()+8*3600e3).toISOString().slice(0,10);
  function isFeatured(deal, now = new Date()) {
    const date = beijingDay(now);
    const offer = deal.subscription_offer;
    const range = offer?.usage_multiplier;
    const hasUsage = offer?.monthly_usage_limit > 0
      || (Array.isArray(range) && range.length === 2 && range.every(n=>Number.isFinite(n)&&n>0) && range[1]>=range[0]);
    return deal.published !== false && deal.verify_status === 'verified'
      && deal.type === 'pricing_plan' && deal.quota_paid === true
      && /^\d{4}-\d{2}-\d{2}$/.test(deal.featured_until || '') && deal.featured_until >= date
      && TokenMath.phase(deal, now) !== 'expired' && TokenMath.phase(deal, now) !== 'upcoming'
      && offer?.currency === 'USD' && offer.price > 0 && hasUsage
      && (!offer.limit_until || (/^\d{4}-\d{2}-\d{2}$/.test(offer.limit_until) && offer.limit_until >= date));
  }

  function featuredDeals(deals, now = new Date()) {
    const seen = new Set();
    return deals.filter(d=>isFeatured(d,now)).sort((a,b)=>(a.featured_rank||99)-(b.featured_rank||99))
      .filter(d=>{const key=d.group||d.provider;if(seen.has(key))return false;seen.add(key);return true;}).slice(0,3);
  }

  function pinnedInvites(deals) {
    const invites = deals.filter(deal => deal.published !== false && deal.pinned_invite_rank > 0
      && deal.type === 'coupon' && deal.via === 'invite' && !deal.placeholder && deal.url
      && TokenMath.phase(deal) === 'active')
      .sort((a,b) => a.pinned_invite_rank - b.pinned_invite_rank);
    if (!invites.length) return '';
    return '<section class="pinned-invites" aria-labelledby="pinnedInviteTitle">'
      +'<div class="layer-head featured-heading">'+icon('bookmark')
      +'<h3 id="pinnedInviteTitle">'+msg('置顶邀请','Pinned invites')+'</h3></div>'
      +invites.map(deal => `<div class="pinned-invite">
        <div class="pinned-invite-text">
          <b>${esc(deal.provider)}</b>
          <span class="chip">${msg('邀请码 ','Code ')}${esc(deal.invite_code)}</span>
          <p>${esc(summary(deal))}</p>
        </div>
        <div class="r-ops"><a class="go cgo" href="${esc(safeUrl(deal.url))}" target="_blank" rel="noopener nofollow sponsored"
          aria-label="${esc(msg('打开 '+deal.provider+' 邀请链接','Open '+deal.provider+' invite link'))}">${msg('邀请链接','Invite link')}</a></div>
      </div>`).join('')+'</section>';
  }

  function featuredHeading(count) {
    return '<div class="layer-head featured-heading">'+icon('bookmark')+'<h3>'
      +msg('补贴推荐 · 付费', 'Featured subsidy · paid')+'</h3><p>'
      +msg('精选补贴套餐，需付费订阅', 'Selected subsidized plans; subscription required')+'</p>'
      +'<span class="layer-count">'+esc(count)+msg(' 个推荐',' picks')+'</span></div>';
  }

  function subscriptionCell(deal) {
    if (!isFeatured(deal)) return '';
    const offer = deal.subscription_offer;
    const price = offer.intro_price || offer.price;
    const usage = offer.monthly_usage_limit > 0
      ? '$'+offer.monthly_usage_limit.toLocaleString(locale)+msg(' 月用量上限',' monthly usage cap')
      : msg('官方 ', 'Official ')+offer.usage_multiplier.join('–')+msg(' 倍用量','× usage');
    return '<span class="quota-value"><span class="num">$'+esc(price)
      +msg(offer.intro_price?' 首月':'/月',offer.intro_price?' first mo':'/mo')+'</span>'
      +(offer.intro_price?'<span class="unit">'+msg('续费 $','Then $')+esc(offer.price)+msg('/月','/mo')+'</span>':'')
      +'<span class="unit">'+esc(offer.model)+'</span><span class="unit quota-native">'+esc(usage)+'</span></span>';
  }
  let featuredDay = beijingDay(new Date());
  setInterval(() => {
    const next = beijingDay(new Date());
    if (next === featuredDay) return;
    featuredDay = next;
    if (document.querySelector('.featured-offer') && typeof window.render === 'function') window.render();
  },60000);

  function timing(d) {
    const formatInstant = value => new Intl.DateTimeFormat(locale,{timeZone:'Asia/Shanghai',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hour12:false}).format(new Date(value))+msg(' 北京时间',' GMT+8');
    if (TokenMath.phase(d) === 'upcoming') return '<span class="offer-timing" title="'+esc(d.starts_at)+'">'+esc(formatInstant(d.starts_at))+msg(' 开始',' starts')+'</span>';
    if (isFeatured(d)) return d.subscription_offer.limit_until
      ? '<span class="offer-deadline">'+msg('提额至 ', 'Boost until ')+esc(d.subscription_offer.limit_until)+'</span>'
      : '<span class="offer-timing">'+msg('月度订阅','Monthly subscription')+'</span>';
    if (d.deadline && !String(d.deadline).startsWith('长期')) {
      const date = String(d.deadline);
      return '<span class="offer-deadline" title="' + esc(date) + '">'
        + esc(/^\d{4}-\d{2}-\d{2}T/.test(date) && Number.isFinite(Date.parse(date)) ? formatInstant(date) : date) + '</span>';
    }
    const label = d.cadence === 'monthly' ? msg('每月刷新', 'Monthly reset')
      : d.cadence === 'daily' ? msg('每日额度', 'Daily allowance')
      : (d.deadline || d.type === 'free_tier' || d.via === 'free') ? msg('长期', 'Ongoing') : '';
    return label ? '<span class="offer-timing">' + label + '</span>' : '';
  }

  function freshness(d) {
    const date = Date.parse(d.verified_at);
    const title = Number.isFinite(date) ? new Date(date).toLocaleDateString(locale) : '';
    const days = Math.max(0, Math.floor((Date.now() - date) / 864e5));
    const badge = (tone, text) => '<span class="badge ' + tone + '" title="' + esc(title) + '">' + text + '</span>';
    if (TokenMath.phase(d) === 'expired') return badge('b-red', msg('已失效', 'Expired'));
    if (d.verify_status !== 'verified' || !Number.isFinite(date)) return badge('b-amber', msg('待复核', 'Needs review'));
    if (d.quota_basis === 'claimed_pack') return badge('b-green', msg('已领实测', 'Claim tested'));
    if (days === 0) return badge('b-green', d.verify_by === 'auto' ? msg('自动核验', 'Auto-checked') : msg('近 24 小时核验', 'Verified in 24h'));
    return badge(days < 7 ? 'b-green' : 'b-amber', msg(days + ' 天前', days + (days === 1 ? ' day ago' : ' days ago')));
  }

  function claimLabel(deal) {
    if (deal.type === 'paid_discount') return requiresApplication(deal) ? msg('查看申请', 'View application') : msg('查看价格', 'View pricing');
    if (deal.claim_status !== 'window_unconfirmed') return '';
    return TokenMath.phase(deal) === 'expired' ? msg('查看历史', 'View history') : msg('查看入口', 'View entry');
  }

  function claimNotice(deal) {
    if (deal.claim_status !== 'window_unconfirmed' || TokenMath.phase(deal) === 'expired') return '';
    return '<span class="badge b-amber">' + msg('新领取待核', 'New claims unconfirmed') + '</span>';
  }

  // Recompute only when a timed offer changes phase; a tab opened before 19:00
  // must not keep its upcoming state after the activity starts.
  let timedSignature = null;
  function refreshTimedOffers() {
    if (typeof DEALS === 'undefined' || !DEALS.length) return;
    const localDay = new Date(Date.now()+8*3600000).toISOString().slice(0,10);
    const next = localDay+'|'+DEALS.filter(d=>d.starts_at || /^\d{4}-\d{2}-\d{2}T/.test(d.deadline || '')).map(d=>d.id+':'+TokenMath.phase(d)).join('|');
    if (next === timedSignature) return;
    const initialized = timedSignature !== null;
    timedSignature = next;
    if (!initialized) return;
    if (typeof window.render === 'function') window.render();
    if (typeof window.calcGlobalBanner === 'function') window.calcGlobalBanner();
    if (typeof window.refreshWorkbenchNews === 'function') window.refreshWorkbenchNews();
    if (typeof window.sumRender === 'function' && el('sumPanel')?.classList.contains('open')) window.sumRender();
    if (typeof DailyEstimateUI !== 'undefined') DailyEstimateUI.refresh();
  }
  setInterval(refreshTimedOffers,1000);
  document.addEventListener('visibilitychange',()=>{if(!document.hidden)refreshTimedOffers();});

  function matches(deal, query) {
    const terms = query.toLowerCase().split(/\s+/);
    const corpora = [deal.provider, deal.group, deal.value, deal.rule, deal.notes, deal.id,
      deal.value_en, deal.rule_en, deal.notes_en,
      deal.url, ...(Array.isArray(deal.sources) ? deal.sources.flatMap(s => [s?.title, s?.url]) : [])
    ].filter(Boolean).join(' ').toLowerCase();
    return terms.every(term => corpora.includes(term));
  }

  const groupLabel = (open, count) => open ? msg('收起信源', 'Hide sources')
    : msg('展开 ' + count + ' 条', 'View ' + count + ' offers');

  function toggleGroup(button) {
    const detail = button.closest('article').nextElementSibling;
    if (!detail?.classList.contains('agg-detail')) return;
    const open = detail.classList.toggle('open');
    if (open) expanded.add(button.dataset.agg);
    else expanded.delete(button.dataset.agg);
    button.setAttribute('aria-expanded', String(open));
    button.textContent = groupLabel(open, button.dataset.count);
  }

  function updateFilters(cat, sort, count) {
    el('cards').setAttribute('aria-busy', 'false');
    el('resultCount').textContent = msg(count + ' 条情报', count + (count === 1 ? ' offer' : ' offers'));
    el('tabs').querySelectorAll('button[data-cat]').forEach(button => {
      const active = button.dataset.cat === cat;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    el('listhead').querySelectorAll('button[data-sort]').forEach(button => {
      const active = button.dataset.sort === sort;
      const label = button.dataset.sort === 'tokens' ? msg('额度/估算', 'Credits/est.') : msg('核验', 'Verification');
      button.classList.toggle('on', active);
      button.setAttribute('aria-pressed', String(active));
      button.textContent = label + (active ? ' ↓' : ' ↕');
    });
  }

  const ticker = el('newsTicker');
  const newsItems = el('ntkItems');
  const newsViewport = ticker.querySelector('.ntk-scroll');
  const newsToggle = ticker.querySelector('[data-news-toggle]');
  const newsSteps = ticker.querySelectorAll('[data-news-step]');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const newsInterval = 6000;
  let news = [], newsIndex = 0, newsTimer;
  let userRotation = null, newsHovered = false;

  function showNews(animate = false) {
    const item = news[newsIndex];
    if (item) {
      const line = document.createElement('span');
      line.className = animate ? 'ntk-item ntk-enter' : 'ntk-item';
      const title = document.createElement('b');
      title.textContent = item.title;
      line.append(title, ' · ' + item.text);
      line.title = item.title + ' · ' + item.text;
      newsItems.replaceChildren(line);
    } else {
      newsItems.textContent = msg('暂无更新', 'No updates yet');
    }
  }

  function rotationEnabled() {
    return userRotation ?? !reducedMotion.matches;
  }

  function scheduleNews(focused = ticker.contains(document.activeElement)) {
    clearTimeout(newsTimer);
    const enabled = newsToggle && rotationEnabled();
    const canRotate = enabled && news.length > 1 && !newsHovered && !focused && !document.hidden;
    if (newsToggle) {
      const label = enabled ? msg('暂停动态轮播', 'Pause news rotation') : msg('播放动态轮播', 'Play news rotation');
      newsToggle.dataset.playing = String(enabled);
      newsToggle.setAttribute('aria-label', label);
      newsToggle.title = label;
    }
    newsViewport.setAttribute('aria-live', canRotate ? 'off' : 'polite');
    if (canRotate) {
      newsTimer = setTimeout(() => {
        stepNews(1);
        scheduleNews();
      }, newsInterval);
    }
  }

  function stepNews(step) {
    newsIndex = (newsIndex + step + news.length) % news.length;
    showNews(true);
  }

  function setNews(items) {
    const current = news[newsIndex];
    const index = items.findIndex(item => item.title === current?.title && item.text === current?.text);
    news = items;
    newsIndex = Math.max(0, index);
    if (newsToggle) newsToggle.disabled = news.length < 2;
    newsSteps.forEach(button => button.disabled = news.length < 2);
    scheduleNews();
    if (index === -1) showNews();
  }
  function refreshNews(deals, production) {
    const fallback = deals.filter(d => d.published !== false && TokenMath.phase(d) !== 'expired' && d.category !== 'intel_source')
      .sort((a, b) => new Date(b.verified_at) - new Date(a.verified_at)).slice(0, 6)
      .map(d => ({title:d.provider, text:zh ? d.value : d.value_en || d.value}));
    setNews(fallback);
    if (production) fetch('/api/news?lang=' + msg('zh','en')).then(r => r.ok ? r.json() : null).then(payload => {
      if (Array.isArray(payload?.items) && payload.items.length) {
        setNews(payload.items.slice(0, 12).map(n => ({title:n.source || msg('资讯','News'), text:n.title || ''})));
      }
    }).catch(() => {});
  }
  ticker.addEventListener('click', event => {
    if (event.target.closest('[data-news-toggle]')) {
      userRotation = !rotationEnabled();
      scheduleNews();
      return;
    }
    const button = event.target.closest('[data-news-step]');
    if (!button || news.length < 2) return;
    stepNews(Number(button.dataset.newsStep));
    scheduleNews();
  });
  ticker.addEventListener('pointerenter', event => {
    if (event.pointerType === 'touch') return;
    newsHovered = true;
    scheduleNews();
  });
  ticker.addEventListener('pointerleave', event => {
    if (event.pointerType === 'touch') return;
    newsHovered = false;
    scheduleNews();
  });
  ticker.addEventListener('focusin', () => scheduleNews(true));
  ticker.addEventListener('focusout', event => scheduleNews(ticker.contains(event.relatedTarget)));
  document.addEventListener('visibilitychange', () => scheduleNews());
  reducedMotion.addEventListener('change', () => scheduleNews());
  document.addEventListener('keydown', event => {
    if (event.key !== '/' || event.metaKey || event.altKey || event.ctrlKey || event.defaultPrevented
      || event.target.closest('input, textarea, select, [contenteditable]') || document.querySelector('[role="dialog"].open,#vault.open')) return;
    event.preventDefault();
    el('search').focus();
  });

  return {msg, locale, groupRows, providerLogo, offerLogo, couponLink, sourceLinks, offerNotes, offerValue, headline, summary, groupSummary, gateLabel, requiresApplication, isFeatured, featuredDeals, pinnedInvites, featuredHeading, subscriptionCell, timing, freshness, claimLabel, claimNotice, matches, expanded, groupLabel, toggleGroup, updateFilters, refreshNews};
})();
