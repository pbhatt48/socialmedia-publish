"""Castle behind a moat: durable competitive advantage. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"

def line(pts, w=1.2, a=0.9, close=False):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + (" Z" if close else "")
    return (f'<path d="{d}" stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="{w}" '
            f'fill="none" stroke-linejoin="round" stroke-linecap="round"/>')

def tower(x, base, w, h, a):
    out = []
    top = base - h
    pts = [(x - w/2, base), (x - w/2, top)]
    m = w / 5
    for i in range(5):
        x0 = x - w/2 + i*m
        if i % 2 == 0:
            pts += [(x0, top - 10), (x0 + m, top - 10), (x0 + m, top)]
        else:
            pts += [(x0 + m, top)]
    pts += [(x + w/2, base)]
    out.append(line(pts, 1.4, a))
    out.append(line([(x, top + 22), (x, top + 36)], 1.2, a * 0.7))
    return out

def build():
    out = []
    ground = 360
    cx = 450
    # far horizon
    out.append(f'<line x1="20" y1="{ground}" x2="880" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # curtain wall
    wl, wr, wt = cx - 130, cx + 130, ground - 110
    pts = [(wl, ground), (wl, wt)]
    n = 13
    step = (wr - wl) / n
    for i in range(n):
        x0 = wl + i * step
        if i % 2 == 0:
            pts += [(x0, wt - 8), (x0 + step, wt - 8), (x0 + step, wt)]
        else:
            pts += [(x0 + step, wt)]
    pts += [(wr, ground)]
    out.append(line(pts, 1.3, .8))
    # gate
    out.append(f'<path d="M{cx-22},{ground} L{cx-22},{ground-40} A22,22 0 0 1 {cx+22},{ground-40} L{cx+22},{ground}" '
               f'stroke="{GOLD}" stroke-width="1.3" stroke-opacity=".9" fill="none"/>')
    for gx in range(-14, 16, 7):
        out.append(line([(cx+gx, ground-55+abs(gx)*0.3), (cx+gx, ground)], .7, .4))
    # towers + keep
    out += tower(wl, ground, 44, 150, .9)
    out += tower(wr, ground, 44, 150, .9)
    out += tower(cx, wt, 70, 90, .95)
    # pennant
    kt = wt - 90 - 10
    out.append(line([(cx, kt), (cx, kt - 34)], 1.1, .9))
    out.append(f'<path d="M{cx},{kt-34} L{cx+20},{kt-28} L{cx},{kt-22} Z" fill="{GOLD}" fill-opacity=".8"/>')
    # moat: wavy lines below ground, widening, fading
    for k in range(5):
        y = ground + 14 + k * 13
        amp = 2.4 - k * 0.3
        half = 300 + k * 60
        p = []
        for i in range(0, 121):
            t = i / 120
            x = cx - half + 2 * half * t
            p.append((x, y + amp * math.sin(t * math.pi * (22 + k * 4))))
        out.append(line(p, 1.0, .75 - k * .13))
    # drawbridge raised (chains)
    out.append(line([(cx-22, ground-40), (cx-10, ground-6)], .6, .35))
    out.append(line([(cx+22, ground-40), (cx+10, ground-6)], .6, .35))
    # competitors: dashed arrows halting at moat edge
    for side in (-1, 1):
        for j, yy in enumerate((ground - 30, ground - 70, ground - 110)):
            x1 = cx + side * (400 - j * 12)
            x2 = cx + side * (230 + j * 8)
            a = .45 - j * .1
            out.append(f'<line x1="{x1}" y1="{yy}" x2="{x2}" y2="{yy}" stroke="{GOLD}" stroke-opacity="{a:.2f}" '
                       f'stroke-width="1" stroke-dasharray="2 6" stroke-linecap="round"/>')
            out.append(line([(x2 + side*7, yy - 5), (x2, yy), (x2 + side*7, yy + 5)], 1, a))
    # labels
    out.append(f'<text x="{cx}" y="{ground+100}" text-anchor="middle" font-family="Inter" font-size="13" '
               f'letter-spacing="4" fill="#8a8578">THE MOAT</text>')
    for side, lab in ((-1, "COMPETITION"), (1, "COMPETITION")):
        out.append(f'<text x="{cx + side*350}" y="{ground-140}" text-anchor="middle" font-family="Inter" font-size="11" '
                   f'letter-spacing="3" fill="#8a8578" fill-opacity=".8">{lab}</text>')
    return "".join(out)
