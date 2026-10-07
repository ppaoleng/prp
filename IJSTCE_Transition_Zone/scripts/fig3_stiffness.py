"""Fig. 3 - peak approach-side static stiffness of M1-M5 (Table 5)."""
import numpy as np
from matplotlib.lines import Line2D
import fig_style as S
from data import MODELS, KD, RHO, K_BRIDGE

S.apply_style()
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9, 3.25))
fig.subplots_adjust(left=0.13, right=0.985, top=0.97, bottom=0.30)

x = np.arange(len(MODELS))
for i, m in enumerate(MODELS):
    S.hatched_bar(ax, i, KD[m], 0.62, S.SERIES[m], S.HATCH[m])
    ax.text(i, KD[m] + 5, f"{KD[m]}", ha="center", va="bottom", fontsize=8.8, fontweight="bold", color=S.INK)
    ax.text(i, KD[m] + 5 + 19, f"({RHO[m]:.2f})", ha="center", va="bottom", fontsize=8.0, color=S.INK_SEC)

# bridge reference
ax.axhline(K_BRIDGE, color=S.INK, lw=0.9, ls=(0, (4.5, 2.5)), zorder=2)
ax.text(-0.46, K_BRIDGE + 6, "Bridge, 264", ha="left", va="bottom", fontsize=8.3, color=S.INK)

ax.set_xlim(-0.55, len(MODELS) - 0.45)
ax.set_ylim(0, 300)
ax.set_yticks(range(0, 301, 50))
ax.set_xticks(x)
ax.set_xticklabels(MODELS, fontsize=8.8)
ax.tick_params(axis="x", length=3, pad=2)
ax.yaxis.grid(True, color=S.GRID, lw=0.5, zorder=0)
ax.set_axisbelow(True)
ax.set_ylabel(r"Peak approach-side stiffness, $k_d$ (kN/mm)")

# configuration matrix under the axis (self-explanatory, no abbreviations needed)
rows = [("PU-injected ballast", [0, 1, 1, 1, 1]),
        ("Auxiliary rail", [0, 0, 1, 0, 1]),
        ("Enlarged sleepers", [0, 0, 0, 1, 1])]
y_rows = [-0.205, -0.285, -0.365]
tr = ax.get_xaxis_transform()
for (name, flags), yy in zip(rows, y_rows):
    ax.text(-0.62, yy, name, transform=tr, ha="right", va="center", fontsize=7.8, color=S.INK, clip_on=False)
    for i, f in enumerate(flags):
        if f:
            ax.plot([i], [yy], marker="s", ms=4.6, mfc=S.SERIES[MODELS[i]], mec=S.INK, mew=0.5,
                    transform=tr, clip_on=False, ls="none")
        else:
            ax.plot([i], [yy], marker="_", ms=5.0, mfc="none", mec="#9a9a95", mew=0.9,
                    transform=tr, clip_on=False, ls="none")
# thin rule separating the matrix from the tick labels
ax.plot([-0.55, len(MODELS) - 0.45], [-0.145, -0.145], transform=tr, color=S.GRID, lw=0.6, clip_on=False)
S.save(fig, "Fig3_stiffness")
