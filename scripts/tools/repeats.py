#!/usr/bin/env python3
"""Find where a reference passage (e.g. the last chorus) repeats in the song — chroma + MFCC cross-correlation.

Usage: python3 repeats.py <project_dir> <ref_start> <ref_end> [--top 5]
Prints the best-matching start times and the shift (ref_start − match). A shift that holds for the whole
chorus means a scene built for one chorus can be reused for another by moving its data-start only.
Runs itself under `uv run --with librosa` when librosa is missing.
"""
import json
import os
import subprocess
import sys

try:
    import librosa  # noqa: F401
    import numpy as np
except ImportError:
    os.execvp("uv", ["uv", "run", "--quiet", "--with", "librosa", "--with", "numpy", "python", os.path.abspath(__file__), *sys.argv[1:]])

P = os.path.abspath(sys.argv[1])
r0, r1 = float(sys.argv[2]), float(sys.argv[3])
top = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 5
cfg = json.load(open(os.path.join(P, "mv.json"), encoding="utf-8"))
y, sr = librosa.load(os.path.join(P, cfg["audio"]), sr=22050)
hop = 256
fps = sr / hop
C = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop)
M = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop, n_mfcc=20)
F = np.vstack([C, M / (np.abs(M).max(axis=1, keepdims=True) + 1e-9)])
F = (F - F.mean(axis=1, keepdims=True)) / (F.std(axis=1, keepdims=True) + 1e-9)
ref = F[:, int(r0 * fps):int(r1 * fps)]
L = ref.shape[1]
scores = []
for i in range(0, F.shape[1] - L):
    t = i / fps
    if abs(t - r0) < (r1 - r0) * 0.5:
        continue
    scores.append((float((F[:, i:i + L] * ref).mean()), t))
scores.sort(reverse=True)
picked = []
for sc, t in scores:
    if all(abs(t - u) > 3 for _, u in picked):
        picked.append((sc, t))
    if len(picked) >= top:
        break
print(f"reference {r0:.2f}–{r1:.2f}")
for sc, t in sorted(picked, key=lambda x: x[1]):
    print(f"  match at {t:8.3f}   shift {r0 - t:+8.3f}   score {sc:.3f}")
print("scores above ~0.4 are the same passage; ~0.3 is a related but different one")
