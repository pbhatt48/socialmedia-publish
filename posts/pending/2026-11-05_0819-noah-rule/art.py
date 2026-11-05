"""The Noah rule: rain clouds on the left, a sturdy ark built on dry ground. Preparation over prediction.
Returns SVG inner markup for a 900x520 viewBox."""
import random

GOLD = "#c9a96a"


def build():
    rnd = random.Random(2001)
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # Clouds: layered arcs in the upper area
    def cloud(cx, cy, s, a):
        parts = []
        for dx, dy, r in ((-60, 8, 30), (-25, -12, 38), (20, -18, 44), (62, 2, 32), (90, 14, 22)):
            parts.append(f'<circle cx="{cx+dx*s:.1f}" cy="{cy+dy*s:.1f}" r="{r*s:.1f}" />')
        out.append(f'<g fill="none" stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="1.1">' + "".join(parts) + '</g>')
        # flat base to the cloud
        out.append(f'<line x1="{cx-88*s:.1f}" y1="{cy+36*s:.1f}" x2="{cx+110*s:.1f}" y2="{cy+36*s:.1f}" '
                   f'stroke="{GOLD}" stroke-opacity="{a*0.7:.2f}" stroke-width="1"/>')
        return cx, cy + 36 * s

    clouds = [cloud(230, 110, 1.0, 0.55), cloud(470, 80, 0.75, 0.35), cloud(690, 120, 0.9, 0.45)]

    # Rain: thin slanted strokes under the clouds
    for (cx, base), w in zip(clouds, (180, 140, 165)):
        for _ in range(26):
            x = cx - w / 2 + rnd.uniform(0, w)
            y = base + rnd.uniform(10, 140)
            ln = rnd.uniform(10, 22)
            a = rnd.uniform(0.15, 0.45)
            out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x-ln*0.25:.1f}" y2="{y+ln:.1f}" stroke="{GOLD}" '
                       f'stroke-opacity="{a:.2f}" stroke-width="1" stroke-linecap="round"/>')

    # Ark on stocks (building cradle), centered
    cx = 450
    keel = ground - 34
    hull_w = 300
    left, right = cx - hull_w / 2, cx + hull_w / 2
    deck = keel - 62
    hull = (f'M{left-20},{deck} L{right+20},{deck} '
            f'C{right+6},{deck+30} {right-30},{keel} {right-60},{keel} '
            f'L{left+60},{keel} C{left+30},{keel} {left-6},{deck+30} {left-20},{deck} Z')
    out.append(f'<path d="{hull}" fill="{GOLD}" fill-opacity=".08" stroke="{GOLD}" stroke-width="1.8" stroke-linejoin="round"/>')
    # planking lines
    for i, t in enumerate((0.25, 0.5, 0.75)):
        y = deck + (keel - deck) * t
        inset = 10 + 34 * t ** 2
        out.append(f'<line x1="{left-20+inset+10*t:.1f}" y1="{y:.1f}" x2="{right+20-inset-10*t:.1f}" y2="{y:.1f}" '
                   f'stroke="{GOLD}" stroke-opacity="{0.5-0.1*i:.2f}" stroke-width=".9"/>')
    # cabin / house on deck
    hx0, hx1, htop = cx - 95, cx + 95, deck - 52
    out.append(f'<rect x="{hx0}" y="{htop}" width="{hx1-hx0}" height="{deck-htop}" fill="none" stroke="{GOLD}" stroke-width="1.4" stroke-opacity=".85"/>')
    out.append(f'<path d="M{hx0-14},{htop} L{cx},{htop-34} L{hx1+14},{htop} Z" fill="{GOLD}" fill-opacity=".1" stroke="{GOLD}" stroke-width="1.4" stroke-linejoin="round"/>')
    for wx in range(int(hx0) + 22, int(hx1) - 10, 38):
        out.append(f'<rect x="{wx}" y="{htop+16}" width="14" height="14" fill="none" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1"/>')
    # cabin wall boards
    for y in range(int(htop) + 40, int(deck), 8):
        out.append(f'<line x1="{hx0}" y1="{y}" x2="{hx1}" y2="{y}" stroke="{GOLD}" stroke-opacity=".2" stroke-width=".7"/>')

    # building cradle: posts from keel to ground
    for px in (cx - 110, cx - 40, cx + 40, cx + 110):
        out.append(f'<line x1="{px}" y1="{keel}" x2="{px}" y2="{ground}" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.6"/>')
    out.append(f'<line x1="{cx-130}" y1="{ground-4}" x2="{cx+130}" y2="{ground-4}" stroke="{GOLD}" stroke-opacity=".4" stroke-width="1"/>')

    # ladder leaning on the hull (work in progress)
    lx0, ly0, lx1, ly1 = right + 70, ground, right - 4, deck + 6
    for off in (0, 14):
        out.append(f'<line x1="{lx0+off}" y1="{ly0}" x2="{lx1+off}" y2="{ly1}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.1"/>')
    for i in range(1, 7):
        t = i / 7
        x = lx0 + (lx1 - lx0) * t
        y = ly0 + (ly1 - ly0) * t
        out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x+14:.1f}" y2="{y:.1f}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # stacked timber on the left
    for i, y in enumerate(range(ground - 6, ground - 34, -7)):
        x0 = 150 + i * 6
        out.append(f'<rect x="{x0}" y="{y-5}" width="{110-i*12}" height="5" rx="2" fill="none" stroke="{GOLD}" stroke-opacity="{0.55-0.07*i:.2f}" stroke-width="1"/>')

    # tiny label
    out.append(f'<text x="{cx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" letter-spacing="3" fill="#8a8578">BUILD BEFORE THE RAIN</text>')
    return "".join(out)
