"""A one-off popcorn doodle for the "Popcorn" Q&A slide, drawn with the brand's icon renderer.

Reads (never writes) the brand repo at ../brand. Writes art/popcorn.svg.
"""
import json
import os
import subprocess
import re
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


def puff(cx, cy, r):
    """A popped kernel: three bumps, a little lopsided."""
    return (f"M{cx - r} {cy + r * .4} C {cx - r * 1.5} {cy - r * .4}, {cx - r * .6} {cy - r * 1.3}, {cx} {cy - r * .8} "
            f"C {cx + r * .5} {cy - r * 1.5}, {cx + r * 1.6} {cy - r * .7}, {cx + r * 1.1} {cy + r * .1} "
            f"C {cx + r * 1.5} {cy + r * .9}, {cx + r * .2} {cy + r * 1.2}, {cx - r} {cy + r * .4} Z")


box = "M30 64 L110 64 L99 134 L41 134 Z"
parts = [
    # kernels heaped in the box, behind its rim
    ("highlighter", puff(46, 60, 14)), ("highlighter", puff(70, 52, 16)), ("highlighter", puff(95, 60, 14)),
    ("mustard", puff(60, 40, 11)), ("highlighter", puff(84, 38, 12)),
    # one kernel mid-pop, off to the side
    ("highlighter", puff(118, 20, 9)),
    (None, "M104 30 L108 26 M126 34 L131 38 M114 6 L113 0"),
    # the box in front of the heap
    ("front", box),
    ("paper", box),
    ("coral", "M30 64 L48 64 L52 134 L41 134 Z"), ("coral", "M62 64 L78 64 L78 134 L64 134 Z"), ("coral", "M92 64 L110 64 L99 134 L89 134 Z"),
    (None, box),
]

body = icons.render(parts, tokens, tokens["ink"])
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 -10 156 156" role="img" aria-label="popcorn doodle">'
       f'<defs>{DEFS}</defs>{body}</svg>')
out = os.path.join(HERE, "popcorn.svg")
open(out, "w").write(svg)
print(out)
