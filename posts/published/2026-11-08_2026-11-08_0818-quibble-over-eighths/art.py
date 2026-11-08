"""A limit order a fraction too low: the bid waits on its dashed line while the price walks away. Returns SVG inner markup for a 900x520 viewBox."""
import random

GOLD = "#c9a96a"
GREY = "#8a8578"

def build():
    out = []
    ground = 430
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # price path: hovers near the bid, then climbs away
    rnd = random.Random(5)
    pts = []
    x, y = 70, 330
    while x < 330:
        pts.append((x, y))
        x += 12
        y = 322 + rnd.uniform(-10, 8)
    pts.append((x, 318))
    while x < 840:
        x += 12
        t = (x - 330) / 510
        y = 318 - 260 * (t ** 1.25) + rnd.uniform(-7, 7)
        pts.append((x, y))
    d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.8" fill="none" stroke-linejoin="round" stroke-linecap="round"/>')
    # faint area shadow
    area = d + f" L{pts[-1][0]:.1f},{ground} L{pts[0][0]:.1f},{ground} Z"
    out.append(f'<path d="{area}" fill="url(#fade)"/>')
    # the bid line: an eighth below
    bid = 344
    out.append(f'<line x1="70" y1="{bid}" x2="840" y2="{bid}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1" stroke-dasharray="3 7"/>')
    # the tiny gap bracket
    gx = 300
    out.append(f'<path d="M{gx-6},{318} H{gx+6} M{gx},{318} V{bid} M{gx-6},{bid} H{gx+6}" stroke="{GOLD}" stroke-opacity=".75" stroke-width="1"/>')
    out.append(f'<text x="{gx+14}" y="{bid-8}" font-family="Inter" font-size="15" letter-spacing="1" fill="{GREY}">1/8</text>')
    # unfilled order marker
    out.append(f'<circle cx="840" cy="{bid}" r="4.5" fill="none" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.2"/>')
    out.append(f'<text x="840" y="{bid+28}" text-anchor="end" font-family="Inter" font-size="12" letter-spacing="3" fill="{GREY}">BID · UNFILLED</text>')
    # end of price path
    ex, ey = pts[-1]
    out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4" fill="{GOLD}"/>')
    out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="22" fill="url(#glow)"/>')
    # time ticks
    for i, lab in enumerate(["YEAR 1", "5", "10", "15", "20"]):
        tx = 70 + i * 192.5
        out.append(f'<line x1="{tx:.1f}" y1="{ground+6}" x2="{tx:.1f}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx:.1f}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" letter-spacing="3" fill="{GREY}">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GOLD}" stop-opacity=".10"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient></defs>')
    return defs + "".join(out)
