"""A one-off Ralph loop doodle for the teach-back prep slide: a plan, with an arrow going round it.

Drawn with the brand's icon renderer. Reads (never writes) the brand repo at ../brand.
Writes art/ralph-loop.svg.
"""
import json
import math
import os
import re
import subprocess
import sys

# The brand repo sits next to this one (../brand from the main checkout); find it from a worktree too.
_common = subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
                         cwd=os.path.dirname(os.path.abspath(__file__)), capture_output=True, text=True).stdout.strip()
BRAND = os.environ.get("BRAND") or os.path.join(os.path.dirname(os.path.dirname(_common)), "brand")
sys.path.insert(0, os.path.join(BRAND, "src"))
import icons  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
tokens = json.load(open(os.path.join(BRAND, "kit", "tokens.json")))["color"]
lightbulb = open(os.path.join(BRAND, "kit", "icons", "lightbulb.svg")).read()
DEFS = re.search(r"<defs>(.*?)</defs>", lightbulb, re.S).group(1)

CX, CY = 70, 72


def at(r, deg):
    a = math.radians(deg)
    return f"{CX + r * math.cos(a):.1f} {CY + r * math.sin(a):.1f}"


# The loop: a band most of the way round, clockwise, ending in an arrowhead; the gap is at the top.
start, end = -62, 246
band = (f"M{at(60, start)} A 60 60 0 1 1 {at(60, end)} L{at(47, end)} "
        f"A 47 47 0 1 0 {at(47, start)} Z")
head = f"M{at(38, end)} L{at(69, end)} L{at(53, end + 30)} Z"
# The plan in the middle, a little tilted, with two tasks ticked off.
page = "M54 50 L80 48 L89 57 L90 96 L56 98 Z"
parts = [
    ("coral", band),
    ("coral", head),
    ("highlighter", page),
    (None, "M80 48 L81 57 L89 57"),
    (None, "M61 63 L64 67 L69 60 M73 64 L83 63 M61 75 L64 79 L69 72 M73 76 L84 75 M62 88 L67 88 M73 88 L84 87"),
]

body = icons.render(parts, tokens, tokens["ink"])
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 -10 156 156" role="img" aria-label="Ralph loop doodle">'
       f'<defs>{DEFS}</defs>{body}</svg>')
out = os.path.join(HERE, "ralph-loop.svg")
open(out, "w").write(svg)
print(out)
