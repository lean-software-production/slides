"""The highlight reel for Session 8: the eight sessions of cohort 2 on one timeline.

Shown on Zoom before "What has changed in your thinking between September and now?", and put on
a Miro frame for students to add stickies to. Its job is to jog memories, so each session is a
title and a few short phrases.

Writes two PNGs next to this script:
- highlight-reel.png: 16:9 (3840x2160), one row of eight sessions with an empty dashed space
  under each for stickies. For the Zoom share and Miro.
- highlight-reel-maven.png: two rows of four (1920 wide), no sticky space, for a Maven lesson,
  whose content column shows images at roughly 720px wide.

Draws with the Sketchbook kit (CSS, icons, fonts) pinned in this cohort's decks, and screenshots
the page with headless Chromium. Set CHROME to the browser binary if it isn't found.

    python3 highlight-reel.py
"""
import glob
import html
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
# The kit pinned for the cohort; Thursday's own copy if it has one, else Tuesday's.
KIT = next(k for k in (os.path.join(HERE, "..", "kit"), os.path.join(HERE, "..", "..", "tuesday", "kit"))
           if os.path.isdir(k))
KIT = os.path.abspath(KIT)
COHORT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def picture(path):
    return os.path.join(COHORT, path) if path.startswith("week-") else os.path.join(KIT, path)

WEEKS = ["Week 1", "Week 2", "Week 3", "Week 4"]

# (date, title, kit colour, picture, phrases). A picture is a kit path ("icons/gear.svg") or a drawing
# from an earlier deck ("week-1/thursday/art/ralph-loop.svg"); each keeps the meaning it had there:
# bikes for the two tracks, gear for the factory, kite for the capstone, robot for a machine.
# Keep phrases to a few words: the picture jogs the memory. Don't name students.
SESSIONS = [
    ("Tue 29 Sep", "Welcome", "teal", "week-1/tuesday/art/bike-ride.svg",
     ["Hopes and fears", "Two tracks: build the bike, ride it", "A real factory builds Tetris"]),
    ("Thu 1 Oct", "Loops", "coral", "week-1/thursday/art/ralph-loop.svg",
     ["Teach-back posters", "Ralph loop: what's awesome, what sucks", "One capstone, committed"]),
    ("Tue 6 Oct", "Validation", "forest", "icons/magnifier.svg",
     ["Same Tetris, twice", "The validator must not be the doer", "Validation is the mold"]),
    ("Thu 8 Oct", "Assembly lines", "mustard", "icons/gear.svg",
     ["Teach-back: context engineering", "Factory kaizen in troikas", "Planner, doer, validator as a graph"]),
    ("Tue 13 Oct", "How far can we push assembly lines?", "blue", "icons/robot.svg",
     ["Plan conformance checker", "Design your machines", "The three big brains"]),
    ("Thu 15 Oct", "Monitoring and steering", "rust", "icons/compass.svg",
     ["Fix the machine, not the code", "Pick your North Star", "Watch, then steer"]),
    ("Tue 20 Oct", "Show and tell, the foreman, superpowers", "deep-teal", "icons/kite.svg",
     ["First capstone show and tells", "Meet the foreman", "Superpowers: each step a machine"]),
    ("Thu 22 Oct", "Next steps", "teal", "icons/lightbulb.svg",
     ["Last show and tells", "Relay and Memba", "Taking it home"]),
]

TITLE = "Four weeks, eight sessions"

