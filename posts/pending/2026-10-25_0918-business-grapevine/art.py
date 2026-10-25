"""Scuttlebutt as a grapevine: a company at the centre, fine vines reaching out to the people around it."""
import math, random

GOLD = "#c9a96a"

NODES = [
    (130, 300, "CUSTOMERS"),
    (250, 140, "SUPPLIERS"),
    (450, 80, "EMPLOYEES"),
    (650, 140, "COMPETITORS"),
    (770, 300, "RESEARCHERS"),
]

def vine(out, rnd, x1, y1, x2, y2, alpha):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    b = rnd.choice([-1, 1]) * L * 0.18
    cx, cy = mx + nx * b, my + ny * b
    out.append(f'<path d="M{x1},{y1} Q{cx:.1f},{cy:.1f} {x2},{y2}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" '
               f'stroke-width="1.3" fill="none" stroke-linecap="round"/>')
    for t in (0.3, 0.5, 0.7):
        px = (1-t)**2*x1 + 2*(1-t)*t*cx + t*t*x2
        py = (1-t)**2*y1 + 2*(1-t)*t*cy + t*t*y2
        tx = 2*(1-t)*(cx-x1) + 2*t*(x2-cx)
        ty = 2*(1-t)*(cy-y1) + 2*t*(y2-cy)
        a = math.degrees(math.atan2(ty, tx)) + rnd.choice([-55, 55])
        out.append(f'<path d="M0,0 q6,-5 13,0 q-7,5 -13,0Z" transform="translate({px:.1f},{py:.1f}) rotate({a:.1f})" '
                   f'fill="{GOLD}" fill-opacity="{alpha*0.7:.2f}"/>')
        # small tendril curl
        if t == 0.5:
            out.append(f'<path d="M{px:.1f},{py:.1f} c4,-6 10,-6 10,0 c0,4 -5,4 -5,1" transform="rotate({a+180:.1f} {px:.1f} {py:.1f})" '
                       f'stroke="{GOLD}" stroke-opacity="{alpha*0.6:.2f}" stroke-width=".8" fill="none"/>')

def build():
    rnd = random.Random(5)
    out = []
    ground = 430
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    cx, cy = 450, 330
    # faint cross-links between neighbours: they talk about each other
    for (x1, y1, _), (x2, y2, _) in zip(NODES, NODES[1:]):
        out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GOLD}" stroke-opacity=".14" '
                   f'stroke-width=".8" stroke-dasharray="2 6"/>')
    for i, (x, y, _) in enumerate(NODES):
        vine(out, rnd, cx, cy - 34, x, y, 0.55 + 0.08 * (i % 2))
    # the company: a simple building
    out.append(f'<circle cx="{cx}" cy="{cy-10}" r="70" fill="url(#glow)"/>')
    out.append(f'<path d="M{cx-40},{ground} L{cx-40},{cy-6} L{cx},{cy-34} L{cx+40},{cy-6} L{cx+40},{ground}" '
               f'stroke="{GOLD}" stroke-width="1.6" fill="none" stroke-linejoin="round"/>')
    for k in range(-2, 3):
        out.append(f'<line x1="{cx+k*14}" y1="{cy+8}" x2="{cx+k*14}" y2="{ground-12}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1"/>')
    out.append(f'<line x1="{cx-46}" y1="{cy}" x2="{cx+46}" y2="{cy}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1"/>')
    for x, y, lab in NODES:
        out.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{GOLD}" fill-opacity=".9"/>'
                   f'<circle cx="{x}" cy="{y}" r="15" stroke="{GOLD}" stroke-opacity=".3" fill="none"/>')
        ly = y - 28 if y < 200 else y + 36
        out.append(f'<text x="{x}" y="{ly}" text-anchor="middle" font-family="Inter" font-size="12" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".28"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
