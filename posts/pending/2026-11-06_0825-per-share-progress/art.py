"""Size vs. per-share: a big pie cut into many thin slices beside a smaller pie whose few slices are each larger."""
import math

GOLD = "#c9a96a"

def pie(out, cx, cy, r, n, hi_alpha, rot=-math.pi / 2):
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{GOLD}" stroke-opacity=".85" stroke-width="1.4" fill="none"/>')
    a0, a1 = rot, rot + 2 * math.pi / n
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    out.append(f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f} Z" '
               f'fill="{GOLD}" fill-opacity="{hi_alpha}" stroke="{GOLD}" stroke-width="1.2"/>')
    for i in range(n):
        a = rot + 2 * math.pi * i / n
        op = 0.55 if i in (0, 1) else 0.28
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + r*math.cos(a):.1f}" y2="{cy + r*math.sin(a):.1f}" '
                   f'stroke="{GOLD}" stroke-opacity="{op}" stroke-width=".8"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="2.2" fill="{GOLD}"/>')

def build():
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    pie(out, 255, ground - 182, 172, 36, 0.5)
    pie(out, 650, ground - 150, 140, 6, 0.42)
    out.append(f'<path d="M455,250 L505,250 M497,244 L505,250 L497,256" stroke="{GOLD}" stroke-opacity=".5" '
               f'stroke-width="1.1" fill="none" stroke-linecap="round"/>')
    for tx, lab in [(255, "SIZE"), (650, "PER SHARE")]:
        out.append(f'<line x1="{tx}" y1="{ground+6}" x2="{tx}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    return "".join(out)
