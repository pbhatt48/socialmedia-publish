"""Insider buying: many paths lead out of the company, a single one leads in and up."""
import math

GOLD = "#c9a96a"
MUTED = "#8a8578"


def build():
    out = []
    ground = 420
    out.append(f'<line x1="30" y1="{ground}" x2="870" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # The company: a minimal classical facade, centered.
    cx, w, h = 450, 150, 150
    x0, x1, top = cx - w / 2, cx + w / 2, ground - h
    out.append(f'<path d="M{x0-14},{top} L{cx},{top-52} L{x1+14},{top} Z" stroke="{GOLD}" stroke-width="1.4" '
               f'fill="{GOLD}" fill-opacity=".06" stroke-linejoin="round"/>')
    out.append(f'<line x1="{x0-14}" y1="{top+8}" x2="{x1+14}" y2="{top+8}" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.2"/>')
    out.append(f'<line x1="{x0-22}" y1="{ground-6}" x2="{x1+22}" y2="{ground-6}" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.2"/>')
    for i in range(5):
        px = x0 + 8 + i * (w - 16) / 4
        out.append(f'<line x1="{px:.1f}" y1="{top+16}" x2="{px:.1f}" y2="{ground-14}" stroke="{GOLD}" '
                   f'stroke-opacity="{.55 + .1*(i%2):.2f}" stroke-width="2.2" stroke-linecap="round"/>')
    out.append(f'<circle cx="{cx}" cy="{top-22}" r="5" fill="none" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1"/>')

    # Many reasons to sell: faint paths leaving to the left, scattering.
    door_l = (x0 - 22, ground - 12)
    ends = [(60, 395), (75, 320), (110, 250), (165, 190), (240, 150), (205, 290), (290, 230), (140, 360)]
    for k, (ex, ey) in enumerate(ends):
        sx, sy = door_l
        c1x, c1y = sx - 60 - k * 9, sy - 10 - k * 6
        c2x, c2y = ex + 50, ey + 30 - k * 3
        op = 0.28 + 0.07 * (k % 3)
        out.append(f'<path d="M{sx:.1f},{sy:.1f} C{c1x:.1f},{c1y:.1f} {c2x:.1f},{c2y:.1f} {ex},{ey}" stroke="{GOLD}" '
                   f'stroke-opacity="{op:.2f}" stroke-width="1" stroke-dasharray="2 6" fill="none" stroke-linecap="round"/>')
        out.append(f'<circle cx="{ex}" cy="{ey}" r="2.6" fill="{GOLD}" fill-opacity="{op+.2:.2f}"/>')

    # One reason to buy: a single, solid path entering and rising.
    sx, sy = x1 + 22, ground - 12
    pts = [(sx, sy), (600, 360), (700, 270), (790, 150), (835, 95)]
    d = f"M{pts[0][0]},{pts[0][1]}"
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        mx = (ax + bx) / 2
        d += f" C{mx:.1f},{ay} {mx:.1f},{by} {bx},{by}"
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
    tx, ty = pts[-1]
    ang = math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0])
    for da in (2.6, -2.6):
        out.append(f'<line x1="{tx}" y1="{ty}" x2="{tx + 13*math.cos(ang+da):.1f}" y2="{ty + 13*math.sin(ang+da):.1f}" '
                   f'stroke="{GOLD}" stroke-width="2.2" stroke-linecap="round"/>')
    out.append(f'<circle cx="{tx}" cy="{ty}" r="30" fill="url(#glow)"/>')

    # Tiny labels.
    out.append(f'<text x="170" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
               f'letter-spacing="3" fill="{MUTED}">SELL · MANY REASONS</text>')
    out.append(f'<text x="700" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
               f'letter-spacing="3" fill="{MUTED}">BUY · ONE</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".4"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
