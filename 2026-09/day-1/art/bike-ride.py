"""A one-off scene for the "Two tracks" slide: someone in a helmet whizzing down the
street on a bike. The rider and bike use the brand's chunky character renderer; the
street, the bush, the lamp post and the speed lines use the thin-ink icon renderer.

Reads (never writes) the brand repo at ~/brand. Writes art/bike-ride.svg.
"""
import json
import os
import re
import sys

BRAND = os.path.expanduser("~/brand")
sys.path.insert(0, os.path.join(BRAND, "src"))
sys.dont_write_bytecode = True
import characters  # noqa: E402  chunky outline + wash
import icons  # noqa: E402  thin wobbly ink + wash

HERE = os.path.dirname(os.path.abspath(__file__))
tokens = json.load(open(os.path.join(BRAND, "kit", "tokens.json")))["color"]
PAPER = tokens["paper"]
W, H = 800, 600  # everything is drawn in one 800x600 box (4:3)


def defs_from(svg_path):
    """The kit's filters, with their regions widened to cover the whole scene."""
    d = re.search(r"<defs>(.*?)</defs>", open(svg_path).read(), re.S).group(1)
    return re.sub(r'x="-?\d+" y="-?\d+" width="\d+" height="\d+"',
                  f'x="-100" y="-100" width="{W + 200}" height="{H + 200}"', d)


DEFS = (defs_from(os.path.join(BRAND, "kit", "characters", "learner.svg"))  # wob-bubble, wash, wob-lite
        + defs_from(os.path.join(BRAND, "kit", "icons", "lightbulb.svg")))  # w, sk-wash


def circle(cx, cy, r):
    return f"M{cx - r} {cy} a{r} {r} 0 1 0 {2 * r} 0 a{r} {r} 0 1 0 {-2 * r} 0 Z"


# ---- palette
TEAL, BLUE, CORAL, MUSTARD, SLATE = (tokens[k] for k in ("teal", "blue", "coral", "mustard", "slate"))
INK = tokens["ink"]
SKIN, HAIR = "#e8b48f", "#6b4a2e"

# ---- background: road, a bush behind, a lamp post ahead, speed lines (thin ink)
back = [
    # the street: two kerb lines and a dashed middle, open at the ends
    (None, "M40 524 C 200 516, 520 528, 724 520 M56 592 C 220 586, 500 596, 708 588"),
    (None, "M80 556 L136 555 M210 558 L276 557 M360 558 L430 559 M510 557 L580 556 M640 556 L690 557"),
    # a bush at the kerb, far behind the rider
    ("forest", "M44 520 C 30 490, 52 462, 80 474 C 90 446, 132 448, 136 478 C 154 482, 156 508, 146 520 Z"),
    # a lamp post up ahead, a little crooked
    (None, "M690 520 L694 250"),
    ("slate", "M672 252 C 674 232, 712 230, 716 250 Z"),
    ("mustard", "M680 252 L708 252 L704 272 L684 272 Z"),
    (None, "M676 520 L710 520"),
    # a small cloud
    ("bubble", "M560 170 C 556 146, 588 136, 600 152 C 612 130, 652 134, 652 158 C 672 160, 674 184, 654 186 L570 186 C 552 186, 548 172, 560 170 Z"),
]
# speed lines streaming out behind, plus a puff of dust off the back tyre
whoosh = [
    (None, "M60 250 L200 250 M100 290 L230 290 M50 330 L170 330 M80 396 L196 396"),
]

# ---- the bike and rider (chunky parts, back to front)
R, F, C = (232, 468), (492, 468), (340, 476)  # rear hub, front hub, crank
S, Hd, Hb = (310, 372), (452, 366), (462, 398)  # seat-tube top, head-tube top/bottom
WR = 64

def wheel(cx, cy):
    return [
        ("shape", circle(cx, cy, WR), PAPER),  # hides the road edge behind the wheel
        ("limb", circle(cx, cy, WR), SLATE, 12),
        # a few whirls instead of spokes: it's spinning
        ("line", f"M{cx - 36} {cy - 14} C {cx - 30} {cy - 40}, {cx - 4} {cy - 44}, {cx + 14} {cy - 34}"
                 f" M{cx + 34} {cy + 18} C {cx + 26} {cy + 40}, {cx} {cy + 44}, {cx - 16} {cy + 34}", 2.5),
        ("dot", cx, cy, 6),
    ]

bike_back = wheel(*R) + wheel(*F)

