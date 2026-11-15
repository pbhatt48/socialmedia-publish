"""Risk vs uncertainty: a wide fan of possible outcomes that never breaks a solid floor. 900x520 viewBox."""
import random

GOLD = "#c9a96a"
GREY = "#8a8578"

def build():
    rnd = random.Random(42)
    out = []
    ground = 430
    floor = 360          # the line of permanent loss the paths never cross
    ox, oy = 110, 250    # origin: today's price
    ex = 790
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1"/>')
    # floor
    out.append(f'<line x1="{ox}" y1="{floor}" x2="{ex}" y2="{floor}" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.6"/>')
    for x in range(ox + 10, ex, 22):
        out.append(f'<line x1="{x}" y1="{floor}" x2="{x-9}" y2="{floor+10}" stroke="{GOLD}" stroke-opacity=".28" stroke-width="1"/>')
    # fan of outcomes
    n = 17
    for i in range(n):
        t = i / (n - 1)
        end = 60 + t * (floor - 72)           # spread from y=60 down to just above the floor
        mid = oy - (oy - end) * rnd.uniform(0.35, 0.6)
        mx = ox + (ex - ox) * rnd.uniform(0.4, 0.6)
        wob = rnd.uniform(-18, 18)
        alpha = 0.25 + 0.6 * (1 - abs(t - 0.45) * 1.6)
        alpha = max(min(alpha, 0.85), 0.18)
        out.append(f'<path d="M{ox},{oy} C{mx-120:.0f},{oy+wob:.0f} {mx:.0f},{mid:.0f} {ex},{end:.0f}" stroke="{GOLD}" '
                   f'stroke-opacity="{alpha:.2f}" stroke-width="{1.4 if i % 4 == 0 else 0.8}" fill="none" stroke-linecap="round"/>')
        out.append(f'<circle cx="{ex}" cy="{end:.0f}" r="{2.4 if i % 4 == 0 else 1.6}" fill="{GOLD}" fill-opacity="{alpha:.2f}"/>')
    # origin
    out.append(f'<circle cx="{ox}" cy="{oy}" r="26" fill="url(#glow)"/>')
    out.append(f'<circle cx="{ox}" cy="{oy}" r="5" fill="{GOLD}"/>')
    # uncertainty bracket
    bx = ex + 28
    out.append(f'<path d="M{bx-6},60 L{bx},60 L{bx},{floor-10} L{bx-6},{floor-10}" stroke="{GOLD}" stroke-opacity=".5" fill="none" stroke-width="1"/>')
    out.append(f'<text x="{bx+16}" y="{(60+floor-10)/2:.0f}" font-family="Inter" font-size="12" letter-spacing="3" fill="{GREY}" '
               f'text-anchor="middle" transform="rotate(90 {bx+16} {(60+floor-10)/2:.0f})">UNCERTAINTY</text>')
    # labels
    out.append(f'<text x="{(ox+ex)/2:.0f}" y="{floor+40}" text-anchor="middle" font-family="Inter" font-size="12" '
               f'letter-spacing="3" fill="{GREY}">RISK: PERMANENT LOSS</text>')
    out.append(f'<text x="{ox}" y="{oy-28}" text-anchor="middle" font-family="Inter" font-size="12" letter-spacing="3" fill="{GREY}">PRICE PAID</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
