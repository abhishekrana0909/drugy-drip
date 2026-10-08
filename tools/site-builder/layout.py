"""Header, footer and pieces shared by every page."""
from html import escape
from urllib.parse import quote

from config import (ASSET_VERSION, BRAND, CITY, CURRENCY, EMAIL, INSTAGRAM, INSTAGRAM_HANDLE, PHONE_DISPLAY,
                    TAGLINE, WHATSAPP)
from products import CATEGORIES

ICON = {
    "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    "bag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 8h14l-1 13H6z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "close": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12h16M14 6l6 6-6 6"/></svg>',
    "left": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m15 6-6 6 6 6"/></svg>',
    "right": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 6 6 6-6 6"/></svg>',
    "down": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2z"/><path d="M16.6 14.1c-.3-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.8-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 2.9 2.9 0 0 0-.9 2.2 5 5 0 0 0 1.1 2.7 11.5 11.5 0 0 0 4.4 3.9c1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2l-.8-.3z"/></svg>',
    "insta": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s7-6.3 7-12a7 7 0 0 0-14 0c0 5.7 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>',
    "up": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 15 6-6 6 6"/></svg>',
}

NAV = [
    ("Home", "index.html", "home"),
    ("Shop", "shop.html", "shop"),
    ("New Drops", "shop.html#new", "new"),
    ("Lookbook", "index.html#lookbook", "lookbook"),
    ("Contact", "contact.html", "contact"),
]


def money(n):
    """79.99 -> $79.99"""
    return f"{CURRENCY}{n:,.2f}"


def wa_link(text=""):
    return f"https://wa.me/{WHATSAPP}?text={quote(text)}"


def socials():
    links = [(wa_link(f"Hi {BRAND}!"), "WhatsApp", ICON["wa"])]
    if INSTAGRAM:
        links.append((INSTAGRAM, "Instagram", ICON["insta"]))
    if EMAIL:
        links.append((f"mailto:{EMAIL}", "Email", ICON["mail"]))
    return "".join(f'<a href="{escape(u)}" target="_blank" rel="noopener" aria-label="{n}">{i}</a>' for u, n, i in links)


