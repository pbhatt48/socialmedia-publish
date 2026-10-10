"""A steep summit reached by a long switchback trail; a flat 'easy' path runs off to nowhere. Returns SVG inner markup for a 900x520 viewBox."""
import random

GOLD = "#c9a96a"

def build():
    rnd = random.Random(5)
    out = []
    ground = 420
    out.append(f'<line x1="30" y1="{ground}" x2="870" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # background ridge
    out.append(f'<path d="M230,{ground} L330,250 L360,290 L430,190 L470,215 L520,170" stroke="{GOLD}" stroke-opacity=".22" '
               f'stroke-width="1" fill="none" stroke-linejoin="round"/>')
    out.append(f'<path d="M640,150 L700,230 L760,200 L860,{ground}" stroke="{GOLD}" stroke-opacity=".22" stroke-width="1" fill="none" stroke-linejoin="round"/>')
    # main peak
    peak = (560, 70)
    left = [(380, ground), (440, 350), (470, 310), (500, 220), (525, 165), peak]
    right = [peak, (600, 120), (640, 170), (690, 240), (740, 300), (820, ground)]
    pts = left + right[1:]
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.8" fill="none" stroke-linejoin="round"/>')
    # hatching on shadow face
    for i in range(1, 26):
        t = i / 26
        y = peak[1] + t * (ground - peak[1])
        # right edge x at y (piecewise interp)
        def edge(pp, yy):
            for (x1, y1), (x2, y2) in zip(pp, pp[1:]):
                lo, hi = min(y1, y2), max(y1, y2)
                if lo <= yy <= hi and y1 != y2:
                    return x1 + (yy - y1) * (x2 - x1) / (y2 - y1)
            return None
        xr = edge(right, y)
        if xr is None:
            continue
        L = min(14 + t * 60, (ground - y) / .35)
        out.append(f'<line x1="{xr-4:.1f}" y1="{y:.1f}" x2="{xr-4-L*rnd.uniform(.7,1):.1f}" y2="{y+L*.35:.1f}" '
                   f'stroke="{GOLD}" stroke-opacity="{.10+.14*t:.2f}" stroke-width=".8"/>')
    # switchback trail to the summit
    trail = [(400, ground), (640, 400), (430, 375), (660, 345), (460, 320), (650, 285), (495, 250), (620, 210),
             (530, 170), (585, 125), (560, 88)]
    td = "M" + " L".join(f"{x},{y}" for x, y in trail)
    out.append(f'<path d="{td}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.2" stroke-dasharray="2 6" '
               f'fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    # summit flag + glow
    out.append(f'<circle cx="{peak[0]}" cy="{peak[1]}" r="34" fill="url(#glow)"/>')
    out.append(f'<line x1="{peak[0]}" y1="{peak[1]}" x2="{peak[0]}" y2="{peak[1]-34}" stroke="{GOLD}" stroke-width="1.4"/>'
               f'<path d="M{peak[0]},{peak[1]-34} L{peak[0]+22},{peak[1]-27} L{peak[0]},{peak[1]-20} Z" fill="{GOLD}" fill-opacity=".85"/>')
    # the easy path: flat, fading away along the ground to the left
    for i in range(18):
        x = 365 - i * 14
        out.append(f'<circle cx="{x}" cy="{ground-6}" r="1.4" fill="{GOLD}" fill-opacity="{max(.05,.6-i*.032):.2f}"/>')
    out.append(f'<circle cx="400" cy="{ground}" r="3" fill="{GOLD}"/>')
    for tx, lab in [(190, "EASY"), (400, "START"), (560, "SUPERIOR")]:
        y = ground + 40 if lab != "SUPERIOR" else ground + 40
        out.append(f'<text x="{tx}" y="{y}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
