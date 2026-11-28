"""Price vs value: a restless price line oscillating around a calm, steadily rising value line.
Marked points where price falls well below value: where the investor acquires and holds."""
import math, random

GOLD = "#c9a96a"

def build():
    rnd = random.Random(8)
    out = []
    ground = 430
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    x0, x1 = 70, 830
    def value(x):
        t = (x - x0) / (x1 - x0)
        return 360 - 230 * (t ** 1.25)
    # value line (smooth, steady)
    vpts = " ".join(f"{x:.1f},{value(x):.1f}" for x in range(x0, x1 + 1, 6))
    out.append(f'<polyline points="{vpts}" stroke="{GOLD}" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-opacity=".95"/>')
    # price line (restless)
    pts, dips = [], []
    phase = 0.0
    for i, x in enumerate(range(x0, x1 + 1, 5)):
        t = (x - x0) / (x1 - x0)
        amp = 44 + 10 * math.sin(t * 5)
        osc = amp * math.sin(t * 2 * math.pi * 3.2 + 0.6) + 12 * math.sin(t * 47) + rnd.uniform(-6, 6)
        y = value(x) - osc
        pts.append((x, y))
    out.append('<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) +
               f'" stroke="{GOLD}" stroke-opacity=".42" stroke-width="1.1" fill="none" stroke-linejoin="round"/>')
    # find local maxima of (y - value) => price far below value
    gaps = [y - value(x) for x, y in pts]
    for i in range(6, len(pts) - 6):
        if gaps[i] == max(gaps[i-6:i+7]) and gaps[i] > 40:
            x, y = pts[i]
            v = value(x)
            out.append(f'<line x1="{x:.1f}" y1="{v:.1f}" x2="{x:.1f}" y2="{y:.1f}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1" stroke-dasharray="2 4"/>')
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="url(#glow)"/>')
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="{GOLD}"/>')
    # labels
    out.append(f'<text x="{x0}" y="{ground+38}" text-anchor="start" font-family="Inter" font-size="13" letter-spacing="3" fill="#8a8578">PRICE FLUCTUATES</text>')
    out.append(f'<text x="{x1}" y="{ground+38}" text-anchor="end" font-family="Inter" font-size="13" letter-spacing="3" fill="#8a8578">VALUE COMPOUNDS</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".5"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
