"""Main Street vs. Wall Street: a small, well-lit storefront under a lens, the distant
towers faint behind it. The edge is in what you already see up close. 900x520 viewBox."""
import random

GOLD = "#c9a96a"
MUTED = "#8a8578"


def line(x1, y1, x2, y2, a, w=1.0):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GOLD}" '
            f'stroke-opacity="{a:.2f}" stroke-width="{w}" stroke-linecap="round"/>')


def rect(x, y, w, h, a, sw=1.0, fill_a=0):
    fill = f'fill="{GOLD}" fill-opacity="{fill_a:.2f}"' if fill_a else 'fill="none"'
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" {fill} stroke="{GOLD}" '
            f'stroke-opacity="{a:.2f}" stroke-width="{sw}"/>')


def skyline(out, ground):
    rnd = random.Random(5)
    x = 520
    for w, h in [(46, 190), (34, 250), (58, 300), (40, 220), (52, 340), (36, 260), (48, 200)]:
        top = ground - h
        out.append(rect(x, top, w, h, 0.22, 0.9))
        out.append(line(x + w / 2, top, x + w / 2, top - rnd.choice([0, 0, 18, 28]), 0.22, 0.9))
        for wy in range(int(top) + 14, ground - 10, 16):
            for wx in range(int(x) + 8, int(x + w) - 6, 10):
                if rnd.random() < 0.55:
                    out.append(line(wx, wy, wx + 4, wy, 0.16, 0.8))
        x += w + 4


def storefront(out, ground):
    x, w, h = 160, 230, 170
    top = ground - h
    out.append(rect(x, top, w, h, 0.85, 1.4))
    # cornice + sign band
    out.append(line(x - 10, top, x + w + 10, top, 0.9, 1.6))
    out.append(rect(x + 30, top + 14, w - 60, 22, 0.6, 1.0))
    # striped awning
    ay, ah = top + 50, 26
    out.append(f'<path d="M{x-6},{ay} L{x+w+6},{ay} L{x+w+18},{ay+ah} L{x-18},{ay+ah} Z" fill="none" '
               f'stroke="{GOLD}" stroke-opacity=".85" stroke-width="1.2"/>')
    n = 9
    for i in range(1, n):
        t = i / n
        out.append(line(x - 6 + t * (w + 12), ay, x - 18 + t * (w + 36), ay + ah, 0.45, 1.0))
    for i in range(n):
        cx = x - 18 + (i + 0.5) / n * (w + 36)
        out.append(f'<path d="M{cx-13:.1f},{ay+ah} Q{cx:.1f},{ay+ah+12} {cx+13:.1f},{ay+ah}" fill="none" '
                   f'stroke="{GOLD}" stroke-opacity=".6" stroke-width="1"/>')
    # window with goods + door
    wy = ay + ah + 18
    out.append(rect(x + 18, wy, 120, ground - wy - 18, 0.75, 1.1, 0.06))
    for i, (bw, bh) in enumerate([(14, 22), (18, 30), (12, 18), (20, 26), (14, 34), (16, 20)]):
        bx = x + 26 + i * 18
        out.append(rect(bx, ground - 18 - bh - 4, bw * 0.8, bh, 0.55, 0.9))
    out.append(line(x + 22, ground - 22, x + 134, ground - 22, 0.5, 0.9))
    out.append(rect(x + 160, wy, 50, ground - wy, 0.8, 1.2))
    out.append(f'<circle cx="{x+200}" cy="{(wy+ground)/2+6:.1f}" r="2.2" fill="{GOLD}"/>')
    return x, w, top


def build():
    out = []
    ground = 430
    out.append(line(30, ground, 870, ground, 0.45, 1.0))
    skyline(out, ground)
    x, w, top = storefront(out, ground)
    # lens hovering over the shop
    cx, cy, r = x + w / 2 + 20, top - 92, 60
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r+40}" fill="url(#glow)"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GOLD}" stroke-width="2.2" stroke-opacity=".95"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r-7}" fill="none" stroke="{GOLD}" stroke-width="0.8" stroke-opacity=".4"/>')
    out.append(f'<path d="M{cx-34},{cy-22} A42,42 0 0 1 {cx-6},{cy-42}" fill="none" stroke="{GOLD}" '
               f'stroke-opacity=".55" stroke-width="1.4" stroke-linecap="round"/>')
    hx, hy = cx + r * 0.707, cy - r * 0.707
    out.append(line(hx, hy, hx + 48, hy - 48, 0.95, 7))
    # dotted sightline from lens down to the shop
    out.append(f'<path d="M{cx},{cy+r} L{cx},{top-6}" stroke="{GOLD}" stroke-opacity=".4" stroke-width="1.2" '
               f'stroke-dasharray="2 6" stroke-linecap="round"/>')
    for tx, lab in [(x + w / 2, "MAIN STREET"), (705, "WALL STREET")]:
        out.append(f'<text x="{tx}" y="{ground+36}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="{MUTED}">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".22"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
