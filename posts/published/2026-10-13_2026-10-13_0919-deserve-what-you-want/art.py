"""Balanced scale: what you deliver to the world on one pan, what you get on the other. 900x520 viewBox."""
import math

GOLD = "#c9a96a"

def pan(out, cx, top):
    # three suspension cords from the beam tip down to a shallow dish
    for dx in (-62, 0, 62):
        out.append(f'<line x1="{cx}" y1="{top}" x2="{cx+dx}" y2="{top+200}" stroke="{GOLD}" stroke-opacity="{.35 if dx else .55}" stroke-width="1"/>')
    y = top + 200
    out.append(f'<path d="M{cx-78},{y} Q{cx},{y+34} {cx+78},{y}" stroke="{GOLD}" stroke-width="1.8" fill="none"/>')
    out.append(f'<line x1="{cx-78}" y1="{y}" x2="{cx+78}" y2="{y}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1"/>')
    return y

def coins(out, cx, base, n):
    for i in range(n):
        y = base - 6 - i * 9
        out.append(f'<ellipse cx="{cx}" cy="{y}" rx="26" ry="5.5" fill="#14130f" stroke="{GOLD}" stroke-opacity="{.5+.5*i/n:.2f}" stroke-width="1.2"/>')

def seedling(out, cx, base):
    # a small mound of earth with a sprouting plant: value created, still growing
    out.append(f'<path d="M{cx-34},{base-2} Q{cx},{base-22} {cx+34},{base-2}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.3" fill="none"/>')
    out.append(f'<path d="M{cx},{base-12} C{cx-2},{base-40} {cx+3},{base-62} {cx},{base-84}" stroke="{GOLD}" stroke-width="1.6" fill="none"/>')
    out.append(f'<path d="M{cx},{base-52} q-26,-4 -32,-24 q22,2 32,24Z" fill="{GOLD}" fill-opacity=".75"/>')
    out.append(f'<path d="M{cx},{base-70} q24,-10 34,-28 q-24,2 -34,28Z" fill="{GOLD}" fill-opacity=".9"/>')

def build():
    out = []
    ground = 440
    cx = 450
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # base and pillar
    out.append(f'<path d="M{cx-70},{ground} L{cx-40},{ground-18} L{cx+40},{ground-18} L{cx+70},{ground} Z" fill="none" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.4"/>')
    out.append(f'<line x1="{cx}" y1="{ground-18}" x2="{cx}" y2="80" stroke="{GOLD}" stroke-width="2.4"/>')
    out.append(f'<line x1="{cx-5}" y1="{ground-18}" x2="{cx-5}" y2="90" stroke="{GOLD}" stroke-opacity=".25" stroke-width="1"/>')
    # fulcrum and level beam
    out.append(f'<path d="M{cx-12},84 L{cx},62 L{cx+12},84 Z" fill="{GOLD}"/>')
    out.append(f'<circle cx="{cx}" cy="62" r="34" fill="url(#glow)"/>')
    L = 230
    out.append(f'<line x1="{cx-L}" y1="80" x2="{cx+L}" y2="80" stroke="{GOLD}" stroke-width="2.2" stroke-linecap="round"/>')
    for s in (-1, 1):
        out.append(f'<circle cx="{cx+s*L}" cy="80" r="4" fill="{GOLD}"/>')
    # level indicator
    out.append(f'<line x1="{cx}" y1="96" x2="{cx}" y2="118" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1"/>')
    left = pan(out, cx - L, 80)
    right = pan(out, cx + L, 80)
    seedling(out, cx - L, left)
    coins(out, cx + L, right, 6)
    for tx, lab in ((cx - L, "DESERVE"), (cx + L, "GET")):
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="4" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
