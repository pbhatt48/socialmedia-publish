"""A long field of stones, most turned over and empty; one reveals a gold find. Diligence as a numbers game.
Returns SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"

def stone_path(cx, cy, w, h, rnd, rot=0.0):
    # irregular rounded stone, flat-ish bottom
    pts = []
    n = 9
    for i in range(n):
        a = math.pi + math.pi * i / (n - 1)  # upper half, left to right
        r = 1 + rnd.uniform(-0.12, 0.1)
        pts.append((w / 2 * math.cos(a) * r, h * math.sin(a) * r))
    pts.append((w / 2 * 0.9, 0))
    pts.append((-w / 2 * 0.9, 0))
    c, s = math.cos(rot), math.sin(rot)
    tp = [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]
    d = f"M{tp[0][0]:.1f},{tp[0][1]:.1f} "
    for i in range(1, len(tp)):
        mx = (tp[i - 1][0] + tp[i][0]) / 2
        my = (tp[i - 1][1] + tp[i][1]) / 2
        d += f"Q{tp[i-1][0]:.1f},{tp[i-1][1]:.1f} {mx:.1f},{my:.1f} "
    return d + "Z"

def build():
    rnd = random.Random(42)
    out = []
    ground = 420
    # distant field: rows of small unturned stones receding toward a faint horizon
    for row, (y, scale, op, n) in enumerate(((120, 0.24, .12, 26), (172, 0.32, .15, 22), (228, 0.44, .19, 18), (290, 0.6, .24, 14), (350, 0.78, .29, 11))):
        out.append(f'<line x1="70" y1="{y}" x2="830" y2="{y}" stroke="{GOLD}" stroke-opacity="{op*0.8:.2f}" stroke-width=".7"/>')
        step = 740 / n
        for k in range(n):
            x = 80 + step * (k + 0.5) + rnd.uniform(-step * 0.2, step * 0.2)
            w = rnd.uniform(40, 60) * scale
            h = rnd.uniform(20, 30) * scale
            out.append(f'<path d="{stone_path(x, y, w, h, rnd)}" stroke="{GOLD}" stroke-opacity="{op:.2f}" '
                       f'stroke-width=".9" fill="none" stroke-linejoin="round"/>')
    # foreground: the stones already turned, and the one that paid off
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    xs = [100, 215, 330, 445, 560, 690, 810]
    find = 5
    for i, x in enumerate(xs):
        w = rnd.uniform(70, 86)
        h = rnd.uniform(34, 44)
        if i < find:
            out.append(f'<path d="M{x-w/2:.1f},{ground} Q{x:.1f},{ground+16:.1f} {x+w/2:.1f},{ground}" '
                       f'stroke="{GOLD}" stroke-opacity=".3" stroke-width="1" fill="none"/>')
            out.append(f'<path d="{stone_path(x + w*0.4, ground, w*0.9, h, rnd, rot=0.55)}" '
                       f'stroke="{GOLD}" stroke-opacity="{0.4 + 0.08*i:.2f}" stroke-width="1.4" fill="none" stroke-linejoin="round"/>')
        elif i == find:
            gx, gy = x - 6, ground - 8
            out.append(f'<circle cx="{gx}" cy="{gy}" r="95" fill="url(#glow)"/>')
            out.append(f'<path d="M{x-w/2-8:.1f},{ground} Q{x:.1f},{ground+22:.1f} {x+w/2+2:.1f},{ground}" '
                       f'stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.2" fill="none"/>')
            s = 1.5
            out.append(f'<path d="M{gx-11*s},{gy-8*s} L{gx+11*s},{gy-8*s} L{gx+16*s},{gy-2*s} L{gx},{gy+12*s} L{gx-16*s},{gy-2*s} Z" '
                       f'fill="{GOLD}" fill-opacity=".92"/>')
            out.append(f'<path d="M{gx-16*s},{gy-2*s} L{gx+16*s},{gy-2*s} M{gx-11*s},{gy-8*s} L{gx-5*s},{gy-2*s} L{gx},{gy+12*s} '
                       f'L{gx+5*s},{gy-2*s} L{gx+11*s},{gy-8*s} M{gx-5*s},{gy-2*s} L{gx},{gy-8*s} L{gx+5*s},{gy-2*s}" '
                       f'stroke="#1a1814" stroke-opacity=".45" stroke-width=".9" fill="none"/>')
            out.append(f'<path d="{stone_path(x + w*0.62, ground, w*1.0, h*1.05, rnd, rot=1.2)}" '
                       f'stroke="{GOLD}" stroke-opacity=".95" stroke-width="1.7" fill="none" stroke-linejoin="round"/>')
            for a in (-0.9, -0.45, 0, 0.45, 0.9):
                ang = -math.pi / 2 + a
                out.append(f'<line x1="{gx + 38*math.cos(ang):.1f}" y1="{gy + 38*math.sin(ang):.1f}" '
                           f'x2="{gx + 56*math.cos(ang):.1f}" y2="{gy + 56*math.sin(ang):.1f}" '
                           f'stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.1" stroke-linecap="round"/>')
        else:
            out.append(f'<path d="{stone_path(x, ground, w, h, rnd)}" stroke="{GOLD}" stroke-opacity=".35" '
                       f'stroke-width="1.2" fill="none" stroke-linejoin="round" stroke-dasharray="3 4"/>')
    for _ in range(30):
        px = rnd.uniform(60, 840)
        out.append(f'<ellipse cx="{px:.1f}" cy="{ground - 1.5:.1f}" rx="{rnd.uniform(1.5,3.5):.1f}" ry="1.4" '
                   f'fill="{GOLD}" fill-opacity="{rnd.uniform(.15,.35):.2f}"/>')
    # tally of rocks examined
    for i, x in enumerate(xs[:find + 1]):
        out.append(f'<line x1="{x}" y1="{ground+30}" x2="{x}" y2="{ground+40}" stroke="{GOLD}" stroke-opacity="{.6 if i == find else .35}"/>')
    out.append(f'<line x1="{xs[0]}" y1="{ground+35}" x2="{xs[find]}" y2="{ground+35}" stroke="{GOLD}" stroke-opacity=".25" stroke-dasharray="2 5"/>')
    out.append(f'<text x="{xs[find]}" y="{ground+68}" text-anchor="middle" font-family="Inter" font-size="13" '
               f'letter-spacing="3" fill="#8a8578">ONE IN MANY</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".38"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
