import numpy as np, matplotlib.pyplot as plt
from fig_style import *; from bond_data import *
apply_style()
fig, axs = plt.subplots(1, 2, figsize=(7.4, 3.2), gridspec_kw={"width_ratios": [1.15, 1]})
ax = axs[0]
rows = ["Plain bar, cement mortar", "Plain bar, non-shrink grout", "Plain bar, epoxy", "GFRP bar, cast in"]
ypos = {r: 3 - k for k, r in enumerate(rows)}; yo = {4.9: .22, 14.7: 0, 23.5: -.22}
def Nstat(row, i):
    f = FC[i]
    if row.startswith("GFRP"):
        return pooled([gfrp_N(d, i) for d in DB])
    ag = {"Plain bar, cement mortar": "Cement mortar", "Plain bar, non-shrink grout": "Non-shrink grout", "Plain bar, epoxy": "Epoxy"}[row]
    m, s = TABLE3[ag][i]; return m / f ** .5, s / f ** .5
for r in rows:
    for i, f in enumerate(FC):
        m, s = Nstat(r, i); c = STRENGTH[f]; y = ypos[r] + yo[f]
        ax.errorbar(m, y, xerr=s, fmt="none", ecolor=c, elinewidth=.9, capsize=2.6, zorder=3)
        ax.plot(m, y, STRENGTH_MK[f], ms=5.8, color=c, mec=STEEL_EDGE if f == 4.9 else c, zorder=4, label=f"{f} MPa")
ax.set_yticks(list(ypos.values())); ax.set_yticklabels(list(ypos.keys())); ax.set_ylim(-.6, 3.6); ax.set_xlim(-.15, 2.3)
ax.axvline(0, color=INK, lw=.6, zorder=1)
for y in (0.5, 1.5, 2.5): ax.axhline(y, color="#dcdcd6", lw=.5, zorder=0)
ax.set_xlabel(r"Normalised bond $N = \tau/\sqrt{f'_c}$"); ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
h, l = ax.get_legend_handles_labels(); u = dict(zip(l, h))
ax.legend(u.values(), u.keys(), title="Nominal $f'_c$", loc="upper right", bbox_to_anchor=(1.0, .86), handlelength=1.3).get_title().set_fontsize(8.6)
ax.text(.0, 1.02, "(a)", transform=ax.transAxes, fontweight="bold", fontsize=10.5)
ax = axs[1]
ax.plot([0, 31], [0, 31], color=INK, lw=.9, ls=(0, (5, 3)), zorder=1)
ax.text(17.2, 18.6, "1:1", rotation=38, color=INK_SEC, fontsize=8.4)
for i, f in enumerate(FC):
    for d in DB:
        x = epoxy_mean_P(d, i); y = GFRP[d][i][0]
        ax.plot(x, y, STRENGTH_MK[f], ms=6, color=STRENGTH[f], mec=STEEL_EDGE if f == 4.9 else STRENGTH[f], zorder=4)
        offs = {(14.7, 12): (-10, 5), (14.7, 9): (5, -8), (23.5, 6): (-10, -10), (23.5, 9): (5, -8)}
        ax.annotate(str(d), (x, y), xytext=offs.get((f, d), (4, 3.5)), textcoords="offset points", fontsize=7.6, color=INK_SEC)
ax.set_xlim(0, 31); ax.set_ylim(0, 31); ax.set_aspect("equal", adjustable="box")
ax.set_xlabel("Epoxy-anchored plain bar: mean peak load (kN)"); ax.set_ylabel("GFRP bar, cast in: mean peak load (kN)")
hh = [plt.Line2D([], [], ls="", marker=STRENGTH_MK[f], color=STRENGTH[f], mec=STEEL_EDGE if f == 4.9 else STRENGTH[f], ms=6, label=f"{f} MPa") for f in FC]
ax.legend(handles=hh, title="Nominal $f'_c$\n(labels: $d_b$, mm)", loc="lower right", handlelength=1.0, borderaxespad=.3).get_title().set_fontsize(8.2)
ax.text(.0, 1.02, "(b)", transform=ax.transAxes, fontweight="bold", fontsize=10.5)
fig.tight_layout(w_pad=1.6); save(fig, "../figs/fig9.png")
