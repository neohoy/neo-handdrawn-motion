#!/usr/bin/env python3
"""Write <project>/assets/lyrics.json from timed lyrics, and print them against the bar grid.

Usage:
  python3 lyrics.py <project_dir> <file>      # .lrc ([mm:ss.xx]line) / .json ([{start,end,text}]) / .tsv (start<TAB>end<TAB>text)
  python3 lyrics.py <project_dir> --show      # print the current lyrics.json with the nearest downbeat

Section tags ([Verse] etc.) and empty lines are dropped. For LRC the end of a line = next start − 0.2 s
(last line: +4 s). Simplified or Traditional both work — scenes convert every text to mv.json "script" when written.
"""
import json
import os
import re
import sys

P = os.path.abspath(sys.argv[1])
cfg = json.load(open(os.path.join(P, "mv.json"), encoding="utf-8"))
out = os.path.join(P, cfg["lyrics"])


def show():
    L = json.load(open(out, encoding="utf-8"))
    db = []
    am = os.path.join(P, cfg["audiomap"])
    if os.path.exists(am):
        db = json.load(open(am, encoding="utf-8"))["grid"]["downbeats_sec"]
    for i, l in enumerate(L):
        near = min(db, key=lambda t: abs(t - l["start"])) if db else None
        bar = f"  (downbeat {near:.2f})" if near is not None else ""
        print(f"{i:3d}  {l['start']:7.2f}–{l['end']:7.2f}  {l['text']}{bar}")


if sys.argv[2] == "--show":
    show()
    sys.exit()
src = sys.argv[2]
text = open(src, encoding="utf-8").read()
lines = []
if src.endswith(".json"):
    lines = [{"start": float(x["start"]), "end": float(x["end"]), "text": x["text"].strip()} for x in json.loads(text)]
elif src.endswith(".tsv"):
    for row in text.splitlines():
        if row.strip():
            a, b, t = row.split("\t", 2)
            lines.append({"start": float(a), "end": float(b), "text": t.strip()})
else:
    stamps = []
    for row in text.splitlines():
        m = re.match(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)", row.strip())
        if m and m.group(3).strip() and not re.match(r"^\[.*\]$", m.group(3).strip()):
            stamps.append((int(m.group(1)) * 60 + float(m.group(2)), m.group(3).strip()))
    for k, (t, s) in enumerate(stamps):
        end = stamps[k + 1][0] - 0.2 if k + 1 < len(stamps) else t + 4.0
        lines.append({"start": round(t, 2), "end": round(end, 2), "text": s})
lines = [l for l in lines if l["text"] and not re.match(r"^\[.*\]$", l["text"])]
json.dump(lines, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"wrote {os.path.relpath(out, P)} — {len(lines)} lines")
show()
