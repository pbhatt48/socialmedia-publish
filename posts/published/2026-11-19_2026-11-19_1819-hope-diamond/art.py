"""A large faceted diamond, one share of it lit, beside a small whole rhinestone: part of the gem beats all of the glass.
Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"
MUTED = "#8a8578"


def gem(cx, top, w, crown_h, pav_h, table_frac=0.5):
    """Return key points of a brilliant-cut gem silhouette (side view)."""
    girdle_y = top + crown_h
    tip = (cx, girdle_y + pav_h)
    tl, tr = cx - w * table_frac / 2, cx + w * table_frac / 2
    gl, gr = cx - w / 2, cx + w / 2
    return dict(top=top, girdle_y=girdle_y, tip=tip, tl=tl, tr=tr, gl=gl, gr=gr, cx=cx, w=w)


def line(x1, y1, x2, y2, op, sw=1.0):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GOLD}" '
            f'stroke-opacity="{op:.2f}" stroke-width="{sw}" stroke-linecap="round"/>')


def draw_gem(out, g, op, sw, facets=True, fill_share=False):
    t, gy, (px, py) = g["top"], g["girdle_y"], g["tip"]
    tl, tr, gl, gr, cx, w = g["tl"], g["tr"], g["gl"], g["gr"], g["cx"], g["w"]
    # Girdle points along the width
    n = 8
    gxs = [gl + w * i / n for i in range(n + 1)]
    txs = [tl + (tr - tl) * i / 4 for i in range(5)]
    if fill_share:
        # One lit share: a pavilion wedge from girdle to tip, plus the crown facet above it
        a, b = gxs[4], gxs[5]
        out.append(f'<path d="M{a:.1f},{gy:.1f} L{b:.1f},{gy:.1f} L{px:.1f},{py:.1f} Z" fill="{GOLD}" fill-opacity=".5"/>')
        out.append(f'<path d="M{txs[2]:.1f},{t:.1f} L{txs[3]:.1f},{t:.1f} L{b:.1f},{gy:.1f} L{a:.1f},{gy:.1f} Z" '
                   f'fill="{GOLD}" fill-opacity=".3"/>')
    # Outline
    out.append(f'<path d="M{tl:.1f},{t:.1f} L{tr:.1f},{t:.1f} L{gr:.1f},{gy:.1f} L{px:.1f},{py:.1f} L{gl:.1f},{gy:.1f} Z" '
               f'fill="none" stroke="{GOLD}" stroke-opacity="{op:.2f}" stroke-width="{sw}" stroke-linejoin="round"/>')
    out.append(line(gl, gy, gr, gy, op, sw))
    if not facets:
        out.append(line(cx, t, cx, gy, op * 0.5, sw * 0.7))
        out.append(line(cx, gy, px, py, op * 0.5, sw * 0.7))
        return
    # Crown facets: table points to girdle points (zig-zag star facets)
    for i in range(5):
        j = min(2 * i, n)
        out.append(line(txs[i], t, gxs[j], gy, op * 0.55, sw * 0.6))
        if 2 * i + 1 <= n and i < 4:
            out.append(line(txs[i], t, gxs[2 * i + 1], gy, op * 0.35, sw * 0.5))
            out.append(line(txs[i + 1], t, gxs[2 * i + 1], gy, op * 0.35, sw * 0.5))
    # Pavilion facets: girdle points to tip, with a lower-girdle break
    for i, gx in enumerate(gxs[1:-1], 1):
        out.append(line(gx, gy, px, py, op * (0.5 if i % 2 == 0 else 0.3), sw * 0.55))


def build():
    out = []
    ground = 452
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".22"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    out.append(f'<line x1="90" y1="{ground}" x2="810" y2="{ground}" stroke="{GOLD}" stroke-opacity=".4" stroke-width="1"/>')

    # The great diamond, floating, one share of it lit
    big = gem(cx=370, top=78, w=320, crown_h=84, pav_h=226)
    out.append(f'<circle cx="370" cy="215" r="175" fill="url(#glow)"/>')
    draw_gem(out, big, 0.95, 1.6, facets=True, fill_share=True)
    sx, sy = 520, 64
    for k in range(8):
        a = k * math.pi / 4
        r1, r2 = (6, 20) if k % 2 == 0 else (5, 12)
        out.append(line(sx + r1 * math.cos(a), sy + r1 * math.sin(a), sx + r2 * math.cos(a), sy + r2 * math.sin(a), 0.5, 1.0))
    out.append(f'<ellipse cx="370" cy="{ground}" rx="56" ry="3" fill="{GOLD}" fill-opacity=".16"/>')

    # The small rhinestone, wholly owned, resting on the ground
    small = gem(cx=640, top=ground - 50, w=60, crown_h=16, pav_h=34)
    draw_gem(out, small, 0.42, 1.1, facets=False)

    # Tiny labels
    for x, lab in ((370, "PART OF THE GEM"), (640, "ALL OF THE GLASS")):
        out.append(line(x, ground + 8, x, ground + 16, 0.5))
        out.append(f'<text x="{x}" y="{ground + 40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="{MUTED}">{lab}</text>')
    return defs + "".join(out)
