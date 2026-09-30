import numpy as np, matplotlib.pyplot as plt
from fig_style import *
apply_style()
fig, axs = plt.subplots(1, 2, figsize=(7.3, 2.9), gridspec_kw={"width_ratios": [1.45, 1]})
modes = ["Pull-out", "Pull-out with bar yielding", "Interface slip", "Interface slip with splitting", "Mortar shear slippage", "Zero-bond slip-out"]
cnt = {"Epoxy": [7, 2, 0, 0, 0, 0], "Non-shrink grout": [0, 0, 6, 1, 0, 2], "Cement mortar": [0, 0, 0, 0, 4, 5]}
ax = axs[0]; w = .26; y = np.arange(len(modes))[::-1]
for j, ag in enumerate(cnt):
    for yi, v in zip(y, cnt[ag]):
        if v == 0: continue
        ax.barh(yi + (1 - j) * w, v, w * .92, color="white", edgecolor=AGENT[ag], hatch=AGENT_HATCH[ag], lw=.9, label=ag, zorder=3)
        ax.text(v + .15, yi + (1 - j) * w, str(v), va="center", fontsize=8.4)
ax.set_yticks(y); ax.set_yticklabels(modes); ax.set_xlim(0, 9); ax.set_ylim(-.6, 5.6)
ax.set_xlabel("Specimen groups (of 9 per agent)"); ax.grid(axis="x", color="#dcdcd6", lw=.5, zorder=0)
h, l = ax.get_legend_handles_labels(); u = dict(zip(l, h))
ax.legend(u.values(), u.keys(), loc="center right", bbox_to_anchor=(1.0, .34), handlelength=1.6)
ax.text(.0, 1.02, "(a)", transform=ax.transAxes, fontweight="bold", fontsize=10.5)
ax = axs[1]; x = np.arange(3)
pull = [10, 6, 6]; split = [5, 9, 9]
ax.bar(x, pull, .55, color="white", edgecolor=STEEL_EDGE, hatch="////", lw=.9, label="Pull-out / slip", zorder=3)
ax.bar(x, split, .55, bottom=pull, color="white", edgecolor=WARM_EDGE, hatch="....", lw=.9, label="Splitting of cube", zorder=3)
for xi, p, s in zip(x, pull, split):
    kw = dict(ha="center", va="center", fontsize=8.6, bbox=dict(boxstyle="square,pad=0.2", facecolor="white", edgecolor="none", alpha=.92), zorder=6)
    ax.text(xi, p / 2, str(p), **kw); ax.text(xi, p + s / 2, str(s), **kw)
ax.set_xticks(x); ax.set_xticklabels(["4.9", "14.7", "23.5"]); ax.set_ylim(0, 19.5); ax.set_xlim(-.6, 2.6)
ax.set_xlabel("Nominal $f'_c$ (MPa)"); ax.set_ylabel("GFRP specimens (of 15)")
ax.legend(loc="upper left", ncol=1, handlelength=1.6, bbox_to_anchor=(0, 1.0)); ax.set_ylim(0, 22)
ax.text(.0, 1.02, "(b)", transform=ax.transAxes, fontweight="bold", fontsize=10.5)
fig.tight_layout(w_pad=1.2); save(fig, "../figs/fig6.png")
