"""Balanced beam scale: safety of principal weighed against adequate return. SVG inner markup for 900x520."""
GOLD = "#c9a96a"

def pan(out, cx, top, label):
    # three suspension cords converging on the beam end
    for dx in (-70, 0, 70):
        out.append(f'<line x1="{cx}" y1="{top}" x2="{cx+dx}" y2="{top+150}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1"/>')
    out.append(f'<path d="M{cx-86},{top+150} Q{cx},{top+205} {cx+86},{top+150} Z" fill="{GOLD}" fill-opacity=".08" '
               f'stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.6"/>')
    out.append(f'<circle cx="{cx}" cy="{top}" r="4" fill="{GOLD}"/>')
    out.append(f'<text x="{cx}" y="{top+238}" text-anchor="middle" font-family="Inter" font-size="13" '
               f'letter-spacing="3" fill="#8a8578">{label}</text>')

def build():
    out = []
    ground = 440
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    cx = 450
    beam_y = 110
    # base and column
    out.append(f'<path d="M{cx-70},{ground} L{cx-40},{ground-18} L{cx+40},{ground-18} L{cx+70},{ground} Z" fill="{GOLD}" fill-opacity=".15" stroke="{GOLD}" stroke-opacity=".8" stroke-width="1.2"/>')
    out.append(f'<line x1="{cx}" y1="{ground-18}" x2="{cx}" y2="{beam_y}" stroke="{GOLD}" stroke-opacity=".85" stroke-width="3"/>')
    out.append(f'<line x1="{cx-7}" y1="{ground-18}" x2="{cx-3}" y2="{beam_y+20}" stroke="{GOLD}" stroke-opacity=".25" stroke-width="1"/>')
    out.append(f'<line x1="{cx+7}" y1="{ground-18}" x2="{cx+3}" y2="{beam_y+20}" stroke="{GOLD}" stroke-opacity=".25" stroke-width="1"/>')
    # fulcrum and beam, perfectly level
    out.append(f'<path d="M{cx-14},{beam_y+14} L{cx},{beam_y-6} L{cx+14},{beam_y+14} Z" fill="{GOLD}"/>')
    out.append(f'<line x1="{cx-230}" y1="{beam_y}" x2="{cx+230}" y2="{beam_y}" stroke="{GOLD}" stroke-width="2.4" stroke-linecap="round"/>')
    # pointer at zero
    out.append(f'<line x1="{cx}" y1="{beam_y-6}" x2="{cx}" y2="{beam_y-48}" stroke="{GOLD}" stroke-width="1.4"/>')
    out.append(f'<path d="M{cx-34},{beam_y-40} A44,44 0 0 1 {cx+34},{beam_y-40}" stroke="{GOLD}" stroke-opacity=".4" fill="none" stroke-width="1"/>')
    for t in (-24, -12, 0, 12, 24):
        out.append(f'<line x1="{cx+t}" y1="{beam_y-50 + abs(t)*0.25}" x2="{cx+t}" y2="{beam_y-56 + abs(t)*0.25}" stroke="{GOLD}" stroke-opacity=".5"/>')
    pan(out, cx - 230, beam_y, "SAFETY OF PRINCIPAL")
    pan(out, cx + 230, beam_y, "ADEQUATE RETURN")
    # contents of pans: a solid block (principal) and a small stack of coins (return)
    lx, py = cx - 230, beam_y + 150
    out.append(f'<rect x="{lx-30}" y="{py-34}" width="60" height="38" fill="{GOLD}" fill-opacity=".2" stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.3"/>')
    out.append(f'<line x1="{lx-30}" y1="{py-34}" x2="{lx-18}" y2="{py-44}" stroke="{GOLD}" stroke-opacity=".6"/><line x1="{lx+30}" y1="{py-34}" x2="{lx+42}" y2="{py-44}" stroke="{GOLD}" stroke-opacity=".6"/>'
               f'<line x1="{lx-18}" y1="{py-44}" x2="{lx+42}" y2="{py-44}" stroke="{GOLD}" stroke-opacity=".6"/><line x1="{lx+42}" y1="{py-44}" x2="{lx+42}" y2="{py-6}" stroke="{GOLD}" stroke-opacity=".6"/>')
    rx = cx + 230
    for i in range(5):
        y = py - 2 - i * 8
        out.append(f'<ellipse cx="{rx + (i%2)*3 - 1}" cy="{y}" rx="26" ry="5" fill="#0f0f0f" fill-opacity=".0" stroke="{GOLD}" stroke-opacity="{.5 + i*.1:.2f}" stroke-width="1.2"/>')
    return "".join(out)
