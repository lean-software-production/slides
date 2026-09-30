"""Shared helper for drawing the instructors in the Sketchbook brand style.

Each instructor has a script next to this one (e.g. matt-wynne.py) that builds a
list of parts and calls write(). The parts are rendered by the brand repo's own
renderer, so the drawings match the kit's characters.

Reads (never writes) the brand repo at ../brand.
"""
import os
import subprocess
import re
import sys

# The brand repo sits next to this one (../brand from the main checkout); find it from a worktree too.
_common = subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
                         cwd=os.path.dirname(os.path.abspath(__file__)), capture_output=True, text=True).stdout.strip()
BRAND = os.environ.get("BRAND") or os.path.join(os.path.dirname(os.path.dirname(_common)), "brand")
sys.path.insert(0, os.path.join(BRAND, "src"))
import characters as gc  # noqa: E402  person(), render(), and the stock people

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = "#FCF9F3"
VIEWBOX = "50 4 196 356"  # same box as the kit's people, so they line up side by side

# Palette (from the brand tokens). Don't invent new colours.
MUSTARD, TEAL, FOREST, CORAL, BLUE = "#EEA306", "#039695", "#4A7D4B", "#F76C37", "#1F78A8"
SLATE, RUST, DEEP_TEAL = "#36545C", "#D6631C", "#094854"

# The wash and wobble filters, taken from a kit character so they match exactly.
_learner = open(os.path.join(BRAND, "kit", "characters", "learner.svg")).read()
DEFS = re.search(r"<defs>(.*?)</defs>", _learner, re.S).group(1)


def write(slug, parts, label, viewbox=VIEWBOX):
    """Render parts with the brand renderer and write instructors/<slug>.svg."""
    body = gc.render(parts, paper=PAPER)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" role="img" '
           f'aria-label="{label}"><defs>{DEFS}</defs>{body}</svg>')
    path = os.path.join(HERE, f"{slug}.svg")
    with open(path, "w") as f:
        f.write(svg)
    return path


HEADSHOT_VIEWBOX = "50 30 160 160"  # head and shoulders, square


def headshot(slug, parts, label, top):
    """Write instructors/<slug>-headshot.svg: the head group from a full-body drawing on a
    shared pair of shoulders, so every instructor's headshot is framed the same way."""
    start = next(i for i, p in enumerate(parts) if p[0] == "head-start")
    end = next(i for i in range(start, len(parts)) if parts[i][0] == "head-end")
    bust = [("shape", "M56 200 C 56 160, 88 132, 130 132 C 172 132, 204 160, 204 200 Z", top),
            ("line", "M112 138 Q130 152 148 138", 3)]
    return write(f"{slug}-headshot", bust + parts[start:end + 1], label, viewbox=HEADSHOT_VIEWBOX)
