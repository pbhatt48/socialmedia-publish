"""The life of a bull market: born at the trough, dying at the peak of euphoria.
Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"
GREY = "#8a8578"


def curve_y(x):
    # trough near x=150, steady climb, crest near x=690, then a steep fall
    if x <= 690:
        t = (x - 60) / 630
        base = 360 - 270 * (t ** 1.55)
        dip = 28 * math.exp(-((x - 150) / 55) ** 2)
        return base + dip
    t = (x - 690) / 150
    return 90 + 300 * (t ** 1.4)


def build():
    out = []
    ground = 420
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GOLD}" stop-opacity=".14"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient></defs>')
    out.append(f'<line x1="30" y1="{ground}" x2="870" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    xs = list(range(60, 841, 4))
    pts = [(x, curve_y(x)) for x in xs]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    # soft area under the curve
    out.append(f'<path d="{d} L840,{ground} L60,{ground} Z" fill="url(#fade)"/>')
    # faint echo lines (the crowd)
    for i, op in ((1, .18), (2, .1)):
        dd = "M" + " L".join(f"{x:.1f},{y + 10 * i:.1f}" for x, y in pts)
        out.append(f'<path d="{dd}" stroke="{GOLD}" stroke-opacity="{op}" stroke-width=".8" fill="none"/>')
    # main line: rising part solid, falling part dashed
    rise = [p for p in pts if p[0] <= 690]
    fall = [p for p in pts if p[0] >= 690]
    out.append('<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in rise) +
               f'" stroke="{GOLD}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    out.append('<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in fall) +
               f'" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1.4" stroke-dasharray="3 6" fill="none" stroke-linecap="round"/>')
    stages = [(150, "PESSIMISM", 1.0), (340, "SKEPTICISM", .8), (530, "OPTIMISM", .65), (690, "EUPHORIA", .45)]
    for x, lab, op in stages:
        y = curve_y(x)
        out.append(f'<line x1="{x}" y1="{y + 8:.1f}" x2="{x}" y2="{ground}" stroke="{GOLD}" stroke-opacity=".22" '
                   f'stroke-width="1" stroke-dasharray="1 5"/>')
        out.append(f'<circle cx="{x}" cy="{y:.1f}" r="4.5" fill="{GOLD}" fill-opacity="{op:.2f}"/>')
        out.append(f'<line x1="{x}" y1="{ground + 6}" x2="{x}" y2="{ground + 14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{x}" y="{ground + 40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="{GREY}">{lab}</text>')
    # birth glow at the trough, burst rays at the euphoric crest
    out.append(f'<circle cx="150" cy="{curve_y(150):.1f}" r="34" fill="url(#glow)"/>')
    cy = curve_y(690)
    for k in range(9):
        a = math.pi * (0.1 + 0.8 * k / 8)
        x1, y1 = 690 + 12 * math.cos(a), cy - 12 * math.sin(a)
        x2, y2 = 690 + 24 * math.cos(a), cy - 24 * math.sin(a)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity=".4" stroke-width="1" stroke-linecap="round"/>')
    return defs + "".join(out)
