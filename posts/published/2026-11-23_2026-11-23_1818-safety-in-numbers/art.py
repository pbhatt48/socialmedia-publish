"""Many columns carry one beam; one has failed, the structure still stands: safety in numbers.
Returns SVG inner markup for a 900x520 viewBox."""
GOLD = "#c9a96a"

def build():
    out = []
    ground = 420
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    left, right, top = 150, 750, 190
    # entablature / beam
    out.append(f'<rect x="{left-30}" y="{top-34}" width="{right-left+60}" height="22" fill="none" stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.6"/>')
    out.append(f'<line x1="{left-30}" y1="{top-40}" x2="{right+30}" y2="{top-40}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1"/>')
    out.append(f'<path d="M{left-40},{top-46} L450,{top-110} L{right+40},{top-46} Z" fill="none" stroke="{GOLD}" stroke-opacity=".7" stroke-width="1.4"/>')
    out.append(f'<path d="M{left+10},{top-52} L450,{top-96} L{right-10},{top-52}" fill="none" stroke="{GOLD}" stroke-opacity=".25" stroke-width="1"/>')
    # stylobate steps
    for i, op in enumerate((.6, .45, .3)):
        y = ground - 8 * (3 - i)
        out.append(f'<line x1="{left-30-12*i}" y1="{y}" x2="{right+30+12*i}" y2="{y}" stroke="{GOLD}" stroke-opacity="{op}" stroke-width="1.2"/>')
    base = ground - 24
    n = 9
    broken = 5
    for i in range(n):
        x = left + (right - left) * i / (n - 1)
        w = 13
        cap = f'<rect x="{x-w-5}" y="{top-12}" width="{2*w+10}" height="8" fill="{GOLD}" fill-opacity=".55"/>'
        foot = f'<rect x="{x-w-4}" y="{base-7}" width="{2*w+8}" height="7" fill="{GOLD}" fill-opacity=".55"/>'
        if i == broken:
            out.append(foot)
            out.append(f'<rect x="{x-w-5}" y="{top-12}" width="{2*w+10}" height="8" fill="{GOLD}" fill-opacity=".3"/>')
            # lower stump with jagged break
            out.append(f'<path d="M{x-w},{base-7} L{x-w},{base-70} L{x-5},{base-82} L{x+3},{base-72} L{x+w},{base-90} L{x+w},{base-7}" '
                       f'fill="none" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.4" stroke-linejoin="round"/>')
            # hanging upper fragment
            out.append(f'<path d="M{x-w},{top-4} L{x-w},{top+48} L{x-3},{top+40} L{x+6},{top+56} L{x+w},{top+44} L{x+w},{top-4}" '
                       f'fill="none" stroke="{GOLD}" stroke-opacity=".4" stroke-width="1.3" stroke-linejoin="round"/>')
            # fallen drum on ground
            out.append(f'<rect x="{x+38}" y="{base-18}" width="44" height="18" rx="2" transform="rotate(-6 {x+60} {base-9})" '
                       f'fill="none" stroke="{GOLD}" stroke-opacity=".4" stroke-width="1.2"/>')
            continue
        out.append(cap + foot)
        out.append(f'<rect x="{x-w}" y="{top-4}" width="{2*w}" height="{base-7-top+4}" fill="none" stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.5"/>')
        for f in (-6, 0, 6):
            out.append(f'<line x1="{x+f}" y1="{top+6}" x2="{x+f}" y2="{base-16}" stroke="{GOLD}" stroke-opacity=".28" stroke-width="1"/>')
    out.append(f'<text x="450" y="{ground+42}" text-anchor="middle" font-family="Inter" font-size="13" letter-spacing="4" fill="#8a8578">ONE FAILS · THE ROOF HOLDS</text>')
    return "".join(out)
