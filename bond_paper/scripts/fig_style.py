"""Shared style for the Bond_RB_GFRP manuscript figures (muted, print-safe, thin lines)."""
import matplotlib as mpl
import matplotlib.pyplot as plt

INK = "#1a1a1a"; INK_SEC = "#5c5c58"; LINE = "#2b2b28"
STEEL = "#8f95a0"; STEEL_EDGE = "#4a5058"
ACCENT = "#3d6a8a"; ACCENT_EDGE = "#274a63"      # epoxy / primary series
WARM = "#9c7a52"; WARM_EDGE = "#6e5636"            # grout / secondary series
MORTAR = "#7a7a76"                                 # cement mortar (neutral gray)
CONCRETE = "#f2f1ec"; GROUND = "#e8e6df"; OK_GREEN = "#4f7a5c"
AGENT = {"Epoxy": ACCENT, "Non-shrink grout": WARM, "Cement mortar": MORTAR}
AGENT_HATCH = {"Epoxy": "////", "Non-shrink grout": "....", "Cement mortar": "xxxx"}
STRENGTH = {4.9: STEEL, 14.7: ACCENT, 23.5: WARM}   # nominal f'c series
STRENGTH_MK = {4.9: "o", 14.7: "s", 23.5: "^"}
DIAM = {6: "#4a5058", 9: ACCENT, 12: WARM}
DIAM_MK = {6: "o", 9: "s", 12: "^"}

def apply_style():
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Liberation Sans", "Arial", "DejaVu Sans"],
        "mathtext.fontset": "custom",
        "mathtext.rm": "Liberation Sans", "mathtext.it": "Liberation Sans:italic",
        "mathtext.bf": "Liberation Sans:bold", "mathtext.default": "it",
        "font.size": 9.6, "axes.labelsize": 9.6, "xtick.labelsize": 9, "ytick.labelsize": 9,
        "legend.fontsize": 8.6, "axes.edgecolor": INK, "axes.linewidth": 0.9,
        "xtick.color": INK, "ytick.color": INK, "text.color": INK, "axes.labelcolor": INK,
        "xtick.major.width": 0.9, "ytick.major.width": 0.9, "xtick.major.size": 3.5, "ytick.major.size": 3.5,
        "axes.spines.top": False, "axes.spines.right": False,
        "lines.linewidth": 1.3, "hatch.linewidth": 0.6, "legend.frameon": False,
        "figure.dpi": 120, "savefig.facecolor": "white",
    })

def panel_label(ax, s, x=0.0, y=1.02, **kw):
    ax.text(x, y, s, transform=ax.transAxes, fontweight="bold", fontsize=10.5, va="bottom", ha="left", **kw)

def save(fig, path):
    fig.savefig(path, dpi=420, bbox_inches="tight", facecolor="white", pad_inches=0.08)
    plt.close(fig)
    from PIL import Image
    w, h = Image.open(path).size
    print(path, w, "x", h)
