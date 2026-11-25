"""A brilliant oarsman's boat straining upstream against a strong current: good management vs poor business economics."""
import math, random

GOLD = "#c9a96a"

def build():
    rnd = random.Random(1980)
    out = []
    bank = 150
    # far bank / horizon
    out.append(f'<line x1="40" y1="{bank}" x2="860" y2="{bank}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # current lines flowing right -> left
    for i in range(15):
        y = bank + 28 + i * 21 + rnd.uniform(-4, 4)
        x1 = rnd.uniform(60, 220)
        x2 = rnd.uniform(680, 840)
        amp = rnd.uniform(3, 7)
        alpha = 0.12 + 0.32 * (1 - abs(i - 7) / 8)
        mid = (x1 + x2) / 2
        out.append(f'<path d="M{x2:.1f},{y:.1f} C{mid+120:.1f},{y-amp:.1f} {mid-120:.1f},{y+amp:.1f} {x1:.1f},{y:.1f}" '
                   f'stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="{rnd.uniform(0.7,1.4):.2f}" fill="none" stroke-linecap="round"/>')
        if i % 3 == 1:
            ax = x1 + 8
            out.append(f'<path d="M{ax+10:.1f},{y-5:.1f} L{ax:.1f},{y:.1f} L{ax+10:.1f},{y+5:.1f}" stroke="{GOLD}" '
                       f'stroke-opacity="{alpha:.2f}" stroke-width="1" fill="none" stroke-linecap="round"/>')
    # boat, heading right (upstream)
    bx, by = 0, 0
    out.append('<g transform="translate(430 335) scale(1.55)">')
    out.append(f'<path d="M{bx-70},{by-6} Q{bx-60},{by+16} {bx-10},{by+18} L{bx+50},{by+18} Q{bx+82},{by+12} {bx+96},{by-8} Z" '
               f'fill="#0f0f10" stroke="{GOLD}" stroke-width="1.6"/>')
    out.append(f'<line x1="{bx-66}" y1="{by-2}" x2="{bx+92}" y2="{by-4}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1"/>')
    # oars
    for dx, ang in ((-10, 0.0), (20, 0.0)):
        ox = bx + dx
        out.append(f'<line x1="{ox}" y1="{by-6}" x2="{ox-48}" y2="{by+44}" stroke="{GOLD}" stroke-width="1.4" stroke-linecap="round"/>')
        out.append(f'<ellipse cx="{ox-50}" cy="{by+47}" rx="4" ry="9" transform="rotate(-44 {ox-50} {by+47})" fill="{GOLD}" fill-opacity=".8"/>')
    # wake/splash behind boat (small, showing effort)
    for k in range(4):
        r = 10 + k * 9
        out.append(f'<path d="M{bx-74-k*6},{by+4-r*0.5:.1f} q-{r*0.5:.1f},{r*0.5:.1f} 0,{r:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity="{0.55-k*0.12:.2f}" stroke-width="1" fill="none"/>')
    out.append('</g>')
    # brilliance: starburst above the boat
    sx, sy = 448, 238
    out.append(f'<circle cx="{sx}" cy="{sy}" r="44" fill="url(#glow)"/>')
    for j in range(16):
        a = j * math.pi / 8
        ln = 26 if j % 2 == 0 else 14
        out.append(f'<line x1="{sx+7*math.cos(a):.1f}" y1="{sy+7*math.sin(a):.1f}" x2="{sx+ln*math.cos(a):.1f}" '
                   f'y2="{sy+ln*math.sin(a):.1f}" stroke="{GOLD}" stroke-opacity="{0.9 if j%2==0 else 0.5}" stroke-width="1.1" stroke-linecap="round"/>')
    out.append(f'<circle cx="{sx}" cy="{sy}" r="4" fill="{GOLD}"/>')
    # labels
    out.append(f'<text x="{sx}" y="{sy-46}" text-anchor="middle" font-family="Inter" font-size="12" letter-spacing="3" fill="#8a8578">BRILLIANCE</text>')
    out.append(f'<text x="450" y="500" text-anchor="middle" font-family="Inter" font-size="12" letter-spacing="3" fill="#8a8578">← ECONOMICS</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".4"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
