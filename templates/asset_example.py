"""Example of a project asset module (copied to scripts/assets/_example.py; files starting with "_" are skipped
by asset_sheet.py). Copy it to e.g. scripts/assets/cast.py and draw THIS song's own cast and props.

Draw each thing as a function around its own origin (base / feet at (0, 0)), then place it in a scene with
tr(x, y, s, thing()) or animate a wrapper <g>. Use the pencil in draw.py; never paste drawings from another song.
"""
import kitpath  # noqa: F401  (kit + this assets folder on sys.path)
from draw import *  # noqa: F401,F403


def hero(eye="open", mouth_kind="smile", wind=-.4, arms="down"):
    """主角 — decide hair, clothes and one signature colour from the lyrics (who sings, how old, what they carry)."""
    r = 80
    return person_front(0, -r * (2.9 + 1.5), r, hair="short", top=TEAL, bottom=NAVY, scarf=None,
                        eye=eye, mouth_kind=mouth_kind, arms=arms, wind=wind)


def paper_boat(fill=WHITE):
    """A prop straight out of a lyric line — shapes + ink outline + one highlight stroke."""
    return (shape("M-120,-40 L120,-40 L80,0 L-80,0Z", fill)
            + shape("M-60,-40 L0,-150 L60,-40Z", YEL)
            + line(-90, -20, 70, -20, 4, INK, .4))


SHEET = [   # (name, svg) — asset_sheet.py measures and fits each drawing into its cell
    ("主角 · 正面", hero()),
    ("主角 · 大笑", hero("happy", "laugh", arms="up")),
    ("纸船", paper_boat()),
]
