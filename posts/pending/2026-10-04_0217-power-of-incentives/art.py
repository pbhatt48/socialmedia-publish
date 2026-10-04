"""Incentives as an invisible field: scattered paths bending toward a single attractor. SVG inner markup for 900x520."""
import math, random

GOLD = "#c9a96a"

def build():
    rnd = random.Random(19)
    out = []
    ground = 440
    ax, ay = 640, 250  # the incentive
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".5"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # faint concentric rings: the reach of the field
    for i, r in enumerate((40, 80, 125, 175, 230)):
        out.append(f'<circle cx="{ax}" cy="{ay}" r="{r}" fill="none" stroke="{GOLD}" '
                   f'stroke-opacity="{0.42 - i*0.07:.2f}" stroke-width=".8" stroke-dasharray="1.5 5"/>')
    # paths: each starts heading its own way, then bends into the attractor
    for k in range(15):
        sx = rnd.uniform(80, 320)
        sy = 120 + k * (ground - 160) / 14 + rnd.uniform(-8, 8)
        h = rnd.uniform(-0.9, 0.9)
        reach = rnd.uniform(110, 190)
        c1x, c1y = sx + reach * math.cos(h), sy + reach * math.sin(h)
        ang = math.atan2(sy - ay, sx - ax)
        c2x, c2y = ax + 90 * math.cos(ang * 0.5), ay + 90 * math.sin(ang * 0.5)
        ex, ey = ax + 20 * math.cos(ang), ay + 20 * math.sin(ang)
        a = rnd.uniform(0.25, 0.65)
        out.append(f'<path d="M{sx:.1f},{sy:.1f} C{c1x:.1f},{c1y:.1f} {c2x:.1f},{c2y:.1f} {ex:.1f},{ey:.1f}" '
                   f'stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="{rnd.uniform(.7,1.3):.2f}" '
                   f'fill="none" stroke-linecap="round"/>')
        out.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="2.6" fill="{GOLD}" fill-opacity="{a:.2f}"/>')
    out.append(f'<circle cx="{ax}" cy="{ay}" r="60" fill="url(#glow)"/>')
    out.append(f'<circle cx="{ax}" cy="{ay}" r="9" fill="{GOLD}"/>')
    out.append(f'<circle cx="{ax}" cy="{ay}" r="15" fill="none" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1"/>')
    out.append(f'<line x1="{ax}" y1="{ay+15}" x2="{ax}" y2="{ground}" stroke="{GOLD}" stroke-opacity=".25" stroke-dasharray="2 5"/>')
    out.append(f'<text x="{ax}" y="{ground+34}" text-anchor="middle" font-family="Inter" font-size="13" '
               f'letter-spacing="3" fill="#8a8578">INCENTIVE</text>')
    out.append(f'<text x="200" y="{ground+34}" text-anchor="middle" font-family="Inter" font-size="13" '
               f'letter-spacing="3" fill="#8a8578">BEHAVIOR</text>')
    return defs + "".join(out)
