"""Org chart under measurement: every node is checked by a gauge from the node above,
except the top one, whose evaluator is an empty dashed outline. Returns SVG inner markup for 900x520."""
GOLD = "#c9a96a"
MUTED = "#8a8578"


def node(out, x, y, r, alpha, fill=0.0):
    out.append(f'<circle cx="{x}" cy="{y}" r="{r}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" '
               f'stroke-width="1.4" fill="{GOLD}" fill-opacity="{fill:.2f}"/>')


def link(out, x1, y1, x2, y2, alpha):
    my = (y1 + y2) / 2
    out.append(f'<path d="M{x1},{y1} L{x1},{my} L{x2},{my} L{x2},{y2}" stroke="{GOLD}" '
               f'stroke-opacity="{alpha:.2f}" stroke-width="1" fill="none"/>')


def gauge(out, x, y, alpha, r=7):
    # small dial beside a node: being measured
    out.append(f'<path d="M{x-r},{y} A{r},{r} 0 0 1 {x+r},{y}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" '
               f'stroke-width="1" fill="none"/>')
    out.append(f'<line x1="{x}" y1="{y}" x2="{x+r*0.45:.1f}" y2="{y-r*0.8:.1f}" stroke="{GOLD}" '
               f'stroke-opacity="{alpha:.2f}" stroke-width="1" stroke-linecap="round"/>')


def build():
    out = []
    ground = 440
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".4" stroke-width="1"/>')

    cx = 450
    top_y = 150
    mid_y = 255
    low_y = 360

    # empty evaluator above the CEO
    out.append(f'<circle cx="{cx}" cy="50" r="16" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1" '
               f'stroke-dasharray="2 5" fill="none" stroke-linecap="round"/>')
    out.append(f'<line x1="{cx}" y1="66" x2="{cx}" y2="{top_y-22}" stroke="{GOLD}" stroke-opacity=".25" '
               f'stroke-width="1" stroke-dasharray="2 6" stroke-linecap="round"/>')

    # CEO
    out.append(f'<circle cx="{cx}" cy="{top_y}" r="44" fill="url(#glow)"/>')
    node(out, cx, top_y, 20, 0.95, 0.55)

    mids = [250, 450, 650]
    lows = {250: [180, 250, 320], 450: [395, 450, 505], 650: [580, 650, 720]}
    for mx in mids:
        link(out, cx, top_y + 20, mx, mid_y - 13, 0.55)
        node(out, mx, mid_y, 13, 0.8, 0.12)
        gauge(out, mx + 28, mid_y + 4, 0.6, 8)
        for lx in lows[mx]:
            link(out, mx, mid_y + 13, lx, low_y - 9, 0.35)
            node(out, lx, low_y, 9, 0.6, 0.06)
            gauge(out, lx + 19, low_y + 3, 0.45, 6)

    out.append(f'<text x="{cx}" y="{ground+34}" text-anchor="middle" font-family="Inter" font-size="12" '
               f'letter-spacing="4" fill="{MUTED}">MEASURED BY WHOM?</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
