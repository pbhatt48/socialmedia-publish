"""A plain waterwheel mill turning on a steady stream: a business so simple it runs itself.
Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"


def build():
    out = []
    ground = 420
    cx, cy, r = 385, 250, 120
    # stream: layered gentle waves flowing beneath the wheel
    for i, (y, a) in enumerate([(395, .55), (408, .4), (421, .28), (434, .18)]):
        pts = []
        for x in range(90, 811, 10):
            pts.append(f"{x},{y + 3.2 * math.sin(x / 38 + i * 1.3):.1f}")
        out.append(f'<polyline points="{" ".join(pts)}" stroke="{GOLD}" stroke-opacity="{a}" '
                   f'stroke-width="1" fill="none" stroke-linecap="round"/>')
    # banks / horizon
    out.append(f'<line x1="60" y1="{ground - 32}" x2="250" y2="{ground - 32}" stroke="{GOLD}" stroke-opacity=".45"/>')
    out.append(f'<line x1="650" y1="{ground - 32}" x2="840" y2="{ground - 32}" stroke="{GOLD}" stroke-opacity=".45"/>')
    # mill house (simple gable) to the right of the wheel
    hx, hw, hy = 525, 170, ground - 32
    out.append(f'<path d="M{hx},{hy} L{hx},{hy-150} L{hx+hw/2},{hy-215} L{hx+hw},{hy-150} L{hx+hw},{hy}" '
               f'stroke="{GOLD}" stroke-opacity=".75" stroke-width="1.4" fill="none" stroke-linejoin="round"/>')
    out.append(f'<rect x="{hx+hw/2-18}" y="{hy-62}" width="36" height="62" stroke="{GOLD}" stroke-opacity=".55" fill="none"/>')
    out.append(f'<rect x="{hx+hw/2-14}" y="{hy-130}" width="28" height="28" stroke="{GOLD}" stroke-opacity=".45" fill="none"/>')
    for k in range(1, 7):
        y = hy - 150 + k * 21
        out.append(f'<line x1="{hx}" y1="{y}" x2="{hx+22}" y2="{y}" stroke="{GOLD}" stroke-opacity=".15"/>')
    # axle beam into the house
    out.append(f'<line x1="{cx}" y1="{cy}" x2="{hx}" y2="{cy}" stroke="{GOLD}" stroke-opacity=".6" stroke-width="2"/>')
    # wheel rims
    for rr, a, w in [(r, .9, 2.2), (r - 14, .5, 1), (34, .7, 1.4)]:
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{rr}" stroke="{GOLD}" stroke-opacity="{a}" stroke-width="{w}" fill="none"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="7" fill="{GOLD}"/>')
    # spokes and paddles
    n = 16
    for k in range(n):
        t = 2 * math.pi * k / n + 0.1
        x1, y1 = cx + 34 * math.cos(t), cy + 34 * math.sin(t)
        x2, y2 = cx + (r - 14) * math.cos(t), cy + (r - 14) * math.sin(t)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity="{.35 + .3 * (k % 2):.2f}" stroke-width="1"/>')
        px1, py1 = cx + r * math.cos(t), cy + r * math.sin(t)
        px2, py2 = cx + (r + 16) * math.cos(t), cy + (r + 16) * math.sin(t)
        out.append(f'<line x1="{px1:.1f}" y1="{py1:.1f}" x2="{px2:.1f}" y2="{py2:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity=".8" stroke-width="2.4" stroke-linecap="round"/>')
    # dashed rotation arc
    out.append(f'<path d="M{cx - r - 40},{cy - 30} A{r + 40},{r + 40} 0 0 1 {cx - 30},{cy - r - 40}" stroke="{GOLD}" '
               f'stroke-opacity=".35" stroke-width="1.2" stroke-dasharray="2 7" fill="none" stroke-linecap="round"/>')
    out.append(f'<path d="M{cx - 40},{cy - r - 46} l12,6 l-12,6" stroke="{GOLD}" stroke-opacity=".45" fill="none"/>')
    # glow at the hub
    out.append(f'<circle cx="{cx}" cy="{cy}" r="60" fill="url(#glow)"/>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".25"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
