"""Price stampedes downward while intrinsic value holds steady; an anchored stone stands as the crowd flees.
Returns SVG inner markup for a 900x520 viewBox."""
import random

GOLD = "#c9a96a"

def build():
    rnd = random.Random(41)
    out = []
    ground = 470
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # Steady intrinsic value line
    vy = 170
    out.append(f'<line x1="90" y1="{vy}" x2="810" y2="{vy}" stroke="{GOLD}" stroke-opacity=".55" '
               f'stroke-width="1.2" stroke-dasharray="3 7" stroke-linecap="round"/>')

    # Jittery price path: drifts around value, then plunges, then recovers toward value
    pts = []
    x, y = 90, 140
    while x < 810:
        if x < 360:
            target = 135
        elif x < 520:
            target = 135 + (x - 360) * 1.2
        elif x < 600:
            target = 327
        else:
            target = 327 - (x - 600) * 0.72
        y += (target - y) * 0.45 + rnd.uniform(-11, 11)
        pts.append((x, y))
        x += 9
    d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.6" fill="none" '
               f'stroke-linejoin="round" stroke-linecap="round"/>')
    # Faint echo of the price path
    d2 = "M" + " L".join(f"{px:.1f},{py+7:.1f}" for px, py in pts)
    out.append(f'<path d="{d2}" stroke="{GOLD}" stroke-opacity=".18" stroke-width="1" fill="none" stroke-linejoin="round"/>')

    # The anchored stone (the steady investor's holding) below the plunge
    sx = 560
    out.append(f'<path d="M{sx-46},{ground} C{sx-44},{ground-30} {sx-22},{ground-46} {sx+2},{ground-44} '
               f'C{sx+28},{ground-42} {sx+46},{ground-24} {sx+48},{ground} Z" fill="{GOLD}" fill-opacity=".14" '
               f'stroke="{GOLD}" stroke-opacity=".85" stroke-width="1.4"/>')
    for i in range(4):
        o = 10 + i * 9
        out.append(f'<path d="M{sx-30+i*6},{ground-o+4} q18,-6 34,-2" stroke="{GOLD}" stroke-opacity="{.35-i*.06:.2f}" '
                   f'stroke-width=".8" fill="none"/>')
    # Roots/keel beneath the stone
    for dx in (-24, -6, 12, 30):
        out.append(f'<path d="M{sx+dx},{ground} q{dx*0.3:.1f},18 {dx*0.5:.1f},34" stroke="{GOLD}" stroke-opacity=".2" '
                   f'stroke-width=".9" fill="none"/>')

    # Stampede: speed streaks fleeing left along the ground, fading out
    for i in range(46):
        x0 = rnd.uniform(110, 470)
        yy = ground - rnd.uniform(6, 62)
        ln = rnd.uniform(14, 46)
        a = 0.12 + 0.5 * (x0 - 110) / 360
        out.append(f'<line x1="{x0:.1f}" y1="{yy:.1f}" x2="{x0-ln:.1f}" y2="{yy+ln*0.08:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity="{a:.2f}" stroke-width="{rnd.uniform(.6,1.3):.2f}" stroke-linecap="round"/>')
    # Dust puffs
    for i in range(14):
        cx = rnd.uniform(140, 470)
        out.append(f'<circle cx="{cx:.1f}" cy="{ground-rnd.uniform(2,10):.1f}" r="{rnd.uniform(1,2.4):.1f}" '
                   f'fill="{GOLD}" fill-opacity="{rnd.uniform(.15,.4):.2f}"/>')

    lab = 'font-family="Inter" font-size="11" letter-spacing="2.5" fill="' + GOLD + '"'
    out.append(f'<text x="810" y="{vy-10}" text-anchor="end" {lab} fill-opacity=".7">VALUE</text>')
    out.append(f'<text x="96" y="108" {lab} fill-opacity=".7">PRICE</text>')
    return "\n".join(out)
