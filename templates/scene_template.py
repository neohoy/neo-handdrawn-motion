#!/usr/bin/env python3
"""<scene-id> (<start>–<end>) — <歌词 1> / <歌词 2>.

画面（from 设计/意象表.md）:
a <start>–<GB>  <what line 1 shows: which nouns / places / actions of the lyric are drawn, where the line sits>
b <GB>–<end>    <line 2>
Copy to scripts/scenes/<scene-id>.py, add {"id", "start", "end", "builder"} to mv.json, then
`python3 <skill>/scripts/tools/build.py . <scene-id>` and preview it.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kitpath  # noqa: E402,F401  (kit + scripts/assets on sys.path)
from scene import *  # noqa: E402,F401,F403   Scene, music, project, band_body, hd_lib (palette, T, label, ribbon…)
from draw import *  # noqa: E402,F401,F403    the pencil: person_front / person_side / sky / weather / buildings
import typo  # noqa: E402                       the fixed lyric look: typing / slam / label_line / ribbon_line / sign …
# from cast import *  # noqa: E402,F401,F403   ← THIS song's own drawings (scripts/assets/cast.py)

SCENE_ID = os.path.splitext(os.path.basename(__file__))[0]
sc = Scene(SCENE_ID, bg=PAPER)           # element-id prefix comes from the id ("s02-…" → "s02"); must be unique in the film
LI = 0                                   # index of the first sung line in this scene (music.LYRICS)
GB = (sc.g0 + sc.g1) / 2                 # group swap time (global seconds) — put it just before a line

# ---------------------------------------------------------------- a · picture of line LI
FLOOR = 1000
r = 80
hero = person_front(960, FLOOR - r * 4.4, r, hair="short", top=TEAL, wind=-.4)   # ← replace with your own asset
ga = (f'<g id="{sc.id("ga")}"><rect width="1920" height="1080" fill="{PAPER}"/>'
      + sc.wob(sun(1500, 300, 110, YEL) + ground(FLOOR, BAMBOOL) + sc.group("hero", hero))
      + sc.wobT(typo.label_line(sc, "a", LI, 960, 190, 72, i=0))
      + sc.grain(.6) + tag(*sc.page(), INK) + "</g>")

# ---------------------------------------------------------------- b · picture of line LI + 1
gb = (f'<g id="{sc.id("gb")}" opacity="0"><rect width="1920" height="1080" fill="{NIGHT}"/>'
      + sc.wob(moon(1600, 260, 80) + stars([(300, 160, 14), (900, 120, 10), (1200, 260, 12)]))
      + sc.wobT(typo.ribbon_line(sc, "b", LI + 1, 300, 1620, 520, 92))
      + sc.grain(.35) + tag(*sc.page(), WHITE) + "</g>")

body = ga + gb + sc.band("mid", NIGHT, YEL)
sc.js += [
    f'tl.fromTo("#{sc.id("hero")}", {{ y: 220, scaleY: 0.85, svgOrigin: "960 {FLOOR}" }}, {{ y: 0, scaleY: 1, duration: 0.42, ease: q("back.out(1.6)", 0.42) }}, 0.1);',
    f'tl.set("#{sc.id("ga")}", {{ opacity: 0 }}, {sc.L(GB)});',
    f'tl.set("#{sc.id("gb")}", {{ opacity: 1 }}, {sc.L(GB)});',
]
sc.band_through("mid", GB)
sc.write(body)
