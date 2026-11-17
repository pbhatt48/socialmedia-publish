"""Outcome fan: from one decision point, paths spread out. Downside paths meet a firm floor; upside is left to take care of itself."""
import math, random

GOLD = "#c9a96a"

def build():
    rnd = random.Random(42)
    out = []
    ox, oy = 150, 250          # decision point
    floor = 400                # protected floor
    ground_y = 440
    # horizon / ground
    out.append(f'<line x1="40" y1="{ground_y}" x2="860" y2="{ground_y}" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1"/>')
    # floor (margin of safety)
    out.append(f'<line x1="{ox}" y1="{floor}" x2="820" y2="{floor}" stroke="{GOLD}" stroke-opacity=".85" stroke-width="2.2"/>')
    for x in range(ox + 10, 821, 22):
        out.append(f'<line x1="{x}" y1="{floor+3}" x2="{x-10}" y2="{floor+15}" stroke="{GOLD}" stroke-opacity=".28" stroke-width="1"/>')
    # fan of outcome paths
    n = 15
    for i in range(n):
        t = i / (n - 1)
        end_y = 60 + t * 440          # 60 (best) .. 500 (worst, would go below floor)
        alpha = 0.18 + 0.5 * (1 - abs(t - 0.5) * 1.4)
        pts = []
        steps = 40
        for s in range(steps + 1):
            u = s / steps
            x = ox + u * 650
            y = oy + (end_y - oy) * (u ** 1.15) + rnd.uniform(-5, 5) * math.sin(u * math.pi)
            if y > floor - 1:
                y = floor - 1
            pts.append((x, y))
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        w = 1.0 if end_y < floor else 1.3
        out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity="{max(alpha,0.15):.2f}" stroke-width="{w}" fill="none" stroke-linejoin="round"/>')
    # decision point
    out.append(f'<circle cx="{ox}" cy="{oy}" r="30" fill="url(#glow)"/>')
    out.append(f'<circle cx="{ox}" cy="{oy}" r="5" fill="{GOLD}"/>')
    # downward glance arrow
    out.append(f'<line x1="{ox}" y1="{oy+18}" x2="{ox}" y2="{floor-12}" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.2" stroke-dasharray="2 5" stroke-linecap="round"/>')
    out.append(f'<path d="M{ox-5},{floor-18} L{ox},{floor-9} L{ox+5},{floor-18}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.2" fill="none"/>')
    # labels
    lab = 'font-family="Inter" font-size="13" letter-spacing="3" fill="#8a8578"'
    out.append(f'<text x="{ox}" y="{oy-28}" text-anchor="middle" {lab}>DECISION</text>')
    out.append(f'<text x="820" y="{floor+38}" text-anchor="end" {lab}>THE FLOOR</text>')
    out.append(f'<text x="820" y="50" text-anchor="end" {lab}>UPSIDE TAKES CARE OF ITSELF</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
