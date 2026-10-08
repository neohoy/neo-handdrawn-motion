#!/usr/bin/env python3
"""s17-years (137.44–146.64) — instrumental: the years go by.

A tear-off calendar on the wall loses one year per beat (2012 → 2026), each page snatched by the wind and
blown off to the left; outside the window the sky cycles day → dusk → night → dawn on the beats; on the
last bar a packed red suitcase lands by the wall (into the bridge: 后来我们去了不同地方).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scene import *  # noqa: E402,F401,F403
from hd_props import *  # noqa: E402,F401,F403
from local.hsinchu import *  # noqa: E402,F401,F403

sc = Scene("s17-years", "s17", PAPER)
BEATS = music.beats(137.5, 146.4)
YEARS = list(range(2012, 2027))
N = len(YEARS)
tears = BEATS[:N - 1] if len(BEATS) >= N - 1 else [137.5 + k * 0.6 for k in range(N - 1)]
CX, CY = 700, 220
pages = "".join(calendar_page(CX, CY, y, f"s17-pg{k}") for k, y in reversed(list(enumerate(YEARS))))
board = (f'<rect x="{CX - 240}" y="{CY - 40}" width="480" height="520" rx="10" fill="{WOOD}" stroke="{INK}" stroke-width="{LW}"/>'
         f'<rect x="{CX - 60}" y="{CY - 70}" width="120" height="50" rx="10" fill="{GREY}" stroke="{INK}" stroke-width="{LW}"/>')
SKY = [YEL, ORANGE, PINK, NIGHT]
window = (f'<rect id="s17-sky" x="1260" y="170" width="460" height="440" fill="{YEL}"/>'
          f'<rect x="1260" y="170" width="460" height="440" fill="none" stroke="{INK}" stroke-width="{LW + 8}"/>'
          f'<line x1="1490" y1="170" x2="1490" y2="610" stroke="{INK}" stroke-width="{LW + 4}"/><line x1="1260" y1="390" x2="1720" y2="390" stroke="{INK}" stroke-width="{LW + 4}"/>'
          f'<rect x="1240" y="610" width="500" height="30" fill="{WOOD}" stroke="{INK}" stroke-width="{LW}"/>')
curtain = (f'<path d="M1180,140 L1300,140 C1290,300 1240,420 1200,520 C1190,560 1200,600 1220,640 L1180,640Z" fill="{PINK}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>')
suitcase = (f'<g id="s17-case" opacity="0"><g id="s17-casesq"><rect x="1000" y="640" width="260" height="300" rx="30" fill="{RED}" stroke="{INK}" stroke-width="{LW}"/>'
            f'<rect x="1080" y="590" width="100" height="60" rx="18" fill="none" stroke="{INK}" stroke-width="{14 + 2 * LW}"/><rect x="1080" y="590" width="100" height="60" rx="18" fill="none" stroke="{BROWN}" stroke-width="14"/>'
            f'<line x1="1060" y1="660" x2="1060" y2="920" stroke="{INK}" stroke-width="5" opacity=".4"/><line x1="1200" y1="660" x2="1200" y2="920" stroke="{INK}" stroke-width="5" opacity=".4"/>'
            f'<circle cx="1040" cy="948" r="16" fill="{INK}"/><circle cx="1220" cy="948" r="16" fill="{INK}"/>'
            f'<path d="M1180,650 L1240,720" stroke="{INK}" stroke-width="4"/><g transform="rotate(14 1260 760)"><rect x="1200" y="720" width="120" height="76" rx="8" fill="{BUFF}" stroke="{INK}" stroke-width="5"/>'
            + T(1260, 772, "新竹", 40, "KL", RED, "middle", allow=True) + "</g></g></g>")
photo_w = (f'<g transform="rotate(-4 260 330)"><rect x="120" y="220" width="280" height="230" fill="{WOOD}" stroke="{INK}" stroke-width="{LW}"/>'
           f'<rect x="142" y="242" width="236" height="186" fill="{TEAL}" stroke="{INK}" stroke-width="5"/>' + friends_back(260, 410, .3) + "</g>")
dots = "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="#E3D8C2"/>' for x in range(60, 1920, 140) for y in range(60, 900, 140))
body = (f'<rect width="1920" height="1080" fill="{PAPER}"/>' + dots
        + sc.wob(window + f'<g id="s17-curt">{curtain}</g>' + photo_w + board + pages
                 + f'<rect y="900" width="1920" height="180" fill="{WOOD}"/><line x1="0" y1="900" x2="1920" y2="900" stroke="{INK}" stroke-width="{LW}"/>'
                 + suitcase + "".join(sc.group(f"lf{i}", leaf(2000, y, 80, 200)) for i, y in enumerate((260, 520, 720))))
        + sc.grain(.6) + tag(*sc.page(), INK))
js = [f'jitter("#s17-curt", 0, {sc.dur}, 1 / 6, [{{ skewX: 0, svgOrigin: "1180 140" }}, {{ skewX: -5, svgOrigin: "1180 140" }}, {{ skewX: -2, svgOrigin: "1180 140" }}, {{ skewX: -6, svgOrigin: "1180 140" }}]);']
for k, t in enumerate(tears):
    lt = sc.L(t)
    js.append(f'tl.to("#s17-pg{k}", {{ x: {-1400 - 40 * (k % 3)}, y: {-160 + 70 * (k % 4)}, rotation: {-70 - 10 * (k % 3)}, svgOrigin: "{CX} {CY + 220}", duration: 0.42, ease: q("power2.in", 0.42) }}, {lt:.3f});')
    js.append(f'tl.set("#s17-pg{k}", {{ opacity: 0 }}, {lt + 0.45:.3f});')
    js.append(f'tl.set("#s17-sky", {{ attr: {{ fill: "{SKY[(k + 1) % 4]}" }} }}, {lt:.3f});')
js += [*[f'tl.fromTo("#s17-lf{i}", {{ x: 0, rotation: 0, svgOrigin: "2000 {y}" }}, {{ x: -2300, rotation: -240, duration: 1.4, ease: q("none", 1.4) }}, {1.0 + i * 2.6:.2f});' for i, y in enumerate((260, 520, 720))],
       f'tl.set("#s17-case", {{ opacity: 1 }}, {sc.L(144.61) - 0.25:.2f});',
       f'tl.fromTo("#s17-case", {{ y: -700 }}, {{ y: 0, duration: 0.25, ease: q("power3.in", 0.25) }}, {sc.L(144.61) - 0.25:.2f});',
       f'tl.to("#s17-casesq", {{ scaleY: 0.84, scaleX: 1.1, svgOrigin: "1130 960", duration: 1 / 12 }}, {sc.L(144.61):.2f});',
       f'tl.to("#s17-casesq", {{ scaleY: 1, scaleX: 1, svgOrigin: "1130 960", duration: 3 / 12, ease: q("back.out(2.5)", 3 / 12) }}, {sc.L(144.61) + 1 / 12:.3f});']
sc.js += js
sc.write(body)
