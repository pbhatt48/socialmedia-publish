"""Capital poured into ever-larger growth while earnings stay flat: the gruesome business. SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"
MUTED = "#8a8578"

def plane(x, y, s, ang):
    # minimal airliner silhouette in outline, nose pointing along ang (degrees)
    p = (f'M{-38*s},0 C{-30*s},{-5*s} {24*s},{-6*s} {36*s},{-2*s} Q{42*s},0 {36*s},{2*s} '
         f'C{24*s},{6*s} {-30*s},{5*s} {-38*s},0 Z')
    wing = f'M{2*s},{-3*s} L{-14*s},{-28*s} L{-6*s},{-28*s} L{16*s},{-3*s} M{2*s},{3*s} L{-14*s},{26*s} L{-6*s},{26*s} L{16*s},{3*s}'
    tail = f'M{-30*s},{-3*s} L{-38*s},{-16*s} L{-33*s},{-16*s} L{-24*s},{-4*s}'
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({-ang:.1f})" stroke="{GOLD}" stroke-width="1.2" '
            f'fill="none" stroke-linejoin="round" stroke-opacity=".9">'
            f'<path d="{p}"/><path d="{wing}"/><path d="{tail}"/></g>')

def build():
    out = []
    ground = 400
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # capital required: bars growing year by year
    n = 9
    x0, step, w = 150, 66, 26
    tops = []
    for i in range(n):
        h = 34 * (1.32 ** i)
        h = min(h, 300)
        x = x0 + i * step
        a = 0.18 + 0.07 * i
        out.append(f'<rect x="{x-w/2:.1f}" y="{ground-h:.1f}" width="{w}" height="{h:.1f}" fill="{GOLD}" '
                   f'fill-opacity="{a*0.35:.2f}" stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="1"/>')
        # stacked coin lines inside the bar
        for k in range(int(h // 9)):
            yy = ground - 6 - k * 9
            out.append(f'<line x1="{x-w/2+4:.1f}" y1="{yy:.1f}" x2="{x+w/2-4:.1f}" y2="{yy:.1f}" '
                       f'stroke="{GOLD}" stroke-opacity="{a*0.6:.2f}" stroke-width=".7"/>')
        tops.append((x, ground - h))
    # growth trajectory over the bars
    d = "M" + " L".join(f"{x:.1f},{y-16:.1f}" for x, y in tops)
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".4" stroke-width="1.2" stroke-dasharray="2 7" '
               f'fill="none" stroke-linecap="round"/>')
    lx, ly = tops[-1]
    px, py = tops[-2]
    ang = math.degrees(math.atan2(py - ly, lx - px))
    out.append(plane(lx + 28, ly - 44, 1.0, min(ang, 35)))
    # earnings: a flat line hugging the ground
    out.append(f'<path d="M{x0-w/2},{ground-5} C340,{ground-9} 460,{ground-2} 600,{ground-7} S700,{ground-4} {x0+(n-1)*step+w/2},{ground-6}" '
               f'stroke="{GOLD}" stroke-width="2" fill="none" stroke-linecap="round"/>')
    out.append(f'<text x="{x0-w/2}" y="{ground+36}" font-family="Inter" font-size="13" letter-spacing="3" fill="{MUTED}">CAPITAL IN</text>')
    out.append(f'<text x="{x0+(n-1)*step+w/2}" y="{ground+36}" text-anchor="end" font-family="Inter" font-size="13" '
               f'letter-spacing="3" fill="{MUTED}">EARNINGS ≈ 0</text>')
    return "".join(out)
