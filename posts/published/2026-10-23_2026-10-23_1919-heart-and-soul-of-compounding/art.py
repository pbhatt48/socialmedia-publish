"""Snowball on a long hill: compounding is powerful, but it takes a long slope and patience.
Returns SVG inner markup for a 900x520 viewBox."""
import math

GOLD = "#c9a96a"


def ball(out, cx, cy, r, alpha):
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{GOLD}" '
               f'stroke-opacity="{alpha:.2f}" stroke-width="{max(0.8, r / 30):.2f}"/>')
    # inner layers of accumulated snow
    for k in range(1, int(r // 9) + 1):
        rr = r - k * 9
        if rr < 3:
            break
        out.append(f'<circle cx="{cx:.1f}" cy="{cy - (r - rr) * 0.25:.1f}" r="{rr:.1f}" fill="none" stroke="{GOLD}" '
                   f'stroke-opacity="{alpha * 0.35:.2f}" stroke-width=".7"/>')


def build():
    out = []
    ground = 430
    out.append(f'<line x1="20" y1="{ground}" x2="880" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # long gentle hill from upper-left down to the ground
    x0, y0, x1, y1 = 40, 150, 820, ground
    out.append(f'<path d="M{x0},{y0} C{300},{y0+40} {560},{y1-30} {x1},{y1}" stroke="{GOLD}" '
               f'stroke-opacity=".8" stroke-width="1.6" fill="none" stroke-linecap="round"/>')
    # hatching under the slope
    def hill(t):
        a, b, c, d = (x0, y0), (300, y0 + 40), (560, y1 - 30), (x1, y1)
        x = (1-t)**3*a[0] + 3*(1-t)**2*t*b[0] + 3*(1-t)*t**2*c[0] + t**3*d[0]
        y = (1-t)**3*a[1] + 3*(1-t)**2*t*b[1] + 3*(1-t)*t**2*c[1] + t**3*d[1]
        dx = 3*(1-t)**2*(b[0]-a[0]) + 6*(1-t)*t*(c[0]-b[0]) + 3*t**2*(d[0]-c[0])
        dy = 3*(1-t)**2*(b[1]-a[1]) + 6*(1-t)*t*(c[1]-b[1]) + 3*t**2*(d[1]-c[1])
        L = math.hypot(dx, dy)
        return x, y, -dy / L, dx / L  # normal pointing up-right
    for i in range(1, 40):
        t = i / 40
        x, y, _, _ = hill(t)
        out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{ground}" stroke="{GOLD}" '
                   f'stroke-opacity=".10" stroke-width=".8"/>')
    # snowballs growing along the slope (exponential radius)
    stops = [0.06, 0.24, 0.44, 0.64, 0.86]
    labels = ["YEAR 1", "10", "20", "30", "40"]
    for i, t in enumerate(stops):
        r = 4 * (1.95 ** i)
        x, y, nx, ny = hill(t)
        nx, ny = -nx, -ny  # flip to point away from hill (upward)
        if ny > 0:
            nx, ny = -nx, -ny
        cx, cy = x + nx * r, y + ny * r
        ball(out, cx, cy, r, 0.55 + 0.1 * i)
        out.append(f'<text x="{x:.1f}" y="{ground + 26}" text-anchor="middle" font-family="Inter" font-size="11" '
                   f'letter-spacing="2" fill="{GOLD}" fill-opacity=".55">{labels[i]}</text>')
        out.append(f'<line x1="{x:.1f}" y1="{ground + 4}" x2="{x:.1f}" y2="{ground + 10}" stroke="{GOLD}" stroke-opacity=".4"/>')
    # faint track pressed into the slope
    out.append(f'<path d="M{x0+20},{y0+6} C{300},{y0+46} {560},{y1-24} {x1-60},{y1-4}" stroke="{GOLD}" '
               f'stroke-opacity=".25" stroke-width="1" stroke-dasharray="2 6" fill="none"/>')
    return "\n".join(out)
