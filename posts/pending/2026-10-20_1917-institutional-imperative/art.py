"""A precarious, leaning tower propped up by a crowd of struts, each anchored on a small
rate-of-return study: analysis recruited to support a foolish craving. 900x520 viewBox."""
import math

GOLD = "#c9a96a"


def build():
    out = []
    ground = 430
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')

    # Leaning tower of stacked blocks, each slightly more askew.
    bx, by = 450, ground
    lean = 0.0
    tops = []
    for i in range(9):
        w = 74 - i * 4
        h = 38
        lean += 0.035 + i * 0.006
        cx, cy = bx + math.sin(lean) * h / 2, by - math.cos(lean) * h / 2
        deg = math.degrees(lean)
        op = 0.95 - i * 0.05
        out.append(f'<rect x="{-w/2:.1f}" y="{-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" '
                   f'transform="translate({cx:.1f},{cy:.1f}) rotate({deg:.2f})" fill="none" '
                   f'stroke="{GOLD}" stroke-opacity="{op:.2f}" stroke-width="1.4"/>')
        tops.append((cx, cy, w, lean))
        bx, by = bx + math.sin(lean) * h, by - math.cos(lean) * h

    # Small flag on top: the leader's craving.
    out.append(f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{bx+8:.1f}" y2="{by-46:.1f}" stroke="{GOLD}" stroke-width="1.3"/>'
               f'<path d="M{bx+8:.1f},{by-46:.1f} l30,7 l-27,9 Z" fill="{GOLD}" fill-opacity=".8"/>')

    # Struts from small "studies" on the ground to the tower's flanks.
    feet = [130, 190, 250, 305, 360, 560, 620, 680, 740, 800]
    for j, fx in enumerate(feet):
        k = 2 + (j * 3) % 7
        cx, cy, w, ln = tops[k]
        side = -1 if fx < 450 else 1
        ax = cx + side * (w / 2) * math.cos(ln)
        ay = cy + side * (w / 2) * math.sin(ln)
        op = 0.25 + 0.05 * (j % 4)
        out.append(f'<line x1="{fx}" y1="{ground-24}" x2="{ax:.1f}" y2="{ay:.1f}" stroke="{GOLD}" '
                   f'stroke-opacity="{op:.2f}" stroke-width="0.9"/>')
        # The study: a tiny document with an upward-sloping chart line.
        out.append(f'<rect x="{fx-11}" y="{ground-24}" width="22" height="24" fill="#0f0f0f" fill-opacity=".0" '
                   f'stroke="{GOLD}" stroke-opacity=".6" stroke-width="0.9"/>'
                   f'<polyline points="{fx-7},{ground-5} {fx-2},{ground-10} {fx+2},{ground-8} {fx+7},{ground-19}" '
                   f'fill="none" stroke="{GOLD}" stroke-opacity=".85" stroke-width="1"/>')

    out.append(f'<text x="450" y="{ground+42}" text-anchor="middle" font-family="Inter" font-size="13" '
               f'letter-spacing="3" fill="#8a8578">SUPPORTING STUDIES</text>')
    return "".join(out)
