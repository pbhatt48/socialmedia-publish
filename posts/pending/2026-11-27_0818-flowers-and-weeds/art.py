"""Flowers pulled, weeds watered: selling winners and holding losers. SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"

def flower(out, x, ground, h, petals=8, r=13, alpha=0.9, sway=0.0):
    tx, ty = x + sway, ground - h
    out.append(f'<path d="M{x},{ground} C{x-4},{ground-h*0.4} {tx+4},{ground-h*0.7} {tx},{ty}" stroke="{GOLD}" '
               f'stroke-opacity="{alpha:.2f}" stroke-width="1.6" fill="none" stroke-linecap="round"/>')
    ly = ground - h * 0.45
    out.append(f'<path d="M{x-1},{ly} q-16,-4 -22,-18 q16,2 22,18Z" fill="{GOLD}" fill-opacity="{alpha*0.55:.2f}"/>'
               f'<path d="M{x+1},{ly-14} q16,-6 24,-18 q-14,0 -24,18Z" fill="{GOLD}" fill-opacity="{alpha*0.45:.2f}"/>')
    for i in range(petals):
        a = 2 * math.pi * i / petals
        px, py = tx + r * math.cos(a), ty + r * math.sin(a)
        out.append(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{r*0.62:.1f}" ry="{r*0.32:.1f}" '
                   f'transform="rotate({math.degrees(a):.0f} {px:.1f} {py:.1f})" fill="none" stroke="{GOLD}" '
                   f'stroke-opacity="{alpha:.2f}" stroke-width="1.1"/>')
    out.append(f'<circle cx="{tx}" cy="{ty}" r="{r*0.38:.1f}" fill="{GOLD}" fill-opacity="{alpha:.2f}"/>')

def weed(out, rnd, x, ground, h, alpha=0.5):
    for i in range(7):
        a = math.pi / 2 + rnd.uniform(-0.9, 0.9)
        L = h * rnd.uniform(0.45, 1.0)
        x2, y2 = x + L * math.cos(a), ground - L * math.sin(a)
        cx, cy = x + L * 0.5 * math.cos(a) + rnd.uniform(-10, 10), ground - L * 0.5 * math.sin(a)
        out.append(f'<path d="M{x},{ground} Q{cx:.1f},{cy:.1f} {x2:.1f},{y2:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity="{alpha:.2f}" stroke-width="1" fill="none" stroke-linecap="round"/>')
        for t in (0.45, 0.7):
            bx, by = x + (x2 - x) * t, ground + (y2 - ground) * t
            s = 1 if rnd.random() > 0.5 else -1
            out.append(f'<path d="M{bx:.1f},{by:.1f} l{s*7:.1f},-6" stroke="{GOLD}" stroke-opacity="{alpha*0.8:.2f}" '
                       f'stroke-width=".8" stroke-linecap="round"/>')

def build():
    rnd = random.Random(5)
    out = []
    ground = 400
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # Left: the flowers (winners), one being pulled out.
    flower(out, 110, ground, 190, alpha=0.9, sway=-6)
    flower(out, 185, ground, 230, petals=9, r=15, alpha=0.95, sway=5)
    # The pulled flower, lifted above an empty hole, roots dangling.
    px, py = 300, 330
    out.append(f'<path d="M{px-22},{ground} q8,-8 14,-2 M{px+8},{ground-2} q6,-6 14,2 M{px-8},{ground} q8,9 16,0" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1" fill="none"/>')
    out.append(f'<g transform="rotate(-14 {px} {py})">')
    flower(out, px, py, 170, petals=8, r=13, alpha=0.6)
    for dx, L in ((-9, 26), (-3, 38), (4, 30), (10, 20)):
        out.append(f'<path d="M{px},{py} q{dx},{L*0.5} {dx*1.6:.1f},{L}" stroke="{GOLD}" stroke-opacity=".45" '
                   f'stroke-width=".9" fill="none" stroke-linecap="round"/>')
    out.append('</g>')
    # Right: weeds being watered.
    for wx, wh in ((560, 95), (630, 130), (705, 105), (775, 80)):
        weed(out, rnd, wx, ground, wh, alpha=0.45)
    # Watering can tilted over the weeds.
    cx, cy = 560, 165
    can = (f'<g transform="rotate(24 {cx} {cy})" stroke="{GOLD}" stroke-width="1.4" fill="none" stroke-linejoin="round">'
           f'<path d="M{cx-45},{cy-30} L{cx+40},{cy-30} L{cx+34},{cy+35} L{cx-39},{cy+35} Z" stroke-opacity=".85"/>'
           f'<path d="M{cx-45},{cy-18} C{cx-90},{cy-20} {cx-90},{cy+25} {cx-41},{cy+20}" stroke-opacity=".7"/>'
           f'<path d="M{cx+38},{cy+10} L{cx+105},{cy-36}" stroke-opacity=".85" stroke-width="2"/>'
           f'<path d="M{cx+100},{cy-46} L{cx+116},{cy-24}" stroke-opacity=".9" stroke-width="2.4"/>'
           f'<path d="M{cx-30},{cy-30} C{cx-20},{cy-62} {cx+25},{cy-62} {cx+30},{cy-30}" stroke-opacity=".6"/>'
           f'</g>')
    out.append(can)
    # Rose tip after rotation ~ (cx+? , ?) — compute.
    a = math.radians(24)
    rx, ry = cx + 108, cy - 35
    tipx = cx + (rx - cx) * math.cos(a) - (ry - cy) * math.sin(a)
    tipy = cy + (rx - cx) * math.sin(a) + (ry - cy) * math.cos(a)
    for i in range(18):
        x = tipx + rnd.uniform(-28, 28)
        y = tipy + 18 + i * 11 + rnd.uniform(-4, 4)
        if y > ground - 110:
            continue
        out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x-1:.1f}" y2="{y+8:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity="{rnd.uniform(.3,.7):.2f}" stroke-width="1.1" stroke-linecap="round"/>')
    for tx, lab in ((185, "WINNERS"), (665, "LOSERS")):
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    return "".join(out)