def head(title, description, extra=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<meta name="theme-color" content="#0b0b0b">
<meta property="og:type" content="website">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:image" content="images/logo/drugydrip-logo-640.webp">
<link rel="icon" href="images/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="images/favicon-192.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&amp;family=Archivo:wght@400;500;600;700&amp;family=Barlow+Condensed:ital,wght@0,600;0,700;1,700;1,800&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css?v={ASSET_VERSION}">
{extra}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""


def header(active):
    links = []
    for label, href, key in NAV:
        cur = ' aria-current="page"' if key == active else ""
        if key == "shop":
            cats = "".join(f'<a href="shop.html#{k}">{escape(v)}</a>' for k, v in CATEGORIES.items())
            links.append(
                f'<li class="nav__drop"><a class="nav__link" href="{href}"{cur}>{label} {ICON["down"]}</a>'
                f'<div class="nav__menu">{cats}</div></li>')
        else:
            links.append(f'<li><a class="nav__link" href="{href}"{cur}>{label}</a></li>')
    return f"""<div class="announce"><div class="announce__track">
  <span>Same leaf. Different drip.</span><span>Good vibes, bigger dreams</span><span>Oversized fits</span><span>Order on WhatsApp</span>
  <span>Same leaf. Different drip.</span><span>Good vibes, bigger dreams</span><span>Oversized fits</span><span>Order on WhatsApp</span>
</div></div>
<header class="header">
  <div class="container header__inner">
    <button class="icon-btn header__menu" type="button" data-nav-open aria-label="Open menu" aria-controls="site-nav" aria-expanded="false">{ICON["menu"]}</button>
    <a class="logo" href="index.html" aria-label="{BRAND} home"><img class="logo__mark" src="images/logo/drugydrip-logo-320.webp" alt="" width="320" height="370"><span class="logo__name">DRUGY <b>DRIP</b><small>Premium streetwear</small></span></a>
    <nav class="nav" id="site-nav" aria-label="Main">
      <button class="icon-btn nav__close" type="button" data-nav-close aria-label="Close menu">{ICON["close"]}</button>
      <ul class="nav__list">{"".join(links)}</ul>
    </nav>
    <div class="header__icons">
      <a class="icon-btn" href="shop.html#search" aria-label="Search products">{ICON["search"]}</a>
      <button class="icon-btn cart-btn" type="button" data-cart-open aria-label="Open cart">{ICON["bag"]}<span class="cart-btn__count" data-cart-count hidden>0</span></button>
    </div>
  </div>
</header>
<main id="main">
"""


def footer():
    cats = "".join(f'<li><a href="shop.html#{k}">{escape(v)}</a></li>' for k, v in CATEGORIES.items())
    contact = [f'<li><a href="{wa_link("Hi " + BRAND + "!")}" target="_blank" rel="noopener">{ICON["wa"]} {escape(PHONE_DISPLAY)}</a></li>']
    if INSTAGRAM:
        contact.append(f'<li><a href="{escape(INSTAGRAM)}" target="_blank" rel="noopener">{ICON["insta"]} {escape(INSTAGRAM_HANDLE)}</a></li>')
    if EMAIL:
        contact.append(f'<li><a href="mailto:{escape(EMAIL)}">{ICON["mail"]} {escape(EMAIL)}</a></li>')
    if CITY:
        contact.append(f'<li><span>{ICON["pin"]} {escape(CITY)}</span></li>')
    return f"""</main>
<footer class="footer">
  <div class="footer__grime" aria-hidden="true"></div>
  <div class="container footer__grid">
    <div class="footer__brand">
      <a class="footer__logo" href="index.html"><img src="images/logo/drugydrip-logo-640.webp" alt="{BRAND}" width="640" height="741" loading="lazy"></a>
      <p class="footer__name">DRUGY <b>DRIP</b></p>
      <p>{escape(TAGLINE)} Heavy cotton, dropped shoulders and wide legs, made to be worn loose.</p>
      <div class="footer__social">{socials()}</div>
    </div>
    <div><h3>Shop</h3><ul>{cats}</ul></div>
    <div><h3>Help</h3><ul>
      <li><a href="contact.html#order">How to order</a></li>
      <li><a href="contact.html#sizes">Size help</a></li>
      <li><a href="contact.html">Contact us</a></li>
    </ul></div>
    <div><h3>Talk to us</h3><ul class="footer__contact">{"".join(contact)}</ul></div>
  </div>
  <div class="container footer__bottom">
    <span>&copy; <span data-year>2026</span> {BRAND}. All rights reserved.</span>
    <span>Same leaf. Different drip.</span>
  </div>
</footer>
<a class="wa-float" href="{wa_link("Hi " + BRAND + "!")}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{ICON["wa"]}</a>
<button class="to-top" type="button" data-to-top aria-label="Back to top">{ICON["up"]}</button>
<script>window.DD_WHATSAPP = "{WHATSAPP}";</script>
<script src="js/cart.js?v={ASSET_VERSION}"></script>
<script src="js/main.js?v={ASSET_VERSION}"></script>
</body>
</html>
"""


def product_card(p, lazy=True):
    price = f'<b>{money(p["price"])}</b>'
    if p.get("mrp"):
        off = round(100 * (p["mrp"] - p["price"]) / p["mrp"])
        price += f' <s>{money(p["mrp"])}</s> <em>{off}% off</em>'
    sizes = "".join(f"<option>{escape(s)}</option>" for s in p["sizes"])
    colors = ""
    if len(p.get("colors", [])) > 1:
        opts = "".join(f"<option>{escape(c)}</option>" for c in p["colors"])
        colors = f'<label class="pick"><span>Colour</span><select data-opt="Colour">{opts}</select></label>'
    fixed = ""
    if len(p.get("colors", [])) == 1:
        fixed = escape('{"Colour": "%s"}' % p["colors"][0])
    badge = '<span class="card__badge">New</span>' if "new" in p.get("tags", []) else ""
    tags = " ".join(p.get("tags", []))
    return f"""<article class="card" data-pid="{p["id"]}" data-name="{escape(p["name"])}" data-price="{p["price"]}" data-img="images/products/{p["img"]}" data-cat="{p["cat"]}" data-tags="{tags}" data-fixed="{fixed}">
  <div class="card__img">{badge}<img src="images/products/{p["img"]}" alt="{escape(p["name"])}" width="560" height="700"{' loading="lazy"' if lazy else ""}></div>
  <div class="card__body">
    <h3 class="card__name">{escape(p["name"])}</h3>
    <p class="card__cat">{escape(CATEGORIES[p["cat"]])}</p>
    <p class="card__price">{price}</p>
    <div class="card__opts">
      <label class="pick"><span>Size</span><select data-opt="Size">{sizes}</select></label>{colors}
    </div>
    <button class="btn btn--add" type="button" data-add>{ICON["bag"]} Add to cart</button>
  </div>
</article>"""


def page_banner(eyebrow, title, image):
    return f"""<section class="page-banner" style="background-image: linear-gradient(90deg, rgba(8,8,8,.88), rgba(8,8,8,.35)), url('images/stock/{image}')">
  <div class="container">
    <p class="eyebrow">{escape(eyebrow)}</p>
    <h1><span class="ink">{title}</span></h1>
  </div>
</section>
"""
