"""A new loom whose savings flow past the mill owner to the customers. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"
MUTED = "#8a8578"


def build():
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # The loom: frame, warp threads, beam and a shuttle
    lx, top, w = 150, 210, 170
    out.append(f'<rect x="{lx}" y="{top}" width="{w}" height="{ground-top}" fill="none" stroke="{GOLD}" stroke-opacity=".85" stroke-width="2"/>')
    out.append(f'<line x1="{lx-12}" y1="{top}" x2="{lx+w+12}" y2="{top}" stroke="{GOLD}" stroke-width="3" stroke-linecap="round"/>')
    for i in range(1, 18):
        x = lx + i * w / 18
        out.append(f'<line x1="{x:.1f}" y1="{top+8}" x2="{x:.1f}" y2="{ground-60}" stroke="{GOLD}" stroke-opacity="{0.25 + 0.3*(i % 2):.2f}" stroke-width=".8"/>')
    for j in range(6):
        y = ground - 60 - j * 6
        out.append(f'<line x1="{lx+6}" y1="{y}" x2="{lx+w-6}" y2="{y}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.4"/>')
    out.append(f'<path d="M{lx+w*0.35},{top+82} l40,0 l8,6 l-8,6 l-40,0 l-8,-6 Z" fill="{GOLD}" fill-opacity=".8"/>')
    # Gear on the side
    gx, gy, r = lx + w + 2, top + 40, 22
    teeth = []
    for k in range(24):
        a = k * math.pi / 12
        rr = r if k % 2 else r + 5
        teeth.append(f'{gx + rr*math.cos(a):.1f},{gy + rr*math.sin(a):.1f}')
    out.append(f'<polygon points="{" ".join(teeth)}" fill="none" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.2"/>')
    out.append(f'<circle cx="{gx}" cy="{gy}" r="5" fill="{GOLD}" fill-opacity=".7"/>')

    # Cloth leaving the loom, fanning out to many customers on the right
    sx, sy = lx + w, ground - 75
    customers = [(620 + (k % 4) * 52 + (k // 4 % 2) * 26, 150 + (k // 4) * 56) for k in range(20)]
    for cx, cy in customers:
        out.append(f'<path d="M{sx},{sy} C{sx+150},{sy} {cx-140},{cy} {cx-12},{cy}" stroke="{GOLD}" stroke-opacity=".28" stroke-width=".9" fill="none"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="{GOLD}" fill-opacity=".85"/>')

    # The mill owner keeps only a thin trickle
    ox = 420
    out.append(f'<path d="M{sx},{sy+20} C{sx+40},{sy+30} {ox-30},{ground-20} {ox},{ground-14}" stroke="{GOLD}" stroke-opacity=".55" stroke-width=".9" stroke-dasharray="2 5" fill="none"/>')
    for k in range(2):
        out.append(f'<ellipse cx="{ox+10}" cy="{ground-3-k*5}" rx="11" ry="3" fill="{GOLD}" fill-opacity=".75"/>')

    labels = [(lx + w/2, "NEW LOOM"), (ox + 10, "OWNER"), (725, "CUSTOMERS")]
    for tx, lab in labels:
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" letter-spacing="3" fill="{MUTED}">{lab}</text>')
    return "".join(out)
