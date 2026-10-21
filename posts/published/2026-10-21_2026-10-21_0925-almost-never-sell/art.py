"""Compounding curve that passes every tempting exit: holding a well-chosen business. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"

def build():
    out = []
    ground = 420
    x0, x1 = 90, 810
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # faint grid of decades
    for k in range(5):
        x = x0 + (x1 - x0) * k / 4
        out.append(f'<line x1="{x:.1f}" y1="{ground}" x2="{x:.1f}" y2="70" stroke="{GOLD}" stroke-opacity=".07" stroke-width="1"/>')
    # compounding curve
    def pt(t):
        return x0 + (x1 - x0) * t, ground - 14 - 320 * (math.exp(3.2 * t) - 1) / (math.exp(3.2) - 1)
    pts = [pt(i / 200) for i in range(201)]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    out.append(f'<path d="{d} L{x1},{ground} L{x0},{ground} Z" fill="url(#fade)"/>')
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
    # tempting exits: faint open rings along the early path, never taken
    for t, a in [(0.12, .5), (0.22, .42), (0.33, .36), (0.45, .3), (0.58, .24), (0.72, .18)]:
        x, y = pt(t)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="1" fill="none"/>')
        out.append(f'<line x1="{x:.1f}" y1="{y-10:.1f}" x2="{x:.1f}" y2="{y-34:.1f}" stroke="{GOLD}" stroke-opacity="{a*0.6:.2f}" '
                   f'stroke-width="1" stroke-dasharray="2 4"/>')
    # purchase point: solid seed with glow
    sx, sy = pt(0)
    out.append(f'<circle cx="{sx}" cy="{sy:.1f}" r="26" fill="url(#glow)"/>')
    out.append(f'<circle cx="{sx}" cy="{sy:.1f}" r="5.5" fill="{GOLD}"/>')
    # present point
    ex, ey = pt(1)
    out.append(f'<circle cx="{ex}" cy="{ey:.1f}" r="30" fill="url(#glow)"/>')
    out.append(f'<circle cx="{ex}" cy="{ey:.1f}" r="4.5" fill="{GOLD}"/>')
    labels = [(x0, "BUY"), (x0 + (x1 - x0) / 4, "10"), (x0 + (x1 - x0) / 2, "20"), (x0 + 3 * (x1 - x0) / 4, "30"), (x1, "40 YRS")]
    for tx, lab in labels:
        out.append(f'<line x1="{tx:.1f}" y1="{ground+6}" x2="{tx:.1f}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx:.1f}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GOLD}" stop-opacity=".10"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient></defs>')
    return defs + "".join(out)
