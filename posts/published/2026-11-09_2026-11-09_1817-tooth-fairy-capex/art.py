"""A factory whose machinery must be fed: coins pour into the plant (capex) just to keep the gears turning.
Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"
GREY = "#8a8578"


def gear(cx, cy, r, teeth, alpha, rot=0.0):
    pts = []
    for i in range(teeth * 4):
        a = rot + i * math.pi * 2 / (teeth * 4)
        rr = r + (5 if i % 4 in (1, 2) else 0)
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return (f'<polygon points="{" ".join(pts)}" fill="none" stroke="{GOLD}" stroke-opacity="{alpha}" stroke-width="1.3" stroke-linejoin="round"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * 0.35:.1f}" fill="none" stroke="{GOLD}" stroke-opacity="{alpha}" stroke-width="1"/>'
            f'<circle cx="{cx}" cy="{cy}" r="2.5" fill="{GOLD}" fill-opacity="{alpha}"/>')


def coin(cx, cy, alpha, rx=11, ry=4):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{GOLD}" stroke-opacity="{alpha}" stroke-width="1.2"/>'
            f'<path d="M{cx - rx},{cy} v4 a{rx},{ry} 0 0 0 {2 * rx},0 v-4" fill="none" stroke="{GOLD}" stroke-opacity="{alpha * 0.7:.2f}" stroke-width="1"/>')


def build():
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # factory: sawtooth roof
    left, right, wall = 330, 690, 300
    roof = f"M{left},{ground} L{left},{wall}"
    x = left
    while x < right:
        roof += f" L{x + 60},{wall - 46} L{x + 60},{wall}"
        x += 60
    roof += f" L{right},{ground}"
    out.append(f'<path d="{roof}" fill="none" stroke="{GOLD}" stroke-opacity=".85" stroke-width="1.6" stroke-linejoin="round"/>')
    # skylight hatching
    x = left
    while x < right:
        for k in range(1, 4):
            out.append(f'<line x1="{x + k * 15}" y1="{wall}" x2="{x + k * 15}" y2="{wall - 46 * k * 15 / 60:.1f}" stroke="{GOLD}" stroke-opacity=".22" stroke-width="1"/>')
        x += 60
    # chimney with fading smoke
    out.append(f'<path d="M640,{wall - 46} L640,170 L662,170 L662,{wall - 46}" fill="none" stroke="{GOLD}" stroke-opacity=".85" stroke-width="1.6"/>')
    for i, (sx, sy, r) in enumerate([(656, 150, 9), (668, 126, 12), (684, 98, 15), (704, 68, 18)]):
        out.append(f'<circle cx="{sx}" cy="{sy}" r="{r}" fill="none" stroke="{GOLD}" stroke-opacity="{.45 - i * .1:.2f}" stroke-width="1"/>')

    # gears visible through the wall
    out.append(gear(430, 368, 30, 10, .75, 0.1))
    out.append(gear(484, 352, 18, 7, .6, 0.3))
    out.append(gear(560, 365, 34, 11, .7, 0.0))
    out.append(gear(616, 386, 16, 6, .5, 0.2))

    # intake hopper on the left wall, coins pouring in
    out.append(f'<path d="M262,250 L318,250 L300,292 L300,330 L330,330" fill="none" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.4" stroke-linejoin="round"/>'
               f'<path d="M262,250 L280,292 L280,346 L330,346" fill="none" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.4" stroke-linejoin="round"/>')
    for i, (cx, cy) in enumerate([(290, 96), (284, 140), (292, 184), (288, 226)]):
        out.append(coin(cx, cy, .35 + i * .15))
    out.append(f'<line x1="289" y1="70" x2="289" y2="84" stroke="{GOLD}" stroke-opacity=".25" stroke-dasharray="2 4"/>')

    # stack of coins beside the plant: the cash that must keep going back in
    for i in range(6):
        out.append(coin(200, ground - 8 - i * 9, .3 + i * .1, rx=16, ry=5))

    # tiny labels
    for tx, ty, lab in [(200, ground + 36, "CASH"), (290, ground + 36, "CAPEX"), (510, ground + 36, "THE BUSINESS")]:
        out.append(f'<line x1="{tx}" y1="{ground + 6}" x2="{tx}" y2="{ground + 14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx}" y="{ty}" text-anchor="middle" font-family="Inter" font-size="13" letter-spacing="3" fill="{GREY}">{lab}</text>')
    return "".join(out)
