"""Fig. 5 - reduction in peak contact force relative to M1 (Table 7)."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import fig_style as S
from data import SPEEDS, REDUCTION

S.apply_style()
fig, ax = plt.subplots(figsize=(5.4, 3.35))
fig.subplots_adjust(left=0.105, right=0.985, top=0.88, bottom=0.14)

models = ["M2", "M3", "M4", "M5"]
bw, gap = 0.19, 0.012
centres = np.arange(len(SPEEDS))
for j, m in enumerate(models):
    off = (j - 1.5) * (bw + gap)
    for i in range(len(SPEEDS)):
        v = REDUCTION[m][i]
        S.hatched_bar(ax, centres[i] + off, v, bw, S.SERIES[m], S.HATCH[m], lw=0.6)
        ax.text(centres[i] + off, v + 0.35, f"{v:.1f}", ha="center", va="bottom", fontsize=6.6, color=S.INK)

ax.set_xticks(centres)
ax.set_xticklabels(SPEEDS)
ax.set_xlim(-0.55, len(SPEEDS) - 0.45)
ax.set_ylim(0, 27)
ax.set_yticks(range(0, 26, 5))
ax.yaxis.grid(True, color=S.GRID, lw=0.5, zorder=0)
ax.set_axisbelow(True)
ax.set_xlabel("Train speed (km/h)")
ax.set_ylabel("Reduction in peak contact force\nrelative to M1 (%)")
handles = [Patch(facecolor=S.SERIES[m], edgecolor=S.INK, linewidth=0.6, hatch=S.HATCH[m]) for m in models]
import matplotlib as mpl
with mpl.rc_context({"hatch.color": "white"}):
    pass
labels = [S.LABEL[m] for m in models]
fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.56, 1.0), ncol=4, frameon=False,
           handlelength=1.6, handleheight=0.9, columnspacing=1.0, fontsize=7.4)
S.save(fig, "Fig5_reduction")
