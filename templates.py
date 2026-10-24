"""HTML-шаблоны страниц. Каждая функция возвращает готовую строку HTML."""
import html
import json

from config import (ADVANTAGES, BRAND, CATEGORIES, FAQ, NAV, PRODUCTS, REVIEWS, STEPS)

CAT_NAMES = dict(CATEGORIES)


def esc(text):
    return html.escape(str(text), quote=True)


def money(value):
    return f"{value:,}".replace(",", " ") + " " + BRAND["currency"]


def svg_art(hue, label="", ratio=(400, 500)):
    """Генерирует SVG-заглушку вместо фото: градиент + силуэт вешалки."""
    w, h = ratio
    h2 = (hue + 50) % 360
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" '
        f'aria-label="{esc(label)}" preserveAspectRatio="xMidYMid slice">'
        f'<defs><linearGradient id="g{hue}" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="hsl({hue},70%,62%)"/>'
        f'<stop offset="1" stop-color="hsl({h2},75%,48%)"/></linearGradient></defs>'
        f'<rect width="{w}" height="{h}" fill="url(#g{hue})"/>'
        f'<circle cx="{w*0.8}" cy="{h*0.18}" r="{w*0.22}" fill="#fff" opacity=".12"/>'
        f'<circle cx="{w*0.15}" cy="{h*0.85}" r="{w*0.3}" fill="#000" opacity=".08"/>'
        f'<g fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" '
        f'stroke-linejoin="round" opacity=".9" transform="translate({w/2-70},{h/2-70})">'
        f'<path d="M70 20a14 14 0 1 1 14 14c-8 0-14 6-14 14v8"/>'
        f'<path d="M70 56L10 100c-8 6-4 16 6 16h108c10 0 14-10 6-16z"/></g>'
        f'<text x="{w/2}" y="{h-28}" text-anchor="middle" fill="#fff" font-size="22" '
        f'font-family="system-ui,sans-serif" font-weight="700" opacity=".95">{esc(label)}</text></svg>'
    )


def head(title, desc, root, path):
    full = f"{title} — {BRAND['name']}" if title else f"{BRAND['name']} — {BRAND['tagline']}"
    url = BRAND["site_url"].rstrip("/") + "/" + path
    return f"""<!doctype html>
<html lang="ru" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(full)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#7c3aed">
<link rel="canonical" href="{esc(url)}">
<meta property="og:title" content="{esc(full)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ru_RU">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{root}assets/style.css">
</head>"""


def header(root, active):
    links = "".join(
        f'<a href="{root}{href}"{" class=active" if href == active else ""}>{label}</a>'
        for href, label in NAV
    )
    return f"""<header class="header"><div class="wrap">
<a class="logo" href="{root}index.html">Neo<span class="grad">Style</span> KG</a>
<nav class="nav" aria-label="Основное меню">{links}</nav>
<div class="tools">
<button class="icon-btn" id="theme" aria-label="Сменить тему">◐</button>
<button class="icon-btn" id="open-cart" aria-label="Корзина">🛍<span class="count" id="cart-count">0</span></button>
<button class="icon-btn burger" aria-label="Меню">☰</button>
</div></div></header>"""


def drawer():
    return f"""<div class="veil"></div>
<aside class="drawer" aria-label="Корзина">
<div style="display:flex;justify-content:space-between;align-items:center">
<h3>Корзина</h3><button class="icon-btn" id="close-cart" aria-label="Закрыть">✕</button></div>
<div class="list" id="cart-list"></div>
<div class="line"><b>Итого</b><b id="cart-total">0 {BRAND['currency']}</b></div>
<a class="btn btn-wa" id="cart-wa" href="#" target="_blank" rel="noopener">Заказать в WhatsApp</a>
</aside><div class="toast" role="status"></div>"""


def footer(root):
    b = BRAND
    return f"""<footer class="footer"><div class="wrap">
<div><b style="color:var(--fg)">{b['name']}</b><br>{esc(b['tagline'])}<br>© {b['year']} Демо-версия сайта</div>
<div>{esc(b['city'])}<br>{esc(b['hours'])}<br><a href="tel:{b['phone'].replace(' ', '')}">{b['phone']}</a></div>
<div><a href="{b['instagram_url']}" target="_blank" rel="noopener">Instagram @{b['instagram']}</a><br>
<a href="https://wa.me/{b['whatsapp']}" target="_blank" rel="noopener">WhatsApp</a><br>
<a href="mailto:{b['email']}">{b['email']}</a></div>
</div></footer>"""


def catalog_json():
    data = {p["id"]: {"name": p["name"], "price": p["price"]} for p in PRODUCTS}
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def layout(title, desc, root, path, active, body):
    return (
        head(title, desc, root, path)
        + f'\n<body data-wa="{BRAND["whatsapp"]}" data-cur="{BRAND["currency"]}">\n'
        + header(root, active) + "\n<main>" + body + "</main>\n"
        + footer(root) + "\n" + drawer()
        + f'\n<script type="application/json" id="catalog-data">{catalog_json()}</script>'
        + f'\n<script src="{root}assets/app.js" defer></script>\n</body>\n</html>\n'
    )


