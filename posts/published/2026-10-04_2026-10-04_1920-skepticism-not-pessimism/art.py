"""Pendulum of sentiment: skepticism leans against whichever extreme the crowd has reached. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"
MUTED = "#8a8578"

def build():
    out = []
    px, py, L = 450, 92, 300
    ground = 452
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # support beam
    out.append(f'<line x1="380" y1="{py}" x2="520" y2="{py}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.6" stroke-linecap="round"/>')
    for i in range(8):
        x = 388 + i * 18
        out.append(f'<line x1="{x}" y1="{py}" x2="{x-8}" y2="{py-10}" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1"/>')
    # swing arc with ticks
    amax = math.radians(42)
    pts = []
    for i in range(61):
        a = -amax + 2 * amax * i / 60
        pts.append(f'{px + (L+18)*math.sin(a):.1f},{py + (L+18)*math.cos(a):.1f}')
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1" stroke-dasharray="2 6" stroke-linecap="round"/>')
    for i in range(-6, 7):
        a = amax * i / 6
        r1, r2 = L + 10, L + (30 if i % 3 == 0 else 22)
        out.append(f'<line x1="{px + r1*math.sin(a):.1f}" y1="{py + r1*math.cos(a):.1f}" x2="{px + r2*math.sin(a):.1f}" y2="{py + r2*math.cos(a):.1f}" '
                   f'stroke="{GOLD}" stroke-opacity="{.6 if i % 3 == 0 else .3}" stroke-width="1"/>')
    # ghost positions of the swing, fading toward the extremes
    for k, deg in enumerate((-36, -24, -12, 12, 24)):
        a = math.radians(deg)
        bx, by = px + L*math.sin(a), py + L*math.cos(a)
        op = 0.10 + 0.04 * (abs(deg) / 12)
        out.append(f'<line x1="{px}" y1="{py}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{GOLD}" stroke-opacity="{op:.2f}" stroke-width="1"/>')
        out.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="13" fill="none" stroke="{GOLD}" stroke-opacity="{op+.06:.2f}" stroke-width="1"/>')
    # the pendulum, at the excessive-optimism extreme
    a = math.radians(36)
    bx, by = px + L*math.sin(a), py + L*math.cos(a)
    out.append(f'<line x1="{px}" y1="{py}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.6"/>')
    out.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="40" fill="url(#glow)"/>')
    out.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="16" fill="{GOLD}" fill-opacity=".9"/>')
    out.append(f'<circle cx="{px}" cy="{py}" r="4" fill="{GOLD}"/>')
    # skeptic's counter-arrow pushing back toward the middle
    ar = L - 70
    a0, a1 = math.radians(30), math.radians(8)
    p0 = (px + ar*math.sin(a0), py + ar*math.cos(a0))
    p1 = (px + ar*math.sin(a1), py + ar*math.cos(a1))
    am = (a0 + a1) / 2
    c = (px + (ar+14)*math.sin(am), py + (ar+14)*math.cos(am))
    out.append(f'<path d="M{p0[0]:.1f},{p0[1]:.1f} Q{c[0]:.1f},{c[1]:.1f} {p1[0]:.1f},{p1[1]:.1f}" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.2" fill="none" stroke-linecap="round"/>')
    out.append(f'<path d="M{p1[0]:.1f},{p1[1]:.1f} l9,-5 M{p1[0]:.1f},{p1[1]:.1f} l8,6" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.2" fill="none" stroke-linecap="round"/>')
    # center plumb mark
    out.append(f'<line x1="{px}" y1="{py+L+36}" x2="{px}" y2="{ground}" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1"/>')
    # labels at the extremes
    for deg, lab in ((-42, "PESSIMISM"), (42, "OPTIMISM")):
        a = math.radians(deg)
        tx, ty = px + (L+60)*math.sin(a), py + (L+60)*math.cos(a)
        out.append(f'<text x="{tx:.1f}" y="{ty+4:.1f}" text-anchor="middle" font-family="Inter" font-size="13" letter-spacing="3" fill="{MUTED}">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
