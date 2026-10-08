"""Draws the realistic Drugy Drip logos (shaded leaf, metal letters).

Run:   python tools/logo/make_logo_real.py
Output: images/logo/drugydrip-real-*.svg

The flat/cartoon versions are in make_logo.py; this file reuses its
letter and drip helpers.
"""
import math
import random

from make_logo import OUT, Font, drips, num, svg

# Metal colours, top to bottom of each line of letters
METALS = {
    "chrome": [(0, "#ffffff"), (.38, "#c9d0d8"), (.5, "#3e4650"), (.53, "#8c96a1"), (.78, "#eef1f4"), (1, "#8f99a4")],
    "gold":   [(0, "#fff6cc"), (.38, "#e6bb55"), (.5, "#6e4a0e"), (.54, "#b8862e"), (.8, "#ffe28e"), (1, "#9c6b1b")],
    "silver-white": [(0, "#ffffff"), (.6, "#eceff1"), (1, "#b9c0c6")],
}

LEAF = dict(dark="#13651c", light="#2fb33a", rib="#d4f5a6", vein="#a8f07a", edge="#0a3a10")

FILTERS = """
<filter id="leafbevel" x="-5%" y="-5%" width="110%" height="110%">
  <feGaussianBlur in="SourceAlpha" stdDeviation="2" result="b"/>
  <feSpecularLighting in="b" surfaceScale="3" specularConstant=".6" specularExponent="30" lighting-color="#eaffd8" result="s">
    <feDistantLight azimuth="235" elevation="50"/>
  </feSpecularLighting>
  <feComposite in="s" in2="SourceAlpha" operator="in" result="s2"/>
  <feComposite in="SourceGraphic" in2="s2" operator="arithmetic" k1="0" k2="1" k3=".3" k4="0"/>
</filter>
<filter id="bevel" x="-5%" y="-5%" width="110%" height="110%">
  <feGaussianBlur in="SourceAlpha" stdDeviation="{blur}" result="b"/>
  <feSpecularLighting in="b" surfaceScale="{depth}" specularConstant=".85" specularExponent="22" lighting-color="#fff" result="s">
    <feDistantLight azimuth="235" elevation="42"/>
  </feSpecularLighting>
  <feComposite in="s" in2="SourceAlpha" operator="in" result="s2"/>
  <feComposite in="SourceGraphic" in2="s2" operator="arithmetic" k1="0" k2="1" k3=".75" k4="0"/>
</filter>
<filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
  <feGaussianBlur in="SourceAlpha" stdDeviation="14"/>
  <feOffset dx="0" dy="14"/>
  <feComponentTransfer><feFuncA type="linear" slope=".75"/></feComponentTransfer>
  <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<radialGradient id="bg" cx="50%" cy="45%" r="70%">
  <stop offset="0" stop-color="#1c1f1c"/><stop offset="1" stop-color="#050505"/>
</radialGradient>
<radialGradient id="leafshade" gradientUnits="userSpaceOnUse" cx="{lx}" cy="{ly}" r="{lr}">
  <stop offset="0" stop-color="#000" stop-opacity=".55"/>
  <stop offset=".45" stop-color="#000" stop-opacity=".12"/>
  <stop offset="1" stop-color="#000" stop-opacity="0"/>
</radialGradient>
"""


# ---------------------------------------------------------------- leaf

def leaflet(origin, angle, length, width, bend, teeth=28):
    """A curved leaflet split into a dark and a light half along the midrib."""
    a = math.radians(angle)
    ux, uy = math.sin(a), -math.cos(a)
    vx, vy = -uy, ux

    def axis(t):
        k = bend * length * t * t
        return origin[0] + ux * length * t + vx * k, origin[1] + uy * length * t + vy * k

    def normal(t):
        dx, dy = ux + vx * 2 * bend * t, uy + vy * 2 * bend * t
        d = math.hypot(dx, dy)
        return -dy / d, dx / d

    def half(t):
        return width * (t ** 0.5) * (1 - t) ** 1.1 / 0.37

    def edge_pt(t, h):
        (x, y), (nx, ny) = axis(t), normal(t)
        return x + nx * h, y + ny * h

    edge = [(0.0, 0.0)]
    t0, t1 = 0.07, 0.975
    step = (t1 - t0) / teeth
    for i in range(teeth):
        ta = t0 + i * step
        tm, tp = ta + step * 0.5, ta + step * 0.92
        edge += [(ta, half(ta) * 0.9), (tm, half(tm) * 1.02), (tp, half(tp) * 1.1)]
    edge.append((1.0, 0.0))

    rib = [axis(t) for t, _ in edge]
    left = [edge_pt(t, -h) for t, h in edge]
    right = [edge_pt(t, h) for t, h in edge]

    def poly(pts):
        return "M" + "L".join(f"{num(x)} {num(y)}" for x, y in pts) + "Z"

    left_half = poly(left + rib[::-1])
    right_half = poly(right + rib[::-1])
    outline = poly(left + right[::-1])

    # midrib: thin wedge that narrows toward the tip
    mw = width * 0.09
    rib_l = [edge_pt(t, -mw * (1 - t)) for t in [i / 30 * 0.94 for i in range(31)]]
    rib_r = [edge_pt(t, mw * (1 - t)) for t in [i / 30 * 0.94 for i in range(31)]]
    midrib = poly(rib_l + rib_r[::-1])

    veins = []
    t = 0.1
    while t < 0.86:
        for side in (-1, 1):
            x0, y0 = axis(t)
            x1, y1 = edge_pt(t + 0.075, side * half(t + 0.075) * 0.82)
            veins.append(f"M{num(x0)} {num(y0)}L{num(x1)} {num(y1)}")
        t += 0.055
    return dict(left=left_half, right=right_half, outline=outline, midrib=midrib, veins="".join(veins))


