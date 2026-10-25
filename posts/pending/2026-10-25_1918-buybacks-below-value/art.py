"""Ownership pies: as shares are retired, each remaining holder's slice grows. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"


def pie(out, cx, cy, r, n):
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.2" fill="none"/>')
    # the holder's slice, filled, starting at 12 o'clock
    a0, a1 = -math.pi / 2, -math.pi / 2 + 2 * math.pi / n
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    out.append(f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f} Z" '
               f'fill="{GOLD}" fill-opacity=".85"/>')
    for i in range(n):
        a = -math.pi / 2 + 2 * math.pi * i / n
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + r * math.cos(a):.1f}" y2="{cy + r * math.sin(a):.1f}" '
                   f'stroke="{GOLD}" stroke-opacity=".38" stroke-width=".9"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="2" fill="{GOLD}"/>')


def build():
    out = []
    ground = 420
    out.append(f'<line x1="20" y1="{ground}" x2="880" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    stages = [(150, 12), (350, 10), (550, 8), (750, 6)]
    r = 78
    cy = 250
    # retired shares drifting off as faint dashed slivers
    for i, (cx, n) in enumerate(stages[1:]):
        px = stages[i][0]
        out.append(f'<path d="M{px + r * 0.6:.1f},{cy - r - 10} Q{(px + cx) / 2},{cy - r - 60} {cx - r * 0.6:.1f},{cy - r - 10}" '
                   f'stroke="{GOLD}" stroke-opacity=".3" stroke-width="1" stroke-dasharray="2 6" fill="none" stroke-linecap="round"/>')
    for cx, n in stages:
        pie(out, cx, cy, r, n)
        out.append(f'<line x1="{cx}" y1="{cy + r + 8}" x2="{cx}" y2="{ground}" stroke="{GOLD}" stroke-opacity=".18" stroke-width="1"/>')
        out.append(f'<line x1="{cx}" y1="{ground + 6}" x2="{cx}" y2="{ground + 14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{cx}" y="{ground + 40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">1/{n}</text>')
    return "".join(out)
