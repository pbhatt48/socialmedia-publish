"""Two cliffs and a gorge: strata of knowledge and judgment on the near side, a single bridge of courage across."""
import random

GOLD = "#c9a96a"

def build():
    rnd = random.Random(20)
    out = []
    g = 400  # ground line
    # horizon / ground line on both sides of the gorge
    out.append(f'<line x1="40" y1="{g}" x2="360" y2="{g}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1"/>')
    out.append(f'<line x1="560" y1="{g}" x2="860" y2="{g}" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1"/>')
    # left cliff face with strata
    out.append(f'<path d="M360,{g} L372,{g+30} L366,{g+62} L380,{g+96}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.2" fill="none"/>')
    out.append(f'<path d="M560,{g} L548,{g+34} L556,{g+70} L540,{g+96}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.2" fill="none"/>')
    # gorge floor hints
    for i in range(5):
        y = g + 70 + i * 6
        out.append(f'<line x1="{400+i*8}" y1="{y}" x2="{520-i*8}" y2="{y}" stroke="{GOLD}" stroke-opacity="{.06+i*.02:.2f}" stroke-width=".8"/>')
    # stacked foundation blocks on the left: knowledge (wide), judgment (narrower)
    def course(y, x0, x1, h, alpha):
        out.append(f'<rect x="{x0}" y="{y-h}" width="{x1-x0}" height="{h}" fill="none" stroke="{GOLD}" stroke-opacity="{alpha}" stroke-width="1.2"/>')
        x = x0 + rnd.uniform(30, 50)
        while x < x1 - 20:
            out.append(f'<line x1="{x:.1f}" y1="{y-h}" x2="{x:.1f}" y2="{y}" stroke="{GOLD}" stroke-opacity="{alpha*.6:.2f}" stroke-width=".8"/>')
            x += rnd.uniform(38, 60)
    course(g, 120, 360, 44, .75)
    course(g - 44, 170, 360, 40, .85)
    out.append(f'<text x="140" y="{g-16}" font-family="Inter" font-size="12" letter-spacing="3" fill="#8a8578">KNOWLEDGE</text>')
    out.append(f'<text x="186" y="{g-58}" font-family="Inter" font-size="12" letter-spacing="3" fill="#8a8578">JUDGMENT</text>')
    # bridge of courage: arch from top of foundation across the gorge
    top = g - 84
    out.append(f'<path d="M360,{top} Q460,{top-70} 560,{g}" stroke="{GOLD}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    out.append(f'<path d="M360,{top+8} Q460,{top-58} 560,{g+8}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1" fill="none"/>')
    # suspension verticals
    for i in range(1, 10):
        t = i / 10
        x = (1-t)**2*360 + 2*(1-t)*t*460 + t*t*560
        y = (1-t)**2*top + 2*(1-t)*t*(top-70) + t*t*g
        out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y+10:.1f}" stroke="{GOLD}" stroke-opacity=".5" stroke-width=".8"/>')
    out.append(f'<text x="460" y="{top-58}" text-anchor="middle" font-family="Inter" font-size="12" letter-spacing="3" fill="#8a8578">COURAGE</text>')
    # far side: a small marker of value reached
    out.append(f'<circle cx="700" cy="{g-40}" r="34" fill="url(#glow)"/>')
    out.append(f'<circle cx="700" cy="{g-40}" r="9" fill="{GOLD}"/>')
    out.append(f'<circle cx="700" cy="{g-40}" r="18" fill="none" stroke="{GOLD}" stroke-opacity=".4"/>')
    out.append(f'<line x1="700" y1="{g-22}" x2="700" y2="{g}" stroke="{GOLD}" stroke-opacity=".5"/>')
    out.append(f'<text x="700" y="{g+34}" text-anchor="middle" font-family="Inter" font-size="12" letter-spacing="3" fill="#8a8578">VALUE</text>')
    # faint stars / sky dots
    for _ in range(14):
        x, y = rnd.uniform(80, 820), rnd.uniform(70, 220)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(.8,1.6):.1f}" fill="{GOLD}" fill-opacity="{rnd.uniform(.15,.45):.2f}"/>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
