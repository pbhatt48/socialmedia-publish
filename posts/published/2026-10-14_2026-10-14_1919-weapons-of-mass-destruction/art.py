"""A dense web of interlinked counterparties above a calm horizon, with a latent
fault spreading unseen beneath the ground. Returns SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"

def build():
    rnd = random.Random(2002)
    out = []
    ground = 400
    cx, cy = 450, 215
    nodes = []
    for ring, (r, n) in enumerate([(0, 1), (62, 7), (122, 12), (178, 16)]):
        for i in range(n):
            a = 2 * math.pi * i / n + ring * 0.37 + rnd.uniform(-0.12, 0.12)
            rr = r + rnd.uniform(-10, 10) if r else 0
            nodes.append((cx + rr * math.cos(a) * 1.55, cy + rr * math.sin(a) * 0.92, ring))
    # links: every node tied to several others, near and far
    for i, (x1, y1, r1) in enumerate(nodes):
        others = sorted(range(len(nodes)), key=lambda j: (nodes[j][0]-x1)**2 + (nodes[j][1]-y1)**2)
        picks = others[1:4] + rnd.sample(others[4:], 2)
        for j in picks:
            if j < i:
                continue
            x2, y2, _ = nodes[j]
            d = math.hypot(x2 - x1, y2 - y1)
            op = max(0.10, 0.55 - d / 700)
            out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GOLD}" '
                       f'stroke-opacity="{op:.2f}" stroke-width=".8"/>')
    for x, y, ring in nodes:
        rad = [7, 4.2, 3.2, 2.4][ring]
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" fill="{GOLD}" fill-opacity="{0.95 - ring*0.15:.2f}"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="16" fill="none" stroke="{GOLD}" stroke-opacity=".5" stroke-width=".8"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="28" fill="none" stroke="{GOLD}" stroke-opacity=".22" stroke-width=".8" stroke-dasharray="2 5"/>')
    # horizon
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # latent fault beneath the surface
    def crack(x, y, ang, length, depth, op):
        if depth == 0 or length < 4:
            return
        pts = [(x, y)]
        for _ in range(4):
            x += length / 4 * math.cos(ang) + rnd.uniform(-4, 4)
            y += length / 4 * math.sin(ang) + rnd.uniform(-1.5, 1.5)
            y = min(max(y, ground + 3), 490)
            pts.append((x, y))
        d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
        out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity="{op:.2f}" stroke-width=".9" fill="none" '
                   f'stroke-dasharray="3 4" stroke-linecap="round"/>')
        crack(x, y, ang + rnd.uniform(-0.5, 0.5), length * 0.7, depth - 1, op * 0.85)
        if rnd.random() < 0.6:
            crack(x, y, ang + rnd.choice([-1, 1]) * rnd.uniform(0.4, 0.8), length * 0.55, depth - 1, op * 0.75)
    for ang in (0.12, math.pi - 0.12, 0.55, math.pi - 0.55):
        crack(cx, ground + 4, ang, 120, 4, 0.42)
    out.append(f'<text x="{cx}" y="505" text-anchor="middle" font-family="Inter" font-size="12" '
               f'letter-spacing="4" fill="#8a8578">LATENT</text>')
    return "".join(out)
