"""Four whirlpools (envy, resentment, revenge, self-pity) and a small boat holding a steady course past them.
Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"

def whirl(out, cx, cy, rmax, turns, alpha):
    # flattened spiral seen in perspective on the water
    pts = []
    steps = int(turns * 90)
    for i in range(steps + 1):
        t = i / steps
        a = t * turns * 2 * math.pi
        r = 3 + (rmax - 3) * t
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + 0.32 * r * math.sin(a):.1f}")
    for k, w in ((0, 1.1), (1, 0.6)):
        op = alpha * (1 if k == 0 else 0.45)
        sub = pts if k == 0 else pts[len(pts)//3:]
        out.append(f'<polyline points="{" ".join(sub)}" stroke="{GOLD}" stroke-opacity="{op:.2f}" '
                   f'stroke-width="{w}" fill="none" stroke-linecap="round" '
                   f'transform="translate(0,{k*3})"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="2" fill="{GOLD}" fill-opacity="{alpha:.2f}"/>')

def build():
    out = []
    water = 170
    out.append(f'<line x1="40" y1="{water}" x2="860" y2="{water}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    out.append(f'<path d="M380,{water} A70,70 0 0 1 520,{water}" stroke="{GOLD}" stroke-opacity=".4" stroke-width="1" fill="none"/>')
    for k in range(9):
        a = math.pi * (k + 1) / 10
        x1, y1 = 450 + 84*math.cos(a), water - 84*math.sin(a)
        x2, y2 = 450 + (100 + 12*(k % 2))*math.cos(a), water - (100 + 12*(k % 2))*math.sin(a)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GOLD}" stroke-opacity=".22" stroke-width=".8"/>')
    # faint swell lines
    for i, y in enumerate((204, 240, 284, 334)):
        op = 0.10 + 0.04 * i
        out.append(f'<path d="M{60-i*6},{y} C220,{y-6} 380,{y+6} 520,{y} S760,{y-5} {840+i*6},{y}" '
                   f'stroke="{GOLD}" stroke-opacity="{op:.2f}" stroke-width=".8" fill="none"/>')
    # four whirlpools below the course
    pools = [(170, 300, 74, 3.2, .75, "ENVY"), (350, 352, 66, 3.0, .6, "RESENTMENT"),
             (550, 312, 78, 3.4, .7, "REVENGE"), (730, 362, 64, 2.9, .55, "SELF-PITY")]
    for cx, cy, r, t, a, lab in pools:
        whirl(out, cx, cy, r, t, a)
        out.append(f'<text x="{cx}" y="{cy + 0.32*r + 30:.0f}" text-anchor="middle" font-family="Inter" '
                   f'font-size="12" letter-spacing="3" fill="#8a8578">{lab}</text>')
    # steady course: dashed line skirting above the whirlpools
    out.append(f'<path d="M70,232 L790,232" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1.2" '
               f'stroke-dasharray="2 7" stroke-linecap="round" fill="none"/>')
    # small sailboat at the right end of the course
    bx, by = 800, 232
    out.append(f'<path d="M{bx-34},{by-8} L{bx+30},{by-8} L{bx+20},{by+2} L{bx-26},{by+2} Z" fill="{GOLD}" fill-opacity=".85"/>')
    out.append(f'<line x1="{bx}" y1="{by-8}" x2="{bx}" y2="{by-92}" stroke="{GOLD}" stroke-width="1.6"/>')
    out.append(f'<path d="M{bx-3},{by-90} L{bx-3},{by-14} L{bx-44},{by-14} Z" fill="{GOLD}" fill-opacity=".55"/>')
    out.append(f'<path d="M{bx+3},{by-80} L{bx+3},{by-14} L{bx+30},{by-14} Z" fill="{GOLD}" fill-opacity=".3"/>')
    out.append(f'<circle cx="{bx}" cy="{by-10}" r="40" fill="url(#glow)"/>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".25"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
