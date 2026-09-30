import numpy as np, matplotlib.pyplot as plt
from fig_style import *; from bond_data import *
apply_style()
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.05))
off = {4.9: -0.03, 14.7: 0.0, 23.5: 0.03}
dd = np.array(DB, float)
ax = axs[0]
for i, f in enumerate(FC):
    c = STRENGTH[f]; xs = dd * np.exp(off[f])
    P = np.array([GFRP[d][i][0] for d in DB]); S = np.array([GFRP[d][i][1] for d in DB])
    lo = np.array([GFRP[d][i][2] for d in DB]); hi = np.array([GFRP[d][i][3] for d in DB])
    ax.vlines(xs, lo, hi, color=c, lw=3.2, alpha=.28, zorder=2)                     # min-max range
    ax.errorbar(xs, P, yerr=S, fmt="none", ecolor=c, elinewidth=.9, capsize=2.6, zorder=3)
    b = GFRP_B[f]; xx = np.linspace(5.3, 13, 20)                                      # slope = reported b, through group means
    ln_ref = np.log(np.exp(np.mean(np.log(P))))
    ax.plot(xx, np.exp(ln_ref + b * (np.log(xx) - np.mean(np.log(dd)))), color=c, lw=.9, ls=(0, (4, 2.5)), zorder=1)
    ax.plot(xs, P, STRENGTH_MK[f], ms=5.8, color=c, mec=STEEL_EDGE if f == 4.9 else c, zorder=4, label=f"{f} MPa  ($b$ = {b:.2f})")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(5.3, 13); ax.set_ylim(9.5, 28)
ax.set_xticks(DB); ax.set_xticklabels(DB); ax.set_yticks([10, 15, 20, 25]); ax.set_yticklabels([10, 15, 20, 25]); ax.minorticks_off()
ax.set_xlabel("Bar diameter $d_b$ (mm)"); ax.set_ylabel("Peak pull-out load $P$ (kN)")
ax.grid(color="#dcdcd6", lw=.5, zorder=0)
leg = ax.legend(title="Nominal $f'_c$", loc="lower right", handlelength=1.3, borderaxespad=.3); leg.get_title().set_fontsize(8.6)
panel_label(ax, "(a)")
ax = axs[1]
for i, f in enumerate(FC):
    c = STRENGTH[f]; xs = dd * np.exp(off[f])
    t = np.array([tau_from_P(GFRP[d][i][0], d) for d in DB]); s = np.array([tau_from_P(GFRP[d][i][1], d) for d in DB])
    ax.plot(xs, t, color=c, lw=1.1, zorder=2); ax.errorbar(xs, t, yerr=s, fmt="none", ecolor=c, elinewidth=.9, capsize=2.6, zorder=3)
    ax.plot(xs, t, STRENGTH_MK[f], ms=5.8, color=c, mec=STEEL_EDGE if f == 4.9 else c, zorder=4, label=f"{f} MPa")
xx = np.linspace(5.4, 12.6, 50)
ax.plot(xx, tau_from_P(POOLED_PLATEAU[0], xx), color=INK, lw=1.0, ls=":", zorder=1, label=r"Constant $P$ = 20.8 kN")
ax.set_xticks(DB); ax.set_xlim(5.3, 12.9); ax.set_ylim(0, 9.2)
ax.set_xlabel("Bar diameter $d_b$ (mm)"); ax.set_ylabel(r"Apparent bond stress $\tau$ (MPa)"); ax.grid(axis="y", color="#dcdcd6", lw=.5, zorder=0)
ax.legend(loc="upper right", handlelength=1.6, borderaxespad=.3)
panel_label(ax, "(b)")
fig.tight_layout(w_pad=1.6); save(fig, "../figs/fig7.png")
