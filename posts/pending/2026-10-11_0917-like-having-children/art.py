"""A tended garden: a few well-cared-for plants under one arc of attention; beyond it, faint untended seedlings."""
import math, random

GOLD = "#c9a96a"

def plant(out, rnd, x, ground, h, alpha):
    top = ground - h
    sway = rnd.uniform(-8, 8)
    out.append(f'<path d="M{x},{ground} Q{x+sway:.1f},{ground-h*0.55:.1f} {x+sway*0.6:.1f},{top:.1f}" '
               f'stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="1.4" fill="none" stroke-linecap="round"/>')
    n = max(2, int(h / 28))
    for i in range(n):
        t = 0.3 + 0.65 * i / max(n - 1, 1)
        px = x + sway * t * 0.9
        py = ground - h * t
        side = 1 if i % 2 == 0 else -1
        L = 18 * (1.15 - t * 0.5)
        lx, ly = px + side * L, py - L * 0.55
        out.append(f'<path d="M{px:.1f},{py:.1f} Q{px+side*L*0.35:.1f},{py-L*0.75:.1f} {lx:.1f},{ly:.1f} '
                   f'Q{px+side*L*0.75:.1f},{py-L*0.05:.1f} {px:.1f},{py:.1f}Z" fill="{GOLD}" fill-opacity="{alpha*0.55:.2f}" '
                   f'stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width=".8"/>')
    out.append(f'<circle cx="{x+sway*0.6:.1f}" cy="{top-4:.1f}" r="3.2" fill="{GOLD}" fill-opacity="{alpha:.2f}"/>')

def sprout(out, x, ground, alpha):
    out.append(f'<path d="M{x},{ground} Q{x-1},{ground-8} {x},{ground-14}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" '
               f'stroke-width="1" fill="none"/>'
               f'<path d="M{x},{ground-13} q-7,-2 -9,-8 q7,0 9,8Z M{x},{ground-14} q6,-5 10,-5 q-2,6 -10,5Z" '
               f'fill="{GOLD}" fill-opacity="{alpha*0.8:.2f}"/>')

def build():
    rnd = random.Random(5)
    out = []
    ground = 430
    cx = 450
    out.append(f'<line x1="20" y1="{ground}" x2="880" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # arc of attention
    out.append(f'<circle cx="{cx}" cy="{ground}" r="310" fill="url(#glow)"/>')
    out.append(f'<path d="M{cx-290},{ground} A290,290 0 0 1 {cx+290},{ground}" stroke="{GOLD}" stroke-opacity=".4" '
               f'stroke-width="1.1" stroke-dasharray="2 6" fill="none" stroke-linecap="round"/>')
    for r, a in ((190, .14), (240, .09)):
        out.append(f'<path d="M{cx-r},{ground} A{r},{r} 0 0 1 {cx+r},{ground}" stroke="{GOLD}" stroke-opacity="{a}" '
                   f'stroke-width=".8" fill="none"/>')
    # tended plants
    xs = [285, 340, 395, 450, 505, 560, 615]
    hs = [130, 180, 220, 255, 215, 170, 135]
    for x, h in zip(xs, hs):
        plant(out, rnd, x, ground, h, 0.92)
    # untended seedlings fading toward the edges
    for i, x in enumerate([40, 65, 90, 115, 140]):
        sprout(out, x, ground, 0.12 + 0.07 * i)
    for i, x in enumerate([760, 785, 810, 835, 860]):
        sprout(out, x, ground, 0.42 - 0.07 * i)
    out.append(f'<text x="{cx}" y="{ground+42}" text-anchor="middle" font-family="Inter" font-size="13" '
               f'letter-spacing="3" fill="#8a8578">WHAT YOU CAN TEND</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".16"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
