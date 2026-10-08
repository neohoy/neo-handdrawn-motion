"""Locate the MV project being built and load its mv.json.

The project root is $HDMV_PROJECT, else the nearest directory at or above the current working directory
that holds mv.json. Builders are run from the project (or with HDMV_PROJECT set), never from the skill.
"""
import json
import os


def _find_root():
    env = os.environ.get("HDMV_PROJECT")
    if env:
        return os.path.abspath(env)
    d = os.getcwd()
    while True:
        if os.path.isfile(os.path.join(d, "mv.json")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            raise SystemExit("mv.json not found: run inside an MV project (tools/new_project.py creates one) or set HDMV_PROJECT")
        d = parent


ROOT = _find_root()
CONFIG = json.load(open(os.path.join(ROOT, "mv.json"), encoding="utf-8"))


def path(rel):
    return os.path.join(ROOT, rel)


def scenes():
    """[(id, start, end)] in film order, global song seconds."""
    return [(s["id"], float(s["start"]), float(s["end"])) for s in CONFIG.get("scenes", [])]


def span(fid):
    for i, a, b in scenes():
        if i == fid:
            return a, b
    raise SystemExit(f"scene {fid!r} is not in mv.json scenes")


def page(fid):
    """(n, total) for the page tag: the scene's place in the film."""
    ids = [s[0] for s in scenes()]
    return ids.index(fid) + 1, len(ids)
