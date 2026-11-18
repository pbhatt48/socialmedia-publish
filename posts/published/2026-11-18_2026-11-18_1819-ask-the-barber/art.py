"""Barber pole and open shears: advice shaped by the adviser's incentive. SVG inner markup, 900x520 viewBox."""
import math

GOLD = "#c9a96a"


def build():
    out = []
    ground = 430
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # Barber pole (center-left)
    cx, top, bot, r = 320, 110, 390, 34
    out.append(f'<circle cx="{cx}" cy="{top-20}" r="20" fill="none" stroke="{GOLD}" stroke-opacity=".85" stroke-width="1.4"/>')
    out.append(f'<circle cx="{cx}" cy="{top-20}" r="44" fill="url(#glow)"/>')
    out.append(f'<rect x="{cx-r-8}" y="{top-2}" width="{2*r+16}" height="10" rx="3" fill="none" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.2"/>')
    out.append(f'<rect x="{cx-r-8}" y="{bot-8}" width="{2*r+16}" height="10" rx="3" fill="none" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.2"/>')
    out.append(f'<line x1="{cx}" y1="{bot+2}" x2="{cx}" y2="{ground}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="2"/>')
    out.append(f'<line x1="{cx-26}" y1="{ground}" x2="{cx+26}" y2="{ground}" stroke="{GOLD}" stroke-opacity=".9" stroke-width="2.4"/>')
    out.append(f'<path d="M{cx-r},{top+8} L{cx-r},{bot-8} M{cx+r},{top+8} L{cx+r},{bot-8}" stroke="{GOLD}" stroke-opacity=".85" stroke-width="1.3"/>')
    # helical stripes, front visible portion
    out.append(f'<clipPath id="pole"><rect x="{cx-r}" y="{top+8}" width="{2*r}" height="{bot-top-16}"/></clipPath>')
    stripes = []
    pitch = 56
    for k in range(-3, 9):
        y0 = top + 8 + k * pitch
        pts = []
        for i in range(0, 41):
            t = i / 40
            x = cx - r + 2 * r * t
            y = y0 + pitch * 0.9 * (0.5 - 0.5 * math.cos(math.pi * t))
            pts.append(f"{x:.1f},{y:.1f}")
        op = 0.75 if k % 2 == 0 else 0.3
        stripes.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{GOLD}" stroke-opacity="{op}" stroke-width="{2.2 if k % 2 == 0 else 1}"/>')
    out.append(f'<g clip-path="url(#pole)">{"".join(stripes)}</g>')

    # Open shears (right), poised
    sx, sy = 540, 250
    def blade(ang, op):
        a = math.radians(ang)
        tipx, tipy = sx + 150 * math.cos(a), sy - 150 * math.sin(a)
        nx, ny = -math.sin(a), -math.cos(a)
        return (f'<path d="M{sx:.1f},{sy:.1f} Q{sx+75*math.cos(a)+9*nx:.1f},{sy-75*math.sin(a)+9*ny:.1f} {tipx:.1f},{tipy:.1f} '
                f'Q{sx+70*math.cos(a)-3*nx:.1f},{sy-70*math.sin(a)-3*ny:.1f} {sx:.1f},{sy:.1f}Z" fill="{GOLD}" fill-opacity="{op*0.18:.2f}" '
                f'stroke="{GOLD}" stroke-opacity="{op}" stroke-width="1.3" stroke-linejoin="round"/>')
    def handle(ang, op):
        a = math.radians(ang)
        hx, hy = sx - 62 * math.cos(a), sy + 62 * math.sin(a)
        return (f'<line x1="{sx}" y1="{sy}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="{GOLD}" stroke-opacity="{op}" stroke-width="2"/>'
                f'<ellipse cx="{hx - 14*math.cos(a):.1f}" cy="{hy + 14*math.sin(a):.1f}" rx="17" ry="12" '
                f'transform="rotate({-ang:.1f} {hx - 14*math.cos(a):.1f} {hy + 14*math.sin(a):.1f})" fill="none" stroke="{GOLD}" stroke-opacity="{op}" stroke-width="1.6"/>')
    out.append(blade(30, 0.9) + blade(-2, 0.7))
    out.append(handle(30, 0.75) + handle(-2, 0.6))
    out.append(f'<circle cx="{sx}" cy="{sy}" r="4" fill="{GOLD}"/>')
    out.append(f'<circle cx="{sx}" cy="{sy}" r="30" fill="url(#glow)"/>')

    # dotted arc linking shears to pole: the adviser's motion
    out.append(f'<path d="M510,320 C470,380 410,390 370,360" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1.2" '
               f'stroke-dasharray="2 7" fill="none" stroke-linecap="round"/>')
    # small labels
    for tx, lab in [(cx, "ADVICE"), (sx + 40, "INCENTIVE")]:
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
        out.append(f'<line x1="{tx}" y1="{ground+6}" x2="{tx}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')

    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
