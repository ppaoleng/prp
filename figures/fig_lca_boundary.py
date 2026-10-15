"""LCA system-boundary diagram (cradle-to-gate, A1-A3). English-only, journal style."""
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

from fig_style import (apply_style, save, INK, INK_SEC, LINE, NEUTRAL_FILL, SLATE,
                       STREAM_RCA, STREAM_BIOCHAR)

apply_style()
plt.rcParams["hatch.linewidth"] = 0.5

W, H = 100.0, 63.0
U = 0.072                                  # inches per data unit
FS = {"h": 8.6, "b": 7.8, "m": 7.8, "s": 7.0}
HATCH = "#b3b3af"
DASH_OUT = (0, (4, 2.6))

fig = plt.figure(figsize=(W * U, H * U))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")
checks = []


def rect(x0, y0, x1, y1, fc, ec, lw=0.8, z=2, ls="-", hatch=None):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=fc, edgecolor=ec, linewidth=lw,
                           linestyle=ls, zorder=z, joinstyle="miter", hatch=hatch))


def head(x, y, dx, dy, color, z=5, L=1.7, hw=0.8):
    """Arrow head with tip at (x, y) pointing along (dx, dy) (axis-aligned)."""
    if dx:      # pointing right
        pts = [[x, y], [x - L * dx, y + hw], [x - L * dx, y - hw]]
    else:       # pointing down
        pts = [[x, y], [x - hw, y - L * dy], [x + hw, y - L * dy]]
    ax.add_patch(Polygon(pts, closed=True, facecolor=color, edgecolor=color, lw=0.3, zorder=z))


def put_lines(x0, y0, x1, y1, lines, white=False):
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    pitch = [2.05 if lines[i][1] == "s" else 2.25 for i in range(1, len(lines))]
    base = cy + sum(pitch) / 2 - 0.34
    arts = []
    for i, (txt, kind) in enumerate(lines):
        if i:
            base -= pitch[i - 1]
        t = ax.text(cx, base, txt, ha="center", va="baseline", fontsize=FS[kind],
                    color=INK_SEC if kind == "s" else INK,
                    fontweight="bold" if kind == "b" else "normal", zorder=6)
        arts.append(t)
        checks.append((t, (x0, y0, x1, y1)))
    return arts


# ------------------------------------------------------------------ system boundary
BX0, BX1, BY0, BY1 = 1.0, 69.0, 0.6, 62.4
rect(BX0, BY0, BX1, BY1, "none", SLATE, lw=1.2, z=1, ls=(0, (6, 3)))
ax.text(BX0 + 2.6, BY1 - 3.2, "System boundary (cradle-to-gate, A1–A3)", ha="left", va="center",
        fontsize=FS["h"], fontweight="bold", color=SLATE, zorder=6)

# ------------------------------------------------------------------ inputs
INPUTS = [
    dict(lines=[("Portland cement", "m")], fc=NEUTRAL_FILL, ec=LINE),
    dict(lines=[("Natural sand", "m")], fc=NEUTRAL_FILL, ec=LINE),
    dict(lines=[("Crushed stone", "m")], fc=NEUTRAL_FILL, ec=LINE),
    dict(lines=[("Recycled concrete", "m"), ("aggregate (RCA)", "m"), ("burden-free; crushing only", "s")],
         fc=STREAM_RCA["fill"], ec=STREAM_RCA["edge"]),
    dict(lines=[("Bamboo biochar", "m"), ("pyrolysis burden; residues cut-off", "s")],
         fc=STREAM_BIOCHAR["fill"], ec=STREAM_BIOCHAR["edge"]),
    dict(lines=[("Water", "m"), ("excluded as negligible", "s")], fc="white", ec=INK_SEC, ls=(0, (4, 2.6))),
]
IX0, IX1, IH, IGAP, ITOP = 4.0, 28.0, 7.4, 1.6, 55.0
BUS = 34.0
centres = []
for i, b in enumerate(INPUTS):
    top = ITOP - i * (IH + IGAP)
    y0, y1 = top - IH, top
    rect(IX0, y0, IX1, y1, b["fc"], b["ec"], lw=0.9, z=3, ls=b.get("ls", "-"))
    put_lines(IX0, y0, IX1, y1, b["lines"])
    centres.append((y0 + y1) / 2)
YC = (centres[0] + centres[-1]) / 2

# connectors: horizontal runs to a vertical bus, then one arrow into the process box
for i, yc in enumerate(centres):
    last = i == len(centres) - 1          # water: excluded flow -> dashed connector
    ax.plot([IX1, BUS], [yc, yc], color=INK_SEC if last else INK, lw=0.9, zorder=1,
            linestyle=DASH_OUT if last else "-", solid_capstyle="butt")
