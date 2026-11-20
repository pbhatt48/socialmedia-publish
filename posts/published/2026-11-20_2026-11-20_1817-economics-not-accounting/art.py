"""Two coin stacks: $1 of reported earnings inside the ledger's frame, $2 of real
earnings outside it. Economics, not accounting. SVG inner markup for 900x520."""

GOLD = "#c9a96a"

def coin(out, cx, y, rx, ry, h, alpha):
    # side band then top ellipse
    out.append(f'<path d="M{cx-rx},{y} L{cx-rx},{y+h} A{rx},{ry} 0 0 0 {cx+rx},{y+h} L{cx+rx},{y}" '
               f'stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="1.1" fill="#0f0e0c" fill-opacity="1"/>')
    out.append(f'<ellipse cx="{cx}" cy="{y}" rx="{rx}" ry="{ry}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" '
               f'stroke-width="1.1" fill="#0f0e0c"/>')

def stack(out, cx, ground, n, alpha, rx=54, ry=13, h=14):
    for i in range(n):
        y = ground - ry - h - i * h
        coin(out, cx, y, rx, ry, h, alpha * (0.55 + 0.45 * (i + 1) / n))
    top = ground - ry - h - (n - 1) * h
    out.append(f'<ellipse cx="{cx}" cy="{top}" rx="{rx*0.62:.1f}" ry="{ry*0.62:.1f}" stroke="{GOLD}" '
               f'stroke-opacity="{alpha*0.5:.2f}" stroke-width=".8" fill="none"/>')
    return top

def build():
    out = []
    ground = 400
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    lx, rx_ = 300, 600
    t1 = stack(out, lx, ground, 8, 0.9)
    t2 = stack(out, rx_, ground, 16, 0.9)
    # ledger frame: a neat ruled rectangle around only the reported stack
    fx0, fx1, fy0 = lx - 92, lx + 92, t1 - 46
    out.append(f'<rect x="{fx0}" y="{fy0}" width="{fx1-fx0}" height="{ground-fy0}" stroke="{GOLD}" '
               f'stroke-opacity=".38" stroke-width="1" fill="none" stroke-dasharray="3 6"/>')
    for k in range(1, 4):
        yy = fy0 + k * 12
        out.append(f'<line x1="{fx0+10}" y1="{yy}" x2="{fx0+44}" y2="{yy}" stroke="{GOLD}" stroke-opacity=".25" stroke-width=".8"/>')
    # soft glow behind the real stack
    out.append(f'<ellipse cx="{rx_}" cy="{(t2+ground)/2:.0f}" rx="150" ry="170" fill="url(#glow)"/>')
    # value arc rising from the small to the large stack
    out.insert(1, f'<path d="M{lx},{t1-70} C{lx+90},{t1-150} {rx_-120},{t2-70} {rx_},{t2-40}" stroke="{GOLD}" '
                  f'stroke-opacity=".3" stroke-width="1.1" stroke-dasharray="2 7" fill="none" stroke-linecap="round"/>')
    for tx, lab in ((lx, "REPORTED  $1"), (rx_, "ECONOMIC  $2")):
        out.append(f'<line x1="{tx}" y1="{ground+6}" x2="{tx}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx}" y="{ground+42}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".16"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    # glow must sit behind coins: move it to the front of the list
    glow = [s for s in out if 'url(#glow)' in s]
    rest = [s for s in out if 'url(#glow)' not in s]
    return defs + "".join(glow + rest)