CSS = """
html, body { margin: 0; background: var(--sk-paper); }
.page { box-sizing: border-box; width: var(--w); height: var(--h); padding: var(--pad);
  display: flex; flex-direction: column; font-family: var(--sk-font-body); color: var(--sk-ink); }
.head { text-align: center; margin-bottom: var(--head-gap); }
.head .sk-title { font-size: var(--title-size); }
.sub { font-family: var(--sk-font-label); color: var(--sk-deep-teal); font-size: var(--sub-size); margin-top: .2em; }
.rows { display: flex; flex-direction: column; gap: var(--row-gap); flex: 1; }
.row { display: grid; grid-template-columns: repeat(var(--cols), 1fr); column-gap: var(--col-gap);
  grid-template-rows: auto auto auto; }
.week { grid-row: 1; font-family: var(--sk-font-label); font-size: var(--week-size); color: var(--sk-slate);
  text-align: center; position: relative; padding-bottom: .15em; }
.week::after { content: ""; position: absolute; left: 6%; right: 6%; bottom: 0; height: 0;
  border-bottom: 3px solid var(--sk-slate); filter: url(#sk-wobble-line); }
.line { grid-row: 2; grid-column: 1 / -1; position: relative; height: var(--node); margin: var(--line-gap) 0; }
.line::before { content: ""; position: absolute; left: 2%; right: 2%; top: 50%; border-top: 5px solid var(--sk-ink);
  filter: url(#sk-wobble-line); }
.line.arrow::after { content: ""; position: absolute; right: 1.2%; top: 50%; width: .4em; height: .4em;
  border-top: 5px solid var(--sk-ink); border-right: 5px solid var(--sk-ink); transform: translateY(-50%) rotate(45deg);
  font-size: var(--node); filter: url(#sk-wobble); }
.node { position: absolute; top: 0; transform: translateX(-50%); font-size: var(--num-size); }
.node .sk-num { width: calc(var(--node) / 1.0); height: calc(var(--node) / 1.0); font-size: 1em; }
.node .sk-num.ink { color: var(--sk-ink); }
.card { grid-row: 3; gap: .3em; padding: .7em .8em .9em; align-items: center; text-align: center; }
.card > img { width: var(--icon); height: var(--icon); }
.card .date { font-family: var(--sk-font-label); font-size: var(--date-size); color: var(--sk-slate); line-height: 1; }
.card h3 { margin: 0; font-family: var(--sk-font-label); font-weight: 400; font-size: var(--name-size);
  line-height: 1.02; color: var(--sk-accent-text); text-transform: uppercase; }
.card ul { margin: .15em 0 0; padding: 0; list-style: none; align-self: stretch; text-align: left; }
.card li { font-size: var(--phrase-size); line-height: 1.12; color: var(--sk-body-text); padding-left: .8em;
  position: relative; margin-top: .3em; }
.card li::before { content: "•"; position: absolute; left: .1em; color: var(--sk-accent); }
.row.with-space { grid-template-rows: auto auto auto auto 1fr; flex: 1; }
.ask { grid-row: 4; grid-column: 1 / -1; text-align: center; font-family: var(--sk-font-label);
  font-size: var(--week-size); color: var(--sk-deep-teal); margin: .35em 0 .25em; }
.space { grid-row: 5; position: relative; }
.space::before { content: ""; position: absolute; inset: 0; border-radius: .9em;
  border: 2.5px dashed #c9bfae; filter: url(#sk-wobble-soft); }
"""

# Heading text in each kit colour, mixed with ink where the bare colour fails 4.5:1 on paper.
ACCENT_TEXT = {
    "teal": "color-mix(in srgb, var(--sk-teal) 70%, var(--sk-ink))",
    "coral": "color-mix(in srgb, var(--sk-coral) 55%, var(--sk-ink))",
    "mustard": "color-mix(in srgb, var(--sk-mustard) 50%, var(--sk-ink))",
    "forest": "var(--sk-forest)", "blue": "var(--sk-blue)", "deep-teal": "var(--sk-deep-teal)",
    "rust": "color-mix(in srgb, var(--sk-rust) 70%, var(--sk-ink))",
}
WHITE_NUM = {"blue", "forest", "deep-teal"}  # white numerals only where they pass contrast

LAYOUTS = {
    # 1920x1080 CSS px at 2x. Room under each card for stickies on Miro.
    "zoom": dict(file="highlight-reel.png", w=1920, h=1080, scale=2, cols=8, space=True, vars={
        "--pad": "34px 38px 30px", "--title-size": "64px", "--sub-size": "30px", "--head-gap": "14px",
        "--row-gap": "0px", "--col-gap": "16px", "--week-size": "30px", "--node": "50px", "--num-size": "26px",
        "--line-gap": "10px", "--icon": "84px", "--date-size": "22px", "--name-size": "28px",
        "--phrase-size": "24px", "--space-gap": "14px"}),
    # 960 CSS px at 2x = 1920px, shown at ~720px in Maven: text sizes are set for that.
    "maven": dict(file="highlight-reel-maven.png", w=960, h=975, scale=2, cols=4, space=False, vars={
        "--pad": "22px 22px 24px", "--title-size": "44px", "--sub-size": "24px", "--head-gap": "8px",
        "--row-gap": "18px", "--col-gap": "14px", "--week-size": "24px", "--node": "40px", "--num-size": "21px",
        "--line-gap": "6px", "--icon": "64px", "--date-size": "19px", "--name-size": "23px",
        "--phrase-size": "20px", "--space-gap": "0px"}),
}


