"""Home page (index.html)."""
from config import BRAND, INSTAGRAM, TAGLINE
from layout import ICON, footer, head, header, product_card
from products import CATEGORIES, PRODUCTS

SLIDES = [
    dict(kicker="New collection", lines=["SAME LEAF.", "NEW DRIP."], text="Premium streetwear for a higher state of mind.",
         photos=("outfit-1.webp", "outfit-2.webp"), link="shop.html#new", cta="Shop the drop"),
    dict(kicker="Our roots. Our culture.", lines=["GOOD VIBES", "BIG DREAMS"], text="Back-print tees, wide-leg pants and the leaf on everything.",
         photos=("outfit-3.webp", "outfit-4.webp"), link="shop.html#tees", cta="Shop tees"),
    dict(kicker="Layer up. Level up.", lines=["STAY", "DRIPPY"], text="Heavy hoodies, zip jackets and baggy cargos.",
         photos=("outfit-5.webp", "outfit-6.webp"), link="shop.html#hoodies", cta="Shop hoodies"),
]

BADGE = """<svg class="badge" viewBox="0 0 200 200" aria-hidden="true">
  <defs><path id="badge-ring" d="M100 100m-72 0a72 72 0 1 1 144 0a72 72 0 1 1-144 0"/></defs>
  <text><textPath href="#badge-ring" textLength="446" lengthAdjust="spacing">PREMIUM QUALITY &#8226; DRUGY DRIP &#8226;</textPath></text>
</svg>"""


def hero():
    slides = []
    for i, s in enumerate(SLIDES):
        a, b = s["photos"]
        load = "eager" if i == 0 else "lazy"
        slides.append(f"""<div class="hero__slide{' is-active' if i == 0 else ''}" data-slide aria-roledescription="slide" aria-label="{i + 1} of {len(SLIDES)}">
      <div class="container hero__inner">
        <div class="hero__text">
          <p class="hero__kicker">{s["kicker"]}</p>
          <h{'1' if i == 0 else '2'} class="hero__title"><span class="ink">{s["lines"][0]}</span><br><span class="ink">{s["lines"][1]}</span></h{'1' if i == 0 else '2'}>
          <p class="hero__sub">{s["text"]}</p>
          <a class="btn btn--dark" href="{s["link"]}">{s["cta"]} {ICON["arrow"]}</a>
        </div>
        <div class="hero__photos">
          <img class="hero__photo hero__photo--a" src="images/stock/{a}" alt="" width="600" height="1420" loading="{load}">
          <img class="hero__photo hero__photo--b" src="images/stock/{b}" alt="" width="600" height="1420" loading="{load}">
          {BADGE}
        </div>
      </div>
    </div>""")
    dots = "".join(f'<button type="button" data-dot="{i}" aria-label="Show slide {i + 1}"{" aria-current=\"true\"" if i == 0 else ""}></button>' for i in range(len(SLIDES)))
    return f"""<section class="hero" aria-roledescription="carousel" aria-label="Featured drops" data-slider>
  {"".join(slides)}
  <button class="hero__arrow hero__arrow--prev" type="button" data-prev aria-label="Previous slide">{ICON["left"]}</button>
  <button class="hero__arrow hero__arrow--next" type="button" data-next aria-label="Next slide">{ICON["right"]}</button>
  <div class="hero__dots">{dots}</div>
</section>
"""


def tiles():
    return f"""<section class="tiles" aria-label="Collections">
  <a class="tile tile--sand" href="shop.html#hoodies">
    <img src="images/stock/outfit-2.webp" alt="" loading="lazy" width="600" height="1420">
    <span class="tile__text tile__text--right"><span class="ink">STREETWEAR</span><br><span class="ink">EXCLUSIVE</span>
      <span class="tile__link">Shop hoodies {ICON["arrow"]}</span></span>
  </a>
  <a class="tile tile--grey" href="shop.html#lowers">
    <img src="images/stock/outfit-1.webp" alt="" loading="lazy" width="600" height="1420">
    <span class="tile__text"><span class="ink">BAGGY</span><br><span class="ink">LOWERS</span>
      <span class="tile__link">Shop lowers {ICON["arrow"]}</span></span>
  </a>
  <a class="tile tile--big tile--tee" href="shop.html#tees">
    <img src="images/stock/tee-back-big.webp" alt="" loading="lazy" width="630" height="772">
    <span class="tile__text tile__text--bottom"><span class="ink ink--xl">OUR ROOTS.</span><br><span class="ink ink--xl">OUR DRIP.</span>
      <span class="tile__sub">The Heritage back print tee {ICON["arrow"]}</span></span>
  </a>
</section>
"""


