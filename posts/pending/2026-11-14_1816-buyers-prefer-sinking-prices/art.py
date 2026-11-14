"""Sinking price, rising accumulation: a steady buyer gets more shares as prices fall. 900x520 viewBox."""
import math

GOLD = "#c9a96a"
GREY = "#8a8578"

def build():
    out = []
    ground = 430
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    cols = [130, 250, 370, 490, 610, 730]
    prices = [330, 300, 255, 220, 185, 160]   # height of price line above ground
    # price path (sinking), smooth with gentle wiggle
    pts = [(x, ground - p) for x, p in zip(cols, prices)]
    d = f"M{70},{ground-345} "
    prev = (70, ground - 345)
    for i, (x, y) in enumerate(pts):
        wob = 10 if i % 2 == 0 else -8
        d += f"Q{(prev[0]+x)/2:.1f},{(prev[1]+y)/2 + wob:.1f} {x},{y} "
        prev = (x, y)
    d += f"Q{780},{ground-152} {830},{ground-148}"
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".9" stroke-width="2" fill="none" stroke-linecap="round"/>')
    # price points
    for x, y in pts:
        out.append(f'<circle cx="{x}" cy="{y}" r="3.2" fill="{GOLD}"/>')
        out.append(f'<line x1="{x}" y1="{y+8}" x2="{x}" y2="{ground-6}" stroke="{GOLD}" stroke-opacity=".14" stroke-width="1" stroke-dasharray="2 5"/>')
    # same budget buys more shares as price sinks: stacks of share tokens
    budget = 330 * 6
    for x, p in zip(cols, prices):
        n = round(budget / p)  # 6 .. 12
        for k in range(n):
            cy = ground - 9 - k * 11
            a = 0.35 + 0.55 * (k / 12)
            out.append(f'<rect x="{x-14}" y="{cy-4.5}" width="28" height="9" rx="4.5" fill="none" '
                       f'stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="1.2"/>')
    # labels
    out.append(f'<text x="70" y="{ground-365}" font-family="Inter" font-size="12" letter-spacing="3" fill="{GREY}">PRICE</text>')
    out.append(f'<text x="830" y="{ground+38}" text-anchor="end" font-family="Inter" font-size="12" letter-spacing="3" fill="{GREY}">SAME DOLLARS, MORE SHARES</text>')
    for x in cols:
        out.append(f'<line x1="{x}" y1="{ground+5}" x2="{x}" y2="{ground+12}" stroke="{GOLD}" stroke-opacity=".5"/>')
    return "".join(out)
