"""Windshield vs. rear-view mirror: the road behind is crisp, the road ahead fades into haze. SVG inner markup for a 900x520 viewBox."""

GOLD = "#c9a96a"


def road(out, cx, horizon, base_y, half_base, clip, fade, n_dashes, alpha_near, alpha_far):
    """Perspective road from base_y up to the vanishing point at (cx, horizon)."""
    steps = 14
    for side in (-1, 1):
        for i in range(steps):
            t0, t1 = i / steps, (i + 1) / steps
            y0 = base_y + (horizon - base_y) * t0
            y1 = base_y + (horizon - base_y) * t1
            x0 = cx + side * half_base * (1 - t0)
            x1 = cx + side * half_base * (1 - t1)
            a = alpha_near + (alpha_far - alpha_near) * (t1 if fade else 0)
            out.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{GOLD}" '
                       f'stroke-opacity="{a:.2f}" stroke-width="{1.6 * (1 - t0) + 0.4:.2f}" stroke-linecap="round"{clip}/>')
    # centre dashes, shrinking with distance
    for i in range(n_dashes):
        t = i / n_dashes
        t2 = t + 0.5 / n_dashes
        y0 = base_y + (horizon - base_y) * (1 - (1 - t) ** 1.6)
        y1 = base_y + (horizon - base_y) * (1 - (1 - t2) ** 1.6)
        a = alpha_near + (alpha_far - alpha_near) * (t if fade else 0)
        out.append(f'<line x1="{cx}" y1="{y0:.1f}" x2="{cx}" y2="{y1:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity="{a:.2f}" stroke-width="{2.2 * (1 - t) + 0.5:.2f}" stroke-linecap="round"{clip}/>')


def build():
    out = []
    cx = 450
    horizon = 300
    # windshield frame
    out.append(f'<path d="M120,470 L190,150 Q200,110 245,108 L655,108 Q700,110 710,150 L780,470" '
               f'stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.6" fill="none" stroke-linejoin="round"/>')
    out.append(f'<line x1="90" y1="470" x2="810" y2="470" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # horizon inside the windshield
    out.append(f'<line x1="172" y1="{horizon}" x2="728" y2="{horizon}" stroke="{GOLD}" stroke-opacity=".3" stroke-width="1"/>')
    # road ahead: strong near, dissolving toward the horizon
    road(out, cx, horizon, 468, 230, "", True, 9, 0.85, 0.04)
    # haze bands over the far road
    for k, (y, op) in enumerate([(286, .07), (300, .10), (314, .07), (328, .04)]):
        out.append(f'<path d="M{230 + k * 12},{y} Q{450},{y - 6} {670 - k * 12},{y}" stroke="{GOLD}" '
                   f'stroke-opacity="{op}" stroke-width="7" fill="none" stroke-linecap="round"/>')
    out.append(f'<ellipse cx="{cx}" cy="{horizon}" rx="170" ry="34" fill="url(#haze)"/>')
    # rear-view mirror: stem + rounded body, crisp road behind
    mx, my, mw, mh = 450, 172, 220, 74
    out.append(f'<line x1="{mx}" y1="108" x2="{mx}" y2="{my - mh / 2}" stroke="{GOLD}" stroke-opacity=".7" stroke-width="2"/>')
    out.append(f'<defs><clipPath id="mirror"><rect x="{mx - mw / 2}" y="{my - mh / 2}" width="{mw}" height="{mh}" rx="30"/></clipPath>'
               f'<radialGradient id="haze"><stop offset="0" stop-color="#0f0f0f" stop-opacity=".0"/>'
               f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    out.append(f'<rect x="{mx - mw / 2}" y="{my - mh / 2}" width="{mw}" height="{mh}" rx="30" fill="#000" fill-opacity=".25" '
               f'stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.6"/>')
    clip = ' clip-path="url(#mirror)"'
    mh_y = my - 8
    out.append(f'<line x1="{mx - mw / 2}" y1="{mh_y}" x2="{mx + mw / 2}" y2="{mh_y}" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1"{clip}/>')
    road(out, mx, mh_y, my + mh / 2 + 2, 70, clip, False, 6, 0.95, 0.95)
    # tiny labels
    for x, y, lab in [(mx, my + mh / 2 + 22, "BEHIND"), (cx, 496, "AHEAD")]:
        out.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Inter" font-size="12" '
                   f'letter-spacing="4" fill="#8a8578">{lab}</text>')
    return "".join(out)
