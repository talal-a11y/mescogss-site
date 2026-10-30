/* MESCO GSS — interactions. Vanilla JS, no framework. */
(() => {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const root = document.documentElement;

  /* ---------- page veil ----------
     Leaving: two panels sweep up (red, then navy) and the mark fades in; we navigate under cover.
     Arriving: the <head> script already stamped html.veil-cover, so the new page paints *under* the
     veil from its first frame. Once fonts and the hero image are ready, the panels sweep up and away
     while the hero reveals underneath. No white flash, no half-rendered frame. */
  const veil = $('.veil');
  const panels = $$('.veil__panel');
  const mark = $('.veil__mark');
  const arriving = root.classList.contains('veil-cover');
  try { sessionStorage.removeItem('mgss-veil'); } catch (e) {}

  const OUT_MS = 900;
  function veilOut() {
    if (!veil) return;
    if (reduce) { root.classList.remove('veil-cover'); return; }
    veil.classList.add('is-active');
    if (mark) { mark.style.transition = 'opacity .25s ease, transform .4s cubic-bezier(.22,1,.36,1)'; mark.style.opacity = '0'; mark.style.transform = 'scale(1.1)'; }
    panels.forEach((p, i) => {
      p.style.transition = `transform ${OUT_MS}ms cubic-bezier(.76,0,.24,1) ${i === 0 ? 120 : 0}ms`;
      p.style.transform = 'translateY(-100%)';
    });
    setTimeout(() => {
      root.classList.remove('veil-cover');
      veil.classList.remove('is-active');
      panels.forEach((p) => { p.style.transition = 'none'; p.style.transform = ''; });
      if (mark) { mark.style.transition = 'none'; mark.style.opacity = ''; mark.style.transform = ''; }
      requestAnimationFrame(() => panels.forEach((p) => { p.style.transition = ''; }));
    }, OUT_MS + 160);
  }

  const IN_MS = 640;
  function veilIn(href) {
    if (!veil || reduce) { location.href = href; return; }
    veil.classList.add('is-active');
    panels.forEach((p, i) => {
      p.style.transition = `transform ${IN_MS}ms cubic-bezier(.76,0,.24,1) ${i === 0 ? 0 : 90}ms`;
      p.style.transform = 'translateY(0)';
    });
    if (mark) { mark.style.transition = 'opacity .3s ease .42s, transform .5s cubic-bezier(.22,1,.36,1) .42s'; mark.style.opacity = '1'; mark.style.transform = 'none'; }
    try { sessionStorage.setItem('mgss-veil', '1'); } catch (e) {}
    setTimeout(() => { location.href = href; }, IN_MS + 140);
  }

  function internal(a) {
    const href = a.getAttribute('href');
    if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:') || a.target === '_blank' || a.hasAttribute('download')) return null;
    const url = new URL(a.href, location.href);
    if (url.origin !== location.origin) return null;
    if (url.pathname === location.pathname) return null;
    return url;
  }

  document.addEventListener('click', (e) => {
    const a = e.target.closest('a');
    if (!a || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
    const url = internal(a);
    if (!url) return;
    e.preventDefault();
    document.body.classList.remove('menu-open');
    root.style.overflow = '';
    veilIn(url.href);
  });

  // warm the next page while the pointer is still on the link
  const prefetched = new Set();
  document.addEventListener('pointerover', (e) => {
    const a = e.target.closest && e.target.closest('a');
    if (!a) return;
    const url = internal(a);
    if (!url || prefetched.has(url.href)) return;
    prefetched.add(url.href);
    const l = document.createElement('link'); l.rel = 'prefetch'; l.href = url.href; l.as = 'document'; document.head.appendChild(l);
  }, { passive: true });

  window.addEventListener('pageshow', (e) => {
    if (e.persisted) { root.classList.remove('veil-cover'); veil && veil.classList.remove('is-active'); panels.forEach((p) => { p.style.transform = ''; }); }
  });

  /* ---------- header state ---------- */
  const header = $('.site-header');
  if ($('.profile')) document.body.classList.add('has-profile');
  const onScroll = () => header && header.classList.toggle('is-solid', window.scrollY > 40);
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  const burger = $('.burger');
  if (burger) {
    burger.addEventListener('click', () => {
      const open = document.body.classList.toggle('menu-open');
      burger.setAttribute('aria-expanded', String(open));
      root.style.overflow = open ? 'hidden' : '';
    });
  }

  /* ---------- hero intro ---------- */
  function splitLines(el) {
    const words = el.textContent.trim().split(/\s+/);
    el.textContent = '';
    const probe = document.createElement('span');
    el.appendChild(probe);
    const lines = []; let current = []; let lastH = null;
    words.forEach((w) => {
      probe.textContent = current.concat(w).join(' ');
      const h = probe.getBoundingClientRect().height;
      if (lastH !== null && h > lastH && current.length) { lines.push(current.join(' ')); current = [w]; probe.textContent = w; lastH = probe.getBoundingClientRect().height; }
      else { current.push(w); lastH = h; }
    });
    if (current.length) lines.push(current.join(' '));
    el.textContent = '';
    lines.forEach((l) => { const d = document.createElement('span'); d.className = 'line'; const s = document.createElement('span'); s.textContent = l; d.appendChild(s); el.appendChild(d); });
    return $$('.line > span', el);
  }

  function introHero(delay) {
    const title = $('.hero__title') || $('.page-head h1');
    const media = $('.hero__media img') || $('.page-head__media img');
    const cue = $('.hero__diamonds path');
    if (title) {
      const spans = splitLines(title);
      spans.forEach((s, i) => {
        if (reduce) { s.style.transform = 'none'; return; }
        s.style.transition = 'transform 1.1s cubic-bezier(.22,1,.36,1)';
        setTimeout(() => { s.style.transform = 'translateY(0)'; }, delay + i * 110);
      });
    }
    if (media && !reduce) { media.style.transition = 'transform 2.6s cubic-bezier(.22,1,.36,1)'; setTimeout(() => { media.style.transform = 'scale(1)'; }, Math.max(0, delay - 150)); }
    if (cue && !reduce) { cue.style.transition = 'stroke-dashoffset 3.2s cubic-bezier(.22,1,.36,1)'; setTimeout(() => { cue.style.strokeDashoffset = '0'; }, delay + 300); }
    $$('.hero [data-reveal], .page-head [data-reveal], .profile [data-reveal]').forEach((el, i) => setTimeout(() => el.classList.add('is-in'), delay + 350 + i * 120));
  }

  /* ---------- scroll reveals ---------- */
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      en.target.classList.add('is-in');
      if (en.target.dataset.maskHost) $$('.mask-img', en.target).forEach((m) => m.classList.add('is-in'));
      if (en.target.hasAttribute('data-count')) countUp(en.target);
      io.unobserve(en.target);
    });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.06 });
  $$('[data-reveal]:not(.hero [data-reveal]):not(.page-head [data-reveal]):not(.profile [data-reveal]), .stagger, [data-count]').forEach((el) => io.observe(el));
  $$('.mask-img').forEach((m) => { const host = m.parentElement; host.dataset.maskHost = '1'; io.observe(host); });

  function countUp(el) {
    const target = parseFloat(el.getAttribute('data-count'));
    if (reduce || isNaN(target)) { el.textContent = el.getAttribute('data-count'); return; }
    const dur = 1400, start = performance.now();
    const step = (now) => { const p = Math.min(1, (now - start) / dur), e = 1 - Math.pow(1 - p, 3); el.textContent = Math.round(target * e); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  }

  /* ---------- parallax on media ---------- */
  if (!reduce) {
    const px = $$('[data-parallax]');
    const tick = () => {
      px.forEach((el) => {
        const r = el.getBoundingClientRect();
        if (r.bottom < 0 || r.top > innerHeight) return;
        const prog = (r.top + r.height / 2 - innerHeight / 2) / innerHeight;
        const img = el.querySelector('img');
        if (img) img.style.translate = `0 ${(-prog * 40).toFixed(1)}px`;
      });
    };
    window.addEventListener('scroll', tick, { passive: true }); tick();
  }

  /* ---------- team strip: drag + arrows ---------- */
  const strip = $('.strip');
  if (strip) {
    let down = false, startX = 0, startL = 0, moved = false;
    strip.addEventListener('pointerdown', (e) => { down = true; moved = false; startX = e.clientX; startL = strip.scrollLeft; strip.classList.add('is-dragging'); });
    window.addEventListener('pointermove', (e) => { if (!down) return; const dx = e.clientX - startX; if (Math.abs(dx) > 4) moved = true; strip.scrollLeft = startL - dx; });
    window.addEventListener('pointerup', () => { down = false; strip.classList.remove('is-dragging'); });
    strip.addEventListener('click', (e) => { if (moved) { e.preventDefault(); e.stopPropagation(); } }, true);
    const card = $('.person', strip);
    const stepW = () => (card ? card.getBoundingClientRect().width + 24 : 320);
    $('.team-nav [data-dir="prev"]')?.addEventListener('click', () => strip.scrollBy({ left: -stepW(), behavior: 'smooth' }));
    $('.team-nav [data-dir="next"]')?.addEventListener('click', () => strip.scrollBy({ left: stepW(), behavior: 'smooth' }));
  }

  /* ---------- inline video ---------- */
  const vf = $('.video__frame');
  if (vf) {
    const v = $('video', vf), btn = $('.video__play', vf);
    btn.addEventListener('click', () => { vf.classList.add('is-playing'); v.play(); });
    v.addEventListener('ended', () => { vf.classList.remove('is-playing'); v.currentTime = 0; });
  }

  /* ---------- forms (static site: open the visitor's mail client) ---------- */
  const form = $('#contact-form');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const d = new FormData(form);
      const subject = encodeURIComponent('Website enquiry from ' + (d.get('name') || ''));
      const body = encodeURIComponent(`Name: ${d.get('name')}\nEmail: ${d.get('email')}\n\n${d.get('message') || ''}`);
      location.href = `mailto:info@mescogss.com?subject=${subject}&body=${body}`;
    });
  }
  const sub = $('#subscribe-form');
  if (sub) {
    sub.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = encodeURIComponent(new FormData(sub).get('email') || '');
      location.href = `mailto:info@mescogss.com?subject=Subscribe&body=Please subscribe ${email}`;
    });
  }

  /* ---------- boot ---------- */
  function ready() {
    // wait for fonts + the hero image so the reveal happens on a finished frame
    const hero = $('.hero__media img') || $('.page-head__media img') || $('.profile__media img');
    const waits = [document.fonts ? document.fonts.ready : Promise.resolve()];
    if (hero && !hero.complete) waits.push(new Promise((r) => { hero.addEventListener('load', r, { once: true }); hero.addEventListener('error', r, { once: true }); }));
    const timeout = new Promise((r) => setTimeout(r, 1200));
    return Promise.race([Promise.all(waits), timeout]);
  }
  ready().then(() => {
    if (arriving) { veilOut(); introHero(260); }
    else introHero(200);
  });
})();
