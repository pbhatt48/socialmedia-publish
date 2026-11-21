"""A well-rooted tree you own in the foreground; faint, unexamined trees on the far horizon. A dotted path goes out to them and returns home."""
import math, random

GOLD = "#c9a96a"

def branch(out, rnd, x, y, ang, length, width, depth, spread, alpha):
    if depth == 0 or length < 2:
        return
    x2 = x + length * math.cos(ang)
    y2 = y - length * math.sin(ang)
    bend = rnd.uniform(-0.18, 0.18)
    cx = (x + x2) / 2 + length * bend * math.sin(ang)
    cy = (y + y2) / 2 + length * bend * math.cos(ang)
    out.append(f'<path d="M{x:.1f},{y:.1f} Q{cx:.1f},{cy:.1f} {x2:.1f},{y2:.1f}" '
               f'stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="{width:.2f}" fill="none" stroke-linecap="round"/>')
    n = 2 if depth > 2 else rnd.choice([2, 3])
    for i in range(n):
        da = spread * (i / (n - 1) - 0.5) * 2 + rnd.uniform(-0.25, 0.25)
        da *= 1.15 if depth < 6 else 1.0
        branch(out, rnd, x2, y2, ang + da, length * rnd.uniform(0.66, 0.8),
               max(width * 0.68, 0.35), depth - 1, spread, alpha)

def roots(out, rnd, x, y, length, width, depth, alpha):
    if depth == 0:
        return
    for _ in range(2):
        ang = -math.pi / 2 + rnd.uniform(-1.1, 1.1)
        x2 = x + length * math.cos(ang) * 1.6
        y2 = y - length * math.sin(ang) * 0.55
        out.append(f'<path d="M{x:.1f},{y:.1f} L{x2:.1f},{y2:.1f}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" '
                   f'stroke-width="{width:.2f}" fill="none" stroke-linecap="round"/>')
        roots(out, rnd, x2, y2, length * 0.62, width * 0.6, depth - 1, alpha)

def tree(out, seed, x, ground, scale, depth, alpha=0.9):
    rnd = random.Random(seed)
    trunk = 70 * scale
    out.append(f'<path d="M{x-6*scale:.1f},{ground} C{x-4*scale:.1f},{ground-trunk*0.5:.1f} {x-3*scale:.1f},{ground-trunk*0.8:.1f} {x:.1f},{ground-trunk:.1f} '
               f'C{x+3*scale:.1f},{ground-trunk*0.8:.1f} {x+4*scale:.1f},{ground-trunk*0.5:.1f} {x+6*scale:.1f},{ground} Z" fill="{GOLD}" fill-opacity="{alpha*0.85:.2f}"/>')
    for a in (math.pi/2 + 0.55, math.pi/2 + 0.15, math.pi/2 - 0.2, math.pi/2 - 0.6):
        branch(out, rnd, x, ground - trunk, a, 56 * scale, 3.0 * scale, depth, 0.5, alpha)
    roots(out, rnd, x, ground, 16 * scale, 1.4 * scale, max(depth - 4, 2), 0.16)

def far_tree(out, seed, x, ground, h, alpha):
    rnd = random.Random(seed)
    out.append(f'<line x1="{x}" y1="{ground}" x2="{x}" y2="{ground-h*0.45:.1f}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="1"/>')
    r = h * 0.32
    cy = ground - h * 0.62
    out.append(f'<ellipse cx="{x}" cy="{cy:.1f}" rx="{r*rnd.uniform(0.8,1.05):.1f}" ry="{r*1.15:.1f}" fill="none" '
               f'stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="0.9" stroke-dasharray="2 3"/>')

def build():
    out = []
    ground = 420
    out.append(f'<line x1="20" y1="{ground}" x2="880" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # distant, unexamined trees receding to the right
    far = [(560, 64, .42), (612, 54, .36), (660, 46, .31), (702, 40, .27), (740, 34, .23), (774, 29, .2), (804, 25, .17), (830, 21, .14), (852, 18, .12)]
    for i, (x, h, a) in enumerate(far):
        far_tree(out, 100 + i, x, ground, h, a)
    # the owned tree, deeply rooted
    tree(out, 23, 300, ground, 1.25, 10, alpha=0.88)
    roots(out, random.Random(5), 300, ground, 30, 2.0, 4, 0.28)
    # dotted path out to the horizon and back home
    out.append(f'<path d="M318,{ground-6} C420,{ground-70} 560,{ground-110} 700,{ground-82} '
               f'C780,{ground-66} 760,{ground-150} 620,{ground-170} C500,{ground-188} 400,{ground-150} 340,{ground-90}" '
               f'stroke="{GOLD}" stroke-opacity=".32" stroke-width="1.1" stroke-dasharray="2 7" fill="none" stroke-linecap="round"/>')
    out.append(f'<path d="M340,{ground-90} l2,-12 M340,{ground-90} l11,-5" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1.1" stroke-linecap="round"/>')
    for tx, lab in [(300, "WHAT YOU KNOW"), (706, "WHAT YOU DON’T")]:
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    return "".join(out)
