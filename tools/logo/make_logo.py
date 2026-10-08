"""Draws the Drugy Drip logos as SVG files.

Run:   python tools/logo/make_logo.py
Output: images/logo/*.svg

Colours live in SCHEMES. Letters come from the fonts in tools/logo/fonts
and are turned into shapes, so the SVGs look the same on every computer.
"""
import math
import random
from pathlib import Path

from fontTools.misc.transform import Transform
from fontTools.pens.basePen import BasePen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "images" / "logo"

SCHEMES = {
    # name: background, leaf, text, outline, shadow
    "og-green":    dict(bg="#0b0b0b", leaf="#49f23a", text="#ffffff", outline="#0b0b0b", shadow="#1f8a17"),
    "purple-haze": dict(bg="#140a22", leaf="#9d4dff", text="#d7ff3a", outline="#140a22", shadow="#ff3ea5"),
    "toxic":       dict(bg="#0b0b0b", leaf="#1d5e26", text="#4dff3a", outline="#0b0b0b", shadow="#ffffff"),
    "graffiti":    dict(bg="#0b0b0b", leaf="#49f23a", text="#ffffff", outline="#0b0b0b", shadow="#ff2d95"),
    "light":       dict(bg="#f3eee4", leaf="#2e7d32", text="#111111", outline="#f3eee4", shadow="#111111"),
}


def num(v):
    """Short number for SVG text: 12.0 -> 12, 3.14159 -> 3.1"""
    return f"{v:.1f}".rstrip("0").rstrip(".")


# ---------------------------------------------------------------- letters

class PointsPen(BasePen):
    """Collects points along a glyph's outline (used to find where drips can hang)."""

    def __init__(self):
        super().__init__(None)
        self.pts = []

    def _moveTo(self, p):
        self.start = p
        self.pts.append(p)

    def _closePath(self):
        # the closing edge back to the start is often a letter's flat bottom
        if self._getCurrentPoint() != self.start:
            self._lineTo(self.start)

    def _lineTo(self, p):
        x0, y0 = self._getCurrentPoint()
        n = max(2, int(math.dist((x0, y0), p) / 2))
        self.pts += [(x0 + (p[0] - x0) * i / n, y0 + (p[1] - y0) * i / n) for i in range(1, n + 1)]

    def _curveToOne(self, p1, p2, p3):
        p0 = self._getCurrentPoint()
        for i in range(1, 17):
            t = i / 16
            u = 1 - t
            self.pts.append(tuple(u**3 * a + 3 * u * u * t * b + 3 * u * t * t * c + t**3 * d
                                  for a, b, c, d in zip(p0, p1, p2, p3)))

    def _qCurveToOne(self, p1, p2):
        p0 = self._getCurrentPoint()
        for i in range(1, 17):
            t = i / 16
            u = 1 - t
            self.pts.append(tuple(u * u * a + 2 * u * t * b + t * t * c for a, b, c in zip(p0, p1, p2)))


class Font:
    def __init__(self, file):
        self.tt = TTFont(HERE / "fonts" / file)
        self.glyphs = self.tt.getGlyphSet()
        self.cmap = self.tt.getBestCmap()
        self.upm = self.tt["head"].unitsPerEm

    def line(self, text, size, cx, baseline, track=0.0, wobble=0.0, rng=None):
        """Lays out one line of text centred on cx. Returns one dict per letter.

        track:  extra space between letters (in em, can be negative)
        wobble: how much each letter bounces and tilts (0 = straight)
        """
        s = size / self.upm
        names = [self.cmap[ord(ch)] for ch in text]
        advances = [self.tt["hmtx"][n][0] * s + track * size for n in names]
        x = cx - (sum(advances) - track * size) / 2
        letters = []
        for ch, name, adv in zip(text, names, advances):
            if ch != " ":
                t = Transform(s, 0, 0, -s, x, baseline)
                if wobble:
                    pivot = (x + adv / 2, baseline - size * 0.35)
                    angle = math.radians(rng.uniform(-6, 6) * wobble)
                    lift = rng.uniform(-0.05, 0.05) * size * wobble
                    t = (Transform().translate(pivot[0], pivot[1] + lift).rotate(angle)
                         .translate(-pivot[0], -pivot[1]).transform(t))
                path = SVGPathPen(self.glyphs, ntos=num)
                self.glyphs[name].draw(TransformPen(path, t))
                pts = PointsPen()
                self.glyphs[name].draw(TransformPen(pts, t))
                letters.append(dict(ch=ch, d=path.getCommands(), pts=pts.pts))
            x += adv
        return letters


def bottom_at(letter, x, window):
    """Lowest point of a letter near x (SVG y grows downwards)."""
    ys = [py for px, py in letter["pts"] if abs(px - x) <= window]
    return max(ys) if ys else None


