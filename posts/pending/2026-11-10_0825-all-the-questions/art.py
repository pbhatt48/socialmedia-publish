"""Circles of knowledge: the larger what you know, the longer its edge with the unknown.
Returns SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"

def sphere(out, rnd, cx, ground, r, alpha):
    cy = ground - r
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r*1.5:.1f}" fill="url(#glow)" opacity="{alpha*0.6:.2f}"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GOLD}" fill-opacity="{0.05+0.04*alpha:.2f}" '
               f'stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="1.3"/>')
    # inner contour rings: what is known
    for k in range(1, 4):
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r*k/4:.1f}" fill="none" stroke="{GOLD}" '
                   f'stroke-opacity="{alpha*0.22:.2f}" stroke-width=".7"/>')
    # frontier: short open strokes + scattered points, count proportional to circumference
    n = int(2 * math.pi * r / 11)
    for i in range(n):
        a = 2 * math.pi * i / n + rnd.uniform(-0.03, 0.03)
        if math.sin(a) < -0.98 + 0.0:  # skip the point touching the ground
            pass
        y_end = cy - (r + 12) * math.sin(a)
        if cy - r * math.sin(a) > ground - 2 or y_end > ground - 4:
            continue
        L = rnd.uniform(6, 16)
        x1, y1 = cx + (r + 4) * math.cos(a), cy - (r + 4) * math.sin(a)
        x2, y2 = cx + (r + 4 + L) * math.cos(a), cy - (r + 4 + L) * math.sin(a)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity="{alpha*rnd.uniform(.35,.8):.2f}" stroke-width=".9" stroke-linecap="round"/>')
        d = r + 4 + L + rnd.uniform(6, 14)
        px, py = cx + d * math.cos(a), cy - d * math.sin(a)
        if py < ground - 6:
            out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{rnd.uniform(.8,1.6):.1f}" fill="{GOLD}" '
                       f'fill-opacity="{alpha*rnd.uniform(.25,.6):.2f}"/>')

def build():
    rnd = random.Random(14)
    out = []
    ground = 430
    out.append(f'<line x1="30" y1="{ground}" x2="870" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    sphere(out, rnd, 150, ground, 34, 0.75)
    sphere(out, rnd, 355, ground, 82, 0.85)
    sphere(out, rnd, 640, ground, 150, 0.95)
    labels = [(150, "KNOWN"), (355, "MORE KNOWN"), (640, "MORE TO ASK")]
    for tx, lab in labels:
        out.append(f'<line x1="{tx}" y1="{ground+6}" x2="{tx}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