def card(p, root):
    badge = f'<span class="badge">{esc(p["badge"])}</span>' if p["badge"] else ""
    old = f'<span class="old">{money(p["old_price"])}</span>' if p["old_price"] else ""
    return f"""<article class="card reveal" data-cat="{p['category']}" data-name="{esc(p['name'].lower())}">
<a class="img" href="{root}product/{p['id']}/index.html">{badge}{svg_art(p['hue'], p['name'])}</a>
<div class="body"><small style="color:var(--muted)">{CAT_NAMES.get(p['category'], '')}</small>
<h3><a href="{root}product/{p['id']}/index.html">{esc(p['name'])}</a></h3>
<div class="price">{money(p['price'])}{old}</div>
<button class="btn btn-primary add" data-add="{p['id']}">В корзину</button></div></article>"""


def page_home():
    root = ""
    hits = [p for p in PRODUCTS if p["badge"] in ("Хит", "New")][:4]
    feats = "".join(
        f'<div class="feature reveal"><div class="em">{e}</div><h3>{t}</h3>'
        f'<p style="color:var(--muted)">{d}</p></div>' for e, t, d in ADVANTAGES)
    steps = "".join(
        f'<div class="step reveal"><i>{n}</i><h3>{t}</h3><p style="color:var(--muted)">{d}</p></div>'
        for n, t, d in STEPS)
    reviews = "".join(
        f'<div class="review reveal"><div class="stars">{"★" * r}{"☆" * (5 - r)}</div>'
        f'<p>{esc(text)}</p><small style="color:var(--muted)">{esc(n)}, {esc(c)}</small></div>'
        for n, c, r, text in REVIEWS)
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in FAQ)
    cats = "".join(
        f'<a class="chip" href="catalog/index.html#{k}">{v}</a>' for k, v in CATEGORIES if k != "all")
    body = f"""
<section class="hero"><div class="wrap hero-grid">
<div><p class="lead" style="margin-bottom:10px">Новая коллекция · {BRAND['year']}</p>
<h1>{esc(BRAND['tagline'])}<br><span class="grad">NeoStyle KG</span></h1>
<p class="lead" style="margin-top:16px">{esc(BRAND['description'])}</p>
<div class="btns"><a class="btn btn-primary" href="catalog/index.html">Смотреть каталог</a>
<a class="btn btn-ghost" href="{BRAND['instagram_url']}" target="_blank" rel="noopener">Instagram</a></div>
<div class="stats"><div><b>{len(PRODUCTS)}+</b><span>товаров в демо</span></div>
<div><b>7 дней</b><span>на обмен</span></div><div><b>КР</b><span>доставка по стране</span></div></div></div>
<div class="hero-art">{svg_art(285, 'NeoStyle', (480, 600))}</div></div></section>
<section><div class="wrap"><h2>Категории</h2><div class="chips">{cats}</div>
<h2>Хиты и новинки</h2><div class="grid">{''.join(card(p, root) for p in hits)}</div>
<p style="margin-top:26px"><a class="btn btn-ghost" href="catalog/index.html">Весь каталог →</a></p></div></section>
<section><div class="wrap"><h2>Почему мы</h2><div class="features">{feats}</div></div></section>
<section><div class="wrap"><h2>Как заказать</h2><div class="steps">{steps}</div></div></section>
<section><div class="wrap"><h2>Отзывы</h2><div class="features">{reviews}</div></div></section>
<section><div class="wrap" style="max-width:780px"><h2>Частые вопросы</h2>{faq}</div></section>"""
    return layout("", BRAND["description"], root, "", "index.html", body)


def page_catalog():
    root = "../"
    chips = "".join(
        f'<button class="chip{" on" if k == "all" else ""}" data-cat="{k}">{v}</button>'
        for k, v in CATEGORIES)
    body = f"""<section><div class="wrap"><h1 style="font-size:2.4rem">Каталог</h1>
<p class="lead">Демо-ассортимент. Актуальные цены и наличие уточняйте в WhatsApp.</p>
<div class="chips" id="filters">{chips}</div>
<input class="search" id="search" type="search" placeholder="Поиск по названию…" aria-label="Поиск">
<div class="grid" id="product-grid" style="margin-top:24px">{''.join(card(p, root) for p in PRODUCTS)}</div>
<p class="empty" id="no-results" style="display:none">Ничего не найдено</p></div></section>"""
    return layout("Каталог", "Каталог одежды и аксессуаров NeoStyle KG.", root,
                  "catalog/", "catalog/index.html", body)


