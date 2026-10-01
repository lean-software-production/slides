"""A one-off popcorn doodle for the check-in slide: a striped tub, overflowing.

A cue for the presenter: popcorn order, anyone goes next.
Drawn with the brand's icon renderer. Reads (never writes) the brand repo at ../brand.
Writes art/popcorn.svg.
"""

import json
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
    ("highlighter", "M30 60 C 18 52, 24 36, 38 40 C 36 26, 54 20, 62 30 C 66 16, 88 16, 90 30 C 102 24, 116 36, 106 46 C 118 50, 116 60, 110 60 Z"),
    (None, "M48 44 C 52 38, 60 40, 60 46 M70 32 C 74 26, 82 28, 80 36 M88 46 C 92 40, 100 42, 98 48"),
    ("front", "M28 58 L112 58 L100 134 L40 134 Z"),
    ("paper", "M28 58 L112 58 L100 134 L40 134 Z"),
    ("coral", "M28 58 L44 58 L50 134 L40 134 Z M60 58 L76 58 L74 134 L62 134 Z M94 58 L112 58 L100 134 L88 134 Z"),
    (None, "M24 58 L116 58"),
]

body = icons.render(parts, tokens, tokens["ink"])
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 -10 156 156" role="img" aria-label="Popcorn doodle">'
       f'<defs>{DEFS}</defs>{body}</svg>')
out = os.path.join(HERE, "popcorn.svg")
open(out, "w").write(svg)
print(out)
