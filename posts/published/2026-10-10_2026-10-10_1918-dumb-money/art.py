"""Many restless, erratic paths (active forecasting) fan out and mostly fall back, while one calm line of
evenly spaced purchases rises steadily above most of them. Returns SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"

def build():
    out = []
    ground = 430
    x0, x1 = 90, 810
    start = 330
    rnd = random.Random(19)
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # the restless crowd: jittery random walks with drag, most ending below the steady line
    n = 22
    for k in range(n):
        y = start
        drift = -0.28 + rnd.uniform(-0.55, 0.35)
        pts = [f"{x0},{start}"]
        for x in range(x0 + 12, x1 + 1, 12):
            y += -drift * 1.0 + rnd.gauss(0, 7.5)
            y = max(70, min(ground - 12, y))
            pts.append(f"{x},{y:.1f}")
        alpha = 0.10 + 0.14 * rnd.random()
        out.append(f'<polyline points="{" ".join(pts)}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" '
                   f'stroke-width=".8" fill="none" stroke-linejoin="round"/>')
    # the steady line: compounding curve with evenly spaced purchase marks
    pts = []
    for x in range(x0, x1 + 1, 6):
        t = (x - x0) / (x1 - x0)
        y = start - 215 * (math.exp(1.6 * t) - 1) / (math.exp(1.6) - 1)
        pts.append((x, y))
    out.append(f'<polyline points="{" ".join(f"{x},{y:.1f}" for x, y in pts)}" stroke="{GOLD}" stroke-opacity=".95" '
               f'stroke-width="2" fill="none" stroke-linecap="round"/>')
    for i in range(9):
        x = x0 + i * 90
        t = (x - x0) / (x1 - x0)
        y = start - 215 * (math.exp(1.6 * t) - 1) / (math.exp(1.6) - 1)
        out.append(f'<circle cx="{x}" cy="{y:.1f}" r="3.6" fill="{GOLD}"/>')
        out.append(f'<line x1="{x}" y1="{y+8:.1f}" x2="{x}" y2="{ground}" stroke="{GOLD}" stroke-opacity=".16" stroke-dasharray="2 5"/>')
        out.append(f'<line x1="{x}" y1="{ground+6}" x2="{x}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
    ex, ey = pts[-1]
    out.append(f'<circle cx="{ex}" cy="{ey:.1f}" r="30" fill="url(#glow)"/>')
    for tx, lab in [(x0, "BUY"), (450, "BUY"), (x1, "BUY")]:
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
