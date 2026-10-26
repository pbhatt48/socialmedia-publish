"""Prospector's sieve: sift a world of pebbles, occasionally find one nugget. Returns SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"

def build():
    rnd = random.Random(1994)
    out = []
    ground = 450
    cx, cy, rx, ry = 450, 190, 250, 54
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".55"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>'
            f'<clipPath id="pan"><ellipse cx="{cx}" cy="{cy}" rx="{rx-4}" ry="{ry-3}"/></clipPath></defs>')
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # the world: a broad scatter of ordinary pebbles on the ground
    for _ in range(260):
        x = rnd.gauss(450, 150)
        if not 70 < x < 830:
            continue
        spread = max(0.0, 1 - abs(x - 450) / 400)
        y = ground - 3 - rnd.random() * 26 * spread ** 1.5
        r = rnd.uniform(1.6, 4.2)
        out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r:.1f}" ry="{r*0.72:.1f}" fill="none" stroke="{GOLD}" '
                   f'stroke-opacity="{rnd.uniform(.18,.45):.2f}" stroke-width=".8"/>')
    # grains falling through the mesh
    for _ in range(120):
        x = cx + rnd.uniform(-0.82, 0.82) * rx
        y = rnd.uniform(cy + 30, ground - 30)
        a = 0.45 * (1 - (y - cy) / (ground - cy)) + 0.06
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(.7,1.5):.1f}" fill="{GOLD}" fill-opacity="{a:.2f}"/>')
    # pan rim, depth, and fine mesh
    out.append(f'<path d="M{cx-rx},{cy} Q{cx},{cy+ry*2.6} {cx+rx},{cy}" fill="none" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.6"/>')
    mesh = []
    for i in range(-25, 26):
        x = cx + i * 10
        mesh.append(f'<line x1="{x}" y1="{cy-ry}" x2="{x}" y2="{cy+ry}"/>')
    for j in range(-7, 8):
        y = cy + j * 8
        mesh.append(f'<line x1="{cx-rx}" y1="{y}" x2="{cx+rx}" y2="{y}"/>')
    out.append(f'<g clip-path="url(#pan)" stroke="{GOLD}" stroke-opacity=".22" stroke-width=".6">{"".join(mesh)}</g>')
    out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{GOLD}" stroke-opacity=".9" stroke-width="2"/>')
    out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx-9}" ry="{ry-5}" fill="none" stroke="{GOLD}" stroke-opacity=".35" stroke-width=".8"/>')
    # handles
    for s in (-1, 1):
        hx = cx + s * rx
        out.append(f'<path d="M{hx},{cy-4} q{s*22},-6 {s*34},-2 q{s*6},4 0,8 q{-s*14},2 {-s*34},2" fill="none" '
                   f'stroke="{GOLD}" stroke-opacity=".75" stroke-width="1.4" stroke-linecap="round"/>')
    # gravel left in the pan
    for _ in range(26):
        a = rnd.uniform(0, 2 * math.pi)
        d = rnd.uniform(.25, .85)
        x, y = cx + math.cos(a) * d * (rx - 30), cy + math.sin(a) * d * (ry - 12)
        if abs(x - 476) < 28 and abs(y - cy) < 14:
            continue
        r = rnd.uniform(1.8, 3.4)
        out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r:.1f}" ry="{r*.7:.1f}" fill="none" stroke="{GOLD}" stroke-opacity=".38" stroke-width=".8"/>')
    # the one nugget
    nx, ny = 476, cy + 2
    out.append(f'<circle cx="{nx}" cy="{ny}" r="44" fill="url(#glow)"/>')
    out.append(f'<path d="M{nx-9},{ny+3} L{nx-6},{ny-5} L{nx+2},{ny-8} L{nx+9},{ny-3} L{nx+8},{ny+4} L{nx},{ny+7} Z" fill="{GOLD}"/>')
    for a in range(0, 360, 45):
        r1, r2 = 15, 24 if a % 90 == 0 else 20
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        out.append(f'<line x1="{nx+ca*r1:.1f}" y1="{ny+sa*r1*.8:.1f}" x2="{nx+ca*r2:.1f}" y2="{ny+sa*r2*.8:.1f}" '
                   f'stroke="{GOLD}" stroke-opacity=".55" stroke-width=".9" stroke-linecap="round"/>')
    return defs + "".join(out)
