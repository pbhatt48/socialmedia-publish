"""Balance scale: a fine gem weighed against the price paid. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"

def line(x1, y1, x2, y2, w=1.2, a=0.9):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GOLD}" '
            f'stroke-opacity="{a:.2f}" stroke-width="{w}" stroke-linecap="round"/>')

def pan(cx, cy):
    out = [line(cx, cy - 110, cx - 70, cy, 0.9, 0.5), line(cx, cy - 110, cx + 70, cy, 0.9, 0.5)]
    out.append(f'<path d="M{cx-78},{cy} Q{cx},{cy+34} {cx+78},{cy}" stroke="{GOLD}" stroke-width="1.6" '
               f'stroke-opacity=".9" fill="{GOLD}" fill-opacity=".06"/>')
    out.append(line(cx - 78, cy, cx + 78, cy, 1.0, 0.6))
    out.append(f'<circle cx="{cx}" cy="{cy-110}" r="3" fill="{GOLD}"/>')
    return out

def gem(cx, base):
    w, h1, h2 = 46, 22, 46
    top, gir = base - h2 - h1, base - h2
    pts = [(cx - w * 0.55, top), (cx + w * 0.55, top), (cx + w, gir), (cx, base), (cx - w, gir)]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    out = [f'<path d="{d}" stroke="{GOLD}" stroke-width="1.5" fill="{GOLD}" fill-opacity=".08" stroke-linejoin="round"/>']
    out.append(line(cx - w, gir, cx + w, gir, 1.0, 0.8))
    for fx in (-0.55, 0, 0.55):
        out.append(line(cx + w * fx * 0.5, gir, cx, base, 0.7, 0.45))
    for a, b in ((-0.55, -0.25), (-0.25, 0.25), (0.25, 0.55)):
        out.append(line(cx + w * a, top, cx + w * (a + b) / 2 * 1.4, gir, 0.7, 0.4))

    return out

def coins(cx, base, n):
    out = []
    for i in range(n):
        y = base - 7 - i * 11
        out.append(f'<ellipse cx="{cx}" cy="{y}" rx="34" ry="7" stroke="{GOLD}" stroke-width="1.2" '
                   f'stroke-opacity="{0.95 - i*0.06:.2f}" fill="#0f0f10" fill-opacity=".9"/>')
    return out

def build():
    out = []
    ground = 440
    out.append(line(40, ground, 860, ground, 1, 0.45))
    px, py = 450, 130
    out.append(f'<path d="M{px-46},{ground} L{px-14},{ground-18} L{px+14},{ground-18} L{px+46},{ground} Z" '
               f'stroke="{GOLD}" stroke-width="1.3" fill="{GOLD}" fill-opacity=".1"/>')
    out.append(line(px, ground - 18, px, py, 2.6, 0.9))
    tilt = math.radians(-9)  # right side (price) heavier
    L = 220
    lx, ly = px - L * math.cos(tilt), py + L * math.sin(tilt)
    rx, ry = px + L * math.cos(tilt), py - L * math.sin(tilt)
    out.append(line(lx, ly, rx, ry, 2.2, 0.95))
    out.append(f'<path d="M{px-12},{py-2} L{px},{py-26} L{px+12},{py-2} Z" fill="{GOLD}" fill-opacity=".85"/>')
    out.append(f'<circle cx="{px}" cy="{py}" r="5" fill="#0f0f10" stroke="{GOLD}" stroke-width="1.5"/>')
    out.append(line(px, py + 10, px, py + 40, 1, 0.5))
    lpy, rpy = ly + 110, ry + 110
    out += pan(lx, lpy)
    out += pan(rx, rpy)
    out += gem(lx, lpy + 6)
    out += coins(rx, rpy + 6, 9)
    for tx, ty, lab in ((lx, lpy + 62, "WHAT YOU BUY"), (rx, rpy + 62, "WHAT YOU PAY")):
        out.append(f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    return "".join(out)
