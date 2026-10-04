"""Balance scale: price paid vs. value received. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"
MUTED = "#8a8578"


def pan(out, cx, top, label, weight):
    # chains
    for dx in (-62, 0, 62):
        out.append(f'<line x1="{cx}" y1="{top-118}" x2="{cx+dx}" y2="{top}" stroke="{GOLD}" '
                   f'stroke-opacity=".45" stroke-width="1"/>')
    # dish
    out.append(f'<path d="M{cx-74},{top} Q{cx},{top+40} {cx+74},{top}" stroke="{GOLD}" stroke-width="1.6" '
               f'fill="{GOLD}" fill-opacity=".06"/>')
    out.append(f'<line x1="{cx-74}" y1="{top}" x2="{cx+74}" y2="{top}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.2"/>')
    out.append(weight(cx, top))
    out.append(f'<text x="{cx}" y="{top+66}" text-anchor="middle" font-family="Inter" font-size="13" '
               f'letter-spacing="4" fill="{MUTED}">{label}</text>')


def coins(cx, top):
    s = []
    for i in range(3):
        y = top - 6 - i * 9
        s.append(f'<ellipse cx="{cx}" cy="{y}" rx="22" ry="5" stroke="{GOLD}" stroke-width="1.2" '
                 f'fill="#14130f" stroke-opacity="{.55 + i*.15:.2f}"/>')
    return "".join(s)


def block(cx, top):
    # a solid little building: the business
    return (f'<path d="M{cx-34},{top-2} L{cx-34},{top-44} L{cx},{top-66} L{cx+34},{top-44} L{cx+34},{top-2}" '
            f'stroke="{GOLD}" stroke-width="1.5" fill="{GOLD}" fill-opacity=".12"/>'
            + "".join(f'<line x1="{cx+dx}" y1="{top-40}" x2="{cx+dx}" y2="{top-4}" stroke="{GOLD}" '
                      f'stroke-opacity=".55" stroke-width="1"/>' for dx in (-20, -7, 7, 20)))


def build():
    out = []
    ground = 440
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    cx, pivot = 450, 120
    # base and column
    out.append(f'<path d="M{cx-70},{ground} L{cx-40},{ground-16} L{cx+40},{ground-16} L{cx+70},{ground} Z" '
               f'fill="{GOLD}" fill-opacity=".8"/>')
    out.append(f'<path d="M{cx-5},{ground-16} L{cx-3},{pivot+6} L{cx+3},{pivot+6} L{cx+5},{ground-16} Z" '
               f'fill="{GOLD}" fill-opacity=".85"/>')
    # beam tilted: value side (right) heavier, sits lower
    tilt = math.radians(5)
    half = 230
    lx, ly = cx - half * math.cos(tilt), pivot - half * math.sin(tilt)
    rx, ry = cx + half * math.cos(tilt), pivot + half * math.sin(tilt)
    out.append(f'<line x1="{lx:.1f}" y1="{ly:.1f}" x2="{rx:.1f}" y2="{ry:.1f}" stroke="{GOLD}" stroke-width="3" stroke-linecap="round"/>')
    out.append(f'<circle cx="{cx}" cy="{pivot}" r="7" fill="#14130f" stroke="{GOLD}" stroke-width="1.6"/>')
    out.append(f'<circle cx="{cx}" cy="{pivot}" r="40" fill="url(#glow)"/>')
    out.append(f'<path d="M{cx},{pivot-12} L{cx-6},{pivot-34} L{cx+6},{pivot-34} Z" fill="{GOLD}" fill-opacity=".7"/>')
    for x, y in ((lx, ly), (rx, ry)):
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{GOLD}"/>')
    pan(out, round(lx), round(ly) + 118, "PRICE", coins)
    pan(out, round(rx), round(ry) + 118, "VALUE", block)
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
