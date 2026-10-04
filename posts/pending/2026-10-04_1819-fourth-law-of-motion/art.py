"""Newton's cradle: a fourth law of motion. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"


def build():
    out = []
    ground = 430
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # frame
    left, right, top = 300, 600, 110
    base_y = ground - 4
    out.append(f'<rect x="{left-40}" y="{base_y-10}" width="{right-left+80}" height="10" rx="2" '
               f'fill="none" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.2"/>')
    for x in (left, right):
        out.append(f'<path d="M{x},{base_y-10} L{x},{top} " stroke="{GOLD}" stroke-opacity=".75" stroke-width="1.6" fill="none"/>')
    out.append(f'<line x1="{left}" y1="{top}" x2="{right}" y2="{top}" stroke="{GOLD}" stroke-opacity=".85" stroke-width="1.6"/>')
    for x in (left, right):
        out.append(f'<circle cx="{x}" cy="{top}" r="3.2" fill="{GOLD}" fill-opacity=".85"/>')

    r = 22
    L = 230
    cx0 = 450 - 4 * r
    xs = [cx0 + i * 2 * r for i in range(5)]

    def ball(px, ang, alpha, fill_alpha, sw=1.0):
        bx = px - L * math.sin(ang)
        by = top + L * math.cos(ang)
        s = (f'<line x1="{px-6}" y1="{top}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{GOLD}" stroke-opacity="{alpha*0.7:.2f}" stroke-width=".8"/>'
             f'<line x1="{px+6}" y1="{top}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{GOLD}" stroke-opacity="{alpha*0.7:.2f}" stroke-width=".8"/>'
             f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="{r}" fill="{GOLD}" fill-opacity="{fill_alpha:.2f}" '
             f'stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="{sw}"/>')
        return s

    # ghost trail of the swinging ball
    lead = xs[0]
    for k, a in enumerate([0.62, 0.5, 0.38, 0.26, 0.14]):
        alpha = 0.10 + 0.06 * k
        out.append(ball(lead, a, alpha, 0.0, 0.8))
    # swing arc
    a0, a1 = 0.0, 0.75
    pts = [(lead - (L + r + 14) * math.sin(t), top + (L + r + 14) * math.cos(t))
           for t in [a0 + (a1 - a0) * i / 30 for i in range(31)]]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1" stroke-dasharray="2 6" fill="none" stroke-linecap="round"/>')
    out.append(ball(lead, 0.75, 0.95, 0.12, 1.4))
    # resting balls
    for x in xs[1:]:
        out.append(ball(x, 0.0, 0.9, 0.85, 1.2))
    # sheen
    for x in xs[1:]:
        out.append(f'<circle cx="{x-7}" cy="{top+L-8}" r="5" fill="#fff" fill-opacity=".12"/>')

    # small apple resting on the ground, to the right
    ax = 720
    ay = ground - 13
    out.append(f'<path d="M{ax},{ay-9} C{ax-16},{ay-18} {ax-18},{ay+6} {ax-6},{ay+12} C{ax-2},{ay+14} {ax+2},{ay+14} {ax+6},{ay+12} '
               f'C{ax+18},{ay+6} {ax+16},{ay-18} {ax},{ay-9} Z" fill="{GOLD}" fill-opacity=".8"/>')
    out.append(f'<path d="M{ax},{ay-9} Q{ax+1},{ay-17} {ax+4},{ay-21}" stroke="{GOLD}" stroke-width="1.4" fill="none"/>')
    out.append(f'<path d="M{ax+2},{ay-16} q9,-8 15,-3 q-8,7 -15,3Z" fill="{GOLD}" fill-opacity=".55"/>')
    out.append(f'<circle cx="{ax}" cy="{ay}" r="40" fill="url(#glow)"/>')

    # tiny labels
    out.append(f'<text x="450" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
               f'letter-spacing="4" fill="#8a8578">THE FOURTH LAW</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".3"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
