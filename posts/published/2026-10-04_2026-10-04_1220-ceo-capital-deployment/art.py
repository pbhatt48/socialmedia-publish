"""Ten years of retained earnings stacked on the original capital: by year 10, ~61% of the capital is newly deployed.
Returns SVG inner markup for a 900x520 viewBox."""

GOLD = "#c9a96a"

def build():
    out = []
    ground = 420
    h0 = 132.0
    x0, step, w = 110, 66, 30
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    tops = []
    for yr in range(11):
        cx = x0 + yr * step
        x = cx - w / 2
        total = h0 * 1.1 ** yr
        top = ground - total
        base_top = ground - h0
        tops.append((cx, top))
        # original capital: faint outline
        out.append(f'<rect x="{x:.1f}" y="{base_top:.1f}" width="{w}" height="{h0:.1f}" fill="none" '
                   f'stroke="{GOLD}" stroke-opacity=".32" stroke-width="1"/>')
        # retained earnings, one layer per year, brighter as they accumulate
        for k in range(1, yr + 1):
            lo = ground - h0 * 1.1 ** (k - 1)
            hi = ground - h0 * 1.1 ** k
            a = 0.35 + 0.5 * k / 10
            out.append(f'<rect x="{x:.1f}" y="{hi:.1f}" width="{w}" height="{lo - hi:.1f}" fill="{GOLD}" '
                       f'fill-opacity="{a * 0.18:.2f}" stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="1"/>')
        out.append(f'<line x1="{cx}" y1="{ground + 6}" x2="{cx}" y2="{ground + 14}" stroke="{GOLD}" stroke-opacity=".5"/>')
        lab = "YEAR 0" if yr == 0 else str(yr)
        out.append(f'<text x="{cx}" y="{ground + 40}" text-anchor="middle" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="#8a8578">{lab}</text>')
    # dotted growth curve over the tops
    d = "M" + " L".join(f"{cx},{top - 10:.1f}" for cx, top in tops)
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1.2" stroke-dasharray="2 7" fill="none" stroke-linecap="round"/>')
    # bracket on final column marking the newly deployed share
    cx, top = tops[-1]
    bx = cx + w / 2 + 14
    mid = ground - h0
    out.append(f'<path d="M{bx - 6},{top:.1f} L{bx},{top:.1f} L{bx},{mid:.1f} L{bx - 6},{mid:.1f}" stroke="{GOLD}" '
               f'stroke-opacity=".7" stroke-width="1" fill="none"/>')
    out.append(f'<text x="{bx + 10}" y="{(top + mid) / 2 + 5:.1f}" font-family="Inter" font-size="13" letter-spacing="3" fill="{GOLD}">61%</text>')
    out.append(f'<text x="{bx + 10}" y="{(top + mid) / 2 + 23:.1f}" font-family="Inter" font-size="10" letter-spacing="2" fill="#8a8578">NEW</text>')
    return "".join(out)
