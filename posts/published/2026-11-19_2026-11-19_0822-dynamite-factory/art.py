"""Wandering path with a lit match vs. a straight bearing guided by a compass: method over improvisation.
Returns SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"
GREY = "#8a8578"

def build():
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # Left: crates of the "factory" (stacked boxes, faint)
    for (x, y, w, h) in [(100, ground-60, 70, 60), (170, ground-60, 70, 60), (135, ground-110, 70, 50)]:
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1"/>')
        out.append(f'<line x1="{x}" y1="{y}" x2="{x+w}" y2="{y+h}" stroke="{GOLD}" stroke-opacity=".18" stroke-width=".8"/>')
        out.append(f'<line x1="{x+w}" y1="{y}" x2="{x}" y2="{y+h}" stroke="{GOLD}" stroke-opacity=".18" stroke-width=".8"/>')

    # Left: a wandering dotted path (no bearing) ending in a struck match
    rnd = random.Random(5)
    pts = []
    x, y = 275, ground - 20
    for i in range(26):
        pts.append((x, y))
        x += 8.5 + rnd.uniform(-1, 1)
        y += 22 * math.sin(i * 0.9) * rnd.uniform(0.6, 1.0) - 5
        y = max(min(y, ground - 12), 150)
    d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1.1" stroke-dasharray="2 6" '
               f'fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    mx, my = pts[-1]
    # match stick
    out.append(f'<line x1="{mx-14:.1f}" y1="{my+22:.1f}" x2="{mx:.1f}" y2="{my:.1f}" stroke="{GOLD}" stroke-opacity=".8" stroke-width="2.2" stroke-linecap="round"/>')
    out.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="3.4" fill="{GOLD}"/>')
    out.append(f'<circle cx="{mx:.1f}" cy="{my-8:.1f}" r="30" fill="url(#glow)"/>')
    out.append(f'<path d="M{mx:.1f},{my-3:.1f} C{mx-8:.1f},{my-10:.1f} {mx-4:.1f},{my-20:.1f} {mx+1:.1f},{my-28:.1f} '
               f'C{mx+2:.1f},{my-18:.1f} {mx+8:.1f},{my-12:.1f} {mx:.1f},{my-3:.1f} Z" fill="{GOLD}" fill-opacity=".85"/>')

    # Center-right: compass medallion
    cx, cy, R = 670, 235, 120
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.2"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{R-12}" fill="none" stroke="{GOLD}" stroke-opacity=".25" stroke-width=".8"/>')
    for k in range(72):
        a = k * math.pi / 36
        r1 = R - 12 if k % 9 == 0 else R - 6
        op = .7 if k % 9 == 0 else .3
        out.append(f'<line x1="{cx+R*math.cos(a):.1f}" y1="{cy+R*math.sin(a):.1f}" x2="{cx+r1*math.cos(a):.1f}" y2="{cy+r1*math.sin(a):.1f}" '
                   f'stroke="{GOLD}" stroke-opacity="{op}" stroke-width=".9"/>')
    # rose
    for k in range(8):
        a = k * math.pi / 4 - math.pi / 2
        L = 92 if k % 2 == 0 else 52
        w = 13 if k % 2 == 0 else 9
        tx, ty = cx + L*math.cos(a), cy + L*math.sin(a)
        lx, ly = cx + w*math.cos(a - math.pi/2), cy + w*math.sin(a - math.pi/2)
        rx, ry = cx + w*math.cos(a + math.pi/2), cy + w*math.sin(a + math.pi/2)
        out.append(f'<path d="M{lx:.1f},{ly:.1f} L{tx:.1f},{ty:.1f} L{rx:.1f},{ry:.1f}" fill="none" stroke="{GOLD}" '
                   f'stroke-opacity="{.75 if k%2==0 else .4}" stroke-width="1"/>')
        out.append(f'<path d="M{cx},{cy} L{tx:.1f},{ty:.1f} L{lx:.1f},{ly:.1f} Z" fill="{GOLD}" fill-opacity="{.5 if k%2==0 else .2}"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{GOLD}"/>')
    out.append(f'<text x="{cx}" y="{cy-R+30}" text-anchor="middle" font-family="Inter" font-size="12" letter-spacing="2" fill="{GREY}">N</text>')

    # Straight bearing line from compass to a marked point on the horizon
    out.append(f'<line x1="{cx}" y1="{cy+R}" x2="{cx}" y2="{ground}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1"/>')
    out.append(f'<path d="M{cx-7},{ground} L{cx},{ground-10} L{cx+7},{ground} Z" fill="{GOLD}" fill-opacity=".8"/>')

    for tx, lab in [(275, "NO IDEA"), (670, "A METHOD")]:
        out.append(f'<line x1="{tx}" y1="{ground+6}" x2="{tx}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="{GREY}">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".5"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
