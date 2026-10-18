"""A market path that compounds through its corrections, beside the flat line of capital that stepped aside to wait for them."""
import math, random

GOLD = "#c9a96a"

def market_path(seed, x0, x1, y0, y1, n):
    rnd = random.Random(seed)
    pts = []
    dips = {int(n * f): d for f, d in ((0.22, 0.07), (0.41, 0.12), (0.63, 0.09), (0.82, 0.16))}
    level = 0.0
    trend = []
    for i in range(n + 1):
        t = i / n
        trend.append((math.exp(2.2 * t) - 1) / (math.exp(2.2) - 1))
    shock = 0.0
    for i in range(n + 1):
        if i in dips:
            shock = dips[i]
        shock *= 0.86
        noise = rnd.uniform(-0.012, 0.012)
        level = max(trend[i] - shock + noise, 0)
        pts.append((x0 + (x1 - x0) * i / n, y0 - (y0 - y1) * level))
    return pts, sorted(dips)

def build():
    out = []
    ground = 430
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    for gy in (330, 230, 130):
        out.append(f'<line x1="70" y1="{gy}" x2="830" y2="{gy}" stroke="{GOLD}" stroke-opacity=".08" stroke-width="1"/>')
    x0, x1, base, top = 90, 810, 380, 70
    n = 120
    pts, dips = market_path(5, x0, x1, base, top, n)
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = d + f" L{x1},{base} L{x0},{base} Z"
    out.append(f'<path d="{area}" fill="url(#gap)"/>')
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-width="2.2" fill="none" stroke-linejoin="round" stroke-linecap="round"/>')
    for i in dips:
        k = min(i + 5, n)
        x, y = pts[k]
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="none" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1"/>')
        out.append(f'<line x1="{x:.1f}" y1="{y+8:.1f}" x2="{x:.1f}" y2="{base-4}" stroke="{GOLD}" stroke-opacity=".18" '
                   f'stroke-width="1" stroke-dasharray="2 5"/>')
    out.append(f'<line x1="{x0}" y1="{base}" x2="{x1}" y2="{base}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.4" stroke-dasharray="3 6"/>')
    out.append(f'<circle cx="{x0}" cy="{base}" r="4" fill="{GOLD}"/>')
    ex, ey = pts[-1]
    out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4.5" fill="{GOLD}"/>')
    out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="22" fill="url(#glow)"/>')
    out.append(f'<line x1="{x1+14}" y1="{ey+6:.1f}" x2="{x1+14}" y2="{base-6}" stroke="{GOLD}" stroke-opacity=".4" stroke-width="1"/>')
    for yy in (ey + 6, base - 6):
        out.append(f'<line x1="{x1+9}" y1="{yy:.1f}" x2="{x1+19}" y2="{yy:.1f}" stroke="{GOLD}" stroke-opacity=".4" stroke-width="1"/>')
    lab = 'font-family="Inter" font-size="13" letter-spacing="3" fill="#8a8578"'
    out.append(f'<text x="{x0}" y="{ground+38}" text-anchor="start" {lab}>INVESTED</text>')
    out.append(f'<text x="{x1}" y="{ground+38}" text-anchor="end" {lab}>WAITING FOR THE DIP</text>')
    out.append(f'<line x1="{x0}" y1="{ground+18}" x2="{x0+26}" y2="{ground+18}" stroke="{GOLD}" stroke-width="2"/>')
    out.append(f'<line x1="{x1-26}" y1="{ground+18}" x2="{x1}" y2="{ground+18}" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.4" stroke-dasharray="3 4"/>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="gap" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GOLD}" stop-opacity=".14"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0.01"/></linearGradient></defs>')
    return defs + "".join(out)
