"""Spring already in bloom before the robin arrives: markets turn before sentiment. SVG inner markup for 900x520."""
import math, random

GOLD = "#c9a96a"

def stem(o, rnd, x, ground, h, stage, alpha):
    """stage 0 = bare shoot, 1 = bud, 2 = opening, 3 = full bloom"""
    top = ground - h
    lean = rnd.uniform(-8, 8)
    o.append(f'<path d="M{x},{ground} Q{x+lean},{ground-h*0.5:.1f} {x+lean*0.6:.1f},{top:.1f}" stroke="{GOLD}" '
             f'stroke-opacity="{alpha:.2f}" stroke-width="1.4" fill="none" stroke-linecap="round"/>')
    tx = x + lean * 0.6
    # leaves
    if stage >= 1:
        ly = ground - h * 0.38
        lx = x + lean * 0.3
        o.append(f'<path d="M{lx:.1f},{ly:.1f} q-14,-4 -18,-16 q14,2 18,16Z" fill="{GOLD}" fill-opacity="{alpha*0.5:.2f}"/>')
    if stage >= 2:
        ly = ground - h * 0.6
        lx = x + lean * 0.45
        o.append(f'<path d="M{lx:.1f},{ly:.1f} q14,-6 20,-18 q-14,0 -20,18Z" fill="{GOLD}" fill-opacity="{alpha*0.45:.2f}"/>')
    if stage == 0:
        o.append(f'<circle cx="{tx:.1f}" cy="{top:.1f}" r="1.8" fill="{GOLD}" fill-opacity="{alpha:.2f}"/>')
    elif stage == 1:
        o.append(f'<ellipse cx="{tx:.1f}" cy="{top-4:.1f}" rx="3.2" ry="5.5" fill="{GOLD}" fill-opacity="{alpha*0.8:.2f}"/>')
    elif stage == 2:
        for a in (-0.5, 0, 0.5):
            px = tx + 9 * math.sin(a); py = top - 9 * math.cos(a)
            o.append(f'<path d="M{tx:.1f},{top:.1f} Q{px-4:.1f},{py:.1f} {px:.1f},{py-2:.1f} Q{px+4:.1f},{py:.1f} {tx:.1f},{top:.1f}Z" '
                     f'fill="{GOLD}" fill-opacity="{alpha*0.55:.2f}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width=".8"/>')
    else:
        n = 6
        r = 12
        for i in range(n):
            a = 2 * math.pi * i / n
            px = tx + r * math.cos(a); py = top + r * math.sin(a)
            o.append(f'<ellipse cx="{(tx+px)/2:.1f}" cy="{(top+py)/2:.1f}" rx="6.5" ry="3.2" '
                     f'transform="rotate({math.degrees(a):.0f} {(tx+px)/2:.1f} {(top+py)/2:.1f})" '
                     f'fill="{GOLD}" fill-opacity="{alpha*0.35:.2f}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width=".8"/>')
        o.append(f'<circle cx="{tx:.1f}" cy="{top:.1f}" r="3.2" fill="{GOLD}" fill-opacity="{alpha:.2f}"/>')

def robin(o, x, y, s=1.0):
    """small songbird in flight, arriving from the right"""
    a = .85
    # body
    o.append(f'<path d="M{x},{y} C{x-14*s},{y-10*s} {x-36*s},{y-8*s} {x-44*s},{y+2*s} '
             f'C{x-34*s},{y+10*s} {x-12*s},{y+12*s} {x},{y} Z" fill="{GOLD}" fill-opacity=".25" '
             f'stroke="{GOLD}" stroke-opacity="{a}" stroke-width="1.2" stroke-linejoin="round"/>')
    # breast
    o.append(f'<path d="M{x-38*s},{y+3*s} C{x-30*s},{y+10*s} {x-18*s},{y+10*s} {x-10*s},{y+4*s}" stroke="{GOLD}" '
             f'stroke-opacity=".6" stroke-width="3" fill="none" stroke-linecap="round"/>')
    # head & beak (heading left)
    o.append(f'<circle cx="{x-44*s}" cy="{y-2*s}" r="{6*s}" fill="{GOLD}" fill-opacity=".35" stroke="{GOLD}" stroke-opacity="{a}" stroke-width="1.2"/>')
    o.append(f'<path d="M{x-50*s},{y-3*s} l{-7*s},{2*s} l{7*s},{1.5*s}Z" fill="{GOLD}"/>')
    o.append(f'<circle cx="{x-45.5*s}" cy="{y-3.5*s}" r="1" fill="#0d0d0d"/>')
    # tail
    o.append(f'<path d="M{x},{y} l{16*s},{-6*s} l{-2*s},{8*s}Z" fill="{GOLD}" fill-opacity=".5"/>')
    # wings raised
    o.append(f'<path d="M{x-20*s},{y-6*s} C{x-14*s},{y-30*s} {x+4*s},{y-40*s} {x+16*s},{y-42*s} '
             f'C{x+6*s},{y-26*s} {x-4*s},{y-12*s} {x-10*s},{y-4*s}" fill="{GOLD}" fill-opacity=".18" '
             f'stroke="{GOLD}" stroke-opacity="{a}" stroke-width="1.1"/>')
    # motion lines
    for i, dy in enumerate((-14, -4, 6)):
        o.append(f'<line x1="{x+26*s}" y1="{y+dy*s}" x2="{x+56*s - i*8}" y2="{y+dy*s}" stroke="{GOLD}" stroke-opacity="{.3-i*.07:.2f}" stroke-width="1"/>')

def build():
    o = []
    ground = 400
    rnd = random.Random(5)
    o.append(f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".30"/>'
             f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    # soft sun
    o.append(f'<circle cx="560" cy="150" r="110" fill="url(#glow)"/>')
    o.append(f'<circle cx="560" cy="150" r="34" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1.1" fill="none"/>')
    # rising dotted path: things improve before anyone announces it
    o.append(f'<path d="M70,370 C260,365 380,300 520,250 S700,170 760,150" stroke="{GOLD}" stroke-opacity=".3" '
             f'stroke-width="1.2" stroke-dasharray="2 7" fill="none" stroke-linecap="round"/>')
    # ground
    o.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # stems progressing left to right: bare -> bud -> opening -> bloom
    xs = list(range(80, 700, 34))
    for i, x in enumerate(xs):
        t = i / (len(xs) - 1)
        stage = min(3, int(t * 4))
        h = 22 + t * 92 + rnd.uniform(-8, 8)
        stem(o, rnd, x + rnd.uniform(-6, 6), ground, h, stage, 0.45 + 0.5 * t)
    # small grass ticks
    for x in range(60, 840, 13):
        hh = rnd.uniform(3, 8)
        o.append(f'<line x1="{x}" y1="{ground}" x2="{x+rnd.uniform(-2,2):.1f}" y2="{ground-hh:.1f}" stroke="{GOLD}" stroke-opacity=".18" stroke-width=".8"/>')
    # the robin, arriving late at the far right
    robin(o, 820, 250, 1.0)
    # labels
    for tx, lab in [(90, "WINTER"), (420, "THAW"), (680, "SPRING")]:
        o.append(f'<line x1="{tx}" y1="{ground+6}" x2="{tx}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        o.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                 f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    return "".join(o)
