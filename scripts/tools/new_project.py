#!/usr/bin/env python3
"""Create a hand-drawn MV project: HyperFrames init + mv.json + song + Latin fonts + scene folder.

Usage: python3 new_project.py <project_dir> <song.mp3> [--title 歌名] [--artist 署名] [--year 2026] [--script zh-Hans|zh-Hant]
Then: analyze.py → lyrics.py → 设计/意象表.md → draw scripts/assets/*.py + asset_sheet.py → storyboard (user) →
      fonts.py → scenes → build.py / preview.py → sample (user) → assemble.py → render.py
"""
import argparse
import json
import os
import shutil
import subprocess

SKILL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KIT = os.path.join(SKILL, "scripts", "kit")
HF = "hyperframes@0.8.123"

ap = argparse.ArgumentParser()
ap.add_argument("project")
ap.add_argument("song")
ap.add_argument("--title", default="")
ap.add_argument("--artist", default="")
ap.add_argument("--year", default="")
ap.add_argument("--script", default="zh-Hans", choices=["zh-Hans", "zh-Hant"], help="简体 zh-Hans / 繁体 zh-Hant（台湾正体）")
a = ap.parse_args()
P = os.path.abspath(a.project)

if not os.path.exists(os.path.join(P, "hyperframes.json")):
    if os.path.exists(P) and os.listdir(P):
        raise SystemExit(f"{P} exists and is not a HyperFrames project; pick an empty or new directory")
    # HYPERFRAMES_SKIP_SKILLS: init would otherwise re-sync the globally installed HyperFrames skills from GitHub
    subprocess.run(["npx", "-y", HF, "init", P, "--non-interactive", "--example=blank", "--skill=music-to-video"], check=True,
                   env={**os.environ, "HYPERFRAMES_SKIP_SKILLS": "1"})
for d in ("assets/fonts", "scripts/scenes", "scripts/assets", "compositions/scenes", "renders", "设计"):
    os.makedirs(os.path.join(P, d), exist_ok=True)
ext = os.path.splitext(a.song)[1].lower() or ".mp3"
shutil.copy(a.song, os.path.join(P, "assets", "song" + ext))
for f in ("JetBrainsMono-400-normal-latin.woff2", "InstrumentSerif-400-italic-latin.woff2"):
    shutil.copy(os.path.join(SKILL, "assets", "fonts", f), os.path.join(P, "assets", "fonts", f))
cfg_path = os.path.join(P, "mv.json")
if not os.path.exists(cfg_path):
    cfg = {
        "title": a.title, "artist": a.artist, "year": a.year,
        "script": a.script,
        "audio": "assets/song" + ext,
        "audiomap": "assets/audiomap.json",
        "lyrics": "assets/lyrics.json",
        "extra_text": f"{a.title}{a.artist}",
        "fonts": {"KL": "assets/fonts/KL.woff2", "WK": "assets/fonts/WK.woff2",
                  "JBM": "assets/fonts/JetBrainsMono-400-normal-latin.woff2", "IS": "assets/fonts/InstrumentSerif-400-italic-latin.woff2"},
        "charset": "assets/fonts/charset.txt",
        "out_dir": "compositions/scenes",
        "volume": 0.9,
        "scenes": [],
    }
    json.dump(cfg, open(cfg_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
shim = ('"""Puts the neo-lyric-mv kit and this project\'s own drawings (scripts/assets) on sys.path."""\n'
        f'import os\nimport sys\nsys.path.insert(0, {KIT!r})\n'
        'sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets"))\n')
for d in ("scenes", "assets"):
    open(os.path.join(P, "scripts", d, "kitpath.py"), "w").write(shim)
for src, dst in (("scene_template.py", "scripts/scenes/_template.py"), ("asset_example.py", "scripts/assets/_example.py"),
                 ("意象表.md", "设计/意象表.md")):
    if not os.path.exists(os.path.join(P, dst)):
        shutil.copy(os.path.join(SKILL, "templates", src), os.path.join(P, dst))
print("project ready:", P)
print("next: python3", os.path.join(SKILL, "scripts/tools/analyze.py"), P)
