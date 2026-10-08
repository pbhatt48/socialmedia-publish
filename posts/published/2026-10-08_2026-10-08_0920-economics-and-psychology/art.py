"""Two overlapping circles: a measured ledger of value (economics) and a restless wave of mood (psychology).
Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"

def build():
    out = []
    ground = 440
    r = 165
    lx, rx, cy = 340, 560, 255
    defs = (f'<defs><clipPath id="L"><circle cx="{lx}" cy="{cy}" r="{r}"/></clipPath>'
            f'<clipPath id="R"><circle cx="{rx}" cy="{cy}" r="{r}"/></clipPath>'
            f'<radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".30"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # economics: a steady, rising staircase of value bars inside the left circle
    bars = []
    for i in range(14):
        x = lx - r + 20 + i * 22
        h = 40 + i * 13
        bars.append(f'<line x1="{x}" y1="{cy+r}" x2="{x}" y2="{cy+r-h}" stroke="{GOLD}" stroke-opacity="{0.18+0.025*i:.2f}" stroke-width="1.2"/>')
    trend = " ".join(f"{lx-r+20+i*22},{cy+r-40-i*13}" for i in range(14))
    bars.append(f'<polyline points="{trend}" stroke="{GOLD}" stroke-opacity=".75" stroke-width="1.4" fill="none"/>')
    out.append(f'<g clip-path="url(#L)">{"".join(bars)}</g>')
    # psychology: oscillating waves of sentiment inside the right circle
    waves = []
    for k, (amp, alpha, off) in enumerate([(70, .75, 0), (48, .45, 0.9), (28, .28, 1.8)]):
        pts = []
        for j in range(0, 341, 4):
            x = rx - r - 5 + j
            y = cy + amp * math.sin(j / 340 * 4.4 * math.pi + off) * (0.55 + 0.45 * math.sin(j / 120))
            pts.append(f"{x:.1f},{y:.1f}")
        waves.append(f'<polyline points="{" ".join(pts)}" stroke="{GOLD}" stroke-opacity="{alpha}" stroke-width="{1.4-0.3*k:.1f}" fill="none" stroke-linejoin="round"/>')
    out.append(f'<g clip-path="url(#R)">{"".join(waves)}</g>')
    # the circles and their lens-shaped intersection
    out.append(f'<circle cx="{lx}" cy="{cy}" r="{r}" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.3" fill="none"/>')
    out.append(f'<circle cx="{rx}" cy="{cy}" r="{r}" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.3" fill="none"/>')
    mx = (lx + rx) / 2
    out.append(f'<g clip-path="url(#L)"><circle cx="{rx}" cy="{cy}" r="{r}" fill="{GOLD}" fill-opacity=".07"/></g>')
    out.append(f'<circle cx="{mx}" cy="{cy}" r="60" fill="url(#glow)"/>')
    out.append(f'<circle cx="{mx}" cy="{cy}" r="5" fill="{GOLD}"/>')
    out.append(f'<line x1="{mx}" y1="{cy+r-30}" x2="{mx}" y2="{ground-6}" stroke="{GOLD}" stroke-opacity=".35" stroke-dasharray="2 6"/>')
    for tx, lab in [(lx - 60, "ECONOMICS"), (rx + 60, "PSYCHOLOGY")]:
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    return defs + "".join(out)
