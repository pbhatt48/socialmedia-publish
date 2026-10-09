"""Optimism vs arithmetic: a balloon drifting off on hope beside a column built block by measured block."""
import math

GOLD = "#c9a96a"

def build():
    out = []
    ground = 430
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # Optimism: a balloon on a loose string, untethered, drifting upward
    bx, by, r = 250, 130, 46
    out.append(f'<ellipse cx="{bx}" cy="{by}" rx="{r}" ry="{r*1.15:.1f}" stroke="{GOLD}" stroke-opacity=".55" '
               f'stroke-width="1.3" fill="{GOLD}" fill-opacity=".05"/>')
    for k in (-0.5, 0, 0.5):
        out.append(f'<path d="M{bx+k*r*1.6:.1f},{by-r*1.1:.1f} Q{bx+k*r*0.4:.1f},{by} {bx+k*r*0.5:.1f},{by+r*1.12:.1f}" '
                   f'stroke="{GOLD}" stroke-opacity=".2" stroke-width=".8" fill="none"/>')
    out.append(f'<path d="M{bx-5},{by+r*1.15+6:.1f} L{bx},{by+r*1.15:.1f} L{bx+5},{by+r*1.15+6:.1f} Z" fill="{GOLD}" fill-opacity=".5"/>')
    pts = []
    for i in range(41):
        t = i / 40
        y = by + r * 1.15 + 6 + t * 170
        x = bx + 14 * math.sin(t * 9) * (0.4 + t)
        pts.append(f"{x:.1f},{y:.1f}")
    out.append(f'<polyline points="{" ".join(pts)}" stroke="{GOLD}" stroke-opacity=".35" stroke-width=".9" fill="none"/>')
    # dotted wishful trajectory
    out.append(f'<path d="M{bx+20},{by-70} C{bx+60},{by-95} {bx+110},{by-100} {bx+150},{by-95}" stroke="{GOLD}" '
               f'stroke-opacity=".3" stroke-width="1.1" stroke-dasharray="2 7" fill="none" stroke-linecap="round"/>')

    # Arithmetic: a column of counted blocks with ruler ticks
    cx, w, h, n = 620, 120, 30, 9
    for i in range(n):
        y = ground - (i + 1) * h
        a = 0.9 - i * 0.05
        out.append(f'<rect x="{cx-w/2+0.5:.1f}" y="{y+1.5:.1f}" width="{w-1}" height="{h-3}" stroke="{GOLD}" '
                   f'stroke-opacity="{a:.2f}" stroke-width="1.2" fill="{GOLD}" fill-opacity="{0.04+i*0.008:.3f}"/>')
    top = ground - n * h
    out.append(f'<rect x="{cx-w/2-10}" y="{top-8}" width="{w+20}" height="8" fill="{GOLD}" fill-opacity=".75"/>')
    out.append(f'<rect x="{cx-w/2-10}" y="{ground-6}" width="{w+20}" height="6" fill="{GOLD}" fill-opacity=".75"/>')
    rx = cx + w / 2 + 34
    out.append(f'<line x1="{rx}" y1="{ground}" x2="{rx}" y2="{top}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1"/>')
    for i in range(n * 2 + 1):
        y = ground - i * h / 2
        L = 10 if i % 2 == 0 else 5
        out.append(f'<line x1="{rx}" y1="{y:.1f}" x2="{rx+L}" y2="{y:.1f}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1"/>')
    for i, lab in ((0, "0"), (3, "3"), (6, "6"), (9, "9")):
        y = ground - i * h
        out.append(f'<text x="{rx+18}" y="{y+4:.1f}" font-family="Inter" font-size="11" fill="#8a8578">{lab}</text>')

    for tx, lab in ((250, "OPTIMISM"), (620, "ARITHMETIC")):
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    return "".join(out)
