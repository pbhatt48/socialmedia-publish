"""Aesop's bird in the hand vs. two in the bush: one certain bird now, a bush of uncertain birds later, with a discounting arc between."""
import math, random

GOLD = "#c9a96a"

def bird(x, y, s, alpha, flip=False, dashed=False):
    d = -1 if flip else 1
    p = (f"M{x-14*s*d:.1f},{y+2*s:.1f} C{x-8*s*d:.1f},{y-9*s:.1f} {x+8*s*d:.1f},{y-10*s:.1f} {x+12*s*d:.1f},{y-4*s:.1f} "
         f"C{x+16*s*d:.1f},{y-12*s:.1f} {x+22*s*d:.1f},{y-10*s:.1f} {x+23*s*d:.1f},{y-6*s:.1f} "
         f"L{x+29*s*d:.1f},{y-5*s:.1f} L{x+22*s*d:.1f},{y-2*s:.1f} "
         f"C{x+20*s*d:.1f},{y+6*s:.1f} {x+6*s*d:.1f},{y+10*s:.1f} {x-6*s*d:.1f},{y+7*s:.1f} "
         f"L{x-24*s*d:.1f},{y+12*s:.1f} L{x-14*s*d:.1f},{y+2*s:.1f} Z")
    wing = (f"M{x-4*s*d:.1f},{y:.1f} C{x+2*s*d:.1f},{y-4*s:.1f} {x+10*s*d:.1f},{y-2*s:.1f} {x+12*s*d:.1f},{y+3*s:.1f}")
    dash = ' stroke-dasharray="3 4"' if dashed else ''
    o = (f'<path d="{p}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="1.3" fill="{GOLD}" '
         f'fill-opacity="{alpha*0.12:.2f}" stroke-linejoin="round"{dash}/>'
         f'<path d="{wing}" stroke="{GOLD}" stroke-opacity="{alpha*0.8:.2f}" stroke-width="1" fill="none"{dash}/>')
    o += f'<circle cx="{x+17*s*d:.1f}" cy="{y-6*s:.1f}" r="{1.3*s:.1f}" fill="{GOLD}" fill-opacity="{alpha:.2f}"/>'
    return o

def twig(out, rnd, x, y, ang, length, w, depth):
    if depth == 0:
        return
    x2 = x + length * math.cos(ang); y2 = y - length * math.sin(ang)
    out.append(f'<path d="M{x:.1f},{y:.1f} L{x2:.1f},{y2:.1f}" stroke="{GOLD}" stroke-opacity="{0.25+0.07*depth:.2f}" '
               f'stroke-width="{w:.2f}" stroke-linecap="round"/>')
    for da in (-0.45, 0.4):
        twig(out, rnd, x2, y2, ang + da + rnd.uniform(-0.2, 0.2), length * rnd.uniform(0.62, 0.78), max(w*0.7, .4), depth-1)
    if depth <= 2 and y2 < 392:
        out.append(f'<ellipse cx="{x2:.1f}" cy="{y2:.1f}" rx="5" ry="2.2" transform="rotate({rnd.uniform(0,180):.0f} {x2:.1f} {y2:.1f})" '
                   f'fill="{GOLD}" fill-opacity=".16"/>')

def build():
    out = []
    ground = 400
    rnd = random.Random(5)
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # left: a single sure bird on a short post (in hand, now)
    lx = 230
    out.append(f'<line x1="{lx}" y1="{ground}" x2="{lx}" y2="{ground-150}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="2"/>')
    out.append(f'<line x1="{lx-34}" y1="{ground-150}" x2="{lx+34}" y2="{ground-150}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="2" stroke-linecap="round"/>')
    out.append(f'<circle cx="{lx}" cy="{ground-170}" r="62" fill="url(#glow)"/>')
    out.append(bird(lx, ground-166, 1.9, 0.95))
    # right: bush of uncertain birds (later)
    bx = 640
    for i in range(7):
        a = math.pi/2 + (i-3)*0.3
        twig(out, rnd, bx, ground, a, 50, 2.0, 4)
    out.append(bird(bx-45, ground-158, 1.4, 0.8, flip=True, dashed=True))
    out.append(bird(bx+50, ground-140, 1.4, 0.8, flip=True, dashed=True))
    # discounting arc from bush back to hand
    out.append(f'<path d="M{bx-20},{ground-200} C{bx-120},{ground-330} {lx+120},{ground-330} {lx+40},{ground-230}" '
               f'stroke="{GOLD}" stroke-opacity=".4" stroke-width="1.2" stroke-dasharray="2 7" fill="none" stroke-linecap="round"/>')
    out.append(f'<path d="M{lx+40},{ground-230} l1,-12 M{lx+40},{ground-230} l11,-6" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1.2" stroke-linecap="round"/>')
    for tx, lab in [(lx, "1 IN HAND"), (bx, "2 IN THE BUSH")]:
        out.append(f'<line x1="{tx}" y1="{ground+6}" x2="{tx}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    out.append(f'<text x="{(lx+bx)/2}" y="{ground-275}" text-anchor="middle" font-family="Inter" font-size="12" '
               f'letter-spacing="3" fill="#8a8578">HOW MANY · HOW SURE · HOW SOON</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
