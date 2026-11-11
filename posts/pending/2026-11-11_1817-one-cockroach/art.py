"""A patched wall that keeps cracking: in a difficult business, one fix begets the next problem.
Returns SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"

def crack(out, rnd, x, y, ang, steps, width, alpha, tips):
    pts = [(x, y)]
    for i in range(steps):
        ang += rnd.uniform(-0.45, 0.45)
        seg = rnd.uniform(9, 16)
        x += seg * math.cos(ang); y += seg * math.sin(ang)
        pts.append((x, y))
        if i > 2 and rnd.random() < 0.18 and steps - i > 3:
            crack(out, rnd, x, y, ang + rnd.choice([-1, 1]) * rnd.uniform(0.6, 1.0),
                  (steps - i) // 2, width * 0.6, alpha * 0.7, tips)
    d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="{width:.2f}" '
               f'fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    tips.append((x, y, alpha))

def build():
    rnd = random.Random(1989)
    out = []
    ground = 430
    L, R, T = 140, 760, 70
    # wall courses (running bond)
    rows = 9
    h = (ground - T) / rows
    for r in range(rows + 1):
        y = T + r * h
        out.append(f'<line x1="{L}" y1="{y:.1f}" x2="{R}" y2="{y:.1f}" stroke="{GOLD}" stroke-opacity=".16" stroke-width="1"/>')
    for r in range(rows):
        y0 = T + r * h
        off = 0 if r % 2 == 0 else 38
        x = L + off + 76
        while x < R:
            out.append(f'<line x1="{x:.1f}" y1="{y0:.1f}" x2="{x:.1f}" y2="{y0+h:.1f}" stroke="{GOLD}" stroke-opacity=".12" stroke-width="1"/>')
            x += 76
    out.append(f'<rect x="{L}" y="{T}" width="{R-L}" height="{ground-T}" fill="none" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1"/>')
    # the patch: one problem, neatly solved
    px, py, ps = 450, 250, 56
    out.append(f'<rect x="{px-ps/2}" y="{py-ps/2}" width="{ps}" height="{ps}" fill="#0f0e0c" fill-opacity=".9" '
               f'stroke="{GOLD}" stroke-opacity=".95" stroke-width="1.6"/>')
    for i in range(1, 5):
        o = ps / 5 * i - ps / 2
        out.append(f'<line x1="{px+o-4:.1f}" y1="{py-ps/2-5:.1f}" x2="{px+o+4:.1f}" y2="{py-ps/2+5:.1f}" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.2"/>')
        out.append(f'<line x1="{px+o-4:.1f}" y1="{py+ps/2-5:.1f}" x2="{px+o+4:.1f}" y2="{py+ps/2+5:.1f}" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.2"/>')
    out.append(f'<path d="M{px-12},{py+2} l8,8 l16,-18" stroke="{GOLD}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    # new cracks surfacing from the patch's edges
    tips = []
    out.append(f'<g clip-path="url(#wall)">')
    starts = [(px + ps/2, py - 14, -0.35, 20, 0.85), (px - ps/2, py + 10, math.pi + 0.3, 19, 0.8),
              (px + 10, py + ps/2, 1.45, 12, 0.7), (px - 12, py - ps/2, -1.75, 12, 0.65),
              (px + ps/2, py + 18, 0.45, 15, 0.6), (px - ps/2, py - 18, math.pi - 0.5, 14, 0.55)]
    for sx, sy, a, n, al in starts:
        crack(out, rnd, sx, sy, a, n, 1.6, al, tips)
    out.append('</g>')
    for tx, ty, al in tips:
        if L + 8 < tx < R - 8 and T + 8 < ty < ground - 8:
            out.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="2.2" fill="{GOLD}" fill-opacity="{min(1, al+0.2):.2f}"/>')
    out.append(f'<circle cx="{px}" cy="{py}" r="120" fill="url(#glow)"/>')
    # ground
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    for tx, lab in [(px, "ONE FIX"), ]:
        out.append(f'<line x1="{tx}" y1="{ground+6}" x2="{tx}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><clipPath id="wall"><rect x="{L}" y="{T}" width="{R-L}" height="{ground-T}"/></clipPath><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".18"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