def drips(letters, size, rng, chance=0.85, longest=0.5, widths=(0.09, 0.12), margin=0.035, shortest=0.1):
    """Paint drips hanging from the flat bottoms of the letters."""
    shapes = []
    for letter in letters:
        bottom = max(py for _, py in letter["pts"])
        feet = sorted(px for px, py in letter["pts"] if py >= bottom - size * 0.045)
        groups, start = [], feet[0]
        for a, b in zip(feet, feet[1:]):
            if b - a > size * 0.05:
                groups.append((start, a))
                start = b
        groups.append((start, feet[-1]))

        for a, b in groups:
            w = rng.uniform(*widths) * size
            m = size * margin                               # keep clear of the letter's rounded corners
            # flare where the drip leaves the letter; it must stay on the flat foot
            f = min(w * 0.45, (b - a - w - 2 * m) / 2)
            if f < w * 0.15 or rng.random() > chance:
                continue
            lo, hi = a + m + w / 2 + f, b - m - w / 2 - f
            cx = rng.uniform(lo, hi) if hi > lo else (a + b) / 2
            xl, xr = cx - w / 2 - f, cx + w / 2 + f
            yl = bottom_at(letter, xl, size * 0.015) or bottom
            yr = bottom_at(letter, xr, size * 0.015) or bottom
            yb = bottom_at(letter, cx, w / 2) or bottom
            top = min(yl, yr) - size * 0.06                # hidden inside the letter
            length = rng.uniform(shortest, longest) * size
            tip = yb + length
            r = w * 0.56
            neck = w * 0.46                                # drips get a bit thinner before the drop
            shapes.append(
                f'<path d="M{num(cx - w/4)} {num(top)}L{num(xl)} {num(yl)}'
                f'Q{num(cx - w/2)} {num(yl)} {num(cx - w/2)} {num(yl + f)}'
                f'L{num(cx - neck)} {num(tip)}L{num(cx + neck)} {num(tip)}'
                f'L{num(cx + w/2)} {num(yr + f)}Q{num(cx + w/2)} {num(yr)} {num(xr)} {num(yr)}'
                f'L{num(cx + w/4)} {num(top)}Z"/>'
                f'<circle cx="{num(cx)}" cy="{num(tip)}" r="{num(r)}"/>'
            )
            if rng.random() < 0.35:
                dr = w * 0.36
                shapes.append(f'<circle cx="{num(cx)}" cy="{num(tip + r + dr + rng.uniform(0.04, 0.1) * size)}" r="{num(dr)}"/>')
    return shapes


# ---------------------------------------------------------------- leaf

def leaflet(origin, angle, length, width, teeth=17):
    """One serrated leaflet. angle in degrees, 0 = straight up."""
    a = math.radians(angle)
    ux, uy = math.sin(a), -math.cos(a)          # along the leaflet
    vx, vy = -uy, ux                            # across the leaflet

    def half(t):                                # half-width: thin base, wide ~35%, sharp tip
        return width * (t ** 0.55) * (1 - t) / 0.365

    def pt(t, side):
        return (origin[0] + ux * length * t + vx * side,
                origin[1] + uy * length * t + vy * side)

    edge = [(0.0, 0.0)]
    t0, t1 = 0.1, 0.97
    step = (t1 - t0) / teeth
    for i in range(teeth):                      # each tooth: valley, bulge, sharp point toward the tip
        ta = t0 + i * step
        tm, tp = ta + step * 0.45, ta + step * 0.85
        edge += [(ta, half(ta) * 0.84), (tm, half(tm) * 1.05), (tp, half(tp) * 1.15)]
    edge.append((1.0, 0.0))

    left = [pt(t, -h) for t, h in edge]
    right = [pt(t, h) for t, h in reversed(edge)]
    outline = "M" + "L".join(f"{num(x)} {num(y)}" for x, y in left + right[1:]) + "Z"
    vein = (pt(0.04, 0), pt(0.86, 0))
    return outline, vein


