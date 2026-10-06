"""Air reserve on the seabed, bubbles rising to the surface: cash as oxygen. Returns SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"

def build():
    rnd = random.Random(14)
    out = []
    surface, floor = 90, 440
    # water surface: a few gentle swell lines
    for i, op in enumerate((.5, .22, .12)):
        y = surface + i * 12
        pts = " ".join(f"{x},{y + 3*math.sin(x/38 + i*1.3):.1f}" for x in range(40, 861, 10))
        out.append(f'<polyline points="{pts}" stroke="{GOLD}" stroke-opacity="{op}" stroke-width="1" fill="none"/>')
    # sea floor
    out.append(f'<line x1="40" y1="{floor}" x2="860" y2="{floor}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    for x in range(70, 840, 46):
        out.append(f'<line x1="{x}" y1="{floor+8}" x2="{x+14}" y2="{floor+8}" stroke="{GOLD}" stroke-opacity=".14" stroke-width="1"/>')
    # air cylinder resting on the floor
    cx, w, h = 450, 64, 150
    top = floor - h
    out.append(f'<rect x="{cx-w/2}" y="{top}" width="{w}" height="{h}" rx="30" fill="{GOLD}" fill-opacity=".06" '
               f'stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.6"/>')
    for k in range(1, 8):
        y = top + 26 + k * 15
        out.append(f'<line x1="{cx-w/2+8}" y1="{y}" x2="{cx+w/2-8}" y2="{y}" stroke="{GOLD}" stroke-opacity="{.08+.03*k:.2f}" stroke-width="1"/>')
    out.append(f'<rect x="{cx-9}" y="{top-16}" width="18" height="16" fill="none" stroke="{GOLD}" stroke-opacity=".85" stroke-width="1.4"/>'
               f'<line x1="{cx-16}" y1="{top-20}" x2="{cx+16}" y2="{top-20}" stroke="{GOLD}" stroke-width="1.8" stroke-linecap="round"/>'
               f'<circle cx="{cx+22}" cy="{top-20}" r="5" fill="none" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.2"/>')
    out.append(f'<circle cx="{cx}" cy="{top+60}" r="90" fill="url(#glow)"/>')
    # bubble stream rising from the valve to the surface
    y = top - 30
    while y > surface + 30:
        t = (top - 30 - y) / (top - 30 - surface)
        x = cx + 26 * math.sin(y / 34) * (0.3 + t) + rnd.uniform(-4, 4)
        r = 2 + 9 * t + rnd.uniform(-1, 1.5)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="none" stroke="{GOLD}" '
                   f'stroke-opacity="{.9 - .55*t:.2f}" stroke-width="{1.4 - .5*t:.2f}"/>')
        out.append(f'<path d="M{x - r*.5:.1f},{y - r*.2:.1f} a{r*.55:.1f},{r*.55:.1f} 0 0 1 {r*.4:.1f},{-r*.4:.1f}" '
                   f'stroke="{GOLD}" stroke-opacity="{.6 - .3*t:.2f}" stroke-width=".8" fill="none"/>')
        y -= 16 + 22 * t
    # faint stray bubbles for depth
    for _ in range(18):
        bx, by = rnd.uniform(110, 790), rnd.uniform(surface + 40, floor - 30)
        if abs(bx - cx) < 90:
            continue
        out.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="{rnd.uniform(1.2, 3.5):.1f}" fill="none" stroke="{GOLD}" '
                   f'stroke-opacity="{rnd.uniform(.12, .3):.2f}" stroke-width=".8"/>')
    for tx, ty, lab in ((cx, floor + 40, "RESERVE"), (cx, surface - 26, "SURFACE")):
        out.append(f'<text x="{tx}" y="{ty}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".22"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
