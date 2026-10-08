#!/usr/bin/env python3
"""Snapshot scenes in isolation (a temp HyperFrames project mounting only them) and tile a contact sheet.

Usage: python3 preview.py <project_dir> <scene_id> [<scene_id> ...] [--at t1,t2,...] [--out sheet.jpg] [--video sample.mp4] [--config mv.json]
Times are GLOBAL song seconds (default: 6 evenly spaced per scene). Prints the sheet path; look at it.
--video also renders just these scenes (with the matching stretch of the song) — the sample for the user.
Snapshots run the scene's real timeline, so a JS error shows up as a frozen / uncovered frame — then run
`npx hyperframes check` on the temp project printed below to read the error.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HF = "hyperframes@0.8.123"
args = sys.argv[1:]
P = os.path.abspath(args.pop(0))
at, sheet, video = None, None, None
if "--video" in args:
    i = args.index("--video")
    video = os.path.abspath(args[i + 1])
    del args[i:i + 2]
if "--at" in args:
    i = args.index("--at")
    at = [float(x) for x in args[i + 1].split(",")]
    del args[i:i + 2]
if "--out" in args:
    i = args.index("--out")
    sheet = os.path.abspath(args[i + 1])
    del args[i:i + 2]
cfg_file = "mv.json"
if "--config" in args:
    i = args.index("--config")
    cfg_file = args[i + 1]
    del args[i:i + 2]
cfg = json.load(open(os.path.join(P, cfg_file), encoding="utf-8"))
out_dir = cfg.get("out_dir", "compositions/scenes")
span = {s["id"]: (float(s["start"]), float(s["end"])) for s in cfg["scenes"]}
fids = args
spans = [span[f] for f in fids]
g0, g1 = spans[0][0], spans[-1][1]
if at is None:
    at = [round(a + (b - a) * k / 6 + 0.02, 3) for a, b in spans for k in range(6)]
tmp = tempfile.mkdtemp(prefix="hdmv-prev-")
os.symlink(os.path.join(P, "compositions"), os.path.join(tmp, "compositions"))
shutil.copy(os.path.join(P, "hyperframes.json"), tmp)
clips = "".join(f'<div id="el-{f}" class="frame" data-composition-id="{f}" data-composition-src="{out_dir}/{f}.html" '
                f'data-start="{round(a - g0, 3)}" data-duration="{round(b - a, 3)}" data-track-index="1"></div>\n' for f, (a, b) in zip(fids, spans))
open(os.path.join(tmp, "index.html"), "w").write(f"""<!doctype html><html><head><meta charset="UTF-8"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0}}html,body{{width:1920px;height:1080px;overflow:hidden;background:#000}}#root{{position:relative;width:1920px;height:1080px;overflow:hidden}}.frame{{position:absolute;inset:0}}</style>
</head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{round(g1 - g0, 3)}" data-width="1920" data-height="1080">
{clips}</div><script>window.__timelines=window.__timelines||{{}};window.__timelines["main"]=gsap.timeline({{paused:true}});</script></body></html>""")
snap = os.path.join(tmp, "snaps")
r = subprocess.run(["npx", "-y", HF, "snapshot", tmp, "-o", snap, "--at", ",".join(str(round(t - g0, 3)) for t in at), "--no-end"],
                   capture_output=True, text=True, env={**os.environ, "PRODUCER_PAGE_NAVIGATION_TIMEOUT_MS": "90000"})
if r.returncode or not os.path.isdir(snap):
    print(r.stdout[-2000:], r.stderr[-2000:])
    raise SystemExit(f"snapshot failed (temp project: {tmp}) — retry once; a navigation timeout is usually machine load")
pngs = sorted((p for p in os.listdir(snap) if p.endswith(".png")), key=lambda p: int(p.split("-")[1]))
sheet = sheet or os.path.join(tmp, f"sheet-{fids[0]}.jpg")
n = len(pngs)
cols = min(3, n)
inputs = sum((["-i", os.path.join(snap, p)] for p in pngs), [])
if n == 1:
    flt = "[0:v]scale=640:360[o]"
else:
    lay = "|".join(f"{(k % cols) * 640}_{(k // cols) * 360}" for k in range(n))
    flt = "".join(f"[{k}:v]scale=640:360[s{k}];" for k in range(n)) + "".join(f"[s{k}]" for k in range(n)) + f"xstack=inputs={n}:layout={lay}:fill=black[o]"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", flt, "-map", "[o]", "-q:v", "3", sheet], check=True)
print(sheet)
print("times (left→right, top→bottom):", ", ".join(f"{t:g}" for t in at))
print("temp project:", tmp)
if video:
    silent = os.path.join(tmp, "silent.mp4")
    subprocess.run(["npx", "-y", HF, "render", tmp, "--fps", "30", "--experimental-fast-capture=false", "-o", silent], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-ss", f"{g0:.3f}", "-t", f"{g1 - g0:.3f}", "-i", os.path.join(P, cfg["audio"]),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-af", f"afade=t=out:st={max(0, g1 - g0 - 0.6):.3f}:d=0.6",
                    "-shortest", "-movflags", "+faststart", video], check=True)
    print("sample:", video)
