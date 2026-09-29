"""A one-off scene for the "Two tracks" slide (left: "Build a factory"): a grown-up and a
child on the floor on Christmas morning, each with a spanner, putting a bike together.

People use the brand's character renderer (chunky outline + wash); the bike and the bits
on the floor (and the tree) use the icon renderer (thin wobbly ink). Reads (never writes) the brand repo
at ~/brand. Writes art/bike-build.svg.
"""
import json
import os
import re
import sys

BRAND = os.path.expanduser("~/brand")
sys.path.insert(0, os.path.join(BRAND, "src"))
sys.dont_write_bytecode = True
import characters as gc  # noqa: E402
import icons  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
tokens = json.load(open(os.path.join(BRAND, "kit", "tokens.json")))["color"]
PAPER, INK = tokens["paper"], tokens["ink"]
MUSTARD, TEAL, FOREST, CORAL = tokens["mustard"], tokens["teal"], tokens["forest"], tokens["coral"]
SLATE, RUST, BLUE = tokens["slate"], tokens["rust"], tokens["blue"]

# Filters, borrowed from the kit so they match exactly. People: wob-bubble / wash / wob-lite.
# Icons: w / sk-wash. The icon wobble's region is widened to cover the whole scene.
_person = open(os.path.join(BRAND, "kit", "characters", "learner.svg")).read()
_icon = open(os.path.join(BRAND, "kit", "icons", "lightbulb.svg")).read()
P_DEFS = re.search(r"<defs>(.*?)</defs>", _person, re.S).group(1)
I_DEFS = re.search(r"<defs>(.*?)</defs>", _icon, re.S).group(1)
I_DEFS = I_DEFS.replace('id="w" filterUnits="userSpaceOnUse" x="-40" y="-40" width="240" height="240"',
                        'id="w" filterUnits="userSpaceOnUse" x="-40" y="-40" width="500" height="400"')
assert 'width="500"' in I_DEFS


def circle(cx, cy, r):
    return f"M{cx - r} {cy} a{r} {r} 0 1 0 {2 * r} 0 a{r} {r} 0 1 0 {-2 * r} 0 Z"


def ellipse(cx, cy, rx, ry):
    return f"M{cx - rx} {cy} a{rx} {ry} 0 1 0 {2 * rx} 0 a{rx} {ry} 0 1 0 {-2 * rx} 0 Z"


# ---------------------------------------------------------------- people (260x380 box)

def spanner(x, y, angle, length=70):
    """A chunky open-ended spanner, handle starting at (x, y), pointing along angle."""
    h = length
    d = (f"M-4 -5 L{h} -6 A15 15 0 0 1 {h + 22} -7 L{h + 10} -5 L{h + 10} 5 L{h + 22} 7 "
         f"A15 15 0 0 1 {h} 6 L-4 5 A5 5 0 0 1 -4 -5 Z")
    return [("head-start", f"translate({x} {y}) rotate({angle})"), ("shape", d, SLATE), ("head-end",)]


def upper_body(spec):
    """person() minus its legs and its front arm/prop: back arm, torso, head."""
    parts = gc.person(spec)
    neck = next(i for i, p in enumerate(parts) if p[0] == "line" and p[1].startswith("M114 140"))
    head = next(i for i, p in enumerate(parts) if p[0] == "head-start")
    return parts[4:neck + 1], parts[head:]


def working_arm(spec, hand, elbow, grip_angle):
    """Front arm reaching down to the bike, a spanner in the fist (fist drawn over the handle)."""
    hx, hy = hand
    ex, ey = elbow
    arm = [("limb", f"M162 152 C {ex} {ey}, {ex} {ey}, {hx} {hy - 6}", spec["top"], 22)]
    fist = ("shape", circle(hx, hy, 11), spec["skin"])
    return arm + spanner(hx - 14, hy + 4, grip_angle) + [fist]


grown = dict(pose="point", look=5, skin="#a8704a", hair="short", hairc="#2b2320", glasses=True,
             top=FOREST, trousers=SLATE)
kid = dict(pose="point", tilt=7, look=4, skin="#a8704a", hair="curly", hairc="#2b2320",
           top=CORAL, trousers=BLUE)


def grown_up():
    """Kneeling on one knee, leaning in with the spanner. Faces right."""
    back, head = upper_body(grown)
    t, s = grown["trousers"], INK
    legs = [
        # back leg: knee on the floor, shin lying back along it, sole up
        ("limb", "M112 252 L118 318", t, 26), ("limb", "M118 322 L62 326", t, 24),
        ("shape", "M40 312 h14 a10 10 0 0 1 10 10 v8 h-34 v-8 a10 10 0 0 1 10 -10 Z", s),
        # front leg: thigh forward, shin down to the floor
        ("limb", "M146 250 L200 258", t, 26), ("limb", "M202 260 L206 322", t, 26),
        ("shape", "M196 322 h26 a10 10 0 0 1 0 20 h-26 a10 10 0 0 1 0 -20 Z", s),
    ]
    arm = working_arm(grown, (232, 214), (196, 170), -28)
    return legs + back + arm + head


