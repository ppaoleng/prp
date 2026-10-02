"""Shared figure style for the PRP 2569 report (follows PRP's academic-figure-style rules):
muted print-safe palette, thin lines, square corners, hatch instead of flat fills, no baked-in
'Fig. N' / title text, 420 dpi export, English axis labels."""
import os, matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "..", "figures")
os.makedirs(FIG, exist_ok=True)

INK = "#1a1a1a"; INK_SEC = "#5c5c58"; LINE = "#2b2b28"
STEEL = "#8f95a0"; STEEL_EDGE = "#4a5058"
ACCENT = "#3d6a8a"; ACCENT_EDGE = "#274a63"
WARM = "#9c7a52"; WARM_EDGE = "#6e5636"
OK_GREEN = "#4f7a5c"; RED_PH = "#c00000"; PAPER = "#f4f2ec"; GRID = "#d9d7d0"
# sequential ramps (light -> dark)
BLUE_RAMP = ["#aeb4be", "#86a3ba", "#4f7ba0", "#274a63"]      # biochar 0,5,10,15 %
WARM_RAMP = ["#cdbba2", "#b99d74", "#9c7a52", "#6e5636"]      # RCA 0,5,10,15 %
MIXCOL = {"NA": "#3a3a38", "RA": BLUE_RAMP[0], "Rab5": BLUE_RAMP[1], "Rab10": BLUE_RAMP[2], "Rab15": BLUE_RAMP[3],
          "RCA0": WARM_RAMP[0], "RCA5": WARM_RAMP[1], "RCA10": WARM_RAMP[2], "RCA15": WARM_RAMP[3]}
AGEHATCH = {7: "////", 14: "....", 28: ""}
AGEMARK = {7: "o", 14: "s", 28: "^"}
LAB = {"NA": "NA", "RA": "RA", "Rab5": "Rab5%", "Rab10": "Rab10%", "Rab15": "Rab15%", "Rab20": "Rab20%", "Rab25": "Rab25%",
       "RCA0": "RCA0%", "RCA5": "RCA5%", "RCA10": "RCA10%", "RCA15": "RCA15%"}

_have = {f.name for f in fm.fontManager.ttflist}
SANS = [f for f in ("Liberation Sans", "Arial", "DejaVu Sans") if f in _have][:1] or ["DejaVu Sans"]
THAI = [f for f in ("Garuda", "Loma", "Laksaman", "Kinnari") if f in _have][:1] or ["DejaVu Sans"]

def apply_style():
    mpl.rcParams.update({
        "font.family": SANS + ["DejaVu Sans"], "font.size": 8.6, "axes.titlesize": 9,
        "axes.labelsize": 8.8, "xtick.labelsize": 8.2, "ytick.labelsize": 8.2, "legend.fontsize": 7.8,
        "axes.edgecolor": LINE, "axes.linewidth": 0.9, "axes.labelcolor": INK, "text.color": INK,
        "xtick.color": LINE, "ytick.color": LINE, "xtick.direction": "in", "ytick.direction": "in",
        "xtick.major.width": 0.8, "ytick.major.width": 0.8, "xtick.major.size": 3.2, "ytick.major.size": 3.2,
        "xtick.top": True, "ytick.right": True, "lines.linewidth": 1.2, "lines.markersize": 4.6,
        "patch.linewidth": 0.8, "hatch.linewidth": 0.6, "legend.frameon": True, "legend.edgecolor": "#8c8c88",
        "legend.fancybox": False, "legend.framealpha": 0.95, "legend.borderpad": 0.45,
        "axes.grid": False, "figure.dpi": 110, "savefig.dpi": 420, "pdf.fonttype": 42,
        "mathtext.default": "regular", "axes.unicode_minus": True,
    })

def save(fig, name, pad=0.08):
    path = os.path.join(FIG, name if name.endswith(".png") else name + ".png")
    fig.savefig(path, dpi=420, bbox_inches="tight", facecolor="white", pad_inches=pad)
    plt.close(fig)
    from PIL import Image
    w, h = Image.open(path).size
    print(f"saved {os.path.basename(path)}  {w}x{h}px")
    return path

def ph_tag(ax, text="[Place Holder]", loc="upper left", fs=7.6):
    """Small bold-red tag marking data that are NOT measurements."""
    xy = {"upper left": (0.012, 0.985, "left", "top"), "upper right": (0.988, 0.985, "right", "top"),
          "lower left": (0.012, 0.015, "left", "bottom")}[loc]
    ax.text(xy[0], xy[1], text, transform=ax.transAxes, ha=xy[2], va=xy[3], color=RED_PH,
            fontsize=fs, fontweight="bold", zorder=20,
            bbox=dict(boxstyle="square,pad=0.18", facecolor="white", edgecolor=RED_PH, linewidth=0.6, alpha=0.95))

def panel(ax, s, dx=-0.0, dy=1.02):
    ax.text(dx, dy, s, transform=ax.transAxes, ha="left", va="bottom", fontsize=9.5, fontweight="bold")

def whitebox(**kw):
    d = dict(boxstyle="square,pad=0.2", facecolor="white", edgecolor="none", alpha=0.9); d.update(kw); return d
