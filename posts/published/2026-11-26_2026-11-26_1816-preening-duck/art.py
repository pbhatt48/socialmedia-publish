"""Every duck on the pond rises with the rain: market tide vs. paddling skill. 900x520 viewBox."""
import random

GOLD = "#c9a96a"
GREY = "#8a8578"


def duck(x, y, s=1.0, alpha=0.9, dash=None, proud=False):
    """Line-art duck floating on waterline y, facing right."""
    d = dash and f' stroke-dasharray="{dash}"' or ""
    head_y = -40 if proud else -34
    p = (f'M{x-34*s:.1f},{y-6*s:.1f} '
         f'C{x-40*s:.1f},{y-22*s:.1f} {x-28*s:.1f},{y-30*s:.1f} {x-12*s:.1f},{y-24*s:.1f} '
         f'C{x-2*s:.1f},{y-20*s:.1f} {x+6*s:.1f},{y-20*s:.1f} {x+10*s:.1f},{y-24*s:.1f} '
         f'C{x+8*s:.1f},{y+(head_y+6)*s:.1f} {x+14*s:.1f},{y+(head_y-6)*s:.1f} {x+22*s:.1f},{y+(head_y-6)*s:.1f} '
         f'C{x+30*s:.1f},{y+(head_y-6)*s:.1f} {x+34*s:.1f},{y+(head_y+2)*s:.1f} {x+32*s:.1f},{y+(head_y+8)*s:.1f} '
         f'C{x+30*s:.1f},{y+(head_y+14)*s:.1f} {x+26*s:.1f},{y-18*s:.1f} {x+30*s:.1f},{y-10*s:.1f} '
         f'C{x+32*s:.1f},{y-4*s:.1f} {x+26*s:.1f},{y:.1f} {x+14*s:.1f},{y:.1f} '
         f'L{x-24*s:.1f},{y:.1f} C{x-30*s:.1f},{y:.1f} {x-33*s:.1f},{y-3*s:.1f} {x-34*s:.1f},{y-6*s:.1f}Z')
    out = [f'<path d="{p}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="1.6" fill="none" '
           f'stroke-linejoin="round"{d}/>']
    # beak
    by = y + (head_y + 1) * s
    out.append(f'<path d="M{x+32*s:.1f},{by-2*s:.1f} L{x+44*s:.1f},{by+1*s:.1f} L{x+32*s:.1f},{by+4*s:.1f}" '
               f'stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="1.4" fill="none" stroke-linejoin="round"{d}/>')
    # eye
    out.append(f'<circle cx="{x+24*s:.1f}" cy="{y+(head_y-1)*s:.1f}" r="{1.6*s:.1f}" fill="{GOLD}" fill-opacity="{alpha:.2f}"/>')
    # wing
    out.append(f'<path d="M{x-18*s:.1f},{y-14*s:.1f} Q{x-2*s:.1f},{y-6*s:.1f} {x+12*s:.1f},{y-12*s:.1f}" '
               f'stroke="{GOLD}" stroke-opacity="{alpha*0.6:.2f}" stroke-width="1.1" fill="none"{d}/>')
    if proud:
        for i, (dx, dy) in enumerate(((54, -48), (60, -38), (54, -28))):
            out.append(f'<line x1="{x+(dx-4)*s:.1f}" y1="{y+(dy-(i-1)*2)*s:.1f}" x2="{x+(dx+8)*s:.1f}" '
                       f'y2="{y+(dy-(i-1)*6)*s:.1f}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.2" stroke-linecap="round"/>')
    return "".join(out)


def build():
    rnd = random.Random(1997)
    out = []
    low, high = 440, 285
    # rain
    for _ in range(70):
        x = rnd.uniform(160, 850)
        y = rnd.uniform(40, 200)
        L = rnd.uniform(10, 22)
        out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x-L*0.3:.1f}" y2="{y+L:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity="{rnd.uniform(.12,.32):.2f}" stroke-width="1" stroke-linecap="round"/>')
    # old water level
    out.append(f'<line x1="30" y1="{low}" x2="860" y2="{low}" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1" stroke-dasharray="3 6"/>')
    # new water level, with faint ripples below
    out.append(f'<line x1="30" y1="{high}" x2="860" y2="{high}" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.2"/>')
    for i, y in enumerate(range(high + 22, low - 8, 26)):
        a = 0.14 - i * 0.02
        x0 = 90 + (i % 2) * 40
        segs = "".join(f'M{x},{y} q12,-4 24,0 ' for x in range(x0, 820, 120))
        out.append(f'<path d="{segs}" stroke="{GOLD}" stroke-opacity="{max(a,.05):.2f}" stroke-width="1" fill="none"/>')
    xs = [250, 385, 520, 655, 790]
    for i, x in enumerate(xs):
        proud = i == 2
        out.append(duck(x, low, 1.0, alpha=0.22, dash="2 4"))
        out.append(f'<line x1="{x-6}" y1="{low-36}" x2="{x-6}" y2="{high+8}" stroke="{GOLD}" stroke-opacity=".28" '
                   f'stroke-width="1" stroke-dasharray="1 4"/>'
                   f'<path d="M{x-10},{high+14} L{x-6},{high+7} L{x-2},{high+14}" stroke="{GOLD}" stroke-opacity=".4" fill="none"/>')
        out.append(duck(x, high, 1.25 if proud else 1.0, alpha=0.95 if proud else 0.6, proud=proud))
    for y, lab in ((high, "AFTER THE RAIN"), (low, "BEFORE")):
        out.append(f'<text x="34" y="{y-10}" font-family="Inter" font-size="12" letter-spacing="3" fill="{GREY}">{lab}</text>')
    return "".join(out)
