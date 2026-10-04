"""A plumb line hanging true amid a crowd of leaning reeds: independent judgment. SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"

def build():
    rnd = random.Random(41)
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # the crowd: reeds all leaning the same way
    x = 70
    while x < 830:
        if abs(x - 450) > 46:
            h = rnd.uniform(90, 210) * (1 - 0.35 * abs(x - 450) / 400)
            lean = rnd.uniform(0.32, 0.46)
            x2 = x + h * math.sin(lean)
            y2 = ground - h * math.cos(lean)
            cx = x + h * 0.15 * math.sin(lean)
            cy = ground - h * 0.6
            a = rnd.uniform(0.18, 0.5)
            out.append(f'<path d="M{x:.1f},{ground} Q{cx:.1f},{cy:.1f} {x2:.1f},{y2:.1f}" stroke="{GOLD}" '
                       f'stroke-opacity="{a:.2f}" stroke-width="{rnd.uniform(0.7,1.4):.2f}" fill="none" stroke-linecap="round"/>')
        x += rnd.uniform(9, 17)
    # the plumb line: one true vertical
    top = 40
    out.append(f'<line x1="400" y1="{top}" x2="500" y2="{top}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.6" stroke-linecap="round"/>')
    out.append(f'<line x1="450" y1="{top}" x2="450" y2="352" stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.1"/>')
    bob = 352
    out.append(f'<path d="M444,{bob} L456,{bob} L450,{bob+38} Z" fill="{GOLD}" fill-opacity=".9"/>')
    out.append(f'<circle cx="450" cy="{bob+14}" r="34" fill="url(#glow)"/>')
    # faint reference ticks: true vertical
    for y in range(80, 340, 40):
        out.append(f'<line x1="438" y1="{y}" x2="444" y2="{y}" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1"/>')
    out.append(f'<line x1="440" y1="{ground}" x2="460" y2="{ground}" stroke="{GOLD}" stroke-opacity=".9" stroke-width="2"/>')
    out.append(f'<text x="450" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" letter-spacing="3" fill="#8a8578">DATA · REASONING</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".4"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
