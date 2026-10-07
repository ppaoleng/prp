"""Fig. 6 - peak contact force at 120 km/h vs. peak approach-side stiffness (Tables 5 and 6)."""
import matplotlib.pyplot as plt
import fig_style as S
from data import MODELS, KD, FORCE

S.apply_style()
fig, ax = plt.subplots(figsize=(4.9, 3.5))
fig.subplots_adjust(left=0.115, right=0.975, top=0.97, bottom=0.14)

xs = {m: KD[m] for m in MODELS}
ys = {m: FORCE[m][3] for m in MODELS}

# guide segments for the three steps discussed in Sect. 3.4 (M1->M2->M3->M5)
path = ["M1", "M2", "M3", "M5"]
label_xy = {"M1": (9, 6), "M2": (9, 6), "M3": (-4, -19)}
for a, b in zip(path[:-1], path[1:]):
    ax.plot([xs[a], xs[b]], [ys[a], ys[b]], color="#9a9a95", lw=0.8, ls=(0, (2.5, 2.0)), zorder=2)
    slope = (ys[a] - ys[b]) / (xs[b] - xs[a])
    mid = ((xs[a] + xs[b]) / 2, (ys[a] + ys[b]) / 2)
    kw = dict(arrowprops=dict(arrowstyle="-", lw=0.5, color="#9a9a95", shrinkA=0, shrinkB=1)) if a == "M3" else {}
    ax.annotate(f"\u2212{slope:.2f} kN per kN/mm", xy=mid, xytext=label_xy[a], textcoords="offset points",
                fontsize=7.2, color=S.INK_SEC, ha="right" if a == "M3" else "left", va="bottom", zorder=5,
                bbox=S.halo(pad=0.1), **kw)

for m in MODELS:
    ax.plot(xs[m], ys[m], marker=S.MARKER[m], ms=8.5 if m != "M4" else 8.0, mfc=S.SERIES[m], mec=S.INK, mew=0.7,
            ls="none", zorder=4)

off = {"M1": (9, 4), "M2": (9, 4), "M3": (-10, 2), "M4": (0, 10), "M5": (11, -1)}
ha = {"M1": "left", "M2": "left", "M3": "right", "M4": "center", "M5": "left"}
for m in MODELS:
    ax.annotate(m, (xs[m], ys[m]), xytext=off[m], textcoords="offset points", ha=ha[m],
                va="center", fontsize=8.6, fontweight="bold", color=S.INK, zorder=6)

ax.set_xlim(38, 84)
ax.set_ylim(50, 71)
ax.set_xticks(range(40, 81, 10))
ax.set_yticks(range(52, 69, 4))
ax.grid(True, color=S.GRID, lw=0.5, zorder=0)
ax.set_axisbelow(True)
ax.set_xlabel("Peak approach-side stiffness (kN/mm)")
ax.set_ylabel("Peak contact force at 120 km/h (kN)")
S.save(fig, "Fig6_force_vs_stiffness")
