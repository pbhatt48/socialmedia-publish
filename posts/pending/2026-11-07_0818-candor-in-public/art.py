"""Candor: a lamp before an arched mirror. The lamp's rays are true; the reflection is the
one image a manager can't escape. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"

def build():
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # Arched mirror (right)
    mx, mw, top = 590, 190, 90
    l, r = mx - mw / 2, mx + mw / 2
    def arch(x0, x1, y0, yb):
        rad = (x1 - x0) / 2
        return f'M{x0},{yb} L{x0},{y0 + rad} A{rad},{rad} 0 0 1 {x1},{y0 + rad} L{x1},{yb}'
    out.append(f'<path d="{arch(l-10, r+10, top-10, ground-18)} Z" fill="none" stroke="{GOLD}" stroke-opacity=".85" stroke-width="2"/>')
    out.append(f'<path d="{arch(l, r, top, ground-26)} Z" fill="{GOLD}" fill-opacity=".04" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # stand feet
    for fx in (l + 10, r - 10):
        out.append(f'<line x1="{fx}" y1="{ground-18}" x2="{fx + (-14 if fx < mx else 14)}" y2="{ground}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.6"/>')
    # glass sheen
    for i, (a, b) in enumerate([(30, 150), (55, 120)]):
        out.append(f'<line x1="{l+a}" y1="{top+80+i*30}" x2="{l+b}" y2="{top+150+i*30}" stroke="{GOLD}" stroke-opacity="{.18 - i*.06:.2f}" stroke-width="1"/>')

    # Lamp (left): candle on a holder
    cx, cb = 250, ground
    out.append(f'<ellipse cx="{cx}" cy="{cb-3}" rx="34" ry="5" fill="none" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.4"/>')
    out.append(f'<rect x="{cx-11}" y="{cb-96}" width="22" height="90" rx="2" fill="{GOLD}" fill-opacity=".8"/>')
    out.append(f'<line x1="{cx}" y1="{cb-96}" x2="{cx}" y2="{cb-104}" stroke="{GOLD}" stroke-width="1.4"/>')
    fy = cb - 120
    out.append(f'<circle cx="{cx}" cy="{fy}" r="70" fill="url(#glow)"/>')
    out.append(f'<path d="M{cx},{fy-22} C{cx+10},{fy-6} {cx+9},{fy+10} {cx},{fy+14} C{cx-9},{fy+10} {cx-10},{fy-6} {cx},{fy-22} Z" fill="{GOLD}"/>')

    # Rays from the flame toward the mirror, and their reflections back
    for k in range(-3, 4):
        ty = 250 + k * 34
        out.append(f'<line x1="{cx+18}" y1="{fy + k*3}" x2="{l-4}" y2="{ty}" stroke="{GOLD}" stroke-opacity="{.5 - abs(k)*.1:.2f}" '
                   f'stroke-width=".9" stroke-dasharray="2 6" stroke-linecap="round"/>')
    # short ambient rays elsewhere
    for a in range(0, 360, 30):
        if -60 < ((a + 180) % 360) - 180 < 60:
            continue
        rad = math.radians(a)
        x1, y1 = cx + 30 * math.cos(rad), fy - 30 * math.sin(rad)
        x2, y2 = cx + 52 * math.cos(rad), fy - 52 * math.sin(rad)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1" stroke-linecap="round"/>')

    # Reflection inside mirror: the same candle, faint
    rx_ = mx - 30
    out.append(f'<rect x="{rx_-7}" y="{ground-26-62}" width="14" height="58" rx="2" fill="{GOLD}" fill-opacity=".28"/>')
    rfy = ground - 26 - 78
    out.append(f'<circle cx="{rx_}" cy="{rfy}" r="38" fill="url(#glow)" opacity=".6"/>')
    out.append(f'<path d="M{rx_},{rfy-14} C{rx_+6},{rfy-4} {rx_+6},{rfy+6} {rx_},{rfy+9} C{rx_-6},{rfy+6} {rx_-6},{rfy-4} {rx_},{rfy-14} Z" fill="{GOLD}" fill-opacity=".55"/>')

    labels = [(cx, "IN PUBLIC"), (mx, "IN PRIVATE")]
    for tx, lab in labels:
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
