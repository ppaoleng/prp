import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from fig_style import *
apply_style()
W, H = 100, 66
fig = plt.figure(figsize=(7.4, 5.0)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
FS = 6.5
xl = [6.4, 27.2, 48.0, 67.3, 87.1]; xw = [19.0, 19.0, 17.5, 18.0, 12.4]
for x, w, n in zip(xl, xw, ["1  Design", "2  Fabrication", "3  Test", "4  Analysis", "5  Findings"]):
    ax.add_patch(Rectangle((x, 61.0), w, 4.2, fc=STEEL_EDGE, ec="none"))
    ax.text(x + 1.0, 63.1, n, color="white", fontsize=8.2, fontweight="bold", va="center")
DASH = (0, (4, 2.4))
def box(x, y, w, h, title, body, c, dashed=False, fc="white", tfs=FS + .4):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=c, lw=.9, ls=(DASH if dashed else "-"), zorder=2))
    if dashed:
        ax.add_patch(Rectangle((x, y + h - 3.6), w, 3.6, fc="#e9e8e3", ec=c, lw=.9, ls=DASH, zorder=3))
    else:
        ax.add_patch(Rectangle((x, y + h - 3.6), w, 3.6, fc=c, ec="none", zorder=3))
    ax.text(x + .8, y + h - 1.8, title, fontsize=tfs, fontweight="bold", va="center", color=(INK if dashed else "white"), zorder=4)
    ax.text(x + .9, y + h - 4.8, body, fontsize=FS, va="top", linespacing=1.5, zorder=4)
def arrow(x0, x1, y, c=INK_SEC):
    ax.annotate("", xy=(x1, y), xytext=(x0, y), arrowprops=dict(arrowstyle="-|>", color=c, lw=.9, shrinkA=0, shrinkB=0, mutation_scale=7), zorder=5)
# common strip
ax.add_patch(Rectangle((xl[0], 55.6), xl[4] + xw[4] - xl[0], 3.9, fc="#f2f1ec", ec=INK_SEC, lw=.9, zorder=2))
ax.text(xl[0] + 1.0, 57.55, "Common to all series:  150 mm cubes,  $l_e$ = 140 mm,  nominal $f'_c$ = 4.9 / 14.7 / 23.5 MPa,  5 specimens per group,  180 specimens (135 plain-bar, 45 GFRP)", fontsize=FS + .2, va="center", zorder=4)
L1, L2, L3 = (36.8, 17.8), (18.6, 16.7), (1.2, 16.0)
for (y0, h), lab, c in ((L1, "Plain steel bars", ACCENT), (L2, "GFRP bars", WARM)):
    ax.add_patch(Rectangle((.6, y0), 4.0, h, fc=c, ec="none", zorder=2))
    ax.text(2.6, y0 + h / 2, lab, rotation=90, ha="center", va="center", fontsize=7.4, color="white", fontweight="bold", zorder=4)
ax.add_patch(Rectangle((.6, L3[0]), 4.0, L3[1], fc="white", ec=INK_SEC, lw=.9, ls=DASH, zorder=2))
ax.text(2.6, L3[0] + L3[1] / 2, "Added in revision", rotation=90, ha="center", va="center", fontsize=7.4, color=INK, fontweight="bold", zorder=4)
y, h = L1
box(xl[0], y, xw[0], h, "RB6 / RB9 / RB12", "3 $d_b$ × 3 agents × 3 $f'_c$ × 5\n= 135 specimens\n\nBonding agents:\n  epoxy (two-part)\n  non-shrink grout\n  cement mortar", ACCENT)
box(xl[1], y, xw[1], h, "Post-installed bars", "1. Cast cube on wooden dowel\n2. Demould at 24 h, water cure\n3. Drill hole along dowel line\n4. Coat bar with agent, insert\n5. Set for 2–3 d, then test", ACCENT)
box(xl[2], y, xw[2], h, "Direct pull-out", "Universal testing machine\nLVDT at the free end\n\nRecorded: peak load $P$,\nfailure mode (one specimen\nper group)", LINE)
box(xl[3], y, xw[3], h, "Plain-bar analysis", r"$\tau = P/(\pi d_b l_e)$" + "\n" + r"$N = \tau/\sqrt{f'_c}$;  $\sigma_b = 4P/\pi d_b^2$" + "\nThree-factor ANOVA\n(agent, $d_b$, $f'_c$)\nPermutation, HC3, transforms\nand subset checks", LINE)
box(xl[4], y, xw[4], h, "Plain bars", "Agent governs;\nepoxy gap opens\nfrom 14.7 MPa", ACCENT, tfs=FS + .2)
y, h = L2
box(xl[0], y, xw[0], h, "GF6 / GF9 / GF12", "3 $d_b$ × 3 $f'_c$ × 5\n= 45 specimens\n\nNo bonding agent", WARM)
box(xl[1], y, xw[1], h, "Cast-in bars", "1. Fix bar through timber top\n    plate\n2. Cast concrete in 3 layers\n3. Demould at 24 h, water cure", WARM)
box(xl[2], y, xw[2], h, "Direct pull-out", "Same arrangement and data\nreduction as plain bars;\nsplitting recorded for\nevery specimen", LINE)
box(xl[3], y, xw[3], h, "GFRP analysis", "Two-factor ANOVA\n($d_b$ × $f'_c$)\n" + r"$P \propto d_b^{\,b}$ (log–log fit)" + "\nMeasured / predicted,\nACI 440.1R-06 form", LINE)
box(xl[4], y, xw[4], h, "GFRP bars", "Load plateau above\n14.7 MPa; apparent\n$\\tau$ falls with $d_b$", WARM, tfs=FS + .2)
y, h = L3
box(xl[0], y, xw[0], h, "Material checks", "Companion cubes:\nmeasured $f'_c$ at test age\nTensile coupons: $f_y$, $f_u$\nGFRP: $f_{fu}$, $E_f$, surface", INK_SEC, dashed=True)
box(xl[1], y, xw[1], h, "Traceability", "Specimen ID, batch, date\nRaw UTM / LVDT files\nData-provenance log for\nall 180 specimens", INK_SEC, dashed=True)
box(xl[2], y, xw[2], h, "Supplementary tests", "Short embedment\n$l_e$ = 5 $d_b$ (ACI 440.3R,\nAnnex B.3)\nLoad–slip curves retained", INK_SEC, dashed=True)
box(xl[3], y, xw[3], h, "Re-analysis", "Bar stress vs measured $f_y$\nNormalisation by measured\n$f'_c$\nLoad–slip parameters", INK_SEC, dashed=True)
box(xl[4], y, xw[4], h, "Cross-system", "Matched $d_b$, $f'_c$:\ndescriptive only\n(installation differs)", LINE, fc="#f2f1ec", tfs=FS + .2)
for (y0, h0), c in ((L1, INK_SEC), (L2, INK_SEC), (L3, INK_SEC)):
    for i in range(4): arrow(xl[i] + xw[i] + .1, xl[i + 1] - .1, y0 + h0 / 2 - 2, c)
save(fig, "../figs/fig1.png")
