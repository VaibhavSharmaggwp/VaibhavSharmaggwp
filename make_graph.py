"""
Generates a GitHub-contribution-graph style SVG that spells a word.
Change TEXT / SUBTITLE below and run:  python make_graph.py
Outputs: graph-dark.svg and graph-light.svg
"""
import random

TEXT = "VAIBHAV"                          # the word drawn in the grid
SUBTITLE = "500+ problems solved · always shipping"   # line above the grid
SEED = 7                                   # change for a different background pattern

# 5x7 pixel font ("#" = lit cell)
FONT = {
 "A": [".###.","#...#","#...#","#####","#...#","#...#","#...#"],
 "B": ["####.","#...#","#...#","####.","#...#","#...#","####."],
 "C": [".####","#....","#....","#....","#....","#....",".####"],
 "D": ["####.","#...#","#...#","#...#","#...#","#...#","####."],
 "E": ["#####","#....","#....","####.","#....","#....","#####"],
 "F": ["#####","#....","#....","####.","#....","#....","#...."],
 "G": [".####","#....","#....","#.###","#...#","#...#",".###."],
 "H": ["#...#","#...#","#...#","#####","#...#","#...#","#...#"],
 "I": ["#####","..#..","..#..","..#..","..#..","..#..","#####"],
 "J": ["..###","...#.","...#.","...#.","...#.","#..#.",".##.."],
 "K": ["#...#","#..#.","#.#..","##...","#.#..","#..#.","#...#"],
 "L": ["#....","#....","#....","#....","#....","#....","#####"],
 "M": ["#...#","##.##","#.#.#","#.#.#","#...#","#...#","#...#"],
 "N": ["#...#","##..#","#.#.#","#..##","#...#","#...#","#...#"],
 "O": [".###.","#...#","#...#","#...#","#...#","#...#",".###."],
 "P": ["####.","#...#","#...#","####.","#....","#....","#...."],
 "Q": [".###.","#...#","#...#","#...#","#.#.#","#..#.",".##.#"],
 "R": ["####.","#...#","#...#","####.","#.#..","#..#.","#...#"],
 "S": [".####","#....","#....",".###.","....#","....#","####."],
 "T": ["#####","..#..","..#..","..#..","..#..","..#..","..#.."],
 "U": ["#...#","#...#","#...#","#...#","#...#","#...#",".###."],
 "V": ["#...#","#...#","#...#","#...#","#...#",".#.#.","..#.."],
 "W": ["#...#","#...#","#...#","#.#.#","#.#.#","##.##","#...#"],
 "X": ["#...#","#...#",".#.#.","..#..",".#.#.","#...#","#...#"],
 "Y": ["#...#","#...#",".#.#.","..#..","..#..","..#..","..#.."],
 "Z": ["#####","....#","...#.","..#..",".#...","#....","#####"],
 "0": [".###.","#...#","#..##","#.#.#","##..#","#...#",".###."],
 "1": ["..#..",".##..","..#..","..#..","..#..","..#..",".###."],
 "2": [".###.","#...#","....#","...#.","..#..",".#...","#####"],
 "<": ["...#.","..#..",".#...","#....",".#...","..#..","...#."],
 ">": [".#...","..#..","...#.","....#","...#.","..#..",".#..."],
 "/": ["....#","....#","...#.","..#..",".#...","#....","#...."],
 "!": ["..#..","..#..","..#..","..#..","..#..",".....","..#.."],
 " ": [".....",".....",".....",".....",".....",".....","....."],
}

COLS, ROWS = 53, 7          # one year of weeks x days, like GitHub
CELL, GAP = 11, 3
PITCH = CELL + GAP
LEFT, TOP = 40, 64          # room for day labels / title + month labels

THEMES = {
    "dark":  {"levels": ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"],
              "text": "#e6edf3", "muted": "#8b949e"},
    "light": {"levels": ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"],
              "text": "#1f2328", "muted": "#57606a"},
}

def build_grid():
    rnd = random.Random(SEED)
    lit = set()
    width = len(TEXT) * 6 - 1
    if width > COLS:
        raise SystemExit(f"'{TEXT}' is too long: max about 8 characters")
    start = (COLS - width) // 2
    for i, ch in enumerate(TEXT.upper()):
        glyph = FONT.get(ch, FONT[" "])
        for r, row in enumerate(glyph):
            for c, px in enumerate(row):
                if px == "#":
                    lit.add((start + i * 6 + c, r))
    grid = {}
    for c in range(COLS):
        for r in range(ROWS):
            if (c, r) in lit:
                grid[(c, r)] = rnd.choice([3, 4, 4, 4])     # bright letters
            else:
                grid[(c, r)] = rnd.choices([0, 1], [93, 7])[0]  # faint noise
    return grid, lit

def svg(theme):
    t = THEMES[theme]
    grid, lit = build_grid()
    W = LEFT + COLS * PITCH + 10
    H = TOP + ROWS * PITCH + 34
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">',
           "<style>",
           ".c{opacity:0;animation:pop .5s ease-out forwards}",
           "@keyframes pop{0%{opacity:0;transform:scale(.3)}100%{opacity:1;transform:scale(1)}}",
           ".l{animation:pop .5s ease-out forwards,glow 3s ease-in-out infinite alternate}",
           "@keyframes glow{from{filter:brightness(1)}to{filter:brightness(1.25)}}",
           "</style>",
           f'<text x="{LEFT}" y="22" font-size="15" fill="{t["text"]}">{SUBTITLE}</text>']
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    for i, m in enumerate(months):
        x = LEFT + int(i * COLS / 12) * PITCH
        out.append(f'<text x="{x}" y="{TOP-8}" font-size="10" fill="{t["muted"]}">{m}</text>')
    for r, d in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        out.append(f'<text x="4" y="{TOP + r*PITCH + 9}" font-size="10" fill="{t["muted"]}">{d}</text>')
    for (c, r), lvl in grid.items():
        x, y = LEFT + c * PITCH, TOP + r * PITCH
        delay = c * 0.04 + r * 0.02          # sweeps left to right
        cls = "c l" if (c, r) in lit else "c"
        out.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" '
                   f'fill="{t["levels"][lvl]}" style="animation-delay:{delay:.2f}s;'
                   f'transform-origin:{x+CELL/2}px {y+CELL/2}px"/>')
    ly = TOP + ROWS * PITCH + 14
    lx = W - 10 - 5 * PITCH - 70
    out.append(f'<text x="{lx}" y="{ly+9}" font-size="10" fill="{t["muted"]}">Less</text>')
    for i, col in enumerate(t["levels"]):
        out.append(f'<rect x="{lx + 30 + i*PITCH}" y="{ly}" width="{CELL}" height="{CELL}" rx="2" fill="{col}"/>')
    out.append(f'<text x="{lx + 34 + 5*PITCH}" y="{ly+9}" font-size="10" fill="{t["muted"]}">More</text>')
    out.append("</svg>")
    return "\n".join(out)

if __name__ == "__main__":
    for theme in THEMES:
        filename = f"graph-{theme}.svg"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(svg(theme))
        print(f"wrote {filename}")
