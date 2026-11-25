"""Funnel filter: many candidate ideas above, only the best passes through. Opportunity cost as a filter.
Returns SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"

def build():
    rnd = random.Random(42)
    out = []
    ground = 430
    cx = 450
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # funnel: wide mouth at y=150, neck at y=310
    top_y, neck_y = 160, 312
    mouth, neck = 250, 14
    for side in (-1, 1):
        x0, x1 = cx + side * mouth, cx + side * neck
        out.append(f'<path d="M{x0},{top_y} C{cx + side*mouth*0.75},{top_y+70} {cx + side*neck*3},{neck_y-50} {x1},{neck_y} L{x1},{neck_y+26}" '
                   f'stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.6" fill="none" stroke-linecap="round"/>')
    # fine mesh lines across the funnel
    for i, t in enumerate((0.25, 0.5, 0.75)):
        y = top_y + (neck_y - top_y) * t
        w = mouth * (1 - t) ** 1.6 + neck * 1.5
        out.append(f'<line x1="{cx-w:.1f}" y1="{y:.1f}" x2="{cx+w:.1f}" y2="{y:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity="{0.18 + i*0.08:.2f}" stroke-width=".8" stroke-dasharray="1 5"/>')
    # many candidate ideas above the mouth
    for _ in range(70):
        x = rnd.uniform(cx - 330, cx + 330)
        y = rnd.uniform(40, 145)
        r = rnd.uniform(1.6, 4.2)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="none" stroke="{GOLD}" '
                   f'stroke-opacity="{rnd.uniform(.25,.6):.2f}" stroke-width=".9"/>')
    # rejected ideas resting on the ground at the sides
    for side in (-1, 1):
        for k in range(14):
            x = cx + side * rnd.uniform(140, 380)
            r = rnd.uniform(2, 4)
            out.append(f'<circle cx="{x:.1f}" cy="{ground - r:.1f}" r="{r:.1f}" fill="none" stroke="{GOLD}" '
                       f'stroke-opacity="{rnd.uniform(.12,.3):.2f}" stroke-width=".8"/>')
    # a few ideas inside funnel, shrinking count
    for _ in range(9):
        t = rnd.uniform(0.08, 0.55)
        y = top_y + (neck_y - top_y) * t
        w = (mouth * (1 - t) ** 1.6) * 0.7
        out.append(f'<circle cx="{cx + rnd.uniform(-w, w):.1f}" cy="{y:.1f}" r="{rnd.uniform(2,3.5):.1f}" fill="none" '
                   f'stroke="{GOLD}" stroke-opacity=".5" stroke-width=".9"/>')
    # dotted fall path and the one that passes
    out.append(f'<line x1="{cx}" y1="{neck_y+32}" x2="{cx}" y2="{ground-30}" stroke="{GOLD}" stroke-opacity=".4" '
               f'stroke-width="1.1" stroke-dasharray="2 6" stroke-linecap="round"/>')
    out.append(f'<circle cx="{cx}" cy="{ground-12}" r="40" fill="url(#glow)"/>')
    out.append(f'<circle cx="{cx}" cy="{ground-12}" r="12" fill="{GOLD}"/>')
    out.append(f'<text x="{cx}" y="{ground+38}" text-anchor="middle" font-family="Inter" font-size="13" '
               f'letter-spacing="3" fill="#8a8578">THE BEST AVAILABLE</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".5"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
