(() => {
  const surface = document.body.dataset.surface || 'home';
  function measure(event) {
    if (navigator.webdriver || new URLSearchParams(location.search).has('__qa') || navigator.doNotTrack === '1' || navigator.globalPrivacyControl || location.hostname !== 'tokenmost.com') return;
    fetch('/assets/interaction.txt?event='+event+'&surface='+encodeURIComponent(surface),
      {method:'HEAD',keepalive:true,credentials:'omit',referrerPolicy:'no-referrer',cache:'no-store'}).catch(()=>{});
  }
  document.addEventListener('click', e => {
    const link = e.target.closest('a');
    if (link?.matches('[data-claim],a.go,a.coupon-link')) {
      if (link.origin !== location.origin && /^https?:$/.test(link.protocol)) measure('claim');
    } else if (link && /\/(verified|rss)\.xml$/.test(link.pathname)) measure('rss');
  });
  const button = document.querySelector('[data-share-page]');
  if (!button) return;
  button.hidden = false;
  button.addEventListener('click',async () => {
    const url = new URL(document.querySelector('link[rel=canonical]').href);
    url.searchParams.set('utm_source','share');
    if (location.hash.startsWith('#deal-')) url.hash=location.hash;
    try {
      if (navigator.share) await navigator.share({title:document.title,url:url.href});
      else {
        await navigator.clipboard.writeText(url.href);
        document.querySelector('[data-share-status]').textContent='链接已复制';
      }
      measure('share');
    } catch (error) {
      if (error.name !== 'AbortError') window.prompt('复制分享链接',url.href);
    }
  });
})();
