#!/usr/bin/env python3
"""Beat grid + energy map for the project's song, via music-to-video's analyze-beatgrid.py (librosa through uv).

Usage: python3 analyze.py <project_dir>
Writes <project>/assets/audiomap.json and prints a section overview (downbeats, energy phases, strong hits).
"""
import json
import os
import subprocess
import sys

P = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
cfg = json.load(open(os.path.join(P, "mv.json"), encoding="utf-8"))
cands = [os.path.expanduser(f"~/{d}/skills/music-to-video/scripts/analyze-beatgrid.py") for d in (".claude", ".agents", ".codex")]
script = next((c for c in cands if os.path.exists(c)), None)
if not script:
    raise SystemExit("music-to-video skill not found (needs scripts/analyze-beatgrid.py) — install the HyperFrames skills first")
out = os.path.join(P, cfg["audiomap"])
subprocess.run(["uv", "run", "--quiet", "--with", "librosa", "--with", "soundfile", "--with", "numpy",
                "python", script, os.path.join(P, cfg["audio"]), "-o", out], check=True)
am = json.load(open(out, encoding="utf-8"))
print(am["summary"])
print("downbeats:", " ".join(f"{t:.2f}" for t in am["grid"]["downbeats_sec"]))
print("energy phases (merged):")
last = None
for ph in am["energy_phases"]:
    if last and last["level"] == ph["level"]:
        last["end"] = ph["end"]
        continue
    if last:
        print(f"  {last['start']:7.1f}–{last['end']:7.1f}  {last['level']}")
    last = dict(ph)
if last:
    print(f"  {last['start']:7.1f}–{last['end']:7.1f}  {last['level']}")
hits = [e["t"] for e in am.get("events", []) if e.get("drum") in ("kick", "snare") and e.get("energy", 0) >= 0.4]
print("strong kicks/snares:", " ".join(f"{t:.2f}" for t in hits[:80]))
