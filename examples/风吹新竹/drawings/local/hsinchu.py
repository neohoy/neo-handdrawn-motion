"""新竹 local props: 东门城, 九降风晒米粉, 柿饼, 香山招潮蟹, 心型石沪, 竹笋仔.

Every MV gets its own local module (local/<place>.py) for landmarks and specialities; keep generic people and
props in hd_people / hd_props so a new city only swaps this file.
"""
from hd_lib import *  # noqa: F401,F403
from hd_people import *  # noqa: F401,F403


def gate(gx, gy, s=1.0):
    """东门城（迎曦门）cartoon, origin = ground centre."""
    g = []
    g.append(f'<rect x="-170" y="-115" width="340" height="115" fill="{RED}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>')
    for (x1, y1, x2) in [(-150, -92, -100), (-60, -70, -10), (40, -96, 90), (110, -60, 150), (-140, -40, -95), (70, -30, 120)]:
        g.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y1}" stroke="{INK}" stroke-width="4" opacity=".35" stroke-linecap="round"/>')
    g.append(f'<path d="M-46,0 L-46,-58 A46,46 0 0 1 46,-58 L46,0Z" fill="#2A2238" stroke="{INK}" stroke-width="{LW}"/>')
    g.append(f'<rect x="-112" y="-176" width="224" height="61" fill="{PAPER}" stroke="{INK}" stroke-width="{LW}"/>')
    for px in (-88, -30, 30, 88):
        g.append(f'<rect x="{px - 7}" y="-176" width="14" height="61" fill="{RED}" stroke="{INK}" stroke-width="4"/>')
    g.append(f'<path d="M-182,-176 Q-160,-166 -130,-182 L130,-182 Q160,-166 182,-176 L138,-216 L-138,-216Z" fill="{ROOF}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>')
    g.append(f'<path d="M-182,-176 q-14,-4 -12,-22 M182,-176 q14,-4 12,-22" fill="none" stroke="{INK}" stroke-width="{LW}" stroke-linecap="round"/>')
    g.append(f'<rect x="-62" y="-252" width="124" height="38" fill="{PAPER}" stroke="{INK}" stroke-width="{LW}"/>')
    g.append(f'<path d="M-124,-250 Q-104,-241 -82,-255 L82,-255 Q104,-241 124,-250 L90,-288 L-90,-288Z" fill="{ROOF}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>')
    g.append(f'<path d="M-96,-290 L96,-290 M-96,-290 q-14,-2 -12,-18 q6,-6 12,0 M96,-290 q14,-2 12,-18 q-6,-6 -12,0" fill="none" stroke="{INK}" stroke-width="{LW}" stroke-linecap="round"/>')
    return f'<g transform="translate({gx},{gy}) scale({s})">{"".join(g)}</g>'


def rice_rack(x, y, s=1.0):
    """九降风晒米粉 — wooden rack with noodle bundles blown LEFT."""
    g = [thick("M-150,140 L-150,-128", BROWN, 18, 6), thick("M150,140 L150,-128", BROWN, 18, 6), thick("M-176,-124 L176,-124", BROWN, 16, 6)]
    for i in range(7):
        bx = -126 + i * 42
        for j in range(3):
            dx = (j - 1) * 7
            g.append(thick(f"M{bx + dx},-116 C{bx + dx - 4},-50 {bx + dx - 22},10 {bx + dx - 54 - j * 6},{70 + j * 8}", WHITE, 5, 2.5))
        g.append(f'<rect x="{bx - 9}" y="-124" width="18" height="16" rx="3" fill="{BUFF}" stroke="{INK}" stroke-width="3"/>')
    return f'<g transform="translate({x},{y}) scale({s})">{"".join(g)}</g>'


def persimmon(x, y, r):
    g = [f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * .8:.0f}" fill="{ORANGE}" stroke="{INK}" stroke-width="5"/>',
         f'<path d="M{x - r * .55:.0f},{y - r * .2:.0f} q{r * .1:.0f},{-r * .3:.0f} {r * .4:.0f},{-r * .36:.0f}" stroke="#FFD2A0" stroke-width="5" fill="none" stroke-linecap="round"/>']
    for a in (0, 90, 180, 270):
        g.append(f'<ellipse cx="{x}" cy="{y - r * .72:.0f}" rx="{r * .24:.0f}" ry="{r * .1:.0f}" transform="rotate({a + 20} {x} {y - r * .72:.0f}) translate({r * .16:.0f},0)" fill="{BAMBOO}" stroke="{INK}" stroke-width="3"/>')
    g.append(f'<circle cx="{x + r * .2:.0f}" cy="{y + r * .25:.0f}" r="{r * .06:.1f}" fill="{WHITE}" opacity=".7"/><circle cx="{x - r * .3:.0f}" cy="{y + r * .35:.0f}" r="{r * .05:.1f}" fill="{WHITE}" opacity=".7"/>')
    return "".join(g)


