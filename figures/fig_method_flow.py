"""Research methodology flow chart (6 stages -> conclusions). English-only, journal style."""
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

from fig_style import (apply_style, save, INK, INK_SEC, LINE, NEUTRAL_FILL, PANEL_FILL, SLATE,
                       OK_GREEN, OK_TINT, STREAM_RCA, STREAM_BIOCHAR)

apply_style()

W = 100.0
U = 0.072                                  # inches per data unit (7.2 in / 100)
FS = {"h": 8.8, "b": 7.8, "m": 7.8, "s": 7.0}
GAP = 2.8                                  # arrow gap between stages
HDR = 5.4                                  # header band height inside a panel
PAD_B = 1.8

# ------------------------------------------------------------------ content
P1_KEYS = ("Biochar in cementitious materials  ·  Recycled concrete aggregate (RCA)  ·  "
           "Concrete paving blocks  ·  Slip resistance  ·  LCA")

STAGES = [
    dict(num="1.", title="Literature review and gap analysis", kind="intro", h=8.8),
    dict(num="2.", title="Materials", bh=10.8, boxes=[
        dict(lines=[("Portland cement", "m"), ("OPC Type I", "s")]),
        dict(lines=[("Fine aggregate (sand)", "m"), ("passing No. 4 sieve", "s")]),
        dict(lines=[("Crushed stone", "m")]),
        dict(lines=[("Recycled concrete", "m"), ("aggregate (RCA)", "m"),
                    ("lab-waste concrete,", "s"), ("0.30–2.36 mm", "s")], style=STREAM_RCA),
        dict(lines=[("Bamboo biochar", "m"), ("No. 100 / 200", "s")], style=STREAM_BIOCHAR),
    ]),
    dict(num="3.", title="Mix design (cement : sand : stone)", bh=10.0, boxes=[
        dict(lines=[("Series 1  ·  RCA at 50 % of fine aggregate", "b"),
                    ("Cement replaced by biochar: 5–25 %", "m"),
                    ("designed 5–25 %; tested 0–15 %", "s")], style=STREAM_BIOCHAR),
        dict(lines=[("Series 2  ·  biochar constant at 48 g", "b"),
                    ("RCA replacing sand: 0, 5, 10, 15 %", "m")], style=STREAM_RCA),
    ]),
    dict(num="4.", title="Mixing, forming and curing", bh=7.4, boxes=[
        dict(lines=[("Mechanical mixing", "m"), ("mortar mixer", "s")]),
        dict(lines=[("Hand-tamped zig-zag block", "m"), ("6 cm thick", "s")]),
        dict(lines=[("Curing: 7, 14 and 28 days", "m"), ("3 blocks per age", "s")]),
    ]),
    dict(num="5.", title="Testing of block properties", bh=7.4, boxes=[
        dict(lines=[("Density", "m")]),
        dict(lines=[("Compressive strength", "m"), ("TIS 827-2565", "s")]),
        dict(lines=[("Water absorption", "m"), ("72 h", "s")]),
        dict(lines=[("Slip resistance (BPT)", "b"), ("dry / wet", "s")],
             style=dict(fill=OK_TINT, edge=OK_GREEN)),
    ]),
    dict(num="6.", title="Results analysis and screening LCA", bh=7.4, boxes=[
        dict(lines=[("Statistical analysis", "m"), ("ANOVA / Tukey", "s")]),
        dict(lines=[("Material-mechanics models", "m"), ("porosity–strength, maturity", "s")]),
        dict(lines=[("GWP per 1 m³ and ci", "m"), ("cradle-to-gate", "s")]),
    ]),
]
FINAL = dict(h=7.6, lines=[("Optimum mix selection, benchmarking and recommendations", "b"),
                           ("comparison with standard criteria and other studies", "s")])

# ------------------------------------------------------------------ layout
for st in STAGES:
    st.setdefault("h", HDR + st.get("bh", 0) + PAD_B)
H = sum(s["h"] for s in STAGES) + FINAL["h"] + GAP * len(STAGES) + 0.6

fig = plt.figure(figsize=(W * U, H * U))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")

