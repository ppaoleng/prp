import numpy as np, matplotlib.pyplot as plt
from fig_style import *; from bond_data import *
apply_style(); T = 2.1448 / np.sqrt(15)   # t(0.975, 14) / sqrt(n): 95 % CI half-width = T * SD
MK = {"Epoxy": "o", "Non-shrink grout": "s", "Cement mortar": "D"}
off = {"Epoxy": -0.18, "Non-shrink grout": 0.0, "Cement mortar": 0.18}
fig, axs = plt.subplots(1, 3, figsize=(7.3, 2.85), gridspec_kw={"width_ratios": [1, 1, 1.08]})
def dots(ax, xs, series):
    for ag, (m, ci) in series.items():
        x = np.arange(len(m)) + off[ag]; c = AGENT[ag]
        ax.plot(x, m, color=c, lw=1.1, zorder=2)
        if ag != "Cement mortar": ax.errorbar(x, m, yerr=ci, fmt="none", ecolor=c, elinewidth=.9, capsize=2.6, zorder=3)
        ax.plot(x, m, MK[ag], ms=5.6, mfc=("white" if ag == "Cement mortar" else c), mec=c, mew=1.1, zorder=4, label=ag)
    ax.set_xticks(range(len(xs))); ax.set_xticklabels(xs); ax.set_xlim(-.55, len(xs) - .45)
    ax.set_ylim(-.3, 5.4); ax.grid(axis="y", color="#dcdcd6", lw=.5, zorder=0)
# (a) agent x strength from Table 3
sa = {ag: (np.array([v[0] for v in TABLE3[ag]]), np.array([v[1] for v in TABLE3[ag]]) * T) for ag in TABLE3}
dots(axs[0], ["4.9", "14.7", "23.5"], sa); axs[0].set_xlabel("Nominal $f'_c$ (MPa)"); axs[0].set_ylabel(r"Mean bond stress $\tau$ (MPa)")
# (b) agent x diameter (pooled over strengths, exact pooling of the nine group summaries)
sb = {}
for ag, g in PLAIN.items():
    pm = [pooled([g[d][i] for i in range(3)]) for d in DB]
    sb[ag] = (np.array([p[0] for p in pm]), np.array([p[1] for p in pm]) * T)
dots(axs[1], ["6", "9", "12"], sb); axs[1].set_xlabel("Bar diameter $d_b$ (mm)"); axs[1].tick_params(labelleft=False)
axs[0].legend(loc="upper left", handlelength=1.4, borderaxespad=.2)
# (c) zero-load share
ax = axs[2]; w = .26
for j, ag in enumerate(ZERO_PCT):
    x = np.arange(3) + (j - 1) * w
    ax.bar(x, ZERO_PCT[ag], w, color="white", edgecolor=AGENT[ag], hatch=AGENT_HATCH[ag], lw=.9, zorder=3)
    for xi, v in zip(x, ZERO_PCT[ag]): ax.text(xi, v + 2, f"{v}", ha="center", va="bottom", fontsize=8)
ax.set_xticks(range(3)); ax.set_xticklabels(["4.9", "14.7", "23.5"]); ax.set_ylim(0, 112); ax.set_xlim(-.6, 2.6)
ax.set_xlabel("Nominal $f'_c$ (MPa)"); ax.set_ylabel("Specimens with zero load (%)"); ax.grid(axis="y", color="#dcdcd6", lw=.5, zorder=0)
for a, l in zip(axs, "abc"): panel_label(a, f"({l})")
fig.tight_layout(w_pad=1.0); save(fig, "../figs/fig4.png")
