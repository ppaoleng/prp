"""Tiny diagram toolkit (square boxes, thin lines, muted fills, Thai+English labels)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from fig_style import *
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Polygon, Circle, Ellipse
from matplotlib import font_manager as fm
apply_style()
_have = {f.name for f in fm.fontManager.ttflist}
TH = "Loma" if "Loma" in _have else THAI[0]
THL = "Laksaman" if "Laksaman" in _have else TH
EN = SANS[0]
FILL = {"paper": "#f4f2ec", "blue": "#dfe6ec", "warm": "#eee3d3", "green": "#e0e8e1", "gray": "#e8e8e4", "white": "white",
        "dblue": "#274a63", "dwarm": "#6e5636", "ink": "#2b2b28"}

def canvas(w, h, xmax=100.0, ymax=None):
    fig = plt.figure(figsize=(w, h)); ax = fig.add_axes([0, 0, 1, 1])
    ymax = ymax or xmax * h / w
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax); ax.axis("off")
    ax._ptu = w * 72.0 / xmax          # points per canvas unit
    return fig, ax

def box(ax, x, y, w, h, lines=(), fc="white", ec=LINE, lw=0.9, hatch=None, ha="center", va="center", pad=1.2, zorder=3, ls="-"):
    """x,y = lower-left. lines = [(text, size, weight, color, family)] stacked from top."""
    patch = Rectangle((x, y), w, h, facecolor=FILL.get(fc, fc), edgecolor=ec, lw=lw, hatch=hatch, zorder=zorder, ls=ls)
    ax.add_patch(patch)
    if not lines: return patch
    ptu = getattr(ax, "_ptu", 4.8)
    heights = [(l[0].count("\n") + 1) * l[1] * 1.5 / ptu + 0.4 for l in lines]
    total = sum(heights); cy = y + h / 2 + total / 2 if va == "center" else y + h - pad
    cx = x + w / 2 if ha == "center" else x + pad
    for (t, sz, wt, col, fam), hh in zip(lines, heights):
        cy -= hh
        ax.text(cx, cy + hh * 0.5, t, fontsize=sz, fontweight=wt, color=col, family=fam, ha=ha, va="center", zorder=zorder + 1, linespacing=1.0,
                bbox=whitebox(alpha=0.92) if hatch else None)
    return patch

def L(t, sz=7.6, wt="normal", col=INK, fam=None):
    fam = fam or TH
    return (t, sz, wt, col, fam)
def LE(t, sz=6.3, wt="normal", col=INK_SEC):
    return (t, sz, wt, col, EN)

def arrow(ax, x1, y1, x2, y2, color=LINE, lw=0.9, ms=7, style="-|>", conn="arc3,rad=0", zorder=2, ls="-", patchA=None, patchB=None):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms, lw=lw, color=color, connectionstyle=conn, zorder=zorder, ls=ls, shrinkA=0, shrinkB=0, patchA=patchA, patchB=patchB))

def label(ax, x, y, t, sz=7, ha="center", va="center", color=INK, fam=None, wt="normal", bg=False, rot=0):
    ax.text(x, y, t, fontsize=sz, ha=ha, va=va, color=color, family=fam or TH, fontweight=wt, rotation=rot, zorder=8,
            bbox=whitebox() if bg else None, linespacing=1.15)

def hline(ax, x1, x2, y, color=LINE, lw=0.8, ls="-"):
    ax.plot([x1, x2], [y, y], color=color, lw=lw, ls=ls, zorder=2)
