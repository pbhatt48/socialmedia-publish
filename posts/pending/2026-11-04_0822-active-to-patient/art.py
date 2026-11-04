"""Money relocating from the restless to the patient: frantic trails on the left,
a stream of coins arcing into a still, filling vessel on the right. 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"


def build():
    rnd = random.Random(1991)
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # Restless activity: many jittery, overlapping zig-zag trails
    cx, cy = 205, 300
    for i in range(14):
        pts = []
        x, y = cx + rnd.uniform(-70, 70), cy + rnd.uniform(-60, 60)
        for _ in range(9):
            pts.append((x, y))
            x += rnd.uniform(-42, 42)
            y += rnd.uniform(-34, 34)
            x = min(max(x, cx - 125), cx + 125)
            y = min(max(y, cy - 105), ground - 20)
        d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
        a = rnd.uniform(0.12, 0.42)
        out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="{rnd.uniform(.6,1.3):.2f}" '
                   f'fill="none" stroke-linejoin="round" stroke-linecap="round"/>')
    # small arrowheads hinting at constant buying and selling
    for _ in range(10):
        x, y = cx + rnd.uniform(-110, 110), cy + rnd.uniform(-90, 90)
        ang = rnd.uniform(0, 2 * math.pi)
        s = 6
        p1 = (x + s * math.cos(ang + 2.6), y + s * math.sin(ang + 2.6))
        p2 = (x + s * math.cos(ang - 2.6), y + s * math.sin(ang - 2.6))
        out.append(f'<path d="M{p1[0]:.1f},{p1[1]:.1f} L{x:.1f},{y:.1f} L{p2[0]:.1f},{p2[1]:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity=".5" stroke-width="1" fill="none" stroke-linecap="round"/>')

    # Vessel on the right: a calm, deep bowl slowly filling
    vx, vtop, vw = 665, 250, 150
    vbot = ground - 2
    out.append(f'<path d="M{vx-vw/2},{vtop} C{vx-vw/2},{vbot-10} {vx-vw/2+10},{vbot} {vx},{vbot} '
               f'C{vx+vw/2-10},{vbot} {vx+vw/2},{vbot-10} {vx+vw/2},{vtop}" stroke="{GOLD}" stroke-width="2" '
               f'stroke-opacity=".9" fill="none" stroke-linecap="round"/>')
    out.append(f'<line x1="{vx-vw/2-10}" y1="{vtop}" x2="{vx-vw/2+6}" y2="{vtop}" stroke="{GOLD}" stroke-width="2" stroke-opacity=".9"/>'
               f'<line x1="{vx+vw/2-6}" y1="{vtop}" x2="{vx+vw/2+10}" y2="{vtop}" stroke="{GOLD}" stroke-width="2" stroke-opacity=".9"/>')
    # fill: calm horizontal strata, denser toward the bottom
    for k, ly in enumerate(range(int(vbot) - 8, 318, -9)):
        t = (vbot - ly) / (vbot - vtop)
        half = vw / 2 - 6 - max(0, (ly - (vbot - 40))) * 1.1
        a = 0.7 - k * 0.055
        out.append(f'<line x1="{vx-half:.1f}" y1="{ly}" x2="{vx+half:.1f}" y2="{ly}" stroke="{GOLD}" '
                   f'stroke-opacity="{max(a, .12):.2f}" stroke-width="1"/>')
    out.append(f'<ellipse cx="{vx}" cy="330" rx="{vw/2-7}" ry="4" fill="none" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.2"/>')

    # Stream of coins arcing from the activity into the vessel
    sx, sy = 300, 220
    ex, ey = vx, 312
    for i in range(16):
        t = i / 15
        x = (1 - t) ** 2 * sx + 2 * (1 - t) * t * 480 + t ** 2 * ex
        y = (1 - t) ** 2 * sy + 2 * (1 - t) * t * 80 + t ** 2 * ey
        r = 3.2 + t * 2.2
        a = 0.3 + 0.6 * t
        out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r:.1f}" ry="{r*0.8:.1f}" fill="{GOLD}" fill-opacity="{a:.2f}"/>')
    out.insert(1, f'<path d="M{sx},{sy} Q480,80 {ex},{ey}" stroke="{GOLD}" stroke-opacity=".28" stroke-width="1" '
                  f'stroke-dasharray="2 6" fill="none" stroke-linecap="round"/>')
    out.append(f'<circle cx="{vx}" cy="330" r="60" fill="url(#glow)"/>')

    for tx, lab in ((205, "ACTIVE"), (665, "PATIENT")):
        out.append(f'<line x1="{tx}" y1="{ground+6}" x2="{tx}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".3"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
