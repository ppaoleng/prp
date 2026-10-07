"""Fig. 4 - peak wheel-rail contact force vs. train speed (Table 6), with enlarged view of M3-M5."""
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import fig_style as S
from data import MODELS, SPEEDS, FORCE

S.apply_style()
fig, ax = plt.subplots(figsize=(4.9, 3.5))
fig.subplots_adjust(left=0.115, right=0.985, top=0.885, bottom=0.135)

def draw(a, models, ms, lw, filled_m1=True):
    for m in models:
        face = S.SERIES[m] if m == "M1" else "white"
        a.plot(SPEEDS, FORCE[m], color=S.SERIES[m], lw=lw, ls=S.LSTYLE[m], marker=S.MARKER[m],
               ms=ms, mfc=face, mec=S.SERIES[m], mew=1.0, zorder=3 + (m == "M1"))

draw(ax, MODELS, 4.6, 1.15)
ax.set_xlim(56, 124)
ax.set_ylim(48, 73)
ax.set_xticks(SPEEDS)
ax.set_yticks(range(50, 71, 5))
ax.yaxis.grid(True, color=S.GRID, lw=0.5, zorder=0)
ax.set_axisbelow(True)
ax.set_xlabel("Train speed (km/h)")
ax.set_ylabel("Peak wheel–rail contact force (kN)")

# legend above the axes, one row
handles = [Line2D([0], [0], color=S.SERIES[m], lw=1.15, ls=S.LSTYLE[m], marker=S.MARKER[m], ms=4.2,
                  mfc=(S.SERIES[m] if m == "M1" else "white"), mec=S.SERIES[m], mew=1.0) for m in MODELS]
leg = fig.legend(handles, [S.LABEL[m] for m in MODELS], loc="upper center", bbox_to_anchor=(0.55, 1.0),
                 ncol=3, frameon=False, handlelength=2.6, columnspacing=1.0, labelspacing=0.35, fontsize=7.6)

# inset: enlarged view of M3-M5
ins = ax.inset_axes([0.075, 0.585, 0.40, 0.375])
draw(ins, ["M3", "M4", "M5"], 3.6, 1.0)
ins.set_xlim(57, 123)
ins.set_ylim(49.0, 54.2)
ins.set_xticks(SPEEDS)
ins.set_yticks([50, 52, 54])
ins.tick_params(labelsize=6.6, length=2.2, width=0.6, pad=1.5)
ins.yaxis.grid(True, color=S.GRID, lw=0.4)
ins.set_axisbelow(True)
for sp in ("left", "bottom"):
    ins.spines[sp].set_linewidth(0.6)
ins.patch.set_facecolor("white")
ins.set_title("Enlarged view of M3–M5", fontsize=7.0, color=S.INK_SEC, pad=2.0, loc="left")
S.save(fig, "Fig4_force_speed")
