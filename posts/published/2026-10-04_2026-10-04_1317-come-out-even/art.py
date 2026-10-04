"""Waiting to break even: a stock path sags and crawls back to its cost line,
while the same capital redeployed early compounds away above it."""
import math

GOLD = "#c9a96a"
GREY = "#8a8578"


def path(points):
    d = f"M{points[0][0]:.1f},{points[0][1]:.1f}"
    for x, y in points[1:]:
        d += f" L{x:.1f},{y:.1f}"
    return d


def build():
    out = []
    ground = 440
    x0, x1 = 90, 810
    cost_y = 250
    mistake_x = 250
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # break-even line
    out.append(f'<line x1="{x0}" y1="{cost_y}" x2="{x1}" y2="{cost_y}" stroke="{GOLD}" stroke-opacity=".4" '
               f'stroke-width="1" stroke-dasharray="3 7"/>')
    # held stock: drift down, long trough, slow recovery to cost
    held = []
    for i in range(181):
        t = i / 180
        x = x0 + (x1 - x0) * t
        dip = 130 * math.sin(math.pi * min(t / 0.92, 1)) ** 1.4
        wob = 6 * math.sin(t * 47) * math.sin(math.pi * t)
        held.append((x, cost_y + dip + wob))
    out.append(f'<path d="{path(held)}" stroke="{GOLD}" stroke-opacity=".9" stroke-width="2" fill="none" stroke-linejoin="round"/>')
    # redeployed capital from the moment the mistake was clear
    my = held[int((mistake_x - x0) / (x1 - x0) * 180)][1]
    alt = []
    for i in range(101):
        t = i / 100
        x = mistake_x + (x1 - mistake_x) * t
        y = my - (my - 70) * (math.exp(1.9 * t) - 1) / (math.exp(1.9) - 1)
        alt.append((x, y + 3 * math.sin(t * 31)))
    out.append(f'<path d="{path(alt)}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.4" fill="none" '
               f'stroke-dasharray="1 0"/>')
    # shaded gap = cost of self-indulgence
    gap = alt + [(x, y) for x, y in reversed(held) if x >= mistake_x]
    out.append(f'<path d="{path(gap)} Z" fill="{GOLD}" fill-opacity=".07"/>')
    # markers
    out.append(f'<circle cx="{x0}" cy="{cost_y}" r="4" fill="{GOLD}"/>')
    out.append(f'<circle cx="{mistake_x}" cy="{my:.1f}" r="4" fill="none" stroke="{GOLD}" stroke-width="1.4"/>')
    out.append(f'<line x1="{mistake_x}" y1="{my+10:.1f}" x2="{mistake_x}" y2="{ground}" stroke="{GOLD}" stroke-opacity=".3" stroke-dasharray="2 5"/>')
    out.append(f'<circle cx="{x1}" cy="{held[-1][1]:.1f}" r="3.5" fill="{GOLD}" fill-opacity=".8"/>')
    out.append(f'<circle cx="{x1}" cy="{alt[-1][1]:.1f}" r="3.5" fill="{GOLD}" fill-opacity=".6"/>')

    def label(x, y, s, anchor="middle"):
        out.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Inter" font-size="13" '
                   f'letter-spacing="3" fill="{GREY}">{s}</text>')
    label(x0, cost_y - 18, "COST", "start")
    label(mistake_x, ground + 30, "MISTAKE SEEN")
    label(x1 - 10, cost_y + 28, "EVEN", "end")
    label(x1 - 10, alt[-1][1] + 6, "REDEPLOYED", "end")
    return "".join(out)