def persimmon_tray(x, y, s=1.0):
    g = [f'<ellipse cx="0" cy="0" rx="168" ry="64" fill="{BUFF}" stroke="{INK}" stroke-width="{LW}"/>',
         f'<ellipse cx="0" cy="-4" rx="140" ry="48" fill="none" stroke="{INK}" stroke-width="4" opacity=".5"/>']
    for k in range(-4, 5):
        g.append(f'<line x1="{k * 30 - 14}" y1="-44" x2="{k * 30 + 14}" y2="44" stroke="{INK}" stroke-width="2" opacity=".25"/>')
    for px, py in ((-92, -12), (-30, -26), (36, -22), (98, -6), (2, 16)):
        g.append(persimmon(px, py, 36))
    return f'<g transform="translate({x},{y}) scale({s})">{"".join(g)}</g>'


def crab(x, y, s=1.0):
    """香山湿地的台湾招潮蟹 — one huge claw raised (waving)."""
    g = []
    for sx in (-1, 1):
        for k in range(3):
            g.append(f'<path d="M{sx * 44},{4 + k * 10} L{sx * (88 + k * 8)},{26 + k * 14} L{sx * (100 + k * 6)},{60 + k * 10}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
    g.append(f'<ellipse cx="0" cy="0" rx="72" ry="46" fill="{ORANGE}" stroke="{INK}" stroke-width="{LW}"/>')
    g.append(f'<path d="M-30,10 q30,18 60,0" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    for sx in (-1, 1):
        g.append(f'<line x1="{sx * 20}" y1="-40" x2="{sx * 28}" y2="-90" stroke="{INK}" stroke-width="6"/><circle cx="{sx * 28}" cy="-96" r="14" fill="{WHITE}" stroke="{INK}" stroke-width="5"/><circle cx="{sx * 30}" cy="-96" r="6" fill="{INK}"/>')
    g.append(thick("M56,-18 L108,-78", RED, 18))
    g.append(shape("M94,-96 C88,-150 150,-172 172,-132 C152,-132 136,-122 130,-106 C150,-100 162,-86 152,-70 C132,-60 106,-70 94,-96Z", RED))
    g.append(thick("M-56,-12 L-86,-38", ORANGE, 12) + f'<circle cx="-92" cy="-44" r="14" fill="{ORANGE}" stroke="{INK}" stroke-width="5"/>')
    return f'<g transform="translate({x},{y}) scale({s})">{"".join(g)}</g>'


def heart_weir(x, y, s=1.0, water=True):
    """香山湿地的心型石沪 — heart-shaped stone fish weir in the sea."""
    g = []
    if water:
        g.append(f'<ellipse cx="0" cy="-20" rx="200" ry="120" fill="{TEAL}" stroke="{INK}" stroke-width="{LW}"/>')
    g.append(f'<path d="{HEART}" fill="#5FCBB8" stroke="none"/>')
    g.append(f'<path d="{HEART}" fill="none" stroke="{INK}" stroke-width="34" stroke-dasharray="0.1 30" stroke-linecap="round"/>')
    g.append(f'<path d="{HEART}" fill="none" stroke="{STONE}" stroke-width="22" stroke-dasharray="0.1 30" stroke-linecap="round"/>')
    return f'<g transform="translate({x},{y}) scale({s})">{"".join(g)}</g>'


def shoot(x, y, s=1.0):
    """备选 B：竹笋仔."""
    g = [leaf(-34, -184, 76, 200, BAMBOOL), leaf(-8, -206, 64, 214, BAMBOO),
         shape("M0,-170 C30,-130 74,-50 78,30 C80,80 46,100 0,100 C-46,100 -80,80 -78,30 C-74,-50 -30,-130 0,-170Z", "#E2CF78"),
         shape("M-78,30 C-72,-30 -42,-90 -6,-120 C-24,-62 -34,10 -26,98 C-56,92 -80,70 -78,30Z", "#9DB04E"),
         shape("M78,30 C72,-30 42,-90 6,-120 C24,-62 34,10 26,98 C56,92 80,70 78,30Z", "#9DB04E"),
         shape("M-34,98 C-38,62 -16,40 0,30 C16,40 38,62 34,98 C20,102 -20,102 -34,98Z", "#B9C960")]
    for sx in (-1, 1):
        g.append(f'<ellipse cx="{sx * 22}" cy="-14" rx="7" ry="11" fill="{INK}"/><ellipse cx="{sx * 40}" cy="6" rx="12" ry="7" fill="{PINK}" opacity=".7"/>')
    g.append(f'<path d="M-12,8 Q0,20 12,8" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    return f'<g transform="translate({x},{y}) scale({s})">{"".join(g)}</g>'


def bamboo_kid(x, y, s=1.0):
    g = [stalk("M0,120 C4,0 2,-160 -10,-300", [(1, 40, 0), (3, -60, 0), (0, -170, -3), (-6, -250, -5)], 70),
         leaf(-70, -300, 110, 200, BAMBOOL), leaf(-40, -330, 90, 215, BAMBOO), leaf(40, -200, 90, -20, BAMBOOL)]
    for sx in (-1, 1):
        g.append(f'<ellipse cx="{sx * 16}" cy="-110" rx="7" ry="11" fill="{INK}"/><ellipse cx="{sx * 28}" cy="-90" rx="10" ry="6" fill="{PINK}" opacity=".7"/>')
    g.append(f'<path d="M-10,-86 Q0,-76 10,-86" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
    return f'<g transform="translate({x},{y}) scale({s})">{"".join(g)}</g>'
