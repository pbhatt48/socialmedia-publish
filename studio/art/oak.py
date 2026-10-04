"""Oak-from-seed growth sequence: patience + compounding. Returns SVG inner markup for a 900x520 viewBox."""
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

def build():
    out = []
    ground = 420
    out.append(f'<line x1="0" y1="{ground}" x2="900" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    sx = 60
    out.append(f'<ellipse cx="{sx}" cy="{ground-9}" rx="6" ry="8.5" fill="{GOLD}"/>'
               f'<path d="M{sx-7.5},{ground-13} Q{sx},{ground-22} {sx+7.5},{ground-13} Z" fill="{GOLD}" fill-opacity=".6"/>'
               f'<line x1="{sx}" y1="{ground-19}" x2="{sx+2}" y2="{ground-25}" stroke="{GOLD}" stroke-width="1.4"/>')
    out.append(f'<circle cx="{sx}" cy="{ground-9}" r="26" fill="url(#glow)"/>')
    x = 165
    out.append(f'<path d="M{x},{ground} Q{x-2},{ground-14} {x},{ground-26}" stroke="{GOLD}" stroke-width="1.6" fill="none"/>'
               f'<path d="M{x},{ground-24} q-12,-4 -16,-14 q12,0 16,14Z M{x},{ground-26} q10,-8 18,-8 q-4,10 -18,8Z" fill="{GOLD}" fill-opacity=".85"/>')
    tree(out, 7, 270, ground, 0.42, 5)
    tree(out, 11, 400, ground, 0.8, 7)
    tree(out, 23, 650, ground, 1.38, 10, alpha=0.85)
    out.insert(0, f'<path d="M60,404 C260,400 430,330 650,60" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1.2" '
                  f'stroke-dasharray="2 7" fill="none" stroke-linecap="round"/>')
    labels = [(60, "YEAR 1"), (165, "5"), (270, "10"), (400, "25"), (650, "50")]
    for tx, lab in labels:
        out.append(f'<line x1="{tx}" y1="{ground+6}" x2="{tx}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
