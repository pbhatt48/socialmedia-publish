"""Gut feelings vs. discipline: a restless, panicky emotional trace swings
above and below a calm, straight measured course that ends at a compass.
Returns SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"
MUTED = "#8a8578"

def build():
    out = []
    rnd = random.Random(42)
    ground = 420
    course_y = 250
    x0, x1 = 70, 740

    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # Emotional trace: several faint layered swings (fear / euphoria), amplitude
    # rising and falling like market mood.
    for layer, (alpha, width, seed) in enumerate([(0.16, 0.8, 3), (0.24, 0.9, 9), (0.38, 1.1, 17)]):
        r = random.Random(seed)
        pts = []
        x = x0
        while x <= x1:
            env = 0.35 + 0.65 * abs(math.sin((x - x0) / 210 + layer))
            y = course_y + math.sin(x / 23 + layer * 1.7) * 70 * env + r.uniform(-28, 28) * env
            pts.append((x, y))
            x += r.uniform(9, 16)
        d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
        out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity="{alpha}" stroke-width="{width}" '
                   f'fill="none" stroke-linejoin="round" stroke-linecap="round"/>')

    # Fear / greed bands
    for yy, lab in ((course_y - 118, "GREED"), (course_y + 128, "FEAR")):
        out.append(f'<line x1="{x0}" y1="{yy}" x2="{x1}" y2="{yy}" stroke="{GOLD}" stroke-opacity=".14" '
                   f'stroke-width="1" stroke-dasharray="2 6"/>')
        out.append(f'<text x="{x0}" y="{yy - 8}" font-family="Inter" font-size="11" letter-spacing="3" fill="{MUTED}">{lab}</text>')

    # The disciplined course: straight, measured, steady.
    out.append(f'<line x1="{x0}" y1="{course_y}" x2="{x1}" y2="{course_y}" stroke="{GOLD}" stroke-opacity=".95" stroke-width="2.2" stroke-linecap="round"/>')
    for i, tx in enumerate(range(x0, x1 + 1, 30)):
        h = 9 if i % 5 == 0 else 4
        out.append(f'<line x1="{tx}" y1="{course_y - h}" x2="{tx}" y2="{course_y + h}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1"/>')
    out.append(f'<circle cx="{x0}" cy="{course_y}" r="4" fill="{GOLD}"/>')

    # Compass at the end of the course.
    cx, cy, R = 790, course_y, 46
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{R + 22}" fill="url(#glow)"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.3" fill="none"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{R - 8}" stroke="{GOLD}" stroke-opacity=".3" stroke-width="0.8" fill="none"/>')
    for k in range(32):
        a = k * math.pi / 16
        r1 = R - (7 if k % 8 == 0 else 3.5)
        out.append(f'<line x1="{cx + R * math.cos(a):.1f}" y1="{cy + R * math.sin(a):.1f}" x2="{cx + r1 * math.cos(a):.1f}" '
                   f'y2="{cy + r1 * math.sin(a):.1f}" stroke="{GOLD}" stroke-opacity=".6" stroke-width="0.8"/>')
    # Needle pointing along the course (east).
    out.append(f'<path d="M{cx - 30},{cy} L{cx},{cy - 6} L{cx + 34},{cy} L{cx},{cy + 6} Z" fill="{GOLD}" fill-opacity=".2" stroke="{GOLD}" stroke-width="1"/>')
    out.append(f'<path d="M{cx},{cy - 6} L{cx + 34},{cy} L{cx},{cy + 6} Z" fill="{GOLD}" fill-opacity=".9"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="2.6" fill="#0d0d0d" stroke="{GOLD}" stroke-width="1"/>')

    # Labels
    out.append(f'<text x="{x0}" y="{ground + 40}" font-family="Inter" font-size="13" letter-spacing="3" fill="{MUTED}">GUT FEELING</text>')
    out.append(f'<text x="{cx}" y="{ground + 40}" text-anchor="middle" font-family="Inter" font-size="13" letter-spacing="3" fill="{MUTED}">DISCIPLINE</text>')
    out.append(f'<line x1="{cx}" y1="{cy + R + 10}" x2="{cx}" y2="{ground - 6}" stroke="{GOLD}" stroke-opacity=".25" stroke-dasharray="2 5"/>')

    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".22"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