def card(i, s, live):
    """live: shown during Session 8, so its card says "today"."""
    date, title, colour, icon, phrases = s
    today = live and i == len(SESSIONS) - 1
    items = "".join(f"<li>{html.escape(p)}</li>" for p in phrases)
    when = html.escape(date) + (" · today" if today else "")
    return (f'<div class="card sk-panel sk-{colour}{" sk-dashed" if today else ""}" '
            f'style="--sk-accent-text:{ACCENT_TEXT[colour]}">'
            f'<img src="file://{picture(icon)}" alt="">'
            f'<div class="date">{when}</div><h3>{html.escape(title)}</h3><ul>{items}</ul></div>')


def row(sessions, start, cols, space, last):
    weeks = "".join(
        f'<div class="week" style="grid-column:{c + 1} / span 2">{WEEKS[(start + c) // 2]}</div>'
        for c in range(0, cols, 2))
    nodes = "".join(
        f'<div class="node" style="left:{(c + .5) * 100 / cols:.3f}%">'
        f'<span class="sk-num sk-{s[2]}{"" if s[2] in WHITE_NUM else " ink"}">{start + c + 1}</span></div>'
        for c, s in enumerate(sessions))
    cards = "".join(card(start + c, s, space) for c, s in enumerate(sessions))
    spaces = ('<div class="ask">What don\'t you want to forget? Add a sticky under the session.</div>'
              + '<div class="space"></div>' * len(sessions)) if space else ""
    return (f'<div class="row{" with-space" if space else ""}">{weeks}'
            f'<div class="line{" arrow" if last else ""}">{nodes}</div>{cards}{spaces}</div>')


def page(layout):
    L = LAYOUTS[layout]
    cols = L["cols"]
    rows = "".join(row(SESSIONS[r:r + cols], r, cols, L["space"], r + cols >= len(SESSIONS))
                   for r in range(0, len(SESSIONS), cols))
    style_vars = ";".join(f"{k}:{v}" for k, v in L["vars"].items())
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="file://{KIT}/sketchbook.css"><style>{CSS}</style></head>
<body class="sk-paper"><div class="page" style="--w:{L["w"]}px;--h:{L["h"]}px;--cols:{cols};{style_vars}">
<div class="head"><h1 class="sk-title"><span class="sk-burst"><span class="sk-hl">{html.escape(TITLE)}</span></span></h1>
<div class="sub">Hands-off agentic coding · cohort 2 · 29 September to 22 October 2026</div></div>
<div class="rows">{rows}</div></div>
<script src="file://{KIT}/sketchbook.js"></script></body></html>"""


def chrome():
    found = os.environ.get("CHROME") or shutil.which("chromium") or shutil.which("google-chrome")
    if not found:
        found = next(iter(sorted(glob.glob(os.path.expanduser(
            "~/.cache/ms-playwright/chromium-*/chrome-linux*/chrome")), reverse=True)), None)
    if not found:
        sys.exit("No Chromium found: set CHROME to the browser binary.")
    return found


def shoot(layout, tmp):
    L = LAYOUTS[layout]
    src = os.path.join(tmp, f"{layout}.html")
    open(src, "w").write(page(layout))
    out = os.path.join(HERE, L["file"])
    subprocess.run([chrome(), "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--allow-file-access-from-files", f"--force-device-scale-factor={L['scale']}",
                    f"--window-size={L['w']},{L['h']}", "--virtual-time-budget=4000",
                    f"--screenshot={out}", f"file://{src}"],
                   check=True, capture_output=True)
    print(out)


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        for name in LAYOUTS:
            shoot(name, tmp)
