"""Toads on lily pads: many hopeful kisses, no transformations. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"


def pad(cx, cy, r, a):
    # lily pad: ellipse with a notch wedge
    rx, ry = r, r * 0.28
    n0, n1 = -0.32, 0.32  # notch angles (radians) facing viewer-right-front
    pts = []
    steps = 48
    for i in range(steps + 1):
        t = n1 + (2 * math.pi - (n1 - n0)) * i / steps
        pts.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
    d = f"M{cx:.1f},{cy:.1f} " + " ".join(f"L{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    return (f'<path d="{d}" stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="1.1" fill="{GOLD}" fill-opacity="{a*0.07:.3f}"/>'
            f'<path d="M{cx:.1f},{cy:.1f} L{cx - rx*0.7:.1f},{cy - ry*0.35:.1f} M{cx:.1f},{cy:.1f} L{cx - rx*0.2:.1f},{cy - ry*0.9:.1f} '
            f'M{cx:.1f},{cy:.1f} L{cx + rx*0.35:.1f},{cy + ry*0.85:.1f}" stroke="{GOLD}" stroke-opacity="{a*0.4:.2f}" stroke-width=".7"/>')


def toad(cx, base, s, a):
    """Seated toad in profile-ish front view, line art. base = y where it sits."""
    o = []
    w = 1.3 * s
    # body
    o.append(f'<path d="M{cx-34*s:.1f},{base:.1f} C{cx-40*s:.1f},{base-30*s:.1f} {cx-26*s:.1f},{base-52*s:.1f} {cx:.1f},{base-52*s:.1f} '
             f'C{cx+26*s:.1f},{base-52*s:.1f} {cx+40*s:.1f},{base-30*s:.1f} {cx+34*s:.1f},{base:.1f} Z" '
             f'stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="{w:.2f}" fill="#0f0f10" fill-opacity=".9" stroke-linejoin="round"/>')
    # eyes
    for ex in (-15, 15):
        o.append(f'<circle cx="{cx+ex*s:.1f}" cy="{base-52*s:.1f}" r="{8*s:.1f}" stroke="{GOLD}" stroke-opacity="{a:.2f}" '
                 f'stroke-width="{w:.2f}" fill="#0f0f10"/>'
                 f'<circle cx="{cx+ex*s:.1f}" cy="{base-52*s:.1f}" r="{2.6*s:.1f}" fill="{GOLD}" fill-opacity="{a:.2f}"/>')
    # mouth
    o.append(f'<path d="M{cx-18*s:.1f},{base-36*s:.1f} Q{cx:.1f},{base-29*s:.1f} {cx+18*s:.1f},{base-36*s:.1f}" stroke="{GOLD}" '
             f'stroke-opacity="{a*0.8:.2f}" stroke-width="{w*0.8:.2f}" fill="none" stroke-linecap="round"/>')
    # front legs
    for sx in (-1, 1):
        o.append(f'<path d="M{cx+sx*12*s:.1f},{base-14*s:.1f} Q{cx+sx*14*s:.1f},{base-4*s:.1f} {cx+sx*10*s:.1f},{base:.1f} '
                 f'M{cx+sx*4*s:.1f},{base:.1f} L{cx+sx*16*s:.1f},{base:.1f}" stroke="{GOLD}" stroke-opacity="{a*0.8:.2f}" '
                 f'stroke-width="{w*0.8:.2f}" fill="none" stroke-linecap="round"/>')
    # warts
    for dx, dy in ((-20, -24), (22, -20), (-8, -14), (10, -40), (-26, -10), (26, -8)):
        o.append(f'<circle cx="{cx+dx*s:.1f}" cy="{base+dy*s:.1f}" r="{1.3*s:.1f}" fill="{GOLD}" fill-opacity="{a*0.45:.2f}"/>')
    return "".join(o)


def kiss_mark(cx, cy, s, a):
    # tiny lips / heart-like mark floating above
    return (f'<path d="M{cx:.1f},{cy+5*s:.1f} C{cx-9*s:.1f},{cy-2*s:.1f} {cx-5*s:.1f},{cy-9*s:.1f} {cx:.1f},{cy-4*s:.1f} '
            f'C{cx+5*s:.1f},{cy-9*s:.1f} {cx+9*s:.1f},{cy-2*s:.1f} {cx:.1f},{cy+5*s:.1f} Z" stroke="{GOLD}" '
            f'stroke-opacity="{a:.2f}" stroke-width=".9" fill="none"/>')


def crown(cx, cy, s, a):
    pts = [(-22, 0), (-22, -18), (-11, -6), (0, -24), (11, -6), (22, -18), (22, 0)]
    d = "M" + " L".join(f"{cx+x*s:.1f},{cy+y*s:.1f}" for x, y in pts) + " Z"
    return (f'<path d="{d}" stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="1.2" stroke-dasharray="3 4" '
            f'fill="none" stroke-linejoin="round"/>')


def build():
    out = []
    water = 400
    out.append(f'<line x1="20" y1="{water}" x2="880" y2="{water}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # ripples
    for i, (x, w, a) in enumerate([(120, 60, .18), (300, 90, .14), (610, 70, .16), (780, 50, .12), (450, 120, .1)]):
        y = water + 28 + (i % 3) * 18
        out.append(f'<path d="M{x-w},{y} Q{x},{y-5} {x+w},{y}" stroke="{GOLD}" stroke-opacity="{a}" stroke-width=".8" fill="none"/>')
    toads = [(140, 0.8, .55), (300, 1.0, .7), (450, 1.35, .95), (600, 1.0, .7), (760, 0.8, .55)]
    for x, s, a in toads:
        out.append(pad(x, water - 4, 62 * s, a))
        out.append(toad(x, water - 6, s, a))
        # kisses rising above each toad, fading
        for k in range(3):
            out.append(kiss_mark(x + (k - 1) * 14 * s, water - 6 - (88 + 30 * k) * s, s, a * (0.7 - 0.2 * k)))
    # the crown that never arrives: faint dashed, high over the center toad
    out.append(crown(450, 92, 1.4, .5))
    out.append(f'<circle cx="450" cy="78" r="46" fill="url(#glow)"/>')
    out.append(f'<text x="450" y="{water+92}" text-anchor="middle" font-family="Inter" font-size="13" '
               f'letter-spacing="3" fill="#8a8578">STILL TOADS</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".18"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
