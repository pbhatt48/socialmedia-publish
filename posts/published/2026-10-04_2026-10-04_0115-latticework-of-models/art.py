"""Isolated facts (scattered points, left) gathering into a latticework of models (right). SVG inner markup for 900x520."""
import math, random

GOLD = "#c9a96a"

def build():
    rnd = random.Random(42)
    out = []
    ground = 430
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    # Left: isolated facts, unconnected, drifting low
    for _ in range(22):
        x = rnd.uniform(70, 300)
        y = rnd.uniform(250, ground - 20)
        r = rnd.uniform(1.6, 3.2)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{GOLD}" fill-opacity="{rnd.uniform(.25,.6):.2f}"/>')
    # Right: lattice of nodes (diamond trellis) rising from the ground
    cx0, dy = 610, 50
    counts = [7, 6, 5, 4, 3, 2]
    nodes = {}
    for r, n in enumerate(counts):
        dx = 46
        for c in range(n):
            x = cx0 + (c - (n - 1) / 2) * dx
            y = ground - 40 - r * dy
            nodes[(r, c)] = (x + rnd.uniform(-2, 2), y + rnd.uniform(-2, 2))
    edges = set()
    for (r, c), (x, y) in nodes.items():
        nb = [(r, c + 1), (r + 1, c), (r + 1, c - 1)]
        for k in nb:
            if k in nodes:
                edges.add(((r, c), k))
    for a, b in sorted(edges):
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        op = 0.28 + 0.5 * rnd.random()
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity="{op:.2f}" stroke-width="1.1" stroke-linecap="round"/>')
    # Posts anchoring the lattice into the ground
    base = [p for (r, c), p in nodes.items() if r == 0]
    for x, y in base:
        out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{ground}" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1"/>')
    for (x, y) in nodes.values():
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="{GOLD}" fill-opacity=".9"/>')
    top = (cx0, ground - 40 - (len(counts) - 1) * dy)
    out.append(f'<circle cx="{top[0]:.1f}" cy="{top[1]:.1f}" r="34" fill="url(#glow)"/>')
    # Dashed drift of facts toward the lattice
    out.insert(1, f'<path d="M300,340 C380,330 440,310 480,280" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1.2" '
                  f'stroke-dasharray="2 7" fill="none" stroke-linecap="round"/>')
    for tx, lab in [(185, "FACTS"), (610, "MODELS")]:
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    return defs + "".join(out)
