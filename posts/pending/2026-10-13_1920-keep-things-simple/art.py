"""Many steady base hits versus one long swing at the fence: simplicity over heroics. SVG inner markup for a 900x520 viewBox."""
GOLD = "#c9a96a"

def arc(x1, x2, h, ground, op, w, dash=""):
    cx = (x1 + x2) / 2
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="M{x1},{ground} Q{cx},{ground - 2*h} {x2},{ground}" stroke="{GOLD}" '
            f'stroke-opacity="{op:.2f}" stroke-width="{w}" fill="none" stroke-linecap="round"{d}/>')

def build():
    out = []
    ground = 400
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    hx = 110
    # home plate
    out.append(f'<path d="M{hx-9},{ground-1} L{hx+9},{ground-1} L{hx+9},{ground-7} L{hx},{ground-13} L{hx-9},{ground-7} Z" '
               f'fill="{GOLD}" fill-opacity=".85"/>')
    out.append(f'<circle cx="{hx}" cy="{ground-6}" r="30" fill="url(#glow)"/>')
    # steady singles: short, low, solid arcs landing in a tight band
    for i, (x2, h, op) in enumerate([(300, 38, .9), (330, 46, .75), (355, 34, .8), (385, 52, .65),
                                     (410, 40, .7), (440, 58, .55), (465, 44, .5)]):
        out.append(arc(hx + 6, x2, h, ground - 4, op, 1.4))
        out.append(f'<circle cx="{x2}" cy="{ground-4}" r="2.6" fill="{GOLD}" fill-opacity="{op:.2f}"/>')
    # the long swing: tall faint dashed arc that dies at the wall
    fx = 760
    out.append(f'<path d="M{hx+6},{ground-4} Q{(hx+fx)/2 + 20},{ground-430} {fx-14},{ground-150}" stroke="{GOLD}" '
               f'stroke-opacity=".32" stroke-width="1.2" fill="none" stroke-dasharray="2 7" stroke-linecap="round"/>')
    out.append(f'<circle cx="{fx-14}" cy="{ground-150}" r="3" fill="none" stroke="{GOLD}" stroke-opacity=".45"/>')
    # outfield fence
    fh = 120
    out.append(f'<line x1="{fx}" y1="{ground}" x2="{fx}" y2="{ground-fh}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.6"/>')
    for k in range(0, fh + 1, 12):
        out.append(f'<line x1="{fx}" y1="{ground-k}" x2="{fx+22}" y2="{ground-k}" stroke="{GOLD}" stroke-opacity=".22" stroke-width="1"/>')
    out.append(f'<line x1="{fx+22}" y1="{ground}" x2="{fx+22}" y2="{ground-fh}" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1"/>')
    # labels
    for tx, lab in [(hx, "HOME"), (382, "BASE HITS"), (fx + 11, "THE FENCE")]:
        out.append(f'<line x1="{tx}" y1="{ground+6}" x2="{tx}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
