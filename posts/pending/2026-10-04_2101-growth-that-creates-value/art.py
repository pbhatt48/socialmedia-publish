"""Each dollar retained becomes more than a dollar of value: coin stacks rising on a value curve,
while a low-return path sinks below cost. Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"
MUTED = "#8a8578"


def coin_stack(out, x, base, n, alpha):
    for i in range(n):
        y = base - i * 9
        out.append(f'<ellipse cx="{x}" cy="{y:.1f}" rx="17" ry="4.6" fill="#0f0f0f" fill-opacity=".9" '
                   f'stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="1.1"/>')


def build():
    out = []
    ground = 400
    x0, x1 = 190, 830
    out.append(f'<line x1="50" y1="{ground}" x2="870" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # cost-of-capital baseline: one dollar in, one dollar out
    out.append(f'<line x1="{x0}" y1="{ground-40}" x2="{x1}" y2="{ground-40}" stroke="{GOLD}" stroke-opacity=".28" '
               f'stroke-width="1" stroke-dasharray="3 6"/>')

    # value-creating path (compounding above cost)
    def up(t):
        return ground - 40 - 250 * (math.exp(2.1 * t) - 1) / (math.exp(2.1) - 1)

    # value-destroying path (growth that hurts)
    def down(t):
        return ground - 40 + 32 * t ** 1.4

    pts_up = " ".join(f"{x0 + (x1 - x0) * t:.1f},{up(t):.1f}" for t in [i / 60 for i in range(61)])
    pts_dn = " ".join(f"{x0 + (x1 - x0) * t:.1f},{down(t):.1f}" for t in [i / 60 for i in range(61)])
    out.append(f'<polyline points="{pts_dn}" fill="none" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1.2" '
               f'stroke-dasharray="1 5" stroke-linecap="round"/>')
    out.append(f'<polyline points="{pts_up}" fill="none" stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.6" '
               f'stroke-linecap="round"/>')

    # each retained dollar (small coin on the baseline) lifts to a taller stack of value
    for k, t in enumerate([0.12, 0.32, 0.52, 0.72, 0.92]):
        x = x0 + (x1 - x0) * t
        top = up(t)
        n = max(1, int(round((ground - top) / 9)) - 1)
        n = min(n, 30)
        # thin rule from stack to curve point
        out.append(f'<line x1="{x:.1f}" y1="{ground-4}" x2="{x:.1f}" y2="{top:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity=".14" stroke-width="1"/>')
        coin_stack(out, x, ground - 6, min(n, 3 + k * 6), 0.35 + 0.12 * k)
        out.append(f'<circle cx="{x:.1f}" cy="{top:.1f}" r="3.2" fill="{GOLD}"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{top:.1f}" r="14" fill="url(#glow)"/>')

    out.append(f'<text x="{x0-14}" y="{ground-36}" text-anchor="end" font-family="Inter" font-size="12" letter-spacing="3" fill="{MUTED}">$1 RETAINED</text>')
    out.append(f'<text x="{x1}" y="{up(1)-16:.1f}" text-anchor="end" font-family="Inter" font-size="12" letter-spacing="3" fill="{MUTED}">&gt; $1 OF VALUE</text>')
    out.append(f'<text x="{x1}" y="{down(1)+22:.1f}" text-anchor="end" font-family="Inter" font-size="12" letter-spacing="3" fill="{MUTED}" fill-opacity=".7">&lt; $1</text>')

    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
