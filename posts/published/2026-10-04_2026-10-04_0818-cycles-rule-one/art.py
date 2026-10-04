"""Market cycles: echoing waves around a horizon, peaks and troughs marked. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"

def wave(x0, x1, mid, amp, period, phase, step=4):
    pts = []
    x = x0
    while x <= x1:
        pts.append(f"{x:.1f},{mid - amp * math.sin(2 * math.pi * (x - x0) / period + phase):.1f}")
        x += step
    return "M" + " L".join(pts)

def build():
    out = []
    mid, x0, x1, period = 270, 60, 840, 260
    out.append(f'<line x1="40" y1="{mid}" x2="860" y2="{mid}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # faint echoes: the same cycle, remembered and forgotten
    for i, (amp, op) in enumerate([(150, .10), (128, .16), (106, .24), (84, .34)]):
        out.append(f'<path d="{wave(x0, x1, mid, amp, period, 0.18 * (4 - i))}" stroke="{GOLD}" '
                   f'stroke-opacity="{op}" stroke-width="1" fill="none"/>')
    main = wave(x0, x1, mid, 120, period, 0)
    out.append(f'<path d="{main}" stroke="{GOLD}" stroke-opacity=".95" stroke-width="2" fill="none" stroke-linecap="round"/>')
    # peaks and troughs
    labels = []
    for k in range(6):
        x = x0 + period * (0.25 + 0.5 * k)
        if x > x1:
            break
        up = k % 2 == 0
        y = mid - 120 if up else mid + 120
        out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{mid}" stroke="{GOLD}" stroke-opacity=".3" '
                   f'stroke-dasharray="2 5" stroke-width="1"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="22" fill="url(#glow)"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{GOLD}"/>')
        ty = y - 22 if up else y + 32
        out.append(f'<text x="{x:.1f}" y="{ty:.1f}" text-anchor="middle" font-family="Inter" font-size="12" '
                   f'letter-spacing="3" fill="#8a8578">{"EUPHORIA" if up else "DESPAIR"}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
