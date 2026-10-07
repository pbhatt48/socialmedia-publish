"""Ten bets on one ground line: four wither, six grow, two tower. Being right six times in ten is enough. SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"

def stem(out, x, ground, h, alpha, lean=0.0, leaves=3):
    tx = x + lean * h
    out.append(f'<path d="M{x},{ground} Q{x + lean*h*0.2:.1f},{ground - h*0.55:.1f} {tx:.1f},{ground - h:.1f}" '
               f'stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="{1.2 + h/180:.2f}" fill="none" stroke-linecap="round"/>')
    for i in range(leaves):
        t = (i + 1) / (leaves + 1)
        ly = ground - h * t
        lx = x + lean * h * t * t
        s = 7 + h * 0.06 * (1 - t * 0.5)
        d = -1 if i % 2 else 1
        out.append(f'<path d="M{lx:.1f},{ly:.1f} q{d*s*0.9:.1f},{-s*0.2:.1f} {d*s*1.6:.1f},{-s*0.9:.1f} '
                   f'q{-d*s*1.0:.1f},{-s*0.1:.1f} {-d*s*1.6:.1f},{s*0.9:.1f}Z" fill="{GOLD}" fill-opacity="{alpha*0.55:.2f}" '
                   f'stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width=".7"/>')
    out.append(f'<circle cx="{tx:.1f}" cy="{ground - h:.1f}" r="{2 + h/120:.1f}" fill="{GOLD}" fill-opacity="{alpha:.2f}"/>')

def wilted(out, x, ground, alpha=0.4):
    out.append(f'<path d="M{x},{ground} Q{x+2},{ground-26} {x+16},{ground-30} Q{x+24},{ground-30} {x+26},{ground-20}" '
               f'stroke="{GOLD}" stroke-opacity="{alpha}" stroke-width="1.1" fill="none" stroke-linecap="round" stroke-dasharray="3 4"/>')

def build():
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    xs = [110 + i * 75 for i in range(10)]
    # outcomes: W = wilt, else height of the grower
    plan = [90, "W", 150, 330, "W", 110, "W", 380, 130, "W"]
    for x, p in zip(xs, plan):
        if p == "W":
            wilted(out, x, ground)
        else:
            big = p > 300
            stem(out, x, ground, p, 0.92 if big else 0.62, lean=0.02 if big else -0.01, leaves=5 if big else 3)
        out.append(f'<line x1="{x}" y1="{ground+6}" x2="{x}" y2="{ground+13}" stroke="{GOLD}" stroke-opacity=".45"/>')
    for i, x in enumerate(xs):
        p = plan[i]
        mark = "×" if p == "W" else "✓"
        op = ".35" if p == "W" else ".75"
        out.append(f'<text x="{x}" y="{ground+38}" text-anchor="middle" font-family="Inter" font-size="13" fill="{GOLD}" fill-opacity="{op}">{mark}</text>')
    out.append(f'<text x="450" y="{ground+74}" text-anchor="middle" font-family="Inter" font-size="12" letter-spacing="4" fill="#8a8578">SIX OF TEN</text>')
    # soft glow behind the two big winners
    for x, p in zip(xs, plan):
        if p != "W" and p > 300:
            out.append(f'<circle cx="{x + 0.02*p:.1f}" cy="{ground - p:.1f}" r="34" fill="url(#glow)"/>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".4"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
