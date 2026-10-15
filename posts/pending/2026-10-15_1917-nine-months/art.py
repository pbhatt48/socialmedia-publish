"""Nine lunar months rising over a horizon: some things cannot be compressed. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"

def moon(cx, cy, r, phase, alpha):
    """phase 0..1: lit fraction growing from a thin crescent to full."""
    out = [f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="none" stroke="{GOLD}" '
           f'stroke-opacity="{alpha*0.55:.2f}" stroke-width="1"/>']
    if phase >= 0.999:
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{GOLD}" fill-opacity="{alpha:.2f}"/>')
        return "".join(out)
    # lit limb on the right; terminator is an ellipse with rx = r*|1-2p|
    k = 1 - 2 * phase
    rx = abs(k) * r
    sweep = 0 if k > 0 else 1
    d = (f'M{cx:.1f},{cy-r:.1f} A{r},{r} 0 0 1 {cx:.1f},{cy+r:.1f} '
         f'A{rx:.2f},{r} 0 0 {sweep} {cx:.1f},{cy-r:.1f} Z')
    out.append(f'<path d="{d}" fill="{GOLD}" fill-opacity="{alpha:.2f}"/>')
    return "".join(out)

def build():
    out = []
    ground = 430
    out.append(f'<line x1="20" y1="{ground}" x2="880" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # faint arc the moons travel along
    xs = [90 + i * 90 for i in range(9)]
    def y_at(x):
        t = (x - 450) / 400
        return 330 - 210 * (1 - t * t)
    pts = " ".join(f"{x:.1f},{y_at(x):.1f}" for x in range(70, 831, 10))
    out.append(f'<polyline points="{pts}" stroke="{GOLD}" stroke-opacity=".28" stroke-width="1.1" '
               f'stroke-dasharray="2 7" fill="none" stroke-linecap="round"/>')
    for i, x in enumerate(xs):
        y = y_at(x)
        phase = 0.12 + 0.88 * i / 8
        alpha = 0.35 + 0.6 * i / 8
        r = 17 + i * 1.6
        if i == 8:
            out.append(f'<circle cx="{x}" cy="{y:.1f}" r="{r*2.6:.1f}" fill="url(#glow)"/>')
        out.append(moon(x, y, round(r, 1), phase, alpha))
        # tick + label on the ground
        out.append(f'<line x1="{x}" y1="{ground+6}" x2="{x}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<line x1="{x}" y1="{y+r+8:.1f}" x2="{x}" y2="{ground-4}" stroke="{GOLD}" '
                   f'stroke-opacity="{0.08+0.1*i/8:.2f}" stroke-width="0.8"/>')
        out.append(f'<text x="{x}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{"MONTH 1" if i == 0 else i + 1}</text>')
    # a small seedling at the base of the final month
    sx = xs[-1]
    out.append(f'<path d="M{sx},{ground} Q{sx-2},{ground-14} {sx},{ground-26}" stroke="{GOLD}" stroke-width="1.6" fill="none"/>'
               f'<path d="M{sx},{ground-24} q-12,-4 -16,-14 q12,0 16,14Z M{sx},{ground-26} q10,-8 18,-8 q-4,10 -18,8Z" '
               f'fill="{GOLD}" fill-opacity=".85"/>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".4"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
