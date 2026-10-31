"""Two paths from one starting point: a steady, flat bond line and a jagged equity line that compounds far higher."""
import math, random

GOLD = "#c9a96a"

def build():
    out = []
    ground = 430
    x0, x1 = 80, 820
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    start_y = 380
    # faint grid of years
    for i in range(0, 6):
        x = x0 + (x1 - x0) * i / 5
        out.append(f'<line x1="{x:.1f}" y1="{ground+6}" x2="{x:.1f}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<line x1="{x:.1f}" y1="70" x2="{x:.1f}" y2="{ground}" stroke="{GOLD}" stroke-opacity=".07" stroke-width="1"/>')
    # bond line: gentle, nearly flat compounding
    pts = []
    n = 120
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        y = start_y - 60 * (math.exp(1.0 * t) - 1) / (math.e - 1)
        pts.append((x, y))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1.4" fill="none" stroke-dasharray="3 6" stroke-linecap="round"/>')
    bx, by = pts[-1]
    # stock line: volatile but compounding much higher
    rnd = random.Random(42)
    spts = []
    noise = 0.0
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        trend = 290 * (math.exp(2.2 * t) - 1) / (math.exp(2.2) - 1)
        noise = noise * 0.75 + rnd.uniform(-1, 1) * 11 * (0.4 + t)
        if i in (38, 39, 40):
            noise -= 14  # a sharp drawdown
        y = start_y - trend - (noise if 0 < i < n else 0)
        spts.append((x, y))
    sd = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in spts)
    # soft area under stock line
    area = sd + f" L{x1},{ground} L{x0},{ground} Z"
    out.append(f'<path d="{area}" fill="url(#fade)"/>')
    out.append(f'<path d="{sd}" stroke="{GOLD}" stroke-opacity=".95" stroke-width="2" fill="none" stroke-linejoin="round" stroke-linecap="round"/>')
    sx, sy = spts[-1]
    # shared origin
    out.append(f'<circle cx="{x0}" cy="{start_y}" r="4.5" fill="{GOLD}"/>')
    out.append(f'<circle cx="{x0}" cy="{start_y}" r="22" fill="url(#glow)"/>')
    # endpoints
    out.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="4" fill="{GOLD}"/><circle cx="{sx:.1f}" cy="{sy:.1f}" r="24" fill="url(#glow)"/>')
    out.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="3.2" fill="none" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.2"/>')
    # gap bracket: what they're missing
    gx = x1 + 22
    out.append(f'<path d="M{gx-6},{sy:.1f} L{gx},{sy:.1f} L{gx},{by:.1f} L{gx-6},{by:.1f}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1" fill="none"/>')
    lab = 'font-family="Inter" font-size="13" letter-spacing="3" fill="#8a8578"'
    out.append(f'<text x="{sx-14:.1f}" y="{sy-18:.1f}" text-anchor="end" {lab}>STOCKS</text>')
    out.append(f'<text x="{bx-14:.1f}" y="{by+28:.1f}" text-anchor="end" {lab}>BONDS</text>')
    for i, l in enumerate(["YEAR 0", "", "", "", "", "30"]):
        if l:
            x = x0 + (x1 - x0) * i / 5
            out.append(f'<text x="{x:.1f}" y="{ground+40}" text-anchor="middle" {lab}>{l}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GOLD}" stop-opacity=".10"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient></defs>')
    return defs + "".join(out)
