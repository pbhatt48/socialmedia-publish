"""A long, jagged but rising path across 240 years: setbacks are real, the trend is up. Returns SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"

def walk(seed, n, x0, x1, y0, y1):
    rnd = random.Random(seed)
    pts = []
    crashes = {int(n * f) for f in (0.22, 0.47, 0.61, 0.83)}
    dip = 0.0
    for i in range(n + 1):
        t = i / n
        trend = y0 + (y1 - y0) * (t ** 1.9)
        if i in crashes:
            dip += rnd.uniform(26, 44)
        dip *= 0.86
        noise = rnd.uniform(-5, 5) * (0.4 + t)
        pts.append((x0 + (x1 - x0) * t, trend + dip + noise))
    return pts

def build():
    out = []
    ground = 420
    x0, x1 = 70, 830
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # faint horizontal guides
    for k, gy in enumerate((330, 240, 150)):
        out.append(f'<line x1="{x0}" y1="{gy}" x2="{x1}" y2="{gy}" stroke="{GOLD}" stroke-opacity="{.07 + k*.02:.2f}" '
                   f'stroke-width="1" stroke-dasharray="2 8"/>')
    pts = walk(1776, 240, x0, x1, 404, 70)
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = d + f" L{x1},{ground} L{x0},{ground} Z"
    out.append(f'<path d="{area}" fill="url(#rise)"/>')
    # echo lines for depth
    for off, op in ((10, .12), (5, .22)):
        e = "M" + " L".join(f"{x:.1f},{y + off:.1f}" for x, y in pts)
        out.append(f'<path d="{e}" stroke="{GOLD}" stroke-opacity="{op}" stroke-width=".8" fill="none" stroke-linejoin="round"/>')
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".95" stroke-width="1.8" fill="none" stroke-linejoin="round" stroke-linecap="round"/>')
    ex, ey = pts[-1]
    out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="30" fill="url(#glow)"/>')
    out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4.5" fill="{GOLD}"/>')
    sx, sy = pts[0]
    out.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="3" fill="{GOLD}" fill-opacity=".7"/>')
    for tx, lab in ((x0, "1776"), (x1, "2016")):
        out.append(f'<line x1="{tx}" y1="{ground+6}" x2="{tx}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    out.append(f'<text x="450" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="11" '
               f'letter-spacing="4" fill="#8a8578" fill-opacity=".8">240 YEARS</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="rise" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GOLD}" stop-opacity=".16"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient></defs>')
    return defs + "".join(out)
