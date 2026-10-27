"""House of cards under a bright sun, a storm gathering at the edge: prosperity is not safety.
Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"


def card(x1, y1, x2, y2, alpha):
    # a playing card seen edge-on: two close parallel lines
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    ox, oy = -dy / n * 2.2, dx / n * 2.2
    return (f'<path d="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f} L{x2+ox:.1f},{y2+oy:.1f} L{x1+ox:.1f},{y1+oy:.1f} Z" '
            f'fill="{GOLD}" fill-opacity="{alpha*0.25:.2f}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" '
            f'stroke-width="1" stroke-linejoin="round"/>')


def build():
    out = []
    ground = 420
    out.append(f'<line x1="20" y1="{ground}" x2="880" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # sun, upper left, with fine rays
    sx, sy = 190, 130
    out.append(f'<circle cx="{sx}" cy="{sy}" r="70" fill="url(#glow)"/>')
    out.append(f'<circle cx="{sx}" cy="{sy}" r="30" fill="none" stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.4"/>')
    for i in range(24):
        a = 2 * math.pi * i / 24
        r1, r2 = 40, (62 if i % 2 == 0 else 52)
        out.append(f'<line x1="{sx+r1*math.cos(a):.1f}" y1="{sy+r1*math.sin(a):.1f}" x2="{sx+r2*math.cos(a):.1f}" '
                   f'y2="{sy+r2*math.sin(a):.1f}" stroke="{GOLD}" stroke-opacity="{.7 if i % 2 == 0 else .4}" stroke-width="1"/>')

    # house of cards, center
    cx, w, h = 450, 34, 64
    tiers = 4
    for t in range(tiers):
        base = ground - t * (h + 4)
        count = tiers - t
        start = cx - (2 * count - 1) * w / 2
        alpha = 0.95 - t * 0.1
        for k in range(count):
            lx = start + k * 2 * w
            out.append(card(lx, base, lx + w / 2, base - h, alpha))
            out.append(card(lx + w, base, lx + w / 2, base - h, alpha))
        if t < tiers - 1:
            # flat card bridging the peaks
            fy = base - h - 2
            for k in range(count - 1):
                a = start + k * 2 * w + w / 2
                out.append(f'<line x1="{a-2:.1f}" y1="{fy:.1f}" x2="{a+2*w+2:.1f}" y2="{fy:.1f}" stroke="{GOLD}" '
                           f'stroke-opacity="{alpha:.2f}" stroke-width="2"/>')

    # storm gathering at the right edge: faint cloud and slanting rain
    cl = (f'M690,150 C690,128 712,116 732,124 C740,100 778,96 792,120 C812,110 838,124 834,146 '
          f'C852,150 852,174 832,176 L700,176 C680,176 676,152 690,150 Z')
    out.append(f'<path d="{cl}" fill="{GOLD}" fill-opacity=".05" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1"/>')
    for i in range(9):
        x = 706 + i * 14
        out.append(f'<line x1="{x}" y1="190" x2="{x-10}" y2="{230 + (i % 3) * 14}" stroke="{GOLD}" '
                   f'stroke-opacity="{.28 - (i % 3) * 0.06:.2f}" stroke-width="1" stroke-linecap="round"/>')

    # a faint dashed business-cycle line across the sky, cresting over the house
    pts = " ".join(f"{x},{300 - 90 * math.cos((x - 450) / 230):.1f}" for x in range(40, 861, 10))
    out.append(f'<polyline points="{pts}" fill="none" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1.1" '
               f'stroke-dasharray="2 7" stroke-linecap="round"/>')

    for tx, lab in [(190, "FAIR WEATHER"), (450, "LOW QUALITY"), (770, "THE TURN")]:
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