def leaf(cx, cy, size, color, vein_color):
    """Seven-leaflet leaf. (cx, cy) is where the leaflets meet, size = centre leaflet length."""
    parts, veins = [], []
    for angle, scale in [(-98, 0.42), (98, 0.42), (-58, 0.68), (58, 0.68), (-28, 0.88), (28, 0.88), (0, 1.0)]:
        outline, vein = leaflet((cx, cy), angle, size * scale, size * scale * 0.115)
        parts.append(f'<path d="{outline}"/>')
        veins.append(f'<path d="M{num(vein[0][0])} {num(vein[0][1])}L{num(vein[1][0])} {num(vein[1][1])}"/>')
    stem_w = size * 0.035
    stem = (f'<path d="M{num(cx - stem_w)} {num(cy - stem_w)}Q{num(cx - stem_w * 0.4)} {num(cy + size * 0.22)} '
            f'{num(cx + size * 0.05)} {num(cy + size * 0.42)}L{num(cx + size * 0.07)} {num(cy + size * 0.41)}'
            f'Q{num(cx + stem_w * 0.6)} {num(cy + size * 0.2)} {num(cx + stem_w)} {num(cy - stem_w)}Z"/>')
    return (f'<g fill="{color}">{stem}{"".join(parts)}</g>'
            f'<g fill="none" stroke="{vein_color}" stroke-width="{num(size * 0.012)}" stroke-linecap="round">'
            f'{"".join(veins)}</g>')


# ---------------------------------------------------------------- logo

def lettering(shapes, c, outline_w, shadow=(0, 0)):
    """Shadow, then thick outline, then fill, so overlapping shapes merge into one sticker."""
    body = "".join(shapes)
    out = []
    if shadow != (0, 0):
        out.append(f'<g transform="translate({num(shadow[0])} {num(shadow[1])})" fill="{c["shadow"]}" '
                   f'stroke="{c["shadow"]}" stroke-width="{num(outline_w)}" stroke-linejoin="round">{body}</g>')
    out.append(f'<g fill="{c["outline"]}" stroke="{c["outline"]}" stroke-width="{num(outline_w)}" '
               f'stroke-linejoin="round">{body}</g>')
    out.append(f'<g fill="{c["text"]}">{body}</g>')
    return "".join(out)


def svg(w, h, body, bg=None, title="Drugy Drip"):
    back = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<title>{title}</title>{back}{body}</svg>\n')


def square_logo(scheme, font_file="TitanOne-Regular.ttf", seed=7, wobble=0.6, track=-0.02):
    c = SCHEMES[scheme]
    font = Font(font_file)
    rng = random.Random(seed)
    top = font.line("DRUGY", 165, 500, 665, track=track, wobble=wobble, rng=rng)
    bottom = font.line("DRIP", 225, 500, 855, track=track, wobble=wobble, rng=rng)
    shapes = [f'<path d="{l["d"]}"/>' for l in top + bottom] + drips(bottom, 225, rng, longest=0.4)
    body = leaf(500, 590, 540, c["leaf"], c["bg"]) + lettering(shapes, c, 34, shadow=(12, 12))
    return svg(1000, 1000, body, c["bg"])


def wordmark(scheme, transparent=False, seed=11):
    """Long one-line logo without the leaf (for ads, tags and the website header)."""
    c = SCHEMES[scheme]
    font = Font("TitanOne-Regular.ttf")
    rng = random.Random(seed)
    letters = font.line("DRUGY DRIP", 200, 800, 230, track=-0.02, wobble=0.5, rng=rng)
    shapes = [f'<path d="{l["d"]}"/>' for l in letters] + drips(letters, 200, rng, chance=0.7, longest=0.45)
    return svg(1600, 420, lettering(shapes, c, 26, shadow=(9, 9)), None if transparent else c["bg"])


def icon(scheme):
    """Small square mark: leaf with DD on it (favicon, profile picture)."""
    c = SCHEMES[scheme]
    font = Font("TitanOne-Regular.ttf")
    rng = random.Random(3)
    letters = font.line("DD", 40, 50, 80, track=-0.06)
    shapes = [f'<path d="{l["d"]}"/>' for l in letters] + drips(letters, 40, rng, chance=1, longest=0.25)
    body = (f'<rect width="100" height="100" rx="22" fill="{c["bg"]}"/>' + leaf(50, 62, 52, c["leaf"], c["bg"])
            + lettering(shapes, c, 7, shadow=(2.5, 2.5)))
    return svg(100, 100, body)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = {
        "drugydrip-og-green.svg": square_logo("og-green"),
        "drugydrip-purple-haze.svg": square_logo("purple-haze"),
        "drugydrip-toxic.svg": square_logo("toxic"),
        "drugydrip-graffiti.svg": square_logo("graffiti", "SedgwickAveDisplay-Regular.ttf", seed=4, wobble=0.3, track=0.0),
        "drugydrip-light.svg": square_logo("light"),
        "drugydrip-wordmark.svg": wordmark("og-green"),
        "drugydrip-wordmark-transparent.svg": wordmark("og-green", transparent=True),
        "drugydrip-icon.svg": icon("og-green"),
    }
    for name, text in files.items():
        (OUT / name).write_text(text, encoding="utf-8")
        print(f"wrote images/logo/{name}  ({len(text) // 1024} KB)")


if __name__ == "__main__":
    main()
