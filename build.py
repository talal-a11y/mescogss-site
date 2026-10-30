#!/usr/bin/env python3
"""Generates the redesigned MESCO GSS static site (into the repo root) from content.py.
Wording comes from content.py verbatim. Run: python3 build.py"""
import os, html, json
from content import SITE, NAV, SERVICES, TEAM, HOME, ABOUT, CONTACT, FOOTER, BIO_PLACEHOLDER

OUT = os.path.dirname(os.path.abspath(__file__))
R = '{R}'  # placeholder, replaced per page with the relative prefix to the site root ('./', '../', '../../')
IMG = R + 'assets/img/'
e = html.escape

# ---------- icons ----------
I = {
  'arrow': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
  'arrow-l': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>',
  'mail': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
  'phone': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
  'wa': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22c5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2m0 1.67c4.54 0 8.24 3.7 8.24 8.24s-3.7 8.24-8.24 8.24c-1.5 0-2.97-.41-4.25-1.18l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.35c0-4.54 3.7-8.24 8.3-8.24m-3.5 4.02c-.18 0-.47.07-.72.34-.25.27-.95.93-.95 2.26s.97 2.62 1.11 2.8c.13.18 1.9 2.9 4.61 4.07 2.25.89 2.71.71 3.2.67.49-.05 1.58-.65 1.8-1.27.22-.62.22-1.15.16-1.27-.07-.11-.25-.18-.52-.31-.27-.14-1.58-.78-1.83-.87-.25-.09-.43-.13-.6.14-.18.27-.7.87-.86 1.05-.16.18-.31.2-.58.07-.27-.14-1.13-.42-2.16-1.33-.8-.71-1.34-1.59-1.5-1.86-.16-.27-.02-.42.12-.55.12-.12.27-.31.4-.47.14-.16.18-.27.27-.45.09-.18.05-.34-.02-.47-.07-.14-.6-1.45-.83-1.98-.22-.52-.44-.45-.6-.46h-.51"/></svg>',
  'pin': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
  'play': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15l13-7.5z"/></svg>',
  'in': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.5 8.5h-3V21h3V8.5zM5 3a1.8 1.8 0 1 0 0 3.6A1.8 1.8 0 0 0 5 3zm16 11.2c0-3.5-1.9-5.2-4.4-5.2-2 0-2.9 1.1-3.4 1.9V8.5h-3V21h3v-6.9c0-1.8.3-3.6 2.6-3.6 2.2 0 2.2 2.1 2.2 3.7V21h3v-6.8z"/></svg>',
  'chev-l': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>',
  'chev-r': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>',
}
SOCIAL_ICON = {'LinkedIn': 'in', 'Email': 'mail', 'WhatsApp': 'wa'}

DIAMONDS = '''<svg viewBox="0 0 467 467" aria-hidden="true">
<path d="M233 8 L459 233 L233 459 L8 233 Z"/>
<path d="M233 70 L397 233 L233 397 L70 233 Z"/>
<path d="M233 132 L335 233 L233 335 L132 233 Z"/>
</svg>'''

