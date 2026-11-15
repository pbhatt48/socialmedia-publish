"""The institutional imperative: a procession of identical markers following one
another toward a ledge, while a single marker turns aside onto its own path.
Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"


def chevron(x, y, ang, size, alpha, width=1.6):
    """A small arrowhead pointing along ang (radians, SVG y-down)."""
    c, s = math.cos(ang), math.sin(ang)
    def pt(dx, dy):
        return x + dx * c - dy * s, y + dx * s + dy * c
    a = pt(-size, -size * 0.75)
    b = pt(0, 0)
    d = pt(-size, size * 0.75)
    return (f'<path d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f} L{d[0]:.1f},{d[1]:.1f}" '
            f'stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="{width}" fill="none" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def build():
    out = []
    ground = 400
    ledge = 640
    # ground: a plateau that ends at a ledge, then a faint drop
    out.append(f'<line x1="40" y1="{ground}" x2="{ledge}" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    out.append(f'<path d="M{ledge},{ground} L{ledge+6},{ground+70} L{ledge+2},{ground+96}" stroke="{GOLD}" '
               f'stroke-opacity=".3" stroke-width="1" fill="none"/>')
    out.append(f'<line x1="{ledge+40}" y1="{ground+96}" x2="860" y2="{ground+96}" stroke="{GOLD}" stroke-opacity=".18" stroke-width="1"/>')
    # hatching under the plateau edge
    for i in range(6):
        y = ground + 12 + i * 13
        out.append(f'<line x1="{ledge-28+i*4}" y1="{y}" x2="{ledge-4+i*1.5}" y2="{y}" stroke="{GOLD}" stroke-opacity=".14"/>')

    # the procession: identical chevrons on a shared track toward the ledge
    track_y = ground - 26
    out.append(f'<line x1="70" y1="{track_y}" x2="{ledge}" y2="{track_y}" stroke="{GOLD}" stroke-opacity=".22" '
               f'stroke-width="1" stroke-dasharray="2 8" stroke-linecap="round"/>')
    xs = [110 + i * 42 for i in range(13)]
    for i, x in enumerate(xs):
        alpha = 0.35 + 0.55 * (i / (len(xs) - 1))
        out.append(chevron(x, track_y, 0, 10, alpha))
    # the leaders already tipping over the edge
    for k, (dx, dy, ang) in enumerate([(26, 22, 0.9), (34, 62, 1.25)]):
        out.append(chevron(ledge + dx, track_y + dy, ang, 10, 0.5 - k * 0.2))

    # the dissenter: one marker breaks from the line and climbs its own path
    bx = xs[5]
    path = f"M{bx},{track_y} C{bx+40},{track_y-10} {bx+70},{track_y-120} {bx+150},{track_y-190} S{bx+290},{track_y-268} {bx+330},{track_y-276}"
    out.append(f'<path d="{path}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.3" fill="none" stroke-linecap="round"/>')
    ex, ey = bx + 330, track_y - 276
    out.append(chevron(ex + 2, ey - 0.5, -0.05, 13, 0.95, 2.0))
    out.append(f'<circle cx="{ex+2}" cy="{ey}" r="34" fill="url(#glow)"/>')
    # a small ring marking where it left the herd
    out.append(f'<circle cx="{bx}" cy="{track_y}" r="15" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1" fill="none"/>')

    # tiny labels
    lab = 'font-family="Inter" font-size="12" letter-spacing="3" fill="#8a8578"'
    out.append(f'<text x="{(xs[0]+xs[-1])/2:.0f}" y="{ground+40}" text-anchor="middle" {lab}>IMITATION</text>')
    out.append(f'<text x="{ex+2}" y="{ey-30}" text-anchor="middle" {lab}>INDEPENDENT THOUGHT</text>')

    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".4"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
