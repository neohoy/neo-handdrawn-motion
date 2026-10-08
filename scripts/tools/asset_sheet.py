#!/usr/bin/env python3
"""Draw the project's own cast + props onto one sheet, render it, and print the image path.

Usage: python3 asset_sheet.py <project_dir> [module ...] [--out 设计/素材表.png] [--cols 4]   (8 drawings per page)

Every song draws its own pictures from its lyrics (references/歌词转画面.md). They live as Python functions
in <project>/scripts/assets/*.py; each module lists what to show in SHEET:

    SHEET = [
        ("主角 · 正面", hero_front()),   # (name, svg) — any coordinates; the sheet measures and fits each drawing
        ("旧车票", ticket_svg()),
    ]

Files starting with "_" are skipped. (Old 4-tuples (name, svg, w, h) still work; w, h are ignored.)
The sheet is a design check, not part of the film: names use the system font. Look at the image before using
any asset in a scene, and show it to the user with the storyboard.
"""
import glob
import importlib.util
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

HF = "hyperframes@0.8.123"
args = sys.argv[1:]
P = os.path.abspath(args.pop(0))
out_rel, cols = os.path.join("设计", "素材表.png"), 4
if "--out" in args:
    i = args.index("--out"); out_rel = args[i + 1]; del args[i:i + 2]
if "--cols" in args:
    i = args.index("--cols"); cols = int(args[i + 1]); del args[i:i + 2]
only = set(args)
os.environ["HDMV_PROJECT"] = P
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kit"))
sys.path.insert(0, os.path.join(P, "scripts", "assets"))
sys.path.insert(0, os.path.join(P, "scripts", "scenes"))
from frame_kit import defs, font_css, FONTS  # noqa: E402

entries = []
for f in sorted(glob.glob(os.path.join(P, "scripts", "assets", "*.py"))):
    name = os.path.splitext(os.path.basename(f))[0]
    if name.startswith("_") or (only and name not in only):
        continue
    spec = importlib.util.spec_from_file_location(f"asset_{name}", f)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for e in getattr(mod, "SHEET", []):
        entries.append((f"{name} · {e[0]}", e[1]))
if not entries:
    raise SystemExit("no SHEET entries found in scripts/assets/*.py")

# a page is one 1920×1080 frame: `cols` × 2 cells; more drawings → more pages (素材表-2.png …)
W, H = 1920, 1080
CW, CH = W // cols, (H - 40) // 2
per = cols * 2
fonts = tuple(k for k in ("KL", "WK", "JBM", "IS") if k in FONTS and os.path.exists(os.path.join(P, FONTS[k])))
outs = []
for page in range(math.ceil(len(entries) / per)):
    cells = []
    for k, (label, svg) in enumerate(entries[page * per:(page + 1) * per]):
        cx, cy = (k % cols) * CW, (k // cols) * CH + 40
        # data-fit = the box to fit into (x, y, w, h); a script measures getBBox() on mount and scales / centres
        cells.append(f'<rect x="{cx + 8}" y="{cy + 8}" width="{CW - 16}" height="{CH - 16}" rx="14" fill="#FBF7EE" stroke="#D8CFBF" stroke-width="3"/>'
                     f'<g data-fit="{cx + 30},{cy + 26},{CW - 60},{CH - 100}"><g>{svg}</g></g>'
                     f'<text x="{cx + CW / 2:.0f}" y="{cy + CH - 26:.0f}" font-family="PingFang SC, Hiragino Sans GB, sans-serif" font-size="22" text-anchor="middle" fill="#333">{label}</text>')
    svg = (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><defs>{defs("sh")}</defs>'
           f'<rect width="{W}" height="{H}" fill="#F3EDE0"/><g filter="url(#sh-wob)">{"".join(cells)}</g></svg>')
    tmp = tempfile.mkdtemp(prefix="hdmv-sheet-")
    os.makedirs(os.path.join(tmp, "compositions"))
    shutil.copy(os.path.join(P, "hyperframes.json"), tmp)
    comp = f"""<!doctype html><html><head><meta charset="UTF-8"/></head><body><template>
<style>{font_css(fonts) if fonts else ""}
#sh-root{{position:absolute;inset:0;overflow:hidden;background:#F3EDE0}}#sh-root svg{{position:absolute;inset:0;width:100%;height:100%;display:block}}</style>
<div id="sh-root" data-composition-id="sheet" data-width="{W}" data-height="{H}" data-duration="1">{svg}</div>
<script>(function(){{document.querySelectorAll("#sh-root [data-fit]").forEach(function(g){{var f=g.getAttribute("data-fit").split(",").map(Number);var b=g.getBBox();if(!b.width||!b.height)return;var s=Math.min(f[2]/b.width,f[3]/b.height,1.6);g.setAttribute("transform","translate("+(f[0]+f[2]/2-(b.x+b.width/2)*s)+" "+(f[1]+f[3]/2-(b.y+b.height/2)*s)+") scale("+s+")");}});
const tl=gsap.timeline({{paused:true}});tl.set("#sh-root",{{opacity:1}},0);tl.seek(0);window.__timelines["sheet"]=tl;}})();</script>
</template></body></html>"""
    open(os.path.join(tmp, "compositions", "sheet.html"), "w").write(comp)
    open(os.path.join(tmp, "index.html"), "w").write(f"""<!doctype html><html><head><meta charset="UTF-8"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0}}html,body{{width:{W}px;height:{H}px;overflow:hidden}}#root{{position:relative;width:{W}px;height:{H}px}}.frame{{position:absolute;inset:0}}</style>
</head><body><div id="root" data-composition-id="main" data-start="0" data-duration="1" data-width="{W}" data-height="{H}">
<div id="el-sheet" class="frame" data-composition-id="sheet" data-composition-src="compositions/sheet.html" data-start="0" data-duration="1" data-track-index="1"></div>
</div><script>window.__timelines=window.__timelines||{{}};window.__timelines["main"]=gsap.timeline({{paused:true}});</script></body></html>""")
    snap = os.path.join(tmp, "snaps")
    r = subprocess.run(["npx", "-y", HF, "snapshot", tmp, "-o", snap, "--at", "0.2", "--no-end"], capture_output=True, text=True,
                       env={**os.environ, "PRODUCER_PAGE_NAVIGATION_TIMEOUT_MS": "90000"})
    pngs = sorted(p for p in os.listdir(snap) if p.endswith(".png")) if os.path.isdir(snap) else []
    if r.returncode or not pngs:
        print(r.stdout[-2000:], r.stderr[-2000:])
        raise SystemExit(f"snapshot failed (temp project {tmp}) — retry once")
    base, ext = os.path.splitext(os.path.join(P, out_rel))
    out = base + (f"-{page + 1}" if page else "") + ext
    os.makedirs(os.path.dirname(out), exist_ok=True)
    shutil.copy(os.path.join(snap, pngs[0]), out)
    outs.append(out)
    print(out)
print(f"{len(entries)} drawings on {len(outs)} page(s):", json.dumps([e[0] for e in entries], ensure_ascii=False))
