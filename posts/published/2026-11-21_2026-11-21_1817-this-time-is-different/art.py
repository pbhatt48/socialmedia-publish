"""Repeating boom-and-bust arcs: each 'new era' traces the same shape as the last."""
import math

GOLD = "#c9a96a"


def bubble(x0, w, h, ground, steps=60):
    """A slow rise, a steep peak, a fast collapse back toward the ground."""
    pts = []
    for i in range(steps + 1):
        t = i / steps
        if t < 0.78:
            u = t / 0.78
            y = h * (u ** 2.4)
        else:
            u = (t - 0.78) / 0.22
            y = h * (1 - u) ** 1.6 * (1 - 0.15 * u) + h * 0.12 * u
        pts.append((x0 + w * t, ground - 8 - y))
    return pts


def path(pts):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def build():
    out = []
    ground = 420
    out.append(f'<line x1="20" y1="{ground}" x2="880" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    starts = [40, 235, 430, 625]
    w, h = 175, 250
    for k, x0 in enumerate(starts):
        pts = bubble(x0, w, h, ground)
        last = k == len(starts) - 1
        if last:
            rise = [p for p in pts if p[0] <= x0 + w * 0.78]
            fall = [p for p in pts if p[0] >= x0 + w * 0.78]
            out.append(f'<path d="{path(rise)}" stroke="{GOLD}" stroke-width="2" fill="none" stroke-linecap="round"/>')
            out.append(f'<path d="{path(fall)}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1.4" '
                       f'stroke-dasharray="2 6" fill="none" stroke-linecap="round"/>')
            px, py = rise[-1]
            out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="24" fill="url(#glow)"/>')
            out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="{GOLD}"/>')
        else:
            a = 0.25 + 0.15 * k
            out.append(f'<path d="{path(pts)}" stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="1.3" fill="none" stroke-linecap="round"/>')
        # faint ghost of the previous cycle superimposed on this one
        if k > 0:
            out.append(f'<path d="{path(bubble(x0, w, h, ground))}" stroke="{GOLD}" stroke-opacity=".12" '
                       f'stroke-width="6" fill="none" stroke-linecap="round"/>')
        out.append(f'<line x1="{x0 + w*0.78:.1f}" y1="{ground+6}" x2="{x0 + w*0.78:.1f}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
    labels = ["AGAIN", "AND AGAIN", "AND AGAIN", "THIS TIME?"]
    for x0, lab in zip(starts, labels):
        out.append(f'<text x="{x0 + w*0.78:.1f}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="12" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
