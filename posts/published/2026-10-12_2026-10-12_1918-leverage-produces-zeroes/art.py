"""Leverage: a long run of rising bars, magnified, ending in a single zero. SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"

def build():
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    n = 15
    x0, dx = 110, 44
    tops = []
    for i in range(n):
        x = x0 + i * dx
        h = 28 * math.exp(0.174 * i)
        h = min(h, 330)
        top = ground - h
        tops.append((x, top))
        a = 0.35 + 0.6 * i / (n - 1)
        out.append(f'<line x1="{x}" y1="{ground}" x2="{x}" y2="{top:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity="{a:.2f}" stroke-width="2.2" stroke-linecap="round"/>')
        out.append(f'<circle cx="{x}" cy="{top:.1f}" r="2.2" fill="{GOLD}" fill-opacity="{a:.2f}"/>')
    # dashed curve through the tops
    d = "M" + " L".join(f"{x},{y:.1f}" for x, y in tops)
    out.insert(1, f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1" stroke-dasharray="2 6" fill="none"/>')
    # the fall: from last top straight down to zero
    lx, ly = tops[-1]
    zx = lx + 70
    out.append(f'<path d="M{lx},{ly:.1f} C{lx+40},{ly:.1f} {zx-6},{ground-120} {zx},{ground-14}" stroke="{GOLD}" '
               f'stroke-opacity=".55" stroke-width="1.2" stroke-dasharray="3 5" fill="none"/>')
    out.append(f'<circle cx="{zx}" cy="{ground-8}" r="8" fill="none" stroke="{GOLD}" stroke-width="1.6"/>')
    out.append(f'<circle cx="{zx}" cy="{ground-8}" r="34" fill="url(#glow)"/>')
    out.append(f'<text x="{zx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
               f'letter-spacing="3" fill="#8a8578">× 0</text>')
    out.append(f'<text x="{x0}" y="{ground+40}" text-anchor="start" font-family="Inter" font-size="13" '
               f'letter-spacing="3" fill="#8a8578">YEAR 1</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".4"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
