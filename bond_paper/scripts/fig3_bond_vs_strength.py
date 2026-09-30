import numpy as np, matplotlib.pyplot as plt
from fig_style import *; from bond_data import *
apply_style()
MK = {"Epoxy": "o", "Non-shrink grout": "s", "Cement mortar": "D"}
off = {"Epoxy": -0.17, "Non-shrink grout": 0.0, "Cement mortar": 0.17}
fig, axs = plt.subplots(1, 3, figsize=(7.3, 2.95), sharey=True)
for ax, d, lab in zip(axs, DB, "abc"):
    for ag, g in PLAIN.items():
        x = np.arange(3) + off[ag]; m = np.array([v[0] for v in g[d]]); s = np.array([v[1] for v in g[d]])
        c = AGENT[ag]
        ax.plot(x, m, color=c, lw=1.1, zorder=2)
        if ag != "Cement mortar":
            ax.errorbar(x, m, yerr=s, fmt="none", ecolor=c, elinewidth=0.9, capsize=2.6, capthick=0.9, zorder=3)
        ax.plot(x, m, MK[ag], ms=5.6, mfc=("white" if ag == "Cement mortar" else c), mec=c, mew=1.1, zorder=4)
    ax.set_xticks(range(3)); ax.set_xticklabels(["4.9", "14.7", "23.5"]); ax.set_xlim(-.55, 2.55)
    ax.set_ylim(-.45, 8.2); ax.axhline(0, color=INK, lw=.5, zorder=1)
    ax.set_xlabel("Nominal $f'_c$ (MPa)"); ax.grid(axis="y", color="#dcdcd6", lw=.5, zorder=0)
    ax.set_title(f"({lab})  RB{d}", loc="left", fontsize=10, fontweight="bold", pad=3)
axs[0].set_ylabel(r"Bond stress $\tau$ (MPa)")
h = [plt.Line2D([], [], color=AGENT[a], marker=MK[a], mfc=("white" if a == "Cement mortar" else AGENT[a]), mew=1.1, ms=5.6, label=a) for a in PLAIN]
fig.legend(handles=h, loc="lower center", ncol=3, bbox_to_anchor=(.5, -.07), columnspacing=2.2)
fig.tight_layout(w_pad=.8); save(fig, "../figs/fig3.png")
