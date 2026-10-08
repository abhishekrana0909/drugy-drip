"""Shop page (shop.html): every product with category filters, search and sort."""
from config import BRAND
from layout import ICON, footer, head, header, page_banner, product_card
from products import CATEGORIES, PRODUCTS


def build():
    chips = ['<button type="button" class="chip is-on" data-filter="all">All</button>',
             '<button type="button" class="chip" data-filter="new">New drops</button>']
    chips += [f'<button type="button" class="chip" data-filter="{k}">{v}</button>' for k, v in CATEGORIES.items()]
    cards = "".join(product_card(p) for p in PRODUCTS)
    body = f"""{page_banner("The full drop", "SHOP ALL", "concrete.webp")}
<section class="section shop" data-shop>
  <div class="container">
    <div class="shop__bar">
      <div class="chips" role="group" aria-label="Filter by category">{"".join(chips)}</div>
      <div class="shop__tools">
        <label class="search" id="search">{ICON["search"]}<span class="sr-only">Search products</span>
          <input type="search" placeholder="Search hoodies, tees, cargos..." data-search></label>
        <label class="sort"><span class="sr-only">Sort</span>
          <select data-sort>
            <option value="">Sort: Featured</option>
            <option value="low">Price: low to high</option>
            <option value="high">Price: high to low</option>
          </select></label>
      </div>
    </div>
    <p class="shop__count" data-count aria-live="polite">{len(PRODUCTS)} products</p>
    <div class="product-grid" data-grid>{cards}</div>
    <p class="shop__empty" data-empty hidden>Nothing matches that. Try another word or category.</p>
  </div>
</section>
"""
    return (head(f"Shop | {BRAND}", f"Shop {BRAND}: oversized tees, hoodies, baggy lowers, jackets and accessories.")
            + header("shop") + body + footer())
