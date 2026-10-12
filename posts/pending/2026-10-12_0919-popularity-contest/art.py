"""Crowd converging on a peak: popularity concentrates attention, and the summit is the riskiest place to buy.
Returns SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"


def hill(x):
    # smooth popularity curve peaking at x=450
    return 400 - 300 * math.exp(-((x - 450) / 120) ** 2)


def build():
    out = []
    ground = 400
    rnd = random.Random(5)
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # nested contour curves of the popularity hill
    for k, (scale, op) in enumerate([(1.0, .9), (0.82, .45), (0.64, .3), (0.46, .2), (0.28, .12)]):
        pts = []
        for i in range(0, 161):
            x = 110 + i * 680 / 160
            y = ground - (ground - hill(x)) * scale
            pts.append(f"{x:.1f},{y:.1f}")
        w = 1.6 if k == 0 else 1
        out.append(f'<polyline points="{" ".join(pts)}" stroke="{GOLD}" stroke-opacity="{op}" stroke-width="{w}" fill="none" stroke-linecap="round"/>')
    peak_y = hill(450)
    # the crowd: small dots on the ground, each drawing a faint sight-line to the summit
    for i in range(34):
        x = 70 + i * 760 / 33 + rnd.uniform(-6, 6)
        d = abs(x - 450) / 380
        op = 0.08 + 0.22 * (1 - d)
        out.append(f'<line x1="{x:.1f}" y1="{ground+18}" x2="450" y2="{peak_y+4:.1f}" stroke="{GOLD}" stroke-opacity="{op:.2f}" stroke-width=".6"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{ground+18}" r="2.2" fill="{GOLD}" fill-opacity="{0.4+0.5*(1-d):.2f}"/>')
    # glow and marker at the peak
    out.append(f'<circle cx="450" cy="{peak_y:.1f}" r="34" fill="url(#glow)"/>')
    out.append(f'<circle cx="450" cy="{peak_y:.1f}" r="5" fill="{GOLD}"/>')
    out.append(f'<circle cx="450" cy="{peak_y:.1f}" r="11" stroke="{GOLD}" stroke-opacity=".6" fill="none"/>')
    out.append(f'<text x="450" y="{peak_y-26:.1f}" text-anchor="middle" font-family="Inter" font-size="12" '
               f'letter-spacing="3" fill="#8a8578">PEAK POPULARITY</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
