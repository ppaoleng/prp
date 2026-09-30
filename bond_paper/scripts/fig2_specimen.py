import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Polygon
from PIL import Image
from fig_style import *
apply_style()
import os
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "source", "fig2_v2_photo_composite.png")
k = 3091 / 2000.0
def crop(x1, y1, x2, y2):   # coordinates of the v2 composite as displayed (2000 px wide)
    return Image.open(SRC).convert("RGB").crop(tuple(int(v * k) for v in (x1, y1, x2, y2)))
photos = {"b": crop(823, 22, 1355, 436), "c": crop(1447, 22, 1978, 436),
          "d": crop(823, 517, 1355, 930), "e": crop(1447, 517, 1978, 930)}
fig = plt.figure(figsize=(7.4, 3.75))
gs = fig.add_gridspec(2, 3, width_ratios=[1.35, .72, .72], wspace=.06, hspace=.07, left=0, right=1, top=.96, bottom=0)
ax = fig.add_subplot(gs[:, 0]); ax.set_aspect("equal"); ax.axis("off")
lw = .9
# concrete cube 150 x 150 (mm, drawn to scale), hole with bonding agent annulus, bar
ax.add_patch(Rectangle((0, 0), 150, 150, fc=CONCRETE, ec=LINE, lw=lw, hatch="..", zorder=1))
bx, bw, aw = 75, 14, 7
ax.add_patch(Rectangle((bx - bw / 2 - aw, 0), bw + 2 * aw, 140, fc="white", ec="none", zorder=2))
for xs in (bx - bw / 2 - aw, bx + bw / 2):
    ax.add_patch(Rectangle((xs, 0), aw, 140, fc="white", ec=ACCENT_EDGE, lw=.6, hatch="xxxx", zorder=3))
ax.add_patch(Rectangle((bx - bw / 2, -45), bw, 45 + 172, fc=STEEL, ec=STEEL_EDGE, lw=lw, hatch="////", zorder=4))
ax.add_patch(Rectangle((-22, -10), 194, 10, fc="#d9d9d4", ec=LINE, lw=lw, hatch="///", zorder=5))        # reaction plate
ax.add_patch(Rectangle((bx - bw / 2 - 6, -10), bw + 12, 10, fc="white", ec="none", zorder=5))
ax.add_patch(Rectangle((bx - bw / 2, -10), bw, 10, fc=STEEL, ec=STEEL_EDGE, lw=lw, hatch="////", zorder=6))
ax.add_patch(Rectangle((bx - 19, -68), 38, 23, fc="#e4e4df", ec=LINE, lw=lw, zorder=5))                   # UTM grip
ax.add_patch(Rectangle((bx - 9, 172), 18, 26, fc="#e4e4df", ec=LINE, lw=lw, zorder=5))                   # LVDT body
ax.plot([bx, bx], [198, 214], color=LINE, lw=lw)
ax.annotate("", xy=(bx, -92), xytext=(bx, -68), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.1, mutation_scale=9))
ax.text(bx + 8, -84, "$P$", fontsize=10, style="italic", va="center")
def dim(x, y0, y1, txt, rot=90, side=-1):
    ax.annotate("", xy=(x, y0), xytext=(x, y1), arrowprops=dict(arrowstyle="<->", color=INK_SEC, lw=.8, shrinkA=0, shrinkB=0))
    ax.text(x + side * 8, (y0 + y1) / 2, txt, rotation=rot, ha="center", va="center", fontsize=8.6, color=INK,
            bbox=dict(boxstyle="square,pad=0.15", facecolor="white", edgecolor="none"), zorder=9)
dim(-16, 0, 140, r"$l_e$ = 140 mm"); dim(164, 0, 150, "150 mm", side=1)
ax.plot([-20, 0], [140, 140], color=INK_SEC, lw=.6, ls=":"); ax.plot([-20, 0], [0, 0], color=INK_SEC, lw=.6, ls=":")
ax.plot([150, 170], [150, 150], color=INK_SEC, lw=.6, ls=":")
def lead(xy, xyt, s, ha="left"):
    ax.annotate(s, xy=xy, xytext=xyt, fontsize=8.6, ha=ha, va="center", arrowprops=dict(arrowstyle="-", color=INK_SEC, lw=.7, shrinkA=0, shrinkB=0),
                bbox=dict(boxstyle="square,pad=0.15", facecolor="white", edgecolor="none"), zorder=10)
lead((bx + bw / 2 + aw / 2, 110), (200, 122), "Bonding agent\n(post-installed)")
lead((bx, 165), (-28, 178), "Bar", ha="right")
lead((128, 35), (200, 28), "Concrete cube")
lead((140, -5), (200, -28), "Reaction plate")
lead((bx + 9, 184), (200, 186), "LVDT")
lead((bx + 6, -56), (-30, -58), "UTM grip", ha="right")
ax.set_xlim(-75, 285); ax.set_ylim(-105, 225)
panel_label(ax, "(a)", x=0.0, y=.94)
for (key, r, c) in (("b", 0, 1), ("c", 0, 2), ("d", 1, 1), ("e", 1, 2)):
    a = fig.add_subplot(gs[r, c]); a.imshow(photos[key]); a.set_xticks([]); a.set_yticks([])
    for s in a.spines.values(): s.set_visible(True); s.set_linewidth(.8); s.set_color(LINE)
    a.text(.04, .94, f"({key})", transform=a.transAxes, color="white", fontweight="bold", fontsize=10.5, va="top",
           bbox=dict(boxstyle="square,pad=0.22", facecolor="#333333", edgecolor="none", alpha=.85))
save(fig, "../figs/fig2.png")
