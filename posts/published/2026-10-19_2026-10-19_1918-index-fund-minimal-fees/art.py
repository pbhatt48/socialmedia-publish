"""The whole market, owned cheaply: a field of many small businesses, and two compounding paths that diverge only by fees. 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"

def build():
    rnd = random.Random(1996)
    out = []
    ground = 420
    x0, x1 = 70, 830
    out.append(f'<line x1="30" y1="{ground}" x2="870" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # the whole market: many small stems of varying height
    n = 76
    for i in range(n):
        x = x0 + (x1 - x0) * i / (n - 1)
        h = 18 + 70 * (i / n) + rnd.uniform(-10, 26)
        a = rnd.uniform(0.18, 0.42)
        out.append(f'<line x1="{x:.1f}" y1="{ground}" x2="{x:.1f}" y2="{ground-h:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity="{a:.2f}" stroke-width="1"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{ground-h:.1f}" r="1.3" fill="{GOLD}" fill-opacity="{a+0.15:.2f}"/>')

    def curve(rate):
        pts = []
        for k in range(61):
            t = k / 60
            x = x0 + (x1 - x0) * t
            v = (math.pow(1 + rate, 30 * t) - 1) / (math.pow(1.10, 30) - 1)
            pts.append((x, ground - 130 - 230 * v))
        return pts

    hi = curve(0.10)
    lo = curve(0.08)
    def path(pts):
        return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    out.append(f'<path d="{path(lo)}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1.3" '
               f'stroke-dasharray="3 6" fill="none" stroke-linecap="round"/>')
    out.append(f'<path d="{path(hi)}" stroke="{GOLD}" stroke-opacity=".95" stroke-width="2" fill="none" stroke-linecap="round"/>')
    # the gap fees open up
    ex, ey_hi, ey_lo = hi[-1][0], hi[-1][1], lo[-1][1]
    out.append(f'<line x1="{ex+16}" y1="{ey_hi:.1f}" x2="{ex+16}" y2="{ey_lo:.1f}" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1"/>')
    for yy in (ey_hi, ey_lo):
        out.append(f'<line x1="{ex+11}" y1="{yy:.1f}" x2="{ex+21}" y2="{yy:.1f}" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1"/>')
    out.append(f'<circle cx="{ex}" cy="{ey_hi:.1f}" r="4" fill="{GOLD}"/>')
    out.append(f'<circle cx="{ex}" cy="{ey_hi:.1f}" r="22" fill="url(#glow)"/>')
    out.append(f'<circle cx="{ex}" cy="{ey_lo:.1f}" r="3" fill="none" stroke="{GOLD}" stroke-opacity=".6"/>')
    out.append(f'<circle cx="{x0}" cy="{ground-130}" r="3" fill="{GOLD}"/>')
    lab = 'font-family="Inter" font-size="13" letter-spacing="3" fill="#8a8578"'
    out.append(f'<text x="{ex-14}" y="{ey_hi-16:.1f}" text-anchor="end" {lab}>MINIMAL FEES</text>')
    lx = ex - 150
    ly = [y for x, y in lo if x >= lx][0]
    out.append(f'<text x="{lx}" y="{ly+30:.1f}" text-anchor="start" {lab}>AFTER COSTS</text>')
    out.append(f'<text x="450" y="{ground+40}" text-anchor="middle" {lab}>THE WHOLE MARKET</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
