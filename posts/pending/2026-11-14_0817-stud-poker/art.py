"""Stud poker hand on a table: four cards face down, one turned over to reveal the business beneath. Research = looking at the cards."""
import math

GOLD = "#c9a96a"
W, H = 112, 160

def card_back(cx, cy, rot, alpha):
    o = [f'<g transform="translate({cx},{cy}) rotate({rot})">',
         f'<rect x="{-W/2}" y="{-H/2}" width="{W}" height="{H}" rx="9" fill="#0f0f0f" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="1.4"/>',
         f'<rect x="{-W/2+9}" y="{-H/2+9}" width="{W-18}" height="{H-18}" rx="5" fill="none" stroke="{GOLD}" stroke-opacity="{alpha*0.55:.2f}" stroke-width=".8"/>']
    # fine diagonal lattice (hidden information), clipped to the inner panel
    o.append('<g clip-path="url(#inner)">')
    for i in range(-10, 11):
        d = i * 13
        o.append(f'<line x1="{-W/2+14+d:.1f}" y1="{-H/2+14}" x2="{-W/2+14+d+H-28:.1f}" y2="{H/2-14}" stroke="{GOLD}" stroke-opacity="{alpha*0.22:.2f}" stroke-width=".6"/>')
        o.append(f'<line x1="{W/2-14-d:.1f}" y1="{-H/2+14}" x2="{W/2-14-d-(H-28):.1f}" y2="{H/2-14}" stroke="{GOLD}" stroke-opacity="{alpha*0.22:.2f}" stroke-width=".6"/>')
    o.append('</g>')
    o.append(f'<circle r="11" fill="#0f0f0f" stroke="{GOLD}" stroke-opacity="{alpha*0.7:.2f}" stroke-width=".9"/>')
    o.append('</g>')
    return o

def card_face(cx, cy, rot):
    o = [f'<g transform="translate({cx},{cy}) rotate({rot})">',
         f'<rect x="{-W/2}" y="{-H/2}" width="{W}" height="{H}" rx="9" fill="#141310" stroke="{GOLD}" stroke-opacity=".95" stroke-width="1.6"/>']
    # rising earnings bars + trend line = the business behind the ticker
    bx0, base = -W/2 + 20, H/2 - 34
    vals = [18, 26, 31, 42, 55, 70]
    pts = []
    for i, v in enumerate(vals):
        x = bx0 + i * 13.5
        o.append(f'<line x1="{x:.1f}" y1="{base}" x2="{x:.1f}" y2="{base-v}" stroke="{GOLD}" stroke-opacity="{0.35+0.1*i:.2f}" stroke-width="5" stroke-linecap="butt"/>')
        pts.append((x, base - v - 9))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    o.append(f'<path d="{d}" stroke="{GOLD}" stroke-width="1.3" fill="none" stroke-linejoin="round"/>')
    o.append(f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="2.8" fill="{GOLD}"/>')
    o.append(f'<line x1="{bx0-8}" y1="{base}" x2="{W/2-14}" y2="{base}" stroke="{GOLD}" stroke-opacity=".5" stroke-width=".8"/>')
    o.append(f'<text x="0" y="{base+20}" text-anchor="middle" font-family="Inter" font-size="9" letter-spacing="2.5" fill="#8a8578">EARNINGS</text>')
    o.append(f'<text x="{-W/2+12}" y="{-H/2+22}" font-family="Inter" font-size="13" fill="{GOLD}">A</text>')
    o.append('</g>')
    return o

def build():
    out = []
    ground = 430
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # soft glow under revealed card
    out.append(f'<ellipse cx="690" cy="{ground-4}" rx="120" ry="14" fill="url(#glow)"/>')
    xs = [170, 300, 430, 560]
    for i, x in enumerate(xs):
        out += card_back(x, ground - H/2 - 2, [-3, 1.5, -1, 2][i], 0.5 + 0.1 * i)
    # revealed card, lifted and tilted as if just turned over
    out += card_face(700, ground - H/2 - 34, 8)
    # small motion arc showing the turn
    out.append(f'<path d="M612,{ground-200} Q650,{ground-250} 700,{ground-246}" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1.1" stroke-dasharray="2 6" fill="none" stroke-linecap="round"/>')
    for tx, lab in [(365, "UNSEEN"), (700, "STUDIED")]:
        out.append(f'<text x="{tx}" y="{ground+38}" text-anchor="middle" font-family="Inter" font-size="12" letter-spacing="3.5" fill="#8a8578">{lab}</text>')
    out.append(f'<line x1="120" y1="{ground+10}" x2="610" y2="{ground+10}" stroke="{GOLD}" stroke-opacity=".25" stroke-width=".8"/>')
    out.append(f'<line x1="640" y1="{ground+10}" x2="760" y2="{ground+10}" stroke="{GOLD}" stroke-opacity=".5" stroke-width=".8"/>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".3"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>'
            f'<clipPath id="inner"><rect x="{-W/2+9}" y="{-H/2+9}" width="{W-18}" height="{H-18}" rx="5"/></clipPath></defs>')
    return defs + "".join(out)
