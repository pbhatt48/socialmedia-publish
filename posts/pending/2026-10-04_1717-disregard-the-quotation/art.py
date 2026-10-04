"""Calm compounding value line beneath a noisy, fading price quotation. 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"

def build():
    out = []
    ground = 430
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    x0, x1 = 80, 820
    def value(x):
        t = (x - x0) / (x1 - x0)
        return 345 - 215 * (math.exp(1.6 * t) - 1) / (math.exp(1.6) - 1)
    # noisy quotation wandering around value
    rnd = random.Random(8)
    pts, drift = [], 0.0
    for i in range(149):
        x = x0 + i * (x1 - x0) / 148
        drift = drift * 0.86 + rnd.gauss(0, 13)
        y = max(70, min(420, value(x) + drift + 18 * math.sin(i / 7.0)))
        pts.append((x, y))
    for k in range(3):
        seg = pts[k * 49:(k + 1) * 49 + 2]
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in seg)
        out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity="{0.42 - 0.1*k:.2f}" stroke-width=".9" fill="none" stroke-linejoin="round"/>')
    # quotation ticks: faint vertical whiskers
    for x, y in pts[::6]:
        out.append(f'<line x1="{x:.1f}" y1="{y-7:.1f}" x2="{x:.1f}" y2="{y+7:.1f}" stroke="{GOLD}" stroke-opacity=".18" stroke-width=".8"/>')
    # steady value line
    d = "M" + " L".join(f"{x:.1f},{value(x):.1f}" for x in range(x0, x1 + 1, 6))
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".95" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    ex, ey = x1, value(x1)
    out.append(f'<circle cx="{ex}" cy="{ey:.1f}" r="22" fill="url(#glow)"/><circle cx="{ex}" cy="{ey:.1f}" r="4" fill="{GOLD}"/>')
    out.append(f'<circle cx="{x0}" cy="{value(x0):.1f}" r="3" fill="{GOLD}" fill-opacity=".8"/>')
    # anchor posts beneath value line
    for x in range(x0 + 60, x1, 120):
        out.append(f'<line x1="{x}" y1="{value(x)+6:.1f}" x2="{x}" y2="{ground}" stroke="{GOLD}" stroke-opacity=".14" stroke-width="1" stroke-dasharray="2 5"/>')
    lab = 'font-family="Inter" font-size="13" letter-spacing="3" fill="#8a8578"'
    out.append(f'<text x="{ex}" y="{ey-30:.1f}" text-anchor="middle" {lab}>VALUE</text>')
    out.append(f'<text x="450" y="{ground+36}" text-anchor="middle" {lab} fill-opacity=".8">THE QUOTATION WANDERS · THE BUSINESS COMPOUNDS</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
