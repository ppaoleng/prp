"""Conceptual flow diagram: RCA (replacing sand) + bamboo biochar (replacing cement) -> paving block."""
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from fig_style import (apply_style, save, INK, INK_SEC, ACCENT, ACCENT_EDGE, ACCENT_TINT,
                       WARM, WARM_EDGE, WARM_TINT, NEUTRAL_FILL)

apply_style()
W, H = 100.0, 69.4
fig, ax = plt.subplots(figsize=(7.2, 7.2 * H / W))
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.set_aspect("equal")
ax.axis("off")


def box(x0, y0, x1, y1, fc, ec, lw=0.9, z=2):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=fc, edgecolor=ec,
                           linewidth=lw, zorder=z, joinstyle="miter"))


def bar(x0, y0, x1, y1, fc):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=fc, edgecolor=fc,
                           linewidth=0, zorder=3))


def outline(x0, y0, x1, y1, ec, lw=0.9):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor="none", edgecolor=ec,
                           linewidth=lw, zorder=4, joinstyle="miter"))


def arrow(pts, color, lw=1.0, head=True):
    xs, ys = zip(*pts)
    if head:
        ax.plot(xs, ys[:-1] + (ys[-1] + 1.0,), color=color, lw=lw,
                solid_capstyle="butt", solid_joinstyle="miter", zorder=1)
        x, y = pts[-1]
        ax.add_patch(plt.Polygon([[x, y], [x - 0.8, y + 1.8], [x + 0.8, y + 1.8]],
                                 closed=True, facecolor=color, edgecolor=color, lw=0.3, zorder=5))
    else:
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="butt", solid_joinstyle="miter", zorder=1)


def label(x, y, title, sub, fs_t=8.6, fs_s=8.0):
    ax.text(x, y + 1.9, title, ha="center", va="center", fontsize=fs_t, fontweight="bold",
            color=INK, zorder=5)
    ax.text(x, y - 1.9, sub, ha="center", va="center", fontsize=fs_s, color=INK, zorder=5)


# ---------------------------------------------------------------- geometry
XL, XR = 27.0, 73.0          # stream centre lines
BW = 41.0                    # box width, tiers 1-2

# ---------------------------------------------------------------- tier 1 (waste streams)
for xc, tint, edge, bar_c, t, s in [
    (XL, ACCENT_TINT, ACCENT_EDGE, ACCENT, "Construction & demolition waste", "(waste concrete)"),
    (XR, WARM_TINT, WARM_EDGE, WARM, "Bamboo biomass residue", "(pyrolysed to biochar)"),
]:
    box(xc - BW / 2, 55, xc + BW / 2, 67, tint, edge)
    bar(xc - BW / 2, 65.9, xc + BW / 2, 67, bar_c)
    outline(xc - BW / 2, 55, xc + BW / 2, 67, edge)
    label(xc, 60.0, t, s)

# ---------------------------------------------------------------- tier 2 (substitute materials)
for xc, edge, t, mat in [
    (XL, ACCENT_EDGE, "Recycled concrete aggregate", r"partial replacement of $\mathbf{sand}$"),
    (XR, WARM_EDGE, "Bamboo biochar", r"partial replacement of $\mathbf{cement}$"),
]:
    box(xc - BW / 2, 40, xc + BW / 2, 50, "white", edge)
    label(xc, 45.0, t, mat)

arrow([(XL, 55), (XL, 50)], ACCENT_EDGE)
arrow([(XR, 55), (XR, 50)], WARM_EDGE)

# ---------------------------------------------------------------- dashed study boundary
DX0, DX1, DY0, DY1 = 2.0, 98.0, 1.0, 32.5
ax.add_patch(Rectangle((DX0, DY0), DX1 - DX0, DY1 - DY0, facecolor="none", edgecolor=INK_SEC,
                       linewidth=0.9, linestyle=(0, (5, 3)), zorder=0))
ax.text(DX0 + 2.5, DY1, "This study", ha="left", va="center", fontsize=8.0, color=INK_SEC,
        bbox=dict(boxstyle="square,pad=0.25", facecolor="white", edgecolor="none"), zorder=6)

# ---------------------------------------------------------------- tier 3 (paving block)
PX0, PX1, PY0, PY1 = 20.0, 80.0, 19.5, 29.5
box(PX0, PY0, PX1, PY1, NEUTRAL_FILL, INK, lw=0)
bar(PX0, PY1 - 1.2, 50.0, PY1, ACCENT)     # left half  = recycled-aggregate stream
bar(50.0, PY1 - 1.2, PX1, PY1, WARM)       # right half = biochar stream
outline(PX0, PY0, PX1, PY1, INK, lw=1.2)
label(50.0, 23.7, "Concrete paving block", "(both substitutions combined in one mix)",
      fs_t=9.2, fs_s=8.0)

# elbow connectors from tier 2 into the block (merge)
YM = 35.5
arrow([(XL, 40), (XL, YM), (38.0, YM), (38.0, PY1)], ACCENT_EDGE)
arrow([(XR, 40), (XR, YM), (62.0, YM), (62.0, PY1)], WARM_EDGE)

# ---------------------------------------------------------------- performance criteria
criteria = ["Compressive\nstrength", "Density", "Water\nabsorption", "Skid\nresistance",
            "Carbon\nfootprint"]
CX0, CX1, GAP = 4.0, 96.0, 2.6
CW = (CX1 - CX0 - GAP * 4) / 5
CY0, CY1 = 3.5, 12.5
centres = []
for i, name in enumerate(criteria):
    x0 = CX0 + i * (CW + GAP)
    box(x0, CY0, x0 + CW, CY1, "white", INK_SEC)
    cy = (CY0 + CY1) / 2
    lines = name.split("\n")
    # fixed baselines (cap-height centred) so text sits at the same level in every box
    for k, ln in enumerate(lines):
        yb = cy - 1.1 + (len(lines) - 1) * 1.15 - k * 2.3
        ax.text(x0 + CW / 2, yb, ln, ha="center", va="baseline", fontsize=8.4, color=INK, zorder=5)
    centres.append(x0 + CW / 2)

YB = 16.5
arrow([(50.0, PY0), (50.0, YB)], INK, head=False)
arrow([(centres[0], YB), (centres[-1], YB)], INK, head=False)
for xc in centres:
    arrow([(xc, YB), (xc, CY1)], INK)

os.makedirs("out", exist_ok=True)
save(fig, "out/fig_concept_flow")
