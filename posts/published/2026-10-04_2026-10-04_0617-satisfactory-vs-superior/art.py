"""Two summits: a broad, gentle hill (satisfactory) and a steep, narrow peak (superior). Returns SVG inner markup for a 900x520 viewBox."""
import random

GOLD = "#c9a96a"

def build():
    out = []
    ground = 420
    rnd = random.Random(5)
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # broad gentle hill with contour echoes
    for i, a in enumerate((0.85, 0.4, 0.22, 0.12)):
        h = 150 - i * 30
        w = 190 - i * 28
        out.append(f'<path d="M{280-w},{ground} C{280-w*0.45},{ground} {280-w*0.5},{ground-h} 280,{ground-h} '
                   f'C{280+w*0.5},{ground-h} {280+w*0.45},{ground} {280+w},{ground}" stroke="{GOLD}" stroke-opacity="{a}" '
                   f'stroke-width="{1.6 if i == 0 else 1}" fill="none"/>')
    # easy switchback path up the hill
    out.append(f'<path d="M140,{ground} C200,{ground-8} 230,{ground-60} 280,{ground-150}" stroke="{GOLD}" stroke-opacity=".5" '
               f'stroke-width="1.2" stroke-dasharray="2 6" fill="none" stroke-linecap="round"/>')
    out.append(f'<circle cx="280" cy="{ground-150}" r="3.5" fill="{GOLD}"/>')
    # steep jagged peak
    pts = [(520, ground), (560, 380), (580, 390), (612, 300), (628, 312), (652, 210), (664, 222), (690, 70),
           (712, 180), (726, 168), (752, 290), (770, 280), (800, 370), (820, 362), (850, ground)]
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.6" fill="none" stroke-linejoin="round"/>')
    # rock hatching on the peak's shadow side
    for _ in range(26):
        y = rnd.uniform(110, 400)
        t = (y - 70) / (ground - 70)
        xr = 690 + t * 160
        x0 = 690 + t * 20
        x = rnd.uniform(x0 + 8, xr - 10)
        out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x+7:.1f}" y2="{y+11:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity="{rnd.uniform(0.12, 0.3):.2f}" stroke-width=".8"/>')
    # narrow climbing route
    out.append(f'<path d="M560,{ground} L600,350 L585,330 L640,260 L622,240 L668,160 L690,70" stroke="{GOLD}" stroke-opacity=".5" '
               f'stroke-width="1.1" stroke-dasharray="2 5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    out.append(f'<circle cx="690" cy="70" r="3.5" fill="{GOLD}"/><circle cx="690" cy="70" r="22" fill="url(#glow)"/>')
    for tx, lab in ((280, "SATISFACTORY"), (690, "SUPERIOR")):
        out.append(f'<line x1="{tx}" y1="{ground+6}" x2="{tx}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
