"""Lopsided balance: attention piled on return, risk left unweighed. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"

def pan(out, cx, cy, w, alpha):
    out.append(f'<path d="M{cx-w},{cy} Q{cx},{cy+34} {cx+w},{cy}" stroke="{GOLD}" stroke-opacity="{alpha}" '
               f'stroke-width="1.6" fill="none" stroke-linecap="round"/>')
    out.append(f'<line x1="{cx-w}" y1="{cy}" x2="{cx+w}" y2="{cy}" stroke="{GOLD}" stroke-opacity="{alpha*0.6:.2f}" stroke-width="1"/>')

def build():
    out = []
    ground = 430
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    px, py = 450, 120
    # stand
    out.append(f'<path d="M{px-70},{ground} Q{px},{ground-26} {px+70},{ground}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.6" fill="none"/>')
    out.append(f'<line x1="{px}" y1="{ground-13}" x2="{px}" y2="{py}" stroke="{GOLD}" stroke-opacity=".85" stroke-width="2.4"/>')
    out.append(f'<circle cx="{px}" cy="{py}" r="7" fill="none" stroke="{GOLD}" stroke-width="1.6"/>')
    out.append(f'<circle cx="{px}" cy="{py}" r="2.2" fill="{GOLD}"/>')
    # tilted beam: left (return) down, right (risk) up
    tilt = math.radians(14)
    L = 250
    lx, ly = px - L*math.cos(tilt), py + L*math.sin(tilt)
    rx, ry = px + L*math.cos(tilt), py - L*math.sin(tilt)
    out.append(f'<line x1="{lx:.1f}" y1="{ly:.1f}" x2="{rx:.1f}" y2="{ry:.1f}" stroke="{GOLD}" stroke-opacity=".9" stroke-width="2" stroke-linecap="round"/>')
    # ghost of level beam
    out.append(f'<line x1="{px-L}" y1="{py}" x2="{px+L}" y2="{py}" stroke="{GOLD}" stroke-opacity=".18" stroke-width="1" stroke-dasharray="2 7" stroke-linecap="round"/>')
    # hangers + pans
    hang_l, hang_r = 170, 120
    w = 80
    for (hx, hy, drop, alpha) in ((lx, ly, hang_l, .85), (rx, ry, hang_r, .55)):
        out.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="3" fill="{GOLD}" fill-opacity="{alpha}"/>')
        for dx in (-w, w):
            out.append(f'<line x1="{hx:.1f}" y1="{hy:.1f}" x2="{hx+dx:.1f}" y2="{hy+drop:.1f}" stroke="{GOLD}" stroke-opacity="{alpha*0.55:.2f}" stroke-width="0.9"/>')
        pan(out, hx, hy + drop, w, alpha)
    # coins piled on return pan
    cx, base = lx, ly + hang_l - 2
    rows = [5, 4, 4, 3, 2, 1]
    for r, n in enumerate(rows):
        y = base - r*11
        for i in range(n):
            x = cx + (i - (n-1)/2) * 24
            a = 0.95 - r*0.08
            out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="11" ry="4.5" fill="{GOLD}" fill-opacity="{a*0.35:.2f}" '
                       f'stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="1"/>')
    # single faint grain on risk pan: overlooked
    out.append(f'<circle cx="{rx:.1f}" cy="{ry+hang_r+3:.1f}" r="3" fill="none" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # labels
    for x, y, lab in ((lx, ly+hang_l+52, "RETURN"), (rx, ry+hang_r+52, "RISK")):
        out.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="4" fill="#8a8578">{lab}</text>')
    return "".join(out)
