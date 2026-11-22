"""A finely rowed boat straining against a strong current: excellent effort, poor terrain.
Returns SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"
GREY = "#8a8578"

def build():
    rnd = random.Random(1985)
    out = []
    water = 330
    # current: long flowing lines moving left, denser and stronger toward the boat
    for i in range(14):
        y = water + 14 + i * 9
        a = 0.12 + 0.30 * (1 - abs(i - 5) / 9)
        x0 = rnd.uniform(70, 160)
        x1 = rnd.uniform(740, 830)
        amp = rnd.uniform(2, 4)
        ph = rnd.uniform(0, 6.28)
        pts = []
        for k in range(41):
            x = x1 - (x1 - x0) * k / 40
            pts.append(f"{x:.1f},{y + amp*math.sin(ph + k*0.55):.1f}")
        out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{GOLD}" '
                   f'stroke-opacity="{a:.2f}" stroke-width="1" stroke-linecap="round"/>')
    # arrow heads on current
    for (x, y) in [(150, water + 40), (210, water + 76), (130, water + 112)]:
        out.append(f'<path d="M{x+12},{y-6} L{x},{y} L{x+12},{y+6}" fill="none" stroke="{GOLD}" '
                   f'stroke-opacity=".55" stroke-width="1.2" stroke-linecap="round"/>')
    # surface line
    out.append(f'<line x1="60" y1="{water}" x2="840" y2="{water}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    boat_start = len(out)
    # boat hull at center
    bx, by = 450, water
    out.append(f'<path d="M{bx-95},{by-18} L{bx+110},{by-18} Q{bx+95},{by+8} {bx+60},{by+10} '
               f'L{bx-70},{by+10} Q{bx-92},{by+4} {bx-95},{by-18} Z" fill="{GOLD}" fill-opacity=".14" '
               f'stroke="{GOLD}" stroke-width="1.6" stroke-linejoin="round"/>')
    out.append(f'<line x1="{bx-88}" y1="{by-10}" x2="{bx+104}" y2="{by-10}" stroke="{GOLD}" stroke-opacity=".5" stroke-width=".8"/>')
    # thwarts
    for dx in (-40, 20):
        out.append(f'<line x1="{bx+dx}" y1="{by-18}" x2="{bx+dx}" y2="{by-4}" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1"/>')
    # oars, mid-stroke, digging in
    for side, op in ((1, .95), (-1, .45)):
        ox, oy = bx - 10, by - 18
        ex, ey = bx - 150, by + 34 + (6 if side < 0 else 0)
        out.append(f'<line x1="{ox+side*4}" y1="{oy-24}" x2="{ex}" y2="{ey}" stroke="{GOLD}" '
                   f'stroke-opacity="{op}" stroke-width="2" stroke-linecap="round"/>')
        out.append(f'<ellipse cx="{ex+6}" cy="{ey-3}" rx="15" ry="4" transform="rotate(20 {ex+6} {ey-3})" '
                   f'fill="{GOLD}" fill-opacity="{op*0.8:.2f}"/>')
    # splash rings at oar blade
    for r, a in ((14, .45), (26, .25), (40, .12)):
        out.append(f'<ellipse cx="{bx-146}" cy="{water+2}" rx="{r}" ry="{r*0.22:.1f}" fill="none" stroke="{GOLD}" '
                   f'stroke-opacity="{a}" stroke-width="1"/>')
    out.insert(boat_start, f'<g transform="translate({bx} {by}) scale(1.4) translate({-bx} {-by})">')
    out.append('</g>')
    # intended path vs actual drift
    out.append(f'<path d="M{bx+120},{by-95} L{bx+330},{by-95}" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.2" '
               f'stroke-dasharray="2 6" stroke-linecap="round"/>')
    out.append(f'<path d="M{bx+318},{by-101} L{bx+330},{by-95} L{bx+318},{by-89}" fill="none" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.2"/>')
    out.append(f'<text x="{bx+225}" y="{by-111}" text-anchor="middle" font-family="Inter" font-size="13" letter-spacing="3" fill="{GREY}">EFFORT</text>')
    out.append(f'<path d="M{bx-130},{by-95} L{bx-330},{by-95}" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1.2" stroke-linecap="round"/>')
    out.append(f'<path d="M{bx-318},{by-101} L{bx-330},{by-95} L{bx-318},{by-89}" fill="none" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1.2"/>')
    out.append(f'<text x="{bx-230}" y="{by-111}" text-anchor="middle" font-family="Inter" font-size="13" letter-spacing="3" fill="{GREY}">INDUSTRY</text>')
    return "".join(out)
