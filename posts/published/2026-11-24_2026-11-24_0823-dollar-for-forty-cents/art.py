"""A balance scale: 40 cents outweighs nothing; a dollar sits light on the high side. Price vs value."""
import math

GOLD = "#c9a96a"

def build():
    out = []
    ground = 430
    out.append(f'<line x1="70" y1="{ground}" x2="830" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    cx, top = 450, 120
    # base and post
    out.append(f'<path d="M{cx-70},{ground} Q{cx},{ground-26} {cx+70},{ground}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.4" fill="none"/>')
    out.append(f'<line x1="{cx}" y1="{ground-14}" x2="{cx}" y2="{top}" stroke="{GOLD}" stroke-opacity=".85" stroke-width="2.2"/>')
    out.append(f'<path d="M{cx-9},{top+4} L{cx},{top-12} L{cx+9},{top+4} Z" fill="{GOLD}" fill-opacity=".9"/>')
    # beam tilted: left (value, $1) heavy -> down; right (price, 40c) up
    ang = math.radians(-9)  # left side lower
    L = 230
    lx, ly = cx - L*math.cos(ang), top - L*math.sin(ang) * -1
    lx, ly = cx - L*math.cos(ang), top + L*math.sin(-ang)
    rx, ry = cx + L*math.cos(ang), top - L*math.sin(-ang)
    out.append(f'<line x1="{lx:.1f}" y1="{ly:.1f}" x2="{rx:.1f}" y2="{ry:.1f}" stroke="{GOLD}" stroke-width="2" stroke-linecap="round"/>')
    out.append(f'<circle cx="{cx}" cy="{top}" r="5" fill="#0f0e0c" stroke="{GOLD}" stroke-width="1.6"/>')
    def pan(px, py, drop):
        by = py + drop
        out.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{px-62:.1f}" y2="{by:.1f}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1"/>')
        out.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{px+62:.1f}" y2="{by:.1f}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1"/>')
        out.append(f'<path d="M{px-70:.1f},{by:.1f} Q{px:.1f},{by+30:.1f} {px+70:.1f},{by:.1f} Z" stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.4" fill="{GOLD}" fill-opacity=".06"/>')
        out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3" fill="{GOLD}"/>')
        return by
    drop = 150
    lb = pan(lx, ly, drop)
    rb = pan(rx, ry, drop)
    # dollar bill on left pan (value)
    bw, bh = 104, 46
    bx, byy = lx - bw/2, lb - bh - 2
    out.append(f'<rect x="{bx:.1f}" y="{byy:.1f}" width="{bw}" height="{bh}" rx="3" stroke="{GOLD}" stroke-width="1.3" fill="{GOLD}" fill-opacity=".08"/>')
    out.append(f'<rect x="{bx+5:.1f}" y="{byy+5:.1f}" width="{bw-10}" height="{bh-10}" rx="2" stroke="{GOLD}" stroke-opacity=".4" stroke-width=".8" fill="none"/>')
    out.append(f'<ellipse cx="{lx:.1f}" cy="{byy+bh/2:.1f}" rx="13" ry="15" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1" fill="none"/>')
    out.append(f'<text x="{lx:.1f}" y="{byy+bh/2+5:.1f}" text-anchor="middle" font-family="Inter" font-size="14" fill="{GOLD}">1</text>')
    # 40c on right pan: four small coins stacked
    for i in range(4):
        cy = rb - 6 - i*7
        out.append(f'<ellipse cx="{rx:.1f}" cy="{cy:.1f}" rx="22" ry="5.5" stroke="{GOLD}" stroke-opacity="{0.55+0.1*i:.2f}" stroke-width="1.1" fill="#0f0e0c"/>')
    # labels
    for x, lab in ((lx, "VALUE  $1.00"), (rx, "PRICE  $0.40")):
        out.append(f'<text x="{x:.1f}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" letter-spacing="3" fill="#8a8578">{lab}</text>')
        out.append(f'<line x1="{x:.1f}" y1="{ground+6}" x2="{x:.1f}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
    # faint margin-of-safety bracket
    out.append(f'<path d="M{rx+96:.1f},{lb-20:.1f} L{rx+104:.1f},{lb-20:.1f} L{rx+104:.1f},{rb-30:.1f} L{rx+96:.1f},{rb-30:.1f}" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1" fill="none"/>')
    return "".join(out)
