"""All products. Prices are in US dollars. Add, remove or edit rows here, then run build.py.

Fields:
  id      unique short name (used by the cart)
  name    product name
  cat     category key from CATEGORIES
  price   selling price (leave it out to use the category price below)
  img     photo in images/products/ (cut from the mockups by tools/crop_mockups.py)
  sizes   size options shown in the dropdown
  colors  colour options (optional)
  tags    "best" = Best Sellers on home page, "new" = New Arrivals
"""

CATEGORIES = {
    "hoodies": "Hoodies",
    "tees": "Tees & Tanks",
    "lowers": "Lowers",
    "jackets": "Jackets",
    "accessories": "Accessories",
}

# one price per category
PRICE = {
    "hoodies": 79.99,
    "tees": 29.99,
    "lowers": 39.99,
    "jackets": 79.99,      # not given yet, same as hoodies for now
    "accessories": 24.99,  # not given yet
}

TOP = ["S", "M", "L", "XL", "XXL"]
WAIST = ["28", "30", "32", "34", "36"]
FREE = ["One size"]

PRODUCTS = [
    # hoodies
    dict(id="hoodie-front-leaf", name="Oversized Leaf Hoodie", cat="hoodies", img="hoodie-front-leaf.webp",
         sizes=TOP, colors=["Black"], tags=["best", "new"]),
    dict(id="hoodie-back-print", name="Flame Back Print Hoodie", cat="hoodies", img="hoodie-back-print.webp",
         sizes=TOP, colors=["Black"], tags=["best"]),
    dict(id="hoodie-forest", name="Forest Green Leaf Hoodie", cat="hoodies", img="hoodie-forest.webp",
         sizes=TOP, colors=["Forest green"], tags=["best", "new"]),
    dict(id="hoodie-zip-olive", name="Olive Zip-Up Hoodie", cat="hoodies", img="hoodie-zip-olive.webp",
         sizes=TOP, colors=["Olive"], tags=["best"]),

    # tees
    dict(id="tee-heritage", name="Heritage Back Print Tee", cat="tees", img="tee-heritage-back.webp",
         sizes=TOP, colors=["Washed sand"], tags=["best", "new"]),
    dict(id="tee-graphic-back", name="Graphic Back Tee", cat="tees", img="tee-graphic-back.webp",
         sizes=TOP, colors=["Cream"], tags=["best"]),
    dict(id="tee-leaf-black", name="Oversized Leaf Tee", cat="tees", img="tee-leaf-black.webp",
         sizes=TOP, colors=["Black"], tags=["best"]),
    dict(id="tee-washed-black", name="Washed Black Leaf Tee", cat="tees", img="tee-washed-black.webp",
         sizes=TOP, colors=["Washed black"], tags=["best", "new"]),
    dict(id="tee-longsleeve", name="Long Sleeve Leaf Tee", cat="tees", img="tee-longsleeve.webp",
         sizes=TOP, colors=["Black"], tags=[]),
    dict(id="tee-jersey", name="420 Jersey Tee", cat="tees", img="tee-jersey.webp",
         sizes=TOP, colors=["Cream"], tags=["new"]),
    dict(id="tee-tank", name="Leaf Tank Top", cat="tees", img="tee-tank.webp",
         sizes=TOP, colors=["Black"], tags=[]),

    # lowers
    dict(id="lower-cargo-black", name="Embroidered Cargo Pants", cat="lowers", img="lower-cargo-black.webp",
         sizes=WAIST, colors=["Black"], tags=["best", "new"]),
    dict(id="lower-cargo-olive", name="Olive Baggy Cargos", cat="lowers", img="lower-cargo-olive.webp",
         sizes=WAIST, colors=["Olive"], tags=["best"]),
    dict(id="lower-flame-pants", name="Flame Wide-Leg Pants", cat="lowers", img="lower-flame-pants.webp",
         sizes=WAIST, colors=["Black"], tags=["best"]),
    dict(id="lower-denim-print", name="Leaf Print Baggy Denim", cat="lowers", img="lower-denim-print.webp",
         sizes=WAIST, colors=["Washed black"], tags=["best"]),
    dict(id="lower-sweatpants", name="Olive Sweatpants", cat="lowers", img="lower-sweatpants.webp",
         sizes=TOP, colors=["Olive"], tags=[]),
    dict(id="lower-shorts", name="Leaf Baggy Shorts", cat="lowers", img="lower-shorts.webp",
         sizes=TOP, colors=["Black"], tags=["new"]),

    # jackets
    dict(id="jacket-varsity", name="Drugy Varsity Jacket", cat="jackets", img="jacket-varsity.webp",
         sizes=TOP, colors=["Black / Cream"], tags=["new"]),
    dict(id="jacket-windbreaker", name="Leaf Windbreaker", cat="jackets", img="jacket-windbreaker.webp",
         sizes=TOP, colors=["Black / Green"], tags=[]),
    dict(id="jacket-washed-zip", name="Washed Zip Jacket", cat="jackets", img="jacket-washed-zip.webp",
         sizes=TOP, colors=["Washed black"], tags=[]),

    # accessories
    dict(id="acc-cap", name="Leaf Logo Cap", cat="accessories", img="acc-cap.webp",
         sizes=FREE, colors=["Black"], tags=[]),
    dict(id="acc-bucket", name="Leaf Bucket Hat", cat="accessories", img="acc-bucket.webp",
         sizes=FREE, colors=["Black"], tags=[]),
    dict(id="acc-beanie", name="Embroidered Beanie", cat="accessories", img="acc-beanie.webp",
         sizes=FREE, colors=["Black"], tags=[]),
    dict(id="acc-socks", name="Leaf Socks (3 pairs)", cat="accessories", img="acc-socks.webp",
         sizes=FREE, colors=["Black / White"], tags=[]),
]

for _p in PRODUCTS:
    _p.setdefault("price", PRICE[_p["cat"]])
