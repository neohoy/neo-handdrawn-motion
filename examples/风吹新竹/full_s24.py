#!/usr/bin/env python3
"""s24-outro (189.90–205.92) — the photo comes alive, then the sky.

The pink band from f4 uncovers the polaroid's picture at full size: the two friends on the sea wall at sunset,
kites, the heart-shaped stone weir. 192.59 (kick): the camera tilts up after the hero kite, through dusk into a
night sky; 风吹新竹 comes out in the stars, hoy neo signs, the 风城 seal stamps. A last gust takes the kite
off to the left, a paper band closes the book, one bamboo leaf drifts across, and it fades out with the song.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scene import *  # noqa: E402,F401,F403
from hd_props import *  # noqa: E402,F401,F403
from local.hsinchu import *  # noqa: E402,F401,F403

sc = Scene("s24-outro", "s24", PINK, fonts=("KL", "WK", "JBM", "IS"))
TILT0, TILT_D, LIFT = 192.59, 3.2, 980
TITLE_T = [196.2, 196.5, 196.8, 197.1]
SIG_T, SEAL_T = 198.0, 199.83
GUST_T, CLOSE_T, FADE_T = 201.9, 203.0, 204.7

# ---------------------------------------------------------------- the world (tilts down as the camera looks up)
sky = (f'<rect x="-40" y="{-LIFT - 200}" width="2000" height="{LIFT + 400}" fill="{NIGHT}"/>'
       f'<rect x="-40" y="-320" width="2000" height="320" fill="{PLUM}"/>'
       f'<rect x="-40" y="-100" width="2000" height="140" fill="#B5527A"/>'
       f'<rect x="-40" y="0" width="2000" height="620" fill="{PINK}"/>')
STARS = [(140, -820, 16), (420, -700, 12), (760, -900, 18), (1100, -760, 12), (1500, -880, 16), (1780, -640, 14), (300, -420, 10), (1650, -420, 12), (900, -560, 10), (1260, -500, 12)]
stars = "".join(sc.group(f"st{i}", sparkle(x, y, s)) for i, (x, y, s) in enumerate(STARS))
sea = (f'<rect x="-40" y="600" width="2000" height="300" fill="{TEAL}"/><line x1="-40" y1="600" x2="1960" y2="600" stroke="{INK}" stroke-width="{LW}"/>'
       + f'<g id="s24-wv">' + "".join(f'<path d="M{x},{y} q22,-24 48,-6 q-16,0 -12,16" fill="none" stroke="{WHITE}" stroke-width="5" stroke-linecap="round" opacity=".85"/>'
                                      for x, y in [(120, 660), (520, 700), (900, 650), (1300, 690), (1700, 660), (300, 790), (1100, 780), (1600, 820)]) + "</g>")
sand = f'<rect x="-40" y="880" width="2000" height="300" fill="{BUFF}"/><line x1="-40" y1="880" x2="1960" y2="880" stroke="{INK}" stroke-width="{LW}"/>'
world = (sky + stars + sc.group("sun", sun(560, 600, 200, ORANGE)) + sea + heart_weir(1500, 760, .6, water=False)
         + sc.group("k2", f'<g id="s24-k2s">{kite(420, 260, .7, -14, .8, False)}</g>')
         + sand + crab(240, 990, .5) + f'<g id="s24-fr">{friends_back(980, 900, 2.0)}</g>')
HERO = (1340, 300)
hero = (f'<g id="s24-hero"><g id="s24-hfly"><path d="M{HERO[0] + 10},{HERO[1] + 90} C1300,700 1150,1000 1060,1300" fill="none" stroke="{INK}" stroke-width="4" opacity=".7"/>'
        f'<g id="s24-hsw">{kite(HERO[0], HERO[1], .95, 10, 1.1, False)}</g></g></g>')

# ---------------------------------------------------------------- the night title
title, t_org = sc.chars("t", "风吹新竹", 960, 600, 210, "KL", YEL, stroke=INK, sw=16, shadow=12)
sc.extra_defs = '<clipPath id="s24-sigclip"><rect id="s24-sigrect" x="760" y="660" width="0" height="140"/></clipPath>'
sig = f'<g clip-path="url(#s24-sigclip)">{T(780, 760, "hoy neo", 96, "IS", WHITE)}</g>'
seal = (f'<g id="s24-seal" opacity="0"><g transform="rotate(-6 1470 690)"><rect x="1424" y="616" width="92" height="156" rx="6" fill="{PAPER}" stroke="{RED}" stroke-width="7"/>'
        + VT(1470, 682, "风城", 58, "KL", {0: RED, 1: RED}, 1.05) + "</g></g>")
GUST = [(2000, 300), (2100, 560), (2000, 820), (2150, 420), (2050, 700)]
gust = "".join(sc.group(f"gu{i}", curl(x + 30, y, .9, color=WHITE) if i % 2 == 0 else leaf(x, y, 100, 200 + 10 * i)) for i, (x, y) in enumerate(GUST))

# ---------------------------------------------------------------- the last page
last = (f'<g id="s24-last" opacity="0">'
        + f'<g id="s24-leaf">{leaf(2000, 520, 170, 200)}</g>'
        + f'<g id="s24-fin" opacity="0">{T(960, 980, "风吹新竹 · hoy neo · 2026", 40, "WK", INK, "middle", op=.8)}</g></g>')

body = (f'<rect width="1920" height="1080" fill="{PINK}"/>'
        + sc.wob(f'<g id="s24-world">{world}</g>' + hero + gust)
        + sc.wobT(title + seal) + sig
        + sc.grain(.4) + sc.group("tag", tag(*sc.page(), WHITE, "No.205 · 风城"), op=0)
        + sc.band("bin", PINK, YEL)
        + f'<g filter="url(#s24-wob)" data-layout-allow-overflow><g id="s24-close">{band_body(PAPER, ORANGE)}</g></g>'
        + f'<rect id="s24-paper" width="1920" height="1080" fill="{PAPER}" opacity="0"/>' + sc.grain(0).replace('opacity="0"', 'id="s24-pgrain" opacity="0"')
        + last
        + f'<rect id="s24-fade" width="1920" height="1080" fill="{INK}" opacity="0"/>')
sc.band_out("bin")
L = sc.L
js = [
    f'tl.fromTo("#s24-wv", {{ x: 0 }}, {{ x: -30, duration: 0.6, ease: q("sine.inOut", 0.6), repeat: 6, yoyo: true }}, 0);',
    f'jitter("#s24-fr", 0, {L(TILT0) + 1:.2f}, 1 / 6, [{{ x: 0 }}, {{ x: -2 }}, {{ x: 0 }}, {{ x: 1 }}]);',
    f'tl.fromTo("#s24-hsw", {{ rotation: -6, svgOrigin: "{HERO[0]} {HERO[1]}" }}, {{ rotation: 6, duration: 0.55, ease: q("sine.inOut", 0.55), repeat: 20, yoyo: true }}, 0);',
    f'tl.fromTo("#s24-k2s", {{ rotation: 5, svgOrigin: "420 260" }}, {{ rotation: -7, duration: 0.65, ease: q("sine.inOut", 0.65), repeat: 8, yoyo: true }}, 0.1);',
    f'bump("#s24-sun", {L(190.19):.2f}, "560 600", 1.08);',
    # the tilt: the world slides down, the hero kite climbs a little and stays with us
    f'tl.fromTo("#s24-world", {{ y: 0 }}, {{ y: {LIFT}, duration: {TILT_D}, ease: q("power2.inOut", {TILT_D}) }}, {L(TILT0):.2f});',
    f'tl.fromTo("#s24-hero", {{ y: 0 }}, {{ y: -60, duration: {TILT_D}, ease: q("power2.inOut", {TILT_D}) }}, {L(TILT0):.2f});',
    *[f'jitter("#s24-st{i}", {L(TILT0) + 1.5 + 0.1 * (i % 3):.2f}, {L(CLOSE_T):.2f}, 1 / 4, [{{ opacity: 1 }}, {{ opacity: 0.4 }}]);' for i in range(len(STARS))],
    *[f'tl.fromTo("#s24-t{i}", {{ opacity: 0, scaleX: 0.6, scaleY: 1.5, y: -90, svgOrigin: "{o[0]} {o[1] + 80}" }}, {{ opacity: 1, scaleX: 1, scaleY: 1, y: 0, duration: 0.25, ease: q("back.out(2.4)", 0.25) }}, {L(t):.2f});'
      for i, (o, t) in enumerate(zip(t_org, TITLE_T))],
    f'tl.fromTo("#s24-sigrect", {{ attr: {{ width: 0 }} }}, {{ attr: {{ width: 520 }}, duration: 0.7, ease: q("power1.inOut", 0.7) }}, {L(SIG_T):.2f});',
    f'pop("#s24-tag", {L(SIG_T) + 0.5:.2f}, "200 80", 0.25, "back.out(2)", -6);',
    f'tl.fromTo("#s24-seal", {{ opacity: 0, scale: 1.9, rotation: -10, svgOrigin: "1470 694" }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.17, ease: q("power3.in", 0.17) }}, {L(SEAL_T) - 0.17:.2f});',
    f'tl.to("#s24-seal", {{ scaleX: 1.1, scaleY: 0.88, svgOrigin: "1470 694", duration: 1 / 12 }}, {L(SEAL_T):.2f});',
    f'tl.to("#s24-seal", {{ scaleX: 1, scaleY: 1, svgOrigin: "1470 694", duration: 2 / 12, ease: q("back.out(2)", 2 / 12) }}, {L(SEAL_T) + 1 / 12:.3f});',
    # the last gust takes the kite away
    *[f'tl.fromTo("#s24-gu{i}", {{ x: 0, rotation: 0, svgOrigin: "{x} {y}" }}, {{ x: -2500, rotation: -200, duration: 0.7, ease: q("power1.in", 0.7) }}, {L(GUST_T) + i * 0.08:.2f});' for i, (x, y) in enumerate(GUST)],
    f'tl.to("#s24-hfly", {{ x: -1900, y: -260, duration: 0.9, ease: q("power2.in", 0.9) }}, {L(GUST_T) + 0.15:.2f});',
    f'tl.to("#s24-hsw", {{ rotation: -50, svgOrigin: "{HERO[0]} {HERO[1]}", duration: 0.9, ease: q("power2.in", 0.9) }}, {L(GUST_T) + 0.15:.2f});',
    # a paper band closes the book; it stays
    f'tl.fromTo("#s24-close", {{ x: 2000 }}, {{ x: -340, duration: 0.33, ease: q("none", 0.33) }}, {L(CLOSE_T):.2f});',
    f'tl.set(["#s24-paper", "#s24-pgrain", "#s24-last"], {{ opacity: 1 }}, {L(CLOSE_T) + 0.34:.2f});',
    f'tl.set("#s24-pgrain", {{ opacity: 0.9 }}, {L(CLOSE_T) + 0.34:.2f});',
    f'tl.fromTo("#s24-leaf", {{ x: 0, y: 0, rotation: 0, svgOrigin: "2000 520" }}, {{ x: -2400, y: 160, rotation: -300, duration: 2.6, ease: q("none", 2.6) }}, {L(CLOSE_T) + 0.4:.2f});',
    f'pop("#s24-fin", {L(CLOSE_T) + 0.7:.2f}, "960 966", 0.25, "back.out(2)", 0);',
    f'tl.fromTo("#s24-fade", {{ opacity: 0 }}, {{ opacity: 1, duration: {sc.dur - L(FADE_T):.2f}, ease: "power1.in" }}, {L(FADE_T):.2f});',
]
sc.js += js
sc.write(body)
