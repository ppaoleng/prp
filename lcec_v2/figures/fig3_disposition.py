"""Fig. 3 - disposition of the 76 retained report records (R2 decisions -> corrected disposition).
All counts are taken from Section 2.2: 37/38/1 recorded; 35/39/1/1 corrected; two INCLUDE corrections."""
from matplotlib.patches import PathPatch, Polygon
from matplotlib.path import Path
from fig_style import *
from matplotlib.patches import Rectangle

B, N, I = "bold", "normal", "normal"
c = Canvas(W_TEXT)
ax = c.ax
top = c.H - 0.05

u = 2.75 / 76.0               # inches per report
LBX, LBW = 1.62, 0.17          # left bars
RBX, RBW = 4.30, 0.17          # right bars
GL, GR = 0.34, 0.22            # gaps between groups (left / right) -> same total height

# column headings
c.para(0.0, top, LBX + LBW, [("Recorded R2 decisions", B, I, INK)], size=8.4, align="right")
c.para(RBX, top, W_TEXT - RBX, [("Corrected disposition", B, I, INK)], size=8.4, align="left")
c.para(0.0, top - 0.17, LBX + LBW, [("n = 76", N, I, INK_SEC)], size=7.6, align="right")
c.para(RBX, top - 0.17, W_TEXT - RBX, [("n = 76", N, I, INK_SEC)], size=7.6, align="left")
y0 = top - 0.50

left = [("INCLUDE", 37), ("BACKGROUND", 38), ("EXCLUDE", 1)]
right = [("core", 35, "Core educational reports"),
         ("noft", 1, "No matched full text in retained records"),
         ("ctx", 39, "Contextual or foundational reports"),
         ("out", 1, "Outside the educational focus")]

# bar positions (top -> bottom)
lpos, y = {}, y0
for name, n in left:
    lpos[name] = (y, n); y -= n * u + GL
rpos, y = {}, y0
for key, n, _ in right:
    rpos[key] = (y, n); y -= n * u + GR

colors = {"core": (ACCENT, ACCENT_EDGE), "noft": (WARM, WARM_EDGE), "ctx": (STEEL, STEEL_EDGE), "out": ("#c9cacb", STEEL_EDGE)}
lcol = ("#cfd3d9", STEEL_EDGE)

def ribbon(x0, ya, x1, yb, h, fc, ec, alpha=0.45, lw=0.5, hatch=None, z=1):
    """ribbon from left (top at ya, height h) to right (top at yb)."""
    xm = (x0 + x1) / 2
    verts = [(x0, ya), (xm, ya), (xm, yb), (x1, yb), (x1, yb - h), (xm, yb - h), (xm, ya - h), (x0, ya - h), (x0, ya)]
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.LINETO, Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.CLOSEPOLY]
    ax.add_patch(PathPatch(Path(verts, codes), facecolor=fc, edgecolor=ec, lw=lw, alpha=alpha, zorder=z, hatch=hatch))
    c.ymin = min(c.ymin, yb - h, ya - h)

xl, xr = LBX + LBW, RBX
# flows: (from, to, n, kind)
flows = [("INCLUDE", "core", 35, "main"), ("INCLUDE", "noft", 1, "corr"), ("INCLUDE", "ctx", 1, "corr"),
         ("BACKGROUND", "ctx", 38, "main"), ("EXCLUDE", "out", 1, "main")]
lcur = {k: v[0] for k, v in lpos.items()}
rcur = {k: v[0] for k, v in rpos.items()}
centers = {}
for a, b, n, kind in flows:
    ya, yb, h = lcur[a], rcur[b], n * u
    fc, ec = colors[b]
    if kind == "corr":
        ribbon(xl, ya, xr, yb, h, WARM, WARM_EDGE, alpha=0.9, lw=0.7, z=2)
    else:
        ribbon(xl, ya, xr, yb, h, fc, ec, alpha=0.35, lw=0.5)
    centers[(a, b)] = ((ya + (ya - h) ) / 2, (yb + (yb - h)) / 2)
    lcur[a] -= h; rcur[b] -= h

# bars + labels
subs = {"core": "37 INCLUDE minus 2 corrections",
        "noft": "Correction: RPT-000065, PDF mismatch",
        "ctx": "38 BACKGROUND plus correction RPT-000069 (published 2010)",
        "out": None}
for name, n in left:
    ytop, _ = lpos[name]
    c.rect(LBX, ytop, LBW, n * u, fc=lcol[0], ec=lcol[1], lw=0.8, z=3)
    cy = ytop - n * u / 2
    c.para(0.0, cy + 0.075, LBX - 0.08, [(f"{n}  ", B, I, INK), (name, N, I, INK)], size=8.4, align="right")
RW = W_TEXT - RBX - RBW - 0.10
for key, n, label in right:
    ytop, _ = rpos[key]
    fc, ec = colors[key]
    c.rect(RBX, ytop, RBW, n * u, fc=fc, ec=ec, lw=0.8, z=3, hatch=("////" if key == "noft" else None))
    cy = ytop - n * u / 2
    main = [(f"{n}  ", B, I, INK), (label, N, I, INK)]
    hm = c.para(RBX + RBW + 0.08, 0, RW, main, size=8.4, draw=False)
    sub = subs[key]
    hs = c.para(RBX + RBW + 0.08, 0, RW, [(sub, N, "italic", WARM_EDGE if key in ("noft", "ctx") else INK_SEC)], size=7.2, draw=False) if sub else 0
    tot = hm + (hs + 0.03 if sub else 0)
    c.para(RBX + RBW + 0.08, cy + tot / 2, RW, main, size=8.4)
    if sub:
        c.para(RBX + RBW + 0.08, cy + tot / 2 - hm - 0.03, RW, [(sub, N, "italic", WARM_EDGE if key in ("noft", "ctx") else INK_SEC)], size=7.2)

# legend (bottom-left)
ly = c.ymin - 0.16
c.rect(0.0, ly, 0.30, 0.07, fc=WARM, ec=WARM_EDGE, lw=0.6, z=3)
c.para(0.38, ly + 0.035 + 0.055, 3.6, [("Correction to a recorded INCLUDE decision", N, I, INK_SEC)], size=7.4)

c.finish("fig3_disposition.png", top=top + 0.02)
