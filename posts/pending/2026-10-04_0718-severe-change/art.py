"""Fortress on bedrock vs. shifting, fractured terrain: stability over severe change. SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"

def line(out, pts, w=1.0, a=0.6, dash=None):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="{w}" fill="none" '
               f'stroke-linejoin="round" stroke-linecap="round"{ds}/>')

def build():
    out = []
    rnd = random.Random(1987)
    ground = 360
    # left: violently shifting terrain, broken strata
    for k in range(6):
        y0 = ground + 14 + k * 18
        pts, x = [], 40
        while x < 380:
            pts.append((x, y0 + rnd.uniform(-10, 10) * (1 + k * 0.25) * (1 - x / 520)))
            x += rnd.uniform(14, 26)
        pts.append((380, y0))
        line(out, pts, 0.9, 0.42 - k * 0.05)
    # surface of the shifting ground: jagged, seismograph-like
    pts, x = [], 40
    while x < 380:
        amp = 46 * (1 - (x - 40) / 360) ** 1.4
        pts.append((x, ground - rnd.uniform(-amp, amp)))
        x += rnd.uniform(9, 16)
    pts.append((380, ground))
    line(out, pts, 1.3, 0.75)
    # fault cracks
    for cx in (110, 200, 290):
        cpts, y, xx = [], ground + 4, cx
        while y < ground + 115:
            cpts.append((xx, y)); y += rnd.uniform(10, 18); xx += rnd.uniform(-7, 7)
        line(out, cpts, 0.8, 0.35)
    # a toppled block on the shifting side
    out.append(f'<g transform="rotate(-14 170 {ground-30})"><rect x="150" y="{ground-50}" width="40" height="32" '
               f'stroke="{GOLD}" stroke-opacity=".5" stroke-width="1" fill="none"/></g>')
    # right: calm level ground and bedrock strata
    line(out, [(380, ground), (860, ground)], 1.2, 0.6)
    for k in range(6):
        line(out, [(400, ground + 14 + k * 18), (860 - k * 6, ground + 14 + k * 18)], 0.9, 0.38 - k * 0.05)
    # fortress
    fx, fw, fh = 560, 220, 120
    top = ground - fh
    out.append(f'<rect x="{fx}" y="{top}" width="{fw}" height="{fh}" fill="{GOLD}" fill-opacity=".06" '
               f'stroke="{GOLD}" stroke-opacity=".85" stroke-width="1.4"/>')
    # crenellations
    n, cw = 11, fw / 11
    for i in range(n):
        if i % 2 == 0 and 0 < i < n - 1:
            out.append(f'<rect x="{fx+i*cw:.1f}" y="{top-14}" width="{cw:.1f}" height="14" fill="none" '
                       f'stroke="{GOLD}" stroke-opacity=".85" stroke-width="1.4"/>')
    # towers
    for tx in (fx - 30, fx + fw - 10):
        ty = top - 50
        out.append(f'<rect x="{tx}" y="{ty}" width="40" height="{ground-ty}" fill="#0b0b0c" fill-opacity=".0" '
                   f'stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.4"/>')
        for j in range(3):
            out.append(f'<rect x="{tx+j*15}" y="{ty-12}" width="10" height="12" fill="none" stroke="{GOLD}" '
                       f'stroke-opacity=".9" stroke-width="1.3"/>')
        out.append(f'<line x1="{tx+20}" y1="{ty+30}" x2="{tx+20}" y2="{ty+48}" stroke="{GOLD}" stroke-opacity=".6" stroke-width="2"/>')
    # gate
    gx = fx + fw / 2
    out.append(f'<path d="M{gx-22},{ground} L{gx-22},{ground-40} A22,22 0 0 1 {gx+22},{ground-40} L{gx+22},{ground}" '
               f'fill="none" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.3"/>')
    # masonry courses
    for r in range(1, 5):
        y = top + r * fh / 5
        line(out, [(fx, y), (gx - 26, y)], 0.6, 0.22)
        line(out, [(gx + 26, y), (fx + fw, y)], 0.6, 0.22)
    # moat (calm water)
    for k, a in ((0, .5), (1, .3)):
        y = ground + 5 + k * 5
        line(out, [(fx - 70, y), (fx + fw + 70, y)], 0.8, a, dash="10 6")
    # flag
    out.append(f'<line x1="{gx}" y1="{top-14}" x2="{gx}" y2="{top-64}" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.2"/>'
               f'<path d="M{gx},{top-64} L{gx+26},{top-57} L{gx},{top-50} Z" fill="{GOLD}" fill-opacity=".7"/>')
    # labels
    for x, lab in ((210, "FEVERISH CHANGE"), (670, "DURABLE FRANCHISE")):
        out.append(f'<text x="{x}" y="{ground+150}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    return "".join(out)