checks = []   # (text artist, (x0, y0, x1, y1)) -> overflow test after drawing


def rect(x0, y0, x1, y1, fc, ec, lw=0.8, z=2):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=fc, edgecolor=ec,
                           linewidth=lw, zorder=z, joinstyle="miter"))


def arrow_down(x, y_from, y_to, color=INK, lw=1.0):
    ax.plot([x, x], [y_from, y_to + 1.0], color=color, lw=lw, solid_capstyle="butt", zorder=1)
    ax.add_patch(Polygon([[x, y_to], [x - 0.8, y_to + 1.7], [x + 0.8, y_to + 1.7]], closed=True,
                         facecolor=color, edgecolor=color, lw=0.3, zorder=5))


def put_lines(x0, y0, x1, y1, lines, white=False):
    """Centre a block of text lines in a box using fixed baselines (identical across boxes)."""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    pitch = [2.05 if lines[i][1] == "s" else 2.25 for i in range(1, len(lines))]
    span = sum(pitch)
    base = cy + span / 2 - 0.34
    for i, (txt, kind) in enumerate(lines):
        if i:
            base -= pitch[i - 1]
        col = ("white" if kind != "s" else "#d9dcdf") if white else (INK_SEC if kind == "s" else INK)
        t = ax.text(cx, base, txt, ha="center", va="baseline", fontsize=FS[kind], color=col,
                    fontweight="bold" if kind == "b" else "normal", zorder=6)
        checks.append((t, (x0, y0, x1, y1)))


y = H - 0.3
for i, st in enumerate(STAGES):
    top, bot = y, y - st["h"]
    rect(0.0, bot, W, top, NEUTRAL_FILL if st.get("kind") == "intro" else PANEL_FILL, INK_SEC)
    ax.text(2.4, top - 2.9, st["num"], ha="left", va="center", fontsize=FS["h"], fontweight="bold",
            color=INK, zorder=6)
    ax.text(5.9, top - 2.9, st["title"], ha="left", va="center", fontsize=FS["h"],
            fontweight="bold", color=INK, zorder=6)
    if st.get("kind") == "intro":
        t = ax.text(W / 2, top - 6.4, P1_KEYS, ha="center", va="center", fontsize=FS["s"] + 0.2,
                    color=INK_SEC, zorder=6)
        checks.append((t, (0, bot, W, top)))
    else:
        n, g = len(st["boxes"]), 2.0
        bw = (W - 4.0 - g * (n - 1)) / n
        by1 = top - HDR
        by0 = by1 - st["bh"]
        for k, b in enumerate(st["boxes"]):
            x0 = 2.0 + k * (bw + g)
            sty = b.get("style")
            rect(x0, by0, x0 + bw, by1, sty["fill"] if sty else "white",
                 sty["edge"] if sty else LINE, lw=1.1 if sty and sty["edge"] == OK_GREEN else 0.8, z=3)
            put_lines(x0, by0, x0 + bw, by1, b["lines"])
    y = bot
    arrow_down(W / 2, bot, bot - GAP)
    y = bot - GAP

# concluding box
top, bot = y, y - FINAL["h"]
rect(0.0, bot, W, top, SLATE, SLATE, z=2)
put_lines(0.0, bot, W, top, FINAL["lines"], white=True)

# ------------------------------------------------------------------ overflow check
fig.canvas.draw()
inv = ax.transData.inverted()
bad = 0
for t, (x0, y0, x1, y1) in checks:
    bb = t.get_window_extent()
    (a0, b0), (a1, b1) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    if a0 < x0 + 0.8 or a1 > x1 - 0.8 or b0 < y0 + 0.5 or b1 > y1 - 0.5:
        bad += 1
        print(f"OVERFLOW: {t.get_text()!r}  text x[{a0:.1f},{a1:.1f}] y[{b0:.1f},{b1:.1f}]  "
              f"box x[{x0:.1f},{x1:.1f}] y[{y0:.1f},{y1:.1f}]")
print(f"figure {W * U:.2f} x {H * U:.2f} in ; overflow count = {bad}")

os.makedirs("out", exist_ok=True)
save(fig, "out/fig_method_flow")
