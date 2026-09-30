"""A one-off bicycle doodle for the "Two tracks" slide, drawn with the brand's icon renderer.

Reads (never writes) the brand repo at ../brand. Writes art/bike.svg.
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


def circle(cx, cy, r):
    return f"M{cx - r} {cy} a{r} {r} 0 1 0 {2 * r} 0 a{r} {r} 0 1 0 {-2 * r} 0 Z"


parts = [
    # wheels: a pale wash, then the tyre and hub
    ("bubble", circle(32, 98, 26)), ("bubble", circle(110, 98, 27)),
    (None, circle(32, 98, 26)), (None, circle(110, 98, 27)),
    (None, "M32 98 L32 74 M32 98 L52 108 M32 98 L14 110 M110 98 L110 72 M110 98 L88 108 M110 98 L128 112"),
    # frame, a little lopsided
    ("coral", "M32 98 L58 56 L68 98 Z"), ("coral", "M58 56 L98 58 L68 98 Z"),
    (None, "M98 58 L110 98"),
    # seat and handlebars
    ("mustard", "M46 50 C 50 44, 66 44, 70 50 Z"), (None, "M58 50 L58 56"),
    (None, "M98 58 L94 40 C 100 36, 108 36, 112 40"),
    ("solid", circle(32, 98, 3.5)), ("solid", circle(110, 98, 3.5)), ("solid", circle(68, 98, 4)),
]

body = icons.render(parts, tokens, tokens["ink"])
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 10 156 130" role="img" aria-label="bicycle doodle">'
       f'<defs>{DEFS}</defs>{body}</svg>')
out = os.path.join(HERE, "bike.svg")
open(out, "w").write(svg)
print(out)
