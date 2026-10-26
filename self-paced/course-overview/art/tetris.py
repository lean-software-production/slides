"""Draw tetris.svg: a finished game of Tetris in the Sketchbook palette, for the video's opening slide.

    python3 tetris.py   # writes tetris.svg beside this script
"""
from pathlib import Path

INK = '#2A2724'
PAPER = '#FCF9F3'
COLOURS = {'T': '#EEA306', 'S': '#039695', 'Z': '#F76C37', 'L': '#1F78A8', 'J': '#4A7D4B', 'O': '#D6631C', 'I': '#094854'}
# 10 columns by 14 rows, top to bottom; '.' is empty. A falling T piece near the top.
BOARD = """
..........
....TTT...
.....T....
..........
..........
..........
..........
..........
I.........
I.....OO..
I...SSOO.L
IJ.SSZZ..L
IJJJ.TZZLL
LLLTTTOOII
""".split()
CELL, PAD = 40, 24
W, H = len(BOARD[0]) * CELL, len(BOARD) * CELL

parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W + 2 * PAD} {H + 2 * PAD}" width="{W + 2 * PAD}" height="{H + 2 * PAD}">',
         '<defs><filter id="w" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="3.5"/></filter></defs>',
         f'<g filter="url(#w)"><rect x="{PAD}" y="{PAD}" width="{W}" height="{H}" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>']
for r, row in enumerate(BOARD):
    for c, ch in enumerate(row):
        if ch in COLOURS:
            x, y = PAD + c * CELL + 3, PAD + r * CELL + 3
            parts.append(f'<rect x="{x}" y="{y}" width="{CELL - 6}" height="{CELL - 6}" rx="5" fill="{COLOURS[ch]}" stroke="{INK}" stroke-width="3"/>')
parts.append('</g></svg>')
Path(__file__).with_name('tetris.svg').write_text('\n'.join(parts) + '\n')