def best_sellers():
    groups = [("hoodies", "Hoodies"), ("tees", "Tees"), ("lowers", "Lowers")]
    tabs = "".join(f'<button type="button" role="tab" data-tab="{k}" aria-selected="{"true" if i == 0 else "false"}">{v}</button>'
                   for i, (k, v) in enumerate(groups))
    panels = []
    for i, (k, _) in enumerate(groups):
        items = sorted((p for p in PRODUCTS if p["cat"] == k), key=lambda p: "best" not in p["tags"])[:4]
        panels.append(f'<div class="product-grid product-grid--lined" role="tabpanel" data-panel="{k}"{"" if i == 0 else " hidden"}>'
                      + "".join(product_card(p) for p in items) + "</div>")
    return f"""<section class="section" id="best-sellers">
  <div class="container">
    <div class="section-head section-head--split">
      <h2 class="title-shadow">BEST SELLERS</h2>
      <div class="tabs" role="tablist" aria-label="Best seller categories">{tabs}</div>
    </div>
  </div>
  <div class="container container--wide">{"".join(panels)}</div>
</section>
"""


def drops_grid():
    return f"""<section class="section section--grain">
  <div class="container drops">
    <a class="drop drop--a" href="shop.html#lowers">
      <img src="images/stock/outfit-6.webp" alt="" loading="lazy" width="600" height="1420">
      <span class="drop__text drop__text--right"><small>Hot days</small><strong>BIGGER<br>DREAMS</strong></span>
    </a>
    <a class="drop drop--b" href="shop.html#lowers">
      <img src="images/stock/outfit-4.webp" alt="" loading="lazy" width="600" height="1420">
      <span class="drop__text drop__text--center"><small>More drip</small><strong>MORE<br>FREEDOM</strong><span class="btn btn--ghost">{ICON["arrow"]} Explore now</span></span>
    </a>
    <a class="drop drop--c" href="shop.html#hoodies">
      <span class="drop__text drop__text--top"><small>Our picks</small><strong>TOP DROPS</strong><span class="btn btn--outline">{ICON["arrow"]} Shop now</span></span>
      <img src="images/stock/outfit-5.webp" alt="" loading="lazy" width="600" height="1420">
    </a>
    <div class="order-strip" id="how-to-order">
      <p class="order-strip__big">ORDER ON<br>WHATSAPP</p>
      <ol class="order-strip__steps">
        <li><mark>Pick your size</mark> and add to cart</li>
        <li><mark>Send the cart</mark> to us on WhatsApp</li>
        <li>We confirm stock, price and delivery</li>
      </ol>
    </div>
  </div>
</section>
"""


def new_arrivals():
    items = [p for p in PRODUCTS if "new" in p["tags"]][:4]
    return f"""<section class="section section--grain" id="new">
  <div class="container">
    <div class="section-head section-head--center">
      <h2 class="title-brush">NEW ARRIVALS</h2>
    </div>
    <div class="product-grid">{"".join(product_card(p) for p in items)}</div>
    <p class="center"><a class="btn btn--dark" href="shop.html">View all products {ICON["arrow"]}</a></p>
  </div>
</section>
"""


def banners():
    return f"""<section class="banners" aria-label="Featured looks">
  <a class="banner banner--mint" href="shop.html#tees">
    <img src="images/stock/detail-print.webp" alt="" loading="lazy" width="932" height="792">
    <span class="banner__text"><small>Print detail</small><strong>WEAR<br>THE<br>VIBE</strong></span>
  </a>
  <a class="banner banner--cream" href="shop.html#tees">
    <img src="images/stock/tee-front-big.webp" alt="" loading="lazy" width="630" height="772">
    <span class="banner__text"><small>Washed heavy cotton</small><strong>SIMPLE.<br>CLEAN.<br>ICONIC.</strong></span>
  </a>
</section>
"""


LOOKS = ["detail-label", "look-hoodie", "detail-print-2", "detail-sleeve", "look-cap", "detail-stitch"]


def lookbook():
    shots = "".join(f'<a class="look" href="{INSTAGRAM or "shop.html"}"{" target=\"_blank\" rel=\"noopener\"" if INSTAGRAM else ""}>'
                    f'<img src="images/stock/{pic}.webp" alt="" loading="lazy" width="600" height="445"></a>' for pic in LOOKS)
    return f"""<section class="section lookbook" id="lookbook">
  <div class="container">
    <div class="section-head section-head--center">
      <p class="eyebrow">Lookbook</p>
      <h2 class="title-brush">#DRUGYDRIP</h2>
      <p>Good vibes. Bigger dreams. Tag us to get featured.</p>
    </div>
  </div>
  <div class="looks">{shots}</div>
</section>
"""


def categories_strip():
    items = "".join(f'<a href="shop.html#{k}">{v}</a>' for k, v in CATEGORIES.items())
    return f'<nav class="cat-strip" aria-label="Categories"><div class="container cat-strip__inner">{items}</div></nav>\n'


def build():
    return (head(f"{BRAND} | Premium Baggy Streetwear",
                 f"{BRAND}: {TAGLINE} Oversized tees, heavy hoodies, baggy lowers, jackets and caps. Order on WhatsApp.")
            + header("home") + hero() + categories_strip() + tiles() + best_sellers() + drops_grid()
            + new_arrivals() + banners() + lookbook() + footer())
