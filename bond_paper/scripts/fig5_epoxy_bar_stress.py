import numpy as np, matplotlib.pyplot as plt
from fig_style import *; from bond_data import *
apply_style()
fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.95))
off = {4.9: -0.14, 14.7: 0.0, 23.5: 0.14}
for k, panel in enumerate(("tau", "sig")):
    ax = axs[k]
    for i, f in enumerate(FC):
        x = np.arange(3) + off[f]
        m = np.array([EPOXY[d][i][0] for d in DB]); s = np.array([EPOXY[d][i][1] for d in DB])
        if panel == "sig":
            fac = np.array([4 * LE / d for d in DB]); m, s = m * fac, s * fac
        c = STRENGTH[f]
        ax.plot(x, m, color=c, lw=1.1, zorder=2); ax.errorbar(x, m, yerr=s, fmt="none", ecolor=c, elinewidth=.9, capsize=2.6, zorder=3)
        ax.plot(x, m, STRENGTH_MK[f], ms=5.8, color=c, mec=STEEL_EDGE if f == 4.9 else c, zorder=4, label=f"{f} MPa")
    ax.set_xticks(range(3)); ax.set_xticklabels(["6", "9", "12"]); ax.set_xlim(-.5, 2.5)
    ax.set_xlabel("Bar diameter $d_b$ (mm)"); ax.grid(axis="y", color="#dcdcd6", lw=.5, zorder=0)
    panel_label(ax, "(a)" if k == 0 else "(b)")
axs[0].set_ylabel(r"Bond stress $\tau$ (MPa)"); axs[0].set_ylim(-.3, 8)
axs[1].set_ylabel(r"Nominal bar stress at peak, $\sigma_b$ (MPa)"); axs[1].set_ylim(-20, 440)
axs[1].axhline(235, color=INK, lw=.9, ls=(0, (5, 3)), zorder=1)
axs[1].text(2.45, 420, "Dashed line: catalogue minimum yield\nof SR24 bar, 235 MPa (not measured)", fontsize=7.8, color=INK_SEC, va="top", ha="right", bbox=dict(boxstyle="square,pad=0.2", facecolor="white", edgecolor="none", alpha=0.9), zorder=6)
leg = axs[0].legend(title="Nominal $f'_c$", loc="upper left", handlelength=1.4, borderaxespad=.2)
leg.get_title().set_fontsize(8.6)
fig.tight_layout(w_pad=1.6); save(fig, "../figs/fig5.png")
