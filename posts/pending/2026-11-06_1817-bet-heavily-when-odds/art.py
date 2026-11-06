"""Long stretch of small, untaken chances, then one heavy stake where the odds rise: betting big rarely."""
import math, random

GOLD = "#c9a96a"

def coin_stack(out, x, base, n, rx=30, ry=7, gap=9):
    for i in range(n):
        y = base - i * gap
        a = 0.55 + 0.4 * (i / max(n - 1, 1))
        out.append(f'<path d="M{x-rx},{y-ry*0.4:.1f} L{x-rx},{y:.1f} A{rx},{ry} 0 0 0 {x+rx},{y:.1f} L{x+rx},{y-ry*0.4:.1f}" '
                   f'stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="1.2" fill="none"/>')
    top = base - (n - 1) * gap - ry * 0.4
    out.append(f'<ellipse cx="{x}" cy="{top:.1f}" rx="{rx}" ry="{ry}" stroke="{GOLD}" stroke-width="1.4" fill="{GOLD}" fill-opacity=".12"/>')
    return top

def build():
    out = []
    rnd = random.Random(5)
    ground = 400
    peak_x = 640
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    # odds curve: flat and low most of the way, rising sharply near the stake
    pts = []
    for i in range(0, 161):
        x = 70 + i * (760 / 160)
        d = (x - peak_x) / 55
        y = ground - 18 - 250 * math.exp(-d * d) - 6 * math.sin(x / 23)
        pts.append(f"{x:.1f},{y:.1f}")
    out.append(f'<polyline points="{" ".join(pts)}" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1.1" '
               f'stroke-dasharray="2 6" stroke-linecap="round" fill="none"/>')
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # many passing chances: faint single coins and ticks
    x = 80
    while x < 560:
        h = rnd.uniform(6, 20)
        out.append(f'<line x1="{x:.1f}" y1="{ground}" x2="{x:.1f}" y2="{ground-h:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity="{rnd.uniform(.15,.35):.2f}" stroke-width="1"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{ground-h-4:.1f}" r="2.2" stroke="{GOLD}" stroke-opacity=".3" fill="none"/>')
        x += rnd.uniform(16, 26)
    for x in (720, 760, 800, 835):
        h = rnd.uniform(6, 16)
        out.append(f'<line x1="{x}" y1="{ground}" x2="{x}" y2="{ground-h:.1f}" stroke="{GOLD}" stroke-opacity=".2" stroke-width="1"/>')
    out.append(f'<circle cx="{peak_x}" cy="{ground-110}" r="140" fill="url(#glow)"/>')
    top = coin_stack(out, peak_x, ground - 6, 22)
    out.append(f'<line x1="{peak_x}" y1="{top-14:.1f}" x2="{peak_x}" y2="{top-40:.1f}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1"/>')
    for tx, lab in ((300, "THE REST OF THE TIME"), (peak_x, "THE ODDS")):
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    return defs + "".join(out)
