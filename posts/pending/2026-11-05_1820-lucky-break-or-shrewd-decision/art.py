"""A lifetime of small, steady journeyman bars beside one towering bar: the single decision that outweighs them all."""
import random

GOLD = "#c9a96a"
MUTED = "#8a8578"


def build():
    rnd = random.Random(1948)
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # journeyman efforts: many small bars
    x = 70
    xs = []
    while x < 560:
        h = rnd.uniform(14, 40)
        a = rnd.uniform(0.35, 0.8)
        out.append(f'<rect x="{x:.1f}" y="{ground-h:.1f}" width="7" height="{h:.1f}" fill="{GOLD}" fill-opacity="{a*0.35:.2f}" '
                   f'stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="0.8"/>')
        xs.append((x, h))
        x += 16
    # their summed height, stacked faintly on the right of the row
    total = sum(h for _, h in xs)
    # the one decision: a tall bar
    bx, top = 700, 70
    out.append(f'<rect x="{bx-11}" y="{top}" width="22" height="{ground-top}" fill="{GOLD}" fill-opacity=".22" '
               f'stroke="{GOLD}" stroke-opacity=".95" stroke-width="1.2"/>')
    out.append(f'<circle cx="{bx}" cy="{top}" r="40" fill="url(#glow)"/>')
    out.append(f'<circle cx="{bx}" cy="{top}" r="3" fill="{GOLD}"/>')
    # fine guide rays from the top
    for dx in (-60, -34, 34, 60):
        out.append(f'<line x1="{bx+dx*0.35:.1f}" y1="{top-abs(dx)*0.12:.1f}" x2="{bx+dx:.1f}" y2="{top-abs(dx)*0.45:.1f}" '
                   f'stroke="{GOLD}" stroke-opacity=".35" stroke-width="0.8" stroke-linecap="round"/>')
    # dashed level of the tallest small bar, carried across to compare
    mh = max(h for _, h in xs)
    out.append(f'<line x1="70" y1="{ground-mh:.1f}" x2="{bx-18}" y2="{ground-mh:.1f}" stroke="{GOLD}" stroke-opacity=".25" '
               f'stroke-width="0.8" stroke-dasharray="2 6"/>')
    # brackets + labels
    out.append(f'<path d="M70,{ground+12} v6 H{xs[-1][0]+7:.1f} v-6" stroke="{GOLD}" stroke-opacity=".5" fill="none" stroke-width="0.8"/>')
    mid = (70 + xs[-1][0] + 7) / 2
    out.append(f'<text x="{mid:.1f}" y="{ground+46}" text-anchor="middle" font-family="Inter" font-size="13" letter-spacing="3" fill="{MUTED}">A LIFETIME OF JOURNEYMAN EFFORTS</text>')
    out.append(f'<line x1="{bx}" y1="{ground+8}" x2="{bx}" y2="{ground+18}" stroke="{GOLD}" stroke-opacity=".5"/>')
    out.append(f'<text x="{bx}" y="{ground+46}" text-anchor="middle" font-family="Inter" font-size="13" letter-spacing="3" fill="{MUTED}">ONE DECISION</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
