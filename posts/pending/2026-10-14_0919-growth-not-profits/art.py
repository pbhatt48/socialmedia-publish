"""Growth is not profit: a contrail soars across the sky while the investor's
line on the ground barely rises. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"
MUTED = "#8a8578"


def build():
    out = []
    ground = 410
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # soaring growth arc: fanned contrail strands
    x0, x1 = 90, 720
    def arc(t, off):
        y = ground - 20 - 330 * t ** 1.7
        return x0 + (x1 - x0) * t, y + off * (1 - t * 0.6)
    for k, off in enumerate([-10, -5, 0, 5, 10]):
        pts = " ".join("%.1f,%.1f" % arc(i / 80, off) for i in range(81))
        a = 0.9 if off == 0 else 0.22 + 0.06 * (2 - abs(k - 2))
        w = 1.6 if off == 0 else 0.8
        out.append(f'<polyline points="{pts}" fill="none" stroke="{GOLD}" stroke-opacity="{a:.2f}" '
                   f'stroke-width="{w}" stroke-linecap="round"/>')

    # minimal airliner at the head of the arc
    hx, hy = arc(1.0, 0)
    px, py = arc(0.985, 0)
    ang = math.degrees(math.atan2(hy - py, hx - px))
    out.append(f'<g transform="translate({hx:.1f},{hy:.1f}) rotate({ang:.1f})" fill="{GOLD}">'
               f'<path d="M-26,0 C-20,-3.4 14,-3.4 24,-1.2 C28,0 28,0 24,1.2 C14,3.4 -20,3.4 -26,0Z"/>'
               f'<path d="M2,-2 L-10,-20 L-4,-20 L12,-2Z M2,2 L-10,20 L-4,20 L12,2Z" fill-opacity=".85"/>'
               f'<path d="M-20,-1.5 L-27,-10 L-23,-10 L-15,-1.5Z M-20,1.5 L-27,10 L-23,10 L-15,1.5Z" fill-opacity=".85"/>'
               f'</g>')
    out.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="46" fill="url(#glow)"/>')

    # investor's path: nearly flat, dotted, with tiny coin markers
    ix0, ix1 = 90, 820
    pts = " ".join(f"{ix0 + (ix1 - ix0) * t:.1f},{ground - 18 - 14 * t + 6 * math.sin(t * 9):.1f}"
                   for t in [i / 80 for i in range(81)])
    out.append(f'<polyline points="{pts}" fill="none" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1.2" '
               f'stroke-dasharray="1 6" stroke-linecap="round"/>')
    for t in (0.0, 0.25, 0.5, 0.75, 1.0):
        x = ix0 + (ix1 - ix0) * t
        y = ground - 18 - 14 * t + 6 * math.sin(t * 9)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="#0f0f0f" stroke="{GOLD}" '
                   f'stroke-opacity=".7" stroke-width="1"/>')

    # gap between the two outcomes
    gx = 640
    gy_top = arc((gx - x0) / (x1 - x0), 0)[1]
    gy_bot = ground - 18 - 14 * ((gx - ix0) / (ix1 - ix0)) + 6 * math.sin(((gx - ix0) / (ix1 - ix0)) * 9)
    out.append(f'<line x1="{gx}" y1="{gy_top + 14:.1f}" x2="{gx}" y2="{gy_bot - 10:.1f}" stroke="{GOLD}" '
               f'stroke-opacity=".18" stroke-width="1" stroke-dasharray="2 5"/>')

    for x, y, lab in ((470, 170, "THE INDUSTRY"), (820, ground + 40, "THE INVESTOR")):
        anchor = "end" if x > 700 else "middle"
        out.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="{MUTED}">{lab}</text>')

    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
