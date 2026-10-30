/* MESCO GSS — interactions. Vanilla JS, no framework. */
(() => {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  /* ---------- page veil: in on load, out on internal navigation ---------- */
  const veil = $('.veil');
  const cameFromInside = sessionStorage.getItem('mgss-veil') === '1';
  sessionStorage.removeItem('mgss-veil');

  function veilOut() {
    if (!veil || reduce) return;
    veil.classList.add('is-in', 'is-active');
    veil.style.transition = 'none';
    veil.style.transform = 'none';
    requestAnimationFrame(() => requestAnimationFrame(() => {
      veil.style.transition = 'transform .9s cubic-bezier(.76,0,.24,1)';
      veil.style.transform = 'translateY(-100%)';
      setTimeout(() => { veil.classList.remove('is-in', 'is-active'); veil.style.transition = ''; veil.style.transform = ''; }, 950);
    }));
  }

  function veilIn(href) {
    if (!veil || reduce) { location.href = href; return; }
    const mark = $('.veil__mark');
    veil.classList.add('is-active');
    veil.style.transition = 'transform .7s cubic-bezier(.76,0,.24,1)';
    veil.style.transform = 'translateY(0)';
    if (mark) { mark.style.transition = 'opacity .3s .35s'; mark.style.opacity = '1'; }
    sessionStorage.setItem('mgss-veil', '1');
    setTimeout(() => { location.href = href; }, 720);
  }

  document.addEventListener('click', (e) => {
    const a = e.target.closest('a');
    if (!a) return;
    const href = a.getAttribute('href');
    if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:') || a.target === '_blank' || a.hasAttribute('download')) return;
    const url = new URL(a.href, location.href);
    if (url.origin !== location.origin) return;
    if (url.pathname === location.pathname && url.hash) return;
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    e.preventDefault();
    document.body.classList.remove('menu-open');
    veilIn(url.href);
  });

  window.addEventListener('pageshow', (e) => { if (e.persisted) { veil && veil.classList.remove('is-active', 'is-in'); } });

  /* ---------- header state ---------- */
  const header = $('.site-header');
  const onScroll = () => header && header.classList.toggle('is-solid', window.scrollY > 40);
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  // services panel (desktop)
  const panelItem = $('.nav__item--has-panel');
  if (panelItem && header) {
    let t;
    panelItem.addEventListener('mouseenter', () => { clearTimeout(t); header.classList.add('is-open'); });
    panelItem.addEventListener('mouseleave', () => { t = setTimeout(() => header.classList.remove('is-open'), 180); });
    panelItem.querySelector('.nav__link').addEventListener('focus', () => header.classList.add('is-open'));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') header.classList.remove('is-open'); });
  }

  // mobile menu
  const burger = $('.burger');
  if (burger) {
    burger.addEventListener('click', () => {
      const open = document.body.classList.toggle('menu-open');
      burger.setAttribute('aria-expanded', String(open));
      document.documentElement.style.overflow = open ? 'hidden' : '';
    });
  }

  /* ---------- hero intro ---------- */
  function splitLines(el) {
    // Wrap each visual line in a mask so lines can rise independently.
    const text = el.textContent.trim();
    const words = text.split(/\s+/);
    el.textContent = '';
    const probe = document.createElement('span');
    probe.style.cssText = 'display:inline';
    el.appendChild(probe);
    const lines = []; let current = [];
    let lastTop = null;
    words.forEach((w) => {
      probe.textContent = (current.concat(w)).join(' ');
      const top = probe.getBoundingClientRect().height;
      if (lastTop !== null && top > lastTop && current.length) { lines.push(current.join(' ')); current = [w]; probe.textContent = w; lastTop = probe.getBoundingClientRect().height; }
      else { current.push(w); lastTop = top; }
    });
    if (current.length) lines.push(current.join(' '));
    el.textContent = '';
    lines.forEach((l) => { const d = document.createElement('span'); d.className = 'line'; const s = document.createElement('span'); s.textContent = l; d.appendChild(s); el.appendChild(d); });
    return $$('.line > span', el);
  }

  function introHero() {
    const title = $('.hero__title') || $('.page-head h1');
    if (!title) return;
    const spans = splitLines(title);
    const delay = cameFromInside ? 700 : 250;
    const cue = $('.hero__diamonds path');
    spans.forEach((s, i) => {
      if (reduce) { s.style.transform = 'none'; return; }
      s.style.transition = 'transform 1.1s cubic-bezier(.22,1,.36,1)';
      setTimeout(() => { s.style.transform = 'translateY(0)'; }, delay + i * 110);
    });
    const media = $('.hero__media img') || $('.page-head__media img');
    if (media && !reduce) {
      media.style.transition = 'transform 2.6s cubic-bezier(.22,1,.36,1)';
      setTimeout(() => { media.style.transform = 'scale(1)'; }, delay - 100);
    }
    if (cue && !reduce) {
      cue.style.transition = 'stroke-dashoffset 3.2s cubic-bezier(.22,1,.36,1)';
      setTimeout(() => { cue.style.strokeDashoffset = '0'; }, delay + 300);
    }
    $$('.hero [data-reveal], .page-head [data-reveal]').forEach((el, i) => setTimeout(() => el.classList.add('is-in'), delay + 350 + i * 120));
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
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
  $$('[data-reveal]:not(.hero [data-reveal]):not(.page-head [data-reveal]), .stagger, [data-count]').forEach((el) => io.observe(el));
  // clip-path'd images report a zero intersection area, so watch their host instead
  $$('.mask-img').forEach((m) => { const host = m.parentElement; host.dataset.maskHost = '1'; io.observe(host); });

  function countUp(el) {
    const target = parseFloat(el.getAttribute('data-count'));
    if (reduce || isNaN(target)) { el.textContent = el.getAttribute('data-count'); return; }
    const dur = 1400, start = performance.now();
    const step = (now) => {
      const p = Math.min(1, (now - start) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * e);
      if (p < 1) requestAnimationFrame(step);
    };
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

  /* ---------- services hover stage ---------- */
  const svc = $('.svc');
  if (svc) {
    const items = $$('.svc__item', svc), imgs = $$('.svc__stage img', svc), label = $('.svc__stage span', svc);
    const activate = (i) => {
      items.forEach((it, k) => it.classList.toggle('is-active', k === i));
      imgs.forEach((im, k) => im.classList.toggle('is-active', k === i));
      if (label) label.textContent = items[i].dataset.name;
    };
    items.forEach((it, i) => { it.addEventListener('mouseenter', () => activate(i)); it.addEventListener('focusin', () => activate(i)); });
    activate(0);
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
  window.addEventListener('load', () => {
    if (cameFromInside) veilOut();
    introHero();
  });
})();
