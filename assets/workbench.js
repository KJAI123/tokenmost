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
    L3: ['stack', msg('其他权益', 'Other perks'), msg('邀请奖励、订阅加成和工具', 'Invites, subscription bonuses and tools')]
  };
  const expanded = new Set();
  const icon = key => '<svg class="ui-icon" aria-hidden="true"><use href="#tm-' + key + '"/></svg>';

  function groupRows(box) {
    const rows = Object.fromEntries(Object.keys(layers).map(key => [key, []]));
    const more = el('moreWrap');
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
    if (more) batch.append(more);
    box.replaceChildren(batch);
  }

  function sourceLinks(deal) {
    const explicit = Array.isArray(deal.sources) ? deal.sources : [];
    const links = new Map();
    for (const source of [...explicit, { url: deal.url, title: msg('条目入口', 'Offer page') }]) {
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
      ).join('') + '</ul>' + (offerNotes(deal) ? '<p>' + esc(offerNotes(deal)) + '</p>' : '') + '</details>';
  }

  function offerNotes(d) {
    const rule = zh ? d.rule : d.rule_en || d.rule;
    const notes = zh ? d.notes : d.notes_en || d.notes;
    return [
      rule && msg('规则：', 'Rules: ') + rule,
      notes && !/^(TODO|⚠️)/.test(notes) && msg('备注：', 'Notes: ') + notes,
    ].filter(Boolean).join(' · ');
  }

  function timing(d) {
    if (d.deadline && !String(d.deadline).startsWith('长期')) {
      const date = String(d.deadline);
      return '<span class="offer-deadline" title="' + esc(date) + '">'
        + esc(/^\d{4}-\d{2}-\d{2}T/.test(date) ? date.slice(0, 10) : date) + '</span>';
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
    if (d.verify_status === 'expired') return badge('b-red', msg('已失效', 'Expired'));
    if (d.verify_status !== 'verified' || !Number.isFinite(date)) return badge('b-amber', msg('待复核', 'Needs review'));
    if (days === 0) return badge('b-green', d.verify_by === 'auto' ? msg('自动核验', 'Auto-checked') : msg('近 24 小时核验', 'Verified in 24h'));
    return badge(days < 7 ? 'b-green' : 'b-amber', msg(days + ' 天前', days + (days === 1 ? ' day ago' : ' days ago')));
  }

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
      const label = button.dataset.sort === 'tokens' ? msg('额度', 'Credits') : msg('核验', 'Verification');
      button.classList.toggle('on', active);
      button.setAttribute('aria-pressed', String(active));
      button.textContent = label + (active ? ' ↓' : ' ↕');
    });
  }

  let news = [], newsIndex = 0;
  function showNews() {
    const item = news[newsIndex];
    const node = el('ntkItems');
    node.replaceChildren();
    if (item) {
      const line = document.createElement('span');
      line.className = 'ntk-item';
      const title = document.createElement('b');
      title.textContent = item.title;
      line.append(title, ' · ' + item.text);
      line.title = item.title + ' · ' + item.text;
      node.append(line);
    } else {
      node.textContent = msg('暂无更新', 'No updates yet');
    }
    el('newsTicker').querySelectorAll('[data-news-step]').forEach(b => b.disabled = news.length < 2);
  }
  function setNews(items) { news = items; newsIndex = 0; showNews(); }
  function refreshNews(deals, production) {
    const fallback = deals.filter(d => d.published !== false && d.verify_status !== 'expired' && d.category !== 'intel_source')
      .sort((a, b) => new Date(b.verified_at) - new Date(a.verified_at)).slice(0, 6)
      .map(d => ({title:d.provider, text:zh ? d.value : d.value_en || d.value}));
    setNews(fallback);
    if (production) fetch('/api/news?lang=' + msg('zh','en')).then(r => r.ok ? r.json() : null).then(payload => {
      if (Array.isArray(payload?.items) && payload.items.length) {
        setNews(payload.items.slice(0, 12).map(n => ({title:n.source || msg('资讯','News'), text:n.title || ''})));
      }
    }).catch(() => {});
  }
  el('newsTicker').addEventListener('click', event => {
    const button = event.target.closest('[data-news-step]');
    if (!button || news.length < 2) return;
    newsIndex = (newsIndex + Number(button.dataset.newsStep) + news.length) % news.length;
    showNews();
  });
  document.addEventListener('keydown', event => {
    if (event.key !== '/' || event.metaKey || event.altKey || event.ctrlKey || event.defaultPrevented
      || event.target.closest('input, textarea, select, [contenteditable]') || document.querySelector('[role="dialog"].open,#vault.open')) return;
    event.preventDefault();
    el('search').focus();
  });

  return {msg, locale, groupRows, sourceLinks, offerNotes, timing, freshness, matches, expanded, groupLabel, toggleGroup, updateFilters, refreshNews};
})();
