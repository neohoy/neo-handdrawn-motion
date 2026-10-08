#!/usr/bin/env python3
"""s02-dusk-gate (10.22–19.43) — 东门城的影子落在傍晚 / 机车穿过巷口的灯盏.

a 10.22–14.62  sunset over 东门城: the sun sinks, the gate's shadow stretches left across the plaza (on twos),
               the kid with a schoolbag walks past, birds cross; the line writes across the sky
b 14.62–19.43  blue hour in an arcaded alley: a string of lanterns; the two friends ride the scooter right → left
               and each lantern lights as they pass (snapped to half-beats); the line hangs on a vertical shop sign
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scene import *  # noqa: E402,F401,F403
from hd_props import *  # noqa: E402,F401,F403
from local.hsinchu import *  # noqa: E402,F401,F403

sc = Scene("s02-dusk-gate", "s02", ORANGE)
GB = 14.62

# ---------------------------------------------------------------- a · 东门城
GX, GY, GS = 900, 770, 1.6
sky = f'<rect width="1920" height="740" fill="{ORANGE}"/><rect y="520" width="1920" height="220" fill="#F6A85A"/>'
plaza = (f'<rect y="740" width="1920" height="340" fill="{BUFF}"/><line x1="0" y1="740" x2="1920" y2="740" stroke="{INK}" stroke-width="{LW}"/>'
         + "".join(f'<line x1="{x}" y1="{y}" x2="{x + 90}" y2="{y}" stroke="{INK}" stroke-width="4" opacity=".25" stroke-linecap="round"/>'
                   for x, y in [(80, 800), (400, 840), (1300, 820), (1600, 900), (200, 960), (1100, 1000), (1500, 1040), (700, 1050)]))
shadow = f'<polygon points="{GX - 272},{GY} {GX + 272},{GY} {GX - 300},{GY + 260} {GX - 1150},{GY + 260}" fill="#8C3F4E" opacity=".45"/>'
def bird_down(x, y, s):
    return f'<path d="M{x - 30 * s:.0f},{y + 8 * s:.0f} Q{x - 14 * s:.0f},{y - 4 * s:.0f} {x},{y - 4 * s:.0f} Q{x + 14 * s:.0f},{y - 4 * s:.0f} {x + 30 * s:.0f},{y + 8 * s:.0f}" fill="none" stroke="{INK}" stroke-width="{6 * s:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'


BIRDS = [(2000, 260, 1.0), (2080, 320, .8), (2150, 230, .9)]
birds = "".join(sc.group(f"bd{i}", f'<g id="s02-bu{i}">{bird(x, y, s)}</g><g id="s02-bv{i}" opacity="0">{bird_down(x, y, s)}</g>') for i, (x, y, s) in enumerate(BIRDS))
SP = side_parts(WHITE, "school")
walker = (f'<g id="s02-wk"><g transform="translate(1900,1010) scale(.62)"><g id="s02-wkbob">{SP["scarf"]}{SP["bag"]}'
          f'<g id="s02-lgA">{SP["legsA"]}</g><g id="s02-lgB" opacity="0">{SP["legsB"]}</g>{SP["body"]}</g></g></g>')
l0, o0 = sc.line("a", 0, 960, 200, 92, fill=INK)
ga = (f'<g id="s02-ga">' + sky
      + sc.wob(sc.group("sun", sun(1480, 700, 150, YEL)) + plaza + sc.group("sh", shadow) + gate(GX, GY, GS) + birds + walker)
      + sc.wobT(l0) + sc.grain(.45) + tag(*sc.page(), INK) + "</g>")

# ---------------------------------------------------------------- b · 巷口的灯盏
houses = "".join(shophouse(x, 900, w, h, c, i, a) for i, (x, w, h, c, a) in enumerate(
    [(-20, 440, 560, "#C96F4A", 3), (420, 380, 660, "#6F8F84", 2), (800, 400, 520, "#C99A55", 3), (1200, 360, 620, "#8E5A7A", 2), (1560, 400, 560, "#5E7FA0", 3)]))
NL = 9
LANT = []
for k in range(NL):
    u = (k + .5) / NL
    lx = -20 + 1960 * u
    ly = 250 + 140 * 4 * u * (1 - u)
    LANT.append((round(lx), round(ly + 40)))
cord = "M-20,250 Q960,530 1940,250"
lan_dim = "".join(lantern(x, y, 34, "#7A2A22") for x, y in LANT)
lan_lit = "".join(f'<g id="s02-ln{k}" opacity="0">{lantern(x, y, 34, (RED, YEL, RED, ORANGE)[k % 4], True)}</g>' for k, (x, y) in enumerate(LANT))
SCX0, SCX1, SCT0, SCT1 = 2050, -560, 14.80, 19.30
scooter = f'<g id="s02-sc"><g transform="translate(0,1010) scale(1.05)"><g id="s02-scbob">{scooter2(0, 0, 1)}</g></g></g>'
L1 = music.line(1)
sign_chars, o1 = sc.chars("b", L1["text"], 200, 250, 70, "WK", YEL, vertical=True, lh=1.08)
sign = (f'<rect x="146" y="160" width="118" height="740" rx="8" fill="{INK}" transform="translate(10,12)"/>'
        f'<rect x="146" y="160" width="118" height="740" rx="8" fill="{RED}" stroke="{INK}" stroke-width="{LW}"/>'
        f'<line x1="264" y1="200" x2="330" y2="200" stroke="{INK}" stroke-width="{LW}"/><line x1="264" y1="860" x2="330" y2="860" stroke="{INK}" stroke-width="{LW}"/>')
gb = (f'<g id="s02-gb" opacity="0"><rect width="1920" height="1080" fill="{PLUM}"/>'
      + sc.wob(sparkle(1500, 120, 14, YEL) + sparkle(700, 90, 10, YEL) + houses
               + f'<rect y="900" width="1920" height="180" fill="#2C3166"/><line x1="0" y1="900" x2="1920" y2="900" stroke="{INK}" stroke-width="{LW}"/>'
               + "".join(f'<line x1="{x}" y1="990" x2="{x + 70}" y2="990" stroke="{WHITE}" stroke-width="6" opacity=".35" stroke-linecap="round"/>' for x in range(40, 1920, 180))
               + f'<path d="{cord}" fill="none" stroke="{INK}" stroke-width="5"/>' + lan_dim + lan_lit + sign + scooter)
      + sc.wobT(sign_chars) + sc.grain(.35) + tag(*sc.page(), WHITE) + "</g>")

body = ga + gb + sc.band("bin", ORANGE, YEL) + sc.band("mid", PLUM, YEL) + sc.band("out", YEL, ORANGE)

# lantern light times: as the scooter passes each one, snapped to the next half-beat
half = []
for a, b in zip(music.BEATS, music.BEATS[1:]):
    half += [a, (a + b) / 2]
lt = []
for (lx, _) in LANT:
    tc = SCT0 + (SCX0 + 200 - lx) / (SCX0 - SCX1) * (SCT1 - SCT0)
    lt.append(next(h for h in half if h >= tc - .03))

sc.band_out("bin")
sc.js += [
    # a · sunset + stretching shadow
    f'tl.fromTo("#s02-sun", {{ y: -80 }}, {{ y: 30, duration: {sc.L(GB):.2f}, ease: q("none", {sc.L(GB):.2f}) }}, 0);',
    f'tl.fromTo("#s02-sh", {{ scaleX: 0.25, svgOrigin: "{GX + 272} {GY}" }}, {{ scaleX: 1, duration: {sc.L(GB) - 0.3:.2f}, ease: q("power1.inOut", {sc.L(GB) - 0.3:.2f}) }}, 0.2);',
    *[f'tl.fromTo("#s02-bd{i}", {{ x: 0, y: 0 }}, {{ x: -2400, y: {-40 + 30 * i}, duration: 3.4, ease: q("none", 3.4) }}, {0.4 + i * 0.35:.2f});' for i in range(3)],
    *[f'cycle(["s02-bu{i}", "s02-bv{i}"], 0.4, {sc.L(GB):.2f}, 1 / 6, [0, 1]);' for i in range(3)],
    f'tl.fromTo("#s02-wk", {{ x: 0 }}, {{ x: -2200, duration: 4.4, ease: q("none", 4.4) }}, 0.1);',
    'cycle(["s02-lgA", "s02-lgB"], 0.1, 4.5, 1 / 6, [0, 1]);',
    'jitter("#s02-wkbob", 0.1, 4.5, 1 / 6, [{ y: 0 }, { y: -6 }]);',
    f'tl.set("#s02-ga", {{ opacity: 0 }}, {sc.L(GB)});',
    f'tl.set("#s02-gb", {{ opacity: 1 }}, {sc.L(GB)});',
    # b · scooter + lanterns
    f'tl.fromTo("#s02-sc", {{ x: {SCX0} }}, {{ x: {SCX1}, duration: {SCT1 - SCT0:.2f}, ease: q("none", {SCT1 - SCT0:.2f}) }}, {sc.L(SCT0)});',
    f'jitter("#s02-scbob", {sc.L(SCT0)}, {sc.dur}, 1 / 12, [{{ y: 0 }}, {{ y: -4 }}, {{ y: 0 }}, {{ y: -2 }}]);',
    *[f'tl.set("#s02-ln{k}", {{ opacity: 1 }}, {sc.L(t)});' for k, t in enumerate(lt)],
    *[f'bump("#s02-ln{k}", {sc.L(t)}, "{x} {y}", 1.15);' for k, (t, (x, y)) in enumerate(zip(lt, LANT))],
]
sc.band_through("mid", GB)
sc.pop_chars("b", o1, music.syllables(1))
sc.band_in("out", sc.g1)
sc.write(body)
