"""Reality drifts gently between 'pretty good' and 'not so hot' while perception swings
wildly from 'flawless' to 'hopeless'. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"
MUTED = "#8a8578"

def wave(x0, x1, mid, amp_fn, period, phase, steps=360):
    pts = []
    for i in range(steps + 1):
        x = x0 + (x1 - x0) * i / steps
        t = (x - x0) / period * 2 * math.pi + phase
        pts.append((x, mid - amp_fn(x) * math.sin(t)))
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)

def build():
    out = []
    x0, x1 = 170, 730
    P = 214
    ph = math.pi / 2 - 2 * math.pi * (x1 - x0) / P
    mid = 230
    top, bot = 80, 380
    ground = 450
    # extreme bounds: faint dashed guides
    for y, lab in ((top, "FLAWLESS"), (bot, "HOPELESS")):
        out.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{GOLD}" stroke-opacity=".22" '
                   f'stroke-width=".8" stroke-dasharray="2 6"/>')
        out.append(f'<text x="{x0-16}" y="{y+4}" text-anchor="end" font-family="Inter" font-size="12" '
                   f'letter-spacing="3" fill="{MUTED}">{lab}</text>')
    # the narrow band where reality actually lives
    band = 22
    out.append(f'<rect x="{x0}" y="{mid-band}" width="{x1-x0}" height="{2*band}" fill="{GOLD}" fill-opacity=".06"/>')
    for y, lab in ((mid - band, "PRETTY GOOD"), (mid + band, "NOT SO HOT")):
        out.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{GOLD}" stroke-opacity=".18" stroke-width=".6"/>')
        out.append(f'<text x="{x0-16}" y="{y+4}" text-anchor="end" font-family="Inter" font-size="10" '
                   f'letter-spacing="2.5" fill="{MUTED}" fill-opacity=".8">{lab}</text>')
    # perception: wide swings, echoed faintly
    swing = lambda x: 146 * (0.72 + 0.28 * math.sin((x - x0) / 210))
    for k, op, w in ((3, .10, .7), (2, .16, .8), (1, .26, .9)):
        out.append(f'<path d="{wave(x0, x1, mid, swing, P, ph + k*0.11)}" stroke="{GOLD}" '
                   f'stroke-opacity="{op}" stroke-width="{w}" fill="none"/>')
    out.append(f'<path d="{wave(x0, x1, mid, swing, P, ph)}" stroke="{GOLD}" stroke-opacity=".85" '
               f'stroke-width="1.6" fill="none" stroke-linecap="round"/>')
    # reality: a calm, slow line
    out.append(f'<path d="{wave(x0, x1, mid, lambda x: 11, 300, 1.1)}" stroke="{GOLD}" stroke-opacity="1" '
               f'stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    # right-hand labels
    out.append(f'<text x="{x1+16}" y="{mid+4}" font-family="Inter" font-size="11" letter-spacing="3" fill="{GOLD}">REALITY</text>')
    py = mid - swing(x1) * math.sin((x1 - x0) / P * 2 * math.pi + ph)
    out.append(f'<circle cx="{x1}" cy="{py:.1f}" r="3.5" fill="{GOLD}"/>')
    out.append(f'<text x="{x1+16}" y="{py+4:.1f}" font-family="Inter" font-size="11" letter-spacing="3" '
               f'fill="{MUTED}">PERCEPTION</text>')
    # horizon
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    return "".join(out)
