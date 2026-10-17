"""Fig. 1 - re-plotted from values read off Toyoda et al. (2022, Fig. 7, CC BY 4.0): 36 / 36 / 6 / 0."""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from fig_style import *

apply_style()
levels = ["Level 1\nReaction", "Level 2\nLearning", "Level 3\nBehaviour", "Level 4\nResults"]
vals = [36, 36, 6, 0]
cols = [ACCENT, ACCENT, WARM, "white"]
edges = [ACCENT_EDGE, ACCENT_EDGE, WARM_EDGE, STEEL_EDGE]

fig, ax = plt.subplots(figsize=(5.4, 3.3))
x = range(4)
bars = ax.bar(x, vals, width=0.58, color=cols, edgecolor=edges, linewidth=0.9, zorder=3)
# Level 4: no study measured results -> keep a dashed baseline marker rather than an invisible bar
ax.plot([3 - 0.29, 3 + 0.29], [0.35, 0.35], color=STEEL_EDGE, lw=1.0, ls=(0, (3, 2)), zorder=4)
ax.text(3, 5.2, "no study measured\nresults", ha="center", va="center", fontsize=7.5, color=INK_SEC, style="italic")

for i, v in enumerate(vals):
    ax.text(i, v + 0.9, str(v), ha="center", va="bottom", fontsize=9.5, fontweight="bold", color=INK, zorder=5)

ax.set_xticks(list(x))
ax.set_xticklabels(levels, fontsize=8.5)
ax.set_ylim(0, 42)
ax.set_yticks(range(0, 41, 10))
ax.set_ylabel("Frequency of usage (count)", fontsize=8.5, labelpad=6)
ax.set_xlabel("Kirkpatrick evaluation level", fontsize=8.5, labelpad=7)
ax.yaxis.grid(True, color="#d9d9d5", lw=0.6, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.spines["left"].set_linewidth(0.8)
ax.spines["bottom"].set_linewidth(0.8)
ax.tick_params(axis="both", length=3, width=0.8, labelsize=8.5)
ax.tick_params(axis="x", length=0, pad=5)

# bracket over Levels 3-4 (claims about workplace capability usually concern these levels)
y0 = 39.2
ax.plot([1.62, 1.62, 3.38, 3.38], [y0 - 1.2, y0, y0, y0 - 1.2], color=WARM_EDGE, lw=0.8, clip_on=False, zorder=4)
ax.text(3.38, y0 + 0.9, "Levels typically implied by workplace-capability claims", ha="right", va="bottom",
        fontsize=7.5, color=WARM_EDGE, style="italic")
ax.set_ylim(0, 44)
fig.subplots_adjust(left=0.12, right=0.98, top=0.97, bottom=0.2)
save(fig, "fig1_kirkpatrick.png")