def child():
    """Sitting back on the heels, reaching in. Drawn facing right, mirrored into place.
    A bigger head than the grown-up's so they read as a child. Returns (body, arm): the
    body sits behind the bike, the arm and spanner are drawn in front of it."""
    back, head = upper_body(kid)
    t = kid["trousers"]
    head[0] = ("head-start", f"rotate({kid['tilt']} 130 134) translate(130 140) scale(1.18) translate(-130 -140)")
    legs = [
        ("shape", "M66 326 h26 a9 9 0 0 1 0 18 h-26 a9 9 0 0 1 0 -18 Z", INK),  # toes peeking out behind
        ("limb", "M92 318 L128 324", t, 28),                       # shin folded under
        ("limb", "M110 300 L186 318", t, 30),                       # thigh along the floor
    ]
    # the whole upper body sits lower: sitting on heels
    lower = ("head-start", "translate(0 44)")
    body = legs + [lower] + back + head + [("head-end",)]
    arm = [lower] + working_arm(kid, (214, 250), (190, 190), -52) + [("head-end",)]
    return body, arm


# ---------------------------------------------------------------- objects (scene coords, 400x300)

REAR = (173, 262)   # rear hub
BB = (221, 270)      # bottom bracket (pedals)
SEAT = (207, 212)    # top of the seat tube
HEAD = (273, 216)    # top of the head tube
FORK = (287, 298)    # fork end, resting on the floor


def bike_frame():
    r = 34
    rx, ry = REAR
    spokes = " ".join(f"M{rx} {ry} L{rx + dx} {ry + dy}" for dx, dy in ((0, -33), (29, 16), (-30, 15)))
    return [
        ("bubble", circle(rx, ry, r)), (None, circle(rx, ry, r)), (None, circle(rx, ry, r - 6)), (None, spokes),
        # frame, a little lopsided
        ("coral", f"M{rx} {ry} L{SEAT[0]} {SEAT[1]} L{BB[0]} {BB[1]} Z"),
        ("coral", f"M{SEAT[0]} {SEAT[1] + 2} L{HEAD[0]} {HEAD[1]} L{HEAD[0] + 4} {HEAD[1] + 16} L{BB[0]} {BB[1]} Z"),
        (None, f"M{HEAD[0] + 3} {HEAD[1] + 10} L{FORK[0]} {FORK[1]}"),
        (None, f"M{HEAD[0]} {HEAD[1]} L{HEAD[0] - 3} {HEAD[1] - 10}"),       # bare stem, no bars yet
        # seat post, no saddle yet
        (None, f"M{SEAT[0]} {SEAT[1]} L{SEAT[0] - 3} {SEAT[1] - 14}"),
        # gift bow on the top tube
        ("mustard", "M237 220 C 225 206, 215 216, 237 224 C 259 232, 251 206, 237 220 Z"),
        (None, "M237 224 C 233 232, 229 236, 225 242 M238 224 C 243 232, 247 236, 251 240"),
        ("solid", circle(rx, ry, 4)), ("solid", circle(*BB, 5)),
    ]


def floor_bits():
    parts = [
        # front wheel lying flat on the floor
        ("bubble", ellipse(236, 314, 42, 11)), (None, ellipse(236, 314, 42, 11)), (None, ellipse(236, 314, 32, 7)),
        ("solid", ellipse(236, 314, 4, 2)),
        (None, "M236 314 L236 307 M236 314 L262 318 M236 314 L212 319"),
        # saddle, waiting
        ("mustard", "M104 326 C 108 316, 136 314, 146 322 C 138 330, 116 334, 104 326 Z"),
        # bolts and a nut
        (None, "M184 326 l5 -3 l5 3 l0 5 l-5 3 l-5 -3 Z"),
        (None, "M286 316 l6 -3 l6 3 l0 6 l-6 3 l-6 -3 Z"),
        (None, "M300 330 L316 326"), ("solid", "M296 327 L302 326 L303 333 L297 334 Z"),
    ]
    return parts


def tree():
    """A little Christmas tree at the back on the left, behind the grown-up."""
    return [
        ("forest", "M34 118 L62 176 L50 174 L72 222 L56 220 L80 264 L-8 266 L12 222 L-2 222 L20 176 L8 176 Z"),
        ("rust", "M28 264 L42 264 L42 280 L28 280 Z"),
        ("mustard", "M34 98 L38 108 L48 109 L40 115 L43 125 L34 119 L25 124 L28 115 L20 108 L30 108 Z"),
        ("solid", circle(24, 196, 3)), ("solid", circle(50, 236, 3)), ("solid", circle(40, 158, 2.5)),
    ]


def g(transform, inner):
    return f'<g transform="{transform}">{inner}</g>'



KID_AT = "translate(398 110) scale(-0.56 0.56)"
kid_body, kid_arm = child()

scene = "".join([
    icons.render(tree(), tokens, INK),
    # child on the right, mirrored so they face the bike
    g(KID_AT, gc.render(kid_body, paper=PAPER)),
    icons.render(bike_frame(), tokens, INK),
    g(KID_AT, gc.render(kid_arm, paper=PAPER)),
    # grown-up on the left, in front of the back wheel
    g("translate(14 76) scale(0.66)", gc.render(grown_up(), paper=PAPER)),
    icons.render(floor_bits(), tokens, INK),
])

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-16 69 392 294" role="img" '
       f'aria-label="a grown-up and a child, spanners in hand, putting a bicycle together">'
       f'<defs>{P_DEFS}{I_DEFS}</defs>{scene}</svg>')
out = os.path.join(HERE, "bike-build.svg")
open(out, "w").write(svg)
print(out)
