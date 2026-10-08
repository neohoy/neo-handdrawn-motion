#!/usr/bin/env python3
"""Run scene builders listed in mv.json (each scene: {"id", "start", "end", "builder", "args"}).

Usage: python3 build.py <project_dir> [scene_id ...]     # no ids → every scene
A builder is any script under the project (usually scripts/scenes/<id>.py) that writes compositions/scenes/<id>.html.
Builders run under `uv run --with opencc-python-reimplemented` so text can be converted to the film's script.
"""
import json
import os
import shutil
import subprocess
import sys

P = os.path.abspath(sys.argv[1])
only = set(sys.argv[2:])
cfg = json.load(open(os.path.join(P, "mv.json"), encoding="utf-8"))
env = {**os.environ, "HDMV_PROJECT": P}
# OpenCC converts every on-screen text to the film's script (zh-Hans / zh-Hant) when a scene is written
PY = (["uv", "run", "--quiet", "--with", "opencc-python-reimplemented", "python"] if shutil.which("uv") else [sys.executable])
fails = []
for s in cfg["scenes"]:
    if only and s["id"] not in only:
        continue
    b = s.get("builder")
    if not b:
        print("skip (no builder):", s["id"])
        continue
    r = subprocess.run([*PY, os.path.join(P, b), *map(str, s.get("args", []))], cwd=P, env=env)
    if r.returncode:
        fails.append(s["id"])
if fails:
    raise SystemExit("failed: " + " ".join(fails))
