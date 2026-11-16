"""Two investments: a high IRR held briefly vs a lower IRR compounded for years. Profit in coins."""
GOLD = "#c9a96a"
GREY = "#8a8578"

def stack(out, cx, ground, n, alpha):
    rx, ry, h = 46, 11, 13
    for i in range(n):
        y = ground - 10 - i * h
        a = alpha * (0.55 + 0.45 * (i + 1) / n)
        out.append(f'<path d="M{cx-rx},{y-h+3} L{cx-rx},{y} A{rx},{ry} 0 0 0 {cx+rx},{y} L{cx+rx},{y-h+3} Z" fill="#17181b"/>')
        out.append(f'<path d="M{cx-rx},{y} v{-h+3} M{cx+rx},{y} v{-h+3}" stroke="{GOLD}" stroke-opacity="{a*0.7:.2f}" stroke-width="1"/>')
        out.append(f'<path d="M{cx-rx},{y} A{rx},{ry} 0 0 0 {cx+rx},{y}" stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="1.2" fill="none"/>')
        out.append(f'<ellipse cx="{cx}" cy="{y-h+3}" rx="{rx}" ry="{ry}" stroke="{GOLD}" stroke-opacity="{a:.2f}" stroke-width="1.2" fill="#17181b"/>')
    top = ground - 10 - (n - 1) * h - h + 3
    return top

def build():
    out = []
    ground = 430
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # left: 40% for one year -> $40 profit on $100 (2 coins of $20)
    lx, rx = 250, 640
    t1 = stack(out, lx, ground, 2, 0.95)
    # right: 18% for eight years -> ~$276 profit (14 coins)
    t2 = stack(out, rx, ground, 14, 0.9)
    # time spans
    out.append(f'<path d="M{lx-70},{ground+18} h140" stroke="{GOLD}" stroke-opacity=".5"/>')
    out.append(f'<path d="M{rx-170},{ground+18} h340" stroke="{GOLD}" stroke-opacity=".5"/>')
    for x in (lx-70, lx+70, rx-170, rx+170):
        out.append(f'<line x1="{x}" y1="{ground+13}" x2="{x}" y2="{ground+23}" stroke="{GOLD}" stroke-opacity=".5"/>')
    for x in range(rx-170, rx+171, 340//8):
        out.append(f'<circle cx="{x}" cy="{ground+18}" r="1.6" fill="{GOLD}" fill-opacity=".55"/>')
    labels = [(lx, ground + 50, "40% IRR · 1 YEAR"), (rx, ground + 50, "18% IRR · 8 YEARS"),
              (lx, t1 - 40, "+$40"), (rx, t2 - 26, "+$276")]
    for x, y, s in labels:
        out.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Inter" font-size="13" letter-spacing="3" fill="{GREY}">{s}</text>')
    out.append(f'<text x="450" y="{ground+80}" text-anchor="middle" font-family="Inter" font-size="11" letter-spacing="3" fill="{GREY}" fill-opacity=".8">PROFIT ON $100 INVESTED</text>')
    return "".join(out)
