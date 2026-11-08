"""Two dives, one simple and one convoluted, landing in identical ripples: degree of difficulty doesn't count."""
import math

GOLD = "#c9a96a"
MUTED = "#8a8578"

def ripples(out, cx, y):
    for i, (rx, op) in enumerate([(14, .9), (30, .6), (48, .38), (68, .2)]):
        out.append(f'<ellipse cx="{cx}" cy="{y + 2 + i}" rx="{rx}" ry="{rx * 0.16:.1f}" fill="none" '
                   f'stroke="{GOLD}" stroke-opacity="{op}" stroke-width="1.1"/>')
    out.append(f'<line x1="{cx}" y1="{y - 4}" x2="{cx}" y2="{y - 22}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1"/>')
    out.append(f'<line x1="{cx - 6}" y1="{y - 3}" x2="{cx - 12}" y2="{y - 16}" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1"/>')
    out.append(f'<line x1="{cx + 6}" y1="{y - 3}" x2="{cx + 12}" y2="{y - 16}" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1"/>')

def build():
    out = []
    water = 400
    # water line
    out.append(f'<line x1="40" y1="{water}" x2="860" y2="{water}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    for k in range(5):
        y = water + 14 + k * 11
        out.append(f'<line x1="{120 + k * 28}" y1="{y}" x2="{780 - k * 28}" y2="{y}" stroke="{GOLD}" '
                   f'stroke-opacity="{.16 - k * .025:.3f}" stroke-width="1" stroke-dasharray="1 9"/>')

    # left: low springboard, one clean arc
    lx = 95
    out.append(f'<line x1="{lx}" y1="{water}" x2="{lx}" y2="300" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.4"/>')
    out.append(f'<line x1="{lx - 15}" y1="300" x2="{lx + 95}" y2="300" stroke="{GOLD}" stroke-width="2"/>')
    out.append(f'<circle cx="{lx + 88}" cy="290" r="3" fill="{GOLD}"/>')
    out.append(f'<path d="M{lx + 88},286 Q{lx + 150},190 {lx + 195},{water - 6}" stroke="{GOLD}" stroke-opacity=".7" '
               f'stroke-width="1.3" fill="none" stroke-dasharray="3 6" stroke-linecap="round"/>')
    ripples(out, lx + 195, water)

    # right: tall platform, convoluted twisting path
    rx = 805
    out.append(f'<line x1="{rx}" y1="{water}" x2="{rx}" y2="80" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.4"/>')
    for y in range(110, water, 40):
        out.append(f'<line x1="{rx - 10}" y1="{y}" x2="{rx + 10}" y2="{y}" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1"/>')
    out.append(f'<line x1="{rx - 110}" y1="80" x2="{rx + 15}" y2="80" stroke="{GOLD}" stroke-width="2"/>')
    out.append(f'<circle cx="{rx - 102}" cy="70" r="3" fill="{GOLD}"/>')
    # looping spiral descent
    pts = []
    sx, sy, ex, ey = rx - 102, 66, rx - 195, water - 6
    n = 400
    for i in range(n + 1):
        t = i / n
        bx = sx + (ex - sx) * t - 55 * math.sin(math.pi * t)
        by = sy + (ey - sy) * t
        amp = 15 * min(1, t * 8, (1 - t) * 8)
        ang = t * math.pi * 2 * 7
        pts.append((bx - amp * 1.25 * math.sin(ang), by - amp * (1 - math.cos(ang))))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.1" fill="none" '
               f'stroke-linejoin="round" stroke-linecap="round"/>')
    ripples(out, ex, water)

    # labels
    def label(x, y, s, anchor="middle"):
        out.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="{MUTED}">{s}</text>')
    label(lx + 40, 284, "1.2")
    label(rx - 47, 64, "3.9")
    label(lx + 195, water + 52, "SAME SPLASH")
    label(ex, water + 52, "SAME SPLASH")
    return "".join(out)
