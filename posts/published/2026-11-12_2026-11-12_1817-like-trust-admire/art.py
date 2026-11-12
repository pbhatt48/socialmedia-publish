"""Three strands braided into one cable, spanning two pillars: partnership built on
liking, trust and admiration. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"


def pillar(out, x, ground, top, w):
    out.append(f'<path d="M{x-w},{ground} L{x-w*0.8},{top} L{x+w*0.8},{top} L{x+w},{ground}" '
               f'stroke="{GOLD}" stroke-opacity=".85" stroke-width="1.6" fill="{GOLD}" fill-opacity=".06"/>')
    out.append(f'<line x1="{x-w*1.2}" y1="{top}" x2="{x+w*1.2}" y2="{top}" stroke="{GOLD}" stroke-opacity=".9" stroke-width="2"/>')
    for i in range(1, 6):
        y = top + (ground - top) * i / 6
        out.append(f'<line x1="{x-w*0.85}" y1="{y:.1f}" x2="{x+w*0.85}" y2="{y:.1f}" stroke="{GOLD}" stroke-opacity=".18" stroke-width="1"/>')


def build():
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    xl, xr, top = 170, 730, 150
    pillar(out, xl, ground, top, 22)
    pillar(out, xr, ground, top, 22)

    # catenary-ish sag between pillar tops
    sag = 120
    def base(t):
        x = xl + (xr - xl) * t
        y = top + sag * 4 * t * (1 - t)
        return x, y

    opac = [0.95, 0.7, 0.5]
    n = 240
    for k in range(3):
        pts = []
        for i in range(n + 1):
            t = i / n
            x, y = base(t)
            amp = 9 * math.sin(math.pi * t) ** 0.4
            y += amp * math.sin(t * math.pi * 18 + k * 2 * math.pi / 3)
            pts.append(f"{x:.1f},{y:.1f}")
        out.append(f'<polyline points="{" ".join(pts)}" stroke="{GOLD}" stroke-opacity="{opac[k]}" '
                   f'stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')

    # deck and hangers
    deck = 330
    out.append(f'<line x1="{xl+22}" y1="{deck}" x2="{xr-22}" y2="{deck}" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.6"/>')
    for i in range(1, 20):
        t = i / 20
        x, y = base(t)
        out.append(f'<line x1="{x:.1f}" y1="{y+10:.1f}" x2="{x:.1f}" y2="{deck}" stroke="{GOLD}" stroke-opacity=".28" stroke-width=".8"/>')

    # back-stays to ground
    for x, d in ((xl, -1), (xr, 1)):
        for s, o in ((0.0, .9), (6, .6), (-6, .45)):
            out.append(f'<path d="M{x},{top} Q{x+d*60},{top+150+s} {x+d*110},{ground}" stroke="{GOLD}" stroke-opacity="{o*0.6:.2f}" '
                       f'stroke-width="1.2" fill="none"/>')

    # unravelled strands below the deck: three single threads that alone would not hold
    labels = [(300, "LIKE"), (450, "TRUST"), (600, "ADMIRE")]
    for x, lab in labels:
        out.append(f'<line x1="{x}" y1="{ground+6}" x2="{x}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{x}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    return "".join(out)
