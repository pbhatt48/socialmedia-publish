"""A hand-built suspension bridge over a deep gorge: preparation spans the gap; the gap itself does not forgive. Returns SVG inner markup for a 900x520 viewBox."""
import random

GOLD = "#c9a96a"


def line(x1, y1, x2, y2, op, w=1.0):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GOLD}" '
            f'stroke-opacity="{op:.2f}" stroke-width="{w:.2f}" stroke-linecap="round"/>')


def build():
    out = []
    rnd = random.Random(1982)
    ground = 300
    lx, rx = 330, 570          # gorge lips
    # plateaus
    out.append(line(40, ground, lx, ground, .5))
    out.append(line(rx, ground, 860, ground, .5))
    # gorge walls: jagged descending paths
    def wall(x0, sign):
        pts = [(x0, ground)]
        x, y = x0, ground
        while y < 470:
            y += rnd.uniform(14, 26)
            x += sign * rnd.uniform(2, 16)
            pts.append((x, min(y, 480)))
        return pts
    for x0, sign in ((lx, 1), (rx, -1)):
        pts = wall(x0, sign)
        d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
        out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.2" fill="none" stroke-linejoin="round"/>')
        # strata hatching on the wall faces
        for px, py in pts[1:-1]:
            ln = rnd.uniform(18, 46)
            out.append(line(px - sign * 2, py, px - sign * (2 + ln), py, .14, .8))
    # depth: fading contour lines deep in the gorge
    for i, y in enumerate(range(400, 486, 14)):
        inset = 40 + i * 14
        out.append(line(lx + inset, y, rx - inset, y, .22 - i * .03, .8))
    # towers
    th = 120
    for tx in (lx - 30, rx + 30):
        out.append(line(tx - 5, ground, tx - 2, ground - th, .85, 2.2))
        out.append(line(tx + 5, ground, tx + 2, ground - th, .85, 2.2))
        out.append(line(tx - 4, ground - th * .55, tx + 4, ground - th * .55, .6, 1.2))
        out.append(line(tx - 3, ground - th + 6, tx + 3, ground - th + 6, .6, 1.2))
    t1, t2 = lx - 30, rx + 30
    deck_y = ground - 4
    sag = 70
    # main cables (quadratic sag) and back-stays
    top = ground - th
    out.append(f'<path d="M{t1},{top} Q{(t1+t2)/2},{top + 2*sag} {t2},{top}" stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.6" fill="none"/>')
    out.append(f'<path d="M{t1},{top} Q{t1-60},{ground-40} {t1-110},{ground}" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.2" fill="none"/>')
    out.append(f'<path d="M{t2},{top} Q{t2+60},{ground-40} {t2+110},{ground}" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.2" fill="none"/>')
    for ax in (t1 - 110, t2 + 110):
        out.append(f'<rect x="{ax-5}" y="{ground-4}" width="10" height="5" fill="{GOLD}" fill-opacity=".7"/>')
    # deck (slight sag) with planks and hangers
    deck_sag = 10
    out.append(f'<path d="M{t1},{deck_y} Q{(t1+t2)/2},{deck_y + 2*deck_sag} {t2},{deck_y}" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.4" fill="none"/>')
    n = 30
    for i in range(1, n):
        t = i / n
        x = t1 + (t2 - t1) * t
        cy = top + 2 * sag * 2 * t * (1 - t)            # cable height at x
        dy = deck_y + 2 * deck_sag * 2 * t * (1 - t)    # deck height at x
        out.append(line(x, cy, x, dy, .38, .8))
        out.append(line(x - 3, dy + 1, x + 3, dy + 1, .75, 1.6))
    # a few planks laid ahead, unfinished at the right is avoided: bridge is complete
    # soft glow at the far side — arrival
    out.append(f'<circle cx="{t2+130}" cy="{ground-1}" r="34" fill="url(#glow)"/>')
    out.append(f'<circle cx="{t2+130}" cy="{ground-3}" r="3" fill="{GOLD}"/>')
    # a faint dotted path leading to the bridge from the left
    out.append(f'<path d="M70,{ground-3} L{t1-110},{ground-3}" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1.2" stroke-dasharray="2 7" stroke-linecap="round"/>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
