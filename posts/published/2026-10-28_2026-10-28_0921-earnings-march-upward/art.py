"""Earnings march upward; price wanders but follows. Returns SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"

def build():
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    n = 20
    x0, step = 90, 38
    earn = [26 * math.exp(0.105 * i) for i in range(n)]
    tops = []
    for i, e in enumerate(earn):
        x = x0 + i * step
        h = min(e, 330)
        tops.append((x, ground - h))
        a = 0.25 + 0.6 * i / (n - 1)
        out.append(f'<rect x="{x-9}" y="{ground-h:.1f}" width="18" height="{h:.1f}" fill="none" '
                   f'stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="1"/>')
        for k in range(int(h // 14)):
            yy = ground - 7 - k * 14
            out.append(f'<line x1="{x-5}" y1="{yy:.1f}" x2="{x+5}" y2="{yy:.1f}" stroke="{GOLD}" stroke-opacity="{a*0.35:.2f}" stroke-width=".6"/>')
    # earnings trend line
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in tops)
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1" stroke-dasharray="2 6" fill="none"/>')
    # price: wanders around earnings, finer steps
    rnd = random.Random(1996)
    pts = []
    for j in range((n - 1) * 4 + 1):
        t = j / 4
        i = int(t); f = t - i
        y = tops[i][1] if i >= n - 1 else tops[i][1] * (1 - f) + tops[i + 1][1] * f
        h = ground - y
        wob = h * (0.28 * math.sin(t * 1.3 + 0.6) + 0.14 * math.sin(t * 3.1)) + rnd.uniform(-6, 6)
        pts.append((x0 + t * step, max(70, y - wob)))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".95" stroke-width="1.8" fill="none" stroke-linejoin="round" stroke-linecap="round"/>')
    ex, ey = pts[-1]
    out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="22" fill="url(#glow)"/><circle cx="{ex:.1f}" cy="{ey:.1f}" r="3.2" fill="{GOLD}"/>')
    for tx, lab in ((x0, "YEAR 1"), (x0 + 19 * step, "20")):
        out.append(f'<line x1="{tx}" y1="{ground+6}" x2="{tx}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" letter-spacing="3" fill="#8a8578">{lab}</text>')
    out.append(f'<line x1="100" y1="96" x2="124" y2="96" stroke="{GOLD}" stroke-width="1.8"/>'
               f'<text x="134" y="101" font-family="Inter" font-size="12" letter-spacing="3" fill="#8a8578">MARKET VALUE</text>'
               f'<rect x="106" y="116" width="12" height="14" fill="none" stroke="{GOLD}" stroke-opacity=".7"/>'
               f'<text x="134" y="128" font-family="Inter" font-size="12" letter-spacing="3" fill="#8a8578">EARNINGS</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
