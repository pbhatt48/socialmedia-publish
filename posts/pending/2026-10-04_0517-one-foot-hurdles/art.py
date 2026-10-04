"""One-foot hurdles stepped over easily; a seven-footer left alone. Returns SVG inner markup for a 900x520 viewBox."""

GOLD = "#c9a96a"


def hurdle(x, ground, h, w, alpha, sw=1.4):
    top = ground - h
    return (f'<line x1="{x}" y1="{ground}" x2="{x}" y2="{top}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="{sw}"/>'
            f'<line x1="{x+w}" y1="{ground}" x2="{x+w}" y2="{top}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="{sw}"/>'
            f'<line x1="{x-4}" y1="{top}" x2="{x+w+4}" y2="{top}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="{sw*2.2:.1f}" stroke-linecap="round"/>'
            f'<line x1="{x-8}" y1="{ground}" x2="{x+6}" y2="{ground}" stroke="{GOLD}" stroke-opacity="{alpha*0.8:.2f}" stroke-width="{sw}"/>'
            f'<line x1="{x+w-6}" y1="{ground}" x2="{x+w+8}" y2="{ground}" stroke="{GOLD}" stroke-opacity="{alpha*0.8:.2f}" stroke-width="{sw}"/>')


def build():
    out = []
    ground = 400
    out.append(f'<line x1="20" y1="{ground}" x2="880" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # lane lines receding
    for i, op in enumerate((.12, .08)):
        y = ground + 26 + i * 22
        out.append(f'<line x1="{60+i*30}" y1="{y}" x2="{840-i*30}" y2="{y}" stroke="{GOLD}" stroke-opacity="{op}" stroke-width="1"/>')

    # five low hurdles, each cleared by a dotted stride arc
    xs = [90, 200, 310, 420, 530]
    w, h = 34, 30
    prev = 40
    for i, x in enumerate(xs):
        out.append(hurdle(x, ground, h, w, 0.55 + i * 0.08))
        mid = x + w / 2
        land = x + w + 40
        out.append(f'<path d="M{prev},{ground-2} Q{mid},{ground-h-70} {land},{ground-2}" stroke="{GOLD}" '
                   f'stroke-opacity=".5" stroke-width="1.2" stroke-dasharray="2 6" fill="none" stroke-linecap="round"/>')
        out.append(f'<circle cx="{land}" cy="{ground-2}" r="2.6" fill="{GOLD}" fill-opacity=".85"/>')
        prev = land

    # the seven-footer, tall and faint, its bar left unattempted
    tx, tw, th = 700, 80, 300
    out.append(hurdle(tx, ground, th, tw, 0.3, sw=1.2))
    for k in range(1, 7):
        y = ground - th * k / 7
        out.append(f'<line x1="{tx+tw+12}" y1="{y:.1f}" x2="{tx+tw+20}" y2="{y:.1f}" stroke="{GOLD}" stroke-opacity=".25" stroke-width="1"/>')
    out.append(f'<line x1="{tx+tw+16}" y1="{ground}" x2="{tx+tw+16}" y2="{ground-th}" stroke="{GOLD}" stroke-opacity=".18" stroke-width="1"/>')
    # path bends away before it, continuing along the ground
    out.append(f'<path d="M{prev+6},{ground-2} L{tx-60},{ground-2}" stroke="{GOLD}" stroke-opacity=".35" '
               f'stroke-width="1.2" stroke-dasharray="2 6" fill="none" stroke-linecap="round"/>')

    glow = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    out.insert(0, f'<ellipse cx="330" cy="{ground-20}" rx="300" ry="90" fill="url(#glow)" opacity=".5"/>')

    for x, lab in ((xs[2] + w / 2, "1 FT"), (tx + tw / 2, "7 FT")):
        out.append(f'<text x="{x}" y="{ground+80}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    return glow + "".join(out)
