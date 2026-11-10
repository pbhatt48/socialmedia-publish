"""Volatility vs. risk: a jagged price path that swings wildly yet trends up, beside
a smooth line that slowly sinks below the ground (permanent loss). 900x520 viewBox."""
import math, random

GOLD = "#c9a96a"

def build():
    out = []
    ground = 400
    out.append(f'<line x1="40" y1="{ground}" x2="860" y2="{ground}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1"/>')
    # faint grid of value levels
    for y in (130, 200, 270, 340):
        out.append(f'<line x1="70" y1="{y}" x2="830" y2="{y}" stroke="{GOLD}" stroke-opacity=".08" stroke-width="1"/>')
    rnd = random.Random(14)
    x0, x1 = 80, 820
    n = 120
    pts = []
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        trend = 330 - 200 * t ** 1.15
        swing = 34 * math.sin(t * 17) + 18 * math.sin(t * 41 + 1.3) + rnd.uniform(-12, 12)
        pts.append((x, trend + swing))
    # underlying value: a calm dashed line beneath the noise
    vals = " ".join(f"L{x0 + (x1 - x0) * i / 40:.1f},{330 - 200 * (i / 40) ** 1.15:.1f}" for i in range(41))
    out.append(f'<path d="M{vals[1:]}" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1.4" '
               f'stroke-dasharray="3 6" fill="none" stroke-linecap="round"/>')
    # the volatile price path
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    out.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".9" stroke-width="1.5" fill="none" stroke-linejoin="round"/>')
    # soft glow at the end
    ex, ey = pts[-1]
    out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="26" fill="url(#glow)"/>')
    out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="3.5" fill="{GOLD}"/>')
    # the "safe-looking" smooth line that quietly erodes (purchasing power)
    sm = " ".join(f"L{x0 + (x1 - x0) * i / 40:.1f},{330 + 55 * (i / 40) ** 1.4:.1f}" for i in range(41))
    out.append(f'<path d="M{sm[1:]}" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1.2" fill="none"/>')
    sx, sy = x1, 330 + 55
    out.append(f'<circle cx="{sx}" cy="{sy}" r="3" fill="none" stroke="{GOLD}" stroke-opacity=".5"/>')
    # tiny labels
    lab = 'font-family="Inter" font-size="12" letter-spacing="3" fill="#8a8578"'
    out.append(f'<text x="{ex - 14:.1f}" y="{ey - 22:.1f}" text-anchor="end" {lab}>STOCKS</text>')
    out.append(f'<text x="{sx - 14}" y="{sy - 12}" text-anchor="end" {lab}>CASH</text>')
    for tx in (x0, (x0 + x1) / 2, x1):
        out.append(f'<line x1="{tx}" y1="{ground + 6}" x2="{tx}" y2="{ground + 14}" stroke="{GOLD}" stroke-opacity=".5"/>')
    out.append(f'<text x="{x0}" y="{ground + 40}" text-anchor="middle" {lab}>YEAR 1</text>')
    out.append(f'<text x="{(x0 + x1) / 2}" y="{ground + 40}" text-anchor="middle" {lab}>10</text>')
    out.append(f'<text x="{x1}" y="{ground + 40}" text-anchor="middle" {lab}>20</text>')
    defs = (f'<defs><radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".45"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient></defs>')
    return defs + "".join(out)
