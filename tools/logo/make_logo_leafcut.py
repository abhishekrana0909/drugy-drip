"""Draws the "leaf-cut" Drugy Drip logos: letters filled with real-looking leaves,
as if the words were cut out of a pile of leaves.

Run:   python tools/logo/make_logo_leafcut.py
Output: images/logo/drugydrip-leafcut-*.svg
"""
import random

from make_logo import OUT, Font, drips, num, svg
from make_logo_real import leaflet

# two leaf colourings so the pile doesn't look copy-pasted
LEAF_TONES = [
    dict(dark="#14621d", light="#2fae39", rib="#cdf29d", vein="#a6ee78", edge="#0a3a10"),
    dict(dark="#0f4f17", light="#23902c", rib="#b5e588", vein="#8fd966", edge="#082d0c"),
    dict(dark="#1d7424", light="#3cc246", rib="#dcf7b0", vein="#b6f58a", edge="#0c4012"),
]

DEFS = """
<radialGradient id="bg" cx="50%" cy="45%" r="70%">
  <stop offset="0" stop-color="#1c1f1c"/><stop offset="1" stop-color="#050505"/>
</radialGradient>
<filter id="bevel" x="-5%" y="-5%" width="110%" height="110%">
  <feGaussianBlur in="SourceAlpha" stdDeviation="3" result="b"/>
  <feSpecularLighting in="b" surfaceScale="5" specularConstant=".8" specularExponent="20" lighting-color="#f4ffe8" result="s">
    <feDistantLight azimuth="235" elevation="40"/>
  </feSpecularLighting>
  <feComposite in="s" in2="SourceAlpha" operator="in" result="s2"/>
  <feComposite in="SourceGraphic" in2="s2" operator="arithmetic" k1="0" k2="1" k3=".55" k4="0"/>
</filter>
<filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
  <feGaussianBlur in="SourceAlpha" stdDeviation="12"/>
  <feOffset dx="0" dy="12"/>
  <feComponentTransfer><feFuncA type="linear" slope=".8"/></feComponentTransfer>
</filter>
<linearGradient id="depth" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#fff" stop-opacity=".10"/>
  <stop offset=".55" stop-color="#000" stop-opacity="0"/>
  <stop offset="1" stop-color="#000" stop-opacity=".35"/>
</linearGradient>
"""


def leaf_symbol(sid, tone):
    """A small seven-leaflet leaf at (0, 0), centre leaflet 100 long, pointing up."""
    parts = []
    for angle, scale in [(-84, .45), (84, .45), (-54, .68), (54, .68), (-26, .88), (26, .88), (0, 1.0)]:
        bend = 0.0 if angle == 0 else (0.07 if angle < 0 else -0.07)
        lf = leaflet((0, 0), angle, 100 * scale, 100 * scale * 0.12, bend, teeth=16)
        lit_left = angle <= 0
        parts.append(
            f'<path d="{lf["outline"]}" fill="{tone["edge"]}" stroke="{tone["edge"]}" stroke-width="1.2" stroke-linejoin="round"/>'
            f'<path d="{lf["left"]}" fill="{tone["light"] if lit_left else tone["dark"]}"/>'
            f'<path d="{lf["right"]}" fill="{tone["dark"] if lit_left else tone["light"]}"/>'
            f'<path d="{lf["veins"]}" fill="none" stroke="{tone["vein"]}" stroke-opacity=".45" stroke-width=".7"/>'
            f'<path d="{lf["midrib"]}" fill="{tone["rib"]}"/>'
        )
    return f'<g id="{sid}">{"".join(parts)}</g>'


def leaf_pile(box, rng, step=50):
    """Leaves scattered over box=(x0, y0, x1, y1), overlapping at random angles."""
    x0, y0, x1, y1 = box
    uses = []
    y = y0 - step
    while y < y1 + step:
        x = x0 - step
        while x < x1 + step:
            px, py = x + rng.uniform(-step * .45, step * .45), y + rng.uniform(-step * .45, step * .45)
            uses.append(f'<use href="#lf{rng.randrange(len(LEAF_TONES))}" transform="translate({num(px)} {num(py)}) '
                        f'rotate({rng.randrange(360)}) scale({rng.uniform(1.0, 1.9):.2f})"/>')
            x += step
        y += step
    rng.shuffle(uses)
    return "".join(uses)


