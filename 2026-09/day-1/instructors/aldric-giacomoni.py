"""Aldric Giacomoni: bald, bearded, big smile, holding up a go stone about to play it."""
import draw

INK = draw.gc.INK
SKIN = "#f1c3a3"
BEARD = "#a0572f"   # reddish brown
GREY = "#a39a90"    # greying at the sides
STONE = INK         # black go stone

spec = dict(pose="point", hair="bald", hairc="#2b2320", skin=SKIN, top=draw.TEAL, trousers=draw.SLATE,
            tilt=5, look=3)
parts = draw.gc.person(spec)

# Swap the stock pointing hand for a raised hand pinching a go stone.
POINT = {"M162 150 C 186 134, 196 108, 198 82", "M199 70 L203 48",
         "M186 40 L180 32 M212 36 L218 28 M200 26 L200 16"}
parts = [p for p in parts
         if not (len(p) > 1 and p[1] in POINT)
         and not (p[0] == "shape" and p[1].startswith("M188 72 "))]

arm = [
    ("limb", "M162 150 C 184 144, 196 128, 198 108", draw.TEAL, 22),
    # the stone: a lens-shaped disc, drawn before the hand so the fingers cover its lower edge
    ("shape", "M186 84 C 190 74, 212 74, 216 84 C 212 94, 190 94, 186 84 Z", STONE),
    # hand in front of the stone
    ("shape", "M188 100 a12 12 0 1 0 24 0 a12 12 0 1 0 -24 0 Z", SKIN),
    ("line", "M194 96 Q199 92 204 94", 2.5),   # fingertip crease
]
head = next(i for i, p in enumerate(parts) if p[0] == "head-start")
parts[head:head] = arm

# Beard, inside the head group (after the face circle, before the eyes and mouth) so it tilts with the head
# and hides the chin line. Red-brown beard, then grey patches over the sideburns.
face = next(i for i, p in enumerate(parts) if p[0] == "shape" and p[1].startswith("M88 92 a42"))
dx = spec["look"]
beard = [
    # one chunky beard from ear to ear, with an opening for the grin
    ("shape", f"M89 86 C 86 124, 104 152, {130 + dx} 152 C 156 152, 174 124, 171 86 "
              f"C 166 100, 162 110, {150 + dx} 114 C {144 + dx} 132, {116 + dx} 132, {110 + dx} 114 "
              f"C 98 110, 94 100, 89 86 Z", BEARD),
    # grey at the sides: a lighter patch over each sideburn
    ("shape", "M89 84 C 87 102, 90 116, 98 126 C 104 118, 106 112, 107 106 C 98 102, 92 94, 89 84 Z", GREY),
    ("shape", "M171 84 C 173 102, 170 116, 162 126 C 156 118, 154 112, 153 106 C 162 102, 168 94, 171 84 Z", GREY),
]
parts[face + 1:face + 1] = beard

# A big open grin instead of the stock smile line, in the gap in the beard.
parts = [p for p in parts if not (p[0] == "line" and p[1].startswith(f"M{119 + dx} 113"))]
parts = [p for p in parts if p[0] != "blush"]
end = next(i for i, p in enumerate(parts) if p[0] == "head-end")
parts[end:end] = [
    ("shape", f"M{116 + dx} 113 Q{130 + dx} 111 {144 + dx} 113 Q{141 + dx} 127 {130 + dx} 127 Q{119 + dx} 127 {116 + dx} 113 Z", "#ffffff"),
    ("blush", 108 + dx, 102), ("blush", 156 + dx, 102),
]

print(draw.write("aldric-giacomoni", parts, "Aldric Giacomoni"))
print(draw.headshot("aldric-giacomoni", parts, "Aldric Giacomoni", draw.TEAL))
