"""A simple business whose earnings rise steadily: years 5, 10, 20. SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"

def build():
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # the business: a plain, easily-understood building
    bx, bw, bh = 110, 120, 110
    out.append(f'<path d="M{bx},{ground} V{ground-bh} L{bx+bw/2},{ground-bh-44} L{bx+bw},{ground-bh} V{ground}" '
               f'stroke="{GOLD}" stroke-width="1.6" fill="none" stroke-linejoin="round"/>')
    for i in range(4):
        x = bx + 18 + i * 24
        out.append(f'<line x1="{x}" y1="{ground-bh+16}" x2="{x}" y2="{ground-12}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.1"/>')
    out.append(f'<line x1="{bx-8}" y1="{ground-bh}" x2="{bx+bw+8}" y2="{ground-bh}" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.2"/>')
    # a fair entry: small price mark under the building
    # earnings over time: columns growing at year 5, 10, 20
    xs = {0: 300, 5: 420, 10: 540, 20: 780}
    def ey(t):
        return ground - 40 * math.exp(t * 0.105)
    pts = [(xs[0] + (xs[20] - xs[0]) * t / 20, ey(t)) for t in [i * 0.5 for i in range(41)]]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-width="1.8" fill="none" stroke-linecap="round"/>')
    # soft fill under the curve
    out.append(f'<path d="{d} L{xs[20]},{ground} L{xs[0]},{ground} Z" fill="url(#fade)"/>')
    for t in range(1, 20):
        x = xs[0] + (xs[20] - xs[0]) * t / 20
        out.append(f'<line x1="{x:.1f}" y1="{ground}" x2="{x:.1f}" y2="{ey(t):.1f}" stroke="{GOLD}" stroke-opacity="{0.12 + t*0.012:.2f}" stroke-width=".8"/>')
    for t, lab in ((0, "TODAY"), (5, "5"), (10, "10"), (20, "20 YEARS")):
        x, y = xs[0] + (xs[20] - xs[0]) * t / 20, ey(t)
        out.append(f'<line x1="{x:.1f}" y1="{ground}" x2="{x:.1f}" y2="{y:.1f}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.3"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{4 + t*0.2:.1f}" fill="{GOLD}"/>')
        out.append(f'<line x1="{x:.1f}" y1="{ground+6}" x2="{x:.1f}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{x:.1f}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    gx, gy = xs[20], ey(20)
    out.append(f'<circle cx="{gx}" cy="{gy:.1f}" r="40" fill="url(#glow)"/>')
    out.append(f'<text x="{bx+bw/2}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
               f'letter-spacing="3" fill="#8a8578">THE BUSINESS</text>')
    # dotted link from business to earnings stream
    out.append(f'<path d="M{bx+bw+14},{ground-50} Q{xs[0]-30},{ground-58} {xs[0]-8},{ey(0)+2:.1f}" stroke="{GOLD}" '
               f'stroke-opacity=".4" stroke-dasharray="2 6" fill="none" stroke-linecap="round"/>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GOLD}" stop-opacity=".14"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient></defs>')
    return defs + "".join(out)
