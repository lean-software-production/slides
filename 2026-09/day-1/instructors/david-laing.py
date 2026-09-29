"""David Laing: waving hello, a closed laptop tucked under his other arm.

Black rectangular glasses, short brown hair swept up and back, a wide closed-mouth smile.
Also writes david-laing-headshot.svg (the head on the shared shoulders).
"""
import draw

INK = draw.gc.INK
spec = dict(pose="wave", tilt=-5, look=2, skin="#f2c9a6", hair="bald", hairc="#6b4a2e",
            top=draw.FOREST, trousers=draw.SLATE)
dx = spec["look"]
body = draw.gc.person(spec)

# Hair and grin are his own (below): drop the stock bald-head line and mouth line.
smile = f"M{119 + dx} 113 Q{130 + dx} 122 {141 + dx} 113"
body = [p for p in body if not (p[0] == "line" and (p[1] == smile or p[1].startswith("M100 62")))]

# Laptop tucked under the back (left) arm, lid facing us. It sits in front of the
# torso (its paper fill hides the torso outline) and behind the arm, so the back
# arm and hand are moved to after the laptop.
laptop = [
    ("shape", "M70 236 L 148 238 C 151 238, 152 241, 150 244 L 72 244 C 68 244, 67 240, 70 236 Z", draw.SLATE),  # base
    ("shape", "M66 196 C 66 191, 69 188, 74 188 L 146 192 C 151 192, 153 195, 153 200 L 151 234 "
              "C 151 239, 148 241, 143 241 L 72 238 C 67 238, 64 235, 64 230 Z", draw.BLUE),
    ("line", "M118 212 a6 6 0 1 0 12 0 a6 6 0 1 0 -12 0", 2.5),  # a sticker on the lid
]

arm = next(i for i, p in enumerate(body) if p[0] == "limb" and p[1].startswith("M98 152"))
back_arm = body[arm:arm + 2]          # the sleeve and the hand
body = body[:arm] + body[arm + 2:]
collar = next(i for i, p in enumerate(body) if p[0] == "line" and p[1].startswith("M114 140"))
body = body[:collar + 1] + laptop + back_arm + body[collar + 1:]
head_end = body.index(("head-end",))
face = [
    # short brown hair: tight at the sides, swept up and back in a tousled top
    ("shape", "M89 88 C 86 68, 92 54, 102 48 C 104 40, 116 34, 126 38 C 134 32, 150 32, 158 40 "
              "C 168 42, 176 54, 173 68 C 175 76, 174 82, 171 88 C 168 76, 163 68, 156 66 "
              "C 146 62, 126 66, 110 66 C 100 70, 92 78, 89 88 Z", spec["hairc"]),
    ("line", "M114 52 C 122 46, 132 44, 142 46 M132 58 C 140 54, 150 54, 158 58", 2),  # strands swept back
    # a wide, closed-mouth smile, lifting more on one side
    ("line", f"M{116 + dx} 114 Q{128 + dx} 121 {144 + dx} 111", 3.5),
    # black rectangular frames
    ("line", f"M{104 + dx} 90 h22 q2 0 2 2 v9 q0 6 -6 6 h-12 q-6 0 -6 -6 v-9 q0 -2 2 -2 Z "
             f"M{134 + dx} 90 h22 q2 0 2 2 v9 q0 6 -6 6 h-12 q-6 0 -6 -6 v-9 q0 -2 2 -2 Z "
             f"M{128 + dx} 94 L{134 + dx} 94", 3),
]
# eyes sit inside the frames
body = [("dot", p[1], 98, 4) if p[0] == "dot" else p for p in body]

parts = body[:head_end] + face + body[head_end:]
path = draw.write("david-laing", parts, "David Laing")

draw.headshot("david-laing", parts, "David Laing", draw.FOREST)
