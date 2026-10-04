"""An iceberg: a simple tip above the waterline, a deep, layered mass below. First- vs second-level thinking. SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"

def contour(rnd, cx, top, bottom, half_w, n=40):
    """Closed, gently irregular outline below the waterline, widest near the top third."""
    ph = [rnd.uniform(0, 6.28) for _ in range(4)]
    def wobble(t, side):
        return 1 + 0.07 * math.sin(7 * t + ph[side]) + 0.04 * math.sin(13 * t + ph[side + 2])
    right, left = [], []
    for i in range(n + 1):
        t = i / n
        y = top + (bottom - top) * t
        shape = math.sin(math.pi * (0.5 + 0.5 * t)) ** 0.9 if t > 0.25 else (t / 0.25) ** 0.5 * math.sin(math.pi * 0.625) ** 0.9
        right.append((cx + half_w * shape * wobble(t, 0), y))
        left.append((cx - half_w * shape * wobble(t, 1), y))
    pts = right + list(reversed(left))
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(1, len(pts) - 1):
        mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
        d += f" Q{pts[i][0]:.1f},{pts[i][1]:.1f} {mx:.1f},{my:.1f}"
    return d + " Z"

def build():
    rnd = random.Random(17)
    out = []
    water = 150
    cx = 450
    out.append(f'<line x1="40" y1="{water}" x2="860" y2="{water}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # faint ripples on the surface
    for x0 in (90, 210, 640, 760):
        out.append(f'<path d="M{x0},{water+10} q15,-5 30,0 t30,0" stroke="{GOLD}" stroke-opacity=".18" stroke-width="1" fill="none"/>')
    # the visible tip: simple, few lines
    out.append(f'<path d="M{cx-58},{water} L{cx-22},{water-62} L{cx+4},{water-44} L{cx+26},{water-84} L{cx+66},{water} Z" '
               f'stroke="{GOLD}" stroke-opacity=".95" stroke-width="1.6" fill="{GOLD}" fill-opacity=".08" stroke-linejoin="round"/>')
    out.append(f'<circle cx="{cx+10}" cy="{water-40}" r="60" fill="url(#glow)"/>')
    # the mass below: nested, irregular contours, fading with depth
    layers = 9
    for k in range(layers):
        f = 1 - k / layers
        d = contour(rnd, cx + rnd.uniform(-4, 4), water + 2 + k * 4, water + 40 + 290 * f, 220 * f + 26)
        a = 0.55 - k * 0.045
        out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="{1.2 - k*0.06:.2f}" fill="none" stroke-linejoin="round"/>')
    # inner fracture lines: complexity
    for _ in range(10):
        y = rnd.uniform(water + 40, water + 260)
        x = cx + rnd.uniform(-120, 120) * (1 - (y - water) / 330)
        segs = [(x, y)]
        for _ in range(3):
            x += rnd.uniform(-28, 28); y += rnd.uniform(8, 22)
            segs.append((x, y))
        d = "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in segs)
        out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity="{rnd.uniform(.12,.3):.2f}" stroke-width=".8" fill="none"/>')
    # depth ticks
    for i, y in enumerate(range(water + 40, water + 330, 48)):
        out.append(f'<line x1="790" y1="{y}" x2="800" y2="{y}" stroke="{GOLD}" stroke-opacity="{.45 - i*.05:.2f}"/>')
    out.append(f'<line x1="800" y1="{water}" x2="800" y2="{water+330}" stroke="{GOLD}" stroke-opacity=".2"/>')
    out.append(f'<text x="120" y="{water-14}" font-family="Inter" font-size="13" letter-spacing="3" fill="#8a8578">FIRST LEVEL</text>')
    out.append(f'<text x="120" y="{water+44}" font-family="Inter" font-size="13" letter-spacing="3" fill="#8a8578">SECOND LEVEL</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".3"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