frame_col = CORAL
far_leg = [
    ("limb", f"M300 350 C 330 350, 360 356, 372 368 L322 452", SLATE, 26),
    ("shape", "M306 446 h28 a9 9 0 0 1 0 18 h-28 a9 9 0 0 1 0 -18 Z", INK),
]
frame = [
    # all the tubes in one stroke, so the joints merge instead of overlapping
    ("limb", f"M{R[0]} {R[1]} L{S[0]} {S[1]} L{C[0]} {C[1]} Z M{S[0]} {S[1]} L{Hd[0]} {Hd[1]} "
             f"M{C[0]} {C[1]} L{Hb[0]} {Hb[1]} M{Hd[0] - 2} {Hd[1] - 8} L{F[0]} {F[1]}", frame_col, 12),
    # handlebar: stem up, bar swept forward
    ("limb", f"M{Hd[0] - 4} {Hd[1] - 4} L{Hd[0] - 8} 336 C {Hd[0] + 6} 326, {Hd[0] + 20} 330, {Hd[0] + 28} 336", SLATE, 8),
    # saddle
    ("shape", "M280 362 C 284 350, 318 348, 334 356 C 334 366, 310 368, 280 362 Z", MUSTARD),
]
chainring = [("shape", circle(C[0], C[1], 18), SLATE), ("dot", C[0], C[1], 4)]

# rider
hair = [  # long hair streaming back from under the helmet
    ("shape", "M404 196 C 380 184, 356 196, 330 186 C 342 202, 352 206, 368 210 "
              "C 352 218, 338 222, 320 218 C 340 236, 372 238, 400 228 Z", HAIR),
]
torso = [("limb", "M306 330 L386 262", BLUE, 74)]
scarf = [
    # the tail flies back over the shoulders
    ("shape", "M404 244 C 376 234, 350 252, 322 240 C 302 232, 288 244, 268 236 "
              "C 276 250, 292 262, 318 258 C 346 256, 370 268, 402 262 Z", MUSTARD),
    ("shape", "M384 238 C 400 232, 424 238, 434 250 C 428 262, 404 266, 388 258 C 380 252, 378 244, 384 238 Z", MUSTARD),
]
cx, cy = 432, 206
face = [
    ("head-start", f"rotate(6 {cx} {cy})"),
    ("shape", circle(cx, cy, 40), SKIN),
    # squinty happy eyes, a big open grin
    ("line", f"M{cx + 2} {cy + 2} Q{cx + 8} {cy - 6} {cx + 14} {cy + 2}"
             f" M{cx + 24} {cy} Q{cx + 30} {cy - 8} {cx + 36} {cy - 1}", 3.5),
    ("shape", f"M{cx + 4} {cy + 16} Q{cx + 22} {cy + 20} {cx + 36} {cy + 12} "
              f"Q{cx + 32} {cy + 32} {cx + 18} {cy + 32} Q{cx + 6} {cy + 30} {cx + 4} {cy + 16} Z", CORAL),
    ("blush", cx - 6, cy + 14),
    # helmet: a dome with a little peak at the front and a vent stripe
    ("shape", f"M{cx - 44} {cy + 2} C {cx - 48} {cy - 44}, {cx + 2} {cy - 64}, {cx + 34} {cy - 40} "
              f"C {cx + 46} {cy - 30}, {cx + 52} {cy - 20}, {cx + 56} {cy - 12} "
              f"L{cx + 36} {cy - 12} C {cx + 10} {cy - 14}, {cx - 20} {cy - 8}, {cx - 44} {cy + 2} Z", TEAL),
    ("line", f"M{cx - 26} {cy - 30} C {cx - 12} {cy - 44}, {cx + 8} {cy - 46}, {cx + 24} {cy - 38}", 3),
    ("line", f"M{cx - 30} {cy - 2} L{cx - 20} {cy + 30}", 3),  # chin strap
    ("head-end",),
]
near_leg = [
    ("limb", "M318 336 C 350 340, 384 360, 396 372 L366 480", SLATE, 26),
    ("shape", "M350 476 h30 a9 9 0 0 1 0 18 h-30 a9 9 0 0 1 0 -18 Z", INK),
]
arm = [
    ("limb", "M392 266 C 420 284, 446 310, 468 330", BLUE, 22),
    ("shape", circle(474, 334, 12), SKIN),
]

rider = (bike_back + far_leg + frame + chainring + hair + torso + scarf + face + near_leg + arm)

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="20 84 720 540" role="img" '
       f'aria-label="someone in a bike helmet riding a bicycle fast down the street">'
       f'<defs>{DEFS}</defs>'
       f'{icons.render(back, tokens, INK)}'
       f'{icons.render(whoosh, tokens, INK)}'
       f'{characters.render(rider, paper=PAPER)}</svg>')
out = os.path.join(HERE, "bike-ride.svg")
open(out, "w").write(svg)
print(out)
