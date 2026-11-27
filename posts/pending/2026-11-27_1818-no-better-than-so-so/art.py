"""58 years of decisions: most are modest ticks, about a dozen rise tall. Returns SVG inner markup for a 900x520 viewBox."""
import random

GOLD = "#c9a96a"


def build():
    rnd = random.Random(58)
    out = []
    ground = 400
    x0, x1 = 90, 810
    n = 58
    step = (x1 - x0) / (n - 1)
    tall = {4, 9, 13, 19, 23, 28, 31, 36, 41, 45, 50, 55}
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    tops = []
    for i in range(n):
        x = x0 + i * step
        if i in tall:
            h = 120 + 150 * (i / n) + rnd.uniform(-25, 25)
            op, w = 0.9, 2.2
        else:
            h = rnd.uniform(14, 40)
            op, w = rnd.uniform(0.28, 0.45), 1.2
        y = ground - h
        tops.append((x, y))
        out.append(f'<line x1="{x:.1f}" y1="{ground}" x2="{x:.1f}" y2="{y:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity="{op:.2f}" stroke-width="{w}" stroke-linecap="round"/>')
        if i in tall:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="{GOLD}"/>')
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="14" fill="url(#glow)"/>')
    # faint cumulative curve: the few good decisions carry the record
    pts, acc = [], 0.0
    for i, (x, y) in enumerate(tops):
        acc += (ground - y) * (3.0 if i in tall else 0.4)
        pts.append((x, acc))
    m = pts[-1][1]
    d = " ".join(f'{"M" if i == 0 else "L"}{x:.1f},{ground - 20 - 300 * v / m:.1f}' for i, (x, v) in enumerate(pts))
    out.insert(0, f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1.2" stroke-dasharray="2 7" '
                  f'fill="none" stroke-linecap="round"/>')
    for x, lab in ((x0, "1965"), (x1, "2022")):
        out.append(f'<line x1="{x}" y1="{ground+6}" x2="{x}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{x}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".4"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
