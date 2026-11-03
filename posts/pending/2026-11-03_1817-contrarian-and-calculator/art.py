"""Contrarian streak + calculator: a flock flies one way, one bird turns back toward a measured gap between price and value."""
import math, random

GOLD = "#c9a96a"

def bird(x, y, s, ang, alpha, w=1.1):
    # chevron "bird" pointing in direction ang (radians, 0 = right)
    ca, sa = math.cos(ang), math.sin(ang)
    def p(dx, dy):
        return x + dx * ca - dy * sa, y + dx * sa + dy * ca
    tip = p(s * 0.5, 0)
    l1, l2 = p(-s * 0.5, -s * 0.55), p(-s * 0.15, -s * 0.12)
    r1, r2 = p(-s * 0.5, s * 0.55), p(-s * 0.15, s * 0.12)
    return (f'<path d="M{l1[0]:.1f},{l1[1]:.1f} Q{l2[0]:.1f},{l2[1]:.1f} {tip[0]:.1f},{tip[1]:.1f} '
            f'Q{r2[0]:.1f},{r2[1]:.1f} {r1[0]:.1f},{r1[1]:.1f}" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" '
            f'stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')

def build():
    rnd = random.Random(5)
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # the crowd: a loose flock drifting up and to the right
    for i in range(46):
        t = rnd.random()
        x = 470 + t * 330 + rnd.uniform(-35, 35)
        y = 290 - t * 200 + rnd.uniform(-45, 45)
        s = rnd.uniform(12, 20)
        a = -0.32 + rnd.uniform(-0.12, 0.12)
        alpha = 0.22 + 0.4 * rnd.random()
        out.append(bird(x, y, s, a, alpha))
    # faint crowd current
    out.append(f'<path d="M430,330 C560,260 690,170 830,70" stroke="{GOLD}" stroke-opacity=".18" stroke-width="1" '
               f'stroke-dasharray="2 7" fill="none" stroke-linecap="round"/>')

    # the contrarian: one bird turning back and down, its path dotted toward the measured gap
    out.append(f'<path d="M330,196 C262,214 222,262 224,322" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.2" '
               f'stroke-dasharray="2 6" fill="none" stroke-linecap="round"/>')
    out.append(bird(340, 192, 30, math.pi - 0.12, 0.95, w=1.8))

    # the calculator: value vs price, measured
    vx1, vx2 = 140, 320
    v_y, p_y = 336, 392
    out.append(f'<line x1="{vx1}" y1="{v_y}" x2="{vx2}" y2="{v_y}" stroke="{GOLD}" stroke-opacity=".85" stroke-width="1.3"/>')
    out.append(f'<line x1="{vx1}" y1="{p_y}" x2="{vx2}" y2="{p_y}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1.1" stroke-dasharray="5 4"/>')
    # fine ruler ticks between them
    for k in range(9):
        yy = v_y + (p_y - v_y) * k / 8
        ln = 9 if k % 4 == 0 else 5
        out.append(f'<line x1="{vx2+14}" y1="{yy:.1f}" x2="{vx2+14+ln}" y2="{yy:.1f}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1"/>')
    out.append(f'<line x1="{vx2+14}" y1="{v_y}" x2="{vx2+14}" y2="{p_y}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1"/>')
    # gap shading
    out.append(f'<rect x="{vx1}" y="{v_y}" width="{vx2-vx1}" height="{p_y-v_y}" fill="{GOLD}" fill-opacity=".07"/>')
    for tx, ty, lab in ((vx1, v_y - 10, "VALUE"), (vx1, p_y + 20, "PRICE")):
        out.append(f'<text x="{tx}" y="{ty}" font-family="Inter" font-size="12" letter-spacing="3" fill="#8a8578">{lab}</text>')
    out.append(f'<text x="{vx2+34}" y="{(v_y+p_y)/2+4:.0f}" font-family="Inter" font-size="12" letter-spacing="3" fill="#8a8578">MARGIN</text>')
    return "".join(out)
