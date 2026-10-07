"""Fig. 2 - schematic longitudinal section of the modified track (not to scale).

Layer order, PU zone order (30 cm next to the bridge), extent of the auxiliary rail and of the
enlarged sleepers (zones 1-2, 'indicative') and all labels follow the original Fig. 2 of the manuscript.
Vertical thicknesses are drawn at a common exaggerated scale (1 in = 1 m) so that 10/20/30 cm PU
and 0.40 m ballast are mutually proportional.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import fig_style as S

S.apply_style()
W, H = 6.5, 2.72
fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")

# ---- geometry (inches) -------------------------------------------------------------------
X0, XA, XB, XE = 0.42, 1.52, 3.86, 5.70        # left end, approach|PU, PU|bridge, right end
ZW = (XB - XA) / 3                              # width of one PU zone
Y_SUB0, Y_SUB1 = 0.62, 0.92                     # sub-ballast
Y_BAL1 = Y_SUB1 + 0.40                          # ballast top (0.40 m)
Y_SLP1 = Y_BAL1 + 0.11                          # sleeper top
Y_RAIL1 = Y_SLP1 + 0.075                        # rail top
PU_T = {3: 0.10, 2: 0.20, 1: 0.30}              # zone number -> thickness (1 in = 1 m)
ZONE_X = {3: XA, 2: XA + ZW, 1: XA + 2 * ZW}    # left edge of each zone


def region(x, y, w, h, fc, hatch=None, hc=S.INK_SEC, ec=S.LINE, lw=0.7, z=1):
    if hatch:
        ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=hc, hatch=hatch, lw=0, zorder=z))
        ax.add_patch(Rectangle((x, y), w, h, fc="none", ec=ec, lw=lw, zorder=z + 0.05))
    else:
        ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, zorder=z))


def label(x, y, s, **kw):
    kw.setdefault("fontsize", 7.8); kw.setdefault("ha", "center"); kw.setdefault("va", "center")
    kw.setdefault("zorder", 8)
    return ax.text(x, y, s, **kw)


def dim(x0, y0, x1, y1, lw=0.7, both=True):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=7,
                arrowprops=dict(arrowstyle="<|-|>" if both else "-|>", lw=lw, color=S.INK, shrinkA=0, shrinkB=0,
                                mutation_scale=6))


# ---- ground layers ----------------------------------------------------------------------
region(X0, Y_SUB0, XB - X0, Y_SUB1 - Y_SUB0, S.SOIL_SAND, "....", hc="#8a8472")                  # sub-ballast
region(X0, Y_SUB1, XB - X0, Y_BAL1 - Y_SUB1, S.GROUND, "oo", hc="#8f8c82")                        # ballast
for k in (3, 2, 1):                                                                              # PU zones
    region(ZONE_X[k], Y_SUB1, ZW, PU_T[k], "#ead9bf", "\\\\\\\\\\", hc=S.WARM, lw=0.7, z=2)
ax.plot([ZONE_X[3], XB], [Y_SUB1, Y_SUB1], color=S.LINE, lw=0.7, zorder=3)
for k in (3, 2):                                                                                 # zone boundaries
    ax.plot([ZONE_X[k] + ZW] * 2, [Y_SUB1, Y_BAL1], color=S.LINE, lw=0.5, zorder=3, ls=(0, (3, 2)))
ax.plot([XA, XA], [Y_SUB1, Y_BAL1], color=S.LINE, lw=0.5, zorder=3, ls=(0, (3, 2)))
region(XB, Y_SUB0, XE - XB, Y_SLP1 - 0.11 - Y_SUB0, "#e3e5e8", "xx", hc="#9aa0aa")                # bridge deck

# ---- sleepers and rail ------------------------------------------------------------------
pitch, sw = 0.105, 0.062
for xc in np.arange(X0 + 0.07, XE - 0.03, pitch):
    ax.add_patch(Rectangle((xc - sw / 2, Y_BAL1), sw, Y_SLP1 - Y_BAL1, fc="#cfcfca", ec=S.LINE, lw=0.5, zorder=4))
ax.add_patch(Rectangle((X0, Y_SLP1), XE - X0, Y_RAIL1 - Y_SLP1, fc="#3c4148", ec=S.INK, lw=0.5, zorder=5))

# auxiliary rail and enlarged sleepers: zones 2 and 1 (indicative extent)
XM0, XM1 = ZONE_X[2], XB
ax.add_patch(Rectangle((XM0, Y_RAIL1 + 0.035), XM1 - XM0, 0.075, fc=S.STEEL, ec=S.STEEL_EDGE, hatch="////", lw=0.6, zorder=5))
ax.add_patch(Rectangle((XM0 - 0.01, Y_BAL1 - 0.015), XM1 - XM0 + 0.02, Y_SLP1 - Y_BAL1 + 0.03, fc="none",
                       ec=S.INK, lw=0.9, ls=(0, (3.5, 2.2)), zorder=6))

# ---- annotations: material labels -------------------------------------------------------
label(X0 + 0.55, Y_BAL1 - 0.20, "Ballast\n(E = 100 MPa)", bbox=S.halo(), linespacing=1.15)
label(X0 + 0.90, Y_SUB0 + 0.15, "Sub-ballast (E = 40 MPa)", bbox=S.halo(), fontsize=7.3)
label((XB + XE) / 2, (Y_SUB0 + Y_SLP1 - 0.11) / 2, "Concrete bridge deck\n(simple support)", bbox=S.halo(), linespacing=1.15)

# PU thickness dimensions inside each zone
for k in (3, 2, 1):
    xc = ZONE_X[k] + ZW / 2
    t = PU_T[k]
    dim(xc, Y_SUB1 + 0.005, xc, Y_SUB1 + t - 0.005, lw=0.6)
    label(xc + 0.04, Y_SUB1 + t / 2, f"{int(round(t * 100))} cm", ha="left", fontsize=7.2, bbox=S.halo(pad=0.1), zorder=9)
    label(xc, Y_SUB0 - 0.23, f"PU zone {k}", fontsize=7.8)
    dim(ZONE_X[k] + 0.01, Y_SUB0 - 0.085, ZONE_X[k] + ZW - 0.01, Y_SUB0 - 0.085, lw=0.6)
    for xx in (ZONE_X[k], ZONE_X[k] + ZW):
        ax.plot([xx, xx], [Y_SUB0 - 0.04, Y_SUB0 - 0.13], color=S.INK, lw=0.5, zorder=7)
    label(xc, Y_SUB0 - 0.38, "5 m", fontsize=7.2, color=S.INK_SEC)
ax.plot([XE, XE], [Y_SUB0 - 0.04, Y_SUB0 - 0.13], color=S.INK, lw=0.0)

# 0.40 m ballast depth (left)
dim(X0 - 0.14, Y_SUB1, X0 - 0.14, Y_BAL1, lw=0.6)
label(X0 - 0.215, (Y_SUB1 + Y_BAL1) / 2, "0.40 m", rotation=90, fontsize=7.2)
# 0.60 m sleeper spacing (callout over two adjacent sleepers near the left end)
xs0 = X0 + 0.07 + 2 * pitch
ax.plot([xs0] * 2, [Y_RAIL1 + 0.01, Y_RAIL1 + 0.15], color=S.INK, lw=0.5, zorder=7)
ax.plot([xs0 + pitch] * 2, [Y_RAIL1 + 0.01, Y_RAIL1 + 0.15], color=S.INK, lw=0.5, zorder=7)
ax.annotate("", xy=(xs0 + pitch, Y_RAIL1 + 0.12), xytext=(xs0, Y_RAIL1 + 0.12), zorder=7,
            arrowprops=dict(arrowstyle="|-|", lw=0.6, color=S.INK, shrinkA=0, shrinkB=0, mutation_scale=2.5))
label(xs0 + pitch / 2 + 0.12, Y_RAIL1 + 0.24, "sleeper spacing 0.60 m", ha="left", fontsize=7.2)

# rail / sleeper labels on the right
label(XE + 0.10, Y_RAIL1 + 0.20, "Rail", ha="left", fontsize=7.8)
ax.plot([XE + 0.09, XE - 0.15], [Y_RAIL1 + 0.19, Y_RAIL1 - 0.02], color=S.INK_SEC, lw=0.5, zorder=7)
label(XE + 0.10, Y_BAL1 - 0.18, "Sleeper", ha="left", fontsize=7.8)
ax.plot([XE + 0.09, XE - 0.05], [Y_BAL1 - 0.18, Y_BAL1 + 0.04], color=S.INK_SEC, lw=0.5, zorder=7)

# ---- top span labels ----------------------------------------------------------------------
Y_SPAN = H - 0.16
for (x0, x1, txt) in [(X0, XA - 0.04, "Ballasted approach"), (XA + 0.04, XB - 0.04, "Stepped PU transition: 3 × 5 m"),
                      (XB + 0.04, XE, "Bridge")]:
    dim(x0, Y_SPAN - 0.10, x1, Y_SPAN - 0.10, lw=0.7)
    label((x0 + x1) / 2, Y_SPAN + 0.03, txt, fontsize=8.0)

# running direction
dim(X0 + 0.05, Y_RAIL1 + 0.62, X0 + 0.80, Y_RAIL1 + 0.62, lw=0.9, both=False)
label(X0 + 0.05, Y_RAIL1 + 0.75, "Running direction", ha="left", fontsize=7.4, color=S.INK_SEC)

# auxiliary rail / enlarged sleepers callouts (extent indicative)
label(XM0 + 0.38, Y_RAIL1 + 0.55, "Auxiliary rail (M3, M5)", ha="right", fontsize=7.8)
ax.plot([XM0 + 0.45, XM0 + 0.45], [Y_RAIL1 + 0.49, Y_RAIL1 + 0.12], color=S.INK_SEC, lw=0.5, zorder=7)
ax.plot([XM0 + 0.38, XM0 + 0.45], [Y_RAIL1 + 0.55, Y_RAIL1 + 0.49], color=S.INK_SEC, lw=0.5, zorder=7)
label(XB + 0.20, Y_RAIL1 + 0.42, "Enlarged sleepers (M4, M5)", ha="left", fontsize=7.8)
label(XB + 0.20, Y_RAIL1 + 0.58, "(extent of both measures indicative)", ha="left", fontsize=7.0, color=S.INK_SEC)
ax.plot([XB + 0.17, XB - 0.04], [Y_RAIL1 + 0.40, Y_SLP1 + 0.02], color=S.INK_SEC, lw=0.5, zorder=7)
S.save(fig, "Fig2_schematic")
