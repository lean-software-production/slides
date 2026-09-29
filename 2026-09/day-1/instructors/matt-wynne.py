"""Matt Wynne: bearded, balding, rectangular glasses, pointing while he explains,
with a small cucumber in his other hand (Cucumber co-founder)."""
import draw

SKIN, HAIR, BEARD = "#f1c6a4", "#5a3d27", "#3f2a1c"
spec = dict(pose="point", tilt=-5, look=3, skin=SKIN, hair="bald", hairc=HAIR,
            top=draw.MUSTARD, trousers=draw.SLATE)
parts = draw.gc.person(spec)
dx = spec["look"]

# Keep the body up to the head circle; redraw the face ourselves so the beard
# sits under the mouth, eyes and glasses.
start = parts.index(next(p for p in parts if p[0] == "head-start"))
head = parts[start + 1]            # the skin-coloured head circle
body, head_start = parts[:start], parts[start]

# Cucumber in the hanging (left) hand, held down in front of him. It goes after
# the torso, and the hand is drawn again on top of it, so the cucumber hides the
# torso and trouser outlines and the fingers hide the cucumber (layering rule).
hand = next(p for p in body if p[0] == "shape" and p[2] == SKIN)
neck = next(i for i, p in enumerate(body) if p[0] == "line")
cucumber = [
    ("shape", "M72 222 C 80 214, 90 218, 94 228 L 112 272 C 116 282, 110 290, 102 290 "
              "C 96 290, 92 286, 90 280 L 72 236 C 70 230, 70 226, 72 222 Z", draw.FOREST),
    ("line", "M84 236 L87 238 M94 252 L97 253 M88 262 L90 265 M102 270 L105 271 M98 282 L100 284", 2.5),
    hand,
]
body = body[:neck + 1] + cucumber + body[neck + 1:]

face = [head_start, head]
# fringe of hair round the sides and back, bald on top, one small tuft at the front
face += [
    ("shape", "M89 104 C 84 86, 88 72, 98 64 C 96 74, 96 86, 99 98 Z", HAIR),
    ("shape", "M171 104 C 176 86, 172 72, 162 64 C 164 74, 164 86, 161 98 Z", HAIR),
    ("line", "M112 62 C 118 56, 126 54, 134 55", 2.5),  # shine on the dome
]
# full beard: sideburns down round the jaw, moustache over the mouth
beard = ("M90 98 C 92 104, 96 110, 104 114 C 112 108, 122 106, 130 108 "
         "C 138 106, 148 108, 156 114 C 164 110, 168 104, 170 98 "
         "C 174 126, 162 152, 134 154 C 104 156, 86 132, 90 98 Z")
face.append(("shape", beard, BEARD))
# mouth: a small open smile showing through the beard
face.append(("shape", f"M{120+dx} 120 Q{130+dx} 118 {140+dx} 120 Q{136+dx} 131 {130+dx} 131 "
                      f"Q{124+dx} 131 {120+dx} 120 Z", draw.CORAL))
# eyes, blush on the cheeks above the beard line, rectangular glasses
face += [
    ("dot", 116 + dx, 97, 4.5), ("dot", 144 + dx, 97, 4.5),
    ("blush", 104 + dx, 106), ("blush", 156 + dx, 106),
    ("line", f"M{104+dx} 89 h24 v15 h-24 Z M{132+dx} 89 h24 v15 h-24 Z "
             f"M{128+dx} 94 L{132+dx} 94 M{104+dx} 92 L90 90 M{156+dx} 92 L170 90", 3.5),
    ("head-end",),
]

draw.write("matt-wynne", body + face, "Matt Wynne")
draw.headshot("matt-wynne", body + face, "Matt Wynne", draw.MUSTARD)
