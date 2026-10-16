"""Good horse vs broken-down nag: a sound horseshoe beside a cracked, worn one on a racetrack. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"

def shoe_arc(cx, cy, r, a0, a1, steps=60):
    pts = []
    for i in range(steps + 1):
        a = math.radians(a0 + (a1 - a0) * i / steps)
        pts.append((cx + r * math.cos(a), cy - r * math.sin(a)))
    return pts

def shoe(out, cx, cy, s, alpha, a0=-40, a1=220, nails=True):
    outer = shoe_arc(cx, cy, 70 * s, a0, a1)
    inner = shoe_arc(cx, cy, 44 * s, a1, a0)
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in outer + inner) + " Z"
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="1.6" fill="{GOLD}" fill-opacity="{alpha*0.12:.2f}" stroke-linejoin="round"/>')
    mid = shoe_arc(cx, cy, 57 * s, a0 + 6, a1 - 6)
    d2 = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in mid)
    out.append(f'<path d="{d2}" stroke="{GOLD}" stroke-opacity="{alpha*0.45:.2f}" stroke-width="0.8" fill="none"/>')
    if nails:
        for k in range(8):
            a = a0 + 18 + k * ((a1 - a0 - 36) / 7)
            if 75 < a < 105:
                continue
            x = cx + 57 * s * math.cos(math.radians(a))
            y = cy - 57 * s * math.sin(math.radians(a))
            out.append(f'<rect x="{x-2.2:.1f}" y="{y-2.2:.1f}" width="4.4" height="4.4" fill="{GOLD}" fill-opacity="{alpha:.2f}" transform="rotate({-a:.0f} {x:.1f} {y:.1f})"/>')

def build():
    out = []
    ground = 420
    out.append('<defs><radialGradient id="glow"><stop offset="0" stop-color="#c9a96a" stop-opacity=".22"/>'
               '<stop offset="1" stop-color="#c9a96a" stop-opacity="0"/></radialGradient></defs>')
    out.append(f'<line x1="20" y1="{ground}" x2="880" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # receding track lanes
    for i, op in enumerate((.22, .16, .11, .07)):
        y = ground + 18 + i * 14 + i * i * 3
        out.append(f'<line x1="40" y1="{y}" x2="860" y2="{y}" stroke="{GOLD}" stroke-opacity="{op}" stroke-width=".8"/>')
    # rail fence
    rail_y = ground - 118
    out.append(f'<line x1="40" y1="{rail_y}" x2="860" y2="{rail_y}" stroke="{GOLD}" stroke-opacity=".28" stroke-width="1.2"/>')
    out.append(f'<line x1="40" y1="{rail_y+14}" x2="860" y2="{rail_y+14}" stroke="{GOLD}" stroke-opacity=".14" stroke-width=".8"/>')
    for x in range(40, 861, 55):
        out.append(f'<line x1="{x}" y1="{rail_y}" x2="{x}" y2="{ground}" stroke="{GOLD}" stroke-opacity=".12" stroke-width=".8"/>')
    # finish post
    out.append(f'<line x1="450" y1="70" x2="450" y2="{ground}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1.4"/>')
    out.append(f'<circle cx="450" cy="62" r="8" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.2" fill="none"/>')
    out.append(f'<circle cx="450" cy="62" r="2.5" fill="{GOLD}" fill-opacity=".7"/>')
    # sound shoe, left
    out.append(f'<circle cx="250" cy="250" r="140" fill="url(#glow)"/>')
    shoe(out, 250, 250, 1.25, 0.95)
    # broken-down shoe, right: cracked into two worn pieces, sagging
    shoe(out, 652, 276, 1.05, 0.42, a0=-40, a1=70, nails=False)
    shoe(out, 628, 300, 1.05, 0.30, a0=110, a1=215, nails=False)
    # crack hairlines
    out.append(f'<path d="M680,196 l6,8 l-5,6 l7,9" stroke="{GOLD}" stroke-opacity=".35" stroke-width=".8" fill="none"/>')
    # dust settling under the nag
    for i, (dx, dy, r) in enumerate([(-40, 128, 1.6), (-12, 134, 1.2), (22, 130, 1.4), (55, 136, 1.0), (85, 131, 1.3)]):
        out.append(f'<circle cx="{640+dx}" cy="{280+dy-10}" r="{r}" fill="{GOLD}" fill-opacity=".3"/>')
    for x, lab in ((250, "GOOD HORSE"), (645, "BROKEN-DOWN NAG")):
        out.append(f'<text x="{x}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    return "".join(out)