def measure(font, text, size):
    """Ink box of a line drawn at baseline 0: (width, top, bottom)."""
    pts = [p for l in font.line(text, size, 0, 0) for p in l["pts"]]
    xs, ys = [x for x, _ in pts], [y for _, y in pts]
    return max(xs) - min(xs), min(ys), max(ys)


def leafcut(lines, w, h, background=True, seed=9, gap=0.06, drip_room=0.22, drip_opts=None):
    """lines: [(font_file, text, ink_width, has_drips)], stacked and centred in a w x h canvas.

    gap: space between lines and drip_room: space kept for the drips, both as a share of h.
    """
    rng = random.Random(seed)
    sized = []
    for font_file, text, width, has_drips in lines:
        font = Font(font_file)
        iw, _, _ = measure(font, text, 100)
        size = 100 * width / iw
        _, top, bottom = measure(font, text, size)
        sized.append((font, text, size, top, bottom, has_drips))
    total = sum(b - t for *_, t, b, _ in sized) + gap * h * (len(sized) - 1) + drip_room * h
    y = (h - total) / 2

    shapes, sizes = [], []
    for font, text, size, top, bottom, has_drips in sized:
        baseline = y - top
        letters = font.line(text, size, w / 2, baseline, track=0.02)
        part = [f'<path d="{l["d"]}"/>' for l in letters]
        if has_drips:
            part += drips(letters, size, rng, **(dict(chance=1) | (drip_opts or {})))
        shapes.append("".join(part))
        sizes.append(size)
        y += bottom - top + gap * h

    edge = min(sizes)
    allshapes = "".join(shapes)
    defs = (DEFS + "".join(leaf_symbol(f"lf{i}", t) for i, t in enumerate(LEAF_TONES))
            + f'<clipPath id="txt">{allshapes}</clipPath>')
    body = (
        f'<defs>{defs}</defs>'
        + (f'<rect width="{w}" height="{h}" fill="url(#bg)"/>' if background else "")
        + f'<g filter="url(#shadow)" fill="#000" stroke="#000" stroke-width="{num(edge * .12)}" stroke-linejoin="round">{allshapes}</g>'
        + f'<g fill="#050805" stroke="#050805" stroke-width="{num(edge * .12)}" stroke-linejoin="round">{allshapes}</g>'
        + f'<g fill="#6fcf4f" stroke="#6fcf4f" stroke-width="{num(edge * .028)}" stroke-linejoin="round">{allshapes}</g>'
        + f'<g filter="url(#bevel)"><g clip-path="url(#txt)">'
        + f'<rect width="{w}" height="{h}" fill="#145a1c"/>{leaf_pile((0, 0, w, h), rng)}'
        + f'<rect width="{w}" height="{h}" fill="url(#depth)"/></g></g>'
    )
    return svg(w, h, body)


def main():
    heavy, tall = "BowlbyOneSC-Regular.ttf", "Anton-Regular.ttf"
    heavy_lines = [(heavy, "DRUGY", 840, False), (heavy, "DRIP", 700, True)]
    files = {
        "drugydrip-leafcut-heavy.svg": leafcut(heavy_lines, 1000, 1000, gap=0.05, drip_room=0.1, drip_opts=dict(longest=0.3, shortest=0.12)),
        "drugydrip-leafcut-tall.svg": leafcut(
            [(tall, "DRUGY", 700, False), (tall, "DRIP", 600, True)], 1000, 1000, gap=0.04, drip_room=0.14,
            drip_opts=dict(longest=0.3, shortest=0.12, widths=(0.06, 0.08), margin=0.015)),
        "drugydrip-leafcut-heavy-transparent.svg": leafcut(
            heavy_lines, 1000, 1000, background=False, gap=0.05, drip_room=0.1,
            drip_opts=dict(longest=0.3, shortest=0.12)),
        "drugydrip-leafcut-wordmark.svg": leafcut(
            [(heavy, "DRUGY DRIP", 1440, True)], 1600, 460, background=False, drip_room=0.3,
            drip_opts=dict(longest=0.35, shortest=0.12, chance=0.8)),
    }
    for name, text in files.items():
        (OUT / name).write_text(text, encoding="utf-8")
        print(f"wrote images/logo/{name}  ({len(text) // 1024} KB)")


if __name__ == "__main__":
    main()
