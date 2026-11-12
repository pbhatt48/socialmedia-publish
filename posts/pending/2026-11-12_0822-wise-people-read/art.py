"""A tall stack of books with an open book on top, radiating fine lines: wisdom built from constant reading."""
import random

GOLD = "#c9a96a"


def build():
    rnd = random.Random(3)
    out = []
    ground = 430
    out.append(f'<line x1="70" y1="{ground}" x2="830" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    cx = 450
    # stack of books, slightly offset
    y = ground
    n = 11
    for i in range(n):
        h = rnd.uniform(14, 22)
        w = rnd.uniform(170, 230) - i * 4
        off = rnd.uniform(-14, 14)
        x = cx - w / 2 + off
        y -= h
        a = 0.35 + 0.55 * (i / (n - 1))
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="2" fill="none" '
                   f'stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="1.3"/>')
        # page edge lines on the right side
        for k in range(1, 3):
            yy = y + h * k / 3
            out.append(f'<line x1="{x + w - 26:.1f}" y1="{yy:.1f}" x2="{x + w - 4:.1f}" y2="{yy:.1f}" '
                       f'stroke="{GOLD}" stroke-opacity="{a * 0.45:.2f}" stroke-width=".7"/>')
        # spine band
        out.append(f'<line x1="{x + 16:.1f}" y1="{y + 3:.1f}" x2="{x + 16:.1f}" y2="{y + h - 3:.1f}" '
                   f'stroke="{GOLD}" stroke-opacity="{a * 0.6:.2f}" stroke-width=".9"/>')
    top = y
    # open book on top
    out.append(f'<circle cx="{cx}" cy="{top - 40}" r="150" fill="url(#glow)"/>')
    for s in (-1, 1):
        out.append(f'<path d="M{cx},{top - 4} C{cx + s * 40},{top - 26} {cx + s * 90},{top - 22} {cx + s * 120},{top - 10} '
                   f'L{cx + s * 120},{top - 4} C{cx + s * 90},{top - 14} {cx + s * 40},{top - 18} {cx},{top + 2} Z" '
                   f'fill="none" stroke="{GOLD}" stroke-opacity=".95" stroke-width="1.4" stroke-linejoin="round"/>')
        for k in range(1, 4):
            out.append(f'<path d="M{cx + s * 4},{top - 6 - k * 1.5} C{cx + s * 40},{top - 24 - k * 3} {cx + s * 88},{top - 22 - k * 3} {cx + s * 116},{top - 12 - k * 2}" '
                       f'fill="none" stroke="{GOLD}" stroke-opacity="{0.5 - k * 0.1:.2f}" stroke-width=".7"/>')
    # rays rising from the open pages
    import math
    for j in range(15):
        ang = math.radians(25 + j * (130 / 14))
        r1, r2 = 60, 60 + rnd.uniform(80, 150)
        x1, y1 = cx + r1 * math.cos(ang), top - 20 - r1 * math.sin(ang) * 0.9
        x2, y2 = cx + r2 * math.cos(ang), top - 20 - r2 * math.sin(ang) * 0.9
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity="{rnd.uniform(.18, .45):.2f}" stroke-width=".8" stroke-linecap="round"/>')
    # a few scattered books leaning / lying nearby, faint
    out.append(f'<rect x="200" y="{ground - 60}" width="20" height="60" rx="2" transform="rotate(-12 210 {ground})" '
               f'fill="none" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1"/>')
    out.append(f'<rect x="226" y="{ground - 54}" width="16" height="54" rx="2" fill="none" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1"/>')
    out.append(f'<rect x="640" y="{ground - 14}" width="90" height="14" rx="2" fill="none" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1"/>')
    out.append(f'<rect x="652" y="{ground - 26}" width="72" height="12" rx="2" fill="none" stroke="{GOLD}" stroke-opacity=".22" stroke-width="1"/>')
    return defs + "".join(out)
