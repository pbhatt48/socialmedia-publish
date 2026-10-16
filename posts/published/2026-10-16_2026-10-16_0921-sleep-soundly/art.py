"""Sleeping soundly: a calm moonlit sea, a small house on a broad, deep foundation. Returns SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"


def build():
    out = []
    rnd = random.Random(5)
    ground = 400
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    # stars
    for _ in range(46):
        x, y = rnd.uniform(40, 860), rnd.uniform(30, 250)
        if math.hypot(x - 640, y - 120) < 80 or (330 < x < 570 and y > 170):
            continue
        r = rnd.choice([0.8, 1.0, 1.2, 1.6])
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{GOLD}" fill-opacity="{rnd.uniform(.25,.75):.2f}"/>')
    # crescent moon
    out.append(f'<circle cx="640" cy="120" r="90" fill="url(#glow)"/>')
    out.append(f'<path d="M640,82 A38,38 0 1,0 662,152 A30,30 0 1,1 640,82 Z" fill="{GOLD}" fill-opacity=".9"/>')
    # horizon
    out.append(f'<line x1="30" y1="{ground}" x2="870" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # calm water ripples below horizon
    for i, (y, a) in enumerate([(418, .28), (436, .2), (456, .14), (478, .09)]):
        w = 520 - i * 90
        x0 = 450 - w / 2
        out.append(f'<path d="M{x0:.0f},{y} Q{450-w/4:.0f},{y-3} 450,{y} T{x0+w:.0f},{y}" stroke="{GOLD}" '
                   f'stroke-opacity="{a}" stroke-width="1" fill="none"/>')
    # moon reflection
    for i, y in enumerate(range(412, 486, 10)):
        hw = 22 - i * 2.4
        out.append(f'<line x1="{640-hw:.1f}" y1="{y}" x2="{640+hw:.1f}" y2="{y}" stroke="{GOLD}" '
                   f'stroke-opacity="{.5 - i*.055:.2f}" stroke-width="1.4" stroke-linecap="round"/>')
    # broad foundation (margin of safety) -- stepped plinth
    hx = 380
    steps = [(150, 14, .55), (120, 12, .7), (96, 10, .85)]
    y = ground
    for half, h, a in steps:
        out.append(f'<rect x="{hx-half}" y="{y-h}" width="{2*half}" height="{h}" fill="none" stroke="{GOLD}" '
                   f'stroke-opacity="{a}" stroke-width="1.2"/>')
        y -= h
    base = y
    # house
    w, h = 120, 82
    out.append(f'<rect x="{hx-w/2}" y="{base-h}" width="{w}" height="{h}" fill="none" stroke="{GOLD}" stroke-width="1.6"/>')
    out.append(f'<path d="M{hx-w/2-14},{base-h} L{hx},{base-h-62} L{hx+w/2+14},{base-h}" fill="none" stroke="{GOLD}" '
               f'stroke-width="1.6" stroke-linejoin="round"/>')
    # chimney
    out.append(f'<path d="M{hx+28},{base-h-34} V{base-h-58} H{hx+42} V{base-h-23}" fill="none" stroke="{GOLD}" stroke-width="1.4"/>')
    # door
    out.append(f'<path d="M{hx-12},{base} V{base-40} H{hx+12} V{base}" fill="none" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.3"/>')
    # darkened windows: lights out, everyone asleep
    for wx in (hx - 44, hx + 22):
        out.append(f'<rect x="{wx}" y="{base-64}" width="22" height="20" fill="none" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.2"/>')
        out.append(f'<line x1="{wx+11}" y1="{base-64}" x2="{wx+11}" y2="{base-44}" stroke="{GOLD}" stroke-opacity=".45"/>')
    # tiny z's drifting from the window
    for i, (zx, zy, s) in enumerate([(hx + 56, base - 158, 8), (hx + 72, base - 180, 11), (hx + 92, base - 208, 14)]):
        out.append(f'<path d="M{zx},{zy} h{s} l-{s},{s} h{s}" fill="none" stroke="{GOLD}" '
                   f'stroke-opacity="{.75 - i*.2:.2f}" stroke-width="1.2" stroke-linejoin="round"/>')
    return defs + "".join(out)
