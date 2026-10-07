"""Guidance vs. reality: honest, uneven quarterly bars beside a ruler-straight promised line,
with the final bars quietly 'topped up' in dashed outline to meet it. Returns SVG inner markup for 900x520."""
import random

GOLD = "#c9a96a"
MUTE = "#8a8578"

def build():
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    rnd = random.Random(4)
    n, x0, step, w = 16, 110, 44, 18
    # the promised line: a perfectly smooth, steady climb
    def promise(i):
        return ground - 95 - i * 13.5
    xa, xb = x0 - 20, x0 + (n - 1) * step + 20
    out.append(f'<line x1="{xa}" y1="{promise(-20/step):.1f}" x2="{xb}" y2="{promise((n-1)+20/step):.1f}" stroke="{GOLD}" '
               f'stroke-opacity=".55" stroke-width="1.2" stroke-dasharray="6 6"/>')
    # honest results: real businesses are lumpy
    level = 0
    for i in range(n):
        x = x0 + i * step
        level += rnd.uniform(-1, 1.6)
        actual = ground - 95 - i * 9.5 + rnd.uniform(-38, 30) + level * 4
        actual = min(actual, promise(i) + 6) if i < 11 else actual
        target = promise(i)
        if i < 11:
            h = ground - actual
            alpha = 0.55 + 0.3 * (i / 10)
            out.append(f'<rect x="{x - w/2:.1f}" y="{actual:.1f}" width="{w}" height="{h:.1f}" fill="{GOLD}" fill-opacity="{alpha*0.22:.2f}" '
                       f'stroke="{GOLD}" stroke-opacity="{alpha:.2f}" stroke-width="1"/>')
            if i in (3, 6, 9):
                out.append(f'<circle cx="{x}" cy="{target:.1f}" r="2.4" fill="{GOLD}" fill-opacity=".7"/>')
        else:
            # what the business really earned
            real = ground - 70 - i * 6 + rnd.uniform(-30, 20)
            out.append(f'<rect x="{x - w/2:.1f}" y="{real:.1f}" width="{w}" height="{ground - real:.1f}" fill="{GOLD}" fill-opacity=".18" '
                       f'stroke="{GOLD}" stroke-opacity=".75" stroke-width="1"/>')
            # the 'adjustment' stacked on top to land exactly on the promise
            out.append(f'<rect x="{x - w/2:.1f}" y="{target:.1f}" width="{w}" height="{real - target:.1f}" fill="none" '
                       f'stroke="{GOLD}" stroke-opacity=".6" stroke-width="1" stroke-dasharray="2 3"/>')
            out.append(f'<circle cx="{x}" cy="{target:.1f}" r="2.4" fill="{GOLD}"/>')
    # divider between earning the numbers and making them up
    xd = x0 + 10.5 * step
    out.append(f'<line x1="{xd}" y1="{ground - 300}" x2="{xd}" y2="{ground + 14}" stroke="{GOLD}" stroke-opacity=".25" stroke-width="1"/>')
    lab = lambda x, y, t, a="middle", c=MUTE: out.append(
        f'<text x="{x}" y="{y}" text-anchor="{a}" font-family="Inter" font-size="13" letter-spacing="3" fill="{c}">{t}</text>')
    lab(xb, promise(n - 1) - 18, "THE PROMISE", "end", GOLD)
    lab((x0 + xd - 22) / 2, ground + 40, "EARNED")
    lab((xd + xb) / 2, ground + 40, "ADJUSTED")
    return "".join(out)
