#!/usr/bin/env python3
"""s11-park-night (87.24–96.52) — verse 2, four quick lines → a four-panel comic page, one panel per line.

1 科学园区的楼还没暗      the office block still lit at night
2 咖啡杯映着凌晨的答案    a coffee cup reflecting a 3 o'clock clock face, steam
3 有人赶着简报和预算      laptop bar chart climbing, papers flying off in the wind
4 有人想念宿舍门前的晚安  the dorm door, a 晚安 note taped on it, the cat asleep
Each panel slams in (overshoot + tilt) just before its line; the caption writes glyph by glyph.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scene import *  # noqa: E402,F401,F403
from hd_props import *  # noqa: E402,F401,F403
from local.hsinchu import *  # noqa: E402,F401,F403

sc = Scene("s11-park-night", "s11", NIGHT)
PW, PH = 900, 470
PANELS = [(40, 40), (980, 40), (40, 570), (980, 570)]
LINES = [20, 21, 22, 23]
defs_ = ""
for k, (x, y) in enumerate(PANELS):
    defs_ += f'<clipPath id="s11-pc{k}"><rect x="{x}" y="{y}" width="{PW}" height="{PH}"/></clipPath>'
sc.extra_defs = defs_


def p1(x, y):
    tw, wins = glass_tower(x + 300, x + 640, y + 130, y + PH + 20, "s11p1", 5)
    lit = tw.replace(' opacity="0"', "")
    return (f'<rect x="{x}" y="{y}" width="{PW}" height="{PH}" fill="{NIGHT}"/>' + moon(x + 790, y + 110, 46) + sparkle(x + 120, y + 90, 12) + sparkle(x + 220, y + 200, 9)
            + lit + f'<rect x="{x + 690}" y="{y + 300}" width="160" height="200" fill="#26306A" stroke="{INK}" stroke-width="{LW}"/>')


def p2(x, y):
    steam = "".join(f'<path id="s11-cs{i}" d="M{x + 400 + i * 90},{y + 150} c-30,-30 30,-60 0,-90 c-30,-30 20,-50 0,-80" fill="none" stroke="{WHITE}" stroke-width="8" stroke-linecap="round" opacity=".85"/>' for i in range(3))
    return (f'<rect x="{x}" y="{y}" width="{PW}" height="{PH}" fill="{ORANGE}"/>'
            + coffee_cup(x + 490, y + 250, .95, "s11") + steam)


def p3(x, y):
    papers = "".join(f'<g id="s11-pp{i}"><rect x="{x + 760}" y="{y + 120 + i * 90}" width="90" height="116" fill="{WHITE}" stroke="{INK}" stroke-width="5" transform="rotate({-10 + i * 12} {x + 805} {y + 178 + i * 90})"/>'
                     f'<line x1="{x + 772}" y1="{y + 150 + i * 90}" x2="{x + 836}" y2="{y + 150 + i * 90}" stroke="{INK}" stroke-width="4" opacity=".4"/></g>' for i in range(3))
    return (f'<rect x="{x}" y="{y}" width="{PW}" height="{PH}" fill="#2F4F7A"/>'
            + f'<rect x="{x}" y="{y + 380}" width="{PW}" height="100" fill="{WOOD}" stroke="{INK}" stroke-width="{LW}"/>'
            + laptop(x + 400, y + 390, .95, "s11") + papers)


def p4(x, y):
    return (f'<rect x="{x}" y="{y}" width="{PW}" height="{PH}" fill="{PLUM}"/>'
            + f'<rect x="{x}" y="{y + 400}" width="{PW}" height="80" fill="#2A2238"/>'
            + dorm_door(x + 330, y + 440, .6, "312")
            + note_paper(x + 330, y + 200, .7, "晚安", -6)
            + cat(x + 650, y + 410, .9)
            + T(x + 600, y + 260, "z", 36, "JBM", WHITE, "middle", allow=True) + T(x + 630, y + 220, "z", 48, "JBM", WHITE, "middle", allow=True))


ART = [p1, p2, p3, p4]
panels, caps, ORG = "", "", []
for k, (x, y) in enumerate(PANELS):
    art = ART[k](x, y)
    frame = (f'<rect x="{x + 12}" y="{y + 14}" width="{PW}" height="{PH}" fill="{INK}"/>'
             f'<g clip-path="url(#s11-pc{k})">{art}</g>'
             f'<rect x="{x}" y="{y}" width="{PW}" height="{PH}" fill="none" stroke="{INK}" stroke-width="12"/>')
    panels += f'<g id="s11-p{k}" opacity="0">{frame}</g>'
    L = music.line(LINES[k])
    n = len(L["text"])
    w = n * 48 + 70
    cx = x + 30 + w / 2
    cy = y + PH - 40
    cap_chars, org = sc.chars(f"c{k}_", L["text"], round(cx), round(cy + 16), 48, "WK", INK)
    caps += f'<g id="s11-cap{k}" opacity="0">{label(x + 30, y + PH - 92, w, 80, "", PAPER if k != 1 else WHITE, -1)}</g>' + cap_chars
    ORG.append(org)

body = (f'<rect width="1920" height="1080" fill="{NIGHT}"/>'
        + "".join(sparkle(x, y, s) for x, y, s in [(960, 540, 18), (20, 540, 10), (1900, 30, 10)])
        + sc.wob(panels) + sc.wobT(caps)
        + sc.grain(.35) + tag(*sc.page(), WHITE)
        + sc.band("bin", "#3A4A9C", YEL) + sc.band("out", TEAL, WHITE))
sc.band_out("bin")
js = []
for k, (x, y) in enumerate(PANELS):
    L = music.line(LINES[k])
    t = sc.L(L["start"]) - 0.28
    o = f"{x + PW / 2:.0f} {y + PH / 2:.0f}"
    js.append(f'tl.fromTo("#s11-p{k}", {{ opacity: 0, scale: 1.25, rotation: {(-5, 4, 3, -4)[k]}, svgOrigin: "{o}" }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.2, ease: q("back.out(2)", 0.2) }}, {max(0.0, t):.2f});')
    js.append(f'pop("#s11-cap{k}", {max(0.0, t) + 0.15:.2f}, "{x + 200} {y + PH - 52}", 0.2, "back.out(2)", -4);')
    sc.pop_chars(f"c{k}_", ORG[k], music.syllables(LINES[k], .75))
js += [
    *[f'jitter("#s11-cs{i}", {sc.L(89.3) + i * 0.08:.2f}, {sc.dur}, 1 / 6, [{{ y: 0, opacity: 0.85 }}, {{ y: -10, opacity: 0.6 }}, {{ y: -20, opacity: 0.3 }}]);' for i in range(3)],
    *[f'tl.fromTo("#s11-bar{i}", {{ scaleY: 0, transformOrigin: "50% 100%" }}, {{ scaleY: 1, duration: 0.17, ease: q("back.out(2)", 0.17) }}, {sc.L(92.04) + i * 0.3:.2f});' for i in range(5)],
    *[f'tl.to("#s11-pp{i}", {{ x: -900, y: {-120 + 60 * i}, rotation: -90, svgOrigin: "{820} {700 + i * 90}", duration: 0.8, ease: q("power1.in", 0.8) }}, {sc.L(92.6) + i * 0.3:.2f});' for i in range(3)],
]
sc.js += js
sc.band_in("out", sc.g1)
sc.write(body)
