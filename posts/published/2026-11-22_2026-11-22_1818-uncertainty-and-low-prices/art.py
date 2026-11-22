"""Price line moving low through a fog of uncertainty, rising once it clears. 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"

def build():
    rnd = random.Random(5)
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # fog: layered wavy strokes, densest in the middle of the fog band
    fx0, fx1 = 70, 500
    for i in range(34):
        y = rnd.uniform(150, 405)
        x0 = rnd.uniform(fx0, fx0 + 120)
        x1 = rnd.uniform(fx1 - 120, fx1)
        amp = rnd.uniform(3, 9)
        pts = []
        n = 10
        for k in range(n + 1):
            x = x0 + (x1 - x0) * k / n
            pts.append(f"{x:.1f},{y + amp*math.sin(k*1.3 + i):.1f}")
        op = rnd.uniform(0.08, 0.26)
        out.append(f'<polyline points="{" ".join(pts)}" stroke="{GOLD}" stroke-opacity="{op:.2f}" '
                   f'stroke-width="{rnd.uniform(0.6,1.4):.2f}" fill="none" stroke-linecap="round"/>')
    # price path: low and jittery inside fog, rising after it clears
    pts = []
    for k in range(0, 61):
        x = 90 + k * 12.5
        if x < 520:
            y = 360 + 12 * math.sin(k * 0.9) + rnd.uniform(-6, 6)
        else:
            t = (x - 520) / (840 - 520)
            y = 360 - 250 * (t ** 1.3) + rnd.uniform(-5, 5) * (1 - t)
        pts.append((x, y))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".9" stroke-width="2" fill="none" '
               f'stroke-linejoin="round" stroke-linecap="round"/>')
    # buy point inside the fog, and the later price
    bx, by = pts[24]
    ex, ey = pts[-1]
    out.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="22" fill="url(#glow)"/>')
    out.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="4.5" fill="{GOLD}"/>')
    out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4" fill="none" stroke="{GOLD}" stroke-width="1.4"/>')
    out.append(f'<line x1="{bx:.1f}" y1="{by-14:.1f}" x2="{bx:.1f}" y2="{ey:.1f}" stroke="{GOLD}" stroke-opacity=".3" stroke-dasharray="2 6"/>')
    out.append(f'<line x1="{bx:.1f}" y1="{ey:.1f}" x2="{ex-10:.1f}" y2="{ey:.1f}" stroke="{GOLD}" stroke-opacity=".3" stroke-dasharray="2 6"/>')
    # boundary where uncertainty resolves
    out.append(f'<line x1="520" y1="130" x2="520" y2="{ground}" stroke="{GOLD}" stroke-opacity=".22" stroke-width="1"/>')
    for tx, lab in [(285, "UNCERTAIN"), (690, "RESOLVED")]:
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