ax.plot([BUS, BUS], [centres[-1], centres[0]], color=INK, lw=0.9, zorder=1, solid_capstyle="butt")

# ------------------------------------------------------------------ process box
PX0, PX1, PH = 40.0, 64.0, 17.0
rect(PX0, YC - PH / 2, PX1, YC + PH / 2, "white", INK, lw=1.2, z=3)
put_lines(PX0, YC - PH / 2, PX1, YC + PH / 2,
          [("Production of 1 m³", "b"), ("of blocks", "b"),
           ("Batching · mixing · forming", "s"), ("cement + aggregate + biochar", "s")])
ax.plot([BUS, PX0 - 1.0], [YC, YC], color=INK, lw=0.9, zorder=1, solid_capstyle="butt")
head(PX0, YC, 1, 0, INK)

# functional unit
for k, ln in enumerate(["Functional unit:", "1 m³ of concrete blocks", "(1 m² of pavement ≈ 40 blocks)"]):
    t = ax.text((PX0 + PX1) / 2, YC - PH / 2 - 5.0 - k * 2.5, ln, ha="center", va="baseline",
                fontsize=FS["s"] + 0.2, color=INK_SEC, zorder=6)
    checks.append((t, (BX0, BY0, BX1, BY1)))

# ------------------------------------------------------------------ outside the boundary
OUT = [("Transport (A2)", None), ("Plant energy", "electricity and fuel for mixing"),
       ("Use stage", "construction and use"), ("End of life", "demolition / recycling")]
OX0, OX1, OH, OGAP = 78.0, 99.0, 9.8, 2.4
BUS2 = 74.5
total = len(OUT) * OH + (len(OUT) - 1) * OGAP
otop = YC + total / 2
ax.text((OX0 + OX1) / 2, BY1 - 3.2, "Outside system boundary", ha="center", va="center",
        fontsize=FS["h"], fontweight="bold", color=INK, zorder=6)
oc = []
label_artists = []
for i, (main, sub) in enumerate(OUT):
    t1 = otop - i * (OH + OGAP)
    y0, y1 = t1 - OH, t1
    rect(OX0, y0, OX1, y1, "white", HATCH, lw=0, z=2, hatch="////")           # hatching
    rect(OX0, y0, OX1, y1, "none", INK_SEC, lw=0.8, z=3, ls=DASH_OUT)          # dashed outline
    lines = [(main, "m")] + ([(sub, "s")] if sub else [])
    label_artists.append(put_lines(OX0, y0, OX1, y1, lines))
    oc.append((y0 + y1) / 2)

# dashed hand-off arrow to the whole group (bus + ticks), not to a single box
ax.plot([PX1, BUS2], [YC, YC], color=INK_SEC, lw=0.9, zorder=1, linestyle=DASH_OUT, solid_capstyle="butt")
ax.plot([BUS2, BUS2], [oc[-1], oc[0]], color=INK_SEC, lw=0.9, zorder=1, solid_capstyle="butt")
for yc in oc:
    ax.plot([BUS2, OX0 - 1.0], [yc, yc], color=INK_SEC, lw=0.9, zorder=1, linestyle=DASH_OUT, solid_capstyle="butt")
    head(OX0, yc, 1, 0, INK_SEC, L=1.4, hw=0.65)

# ------------------------------------------------------------------ white label plates over hatching (rule 6)
fig.canvas.draw()
inv = ax.transData.inverted()
for arts in label_artists:
    bbs = [a.get_window_extent() for a in arts]
    (x0, y0), (x1, y1) = inv.transform([(min(b.x0 for b in bbs), min(b.y0 for b in bbs)),
                                         (max(b.x1 for b in bbs), max(b.y1 for b in bbs))])
    rect(x0 - 1.0, y0 - 0.8, x1 + 1.0, y1 + 0.8, "white", "white", lw=0, z=5)

# ------------------------------------------------------------------ overflow check
bad = 0
for t, (x0, y0, x1, y1) in checks:
    bb = t.get_window_extent()
    (a0, b0), (a1, b1) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    if a0 < x0 + 0.8 or a1 > x1 - 0.8 or b0 < y0 + 0.4 or b1 > y1 - 0.4:
        bad += 1
        print(f"OVERFLOW: {t.get_text()!r} x[{a0:.1f},{a1:.1f}] y[{b0:.1f},{b1:.1f}] box x[{x0:.1f},{x1:.1f}] y[{y0:.1f},{y1:.1f}]")
print(f"figure {W * U:.2f} x {H * U:.2f} in ; overflow count = {bad}")

os.makedirs("out", exist_ok=True)
save(fig, "out/fig_lca_boundary")