# ---------- shell ----------
def head(title, desc, path):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" type="image/png" href="{IMG}favicon.png">
<meta name="theme-color" content="#0A1831">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{IMG}banner.jpg">
<script>try{{if(sessionStorage.getItem('mgss-veil')==='1')document.documentElement.classList.add('veil-cover')}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{R}assets/style.css">
</head>
<body>
<div class="veil" aria-hidden="true"><div class="veil__panel veil__panel--a"></div><div class="veil__panel veil__panel--b"></div><div class="veil__mark"><span></span><span></span><span></span></div></div>
'''

def header(path):
    links = ''
    for label, href in NAV:
        cur = ' is-current' if href == path or (href != '/' and path.startswith(href)) else ''
        if label == 'SERVICES':
            items = ''.join(f'<li><a href="{R}{s["slug"]}/"{" class=\"is-current\"" if path=="/"+s["slug"]+"/" else ""}>{e(s["name"])}</a></li>' for s in SERVICES)
            links += f'<div class="nav__item nav__item--has-menu"><a class="nav__link{cur}" href="{R}{href[1:]}" aria-haspopup="true">{label}<span class="plus">+</span></a><ul class="dropdown">{items}</ul></div>'
        elif label == 'CONTACT US':
            links += f'<div class="nav__item"><a class="nav__link nav__link--cta" href="{R}{href[1:]}">{label}</a></div>'
        else:
            links += f'<div class="nav__item"><a class="nav__link{cur}" href="{R}{href[1:]}">{label}</a></div>'
    mobile_big = ''.join(f'<a class="big" href="{R}{href[1:]}" style="transition-delay:{.15+i*.07:.2f}s">{e(nice(l))}</a>' for i, (l, href) in enumerate(NAV))
    mobile_sub = ''.join(f'<a href="{R}{s["slug"]}/">{e(s["name"])}</a>' for s in SERVICES)
    return f'''<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{R}" aria-label="MESCO GSS — home"><img src="{IMG}MESCO-GSS.png" alt="MESCO GSS" width="1400" height="245"></a>
    <nav class="nav" aria-label="Primary">
      <a class="nav__email" href="mailto:{SITE['email']}">{I['mail']}{SITE['email']}</a>
      {links}
    </nav>
    <button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>
<div class="mobile-menu" aria-hidden="true">
  <div>{mobile_big}<div class="sub">{mobile_sub}</div></div>
  <div class="meta"><a href="mailto:{SITE['email']}">{SITE['email']}</a><br>{e(SITE['address'])}</div>
</div>
'''

def nice(label):
    return {'HOME': 'Home', 'ABOUT US': 'About us', 'SERVICES': 'Services', 'OUR TEAM': 'Our Team', 'CONTACT US': 'Contact us'}[label]

def footer(path):
    quick = ''.join(f'<li><a href="{R}{href[1:]}"{" class=\"is-current\"" if href==path else ""}>{e(nice(l))}</a></li>' for l, href in NAV)
    svcs = ''.join(f'<li><a href="{R}{s["slug"]}/"{" class=\"is-current\"" if path=="/"+s["slug"]+"/" else ""}>{e(s["name"])}</a></li>' for s in SERVICES)
    return f'''<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand"><img src="{IMG}Mesco-Gss-V-white.png" alt="MESCO GSS" width="482" height="368"></div>
      <div><h4>{FOOTER['quick']}</h4><ul>{quick}</ul></div>
      <div><h4>{FOOTER['services']}</h4><ul>{svcs}</ul></div>
      <div><h4>{FOOTER['contact']}</h4><ul class="footer__contact">
        <li>{I['mail']}<a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
        <li>{I['pin']}<span>{e(SITE['address'])}</span></li></ul></div>
      <div><h4>{FOOTER['subscribe']}</h4>
        <form class="subscribe" id="subscribe-form"><label class="sr" for="sub-email">{FOOTER['subscribe_placeholder']}</label><input id="sub-email" name="email" type="email" placeholder="{FOOTER['subscribe_placeholder']}" required><button class="btn" type="submit">{FOOTER['subscribe_cta']}</button></form></div>
    </div>
    <div class="footer__bottom"><span>MESCO GSS</span><span>Dubai, United Arab Emirates</span></div>
  </div>
</footer>
<script src="{R}assets/main.js" defer></script>
</body>
</html>
'''

def page_head(title, image, crumbs):
    cr = ''.join(f'<span>{e(c)}</span>' for c in crumbs)
    return f'''<section class="page-head">
  <div class="page-head__media" data-parallax><img src="{IMG}{image}" alt=""></div>
  <div class="page-head__content wrap">
    <div class="crumbs" data-reveal="fade">{cr}</div>
    <h1>{e(title)}</h1>
  </div>
</section>
'''

def sec_head(eyebrow, title, extra='', cls=''):
    return f'<div class="sec-head {cls}" data-reveal><div><p class="eyebrow">{e(eyebrow)}</p><h2 class="h-l">{e(title)}</h2></div>{extra}</div>'

# ---------- components ----------
def services_diamonds(cta):
    tiles = ''.join(f'''<a class="dia" href="{R}{sv["slug"]}/">
      <span class="dia__clip"><img src="{IMG}{sv["card"]}" alt="" loading="lazy"></span>
      <span class="dia__label"><b>{e(sv["name_upper"])}</b><i>{cta} {I["arrow"]}</i></span>
    </a>''' for sv in SERVICES)
    return f'<div class="dia-grid stagger">{tiles}</div>'

def person_links(p, cls=''):
    out = ''
    for kind, val in p['links']:
        if kind == 'tel': out += f'<a class="{cls}" href="tel:{val}" aria-label="Call {e(p["name"])}">{I["phone"]}<span>{e(val)}</span></a>'
        elif kind == 'mail': out += f'<a class="{cls}" href="mailto:{val}" aria-label="Email {e(p["name"])}">{I["mail"]}<span>{e(val)}</span></a>'
        elif kind == 'wa': out += f'<a class="{cls}" href="https://wa.me/{val}" target="_blank" rel="noopener" aria-label="WhatsApp {e(p["name"])}">{I["wa"]}<span>WhatsApp</span></a>'
    return out

def person_card(p):
    return f'''<article class="person">
  <a class="person__img" href="{R}our-team/{p['slug']}/" aria-label="{e(p['name'])}"><img src="{IMG}{p['img']}" alt="{e(p['name'])}" loading="lazy" draggable="false"></a>
  <div class="person__panel">
    <div class="person__name"><b>{e(p['name'])}</b><span>{e(p['role'])}</span></div>
    <p class="person__bio">{e(p.get('bio') or BIO_PLACEHOLDER)}</p>
    <div class="person__foot"><a class="link-arrow" href="{R}our-team/{p['slug']}/">View profile {I['arrow']}</a><div class="person__icons">{person_links(p)}</div></div>
  </div>
</article>'''

def team_strip():
    t = HOME['team']
    cards = ''.join(person_card(p) for p in TEAM)
    return f'''<section class="section">
  <div class="wrap">
    {sec_head(t['eyebrow'], t['title'], f'<div class="team-nav"><button type="button" data-dir="prev" aria-label="Previous">{I["chev-l"]}</button><button type="button" data-dir="next" aria-label="Next">{I["chev-r"]}</button></div>')}
    <div class="strip">{cards}</div>
    <div class="actions" data-reveal><a class="btn" href="{R}our-team/">OUR TEAM {I['arrow']}</a><a class="btn btn--ghost" href="{R}contact-us/">{t['cta']} {I['arrow']}</a></div>
  </div>
</section>
'''

def contact_band():
    c = HOME['contact']
    return f'''<section class="section">
  <div class="wrap cta-band">
    <div class="mask-img" data-parallax><img src="{IMG}contact.jpg" alt="" loading="lazy"></div>
    <div data-reveal>
      <p class="eyebrow">{c['eyebrow']}</p>
      <h2 class="h-l">{e(c['title'])}</h2>
      <p class="lede">{e(c['text'])}</p>
      <a class="contact-line" href="mailto:{SITE['email']}"><i>{I['mail']}</i>{SITE['email']}</a>
      <div class="actions"><a class="btn" href="{R}contact-us/">{c['cta']} {I['arrow']}</a></div>
    </div>
  </div>
</section>
'''

# ---------- HOME ----------
def home():
    a, s, w, q, cn = HOME['about'], HOME['services'], HOME['why'], HOME['partners'], HOME['counters']
    counters = ''.join(f'<div class="counter"><b><span data-count="{n}">0</span><em>{u}</em></b><span>{e(l)}</span></div>' for n, u, l in cn['items'])
    why = ''.join(f'<div class="why__item"><i></i><h3>{e(h)}</h3><p>{e(p)}</p></div>' for h, p in w['items'])
    quotes = ''.join(f'<blockquote class="quote"><p>{e(qt)}</p><h3>{e(who)}</h3></blockquote>' for qt, who in q['quotes'])
    body = f'''
<section class="hero">
  <div class="hero__media"><img src="{IMG}banner.jpg" alt="" fetchpriority="high"></div>
  <div class="hero__diamonds">{DIAMONDS}</div>
  <div class="hero__content wrap">
    <p class="hero__eyebrow" data-reveal="fade">{HOME['eyebrow']}</p>
    <h1 class="hero__title">{e(SITE['tagline'])}</h1>
    <div class="hero__row">
      <a class="btn" href="{R}services/" data-reveal>{HOME['hero_cta']} {I['arrow']}</a>
      <div class="hero__cue" data-reveal="fade"><i></i><span>Scroll</span></div>
    </div>
  </div>
</section>

<section class="section section--light">
  <div class="wrap about">
    <div class="about__media">
      <div class="mask-img" data-parallax><img src="{IMG}about.jpg" alt="" loading="lazy"></div>
      <div class="about__stat" data-reveal><b><span data-count="15">0</span>+</b><span>{a['stat_label']}</span></div>
    </div>
    <div class="about__body" data-reveal>
      <p class="eyebrow">{a['eyebrow']}</p>
      <h2 class="h-l">{e(a['title'])}</h2>
      <p class="lede">{e(a['text'])}</p>
      <div class="actions"><a class="btn" href="{R}about-us/">{a['cta']} {I['arrow']}</a></div>
    </div>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap">
    {sec_head(cn['eyebrow'], cn['title'])}
    <div class="counters stagger">{counters}</div>
  </div>
</section>

<section class="video">
  <div class="video__frame">
    <img src="{IMG}video.jpg" alt="" loading="lazy">
    <video src="{R}assets/video/jebel-ali.mp4" playsinline preload="none" controls></video>
    <button class="video__play" aria-label="Play video">{I['play']}</button>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {sec_head(s['eyebrow'], s['title'], f'<a class="link-arrow" href="{R}services/">All services {I["arrow"]}</a>', 'sec-head--center')}
    {services_diamonds(s['cta'])}
  </div>
</section>

<section class="section section--light">
  <div class="wrap">
    {sec_head(w['eyebrow'], w['title'])}
    <div class="why stagger">{why}</div>
    <div class="actions actions--center" data-reveal><a class="btn" href="{R}contact-us/">{e(w['cta'])} {I['arrow']}</a></div>
  </div>
</section>

{team_strip()}

<section class="section section--dark">
  <div class="wrap">
    {sec_head(q['eyebrow'], q['title'])}
    <div class="quotes stagger">{quotes}</div>
    <a class="linkedin" href="https://www.linkedin.com/" target="_blank" rel="noopener">{I['in']} Linkedin</a>
  </div>
</section>

{contact_band()}
'''
    return head('MESCO GSS', 'Protecting you today, preparing you for tomorrow. MESCO GSS — ship insurance solutions in Dubai.', '/') + header('/') + '<main>' + body + '</main>' + footer('/')

# ---------- ABOUT ----------
def about():
    b1, b2 = ABOUT['block1'], ABOUT['block2']
    cards = ''
    for (name, year), para in zip(ABOUT['origins_cards'], b1):
        cards += f'''<article class="origin" data-reveal>
      <div class="origin__head"><span class="origin__dia"></span><div><b>{e(name)}</b><span>{e(year)}</span></div></div>
      <p>{e(para)}</p>
    </article>'''
    body = page_head(ABOUT['title'], 'hero.jpg', ['Home', 'About us']) + f'''
<section class="section">
  <div class="wrap">
    {sec_head(HOME['about']['eyebrow'], ABOUT['origins_title'])}
    <div class="origins">
      {cards}
      <div class="origins__join" aria-hidden="true"><span></span><span></span><span></span></div>
    </div>
  </div>
</section>
<section class="section section--light">
  <div class="wrap story">
    <div class="story__media"><div class="mask-img" data-parallax><img src="{IMG}about-us.jpg" alt="" loading="lazy"></div></div>
    <div class="story__body" data-reveal>
      <p class="eyebrow">{HOME['about']['eyebrow']}</p>
      <h2 class="h-l">{e(ABOUT['venture_title'])}</h2>
      <p>{e(b2[0])}</p>
      <p>{e(b2[1])}</p>
    </div>
  </div>
</section>
<section class="section section--dark">
  <div class="wrap about-media">
    <div class="mask-img" data-parallax><img src="{IMG}about.jpg" alt="" loading="lazy"></div>
    <div data-reveal>
      <p class="eyebrow">{HOME['about']['eyebrow']}</p>
      <h2 class="h-l">{e(HOME['about']['title'])}</h2>
      <p class="lede">{e(HOME['about']['text'])}</p>
      <div class="actions"><a class="btn" href="{R}services/">{HOME['hero_cta']} {I['arrow']}</a></div>
    </div>
  </div>
</section>
''' + contact_band()
    return head('About us – MESCO GSS', b2[0][:150], '/about-us/') + header('/about-us/') + '<main>' + body + '</main>' + footer('/about-us/')

# ---------- SERVICES ----------
def services():
    s = HOME['services']
    body = page_head('Services', 'hero.jpg', ['Home', 'Services']) + f'''
<section class="section">
  <div class="wrap">
    {sec_head(s['eyebrow'], s['title'], '', 'sec-head--center')}
    {services_diamonds(s['cta'])}
  </div>
</section>
''' + contact_band()
    return head('Services – MESCO GSS', s['title'], '/services/') + header('/services/') + '<main>' + body + '</main>' + footer('/services/')

# ---------- TEAM ----------
def team():
    t = HOME['team']
    divisions = {}
    for p in TEAM: divisions.setdefault(p['division'], []).append(p)
    groups = ''
    for name, people in divisions.items():
        cards = ''.join(person_card(p) for p in people)
        label = f'<h3 class="division" data-reveal>{e(name)}</h3>' if len(divisions) > 1 else ''
        groups += f'{label}<div class="team-grid stagger">{cards}</div>'
    body = page_head('Our Team', 'hero.jpg', ['Home', 'Our Team']) + f'''
<section class="section">
  <div class="wrap">
    {sec_head(t['eyebrow'], t['title'])}
    {groups}
    <div class="actions actions--center" data-reveal><a class="btn" href="{R}contact-us/">{t['cta']} {I['arrow']}</a></div>
  </div>
</section>
''' + contact_band()
    return head('Our Team – MESCO GSS', t['title'], '/our-team/') + header('/our-team/') + '<main>' + body + '</main>' + footer('/our-team/')

def person_page(p):
    idx = TEAM.index(p)
    prev_p, next_p = TEAM[idx - 1], TEAM[(idx + 1) % len(TEAM)]
    others = ''.join(f'<a class="mini" href="{R}our-team/{o["slug"]}/"><img src="{IMG}{o["img"]}" alt="" loading="lazy"><b>{e(o["name"])}</b><span>{e(o["role"])}</span></a>' for o in TEAM if o is not p)
    body = f'''
<section class="profile">
  <div class="profile__media"><img src="{IMG}{p['img']}" alt="{e(p['name'])}" fetchpriority="high"></div>
  <div class="profile__body wrap">
    <a class="back" href="{R}our-team/">{I['arrow-l']} Our Team</a>
    <p class="eyebrow">{e(p['division'])}</p>
    <h1 class="h-xl">{e(p['name'])}</h1>
    <p class="profile__role">{e(p['role'])}</p>
    <div class="profile__bio" data-reveal>
      <p>{e(p.get('bio') or BIO_PLACEHOLDER)}</p>
    </div>
    <div class="profile__links" data-reveal>{person_links(p, 'pill')}</div>
    <div class="profile__nav" data-reveal>
      <a href="{R}our-team/{prev_p['slug']}/">{I['arrow-l']} {e(prev_p['name'])}</a>
      <a href="{R}our-team/{next_p['slug']}/">{e(next_p['name'])} {I['arrow']}</a>
    </div>
  </div>
</section>
<section class="section section--light">
  <div class="wrap">
    {sec_head(HOME['team']['eyebrow'], HOME['team']['title'])}
    <div class="minis stagger">{others}</div>
  </div>
</section>
'''
    path = f'/our-team/{p["slug"]}/'
    return head(f'{p["name"]} – MESCO GSS', f'{p["name"]}, {p["role"]} at MESCO GSS.', path) + header('/our-team/') + '<main>' + body + '</main>' + footer('/our-team/')

# ---------- CONTACT ----------
def contact():
    fields = ''
    for label, kind, name in CONTACT['form']:
        req = '' if 'optional' in label else ' required'
        if kind == 'textarea':
            fields += f'<div class="field"><textarea id="f-{name}" name="{name}" placeholder=" "></textarea><label for="f-{name}">{e(label)}</label></div>'
        else:
            fields += f'<div class="field"><input id="f-{name}" name="{name}" type="{kind}" placeholder=" "{req}><label for="f-{name}">{e(label)}</label></div>'
    socials = ''.join(f'<a href="{u}"{" target=\"_blank\" rel=\"noopener\"" if u.startswith("http") else ""}>{I[SOCIAL_ICON[n]]}<span>{e(n)}</span></a>' for n, u in SITE['socials'])
    body = page_head(CONTACT['title'], 'hero.jpg', ['Home', 'Contact us']) + f'''
<section class="section">
  <div class="wrap contact">
    <form class="form" id="contact-form" data-reveal>
      {fields}
      <div class="actions"><button class="btn" type="submit">Send {I['arrow']}</button></div>
    </form>
    <aside class="contact__aside" data-reveal="right">
      <h2 class="h-m">{e(CONTACT['heading'])}</h2>
      <ul class="details">
        <li><i>{I['mail']}</i><a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
        <li><i>{I['pin']}</i><span>{e(SITE['address'])}</span></li>
      </ul>
      <div class="socials">{socials}</div>
    </aside>
  </div>
</section>
'''
    return head('Contact us – MESCO GSS', 'Get in touch with MESCO GSS.', '/contact-us/') + header('/contact-us/') + '<main>' + body + '</main>' + footer('/contact-us/')

# ---------- SERVICE DETAIL ----------
def service(sv):
    pts = ''.join(f'<li class="point"><i></i><p>{e(p)}</p></li>' for p in sv['points'])
    others = ''.join(f'<a href="{R}{o["slug"]}/"><img src="{IMG}{o["card"]}" alt="" loading="lazy"><span>{e(o["name_upper"])}</span></a>' for o in SERVICES if o['slug'] != sv['slug'])
    body = page_head(sv['name'], sv['header'], ['Home', 'Services', sv['name']]) + f'''
<section class="section section--tight">
  <div class="wrap">
    <div class="svc-intro" data-reveal>
      <p class="eyebrow">{HOME['services']['eyebrow']}</p>
      <p class="lede lede--big">{e(sv['intro'])}</p>
    </div>
    <ul class="points stagger">{pts}</ul>
    <div class="svc-outro" data-reveal>
      <p>{e(sv['outro'])}</p>
      <a class="btn" href="{R}contact-us/">CONTACT US {I['arrow']}</a>
    </div>
  </div>
</section>
<section class="section section--light">
  <div class="wrap">
    {sec_head(HOME['services']['eyebrow'], HOME['services']['title'])}
    <div class="more-svc stagger">{others}</div>
  </div>
</section>
'''
    p = f'/{sv["slug"]}/'
    return head(f'{sv["name"]} – MESCO GSS', sv['intro'], p) + header(p) + '<main>' + body + '</main>' + footer(p)

# ---------- write ----------
def write(path, content):
    full = os.path.join(OUT, path.strip('/'), 'index.html') if path != '/' else os.path.join(OUT, 'index.html')
    os.makedirs(os.path.dirname(full), exist_ok=True)
    depth = len([s for s in path.strip('/').split('/') if s])
    rel = './' if depth == 0 else '../' * depth
    open(full, 'w').write(content.replace('{R}', rel))

write('/', home()); write('/about-us/', about()); write('/services/', services()); write('/our-team/', team()); write('/contact-us/', contact())
for sv in SERVICES: write(f'/{sv["slug"]}/', service(sv))
for p in TEAM: write(f'/our-team/{p["slug"]}/', person_page(p))
json.dump({"cleanUrls": True, "trailingSlash": True,
           "headers": [{"source": "/(.*)", "headers": [{"key": "X-Robots-Tag", "value": "noindex, nofollow"}]}]},
          open(os.path.join(OUT, 'vercel.json'), 'w'), indent=2)
print('built', 5 + len(SERVICES) + len(TEAM), 'pages')
