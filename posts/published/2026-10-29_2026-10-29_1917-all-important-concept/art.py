"""Discounted cash flows: future streams of cash, each worth less the further away it lies,
all drawn back to a single present value. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"

def build():
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    px, py = 120, 140  # present value point
    n = 12
    x0, dx = 250, 52
    for i in range(n):
        x = x0 + i * dx
        cf = 150 * (1.06 ** i)            # growing cash flow
        pv = cf / (1.10 ** (i + 1))        # its discounted value
        h_cf, h_pv = cf * 0.95, pv * 1.35
        a = 0.85 - i * 0.05
        # nominal cash flow: faint outline
        out.append(f'<rect x="{x-9}" y="{ground-h_cf:.1f}" width="18" height="{h_cf:.1f}" fill="none" '
                   f'stroke="{GOLD}" stroke-opacity="{a*0.35:.2f}" stroke-width=".8"/>')
        # discounted portion: solid
        out.append(f'<rect x="{x-9}" y="{ground-h_pv:.1f}" width="18" height="{h_pv:.1f}" fill="{GOLD}" fill-opacity="{a*0.55:.2f}"/>')
        # thread back to present value
        out.append(f'<line x1="{x}" y1="{ground-h_pv:.1f}" x2="{px}" y2="{py}" stroke="{GOLD}" '
                   f'stroke-opacity="{a*0.45:.2f}" stroke-width=".8" stroke-dasharray="2 5" stroke-linecap="round"/>')
    # present value: a single glowing point with a stem to the ground
    out.append(f'<line x1="{px}" y1="{py}" x2="{px}" y2="{ground}" stroke="{GOLD}" stroke-opacity=".6" stroke-width="1.4"/>')
    out.append(f'<circle cx="{px}" cy="{py}" r="34" fill="url(#glow)"/>')
    out.append(f'<circle cx="{px}" cy="{py}" r="6" fill="{GOLD}"/>')
    out.append(f'<circle cx="{px}" cy="{py}" r="13" fill="none" stroke="{GOLD}" stroke-opacity=".5" stroke-width=".8"/>')
    labels = [(px, "TODAY"), (x0, "YEAR 1"), (x0 + 5 * dx, "6"), (x0 + 11 * dx, "12 …")]
    for tx, lab in labels:
        out.append(f'<line x1="{tx}" y1="{ground+6}" x2="{tx}" y2="{ground+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
