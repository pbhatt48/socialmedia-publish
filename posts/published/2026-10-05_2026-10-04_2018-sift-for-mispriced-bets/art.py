"""A sieve over a field of grains: many pass through, one mispriced bet is caught. Returns SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"

def build():
    rnd = random.Random(42)
    out = []
    ground = 440
    cx, sy = 450, 170          # sieve centre / rim height
    rx, ry = 260, 44
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".55"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>'
            f'<clipPath id="mesh"><ellipse cx="{cx}" cy="{sy}" rx="{rx-4}" ry="{ry-3}"/></clipPath></defs>')
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # grains falling from the mesh to the ground
    for _ in range(170):
        x = cx + rnd.uniform(-1, 1) * (rx - 30) * math.sqrt(rnd.random())
        y = rnd.uniform(sy + 30, ground - 8)
        r = rnd.uniform(0.7, 1.6)
        a = 0.15 + 0.5 * (1 - (y - sy) / (ground - sy))
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{GOLD}" fill-opacity="{a:.2f}"/>')
    # settled pile on the ground
    out.append(f'<path d="M{cx-250},{ground} Q{cx},{ground-34} {cx+250},{ground}" stroke="{GOLD}" '
               f'stroke-opacity=".35" stroke-width="1" fill="{GOLD}" fill-opacity=".06"/>')
    for _ in range(140):
        t = rnd.uniform(-1, 1)
        x = cx + t * 240
        top = ground - 17 * (1 - t * t)
        y = rnd.uniform(top, ground - 1)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(.6, 1.3):.2f}" fill="{GOLD}" fill-opacity="{rnd.uniform(.2, .5):.2f}"/>')
    # sieve: back rim, mesh, front rim, depth
    out.append(f'<path d="M{cx-rx},{sy} A{rx},{ry} 0 0 1 {cx+rx},{sy}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.4" fill="none"/>')
    mesh = []
    for i in range(-rx, rx + 1, 14):
        mesh.append(f'<line x1="{cx+i}" y1="{sy-ry}" x2="{cx+i}" y2="{sy+ry}"/>')
    for j in range(-ry, ry + 1, 7):
        mesh.append(f'<line x1="{cx-rx}" y1="{sy+j}" x2="{cx+rx}" y2="{sy+j}"/>')
    out.append(f'<g clip-path="url(#mesh)" stroke="{GOLD}" stroke-opacity=".22" stroke-width=".6">{"".join(mesh)}</g>')
    out.append(f'<path d="M{cx-rx},{sy} A{rx},{ry} 0 0 0 {cx+rx},{sy}" stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.8" fill="none"/>')
    out.append(f'<path d="M{cx-rx},{sy} L{cx-rx},{sy-26} M{cx+rx},{sy} L{cx+rx},{sy-26}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1.2"/>')
    out.append(f'<path d="M{cx-rx},{sy-26} A{rx},{ry} 0 0 0 {cx+rx},{sy-26}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1.2" fill="none"/>')
    out.append(f'<path d="M{cx-rx},{sy-26} A{rx},{ry} 0 0 1 {cx+rx},{sy-26}" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1" fill="none"/>')
    # a few grains still on the mesh, and the one find
    for _ in range(24):
        x = cx + rnd.uniform(-200, 200); y = sy + rnd.uniform(-22, 22)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(.8, 1.4):.2f}" fill="{GOLD}" fill-opacity=".45"/>')
    nx, ny = cx + 62, sy + 6
    out.append(f'<circle cx="{nx}" cy="{ny}" r="34" fill="url(#glow)"/>')
    out.append(f'<path d="M{nx-9},{ny+2} L{nx-4},{ny-7} L{nx+6},{ny-8} L{nx+10},{ny} L{nx+4},{ny+7} L{nx-5},{ny+6} Z" fill="{GOLD}"/>')
    out.append(f'<line x1="{nx}" y1="{ny-16}" x2="{nx}" y2="{ny-84}" stroke="{GOLD}" stroke-opacity=".5" stroke-width=".8"/>')
    out.append(f'<text x="{nx}" y="{ny-94}" text-anchor="middle" font-family="Inter" font-size="13" '
               f'letter-spacing="3" fill="#8a8578">MISPRICED</text>')
    return defs + "".join(out)
