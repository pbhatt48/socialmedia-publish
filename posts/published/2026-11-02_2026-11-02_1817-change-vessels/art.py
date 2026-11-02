"""Two hulls on one waterline: a leaking boat sinking amid patches, and a sound vessel riding high."""
import math

GOLD = "#c9a96a"
W = 360  # waterline

def hull(x, y, w, h, tilt, alpha):
    """Hull centered at x with deck at y; tilt in degrees."""
    p = (f'M{x-w/2:.1f},{y:.1f} L{x+w/2:.1f},{y:.1f} '
         f'C{x+w/2-8:.1f},{y+h*0.7:.1f} {x+w*0.3:.1f},{y+h:.1f} {x+w*0.18:.1f},{y+h:.1f} '
         f'L{x-w*0.18:.1f},{y+h:.1f} C{x-w*0.3:.1f},{y+h:.1f} {x-w/2+8:.1f},{y+h*0.7:.1f} {x-w/2:.1f},{y:.1f} Z')
    return (f'<g transform="rotate({tilt} {x} {y+h/2})">'
            f'<path d="{p}" fill="#121315" fill-opacity=".92" stroke="{GOLD}" stroke-opacity="{alpha}" stroke-width="1.6" stroke-linejoin="round"/>')

def build():
    o = []
    defs = (f'<defs><linearGradient id="sea" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{GOLD}" stop-opacity=".10"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient></defs>')
    o.append(f'<rect x="20" y="{W}" width="860" height="110" fill="url(#sea)"/>')
    o.append(f'<line x1="20" y1="{W}" x2="880" y2="{W}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1"/>')
    for i, yy in enumerate((W + 22, W + 46, W + 74)):
        for k in range(6):
            sx = 60 + k * 140 + i * 40
            o.append(f'<path d="M{sx},{yy} q12,-5 24,0 t24,0" stroke="{GOLD}" stroke-opacity="{.28 - i*.07:.2f}" stroke-width="1" fill="none"/>')

    # --- leaking boat (left), low in the water and listing
    lx, ly = 250, W - 14
    o.append(hull(lx, ly, 240, 62, 7, .55))
    # patches on the hull
    for px, py, r in ((-60, 18, 0), (-10, 30, 18), (40, 22, -12), (75, 10, 8)):
        o.append(f'<rect x="{lx+px-9}" y="{ly+py-6}" width="18" height="12" transform="rotate({r} {lx+px} {ly+py})" '
                 f'fill="none" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>'
                 f'<path d="M{lx+px-6},{ly+py} h12" stroke="{GOLD}" stroke-opacity=".35" stroke-width=".8"/>')
    # stubby broken mast + slack sail
    o.append(f'<line x1="{lx-10}" y1="{ly}" x2="{lx-4}" y2="{ly-120}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1.6"/>')
    o.append(f'<path d="M{lx-4},{ly-114} Q{lx+30},{ly-70} {lx+22},{ly-8}" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1.1" fill="none"/>')
    o.append('</g>')
    # bailing splashes / drips
    for i, (dx, dy) in enumerate(((-120, -40), (-138, -10), (-100, -62), (110, -30), (128, -54))):
        o.append(f'<path d="M{lx+dx},{ly+dy} q-3,6 0,9 q3,-3 0,-9Z" fill="{GOLD}" fill-opacity="{.25 + .08*(i%3):.2f}"/>')
    # small bucket
    o.append(f'<path d="M{lx-84},{ly-30} l4,16 h12 l4,-16 Z" fill="none" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1"/>')

    # --- sound vessel (right), riding high and level
    rx, ry = 650, W - 40
    o.append(hull(rx, ry, 260, 58, 0, .95))
    o.append(f'<line x1="{rx-115}" y1="{ry+12}" x2="{rx+115}" y2="{ry+12}" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1"/>')
    o.append('</g>')
    o.append(f'<line x1="{rx}" y1="{ry}" x2="{rx}" y2="{ry-230}" stroke="{GOLD}" stroke-opacity=".9" stroke-width="2"/>')
    o.append(f'<path d="M{rx+4},{ry-222} Q{rx+92},{ry-120} {rx+104},{ry-14} L{rx+4},{ry-14} Z" fill="{GOLD}" fill-opacity=".14" stroke="{GOLD}" stroke-opacity=".85" stroke-width="1.3"/>')
    o.append(f'<path d="M{rx-4},{ry-200} Q{rx-60},{ry-110} {rx-82},{ry-14} L{rx-4},{ry-14} Z" fill="{GOLD}" fill-opacity=".07" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.1"/>')
    o.append(f'<path d="M{rx},{ry-230} l18,6 l-18,6" fill="{GOLD}" fill-opacity=".7"/>')
    # wake
    o.append(f'<path d="M{rx-150},{W+8} q-40,4 -80,14" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1" fill="none"/>')

    # dashed transfer arc
    o.append(f'<path d="M{lx+40},{ly-150} C{lx+150},{ly-215} {rx-170},{ry-205} {rx-70},{ry-150}" stroke="{GOLD}" stroke-opacity=".45" '
             f'stroke-width="1.2" stroke-dasharray="2 7" stroke-linecap="round" fill="none"/>')
    o.append(f'<path d="M{rx-70},{ry-150} l-12,-2 m12,2 l-6,-10" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.2" fill="none" stroke-linecap="round"/>')

    for tx, lab in ((lx, "PATCHING LEAKS"), (rx, "CHANGING VESSELS")):
        o.append(f'<text x="{tx}" y="{W+130}" text-anchor="middle" font-family="Inter" font-size="13" letter-spacing="3" fill="#8a8578">{lab}</text>')
    return defs + "".join(o)
