"""A one-off whiteboard doodle for the homework slide: a board on an easel, stickies on it, a marker writing.

A cue for the presenter: send everyone to the Zoom whiteboard.
Drawn with the brand's icon renderer. Reads (never writes) the brand repo at ../brand.
Writes art/whiteboard.svg.
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

parts = [
    (None, "M40 110 L28 138 M100 110 L112 138 M70 110 L70 134"),
    ("slate", "M8 14 L132 14 L132 112 L8 112 Z M16 22 L16 104 L124 104 L124 22 Z"),
    ("paper", "M16 22 L124 22 L124 104 L16 104 Z"),
    ("mustard", "M26 32 L52 30 L54 56 L28 58 Z"),
    ("coral", "M60 34 L86 34 L86 60 L60 60 Z"),
    ("teal", "M28 70 L54 68 L56 94 L30 96 Z"),
    (None, "M32 40 L46 39 M32 47 L44 46 M65 42 L80 42 M65 50 L76 50 M34 78 L48 77 M34 85 L46 85"),
    (None, "M64 76 C 70 70, 74 82, 80 76 C 84 72, 86 80, 90 76"),
    ("front", "M90 74 L128 40 L138 50 L100 84 L88 88 Z"),
    ("teal", "M98 66 L128 40 L138 50 L108 76 Z"),
    ("paper", "M90 74 L98 66 L108 76 L100 84 L88 88 Z"),
]

body = icons.render(parts, tokens, tokens["ink"])
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 -10 156 156" role="img" aria-label="Whiteboard doodle">'
       f'<defs>{DEFS}</defs>{body}</svg>')
out = os.path.join(HERE, "whiteboard.svg")
open(out, "w").write(svg)
print(out)
