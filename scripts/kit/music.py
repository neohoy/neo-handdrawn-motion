"""Song timing for scene builders (global song seconds).

- beat grid / downbeats: the project's audiomap.json (music-to-video's analyze-beatgrid.py)
- lyric lines: the project's lyrics.json — [{"start": s, "end": s, "text": "…"}], one entry per sung line
"""
import json

from project import CONFIG, path

_AM = json.load(open(path(CONFIG["audiomap"]), encoding="utf-8"))
BEATS = _AM["grid"]["beats_sec"]
DOWNBEATS = _AM["grid"]["downbeats_sec"]
SONG = float(_AM["audio"]["duration_sec"])
EVENTS = _AM.get("events", [])
LYRICS = json.load(open(path(CONFIG["lyrics"]), encoding="utf-8"))


def line(i):
    return LYRICS[i]


def beats(t0, t1):
    return [b for b in BEATS if t0 - 1e-6 <= b < t1 - 1e-6]


def downbeats(t0, t1):
    return [b for b in DOWNBEATS if t0 - 1e-6 <= b < t1 - 1e-6]


def half_beats():
    out = []
    for a, b in zip(BEATS, BEATS[1:]):
        out += [a, (a + b) / 2]
    return out


def hits(t0, t1, drums=("kick", "snare"), min_energy=0.3):
    """Strong drum hits in [t0, t1) — candidates for colour flips and slams."""
    return [e["t"] for e in EVENTS if t0 <= e["t"] < t1 and e.get("drum") in drums and e.get("energy", 0) >= min_energy]


def syllables(i, frac=0.72, lead=0.04):
    """Per-character times spread over the first `frac` of the sung span (just ahead of each syllable)."""
    L = LYRICS[i]
    n = len(L["text"])
    span = (L["end"] - L["start"]) * frac
    return [round(L["start"] - lead + span * k / max(1, n - 1), 3) for k in range(n)]
