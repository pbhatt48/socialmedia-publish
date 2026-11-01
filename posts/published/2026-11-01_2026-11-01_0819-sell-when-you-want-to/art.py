"""A sailboat riding at anchor on calm water: no forced departure. SVG inner markup for 900x520."""
import math

GOLD = "#c9a96a"

def build():
    o = []
    water = 330
    o.append(f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/>'
             f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    # low sun on the horizon, right
    sx = 690
    o.append(f'<circle cx="{sx}" cy="{water}" r="90" fill="url(#glow)"/>')
    o.append(f'<path d="M{sx-46},{water} A46,46 0 0 1 {sx+46},{water}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.3" fill="none"/>')
    for i in range(9):
        a = math.pi * (i + 1) / 10
        x1, y1 = sx + 58 * math.cos(a), water - 58 * math.sin(a)
        x2, y2 = sx + 74 * math.cos(a), water - 74 * math.sin(a)
        o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1"/>')
    # horizon
    o.append(f'<line x1="30" y1="{water}" x2="870" y2="{water}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # calm ripples
    for k, (y, op) in enumerate([(348, .30), (366, .22), (386, .15), (408, .10)]):
        for j in range(5 - k // 2):
            x = 90 + j * 170 + (k % 2) * 80
            w = 60 - k * 8
            o.append(f'<path d="M{x},{y} q{w/4},-3 {w/2},0 t{w/2},0" stroke="{GOLD}" stroke-opacity="{op}" stroke-width="1" fill="none"/>')
    # sun reflection
    for i, y in enumerate(range(342, 420, 12)):
        w = 40 - i * 5
        o.append(f'<line x1="{sx-w}" y1="{y}" x2="{sx+w}" y2="{y}" stroke="{GOLD}" stroke-opacity="{.4 - i*.05:.2f}" stroke-width="1"/>')
    # boat
    bx = 330
    hull = water - 2
    o.append(f'<path d="M{bx-80},{hull-22} L{bx+90},{hull-22} Q{bx+70},{hull+6} {bx+40},{hull+6} L{bx-50},{hull+6} Q{bx-72},{hull} {bx-80},{hull-22} Z" '
             f'fill="{GOLD}" fill-opacity=".14" stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.6" stroke-linejoin="round"/>')
    mast_top = hull - 230
    o.append(f'<line x1="{bx}" y1="{hull-22}" x2="{bx}" y2="{mast_top}" stroke="{GOLD}" stroke-width="2"/>')
    # furled main along boom, jib lowered: sails gently furled, at rest
    o.append(f'<line x1="{bx}" y1="{hull-50}" x2="{bx+80}" y2="{hull-46}" stroke="{GOLD}" stroke-opacity=".9" stroke-width="2"/>')
    o.append(f'<path d="M{bx+4},{hull-55} q38,-6 74,2" stroke="{GOLD}" stroke-opacity=".6" stroke-width="5" stroke-linecap="round" fill="none"/>')
    # stays
    o.append(f'<line x1="{bx}" y1="{mast_top}" x2="{bx-78}" y2="{hull-22}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    o.append(f'<line x1="{bx}" y1="{mast_top}" x2="{bx+86}" y2="{hull-22}" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1"/>')
    o.append(f'<path d="M{bx},{mast_top} l18,6 l-18,6 Z" fill="{GOLD}" fill-opacity=".7"/>')
    # reflection of boat
    o.append(f'<path d="M{bx-50},{hull+10} L{bx+40},{hull+10}" stroke="{GOLD}" stroke-opacity=".25" stroke-width="1"/>')
    o.append(f'<line x1="{bx}" y1="{hull+14}" x2="{bx}" y2="{hull+80}" stroke="{GOLD}" stroke-opacity=".12" stroke-width="2" stroke-dasharray="6 6"/>')
    # anchor rode from bow down to anchor
    ax, ay = bx - 170, 470
    o.append(f'<path d="M{bx-74},{hull-18} C{bx-110},{hull+40} {ax+30},{ay-60} {ax},{ay-24}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.2" stroke-dasharray="3 4" fill="none"/>')
    # anchor
    o.append(f'<circle cx="{ax}" cy="{ay-30}" r="5" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.4" fill="none"/>')
    o.append(f'<line x1="{ax}" y1="{ay-25}" x2="{ax}" y2="{ay+8}" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.6"/>')
    o.append(f'<line x1="{ax-11}" y1="{ay-16}" x2="{ax+11}" y2="{ay-16}" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.4"/>')
    o.append(f'<path d="M{ax-18},{ay-6} Q{ax-14},{ay+10} {ax},{ay+10} Q{ax+14},{ay+10} {ax+18},{ay-6}" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.6" fill="none"/>')
    # seabed
    o.append(f'<path d="M60,{ay+14} Q300,{ay+6} 480,{ay+14} T840,{ay+12}" stroke="{GOLD}" stroke-opacity=".2" stroke-width="1" fill="none"/>')
    return "".join(o)
