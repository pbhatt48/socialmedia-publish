"""A tangle of theory vs. one plain path to value. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"

def build():
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # start and destination
    sx, sy = 110, ground
    ex, ey = 790, ground
    # tangled path: Lissajous-like knot over the start-to-end span, drawn above
    for k, (a, b, ph, op) in enumerate([(3, 4, 0.0, .42), (5, 3, 0.7, .30), (4, 5, 1.3, .22), (2, 5, 2.1, .16)]):
        pts = []
        n = 420
        for i in range(n + 1):
            t = i / n
            env = math.sin(math.pi * t)
            x = sx + (ex - sx) * t + 70 * env * math.sin(a * 2 * math.pi * t + ph)
            y = sy - 170 * env - 80 * env * math.sin(b * 2 * math.pi * t + ph * 1.7)
            pts.append(f'{x:.1f},{y:.1f}')
        out.append(f'<polyline points="{" ".join(pts)}" stroke="{GOLD}" stroke-opacity="{op}" stroke-width="0.9" fill="none" stroke-linejoin="round"/>')
    # simple path: one clean arc beneath, confident
    out.append(f'<path d="M{sx},{sy} Q{(sx+ex)/2},{ground-90} {ex},{ey}" stroke="{GOLD}" stroke-opacity=".95" stroke-width="2" fill="none" stroke-linecap="round"/>')
    # markers
    out.append(f'<circle cx="{sx}" cy="{sy}" r="4.5" fill="{GOLD}"/>')
    out.append(f'<circle cx="{ex}" cy="{ey}" r="30" fill="url(#glow)"/>')
    out.append(f'<circle cx="{ex}" cy="{ey}" r="7" fill="none" stroke="{GOLD}" stroke-width="1.6"/>')
    out.append(f'<circle cx="{ex}" cy="{ey}" r="2.6" fill="{GOLD}"/>')
    # faint theory labels floating in the tangle
    for x, y, lab in [(270, 175, "BETA"), (450, 120, "MPT"), (630, 170, "OPTIONS"), (360, 255, "EMH")]:
        out.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Inter" font-size="11" letter-spacing="3" fill="#8a8578" fill-opacity=".85">{lab}</text>')
    for tx, lab in [(ex, "VALUE")]:
        out.append(f'<line x1="{tx}" y1="{ground+6}" x2="{tx}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" letter-spacing="3" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
