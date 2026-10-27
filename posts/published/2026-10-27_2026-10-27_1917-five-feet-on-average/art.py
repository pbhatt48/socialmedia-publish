"""Stream cross-section: the average depth hides the one place that drowns you."""
import math

GOLD = "#c9a96a"
GREY = "#8a8578"


def bed_y(x):
    # Riverbed profile: mostly shallow, one deep channel near x=600.
    base = 300 + 40 * math.sin((x - 120) / 660 * math.pi)
    channel = 150 * math.exp(-((x - 610) / 48) ** 2)
    ripple = 6 * math.sin(x / 23)
    return base + channel + ripple


def build():
    out = []
    surface = 150
    x0, x1 = 120, 780
    xs = list(range(x0, x1 + 1, 4))
    pts = [(x, bed_y(x)) for x in xs]
    # Banks rising to the surface at each end.
    bed = f"M60,{surface} C90,{surface} 100,{pts[0][1]-30:.1f} {x0},{pts[0][1]:.1f} "
    bed += " ".join(f"L{x},{y:.1f}" for x, y in pts)
    bed += f" C800,{pts[-1][1]-30:.1f} 810,{surface} 840,{surface}"
    # Faint water fill and the bed line.
    out.append(f'<path d="{bed} L840,{surface} L60,{surface} Z" fill="{GOLD}" fill-opacity=".05"/>')
    out.append(f'<path d="{bed}" stroke="{GOLD}" stroke-opacity=".85" stroke-width="1.6" fill="none" stroke-linejoin="round"/>')
    # Sediment hatching below the bed.
    for x, y in pts[::3]:
        out.append(f'<line x1="{x}" y1="{y+6:.1f}" x2="{x-8}" y2="{y+16:.1f}" stroke="{GOLD}" stroke-opacity=".18" stroke-width="1"/>')
    # Ground/horizon line through the banks.
    out.append(f'<line x1="20" y1="{surface}" x2="60" y2="{surface}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    out.append(f'<line x1="840" y1="{surface}" x2="880" y2="{surface}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # Water surface with gentle ripples.
    for i, op in enumerate((.7, .35, .18)):
        yy = surface + i * 7
        d = f"M{70+i*14},{yy} " + " ".join(
            f"Q{x+10},{yy-3 if (x//20)%2 else yy+3} {x+20},{yy}" for x in range(70 + i * 14, 820 - i * 14, 20))
        out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity="{op}" stroke-width="1" fill="none"/>')
    # Average depth: dashed line.
    avg = sum(y for _, y in pts) / len(pts)
    out.append(f'<line x1="{x0}" y1="{avg:.1f}" x2="{x1}" y2="{avg:.1f}" stroke="{GOLD}" stroke-opacity=".55" '
               f'stroke-width="1.1" stroke-dasharray="3 7" stroke-linecap="round"/>')
    out.append(f'<text x="{x0+6}" y="{avg+24:.1f}" font-family="Inter" font-size="13" letter-spacing="3" fill="{GREY}">AVERAGE · 5 FT</text>')
    # Measuring rod in the shallows: six feet, taller than average depth.
    rx = 300
    six = (avg - surface) * 6 / 5
    rod_top = bed_y(rx) - six
    out.append(f'<line x1="{rx}" y1="{bed_y(rx):.1f}" x2="{rx}" y2="{rod_top:.1f}" stroke="{GOLD}" stroke-width="2" stroke-linecap="round"/>')
    for k in range(7):
        ty = bed_y(rx) - six * k / 6
        w = 7 if k % 3 == 0 else 4
        out.append(f'<line x1="{rx}" y1="{ty:.1f}" x2="{rx+w}" y2="{ty:.1f}" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1"/>')
    out.append(f'<text x="{rx}" y="{rod_top-12:.1f}" text-anchor="middle" font-family="Inter" font-size="13" letter-spacing="3" fill="{GREY}">6 FT</text>')
    # The deep channel: a plumb line down to the bottom.
    cx = 610
    cy = bed_y(cx)
    out.append(f'<line x1="{cx}" y1="{surface+14}" x2="{cx}" y2="{cy-8:.1f}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1"/>')
    out.append(f'<path d="M{cx-5},{cy-14:.1f} L{cx+5},{cy-14:.1f} L{cx},{cy-4:.1f} Z" fill="{GOLD}" fill-opacity=".85"/>')
    out.append(f'<circle cx="{cx}" cy="{cy-30:.1f}" r="38" fill="url(#glow)"/>')
    out.append(f'<text x="{cx+44}" y="{cy-22:.1f}" font-family="Inter" font-size="13" letter-spacing="3" fill="{GREY}">THE ONE</text>')
    out.append(f'<text x="{cx+44}" y="{cy-2:.1f}" font-family="Inter" font-size="13" letter-spacing="3" fill="{GREY}">THAT MATTERS</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
