"""The herd and the outlier: many paths converge on the average; one departs. Returns SVG inner markup for a 900x520 viewBox."""
import random

GOLD = "#c9a96a"

def build():
    rnd = random.Random(3)
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # consensus point
    cx, cy = 560, 250
    n = 15
    for i in range(n):
        y0 = 120 + i * (260 / (n - 1)) + rnd.uniform(-4, 4)
        x0 = 90
        alpha = 0.18 + 0.32 * (1 - abs(i - n / 2) / (n / 2))
        out.append(f'<path d="M{x0},{y0:.1f} C{x0+220},{y0:.1f} {cx-160},{cy+(y0-cy)*0.12:.1f} {cx},{cy}" '
                   f'stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="1" fill="none" stroke-linecap="round"/>')
    # the average continues as one tight bundle
    for d in (0,):
        out.append(f'<line x1="{cx}" y1="{cy+d}" x2="800" y2="{cy+d}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1.2"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{GOLD}" fill-opacity=".7"/>')
    # the outlier path: departs early, its own way
    out.append(f'<path d="M90,330 C260,330 330,240 420,170 S640,90 790,80" stroke="{GOLD}" stroke-width="2.2" '
               f'fill="none" stroke-linecap="round" stroke-dasharray="1 0"/>')
    out.append(f'<circle cx="790" cy="80" r="22" fill="url(#glow)"/>')
    out.append(f'<circle cx="790" cy="80" r="4.5" fill="{GOLD}"/>')
    out.append(f'<circle cx="90" cy="330" r="3.5" fill="{GOLD}"/>')
    labels = [(cx, ground, "CONSENSUS"), (790, ground, "DIFFERENT")]
    for tx, gy, lab in labels:
        out.append(f'<line x1="{tx}" y1="{gy+6}" x2="{tx}" y2="{gy+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx}" y="{gy+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    for tx in (cx, 790):
        out.append(f'<line x1="{tx}" y1="{ground-4}" x2="{tx}" y2="{ground}" stroke="{GOLD}" stroke-opacity=".5"/>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
