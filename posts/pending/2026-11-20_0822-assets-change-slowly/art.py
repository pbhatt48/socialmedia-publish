"""Volatile earnings line above a slowly rising foundation of stacked stones (assets)."""
import math, random

GOLD = "#c9a96a"

def build():
    out = []
    ground = 420
    x0, x1 = 70, 830
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # Foundation: courses of stones, growing slowly left to right
    rnd = random.Random(5)
    bw = 38
    n = int((x1 - x0) / bw)
    for i in range(n):
        x = x0 + i * bw
        courses = 2 + int(i * 3.2 / n)
        for c in range(courses):
            h = 22
            y = ground - (c + 1) * h
            off = (bw / 2) if c % 2 else 0
            sx = x + off * 0 + 1.5
            alpha = 0.75 - c * 0.12
            out.append(f'<rect x="{sx:.1f}" y="{y+1.5:.1f}" width="{bw-3:.1f}" height="{h-3:.1f}" rx="2" '
                       f'fill="{GOLD}" fill-opacity="{alpha*0.12:.2f}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="1"/>')
    # Earnings: jagged, volatile line above
    rnd = random.Random(17)
    pts = []
    steps = 38
    base = 230
    for k in range(steps + 1):
        x = x0 + (x1 - x0) * k / steps
        drift = -40 * k / steps
        swing = rnd.uniform(-1, 1) * (55 + 35 * math.sin(k * 0.7))
        y = base + drift + swing
        y = max(70, min(300, y))
        pts.append((x, y))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.4" fill="none" stroke-linejoin="round"/>')
    for x, y in pts[::4]:
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.2" fill="{GOLD}" fill-opacity=".7"/>')
    # Slow asset trend line: top of the foundation
    out.append(f'<path d="M{x0},{ground-50} L{x1},{ground-106}" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1" stroke-dasharray="2 6" fill="none"/>')
    out.append(f'<text x="{x0}" y="60" font-family="Inter" font-size="13" letter-spacing="3" fill="#8a8578">EARNINGS</text>')
    out.append(f'<text x="{x0}" y="{ground+40}" font-family="Inter" font-size="13" letter-spacing="3" fill="#8a8578">ASSETS</text>')
    return "".join(out)
