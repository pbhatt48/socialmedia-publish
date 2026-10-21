"""A fan of uncertain futures, all staying above a price paid well below value: the margin absorbs forecast error."""
import math, random

GOLD = "#c9a96a"

def build():
    out = []
    rnd = random.Random(20)
    ground = 440
    x0, y0, x1 = 230, 210, 730
    price_y = 370
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # shaded margin band between value estimate and price paid
    out.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{price_y-y0}" fill="url(#band)"/>')
    # possible futures: wandering paths diverging from the estimate
    for i in range(26):
        drift = rnd.uniform(-1.4, 1.4)
        pts = [(x0, y0)]
        y = y0
        steps = 34
        for s in range(1, steps + 1):
            t = s / steps
            x = x0 + (x1 - x0) * t
            y += drift * 2.6 + rnd.gauss(0, 3.2) * (0.6 + t)
            y = min(y, price_y - 8 - rnd.uniform(0, 6))
            y = max(y, 80)
            pts.append((x, y))
        d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
        a = 0.18 + 0.5 * (1 - abs(drift) / 1.4)
        out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="0.9" fill="none" stroke-linejoin="round"/>')
    # value estimate (dashed) and price paid (solid)
    out.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1" stroke-dasharray="3 6"/>')
    out.append(f'<line x1="{x0}" y1="{price_y}" x2="{x1}" y2="{price_y}" stroke="{GOLD}" stroke-opacity=".95" stroke-width="2"/>')
    out.append(f'<circle cx="{x0}" cy="{y0}" r="4" fill="{GOLD}"/><circle cx="{x0}" cy="{y0}" r="22" fill="url(#glow)"/>')
    # margin bracket
    bx = x1 + 22
    out.append(f'<path d="M{bx-6},{y0} H{bx} V{price_y} H{bx-6}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1" fill="none"/>')
    lab = 'font-family="Inter" font-size="12" letter-spacing="3" fill="#8a8578"'
    out.append(f'<text x="{x0-18}" y="{y0+4}" text-anchor="end" {lab}>VALUE ESTIMATE</text>')
    out.append(f'<text x="{x0-18}" y="{price_y+4}" text-anchor="end" {lab}>PRICE PAID</text>')
    out.append(f'<text x="{bx+12}" y="{(y0+price_y)/2+4}" {lab}>MARGIN</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="band" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GOLD}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity=".10"/></linearGradient></defs>')
    return defs + "".join(out)