def page_product(p):
    root = "../../"
    opts = lambda items: "".join(
        f'<button class="chip{" on" if i == 0 else ""}">{esc(x)}</button>' for i, x in enumerate(items))
    old = f'<span class="old">{money(p["old_price"])}</span>' if p["old_price"] else ""
    related = [q for q in PRODUCTS if q["category"] == p["category"] and q["id"] != p["id"]][:4]
    rel = (f'<h2 style="margin-top:56px">Похожие товары</h2><div class="grid">'
           f'{"".join(card(q, root) for q in related)}</div>') if related else ""
    body = f"""<section><div class="wrap" data-product>
<div class="crumbs"><a href="{root}index.html">Главная</a> / <a href="{root}catalog/index.html">Каталог</a> / {esc(p['name'])}</div>
<div class="product"><div class="img">{svg_art(p['hue'], p['name'], (600, 750))}</div>
<div><small style="color:var(--muted)">{CAT_NAMES.get(p['category'], '')}</small>
<h1 style="font-size:2.3rem;margin:6px 0 12px">{esc(p['name'])}</h1>
<div class="price" style="font-size:1.5rem">{money(p['price'])}{old}</div>
<p class="lead" style="margin:16px 0">{esc(p['desc'])}</p>
<b>Цвет</b><div class="opts">{opts(p['colors'])}</div>
<b>Размер</b><div class="opts">{opts(p['sizes'])}</div>
<div style="display:flex;gap:12px;flex-wrap:wrap">
<button class="btn btn-primary" data-add="{p['id']}">В корзину</button>
<a class="btn btn-wa" target="_blank" rel="noopener"
href="https://wa.me/{BRAND['whatsapp']}?text=Здравствуйте!%20Интересует%20{esc(p['name'])}">Спросить в WhatsApp</a></div>
</div></div>{rel}</div></section>"""
    return layout(p["name"], p["desc"], root, f"product/{p['id']}/", "catalog/index.html", body)


def page_about():
    root = "../"
    body = f"""<section><div class="wrap" style="max-width:820px"><h1 style="font-size:2.4rem">О нас</h1>
<p class="lead" style="margin:14px 0 22px">{esc(BRAND['name'])} — это история про удобную и современную одежду,
которую хочется носить каждый день.</p>
<p style="color:var(--muted);margin-bottom:14px">Мы следим за трендами, отбираем ткани и фасоны, которые
хорошо сидят на реальных людях, и показываем новинки в Instagram
<a href="{BRAND['instagram_url']}" target="_blank" rel="noopener"><b>@{BRAND['instagram']}</b></a>.</p>
<p style="color:var(--muted);margin-bottom:14px">Это демонстрационная страница: замените текст на реальную историю
магазина в файле <code>config.py</code> и пересоберите сайт командой <code>python build.py</code>.</p>
<a class="btn btn-primary" href="../catalog/index.html">Перейти в каталог</a></div></section>"""
    return layout("О нас", "О магазине NeoStyle KG.", root, "about/", "about/index.html", body)


def page_contacts():
    root = "../"
    b = BRAND
    body = f"""<section><div class="wrap"><h1 style="font-size:2.4rem">Контакты</h1>
<p class="lead" style="margin:10px 0 24px">Напишите нам — ответим в течение нескольких минут.</p>
<div class="contact-grid"><div class="panel"><ul>
<li>📍 {esc(b['address'])}</li><li>🕒 {esc(b['hours'])}</li>
<li>📞 <a href="tel:{b['phone'].replace(' ', '')}">{b['phone']}</a></li>
<li>✉️ <a href="mailto:{b['email']}">{b['email']}</a></li>
<li>📷 <a href="{b['instagram_url']}" target="_blank" rel="noopener">@{b['instagram']}</a></li></ul>
<p style="margin-top:18px"><a class="btn btn-wa" target="_blank" rel="noopener"
href="https://wa.me/{b['whatsapp']}">Написать в WhatsApp</a></p></div>
<div class="panel"><h3>Быстрое сообщение</h3>
<p style="color:var(--muted);margin:8px 0 14px">Форма откроет WhatsApp с готовым текстом.</p>
<input class="search" id="cname" placeholder="Ваше имя" style="margin-bottom:10px;max-width:none">
<input class="search" id="cmsg" placeholder="Сообщение" style="margin-bottom:14px;max-width:none">
<a class="btn btn-primary" id="cform" href="#">Отправить</a></div></div></div></section>
<script>document.addEventListener('DOMContentLoaded',function(){{var a=document.getElementById('cform');
a.addEventListener('click',function(e){{e.preventDefault();var n=document.getElementById('cname').value||'';
var m=document.getElementById('cmsg').value||'';
window.open('https://wa.me/{b['whatsapp']}?text='+encodeURIComponent('Привет! Я '+n+'. '+m),'_blank')}})}})</script>"""
    return layout("Контакты", "Контакты NeoStyle KG.", root, "contacts/", "contacts/index.html", body)


def page_404():
    root = "/"
    body = """<section><div class="wrap" style="text-align:center;padding:80px 0">
<h1>404</h1><p class="lead" style="margin:12px auto 24px">Такой страницы нет.</p>
<a class="btn btn-primary" href="/index.html">На главную</a></div></section>"""
    return layout("Страница не найдена", "Страница не найдена", root, "404.html", "", body)


def favicon():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs>'
            '<linearGradient id="a" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7c3aed"/>'
            '<stop offset="1" stop-color="#ec4899"/></linearGradient></defs>'
            '<rect width="64" height="64" rx="16" fill="url(#a)"/>'
            '<text x="32" y="44" text-anchor="middle" font-size="34" font-weight="800" fill="#fff" '
            'font-family="system-ui,sans-serif">N</text></svg>')
