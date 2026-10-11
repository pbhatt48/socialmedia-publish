"""A tipped balance: a heap of coins outweighed by a single small seal. Reputation over money.
Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"
MUTED = "#8a8578"


def pan(out, cx, cy, w=150):
    # three suspension chains meeting at the beam tip above
    out.append(f'<path d="M{cx-w/2:.1f},{cy:.1f} Q{cx:.1f},{cy+34:.1f} {cx+w/2:.1f},{cy:.1f}" '
               f'stroke="{GOLD}" stroke-width="1.6" fill="none" stroke-opacity=".9"/>')
    out.append(f'<line x1="{cx-w/2:.1f}" y1="{cy:.1f}" x2="{cx+w/2:.1f}" y2="{cy:.1f}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')


def build():
    out = []
    ground = 440
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".4" stroke-width="1"/>')
    cx, top = 450, 120
    # base and pillar
    out.append(f'<path d="M{cx-70},{ground} Q{cx},{ground-26} {cx+70},{ground}" stroke="{GOLD}" stroke-width="1.6" fill="none"/>')
    out.append(f'<line x1="{cx}" y1="{ground-13}" x2="{cx}" y2="{top+8}" stroke="{GOLD}" stroke-width="2.2"/>')
    out.append(f'<line x1="{cx-5}" y1="{ground-13}" x2="{cx-5}" y2="{top+20}" stroke="{GOLD}" stroke-opacity=".35" stroke-width=".8"/>')
    out.append(f'<circle cx="{cx}" cy="{top}" r="7" fill="none" stroke="{GOLD}" stroke-width="1.6"/>')
    out.append(f'<path d="M{cx},{top-7} L{cx},{top-26}" stroke="{GOLD}" stroke-width="1.4"/>')
    out.append(f'<circle cx="{cx}" cy="{top-30}" r="3.5" fill="{GOLD}"/>')
    # beam tilted: right side (reputation) down
    tilt = math.radians(14)
    L = 230
    lx, ly = cx - L * math.cos(tilt), top - L * math.sin(tilt)
    rx, ry = cx + L * math.cos(tilt), top + L * math.sin(tilt)
    out.append(f'<line x1="{lx:.1f}" y1="{ly:.1f}" x2="{rx:.1f}" y2="{ry:.1f}" stroke="{GOLD}" stroke-width="2.4" stroke-linecap="round"/>')
    out.append(f'<line x1="{lx:.1f}" y1="{ly+5:.1f}" x2="{rx:.1f}" y2="{ry+5:.1f}" stroke="{GOLD}" stroke-opacity=".3" stroke-width=".8"/>')
    for x, y in ((lx, ly), (rx, ry)):
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{GOLD}"/>')
    drop = 150
    for (x, y) in ((lx, ly), (rx, ry)):
        py = y + drop
        for dx in (-75, 0, 75):
            op = .7 if dx == 0 else .45
            out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x+dx:.1f}" y2="{py:.1f}" stroke="{GOLD}" stroke-opacity="{op}" stroke-width=".9"/>')
        pan(out, x, py)
    # left pan: a heap of coins (money) — much, yet lighter
    px, py = lx, ly + drop
    rows = [7, 6, 5, 4, 3, 2]
    for r, n in enumerate(rows):
        for i in range(n):
            x = px + (i - (n - 1) / 2) * 17
            y = py + 4 - r * 8
            op = 0.95 - r * 0.08
            out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="8.5" ry="3.6" fill="#0f0f0f" stroke="{GOLD}" '
                       f'stroke-opacity="{op:.2f}" stroke-width="1.1"/>')
    # right pan: one small seal (reputation) — slight, yet heavier
    sx, sy = rx, ry + drop - 14
    out.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="30" fill="url(#glow)"/>')
    out.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="11" fill="{GOLD}"/>')
    out.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="7" fill="none" stroke="#0f0f0f" stroke-opacity=".6" stroke-width="1"/>')
    for k in range(12):
        a = k * math.pi / 6
        out.append(f'<line x1="{sx+13*math.cos(a):.1f}" y1="{sy+13*math.sin(a):.1f}" x2="{sx+16*math.cos(a):.1f}" '
                   f'y2="{sy+16*math.sin(a):.1f}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1"/>')
    # labels
    for x, lab in ((lx, "MONEY"), (rx, "REPUTATION")):
        out.append(f'<text x="{x:.1f}" y="{ground+36}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="{MUTED}">{lab}</text>')
        out.append(f'<line x1="{x:.1f}" y1="{ground+6}" x2="{x:.1f}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".4"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
