"""Fig. 1 - research workflow (seven steps, calibration loop, three phases)."""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
import fig_style as S

S.apply_style()
W, H = 6.5, 4.62
fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")

ARROW = dict(arrowstyle="-|>", lw=0.8, color=S.INK, shrinkA=0, shrinkB=0, mutation_scale=7)
TITLE_FS, BODY_FS, TAG_FS = 8.2, 7.5, 7.0


def band(x0, y0, x1, y1, fc, ec, label, tc):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=fc, ec=ec, lw=0.6, zorder=0))
    ax.text(x0 + 0.10, y1 - 0.14, label, fontsize=7.4, fontweight="bold", color=tc, ha="left", va="center")


def box(x0, y1, w, h, title, body, tag=None):
    """Rectangle with top edge at y1; title (bold), body (regular), optional output tag (italic)."""
    y0 = y1 - h
    ax.add_patch(Rectangle((x0, y0), w, h, fc="white", ec=S.INK, lw=0.8, zorder=2))
    cx = x0 + w / 2
    ax.text(cx, y1 - 0.15, title, fontsize=TITLE_FS, fontweight="bold", ha="center", va="center", zorder=3)
    n = body.count("\n") + 1
    ax.text(cx, y1 - 0.30, body, fontsize=BODY_FS, ha="center", va="top", linespacing=1.28, zorder=3)
    if tag:
        ax.text(x0 + w - 0.07, y0 + 0.07, tag, fontsize=TAG_FS, style="italic", color=S.INK_SEC,
                ha="right", va="bottom", zorder=3)
    return (x0, y0, w, h)


def down(a, b):
    """Arrow from bottom centre of box a to top centre of box b."""
    ax.annotate("", xy=(b[0] + b[2] / 2, b[1] + b[3]), xytext=(a[0] + a[2] / 2, a[1]), arrowprops=ARROW, zorder=4)


# ---- layout (top-down) ------------------------------------------------------------------
YT = H - 0.05
LX, LW = 0.55, 2.42          # left column boxes
RX, RW = 3.55, 2.72          # right column boxes
HDR = 0.33                   # band header height

# left column geometry
l1_top = YT - HDR
b1 = box(LX, l1_top, LW, 0.66, "1. Select measures", "PU-injected ballast, auxiliary rail,\nenlarged sleepers")
b2 = box(LX, b1[1] - 0.24, LW, 0.98, "2. Baseline FE model",
         "3D ABAQUS model of the unmodified\ntrack\u2013bridge system (M1)")
ax.text(LX + LW / 2, b2[1] + 0.07, "Inputs: Table 1; UIC54 rail, meter gauge;\nsleeper spacing 0.60 m; ballast depth 0.40 m",
        fontsize=TAG_FS, style="italic", color=S.INK_SEC, ha="center", va="bottom", linespacing=1.25, zorder=3)
b3 = box(LX, b2[1] - 0.24, LW, 0.85, "3. Verification and calibration",
         "force equilibrium; interface compatibility;\nstiffness calibration to 44 and 264 kN/mm\n(ballasted track and bridge)")
down(b1, b2); down(b2, b3)

dhw, dhh = 1.16, 0.45
dcx, dcy = LX + LW / 2, b3[1] - 0.26 - dhh
ax.add_patch(Polygon([(dcx - dhw, dcy), (dcx, dcy + dhh), (dcx + dhw, dcy), (dcx, dcy - dhh)], closed=True,
                     fc="white", ec=S.INK, lw=0.8, zorder=2))
ax.text(dcx, dcy, "Calibrated\nstiffness matched?", fontsize=BODY_FS + 0.1, ha="center", va="center", linespacing=1.2, zorder=3)
ax.annotate("", xy=(dcx, dcy + dhh), xytext=(b3[0] + b3[2] / 2, b3[1]), arrowprops=ARROW, zorder=4)
left_bottom = dcy - dhh - 0.10

# right column geometry
b4 = box(RX, YT - HDR, RW, 0.66, "4. Modified models M2\u2013M5",
         "stepped PU 30/20/10 cm, 5 m each, with or\nwithout auxiliary rail and enlarged sleepers")
b5 = box(RX, b4[1] - 0.20, RW, 0.82, "5. Static stiffness profile",
         r"$k_d = \Sigma Q_i \, / \, \Sigma w_j$ over five sleepers under" "\n" r"a 20-t axle load (Eq. 1); ratio $\rho$ (Eq. 2)",
         tag=r"Output: peak $k_d$ and $\rho$ (Fig. 3, Table 5)")
down(b4, b5)
r1_bottom = b5[1] - 0.12
r2_top = r1_bottom - 0.12
b6 = box(RX, r2_top - HDR, RW, 0.84, "6. Vehicle\u2013track dynamics",
         "Universal Mechanism (UM), one car, 60\u2013120 km/h;\nstiffness profile from Step 5 used as\ntrack input")
b7 = box(RX, b6[1] - 0.20, RW, 0.82, "7. Comparison",
         "peak wheel\u2013rail contact force and\nreduction relative to M1 (Eq. 3)",
         tag="Output: Figs. 4\u20136, Tables 6 and 7")
down(b6, b7)
ax.annotate("", xy=(RX + RW / 2, b6[1] + b6[3]), xytext=(RX + RW / 2, b5[1]), arrowprops=ARROW, zorder=4)
r2_bottom = b7[1] - 0.12

# ---- bands (drawn after boxes so their extent follows the content) --------------------------
band(0.03, left_bottom, 3.14, YT, "#eef1f5", S.ACCENT, "Model development and verification", S.ACCENT_EDGE)
band(3.38, r1_bottom, W - 0.03, YT, "#f4efe6", S.WARM, "Stiffness evaluation (ABAQUS)", S.WARM_EDGE)
band(3.38, r2_bottom, W - 0.03, r2_top, "#edf1ee", S.OK_GREEN, "Dynamic analysis (UM)", "#2f5a3d")

# ---- loops ------------------------------------------------------------------------------
lx_loop = 0.30
yb2 = b2[1] + b2[3] / 2
ax.plot([dcx - dhw, lx_loop, lx_loop], [dcy, dcy, yb2], color=S.INK, lw=0.8, zorder=1, solid_capstyle="butt")
ax.annotate("", xy=(LX, yb2), xytext=(lx_loop, yb2), arrowprops=ARROW, zorder=4)
ax.text(0.17, (dcy + yb2) / 2, "No: adjust material properties", fontsize=7.2, rotation=90,
        ha="center", va="center", color=S.INK)
xm = 3.26
yb4 = b4[1] + b4[3] / 2
ax.plot([dcx + dhw, xm, xm], [dcy, dcy, yb4], color=S.INK, lw=0.8, zorder=1, solid_capstyle="butt")
ax.annotate("", xy=(RX, yb4), xytext=(xm, yb4), arrowprops=ARROW, zorder=4)
ax.text(dcx + dhw + 0.03, dcy + 0.04, "Yes", fontsize=7.4, ha="left", va="bottom")
S.save(fig, "Fig1_workflow")
