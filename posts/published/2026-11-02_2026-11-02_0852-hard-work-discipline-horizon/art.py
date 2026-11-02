"""A long path toward a distant horizon, marked by cairns built stone by stone: hard work, discipline, a long horizon."""
import math, random

GOLD = "#c9a96a"

def cairn(out, rnd, x, base, scale, n, alpha):
    y = base
    for i in range(n):
        w = (22 - i * 2.2) * scale * rnd.uniform(0.9, 1.1)
        h = (8 - i * 0.5) * scale
        cy = y - h
        out.append(f'<ellipse cx="{x + rnd.uniform(-1.5,1.5)*scale:.1f}" cy="{cy:.1f}" rx="{w/2:.1f}" ry="{h:.1f}" '
                   f'fill="none" stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="{max(0.6,1.3*scale):.2f}"/>')
        y = cy - h + 1.2 * scale

def build():
    rnd = random.Random(5)
    out = []
    hz = 250          # horizon
    vx = 560          # vanishing point
    out.append(f'<line x1="40" y1="{hz}" x2="860" y2="{hz}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # distant sun
    out.append(f'<circle cx="{vx}" cy="{hz}" r="70" fill="url(#glow)"/>')
    out.append(f'<path d="M{vx-34},{hz} A34,34 0 0 1 {vx+34},{hz}" fill="none" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.2"/>')
    for k in range(9):
        a = math.pi * (k + 1) / 10
        r1, r2 = 44, 58 + (k % 2) * 10
        out.append(f'<line x1="{vx+r1*math.cos(a):.1f}" y1="{hz-r1*math.sin(a):.1f}" x2="{vx+r2*math.cos(a):.1f}" '
                   f'y2="{hz-r2*math.sin(a):.1f}" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1"/>')
    # distant hills
    out.append(f'<path d="M60,{hz} C160,{hz-38} 250,{hz-30} 330,{hz-8} C380,{hz-22} 430,{hz-26} 480,{hz}" fill="none" stroke="{GOLD}" stroke-opacity=".28" stroke-width="1"/>')
    out.append(f'<path d="M640,{hz} C700,{hz-30} 780,{hz-44} 840,{hz-14}" fill="none" stroke="{GOLD}" stroke-opacity=".28" stroke-width="1"/>')
    # winding path edges (perspective)
    left = f'M250,480 C330,420 420,360 470,320 C520,285 545,265 {vx-3},{hz}'
    right = f'M470,480 C500,420 560,370 590,330 C610,300 575,270 {vx+3},{hz}'
    out.append(f'<path d="{left}" fill="none" stroke="{GOLD}" stroke-opacity=".75" stroke-width="1.3"/>')
    out.append(f'<path d="{right}" fill="none" stroke="{GOLD}" stroke-opacity=".75" stroke-width="1.3"/>')
    # dashed center line receding
    out.append(f'<path d="M360,480 C420,420 480,365 525,327 C560,295 560,268 {vx},{hz}" fill="none" stroke="{GOLD}" '
               f'stroke-opacity=".35" stroke-width="1" stroke-dasharray="3 9"/>')
    # ground texture lines
    for i in range(14):
        y = hz + 8 + (i ** 1.6) * 3.2
        if y > 470: break
        out.append(f'<line x1="{60+i*4}" y1="{y:.1f}" x2="{200-i*3}" y2="{y:.1f}" stroke="{GOLD}" stroke-opacity="{.10+i*.01:.2f}" stroke-width=".8"/>')
        out.append(f'<line x1="{700+i*3}" y1="{y:.1f}" x2="{840-i*4}" y2="{y:.1f}" stroke="{GOLD}" stroke-opacity="{.10+i*.01:.2f}" stroke-width=".8"/>')
    # cairns along the path, nearer = larger, built stone by stone
    for x, base, s, n, a in [(548, 268, 0.35, 3, .45), (612, 300, 0.55, 4, .6), (440, 352, 0.8, 5, .75), (650, 405, 1.1, 6, .85), (200, 470, 1.45, 7, .95)]:
        cairn(out, rnd, x, base, s, n, a)
    # footsteps on the path
    for i, (fx, fy) in enumerate([(380, 462), (400, 440), (425, 418), (445, 398), (470, 378), (488, 360), (508, 344)]):
        sc = 1 - i * 0.1
        dx = -6 * sc if i % 2 else 6 * sc
        out.append(f'<ellipse cx="{fx+dx:.1f}" cy="{fy}" rx="{3*sc:.1f}" ry="{5.5*sc:.1f}" fill="{GOLD}" fill-opacity="{.55-i*.05:.2f}"/>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
