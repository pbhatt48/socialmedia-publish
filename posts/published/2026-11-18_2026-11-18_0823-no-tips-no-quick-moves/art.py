"""Tips and quick moves vs. patient ownership: a tangle of short, jittery trades fading out
beside one calm, slowly compounding line. SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"
GREY = "#8a8578"

def build():
    rnd = random.Random(1994)
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # Left: a tangle of short, frantic trades -- each starts somewhere, darts, and stops.
    for i in range(26):
        x = rnd.uniform(70, 300)
        y = rnd.uniform(200, 380)
        pts = [(x, y)]
        for _ in range(rnd.randint(5, 11)):
            x += rnd.uniform(5, 13)
            y += rnd.uniform(-22, 22)
            y = min(max(y, 150), 395)
            pts.append((x, y))
        d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
        a = rnd.uniform(0.12, 0.42)
        out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="{rnd.uniform(0.6, 1.2):.2f}" '
                   f'fill="none" stroke-linejoin="round" stroke-linecap="round"/>')
        ex, ey = pts[-1]
        out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="1.6" fill="{GOLD}" fill-opacity="{a:.2f}"/>')

    # A divider: thin vertical hairline
    out.append(f'<line x1="372" y1="150" x2="372" y2="{ground-10}" stroke="{GOLD}" stroke-opacity=".18" '
               f'stroke-width="1" stroke-dasharray="2 6"/>')

    # Right: one calm compounding line, a business held for years.
    x0, x1 = 420, 840
    pts = []
    for k in range(0, 101):
        t = k / 100
        x = x0 + (x1 - x0) * t
        base = ground - 18 - 230 * (math.exp(2.1 * t) - 1) / (math.exp(2.1) - 1)
        wobble = 4 * math.sin(t * 19) * (0.6 + t)
        pts.append((x, base + wobble))
    d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    out.append(f'<path d="{d} L{x1},{ground} L{x0},{ground} Z" fill="url(#fade)"/>')
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
    ex, ey = pts[-1]
    out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="22" fill="url(#glow)"/>')
    out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4" fill="{GOLD}"/>')
    sx, sy = pts[0]
    out.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="3" fill="{GOLD}" fill-opacity=".8"/>')

    # Year ticks under the long line
    for j in range(0, 11):
        tx = x0 + (x1 - x0) * j / 10
        h = 10 if j % 5 == 0 else 5
        out.append(f'<line x1="{tx:.1f}" y1="{ground+4}" x2="{tx:.1f}" y2="{ground+4+h}" stroke="{GOLD}" stroke-opacity=".45"/>')

    for tx, lab in [(185, "TIPS · QUICK MOVES"), (630, "PATIENT OWNERSHIP")]:
        out.append(f'<text x="{tx}" y="{ground+46}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="{GREY}">{lab}</text>')

    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GOLD}" stop-opacity=".14"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient></defs>')
    return defs + "".join(out)
