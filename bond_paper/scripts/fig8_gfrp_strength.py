import numpy as np, matplotlib.pyplot as plt
from fig_style import *; from bond_data import *
apply_style()
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.05))
off = {6: -0.35, 9: 0.0, 12: 0.35}
ax = axs[0]
ax.axhspan(POOLED_PLATEAU[0] - POOLED_PLATEAU[1], POOLED_PLATEAU[0] + POOLED_PLATEAU[1], xmin=.33, xmax=.97, facecolor="#e6e8ec", edgecolor="none", zorder=0)
ax.hlines(POOLED_PLATEAU[0], 14.7 - 5.2, 23.5 + 3.2, color=INK_SEC, lw=.9, ls=":", zorder=1)
for d in DB:
    c = DIAM[d]; x = np.array(FC) + off[d]
    P = np.array([GFRP[d][i][0] for i in range(3)]); S = np.array([GFRP[d][i][1] for i in range(3)])
    ax.plot(x, P, color=c, lw=1.1, zorder=2); ax.errorbar(x, P, yerr=S, fmt="none", ecolor=c, elinewidth=.9, capsize=2.6, zorder=3)
    ax.plot(x, P, DIAM_MK[d], ms=5.8, color=c, zorder=4, label=f"{d} mm")
ax.set_xlim(2.8, 26.2); ax.set_ylim(9, 28); ax.set_xticks(FC)
ax.set_xlabel("Nominal concrete strength $f'_c$ (MPa)"); ax.set_ylabel("Peak pull-out load $P$ (kN)")
ax.text(25.9, 27.6, "Band: pooled mean ± 1 SD at\n$f'_c$ ≥ 14.7 MPa, 20.8 ± 2.7 kN", ha="right", va="top", fontsize=7.8, color=INK_SEC)
ax.legend(title="Bar diameter", loc="lower right", handlelength=1.4, borderaxespad=.3).get_title().set_fontsize(8.6)
ax.grid(axis="y", color="#dcdcd6", lw=.5, zorder=0); panel_label(ax, "(a)")
ax = axs[1]
for d in DB:
    c = DIAM[d]; x = np.array(FC) + off[d]
    N = np.array([gfrp_N(d, i)[0] for i in range(3)]); S = np.array([gfrp_N(d, i)[1] for i in range(3)])
    ax.plot(x, N, color=c, lw=1.1, zorder=2); ax.errorbar(x, N, yerr=S, fmt="none", ecolor=c, elinewidth=.9, capsize=2.6, zorder=3)
    ax.plot(x, N, DIAM_MK[d], ms=5.8, color=c, zorder=4, label=f"{d} mm")
    ax.hlines(ACI_N[d], 2.8, 24.6, color=c, lw=.9, ls=(0, (5, 3)), zorder=1)
    ax.text(24.9, ACI_N[d] + (0.045 if d == 12 else (-0.0 if d == 9 else -0.045)), f"{ACI_N[d]:.2f}", color=c, fontsize=8, va="center" if d == 9 else ("bottom" if d == 12 else "top"))
ax.set_xlim(2.8, 26.6); ax.set_ylim(.5, 2.4); ax.set_xticks(FC)
ax.set_xlabel("Nominal concrete strength $f'_c$ (MPa)"); ax.set_ylabel(r"Normalised bond $N = \tau/\sqrt{f'_c}$")
ax.text(2.95, .56, "Dashed lines: ACI 440.1R-06 prediction, Eq. (4)", fontsize=7.8, color=INK_SEC, va="bottom")
ax.grid(axis="y", color="#dcdcd6", lw=.5, zorder=0); panel_label(ax, "(b)")
fig.tight_layout(w_pad=1.6); save(fig, "../figs/fig8.png")