def real_leaf(cx, cy, size):
    """Nine leaflets, the lower ones drawn first so the upper ones overlap them."""
    spec = [(-112, .3), (112, .3), (-84, .58), (84, .58), (-54, .7), (54, .7), (-26, .88), (26, .88), (0, 1.0)]
    clip, body = [], []
    vein_w = size * 0.0035
    for angle, scale in spec:
        bend = 0.0 if angle == 0 else -math.copysign(0.07, angle)
        lf = leaflet((cx, cy), angle, size * scale, size * scale * 0.11, bend)
        # light comes from the top left, so the half facing it is brighter
        lit_left = angle <= 0
        body.append(
            f'<path d="{lf["outline"]}" fill="{LEAF["edge"]}" stroke="{LEAF["edge"]}" stroke-width="{num(size * .006)}" stroke-linejoin="round"/>'
            f'<path d="{lf["left"]}" fill="{LEAF["light"] if lit_left else LEAF["dark"]}"/>'
            f'<path d="{lf["right"]}" fill="{LEAF["dark"] if lit_left else LEAF["light"]}"/>'
            f'<path d="{lf["veins"]}" fill="none" stroke="{LEAF["vein"]}" stroke-opacity=".45" stroke-width="{num(vein_w)}" stroke-linecap="round"/>'
            f'<path d="{lf["midrib"]}" fill="{LEAF["rib"]}"/>'
        )
        clip.append(f'<path d="{lf["outline"]}"/>')
    sw = size * 0.03
    stem = (f'<path d="M{num(cx - sw)} {num(cy - sw)}Q{num(cx - sw * .3)} {num(cy + size * .25)} {num(cx + size * .06)} {num(cy + size * .45)}'
            f'L{num(cx + size * .085)} {num(cy + size * .44)}Q{num(cx + sw * .8)} {num(cy + size * .22)} {num(cx + sw)} {num(cy - sw)}Z" '
            f'fill="{LEAF["dark"]}" stroke="{LEAF["edge"]}" stroke-width="{num(size * .006)}"/>')
    return (f'<clipPath id="leafclip">{"".join(clip)}</clipPath>'
            f'<g filter="url(#shadow)"><g filter="url(#leafbevel)">{stem}{"".join(body)}</g></g>'
            f'<rect width="100%" height="100%" fill="url(#leafshade)" clip-path="url(#leafclip)"/>')


# ---------------------------------------------------------------- letters

def gradient(gid, stops, y0, y1):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="0" y1="{num(y0)}" x2="0" y2="{num(y1)}">{s}</linearGradient>'


def metal_text(lines, metal, rim, rng, longest=0.36):
    """lines: [(font, text, size, baseline, has_drips)]. Returns (defs, body)."""
    defs, layers = [], []
    for i, (font, text, size, baseline, has_drips) in enumerate(lines):
        letters = font.line(text, size, 500, baseline, track=0.01)
        shapes = [f'<path d="{l["d"]}"/>' for l in letters]
        if has_drips:
            shapes += drips(letters, size, rng, chance=1, longest=longest, shortest=0.17, widths=(0.065, 0.085), margin=0.015)
        top = min(py for l in letters for _, py in l["pts"])
        defs.append(gradient(f"metal{i}", METALS[metal], top, baseline))
        layers.append(("".join(shapes), f"metal{i}", size))

    outline = "".join(f'<g stroke-width="{num(s * .16)}">{b}</g>' for b, _, s in layers)
    rim_layer = "".join(f'<g stroke-width="{num(s * .07)}">{b}</g>' for b, _, s in layers)
    fill = "".join(f'<g fill="url(#{g})">{b}</g>' for b, g, _ in layers)
    body = (f'<g filter="url(#shadow)" fill="#0a0a0a" stroke="#0a0a0a" stroke-linejoin="round">{outline}</g>'
            f'<g fill="{rim}" stroke="{rim}" stroke-linejoin="round">{rim_layer}</g>'
            f'<g filter="url(#bevel)">{fill}</g>')
    return "".join(defs), body


def real_logo(metal, title_font, rim, upper=True, seed=5):
    rng = random.Random(seed)
    font = Font(title_font)
    if upper:
        lines = [(font, "DRUGY", 175, 668, False), (font, "DRIP", 235, 872, True)]
    else:
        lines = [(font, "Drugy", 200, 640, False), (font, "Drip", 250, 880, True)]
    tdefs, text = metal_text(lines, metal, rim, rng, 0.36 if upper else 0.3)
    leaf_c, leaf_size = (500, 600), 520
    defs = (FILTERS.format(blur=3, depth=4, lx=leaf_c[0], ly=leaf_c[1], lr=leaf_size * .75) + tdefs)
    body = (f'<defs>{defs}</defs><rect width="1000" height="1000" fill="url(#bg)"/>'
            + real_leaf(*leaf_c, leaf_size) + text)
    return svg(1000, 1000, body)


def main():
    files = {
        "drugydrip-real-chrome.svg": real_logo("chrome", "Anton-Regular.ttf", "#49f23a"),
        "drugydrip-real-gold.svg": real_logo("gold", "Anton-Regular.ttf", "#0f3d14"),
        "drugydrip-real-gothic.svg": real_logo("silver-white", "UnifrakturCook-Bold.ttf", "#49f23a", upper=False),
    }
    for name, text in files.items():
        (OUT / name).write_text(text, encoding="utf-8")
        print(f"wrote images/logo/{name}  ({len(text) // 1024} KB)")


if __name__ == "__main__":
    main()
