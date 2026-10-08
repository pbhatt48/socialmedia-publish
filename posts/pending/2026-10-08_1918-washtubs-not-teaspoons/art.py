"""Dark clouds raining gold onto a washtub beside a teaspoon. Returns SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"


def cloud(out, x0, base, bumps, alpha):
    """Cloud outline: flat base with a run of rounded bumps over the top.
    bumps are (end_x, lift) pairs; lift raises the bump's end point above the base."""
    d = f"M{x0},{base}"
    px, py = x0, base
    for i, (x, lift) in enumerate(bumps):
        y = base if i == len(bumps) - 1 else base - lift
        r = math.hypot(x - px, y - py) * 0.56
        d += f" A{r:.1f},{r:.1f} 0 1 1 {x},{y}"
        px, py = x, y
    d += " Z"
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="1.2" '
               f'fill="{GOLD}" fill-opacity=".05" stroke-linejoin="round"/>')


def build():
    out = []
    rnd = random.Random(16)
    ground = 440
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # gold rain: short falling strokes and small drops, densest under the clouds
    for _ in range(140):
        x = rnd.uniform(265, 680)
        y = rnd.uniform(165, 395)
        l = rnd.uniform(8, 18)
        if 305 < x < 495 and y + l > 365:
            continue
        if y + l > 420:
            continue
        a = rnd.uniform(0.25, 0.85)
        out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x-2:.1f}" y2="{y+l:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity="{a:.2f}" stroke-width="1.2" stroke-linecap="round"/>')
    for _ in range(26):
        x = rnd.uniform(270, 670)
        y = rnd.uniform(175, 360)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(1.6,2.8):.1f}" fill="{GOLD}" fill-opacity="{rnd.uniform(.5,.95):.2f}"/>')

    cloud(out, 262, 150, [(318, 22), (392, 30), (446, 16), (472, 0)], 0.8)
    cloud(out, 486, 132, [(530, 18), (606, 34), (664, 20), (694, 0)], 0.6)

    # washtub (left of centre), brimming
    tx, tw, th = 400, 170, 62
    top = ground - th
    out.append(f'<path d="M{tx-tw/2},{top} L{tx-tw/2+16},{ground-2} L{tx+tw/2-16},{ground-2} L{tx+tw/2},{top}" '
               f'stroke="{GOLD}" stroke-width="2" fill="none" stroke-linejoin="round"/>')
    out.append(f'<ellipse cx="{tx}" cy="{top}" rx="{tw/2}" ry="9" stroke="{GOLD}" stroke-width="2" fill="{GOLD}" fill-opacity=".28"/>')
    for k in (0.33, 0.66):
        y = top + th * k
        inset = 16 * k
        out.append(f'<line x1="{tx-tw/2+inset+2:.1f}" y1="{y:.1f}" x2="{tx+tw/2-inset-2:.1f}" y2="{y:.1f}" '
                   f'stroke="{GOLD}" stroke-opacity=".35" stroke-width="1"/>')
    for side in (-1, 1):
        hx = tx + side * (tw / 2 + 2)
        out.append(f'<path d="M{hx},{top+8} q{side*14},6 0,18" stroke="{GOLD}" stroke-width="1.6" fill="none"/>')

    # teaspoon (right), nearly empty
    sx, sy = 560, ground - 6
    out.append(f'<ellipse cx="{sx}" cy="{sy}" rx="13" ry="6" stroke="{GOLD}" stroke-width="1.6" fill="none"/>')
    out.append(f'<path d="M{sx+12},{sy-2} L{sx+70},{sy-12}" stroke="{GOLD}" stroke-width="2" stroke-linecap="round"/>')

    for x, lab in ((tx, "WASHTUB"), (sx + 28, "TEASPOON")):
        out.append(f'<text x="{x}" y="{ground+36}" text-anchor="middle" font-family="Inter" font-size="12" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    return "".join(out)
