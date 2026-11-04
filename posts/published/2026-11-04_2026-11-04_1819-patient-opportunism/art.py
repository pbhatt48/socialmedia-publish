"""Patient opportunism: price wanders above a value line for years; the investor waits for the rare dip below."""
import math, random

GOLD = "#c9a96a"

def price_path():
    rnd = random.Random(42)
    pts = []
    n = 160
    for i in range(n + 1):
        t = i / n
        x = 70 + t * 760
        base = 205 - 40 * math.sin(t * 5.2) - 18 * math.sin(t * 13.1 + 1.0)
        # the rare bargain: a deep, brief dip below value near t = 0.72
        dip = 140 * math.exp(-((t - 0.72) / 0.055) ** 2)
        y = base + dip + rnd.uniform(-5, 5)
        pts.append((x, y))
    return pts

def build():
    out = []
    ground = 430
    value_y = 300
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    for i in range(11):
        tx = 70 + i * 76
        out.append(f'<line x1="{tx}" y1="{ground+6}" x2="{tx}" y2="{ground+13}" stroke="{GOLD}" stroke-opacity=".4"/>')
    # intrinsic value line
    out.append(f'<line x1="70" y1="{value_y}" x2="830" y2="{value_y}" stroke="{GOLD}" stroke-opacity=".55" '
               f'stroke-width="1.2" stroke-dasharray="3 7" stroke-linecap="round"/>')
    out.append(f'<text x="70" y="{value_y-14}" font-family="Inter" font-size="13" letter-spacing="3" fill="#8a8578">VALUE</text>')
    pts = price_path()
    # shaded bargain zone where price sits below value
    below = [p for p in pts if p[1] > value_y]
    if below:
        poly = f"M{below[0][0]:.1f},{value_y} " + " ".join(f"L{x:.1f},{y:.1f}" for x, y in below) + f" L{below[-1][0]:.1f},{value_y} Z"
        out.append(f'<path d="{poly}" fill="{GOLD}" fill-opacity=".14"/>')
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.8" fill="none" stroke-linejoin="round" stroke-linecap="round"/>')
    # faint echo line for depth
    d2 = "M" + " L".join(f"{x:.1f},{y-10:.1f}" for x, y in pts)
    out.append(f'<path d="{d2}" stroke="{GOLD}" stroke-opacity=".15" stroke-width="1" fill="none"/>')
    # the moment of action
    lo = max(pts, key=lambda p: p[1])
    out.append(f'<circle cx="{lo[0]:.1f}" cy="{lo[1]:.1f}" r="30" fill="url(#glow)"/>')
    out.append(f'<circle cx="{lo[0]:.1f}" cy="{lo[1]:.1f}" r="5" fill="{GOLD}"/>')
    out.append(f'<circle cx="{lo[0]:.1f}" cy="{lo[1]:.1f}" r="12" stroke="{GOLD}" stroke-opacity=".5" fill="none"/>')
    out.append(f'<line x1="{lo[0]:.1f}" y1="{lo[1]+16:.1f}" x2="{lo[0]:.1f}" y2="{ground}" stroke="{GOLD}" stroke-opacity=".3" stroke-dasharray="2 5"/>')
    out.append(f'<text x="{lo[0]:.1f}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" letter-spacing="3" fill="#8a8578">ACT</text>')
    # the long wait
    wx2 = lo[0] - 70
    mid = (70 + wx2) / 2
    for a, b in ((70, mid - 40), (mid + 40, wx2)):
        out.append(f'<line x1="{a:.1f}" y1="{ground+35}" x2="{b:.1f}" y2="{ground+35}" stroke="{GOLD}" stroke-opacity=".3"/>')
    out.append(f'<text x="{(70+wx2)/2:.1f}" y="{ground+40}" text-anchor="middle" font-family="Inter" font-size="13" letter-spacing="3" fill="#8a8578">WAIT</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
