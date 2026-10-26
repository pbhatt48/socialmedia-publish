"""A farm field in perspective: furrows converging to the horizon, wheat in the foreground,
and a faint, ignored price squiggle in the sky. Value comes from what the asset produces."""
import math, random

GOLD = "#c9a96a"

def stalk(out, rnd, x, base, h, alpha):
    lean = rnd.uniform(-6, 6)
    tx, ty = x + lean, base - h
    out.append(f'<path d="M{x:.1f},{base:.1f} Q{x+lean*0.3:.1f},{base-h*0.6:.1f} {tx:.1f},{ty:.1f}" stroke="{GOLD}" '
               f'stroke-opacity="{alpha:.2f}" stroke-width="1" fill="none" stroke-linecap="round"/>')
    ang = math.atan2(-(ty - (base - h * 0.6)), tx - (x + lean * 0.3))
    for i in range(6):
        t = i * 4.2
        px = tx - t * math.cos(ang) * 0.9
        py = ty + t * math.sin(ang) * 0.9
        for s in (-1, 1):
            out.append(f'<ellipse cx="{px + s*2.6:.1f}" cy="{py - 1:.1f}" rx="1.6" ry="3.4" '
                       f'transform="rotate({s*28 + lean*2:.1f} {px + s*2.6:.1f} {py - 1:.1f})" '
                       f'fill="{GOLD}" fill-opacity="{alpha*0.8:.2f}"/>')

def build():
    rnd = random.Random(13)
    out = []
    horizon, vx = 300, 450
    # horizon
    out.append(f'<line x1="40" y1="{horizon}" x2="860" y2="{horizon}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # sun
    out.append(f'<circle cx="{vx}" cy="{horizon}" r="70" fill="url(#glow)"/>')
    out.append(f'<path d="M{vx-44},{horizon} A44,44 0 0 1 {vx+44},{horizon}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.2" fill="none"/>')
    for i in range(9):
        a = math.pi * (i + 1) / 10
        r1, r2 = 54, 54 + (16 if i % 2 == 0 else 9)
        out.append(f'<line x1="{vx+r1*math.cos(a):.1f}" y1="{horizon-r1*math.sin(a):.1f}" x2="{vx+r2*math.cos(a):.1f}" '
                   f'y2="{horizon-r2*math.sin(a):.1f}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # furrows converging to the vanishing point
    bottom = 470
    for i in range(-11, 12):
        bx = vx + i * 46
        op = 0.55 - abs(i) * 0.035
        out.append(f'<line x1="{vx + i*4:.1f}" y1="{horizon+2}" x2="{bx:.1f}" y2="{bottom}" stroke="{GOLD}" '
                   f'stroke-opacity="{max(op,0.12):.2f}" stroke-width="{0.6 + (11-abs(i))*0.05:.2f}"/>')
    # field edge
    out.append(f'<line x1="-56" y1="{bottom}" x2="956" y2="{bottom}" stroke="{GOLD}" stroke-opacity="0" />')
    # clip furrows to the canvas interior
    # wheat in the foreground, left and right clusters
    for cx0, n in ((120, 9), (780, 9)):
        for k in range(n):
            x = cx0 + (k - n / 2) * 11 + rnd.uniform(-3, 3)
            stalk(out, rnd, x, bottom, rnd.uniform(95, 140), rnd.uniform(0.55, 0.9))
    # faint, ignored price squiggle in the sky
    pts, x, y = [], 90, 120
    while x < 810:
        pts.append(f'{x:.1f},{y:.1f}')
        x += rnd.uniform(9, 16)
        y = min(max(y + rnd.uniform(-22, 22), 50), 190)
    out.append(f'<polyline points="{" ".join(pts)}" stroke="{GOLD}" stroke-opacity=".18" stroke-width="1" '
               f'stroke-dasharray="3 4" fill="none" stroke-linejoin="round"/>')
    out.append(f'<text x="810" y="40" text-anchor="end" font-family="Inter" font-size="12" letter-spacing="3" fill="#8a8578" fill-opacity=".7">PRICE</text>')
    out.append(f'<text x="{vx}" y="{bottom+34}" text-anchor="middle" font-family="Inter" font-size="13" letter-spacing="3" fill="#8a8578">EARNINGS</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>'
            f'<clipPath id="fieldclip"><rect x="40" y="0" width="820" height="520"/></clipPath></defs>')
    return defs + '<g clip-path="url(#fieldclip)">' + "".join(out) + '</g>'
