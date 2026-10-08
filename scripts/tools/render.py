#!/usr/bin/env python3
"""Render the film with the settings known to be correct, then make share copies.

Usage: python3 render.py <project_dir> [--name film] [--chunk N] [--config mv.json]
  --chunk N (default 4): render N scenes at a time in a temp project and join the pieces losslessly, then lay
            the whole song under them. A page that mounts every scene captures ~10× slower than a few scenes
            (24 scenes: ~3 fps vs ~30 fps), so chunks are much faster. Chunk cuts must sit on whole frames —
            run `assemble.py P --snap` once and rebuild if render.py says they don't.
  --chunk 0 renders index.html in one pass.
Outputs:
  renders/<name>.mp4         30 fps, screenshot capture (--experimental-fast-capture=false: the default fast
                             capture paints ~0.15 s early, which breaks beat sync)
  renders/<name>-share.mp4   1080p CRF 25 (desktop / sharing)
  renders/<name>-phone.mp4   720p CRF 25 (≈ under 30 MB for a 3.5 min song — phone / chat upload)
  renders/<name>-cuts.jpg    last frame of each scene | first frame of the next, for checking every cut
"""
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time

HF = "hyperframes@0.8.123"
P = os.path.abspath(sys.argv[1])
name = sys.argv[sys.argv.index("--name") + 1] if "--name" in sys.argv else "film"
chunk = int(sys.argv[sys.argv.index("--chunk") + 1]) if "--chunk" in sys.argv else 4
# --config: another mv.json-style file in the project (e.g. one per edition: mv.json 简体 / mv-hant.json 繁体)
cfg = json.load(open(os.path.join(P, sys.argv[sys.argv.index("--config") + 1] if "--config" in sys.argv else "mv.json"), encoding="utf-8"))
out_dir = cfg.get("out_dir", "compositions/scenes")
scenes = [(s["id"], float(s["start"]), float(s["end"])) for s in cfg["scenes"]]
song = os.path.join(P, cfg["audio"])
master = os.path.join(P, "renders", f"{name}.mp4")
os.makedirs(os.path.dirname(master), exist_ok=True)
env = {**os.environ, "PRODUCER_PAGE_NAVIGATION_TIMEOUT_MS": "90000"}
t_start = time.time()


def nframes(f):
    return int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries", "stream=nb_read_packets",
                               "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip())


def hf_render(project, out):
    subprocess.run(["npx", "-y", HF, "render", project, "--fps", "30", "--experimental-fast-capture=false", "-o", out], check=True, env=env)


if chunk <= 0:
    hf_render(P, master)
else:
    groups = [scenes[i:i + chunk] for i in range(0, len(scenes), chunk)]
    for g in groups[1:]:
        a = g[0][1]
        if abs(a * 30 - round(a * 30)) > 1e-2:
            raise SystemExit(f"chunk cut {a} s is not on a whole frame — run: python3 assemble.py {P} --snap, rebuild, then render again")
    tmp = tempfile.mkdtemp(prefix="hdmv-render-")
    pieces = []
    for k, g in enumerate(groups):
        c0, c1 = g[0][1], g[-1][2]
        d = os.path.join(tmp, f"c{k}")
        os.makedirs(d)
        os.symlink(os.path.join(P, "compositions"), os.path.join(d, "compositions"))
        shutil.copy(os.path.join(P, "hyperframes.json"), d)
        clips = "".join(f'<div id="el-{f}" class="frame" data-composition-id="{f}" data-composition-src="{out_dir}/{f}.html" '
                        f'data-start="{round(a - c0, 4)}" data-duration="{round(b - a, 4)}" data-track-index="1"></div>\n' for f, a, b in g)
        open(os.path.join(d, "index.html"), "w").write(f"""<!doctype html><html><head><meta charset="UTF-8"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0}}html,body{{width:1920px;height:1080px;overflow:hidden;background:#000}}#root{{position:relative;width:1920px;height:1080px;overflow:hidden}}.frame{{position:absolute;inset:0}}</style>
</head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{round(c1 - c0, 4)}" data-width="1920" data-height="1080">
{clips}</div><script>window.__timelines=window.__timelines||{{}};window.__timelines["main"]=gsap.timeline({{paused:true}});</script></body></html>""")
        piece = os.path.join(tmp, f"c{k}.mp4")
        print(f"— chunk {k + 1}/{len(groups)}: {g[0][0]} … {g[-1][0]} ({c0:.2f}–{c1:.2f} s)")
        hf_render(d, piece)
        # HyperFrames may emit one extra frame at a chunk's end; trim every piece to its exact length so later
        # chunks don't drift against the song (cutting at the end is safe with stream copy)
        want_k = round((c1 - c0) * 30)
        got_k = nframes(piece)
        if got_k > want_k:
            fixed = piece.replace(".mp4", "-trim.mp4")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", piece, "-map", "0:v", "-frames:v", str(want_k), "-c", "copy", fixed], check=True)
            piece = fixed
        elif got_k < want_k:
            print(f"warning: chunk {k + 1} has {got_k} frames, expected {want_k}")
        pieces.append(piece)
    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in pieces))
    joined = os.path.join(tmp, "joined.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-map", "0:v", "-c", "copy", joined], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", joined, "-i", song, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-af", f"volume={cfg.get('volume', 0.9)}", "-shortest", "-movflags", "+faststart", master], check=True)
    want, got = round(scenes[-1][2] * 30), nframes(joined)
    print(f"frames: {got} (expected {want})" + ("" if got == want else "  ← MISMATCH, check the chunk cuts"))
    shutil.rmtree(tmp, ignore_errors=True)
print(f"master: {master} ({os.path.getsize(master) / 1e6:.0f} MB), {(time.time() - t_start) / 60:.1f} min")

for suffix, vf in (("share", None), ("phone", "scale=1280:720:flags=lanczos")):
    dst = os.path.join(P, "renders", f"{name}-{suffix}.mp4")
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", master]
    if vf:
        cmd += ["-vf", vf]
    cmd += ["-c:v", "libx264", "-preset", "slow", "-crf", "25", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k" if vf else "160k", "-movflags", "+faststart", dst]
    subprocess.run(cmd, check=True)
    print(f"{suffix}: {dst} ({os.path.getsize(dst) / 1e6:.1f} MB)")
# last frame of a scene | first frame of the next (a cut between frames shows from frame ceil(start × 30))
frames = []
for _, a, _ in scenes[1:]:
    n = math.ceil(a * 30 - 1e-6)
    frames += [n - 1, n]
if frames:
    sel = "+".join(f"eq(n\\,{n})" for n in frames)
    cuts = os.path.join(P, "renders", f"{name}-cuts.jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", master, "-vf", f"select='{sel}',scale=320:180,tile=8x{math.ceil(len(frames) / 8)}",
                    "-frames:v", "1", "-q:v", "3", cuts], check=True)
    print("cuts sheet:", cuts)
