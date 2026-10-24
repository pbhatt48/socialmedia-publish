"""A balance held level: price (p/e) on one pan, growth on the other. Returns SVG inner markup for a 900x520 viewBox."""

GOLD = "#c9a96a"


def pan(out, cx, top, label):
    # three fine chains down to a shallow dish
    dish_y = top + 120
    for dx in (-52, 0, 52):
        out.append(f'<line x1="{cx}" y1="{top}" x2="{cx + dx}" y2="{dish_y}" stroke="{GOLD}" '
                   f'stroke-opacity="{.5 if dx else .3}" stroke-width=".9"/>')
    out.append(f'<path d="M{cx - 70},{dish_y} Q{cx},{dish_y + 34} {cx + 70},{dish_y}" stroke="{GOLD}" '
               f'stroke-opacity=".9" stroke-width="1.6" fill="none" stroke-linecap="round"/>')
    out.append(f'<line x1="{cx - 70}" y1="{dish_y}" x2="{cx + 70}" y2="{dish_y}" stroke="{GOLD}" '
               f'stroke-opacity=".35" stroke-width=".8"/>')
    out.append(f'<text x="{cx}" y="{dish_y + 62}" text-anchor="middle" font-family="Inter" font-size="12" '
               f'letter-spacing="3" fill="#8a8578">{label}</text>')
    return dish_y


def build():
    out = []
    ground = 440
    cx, beam_y = 450, 120
    out.append(f'<line x1="60" y1="{ground}" x2="840" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # pillar and base
    out.append(f'<line x1="{cx}" y1="{beam_y}" x2="{cx}" y2="{ground - 14}" stroke="{GOLD}" stroke-opacity=".85" stroke-width="2.2"/>')
    out.append(f'<path d="M{cx - 70},{ground} L{cx - 40},{ground - 14} L{cx + 40},{ground - 14} L{cx + 70},{ground} Z" '
               f'fill="{GOLD}" fill-opacity=".18" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1"/>')
    # level beam
    left, right = cx - 230, cx + 230
    out.append(f'<line x1="{left}" y1="{beam_y}" x2="{right}" y2="{beam_y}" stroke="{GOLD}" stroke-opacity=".95" '
               f'stroke-width="2" stroke-linecap="round"/>')
    for x in (left, right):
        out.append(f'<circle cx="{x}" cy="{beam_y}" r="3.2" fill="{GOLD}"/>')
    # fulcrum glow and pointer
    out.append(f'<circle cx="{cx}" cy="{beam_y}" r="36" fill="url(#glow)"/>')
    out.append(f'<path d="M{cx},{beam_y - 30} L{cx - 7},{beam_y - 6} L{cx + 7},{beam_y - 6} Z" fill="{GOLD}"/>')
    out.append(f'<circle cx="{cx}" cy="{beam_y}" r="5" fill="#0f0f0f" stroke="{GOLD}" stroke-width="1.5"/>')
    # faint level guide
    out.append(f'<line x1="{left - 50}" y1="{beam_y}" x2="{left - 14}" y2="{beam_y}" stroke="{GOLD}" '
               f'stroke-opacity=".25" stroke-dasharray="2 5"/>')
    out.append(f'<line x1="{right + 14}" y1="{beam_y}" x2="{right + 50}" y2="{beam_y}" stroke="{GOLD}" '
               f'stroke-opacity=".25" stroke-dasharray="2 5"/>')
    dl = pan(out, left, beam_y, "P/E")
    dr = pan(out, right, beam_y, "GROWTH")
    # contents: stacked bars (price multiple) vs rising steps (growth), equal in weight
    for i in range(4):
        w = 64 - i * 10
        out.append(f'<rect x="{left - w / 2}" y="{dl - 10 - i * 11}" width="{w}" height="7" fill="{GOLD}" '
                   f'fill-opacity="{.75 - i * .12:.2f}"/>')
    for i in range(5):
        h = 8 + i * 8
        out.append(f'<rect x="{right - 46 + i * 19}" y="{dr - 4 - h}" width="11" height="{h}" fill="{GOLD}" '
                   f'fill-opacity="{.4 + i * .1:.2f}"/>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".4"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
