"""Shared style for the manuscript figures (muted, print-safe, thin lines, square corners).

Rules followed (PRP academic-figure-style):
  * no 'Fig. N' / titles / captions baked into the image
  * restrained palette, CVD-checked; secondary encoding (hatch, marker shape, line style)
  * thin lines, rectangles with square corners, no shadows
  * standard hatch symbols for materials (ballast, sub-ballast, PU, concrete, steel)
  * white bbox behind any label placed over a hatched region
  * dpi 420 + bbox_inches='tight'; pixel size verified after saving
"""
from pathlib import Path
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

OUT = Path(__file__).resolve().parent.parent / "figures"

# ---- neutrals -----------------------------------------------------------
INK = "#1a1a1a"
INK_SEC = "#5c5c58"
LINE = "#2b2b28"
GRID = "#e4e3de"
STEEL = "#8f95a0"
STEEL_EDGE = "#4a5058"
ACCENT = "#3d6a8a"
ACCENT_EDGE = "#274a63"
WARM = "#9c7a52"
WARM_EDGE = "#6e5636"
GROUND = "#f2f1ec"
SOIL_SAND = "#efece0"
OK_GREEN = "#4f7a5c"

# ---- model series (validated: CVD dE >= 8, normal-vision dE >= 15, contrast >= 3:1) ----
SERIES = {"M1": "#222220", "M2": "#33689a", "M3": "#b5822e", "M4": "#3f8f86", "M5": "#7b4b86"}
MARKER = {"M1": "s", "M2": "o", "M3": "^", "M4": "D", "M5": "v"}
LSTYLE = {"M1": "-", "M2": (0, (5, 2)), "M3": (0, (6, 2, 1.5, 2)), "M4": (0, (1.2, 1.6)), "M5": (0, (6, 2, 1.2, 2, 1.2, 2))}
HATCH = {"M1": "", "M2": "////", "M3": "\\\\\\\\", "M4": "....", "M5": "xxxx"}
LABEL = {"M1": "M1 (unmodified)", "M2": "M2 (PU)", "M3": "M3 (PU + AR)",
         "M4": "M4 (PU + ES)", "M5": "M5 (PU + AR + ES)"}


def apply_style(base=8.5):
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Liberation Sans", "Arial", "Helvetica", "DejaVu Sans"],
        "font.size": base,
        "axes.labelsize": base + 0.3,
        "axes.titlesize": base + 0.3,
        "xtick.labelsize": base,
        "ytick.labelsize": base,
        "legend.fontsize": base - 0.5,
        "axes.edgecolor": LINE,
        "axes.linewidth": 0.8,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": LINE,
        "ytick.color": LINE,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "xtick.major.size": 3.0,
        "ytick.major.size": 3.0,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "hatch.linewidth": 0.55,
        "lines.solid_capstyle": "butt",
        "mathtext.fontset": "custom",
        "mathtext.rm": "Liberation Sans",
        "mathtext.it": "Liberation Sans:italic",
        "mathtext.bf": "Liberation Sans:bold",
        "mathtext.default": "it",
        "savefig.facecolor": "white",
        "figure.facecolor": "white",
        "pdf.fonttype": 42,
    })


def save(fig, name, dpi=420):
    """Save as PNG (manuscript) and verify the pixel size (Springer minimum 1500 x 1200 px)."""
    OUT.mkdir(exist_ok=True)
    path = OUT / f"{name}.png"
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white", pad_inches=0.08)
    with Image.open(path) as im:
        w, h = im.size
    print(f"{path.name}: {w} x {h} px  ({w/dpi:.2f} x {h/dpi:.2f} in at {dpi} dpi)")
    plt.close(fig)
    return path


def halo(**kw):
    """White label background for text over hatched/busy regions."""
    d = dict(boxstyle="square,pad=0.15", facecolor="white", edgecolor="none", alpha=0.92)
    d.update(kw)
    return d


def hatched_bar(ax, x, h, w, color, hatch, y0=0.0, lw=0.7, edge=INK, z=3):
    """Bar = coloured fill + white hatch lines + thin dark outline (square corners)."""
    from matplotlib.patches import Rectangle
    ax.add_patch(Rectangle((x - w / 2, y0), w, h, facecolor=color, edgecolor="white",
                           hatch=hatch, linewidth=0, zorder=z))
    ax.add_patch(Rectangle((x - w / 2, y0), w, h, facecolor="none", edgecolor=edge,
                           linewidth=lw, zorder=z + 0.1))
