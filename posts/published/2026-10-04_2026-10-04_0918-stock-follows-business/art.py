"""Two businesses compounding at 6% and 18% on capital; the stock price wanders but is tethered to each. Returns SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"
X0, X1, GROUND = 90, 810, 420

def curve(rate, years=40, top=None):
    pts = []
    for i in range(years + 1):
        v = (1 + rate) ** i
        pts.append((i, v))
    return pts

def to_xy(pts, vmax, height):
    out = []
    for i, v in pts:
        x = X0 + (X1 - X0) * i / 40
        y = GROUND - height * (math.log(v) / math.log(vmax))
        out.append((x, y))
    return out

def path(xy):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in xy)

def price(xy, seed, amp):
    rnd = random.Random(seed)
    out, d = [], 0.0
    for k in range(len(xy) - 1):
        (xa, ya), (xb, yb) = xy[k], xy[k + 1]
        for s in range(4):
            t = s / 4
            d = d * 0.72 + rnd.uniform(-1, 1) * amp
            out.append((xa + (xb - xa) * t, ya + (yb - ya) * t + d))
    out.append(xy[-1])
    return out

def build():
    out = []
    out.append(f'<line x1="40" y1="{GROUND}" x2="860" y2="{GROUND}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    vmax = 1.18 ** 40
    hi = to_xy(curve(0.18), vmax, 340)
    lo = to_xy(curve(0.06), vmax, 340)
    for xy, seed, lab in ((lo, 3, "6% ON CAPITAL"), (hi, 9, "18% ON CAPITAL")):
        out.append(f'<path d="{path(price(xy, seed, 9))}" stroke="{GOLD}" stroke-opacity=".38" stroke-width="1" fill="none" stroke-linejoin="round"/>')
        out.append(f'<path d="{path(xy)}" stroke="{GOLD}" stroke-opacity=".95" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
        ex, ey = xy[-1]
        out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4" fill="{GOLD}"/>')
        out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="22" fill="url(#glow)"/>')
        out.append(f'<text x="{ex-14:.1f}" y="{ey-16:.1f}" text-anchor="end" font-family="Inter" font-size="12" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    for yr in (0, 10, 20, 30, 40):
        tx = X0 + (X1 - X0) * yr / 40
        out.append(f'<line x1="{tx}" y1="{GROUND+6}" x2="{tx}" y2="{GROUND+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx}" y="{GROUND+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{"YEAR 0" if yr == 0 else yr}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
