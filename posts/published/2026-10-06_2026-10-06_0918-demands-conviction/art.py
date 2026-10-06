"""Conviction in a storm: a deep-rooted oak holds while an unrooted sapling is torn away by the wind.
Returns SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"


def branch(out, rnd, x, y, ang, length, width, depth, spread, alpha, lean):
    if depth == 0 or length < 2:
        return
    ang += lean
    x2 = x + length * math.cos(ang)
    y2 = y - length * math.sin(ang)
    bend = rnd.uniform(-0.15, 0.15)
    cx = (x + x2) / 2 + length * bend * math.sin(ang)
    cy = (y + y2) / 2 + length * bend * math.cos(ang)
    out.append(f'<path d="M{x:.1f},{y:.1f} Q{cx:.1f},{cy:.1f} {x2:.1f},{y2:.1f}" stroke="{GOLD}" '
               f'stroke-opacity="{alpha:.2f}" stroke-width="{width:.2f}" fill="none" stroke-linecap="round"/>')
    n = 2 if depth > 2 else rnd.choice([2, 3])
    for i in range(n):
        da = spread * (i / (n - 1) - 0.5) * 2 + rnd.uniform(-0.22, 0.22)
        branch(out, rnd, x2, y2, ang + da, length * rnd.uniform(0.66, 0.8),
               max(width * 0.68, 0.35), depth - 1, spread, alpha, lean * 0.9)


def roots(out, rnd, x, y, length, width, depth, alpha):
    if depth == 0:
        return
    for _ in range(2):
        ang = -math.pi / 2 + rnd.uniform(-0.9, 0.9)
        x2 = x + length * math.cos(ang) * 1.3
        y2 = y - length * math.sin(ang)
        out.append(f'<path d="M{x:.1f},{y:.1f} L{x2:.1f},{y2:.1f}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" '
                   f'stroke-width="{width:.2f}" fill="none" stroke-linecap="round"/>')
        roots(out, rnd, x2, y2, length * 0.7, max(width * 0.65, 0.3), depth - 1, alpha * 0.92)


def build():
    out = []
    ground = 360
    # soil hatching hint and ground line
    out.append(f'<line x1="20" y1="{ground}" x2="880" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # wind streaks blowing left to right
    rnd = random.Random(3)
    for i in range(6):
        y = 110 + i * 34 + rnd.uniform(-6, 6)
        x1 = 40 + rnd.uniform(0, 60)
        x2 = x1 + rnd.uniform(160, 300)
        a = 0.08 + 0.14 * rnd.random()
        out.append(f'<path d="M{x1:.1f},{y:.1f} C{x1+80:.1f},{y-14:.1f} {x2-80:.1f},{y+12:.1f} {x2:.1f},{y-4:.1f}" '
                   f'stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="1" fill="none" stroke-linecap="round"/>')

    # the rooted oak (conviction)
    x = 610
    rnd = random.Random(23)
    trunk = 92
    out.append(f'<path d="M{x-9},{ground} C{x-6},{ground-trunk*0.5:.1f} {x-5},{ground-trunk*0.8:.1f} {x+2},{ground-trunk} '
               f'C{x+5},{ground-trunk*0.8:.1f} {x+7},{ground-trunk*0.5:.1f} {x+9},{ground} Z" fill="{GOLD}" fill-opacity=".8"/>')
    for a in (math.pi/2 + 0.6, math.pi/2 + 0.2, math.pi/2 - 0.15, math.pi/2 - 0.55):
        branch(out, rnd, x + 2, ground - trunk, a, 66, 3.6, 8, 0.48, 0.85, -0.04)
    roots(out, rnd, x, ground, 34, 2.4, 6, 0.42)

    # the unrooted sapling, torn loose and tumbling downwind
    sx, sy = 300, 292
    rnd = random.Random(5)
    out.append(f'<g transform="rotate(-58 {sx} {sy})">')
    out.append(f'<path d="M{sx},{sy} L{sx},{sy-38}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.6" stroke-linecap="round"/>')
    for a in (math.pi/2 + 0.5, math.pi/2 - 0.45):
        branch(out, rnd, sx, sy - 38, a, 16, 1.1, 4, 0.5, 0.5, 0)
    for dx in (-6, 0, 7):
        out.append(f'<path d="M{sx},{sy} l{dx},{9}" stroke="{GOLD}" stroke-opacity=".35" stroke-width=".8" stroke-linecap="round"/>')
    out.append('</g>')
    # its empty hole and drifting leaves
    out.append(f'<path d="M150,{ground} q12,9 24,0" stroke="{GOLD}" stroke-opacity=".4" stroke-width="1" fill="none"/>')
    out.append(f'<path d="M168,{ground-2} C210,{ground-30} 250,{ground-58} 292,292" stroke="{GOLD}" stroke-opacity=".28" '
               f'stroke-width="1" stroke-dasharray="2 6" fill="none" stroke-linecap="round"/>')
    rnd = random.Random(9)
    for i in range(7):
        lx = 340 + i * 26 + rnd.uniform(-8, 8)
        ly = 260 - i * 9 + rnd.uniform(-12, 12)
        rot = rnd.uniform(0, 180)
        out.append(f'<path d="M{lx:.1f},{ly:.1f} q5,-6 10,0 q-5,6 -10,0Z" fill="{GOLD}" fill-opacity="{0.55 - i*0.06:.2f}" '
                   f'transform="rotate({rot:.0f} {lx+5:.1f} {ly:.1f})"/>')

    # labels
    for tx, lab in ((162, "UNCONVINCED"), (610, "CONVICTION")):
        out.append(f'<text x="{tx}" y="{ground+125}" text-anchor="middle" font-family="Inter" font-size="12" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    return "".join(out)
