"""Probability vs outcome: a distribution of possibilities, with the realized outcome landing in the tail. Returns SVG inner markup for a 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"

def density(x, mu=380, sigma=95):
    return math.exp(-0.5 * ((x - mu) / sigma) ** 2)

def build():
    out = []
    ground = 420
    peak = 300
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # faint alternate futures: many thin possible paths fanning from the left
    rnd = random.Random(5)
    for i in range(46):
        y = 160 + rnd.gauss(0, 1) * 0
        end = 380 + rnd.gauss(0, 95)
        end = max(110, min(800, end))
        h = ground - peak * density(end) - 6
        out.append(f'<path d="M80,{ground-40:.1f} C260,{ground-60:.1f} {end-120:.1f},{h-80:.1f} {end:.1f},{h:.1f}" '
                   f'stroke="{GOLD}" stroke-opacity="{rnd.uniform(.05,.14):.2f}" stroke-width=".7" fill="none"/>')
    # sample ticks under the curve
    for x in range(100, 801, 9):
        h = peak * density(x)
        if h < 3:
            continue
        out.append(f'<line x1="{x}" y1="{ground}" x2="{x}" y2="{ground-h:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity="{0.08 + 0.22 * h / peak:.2f}" stroke-width="1"/>')
    # the curve itself
    pts = " ".join(f"{x},{ground - peak * density(x):.1f}" for x in range(70, 831, 4))
    out.append(f'<polyline points="{pts}" stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.8" fill="none" stroke-linejoin="round"/>')
    # most probable marker
    out.append(f'<line x1="380" y1="{ground}" x2="380" y2="{ground-peak-18}" stroke="{GOLD}" stroke-opacity=".4" stroke-dasharray="2 6"/>')
    out.append(f'<circle cx="380" cy="{ground-peak}" r="3.2" fill="none" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.2"/>')
    # realized outcome in the right tail
    ox = 690
    oy = ground - peak * density(ox)
    out.append(f'<line x1="{ox}" y1="{ground}" x2="{ox}" y2="{ground-150}" stroke="{GOLD}" stroke-opacity=".75" stroke-width="1.2"/>')
    out.append(f'<circle cx="{ox}" cy="{ground-150}" r="28" fill="url(#glow)"/>')
    out.append(f'<circle cx="{ox}" cy="{ground-150}" r="5" fill="{GOLD}"/>')
    out.append(f'<circle cx="{ox}" cy="{oy:.1f}" r="2.4" fill="{GOLD}"/>')
    for tx, lab in [(380, "PROBABLE"), (ox, "WHAT HAPPENED")]:
        out.append(f'<line x1="{tx}" y1="{ground+6}" x2="{tx}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
