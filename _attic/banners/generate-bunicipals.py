#!/usr/bin/env python3
"""
Generate abstract banner SVGs for the 6 featured projects on the home page.

Each banner is a 600x200 SVG that visually represents the project's essence.
Style: monochromatic + single warm accent, geometric/abstract.
"""
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANNER_DIR = os.path.join(BASE, "assets", "banners")
os.makedirs(BANNER_DIR, exist_ok=True)

W, H = 600, 200

# Color palette
INK = "#0e0e0e"
INK_SOFT = "#1a1d29"
ACCENT = "#c8553d"
ACCENT_2 = "#d2691e"
WHITE = "#f5f3ee"


def svg_wrap(content, bg=INK, pattern_overlay=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img">
  <defs>
    <radialGradient id="rg" cx="80%" cy="20%" r="60%">
      <stop offset="0%" stop-color="{ACCENT}" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="{WHITE}" stroke-opacity="0.06" stroke-width="0.5"/>
    </pattern>
    <pattern id="diagonal" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="14" stroke="{WHITE}" stroke-opacity="0.05" stroke-width="1"/>
    </pattern>
    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="12" cy="12" r="1" fill="{WHITE}" fill-opacity="0.12"/>
    </pattern>
  </defs>
  <rect width="{W}" height="{H}" fill="{bg}"/>
  <rect width="{W}" height="{H}" fill="url(#rg)"/>
  {pattern_overlay}
  {content}
</svg>'''


# ──────────────────────────────────────────────────────────
# 1. ResolveAgent — node graph / AIOps / RAG retrieval
# ──────────────────────────────────────────────────────────
def resolve_agent():
    nodes = [
        (60, 100, 4), (140, 60, 6), (140, 140, 4),
        (240, 100, 8), (320, 50, 5), (320, 150, 5),
        (420, 100, 4), (500, 70, 5), (500, 130, 5), (560, 100, 3),
    ]
    edges = [
        (0, 1), (0, 2), (1, 3), (2, 3),
        (3, 4), (3, 5), (4, 6), (5, 6),
        (6, 7), (6, 8), (7, 9), (8, 9),
    ]
    lines = "\n  ".join(
        f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="{WHITE}" stroke-opacity="0.25" stroke-width="0.8"/>'
        for a, b in edges
    )
    circles = "\n  ".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="{(ACCENT if i == 3 else WHITE)}" fill-opacity="{(0.95 if i == 3 else 0.7)}"/>'
        for i, (x, y, r) in enumerate(nodes)
    )
    return svg_wrap(f'{lines}\n  {circles}', bg=INK_SOFT, pattern_overlay='<rect width="{W}" height="{H}" fill="url(#grid)"/>'.format(W=W, H=H))


# ──────────────────────────────────────────────────────────
# 2. Kudig — K8s cluster / node diagnosis
# ──────────────────────────────────────────────────────────
def kudig():
    # hex grid of nodes, one highlighted (accent) representing diagnosis
    nodes = []
    for row in range(3):
        for col in range(7):
            x = 60 + col * 75
            y = 50 + row * 50
            if col % 2:
                y += 25
            nodes.append((x, y))
    highlight = nodes[8]  # center
    lines = ""
    # connect each to its 2-3 neighbors
    for i, (x, y) in enumerate(nodes):
        for j, (x2, y2) in enumerate(nodes):
            if j <= i: continue
            d = ((x2-x)**2 + (y2-y)**2) ** 0.5
            if d < 90:
                lines += f'\n  <line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{WHITE}" stroke-opacity="0.18" stroke-width="0.6"/>'
    circles = "\n  ".join(
        f'<circle cx="{x}" cy="{y}" r="{(14 if (x,y)==highlight else 6)}" fill="{(ACCENT if (x,y)==highlight else WHITE)}" fill-opacity="{(0.95 if (x,y)==highlight else 0.55)}"/>'
        for (x, y) in nodes
    )
    # pulse rings around highlight
    rings = ""
    for r, op in [(22, 0.4), (30, 0.25), (40, 0.12)]:
        rings += f'\n  <circle cx="{highlight[0]}" cy="{highlight[1]}" r="{r}" fill="none" stroke="{ACCENT}" stroke-opacity="{op}" stroke-width="1"/>'
    return svg_wrap(f'{lines}\n  {circles}{rings}', bg=INK_SOFT, pattern_overlay='<rect width="{W}" height="{H}" fill="url(#dots)"/>'.format(W=W, H=H))


# ──────────────────────────────────────────────────────────
# 3. EtcdGuardian — shield / protection
# ──────────────────────────────────────────────────────────
def etcd_guardian():
    # shield with concentric layers, lock at center
    cx, cy = W // 2, H // 2
    layers = []
    for r in [80, 60, 40]:
        layers.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{WHITE}" stroke-opacity="0.2" stroke-width="1"/>')
    # shield outline (hex)
    shield = f'''
  <path d="M {cx} 30 L {cx+70} 60 L {cx+70} 130 L {cx} 170 L {cx-70} 130 L {cx-70} 60 Z"
        fill="{ACCENT}" fill-opacity="0.18" stroke="{ACCENT}" stroke-width="1.5" stroke-opacity="0.9"/>
  <path d="M {cx} 50 L {cx+50} 70 L {cx+50} 120 L {cx} 150 L {cx-50} 120 L {cx-50} 70 Z"
        fill="none" stroke="{WHITE}" stroke-opacity="0.5" stroke-width="1"/>
  <circle cx="{cx}" cy="{cy-5}" r="8" fill="{WHITE}"/>
  <rect x="{cx-5}" y="{cy-5}" width="10" height="20" fill="{WHITE}"/>
'''
    # backup arrows
    arrows = ""
    for i, (x, y, dx, dy) in enumerate([(80, 40, 25, 15), (520, 40, -25, 15), (80, 160, 25, -15), (520, 160, -25, -15)]):
        arrows += f'\n  <path d="M {x} {y} l {dx} {dy} m -{dx} -{dy} l {abs(dx)*0.6} {abs(dy)*0.6} m -{abs(dx)*0.6} -{abs(dy)*0.6} l {abs(dx)} {dy}" fill="none" stroke="{WHITE}" stroke-opacity="0.4" stroke-width="1"/>'
    return svg_wrap(f'{"".join(layers)}\n  {shield}\n  {arrows}', bg=INK_SOFT, pattern_overlay='<rect width="{W}" height="{H}" fill="url(#grid)"/>'.format(W=W, H=H))


# ──────────────────────────────────────────────────────────
# 4. LeetCast — sound wave / podcast
# ──────────────────────────────────────────────────────────
def leetcast():
    # waveform bars across the canvas
    import random
    random.seed(7)
    bars = []
    bar_count = 40
    bar_w = 6
    gap = (W - 80 - bar_count * bar_w) / (bar_count - 1)
    for i in range(bar_count):
        x = 40 + i * (bar_w + gap)
        # waveform shape: sin * exp
        h = abs(int(60 * (1 - abs(i - bar_count/2) / (bar_count/2)) * (0.5 + 0.5 * random.random())))
        h = max(8, h)
        y = (H - h) / 2
        is_accent = random.random() < 0.15
        color = ACCENT if is_accent else WHITE
        op = 0.95 if is_accent else 0.7
        bars.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w}" height="{h}" rx="1" fill="{color}" fill-opacity="{op}"/>')
    # play triangle
    tri = f'<polygon points="280,80 280,120 320,100" fill="{ACCENT}" fill-opacity="0.9"/>'
    return svg_wrap(f'{"".join(bars)}\n  {tri}', bg=INK_SOFT)


# ──────────────────────────────────────────────────────────
# 5. mcp4coder — connector plugs
# ──────────────────────────────────────────────────────────
def mcp4coder():
    # multiple "plug" icons connecting in a network
    import random
    random.seed(3)
    plugs = [
        (100, 100, ACCENT, 1.0),  # source
        (260, 60, WHITE, 0.85),
        (260, 140, WHITE, 0.85),
        (420, 100, ACCENT, 1.0),  # sink
        (180, 30, WHITE, 0.5),
        (180, 170, WHITE, 0.5),
        (340, 30, WHITE, 0.5),
        (340, 170, WHITE, 0.5),
        (500, 100, WHITE, 0.7),
    ]
    # lines first
    connections = [
        (0, 1), (0, 2), (1, 3), (2, 3), (3, 8),
        (0, 4), (0, 5), (3, 6), (3, 7),
        (1, 4), (1, 6), (2, 5), (2, 7),
    ]
    lines = "\n  ".join(
        f'<line x1="{plugs[a][0]}" y1="{plugs[a][1]}" x2="{plugs[b][0]}" y2="{plugs[b][1]}" stroke="{WHITE}" stroke-opacity="0.25" stroke-width="0.8"/>'
        for a, b in connections
    )
    # nodes — square plugs
    nodes = "\n  ".join(
        f'<rect x="{x-10}" y="{y-10}" width="20" height="20" rx="3" fill="{color}" fill-opacity="{op}" transform="rotate(45 {x} {y})"/>'
        for (x, y, color, op) in plugs
    )
    return svg_wrap(f'{lines}\n  {nodes}', bg=INK_SOFT, pattern_overlay='<rect width="{W}" height="{H}" fill="url(#diagonal)"/>'.format(W=W, H=H))


# ──────────────────────────────────────────────────────────
# 6. OpenDemo — grid of demo squares
# ──────────────────────────────────────────────────────────
def opendemo():
    # 8x4 grid of squares, some filled with accent
    import random
    random.seed(11)
    grid = []
    cols, rows = 10, 4
    cell_w, cell_h = 50, 35
    start_x, start_y = 50, 30
    for r in range(rows):
        for c in range(cols):
            x = start_x + c * (cell_w + 4)
            y = start_y + r * (cell_h + 4)
            v = random.random()
            if v < 0.12:
                fill = ACCENT
                op = 0.95
            elif v < 0.35:
                fill = WHITE
                op = 0.7
            elif v < 0.55:
                fill = WHITE
                op = 0.3
            else:
                fill = "none"
                op = 0
            stroke = WHITE
            so = 0.2
            grid.append(f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" rx="2" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-opacity="{so}" stroke-width="0.6"/>')
    return svg_wrap("\n  ".join(grid), bg=INK_SOFT)


# ──────────────────────────────────────────────────────────

BANNERS = {
    "resolve-agent": resolve_agent,
    "kudig": kudig,
    "etcd-guardian": etcd_guardian,
    "leetcast": leetcast,
    "mcp4coder": mcp4coder,
    "opendemo": opendemo,
}


def main():
    for name, fn in BANNERS.items():
        path = os.path.join(BANNER_DIR, f"{name}.svg")
        with open(path, "w") as f:
            f.write(fn())
        size = os.path.getsize(path)
        print(f"  Wrote: {path}  ({size}B)")


if __name__ == "__main__":
    main()
