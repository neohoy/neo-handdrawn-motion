"""Plumbing shared by every scene: embedded fonts, per-scene boil / grain filters, the 12fps JS kit, and
write_frame() — the <template>-wrapped HyperFrames sub-composition that index.html mounts.

- fonts come from mv.json "fonts" (family key → woff2 path); embedded as data-URI @font-face
- filter ids carry the scene prefix (ids must stay unique across the assembled page)
"""
import base64
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from project import CONFIG, ROOT, path  # noqa: E402
import text  # noqa: E402

FONTS = CONFIG.get("fonts", {})


def font_css(names=("KL", "WK", "JBM")):
    out = []
    for n in names:
        if n not in FONTS:
            raise SystemExit(f"font {n!r} missing from mv.json fonts")
        with open(path(FONTS[n]), "rb") as fh:
            data = base64.b64encode(fh.read()).decode()
        out.append(f'@font-face{{font-family:"{n}";src:url(data:font/woff2;base64,{data}) format("woff2")}}')
    return "\n".join(out)


def defs(p, wob=6, wobT=3.2):
    return (f'<filter id="{p}-wob" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence id="{p}-turb" type="turbulence" baseFrequency="0.022" numOctaves="2" seed="1" result="n"/>'
            f'<feDisplacementMap in="SourceGraphic" in2="n" scale="{wob}" xChannelSelector="R" yChannelSelector="G"/></filter>'
            f'<filter id="{p}-wobT" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence id="{p}-turbT" type="turbulence" baseFrequency="0.035" numOctaves="2" seed="4" result="n"/>'
            f'<feDisplacementMap in="SourceGraphic" in2="n" scale="{wobT}" xChannelSelector="R" yChannelSelector="G"/></filter>'
            f'<filter id="{p}-grain" x="0" y="0" width="100%" height="100%"><feTurbulence id="{p}-turbG" type="fractalNoise" baseFrequency="0.8" numOctaves="3" seed="7" stitchTiles="stitch"/>'
            f'<feColorMatrix type="matrix" values="0 0 0 0 0.25  0 0 0 0 0.2  0 0 0 0 0.12  0 0 0 0.16 0"/>'
            # keep the grain inside the element's own pixels: a hidden (inactive) frame then paints no grain
            f'<feComposite in2="SourceGraphic" operator="in"/></filter>')


JS_KIT = r"""
  // drawn motion is quantised to 12fps ("on twos"): floor the tween progress to 1/12 s steps, then ease
  const q = (name, dur) => { const b = gsap.parseEase(name); const n = Math.max(1, Math.round(dur * 12)); return (p) => b(Math.floor(p * n + 1e-6) / n); };
  const at = (x, y) => x + " " + y;
  // line boil: every drawn group re-jitters every 1/12 s (3-seed cycle)
  const boil = (P, t0, t1) => {
    for (let k = Math.ceil(t0 * 12 - 1e-6); k / 12 < t1; k++) {
      const t = k / 12, s = (k % 3) + 1;
      tl.set("#" + P + "-turb", { attr: { seed: s } }, t);
      tl.set("#" + P + "-turbT", { attr: { seed: s + 3 } }, t);
      tl.set("#" + P + "-turbG", { attr: { seed: s + 6 } }, t);
    }
  };
  // swap whole drawings (one visible at a time)
  const cycle = (ids, t0, t1, step, order) => {
    let k = 0;
    for (let t = t0; t < t1 - 1e-6; t += step, k++) {
      const on = order[k % order.length];
      ids.forEach((id, i) => tl.set("#" + id, { opacity: i === on ? 1 : 0 }, t));
    }
  };
  // step a wrapper through transform states (flutter, bob)
  const jitter = (sel, t0, t1, step, states) => {
    let k = 0;
    for (let t = t0; t < t1 - 1e-6; t += step, k++) tl.set(sel, states[k % states.length], t);
  };
  // standard hand-drawn pop-in
  const pop = (sel, t, origin, dur = 0.25, ease = "back.out(2.2)", rot = -12) =>
    tl.fromTo(sel, { opacity: 0, scale: 0.3, rotation: rot, svgOrigin: origin }, { opacity: 1, scale: 1, rotation: 0, duration: dur, ease: q(ease, dur) }, t);
"""


def write_frame(fid, p, dur, svg, js_body, bg, fonts=("KL", "WK", "JBM")):
    svg = text.convert_svg(svg)      # → the film's script (mv.json "script": zh-Hans / zh-Hant)
    text.check_glyphs(svg)
    style = (font_css(fonts) + "\n"
             + f"#{p}-root{{position:absolute;inset:0;overflow:hidden;background:{bg}}}\n"
             + f"#{p}-root svg{{position:absolute;inset:0;width:100%;height:100%;display:block}}\n")
    script = ("\n(function () {\n  const tl = gsap.timeline({ paused: true, defaults: { ease: \"none\" } });\n"
              + JS_KIT + js_body
              + f"\n  tl.seek(0);\n  window.__timelines[\"{fid}\"] = tl;\n}})();\n")
    html = f"""<!doctype html>
<html lang="{"zh-TW" if text.SCRIPT == "zh-Hant" else "zh-CN"}">
  <head>
    <meta charset="UTF-8" />
    <title>{fid} — {CONFIG.get("title", "MV")}</title>
  </head>
  <body>
    <template>
      <style>
{style}      </style>
      <div id="{p}-root" data-composition-id="{fid}" data-width="1920" data-height="1080" data-duration="{dur}">
{svg}
      </div>
      <script>{script}      </script>
    </template>
  </body>
</html>
"""
    out = path(os.path.join(CONFIG.get("out_dir", "compositions/scenes"), f"{fid}.html"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as fh:
        fh.write(html)
    print("wrote", os.path.relpath(out, ROOT), f"{len(html) / 1024:.0f} KB")


def js_data(obj):
    return json.dumps(obj, ensure_ascii=False)
