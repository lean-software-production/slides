"""Jeremy Lightsmith: co-creator of Lean Coffee, so he holds a coffee mug and a sticky note.

From his photo: bald on top with short dark hair round the sides, rimless glasses,
a dark moustache over a short salt-and-pepper beard, and a big toothy grin.
"""
import draw

spec = dict(pose="mug", look=3, skin="#ecbf9c", hair="bald", hairc="#3a3431", 
            top=draw.CORAL, trousers=draw.SLATE, mugc=draw.TEAL)
parts = draw.gc.person(spec)
dx = spec["look"]

# Drop the stock smile; he gets an open, toothy grin inside the beard instead.
parts = [p for p in parts if not (p[0] == "line" and " Q" in p[1] and " 113 " in p[1] + " ")]

# Short hair round the sides, running down into the beard as sideburns (the top stays bald).
sides = [("shape", "M94 68 C 88 78, 86 92, 88 106 L 96 104 C 94 92, 95 80, 100 72 Z", spec["hairc"]),
         ("shape", "M166 70 C 172 80, 174 94, 172 106 L 164 104 C 166 92, 165 82, 160 74 Z", spec["hairc"])]
# Thin, wide rimless-style glasses (the stock pair is round and heavy).
glasses = ("line", f"M{103+dx} 98 a13 10 0 1 0 26 0 a13 10 0 1 0 -26 0 "
                   f"M{131+dx} 98 a13 10 0 1 0 26 0 a13 10 0 1 0 -26 0 M{129+dx} 97 L{131+dx} 97", 2)
# Short grey beard round the jaw; the grin is a hole (opposite winding) so the
# teeth drawn underneath show through.
beard = (f"M88 104 C 90 134, 108 150, {130+dx} 150 C 154 150, 172 134, 172 104 "
         f"C 168 114, 160 118, {150+dx} 116 L {110+dx} 116 C 100 118, 92 114, 88 104 Z "
         f"M{149+dx} 116 C {147+dx} 138, {113+dx} 138, {111+dx} 116 Z")
teeth = f"M{111+dx} 116 C {113+dx} 138, {147+dx} 138, {149+dx} 116 Z"
# Dark moustache, thin, sitting on top of the grin.
moustache = (f"M{108+dx} 118 C {112+dx} 107, {124+dx} 105, {130+dx} 109 "
             f"C {136+dx} 105, {148+dx} 107, {152+dx} 118 C {144+dx} 113, {136+dx} 113, {130+dx} 114 "
             f"C {124+dx} 113, {116+dx} 113, {108+dx} 118 Z")
face = sides + [
    glasses,
    ("shape", teeth, "#ffffff"),
    ("line", f"M{115+dx} 123 L{145+dx} 123", 1.5),
    ("shape", beard, "#8f8a85"),
    ("shape", moustache, spec["hairc"]),
]
i = next(n for n, p in enumerate(parts) if p[0] == "head-end")
parts[i:i] = face

# Sticky note in the back hand: slipped in before the hand, so the hand covers its corner.
hand = next(n for n, p in enumerate(parts) if p[0] == "shape" and p[1].startswith("M71 236"))
parts[hand:hand] = [("shape", "M58 208 L90 204 L94 236 L61 239 Z", draw.MUSTARD),
                    ("line", "M66 218 L84 216 M67 226 L80 225", 2.5)]

print(draw.write("jeremy-lightsmith", parts, "Jeremy Lightsmith"))
print(draw.headshot("jeremy-lightsmith", parts, "Jeremy Lightsmith", draw.CORAL))
