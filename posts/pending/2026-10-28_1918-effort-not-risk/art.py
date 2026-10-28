"""Two climbs: a gentle path to a low plateau (defensive) and a switchback trail to a high summit (enterprising).
Return follows effort, not appetite for risk. Returns SVG inner markup for a 900x520 viewBox."""
GOLD = "#c9a96a"

def line(pts, op, w=1.2, dash=None):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" stroke="{GOLD}" stroke-opacity="{op:.2f}" stroke-width="{w}" fill="none" '
            f'stroke-linecap="round" stroke-linejoin="round"{da}/>')

def build():
    g = 420
    out = [f'<line x1="40" y1="{g}" x2="860" y2="{g}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>']
    # low plateau (left)
    mesa = [(90, g), (170, g - 70), (300, g - 82), (380, g)]
    out.append(line(mesa, .55, 1.4))
    for i in range(1, 6):  # faint strata
        y = g - 12 * i
        if y > g - 66:
            out.append(line([(90 + 80 * (g - y) / 70 + 6, y), (380 - 80 * (g - y) / 82 - 6, y)], .12, .8))
    # gentle path to plateau
    out.append(line([(110, g - 4), (150, g - 40), (210, g - 74)], .6, 1.2, "2 6"))
    out.append(f'<circle cx="235" cy="{g-78}" r="4" fill="{GOLD}" fill-opacity=".7"/>')
    # high summit (right)
    peak = [(430, g), (560, g - 180), (610, g - 250), (650, g - 320), (700, g - 230), (760, g - 140), (840, g)]
    out.append(line(peak, .85, 1.6))
    for k, op in ((0.82, .18), (0.64, .14), (0.46, .1)):  # inner ridges
        out.append(line([(650 - (650 - 430) * k, g), (650, g - 320 * k - 0)], op, .8))
    # switchback trail up the summit
    trail = [(470, g - 6), (600, g - 40), (520, g - 80), (640, g - 115), (575, g - 155), (660, g - 190),
             (620, g - 230), (668, g - 262), (650, g - 300)]
    out.append(line(trail, .7, 1.2, "2 6"))
    # flag at summit
    out.append(f'<line x1="650" y1="{g-320}" x2="650" y2="{g-362}" stroke="{GOLD}" stroke-width="1.4"/>')
    out.append(f'<path d="M650,{g-362} L678,{g-354} L650,{g-346} Z" fill="{GOLD}" fill-opacity=".85"/>')
    out.append(f'<circle cx="650" cy="{g-322}" r="34" fill="url(#glow)"/>')
    # labels
    for tx, lab in ((235, "DEFENSIVE"), (650, "ENTERPRISING")):
        out.append(f'<line x1="{tx}" y1="{g+6}" x2="{tx}" y2="{g+14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        out.append(f'<text x="{tx}" y="{g+40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".4"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
