"""Classical corporate facade whose columns are equal partners' shares: a pediment holding a circle of equal wedges. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"

def build():
    out = []
    ground = 430
    cx = 450
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # stepped base
    for i, (w, h) in enumerate([(520, 0), (490, 12), (460, 24)]):
        y = ground - h
        out.append(f'<rect x="{cx-w/2}" y="{y-12}" width="{w}" height="12" fill="none" stroke="{GOLD}" '
                   f'stroke-opacity="{.55-.08*i:.2f}" stroke-width="1"/>')
    top_base = ground - 36
    # columns
    n = 8
    span = 400
    col_top = 210
    for i in range(n):
        x = cx - span / 2 + span * i / (n - 1)
        a = .55 + .3 * (1 - abs(i - (n - 1) / 2) / ((n - 1) / 2))
        out.append(f'<rect x="{x-11}" y="{top_base-8}" width="22" height="8" fill="none" stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="1"/>')
        out.append(f'<rect x="{x-11}" y="{col_top}" width="22" height="8" fill="none" stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="1"/>')
        for f in (-5, 0, 5):
            out.append(f'<line x1="{x+f}" y1="{col_top+8}" x2="{x+f}" y2="{top_base-8}" stroke="{GOLD}" '
                       f'stroke-opacity="{a*(1 if f == 0 else .55):.2f}" stroke-width="{1.2 if f == 0 else .8}"/>')
    # entablature
    out.append(f'<rect x="{cx-235}" y="{col_top-22}" width="470" height="22" fill="none" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1"/>')
    out.append(f'<line x1="{cx-235}" y1="{col_top-11}" x2="{cx+235}" y2="{col_top-11}" stroke="{GOLD}" stroke-opacity=".3" stroke-width=".8"/>')
    # pediment
    py = col_top - 22
    peak = 70
    out.append(f'<path d="M{cx-250},{py} L{cx},{peak} L{cx+250},{py} Z" fill="none" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.3" stroke-linejoin="round"/>')
    out.append(f'<path d="M{cx-222},{py-8} L{cx},{peak+14} L{cx+222},{py-8} Z" fill="none" stroke="{GOLD}" stroke-opacity=".3" stroke-width=".8"/>')
    # circle of equal shares in the pediment
    r = 34
    ccy = py - 44
    out.append(f'<circle cx="{cx}" cy="{ccy}" r="{r+16}" fill="url(#glow)"/>')
    out.append(f'<circle cx="{cx}" cy="{ccy}" r="{r}" fill="none" stroke="{GOLD}" stroke-width="1.4"/>')
    for k in range(n):
        ang = -math.pi / 2 + 2 * math.pi * k / n
        out.append(f'<line x1="{cx}" y1="{ccy}" x2="{cx + r*math.cos(ang):.1f}" y2="{ccy + r*math.sin(ang):.1f}" '
                   f'stroke="{GOLD}" stroke-opacity=".7" stroke-width="1"/>')
    out.append(f'<circle cx="{cx}" cy="{ccy}" r="3" fill="{GOLD}"/>')
    # faint threads from each wedge down to each column: every column is an owner
    for i in range(n):
        x = cx - span / 2 + span * i / (n - 1)
        ang = -math.pi / 2 + 2 * math.pi * (i + .5) / n
        out.append(f'<path d="M{cx + r*.6*math.cos(ang):.1f},{ccy + r*.6*math.sin(ang):.1f} Q{(cx+x)/2:.1f},{ccy+60} {x:.1f},{col_top-24}" '
                   f'stroke="{GOLD}" stroke-opacity=".14" stroke-width=".8" stroke-dasharray="2 5" fill="none"/>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
