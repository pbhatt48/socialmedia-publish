"""Still water: a single line cast, concentric ripples spreading slowly. Patience over activity. 900x520 viewBox."""
import math

GOLD = "#c9a96a"

def build():
    out = []
    water = 340
    cx = 520
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    # moon and its reflection
    out.append(f'<circle cx="250" cy="120" r="60" fill="url(#glow)"/>')
    out.append(f'<circle cx="250" cy="120" r="22" fill="none" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.2"/>')
    for i, (w, dy) in enumerate([(34, 18), (26, 32), (40, 48), (18, 64), (28, 82), (12, 100)]):
        out.append(f'<line x1="{250-w/2}" y1="{water+dy}" x2="{250+w/2}" y2="{water+dy}" stroke="{GOLD}" '
                   f'stroke-opacity="{0.45 - i*0.06:.2f}" stroke-width="1"/>')
    # horizon / water line
    out.append(f'<line x1="40" y1="{water}" x2="860" y2="{water}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # rod and line from upper right
    out.append(f'<path d="M820,70 Q700,90 610,150" stroke="{GOLD}" stroke-opacity=".8" stroke-width="2" fill="none" stroke-linecap="round"/>')
    out.append(f'<path d="M610,150 Q560,250 {cx},{water-14}" stroke="{GOLD}" stroke-opacity=".5" stroke-width=".8" fill="none"/>')
    # bobber
    out.append(f'<ellipse cx="{cx}" cy="{water-6}" rx="6" ry="9" fill="{GOLD}"/>')
    out.append(f'<line x1="{cx}" y1="{water-15}" x2="{cx}" y2="{water-22}" stroke="{GOLD}" stroke-width="1.2"/>')
    # concentric ripples, slow and wide
    for i in range(1, 8):
        rx = 22 * i ** 1.25
        ry = rx * 0.16
        a = max(0.75 - i * 0.1, 0.08)
        out.append(f'<ellipse cx="{cx}" cy="{water+3}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" stroke="{GOLD}" '
                   f'stroke-opacity="{a:.2f}" stroke-width="{max(1.3 - i*0.12, 0.5):.2f}"/>')
    # time marks along the bottom
    labels = [(160, "DAY"), (360, "YEAR"), (560, "DECADE"), (760, "LIFETIME")]
    for tx, lab in labels:
        out.append(f'<line x1="{tx}" y1="452" x2="{tx}" y2="460" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx}" y="486" text-anchor="middle" font-family="Inter" font-size="12" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    out.append(f'<line x1="160" y1="456" x2="760" y2="456" stroke="{GOLD}" stroke-opacity=".25" stroke-dasharray="2 6"/>')
    return defs + "".join(out)
