#!/usr/bin/env python3
"""Cut the two Chinese fonts down to exactly the characters the film uses, and record the covered charset.

  zh-Hans: KL = 站酷快乐体 ZCOOL KuaiLe          WK = 霞鹜文楷 LXGW WenKai TC
  zh-Hant: KL = Chiron GoRound TC 900（粗圆体）   WK = 霞鹜文楷 LXGW WenKai TC
  (KL: slams, titles, seals · WK: sung lines, labels. ZCOOL KuaiLe has no Traditional glyphs.)

Usage:
  python3 fonts.py <project_dir> fetch                 # Google Fonts subset API (text=…), needs network
  python3 fonts.py <project_dir> local KL=a.ttf WK=b.ttf   # subset local font files with fontTools
  python3 fonts.py <project_dir> check                 # only re-verify coverage → charset.txt

Characters = every lyric line + mv.json extra_text + every CJK character in scripts/scenes/*.py, converted to the
film's script first (OpenCC s2tw / t2s, as the scenes are).
Writes assets/fonts/KL.woff2, WK.woff2 and charset.txt (what BOTH fonts cover; scene builds check against it).
Runs itself under `uv run --with fonttools --with brotli` when fontTools is missing.
"""
import glob
import json
import os
import re
import sys
import urllib.parse
import urllib.request

try:
    from fontTools.ttLib import TTFont
    from opencc import OpenCC
except ImportError:
    os.execvp("uv", ["uv", "run", "--quiet", "--with", "fonttools", "--with", "brotli", "--with", "opencc-python-reimplemented",
                     "python", os.path.abspath(__file__), *sys.argv[1:]])

P = os.path.abspath(sys.argv[1])
mode = sys.argv[2]
cfg = json.load(open(os.path.join(P, "mv.json"), encoding="utf-8"))
SCRIPT = cfg.get("script", "zh-Hans")
FAM = ({"KL": ("Chiron GoRound TC", "900"), "WK": ("LXGW WenKai TC", None)} if SCRIPT == "zh-Hant" else
       {"KL": ("ZCOOL KuaiLe", None), "WK": ("LXGW WenKai TC", None)})
CC = OpenCC(cfg.get("opencc") or ("s2tw" if SCRIPT == "zh-Hant" else "t2s"))


def needed():
    # convert whole strings, never single characters: s2tw needs the context (心里 → 心裡, but 公里 stays)
    strings = [l["text"] for l in json.load(open(os.path.join(P, cfg["lyrics"]), encoding="utf-8"))]
    strings.append(cfg.get("extra_text", ""))
    for f in glob.glob(os.path.join(P, "scripts", "scenes", "*.py")):
        if os.path.basename(f).startswith("_") or os.path.basename(f) == "kitpath.py":
            continue   # the template and the path shim are not part of the film
        strings += open(f, encoding="utf-8").read().splitlines()
    chars = set("".join(CC.convert(t) for t in strings))
    keep = {c for c in chars if ord(c) > 0x2E80 or c in "·→←「」，。！？、…—"}
    return "".join(sorted(keep)) + "0123456789"


def fetch_url(url, headers=None, timeout=60, tries=4):
    """Google Fonts occasionally drops the TLS handshake; retry a few times."""
    import time
    for k in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=headers or {}), timeout=timeout).read()
        except OSError as e:
            if k == tries - 1:
                raise
            print(f"  retry ({type(e).__name__})")
            time.sleep(2 + 2 * k)


def out(key):
    return os.path.join(P, cfg["fonts"][key])


if mode == "fetch":
    text = needed()
    for key, (fam, wght) in FAM.items():
        url = "https://fonts.googleapis.com/css2?" + urllib.parse.urlencode({"family": fam + (f":wght@{wght}" if wght else ""), "text": text})
        css = fetch_url(url, {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"}, 30).decode()
        m = re.search(r"url\((https://[^)]+)\)\s*format\('woff2'\)", css)
        if not m:
            raise SystemExit(f"no woff2 in Google Fonts CSS for {fam}")
        data = fetch_url(m.group(1))
        os.makedirs(os.path.dirname(out(key)), exist_ok=True)
        open(out(key), "wb").write(data)
        print(f"{key}: {fam} → {os.path.relpath(out(key), P)} ({len(data) // 1024} KB)")
elif mode == "local":
    from fontTools import subset
    text = needed()
    for arg in sys.argv[3:]:
        key, src = arg.split("=", 1)
        opts = subset.Options()
        opts.flavor = "woff2"
        font = subset.load_font(src, opts)
        sub = subset.Subsetter(opts)
        sub.populate(text=text)
        sub.subset(font)
        subset.save_font(font, out(key), opts)
        print(f"{key}: {src} → {os.path.relpath(out(key), P)} ({os.path.getsize(out(key)) // 1024} KB)")
elif mode != "check":
    raise SystemExit("mode must be fetch, local or check")

# verify: what both CJK fonts cover
cover = None
for key in FAM:
    cm = {chr(c) for c in TTFont(out(key)).getBestCmap()}
    cover = cm if cover is None else cover & cm
miss = [c for c in needed() if c not in cover and c.strip()]
cs = os.path.join(P, cfg.get("charset", "assets/fonts/charset.txt"))
open(cs, "w", encoding="utf-8").write("".join(sorted(cover)))
print(f"charset: {len(cover)} glyphs covered by both KL and WK → {os.path.relpath(cs, P)}")
if miss:
    print("NOT covered (fonts lack them — reword or pick another font):", "".join(miss))
