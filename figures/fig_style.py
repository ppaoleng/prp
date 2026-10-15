"""Shared style for manuscript figures (muted, print-safe, thin lines, square corners)."""
import matplotlib as mpl
import matplotlib.pyplot as plt

INK = "#1a1a1a"
INK_SEC = "#5c5c58"
LINE = "#2b2b28"
ACCENT = "#3d6a8a"        # muted steel blue  -> recycled-aggregate stream
ACCENT_EDGE = "#274a63"
ACCENT_TINT = "#e7edf2"
WARM = "#9c7a52"          # muted warm brown  -> bamboo-biochar stream
WARM_EDGE = "#6e5636"
WARM_TINT = "#f0e9df"
NEUTRAL_FILL = "#e3e4e5"


def apply_style():
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"],
        "font.size": 9,
        "axes.linewidth": 0.8,
        "mathtext.fontset": "custom",
        "mathtext.rm": "Liberation Sans",
        "mathtext.cal": "Liberation Sans",
        "mathtext.it": "Liberation Sans:italic",
        "mathtext.bf": "Liberation Sans:bold",
        "mathtext.default": "regular",
        "pdf.fonttype": 42,   # embed TrueType, keeps text editable/searchable
        "svg.fonttype": "none",
    })


def save(fig, path_stem):
    """Save PNG (420 dpi) plus vector PDF/SVG alongside it."""
    kw = dict(bbox_inches="tight", facecolor="white", pad_inches=0.08)
    fig.savefig(f"{path_stem}.png", dpi=420, **kw)
    fig.savefig(f"{path_stem}.pdf", **kw)
    fig.savefig(f"{path_stem}.svg", **kw)
