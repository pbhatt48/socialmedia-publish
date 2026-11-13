"""One untested idea vs. a proven model, copied and scaled. SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"
GREY = "#8a8578"

def motel(out, x, ground, w, h, alpha):
    """A simple roadside motel: block, low roof, row of doors/windows."""
    top = ground - h
    out.append(f'<rect x="{x:.1f}" y="{top:.1f}" width="{w:.1f}" height="{h:.1f}" fill="none" stroke="{GOLD}" '
               f'stroke-opacity="{alpha:.2f}" stroke-width="1.4"/>')
    out.append(f'<path d="M{x-6:.1f},{top:.1f} L{x+w/2:.1f},{top-h*0.32:.1f} L{x+w+6:.1f},{top:.1f}" fill="none" '
               f'stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="1.4" stroke-linejoin="round"/>')
    n = 3
    for i in range(n):
        dx = x + w * (i + 0.5) / n
        out.append(f'<rect x="{dx-5:.1f}" y="{ground-h*0.55:.1f}" width="10" height="{h*0.55:.1f}" fill="{GOLD}" '
                   f'fill-opacity="{alpha*0.35:.2f}" stroke="{GOLD}" stroke-opacity="{alpha*0.8:.2f}" stroke-width=".8"/>')
    out.append(f'<line x1="{x+w/2:.1f}" y1="{top-h*0.32:.1f}" x2="{x+w/2:.1f}" y2="{top-h*0.32-14:.1f}" '
               f'stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="1"/>')

def build():
    out = []
    ground = 400
    out.append(f'<line x1="30" y1="{ground}" x2="870" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # The innovator: a lone lightbulb on a thin, uncertain stalk
    bx, by = 140, 190
    out.append(f'<circle cx="{bx}" cy="{by}" r="70" fill="url(#glow)"/>')
    out.append(f'<path d="M{bx-16},{by+34} C{bx-16},{by+14} {bx-36},{by+4} {bx-36},{by-20} '
               f'A36,36 0 1 1 {bx+36},{by-20} C{bx+36},{by+4} {bx+16},{by+14} {bx+16},{by+34} Z" '
               f'fill="none" stroke="{GOLD}" stroke-width="1.6"/>')
    for k in range(3):
        y = by + 40 + k * 7
        out.append(f'<line x1="{bx-14}" y1="{y}" x2="{bx+14}" y2="{y}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.2"/>')
    out.append(f'<path d="M{bx-8},{by+30} L{bx-8},{by-6} L{bx},{by-16} L{bx+8},{by-6} L{bx+8},{by+30}" fill="none" '
               f'stroke="{GOLD}" stroke-opacity=".6" stroke-width="1"/>')
    for a in range(-150, -20, 26):
        r = math.radians(a)
        x1, y1 = bx + 52 * math.cos(r), by - 20 + 52 * math.sin(r)
        x2, y2 = bx + 66 * math.cos(r), by - 20 + 66 * math.sin(r)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity=".45" stroke-width="1.2" stroke-linecap="round"/>')
    # thin dashed stalk to the ground: unproven footing
    out.append(f'<line x1="{bx}" y1="{by+56}" x2="{bx}" y2="{ground}" stroke="{GOLD}" stroke-opacity=".35" '
               f'stroke-width="1" stroke-dasharray="3 6"/>')

    # The copycats: one proven motel, then the same model repeated
    xs = [300, 395, 490, 585, 680, 775]
    for i, x in enumerate(xs):
        alpha = 0.95 if i == 0 else 0.45 + 0.09 * i
        motel(out, x - 34, ground, 68, 62, min(alpha, 0.95))
    out.append(f'<path d="M266,{ground-118} C420,{ground-160} 640,{ground-160} 809,{ground-118}" fill="none" '
               f'stroke="{GOLD}" stroke-opacity=".35" stroke-width="1.1" stroke-dasharray="2 7" stroke-linecap="round"/>')

    labels = [(140, "ONE NEW IDEA"), (300, "PROVEN"), (585, "COPIED · IMPROVED · SCALED")]
    for tx, lab in labels:
        out.append(f'<line x1="{tx}" y1="{ground+6}" x2="{tx}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="{GREY}">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".3"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
