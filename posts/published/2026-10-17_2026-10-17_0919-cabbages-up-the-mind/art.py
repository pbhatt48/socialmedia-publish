"""Munger's whirlpool: intense ideology as a vortex that pulls the current in, while a canoe slips past into open water. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"

def spiral(cx, cy, r0, r1, turns, squash, steps=360):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        a = t * turns * 2 * math.pi
        r = r0 + (r1 - r0) * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a) * squash))
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)

def build():
    out = []
    cx, cy, sq = 300, 300, 0.36
    out.append(f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".28"/>'
               f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    # far bank / horizon
    out.append(f'<line x1="30" y1="150" x2="870" y2="150" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # current lines: bend toward the vortex near it, run straight and calm far from it
    for i, y0 in enumerate(range(176, 470, 22)):
        pts = []
        for x in range(40, 861, 8):
            dx, dy = x - cx, (y0 - cy) / sq
            d = math.hypot(dx, dy)
            pull = 38 * math.exp(-(d / 210) ** 2)
            y = y0 - pull * (1 if y0 > cy else -1) * sq * 1.6 + 2.2 * math.sin(x / 47 + i)
            pts.append((x, y))
        far = abs(y0 - cy)
        op = 0.10 + 0.18 * (1 - min(far, 170) / 170)
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity="{op:.2f}" stroke-width=".8" fill="none"/>')
    # the vortex
    out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="190" ry="{190*sq:.0f}" fill="url(#glow)"/>')
    for k, (r1, op, w) in enumerate([(170, .30, .9), (140, .5, 1.1), (110, .75, 1.3)]):
        out.append(f'<path d="{spiral(cx, cy, 3, r1, 3.2 + k * 0.5, sq)}" stroke="{GOLD}" '
                   f'stroke-opacity="{op}" stroke-width="{w}" fill="none" stroke-linecap="round"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="3.2" fill="{GOLD}"/>')
    # canoe on calm water, heading away to the right
    bx, by = 650, 236
    out.append(f'<path d="M{bx-62},{by} Q{bx},{by+18} {bx+62},{by} Q{bx+66},{by-6} {bx+70},{by-10} '
               f'Q{bx},{by-2} {bx-70},{by-10} Q{bx-66},{by-6} {bx-62},{by} Z" fill="{GOLD}" fill-opacity=".85"/>')
    # paddle, blade trailing back
    out.append(f'<line x1="{bx+22}" y1="{by-46}" x2="{bx-4}" y2="{by+22}" stroke="{GOLD}" stroke-width="1.6" stroke-linecap="round"/>')
    out.append(f'<ellipse cx="{bx-6}" cy="{by+26}" rx="3.5" ry="9" transform="rotate(21 {bx-6} {by+26})" fill="{GOLD}" fill-opacity=".8"/>')
    # wake trailing behind, back toward the vortex it slipped past
    for j, op in enumerate((.45, .3, .18)):
        out.append(f'<path d="M{bx-72},{by-8+j*2} Q{bx-105-j*18},{by-14-j*5} {bx-140-j*26},{by-16-j*7}" stroke="{GOLD}" '
                   f'stroke-opacity="{op}" stroke-width=".9" fill="none"/>')
        out.append(f'<path d="M{bx-72},{by-4+j*2} Q{bx-105-j*18},{by+4+j*4} {bx-140-j*26},{by+8+j*6}" stroke="{GOLD}" '
                   f'stroke-opacity="{op*0.7:.2f}" stroke-width=".9" fill="none"/>')
    return "".join(out)
