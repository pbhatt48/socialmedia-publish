"""Two fortunes moving in lockstep: one path, two lines bound by fine ties. Returns SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"


def path_points(seed, n=120):
    rnd = random.Random(seed)
    pts, y, drift = [], 330.0, 0.0
    for i in range(n + 1):
        x = 80 + 680 * i / n
        drift = drift * 0.85 + rnd.uniform(-11, 11)
        trend = -1.55 * (720 * i / n) / 6.0 / n * 6
        y += drift * 0.35 + trend
        pts.append((x, y))
    # rescale vertical range into a calm, rising band
    ys = [p[1] for p in pts]
    lo, hi = min(ys), max(ys)
    return [(x, 360 - (hi - y) / (hi - lo) * 230) for x, y in pts]


def poly(pts, dy=0):
    return "M" + " L".join(f"{x:.1f},{y + dy:.1f}" for x, y in pts)


def build():
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    pts = path_points(9)
    gap = 14
    # fine ties binding the two lines together
    for i in range(0, len(pts), 4):
        x, y = pts[i]
        out.append(f'<line x1="{x:.1f}" y1="{y - gap/2:.1f}" x2="{x:.1f}" y2="{y + gap/2:.1f}" '
                   f'stroke="{GOLD}" stroke-opacity=".28" stroke-width=".8"/>')
    # faint drop lines to the ground, every few steps
    for i in range(0, len(pts), 12):
        x, y = pts[i]
        out.append(f'<line x1="{x:.1f}" y1="{y + gap/2 + 6:.1f}" x2="{x:.1f}" y2="{ground - 4}" '
                   f'stroke="{GOLD}" stroke-opacity=".1" stroke-width=".8" stroke-dasharray="2 5"/>')
    out.append(f'<path d="{poly(pts, -gap/2)}" stroke="{GOLD}" stroke-opacity=".95" stroke-width="1.8" fill="none" '
               f'stroke-linejoin="round" stroke-linecap="round"/>')
    out.append(f'<path d="{poly(pts, gap/2)}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.8" fill="none" '
               f'stroke-linejoin="round" stroke-linecap="round"/>')
    x0, y0 = pts[0]
    x1, y1 = pts[-1]
    for (x, y) in ((x0, y0), (x1, y1)):
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="30" fill="url(#glow)"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{y - gap/2:.1f}" r="3.6" fill="{GOLD}"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{y + gap/2:.1f}" r="3.6" fill="{GOLD}" fill-opacity=".6"/>')
    out.append(f'<text x="{x1 + 16:.1f}" y="{y1 - gap/2 + 4:.1f}" text-anchor="start" font-family="Inter" font-size="12" '
               f'letter-spacing="3" fill="#8a8578">OURS</text>')
    out.append(f'<text x="{x1 + 16:.1f}" y="{y1 + gap/2 + 4:.1f}" text-anchor="start" font-family="Inter" font-size="12" '
               f'letter-spacing="3" fill="#8a8578">YOURS</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".4"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
