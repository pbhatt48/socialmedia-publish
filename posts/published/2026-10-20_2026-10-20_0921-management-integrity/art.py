"""Plumb line beside a true column: integrity as structure that holds. Returns SVG inner markup for a 900x520 viewBox."""

GOLD = "#c9a96a"

def line(x1, y1, x2, y2, a=0.9, w=1.2, extra=""):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GOLD}" '
            f'stroke-opacity="{a:.2f}" stroke-width="{w}" stroke-linecap="round"{extra}/>')

def column(out, cx, base, height, width, a):
    top = base - height
    hw = width / 2
    # stylobate steps
    for i, (sw, sh) in enumerate([(1.9, 0), (1.6, 10), (1.35, 20)]):
        y = base - sh
        out.append(line(cx - hw * sw, y, cx + hw * sw, y, a * 0.8, 1.1))
        out.append(line(cx - hw * sw, y, cx - hw * sw, y - 10, a * 0.6, 1))
        out.append(line(cx + hw * sw, y, cx + hw * sw, y - 10, a * 0.6, 1))
    shaft_b = base - 30
    shaft_t = top + 34
    # torus base
    out.append(f'<path d="M{cx-hw*1.2},{shaft_b} Q{cx},{shaft_b-14} {cx+hw*1.2},{shaft_b}" stroke="{GOLD}" '
               f'stroke-opacity="{a*0.8:.2f}" stroke-width="1.1" fill="none"/>')
    # shaft with slight entasis and flutes
    out.append(f'<path d="M{cx-hw},{shaft_b-6} C{cx-hw*1.04},{shaft_b-120} {cx-hw*0.9},{shaft_t+60} {cx-hw*0.86},{shaft_t}" '
               f'stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="1.4" fill="none"/>')
    out.append(f'<path d="M{cx+hw},{shaft_b-6} C{cx+hw*1.04},{shaft_b-120} {cx+hw*0.9},{shaft_t+60} {cx+hw*0.86},{shaft_t}" '
               f'stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="1.4" fill="none"/>')
    for k in range(1, 6):
        f = k / 6 * 2 - 1
        out.append(line(cx + f * hw * 0.93, shaft_b - 8, cx + f * hw * 0.82, shaft_t + 2, a * 0.35, 0.8))
    # capital
    out.append(line(cx - hw * 1.05, shaft_t, cx + hw * 1.05, shaft_t, a, 1.2))
    out.append(f'<path d="M{cx-hw*1.05},{shaft_t} Q{cx},{shaft_t-22} {cx+hw*1.05},{shaft_t}" stroke="{GOLD}" '
               f'stroke-opacity="{a*0.8:.2f}" stroke-width="1.1" fill="none"/>')
    for s in (-1, 1):
        vx = cx + s * hw * 1.28
        out.append(f'<circle cx="{vx}" cy="{shaft_t-14}" r="8" stroke="{GOLD}" stroke-opacity="{a*0.8:.2f}" stroke-width="1" fill="none"/>'
                   f'<circle cx="{vx}" cy="{shaft_t-14}" r="3" stroke="{GOLD}" stroke-opacity="{a*0.6:.2f}" stroke-width="0.9" fill="none"/>')
    out.append(f'<rect x="{cx-hw*1.55}" y="{top}" width="{hw*3.1}" height="12" stroke="{GOLD}" '
               f'stroke-opacity="{a:.2f}" stroke-width="1.2" fill="none"/>')
    return top

def build():
    out = []
    ground = 430
    out.append(line(40, ground, 860, ground, 0.45, 1))
    # faint foundation hatching below ground
    for i in range(14):
        x = 300 + i * 22
        out.append(line(x, ground + 4, x - 14, ground + 22, 0.14, 0.8))
    cx = 420
    top = column(out, cx, ground, 330, 70, 0.9)
    # architrave fragment resting on column
    out.append(line(cx - 150, top, cx + 210, top, 0.55, 1.1))
    out.append(line(cx - 150, top - 18, cx + 210, top - 18, 0.55, 1.1))
    out.append(line(cx - 150, top, cx - 150, top - 18, 0.4, 1))
    # plumb line hanging from the architrave, true vertical
    px = 580
    bob_y = 372
    out.append(f'<circle cx="{px}" cy="{top}" r="3" fill="{GOLD}" fill-opacity=".9"/>')
    out.append(line(px, top, px, bob_y - 18, 0.75, 0.9))
    out.append(f'<path d="M{px-9},{bob_y-18} L{px+9},{bob_y-18} L{px+9},{bob_y-10} L{px},{bob_y+14} L{px-9},{bob_y-10} Z" '
               f'fill="{GOLD}" fill-opacity=".85"/>')
    out.append(f'<circle cx="{px}" cy="{bob_y}" r="30" fill="url(#glow)"/>')
    # dashed alignment guide: the column's axis is parallel to the plumb
    out.append(line(cx, top - 40, cx, ground + 34, 0.22, 1, ' stroke-dasharray="2 7"'))
    out.append(line(px, bob_y + 22, px, ground + 34, 0.22, 1, ' stroke-dasharray="2 7"'))
    # right-angle marker at ground
    out.append(f'<path d="M{px+14},{ground} L{px+14},{ground-14} L{px},{ground-14}" stroke="{GOLD}" '
               f'stroke-opacity=".5" stroke-width="1" fill="none"/>')
    out.append(f'<text x="{px+28}" y="{bob_y+6}" font-family="Inter" font-size="12" letter-spacing="3" '
               f'fill="#8a8578">TRUE</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".4"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
