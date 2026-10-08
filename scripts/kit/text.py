"""Simplified / Traditional output and glyph coverage.

mv.json "script": "zh-Hans" (default) or "zh-Hant". Builders may be written in either; every <text> node is
converted to the film's script when the scene is written (OpenCC: s2tw for zh-Hant — Taiwan standard characters,
phrase-aware: 裡面 / 公里, 著 / 着 — and t2s for zh-Hans; override with mv.json "opencc").
OpenCC comes from `opencc-python-reimplemented`; tools/build.py runs builders under uv with it.
"""
import os
import re

import project

SCRIPT = project.CONFIG.get("script", "zh-Hans")
OPENCC = project.CONFIG.get("opencc") or ("s2tw" if SCRIPT == "zh-Hant" else "t2s")
_cc = None


def convert(s):
    global _cc
    if _cc is None:
        try:
            from opencc import OpenCC
            _cc = OpenCC(OPENCC)
        except ImportError:
            if SCRIPT == "zh-Hant":
                raise SystemExit("zh-Hant needs OpenCC — build through tools/build.py (it runs builders with uv + opencc)")
            _cc = False   # simplified film, sources already simplified: nothing to convert
    return _cc.convert(s) if _cc else s


def convert_svg(svg):
    """Convert the content of every <text> node (attributes and ids are left alone)."""
    return re.sub(r"(<text\b[^>]*>)([^<]+)(</text>)", lambda m: m.group(1) + convert(m.group(2)) + m.group(3), svg)


_CMAP = None


def check_glyphs(svg):
    """Every CJK glyph must exist in the embedded font subsets (charset.txt, written by tools/fonts.py)."""
    global _CMAP
    if _CMAP is None:
        cs = project.path(project.CONFIG.get("charset", "assets/fonts/charset.txt"))
        if not os.path.exists(cs):
            print("warning: no charset.txt — glyph coverage not checked (run tools/fonts.py)")
            _CMAP = False
        else:
            _CMAP = set(open(cs, encoding="utf-8").read())
    if _CMAP is False:
        return
    texts = re.findall(r">([^<>]+)</text>", svg)
    bad = sorted({ch for t in texts for ch in t if ord(ch) > 0x2E80 and ch not in _CMAP})
    if bad:
        raise SystemExit(f"glyphs missing from the font subsets: {''.join(bad)} — add them to mv.json extra_text and re-run tools/fonts.py")
