"""Retained capital piling up: earnings per share climb every year while the
rate earned on the capital stays flat, a stopped clock dressed as a growth
stock. Returns SVG inner markup for a 900x520 viewBox."""
GOLD = "#c9a96a"


def build():
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    cols = 8
    x0, step, w = 110, 70, 34
    tops = []
    for i in range(cols):
        cx = x0 + i * step
        layers = 4 + int(i * 3.2)
        for j in range(layers):
            y = ground - 6 - j * 9
            a = 0.25 + 0.5 * (j / max(layers - 1, 1))
            out.append(f'<line x1="{cx-w/2:.1f}" y1="{y}" x2="{cx+w/2:.1f}" y2="{y}" stroke="{GOLD}" '
                       f'stroke-opacity="{a:.2f}" stroke-width="1.6" stroke-linecap="round"/>')
        top = ground - 6 - (layers - 1) * 9
        cap = 3 + layers * 0.45
        out.append(f'<rect x="{cx-w/2:.1f}" y="{top-8-cap:.1f}" width="{w}" height="{cap:.1f}" rx="1.5" '
                   f'fill="{GOLD}" fill-opacity=".9"/>')
        tops.append((cx, top - 8 - cap))
    pts = " ".join(f"{x:.1f},{y-14:.1f}" for x, y in tops)
    out.append(f'<polyline points="{pts}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.2" '
               f'stroke-dasharray="2 6" fill="none" stroke-linecap="round"/>')
    lx, ly = tops[-1][0], tops[-1][1] - 14
    out.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="3" fill="{GOLD}"/>')
    out.append(f'<text x="{lx-22:.1f}" y="{ly-8:.1f}" text-anchor="end" font-family="Inter" font-size="12" '
               f'letter-spacing="3" fill="#8a8578">EARNINGS PER SHARE</text>')
    # flat rate-of-return line
    ry = 120
    out.append(f'<line x1="{x0-w/2}" y1="{ry}" x2="{x0+(cols-1)*step+w/2}" y2="{ry}" stroke="{GOLD}" '
               f'stroke-opacity=".35" stroke-width="1"/>')
    out.append(f'<text x="{x0-w/2}" y="{ry-12}" font-family="Inter" font-size="12" letter-spacing="3" '
               f'fill="#8a8578">RETURN ON EQUITY · UNCHANGED</text>')
    # stopped clock
    ccx, ccy, r = 770, 300, 46
    out.append(f'<circle cx="{ccx}" cy="{ccy}" r="{r}" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.4" fill="none"/>')
    out.append(f'<circle cx="{ccx}" cy="{ccy}" r="{r-6}" stroke="{GOLD}" stroke-opacity=".25" stroke-width="1" fill="none"/>')
    import math
    for k in range(12):
        a = k * math.pi / 6
        r1 = r - 10 if k % 3 else r - 14
        out.append(f'<line x1="{ccx+r1*math.sin(a):.1f}" y1="{ccy-r1*math.cos(a):.1f}" x2="{ccx+(r-6)*math.sin(a):.1f}" '
                   f'y2="{ccy-(r-6)*math.cos(a):.1f}" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1"/>')
    out.append(f'<line x1="{ccx}" y1="{ccy}" x2="{ccx}" y2="{ccy-30}" stroke="{GOLD}" stroke-width="1.8" stroke-linecap="round"/>')
    out.append(f'<line x1="{ccx}" y1="{ccy}" x2="{ccx+17}" y2="{ccy+10}" stroke="{GOLD}" stroke-width="2.4" stroke-linecap="round"/>')
    out.append(f'<circle cx="{ccx}" cy="{ccy}" r="2.6" fill="{GOLD}"/>')
    out.append(f'<line x1="{ccx}" y1="{ccy+r}" x2="{ccx}" y2="{ground}" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1"/>')
    out.append(f'<text x="{ccx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="12" '
               f'letter-spacing="3" fill="#8a8578">A STOPPED CLOCK</text>')
    out.append(f'<text x="{x0+(cols-1)*step/2:.0f}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="12" '
               f'letter-spacing="3" fill="#8a8578">RETAINED CAPITAL, YEAR BY YEAR</text>')
    return "".join(out)
