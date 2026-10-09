"""Effortless money vs rationality: a row of balance scales, each fainter as the coin stack on one pan grows."""

GOLD = "#c9a96a"


def coins(out, x, base, n, alpha):
    for i in range(n):
        y = base - i * 6.5
        out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="17" ry="4" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" '
                   f'stroke-width="1" fill="#0d0f12" fill-opacity="1"/>')


def scale(out, x, ground, tilt, n, alpha):
    post_top = ground - 270
    out.append(f'<line x1="{x}" y1="{ground}" x2="{x}" y2="{post_top}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="1.6"/>')
    out.append(f'<path d="M{x-22},{ground} L{x+22},{ground} L{x},{ground-14} Z" fill="{GOLD}" fill-opacity="{alpha*0.6:.2f}"/>')
    out.append(f'<circle cx="{x}" cy="{post_top}" r="3.5" fill="{GOLD}" fill-opacity="{alpha:.2f}"/>')
    arm = 54
    lx, ly = x - arm, post_top + tilt
    rx, ry = x + arm, post_top - tilt
    out.append(f'<line x1="{lx}" y1="{ly}" x2="{rx}" y2="{ry}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="1.4"/>')
    for px, py, load in ((lx, ly, n), (rx, ry, 0)):
        pan_y = py + 90
        out.append(f'<path d="M{px},{py} L{px-24},{pan_y} M{px},{py} L{px+24},{pan_y}" stroke="{GOLD}" '
                   f'stroke-opacity="{alpha*0.6:.2f}" stroke-width=".8" fill="none"/>')
        out.append(f'<path d="M{px-28},{pan_y} Q{px},{pan_y+16} {px+28},{pan_y}" stroke="{GOLD}" '
                   f'stroke-opacity="{alpha:.2f}" stroke-width="1.3" fill="none"/>')
        if load:
            coins(out, px, pan_y - 2, load, min(1, alpha + 0.25))


def build():
    out = []
    ground = 430
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    specs = [(150, 0, 0, 0.9), (350, 14, 3, 0.68), (550, 28, 7, 0.45), (750, 42, 12, 0.24)]
    for x, tilt, n, a in specs:
        scale(out, x, ground, tilt, n, a)
    for x, lab in ((150, "REASON"), (750, "EUPHORIA")):
        out.append(f'<text x="{x}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    out.append(f'<path d="M210,{ground+35} L690,{ground+35}" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1" '
               f'stroke-dasharray="2 7" stroke-linecap="round"/>')
    return "".join(out)
