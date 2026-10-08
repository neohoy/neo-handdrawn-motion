#!/usr/bin/env python3
"""c1-grow-up / c2-grow-up — 「原来我们都在这里长大」 (chorus 1 and 2, last line).

A wooden door frame used as a growth chart. The two friends stand in it and grow on the downbeats
(kid → teen → grown-up, drawing swaps with a squash), a pencil mark + year is drawn at each new height;
the line writes across the top and 长大 slams in big and red.
Usage: HD_CUT=full python3 full_grow.py 1|2
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scene import *  # noqa: E402,F401,F403
from hd_props import *  # noqa: E402,F401,F403
from local.hsinchu import *  # noqa: E402,F401,F403

N = int(sys.argv[1]) if len(sys.argv) > 1 else 1
LI = 19 if N == 1 else 35
sc = Scene(f"c{N}-grow-up", f"gr{N}", YEL)
FLOOR = 1000
FX = 600
STAGES = [(66, .6), (78, 1.0), (88, 1.3)]          # head radius, leg length
YEARS = ["2008", "2014", "2026"] if N == 1 else ["2010", "2018", "2026"]
db = music.downbeats(sc.g0 - .05, sc.g1)
SW = [sc.g0, db[1] if len(db) > 1 else sc.g0 + 2.4, (db[1] if len(db) > 1 else sc.g0 + 2.4) + 1.21]   # stage swap times (global)

people, marks = "", ""
TOPS = []
for k, (r, legs) in enumerate(STAGES):
    cy = FLOOR - r * (2.9 + 1.5 * legs)
    pa = pro_front(FX - 118, cy, r, "happy" if k == 2 else "open", "laugh" if k == 2 else "smile", WHITE, legs, .4)
    fr = friend_front(FX + 118, cy + 6, r * .96, "happy" if k == 2 else "open", "smile", PINK, legs * .96, .4)
    people += sc.group(f"st{k}", pa + fr, op=0)
    top = round(cy - r * 1.5)
    TOPS.append(top)
    marks += (f'<path id="{sc.id(f"mk{k}")}" d="M{FX - 276},{top} L{FX - 206},{top}" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" '
              f'fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
              + sc.group(f"yr{k}", T(FX - 350, top + 11, YEARS[k], 34, "JBM", INK, "middle", allow=True), op=0))

wall = (f'<rect width="1920" height="{FLOOR}" fill="{YEL}"/>'
        + "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{FLOOR}" stroke="#E9C230" stroke-width="18"/>' for x in range(40, 1920, 120))
        + f'<rect x="0" y="{FLOOR}" width="1920" height="{1080 - FLOOR}" fill="{WOOD}"/><line x1="0" y1="{FLOOR}" x2="1920" y2="{FLOOR}" stroke="{INK}" stroke-width="{LW}"/>')
# wall decor: a framed photo of the two at the sea, a wall clock, a potted bamboo
deco = (f'<g transform="rotate(4 1640 330)"><rect x="1490" y="200" width="300" height="250" fill="{WOOD}" stroke="{INK}" stroke-width="{LW}"/>'
        f'<rect x="1514" y="224" width="252" height="202" fill="{PINK}" stroke="{INK}" stroke-width="5"/>'
        f'<circle cx="1600" cy="350" r="44" fill="{ORANGE}" stroke="{INK}" stroke-width="5"/>'
        f'<rect x="1514" y="350" width="252" height="76" fill="{TEAL}" stroke="{INK}" stroke-width="5"/>'
        + friends_back(1660, 400, .34) + "</g>"
        + clock(1150, 300, 70)
        + f'<path d="M1790,1000 L1770,900 L1890,900 L1870,1000Z" fill="{ORANGE}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>'
        + stalk("M1830,905 C1834,800 1826,700 1812,620", [(1832, 820, 0), (1824, 720, -4)], 22) + leaf(1780, 640, 80, 200) + leaf(1860, 700, 70, -20))
L = music.line(LI)
top_line, top_org = sc.chars("c", L["text"][:8], 960, 170, 96, "WK", INK)
big, big_org = sc.chars("b", "长大", 1400, 800, 300, "KL", RED, adv=1.0, stroke=INK, sw=18, shadow=12)
spk = "".join(sc.group(f"sp{i}", sparkle(x, y, s, WHITE), op=0) for i, (x, y, s) in enumerate([(1130, 520, 30), (1660, 520, 24), (1720, 860, 20), (1100, 880, 18)]))
leaves = "".join(sc.group(f"lf{i}", leaf(2000, y, 90, 200 + i * 7)) for i, y in enumerate((300, 620, 860)))

body = (wall
        + sc.wob(door_frame(FX, FLOOR, 790, 560) + marks + people
                 + deco + leaves)
        + sc.wobT(top_line + big + spk)
        + sc.grain(.45) + tag(*sc.page(), INK))

syl = music.syllables(LI)
sc.pop_chars("c", top_org, syl[:8])
J = [sc.L(t) for t in syl[8:]]
sc.js += [
    # growth: drawing swaps with a squash from the feet, a pencil mark at each new height
    *[f'tl.set("#{sc.id(f"st{k}")}", {{ opacity: 1 }}, {sc.L(t)});' for k, t in enumerate(SW)],
    *[f'tl.set("#{sc.id(f"st{k}")}", {{ opacity: 0 }}, {sc.L(SW[k + 1])});' for k in range(2)],
    *[f'tl.fromTo("#{sc.id(f"st{k}")}", {{ scaleY: 0.82, scaleX: 1.12, svgOrigin: "{FX} {FLOOR}" }}, {{ scaleY: 1, scaleX: 1, duration: 0.25, ease: q("back.out(2.6)", 0.25) }}, {sc.L(t)});' for k, t in enumerate(SW)],
    *[f'drawOn("#{sc.id(f"mk{k}")}", {sc.L(t) + 0.15:.3f}, 0.25);' for k, t in enumerate(SW)],
    *[f'pop("#{sc.id(f"yr{k}")}", {sc.L(t) + 0.3:.3f}, "{FX - 350} {TOPS[k]}", 0.2, "back.out(2)", 0);' for k, t in enumerate(SW)],
    # 长大 slams in, squash + sparkles
    *[f'tl.fromTo("#{sc.id(f"b{i}")}", {{ opacity: 0, scaleX: 0.6, scaleY: 1.5, y: -120, svgOrigin: "{o[0]} {o[1] + 110}" }}, {{ opacity: 1, scaleX: 1, scaleY: 1, y: 0, duration: 0.25, ease: q("back.out(2.4)", 0.25) }}, {J[i]});'
      for i, o in enumerate(big_org)],
    *[f'pop("#{sc.id(f"sp{i}")}", {J[1] + 0.1 + i * 0.07:.3f}, "{x} {y}", 0.2, "back.out(3)", 30);' for i, (x, y) in enumerate([(1130, 520), (1660, 520), (1720, 860), (1100, 880)])],
    *[f'tl.fromTo("#{sc.id(f"lf{i}")}", {{ x: 0, rotation: 0, svgOrigin: "2000 {y}" }}, {{ x: -2300, rotation: -280, duration: 1.6, ease: q("none", 1.6) }}, {0.3 + i * 1.3});' for i, y in enumerate((300, 620, 860))],
]
sc.write(body)
