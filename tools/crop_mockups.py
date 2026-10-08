"""Cuts product and lifestyle photos out of the mockup sheets in images/source/.

Run:   python tools/crop_mockups.py
Product photos -> images/products/  (4:5, centred on a matching background)
Big photos     -> images/stock/

Boxes are (left, top, right, bottom) in pixels of the 1254 x 1254 sheets.
"""
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "images" / "source"

SHEETS = {
    "cs": "collection-sheet.webp",   # 30-item grid
    "os": "outfits-sheet.webp",      # 6 outfits, flat-lays, details
    "ts": "tee-sheet.webp",          # washed tee front/back + details
}

# collection sheet grid: column lefts and row (top, bottom)
CS_X = [12, 219, 424, 629, 834, 1039]
CS_Y = [(141, 377), (416, 630), (668, 838), (873, 1024), (1062, 1212)]


def cs(col, row):
    x, (t, b) = CS_X[col - 1], CS_Y[row - 1]
    return ("cs", (x + 2, t + 2, x + 199, b - 2))


# outfit sheet: column lefts/rights of the six lifestyle photos
OS_X = [(9, 211), (218, 417), (425, 623), (631, 830), (838, 1035), (1043, 1244)]


def outfit(n):
    l, r = OS_X[n - 1]
    return ("os", (l + 2, 180, r - 2, 658))


PRODUCTS = {
    # hoodies
    "hoodie-front-leaf": cs(1, 1),
    "hoodie-back-print": cs(2, 1),
    "hoodie-zip-olive": cs(6, 1),
    "hoodie-forest": ("os", (232, 698, 402, 864)),
    # tees
    "tee-heritage": ("ts", (0, 60, 630, 812)),
    "tee-heritage-back": ("ts", (624, 60, 1254, 812)),
    "tee-graphic-back": cs(3, 1),
    "tee-leaf-black": cs(4, 1),
    "tee-washed-black": ("os", (12, 700, 210, 864)),
    "tee-longsleeve": cs(5, 1),
    "tee-jersey": cs(2, 2),
    "tee-tank": cs(1, 2),
    # lowers
    "lower-cargo-black": cs(3, 2),
    "lower-sweatpants": cs(4, 2),
    "lower-denim-print": cs(5, 2),
    "lower-shorts": cs(6, 2),
    "lower-cargo-olive": ("os", (248, 860, 392, 1042)),
    "lower-flame-pants": ("os", (648, 864, 806, 1042)),
    # jackets
    "jacket-windbreaker": cs(1, 3),
    "jacket-varsity": cs(2, 3),
    "jacket-washed-zip": ("os", (850, 700, 1026, 864)),
    # accessories
    "acc-beanie": cs(3, 3),
    "acc-bucket": cs(4, 3),
    "acc-cap": cs(5, 3),
    "acc-socks": cs(5, 4),
}

STOCK = {
    "outfit-1": outfit(1), "outfit-2": outfit(2), "outfit-3": outfit(3),
    "outfit-4": outfit(4), "outfit-5": outfit(5), "outfit-6": outfit(6),
    "tee-front-big": ("ts", (0, 40, 630, 812)),
    "tee-back-big": ("ts", (624, 40, 1254, 812)),
    "detail-neck": ("ts", (18, 842, 428, 1238)),
    "detail-sleeve": ("ts", (444, 842, 754, 1238)),
    "detail-print": ("ts", (772, 842, 1238, 1238)),
    "detail-label": cs(1, 5),
    "detail-stitch": cs(2, 5),
    "detail-print-2": cs(3, 5),
    "look-hoodie": cs(4, 5),
    "look-cap": cs(5, 5),
    "brand-logo": ("cs", (555, 4, 695, 140)),
}


def edge_colour(im):
    """Average colour of the crop's border, used to pad it out to 4:5."""
    w, h = im.size
    px = [im.getpixel((x, y)) for x in range(0, w, 4) for y in (0, h - 1)]
    px += [im.getpixel((x, y)) for y in range(0, h, 4) for x in (0, w - 1)]
    return tuple(sorted(p[i] for p in px)[len(px) // 2] for i in range(3))


def sharpen_up(im, width):
    h = round(im.height * width / im.width)
    big = im.resize((width, h), Image.LANCZOS)
    return big.filter(ImageFilter.UnsharpMask(radius=1.4, percent=70, threshold=2))


def main():
    sheets = {k: Image.open(SRC / v).convert("RGB") for k, v in SHEETS.items()}
    out = ROOT / "images" / "products"
    out.mkdir(parents=True, exist_ok=True)
    for name, (sheet, box) in PRODUCTS.items():
        im = sheets[sheet].crop(box)
        w, h = im.size
        cw, ch = (w, round(w * 5 / 4)) if h < w * 5 / 4 else (round(h * 4 / 5), h)
        canvas = Image.new("RGB", (cw, ch), edge_colour(im))
        canvas.paste(im, ((cw - w) // 2, (ch - h) // 2))
        sharpen_up(canvas, 600).save(out / f"{name}.webp", quality=84)
        print("product", name, im.size)

    out = ROOT / "images" / "stock"
    out.mkdir(parents=True, exist_ok=True)
    for name, (sheet, box) in STOCK.items():
        im = sheets[sheet].crop(box)
        sharpen_up(im, max(600, im.width * 2) if im.width < 400 else im.width).save(out / f"{name}.webp", quality=84)
        print("stock", name, im.size)


if __name__ == "__main__":
    main()
