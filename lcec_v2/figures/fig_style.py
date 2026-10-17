"""Shared style helpers for the LCEC manuscript figures (muted, print-safe, square corners)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch

INK = "#1a1a1a"
INK_SEC = "#5c5c58"
LINE = "#2b2b28"
STEEL = "#8f95a0"
STEEL_EDGE = "#4a5058"
PANEL = "#eef0f2"
ACCENT = "#3d6a8a"        # LC / primary
ACCENT_EDGE = "#274a63"
ACCENT_TINT = "#e3ebf1"
GREEN = "#4f7a5c"         # E
GREEN_EDGE = "#35553f"
GREEN_TINT = "#e5ede7"
WARM = "#9c7a52"          # C / emphasis
WARM_EDGE = "#6e5636"
WARM_TINT = "#f1e9de"
GREY_TINT = "#f4f4f2"

W_TEXT = 6.37             # A4 text width of the manuscript (inches)
FONT = "Liberation Sans"  # metric-compatible with Arial


def apply_style():
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": [FONT, "Arial", "DejaVu Sans"],
        "font.size": 8,
        "axes.linewidth": 0.8,
        "axes.edgecolor": INK,
        "text.color": INK,
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
    })


def save(fig, path, dpi=420):
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white", pad_inches=0.06)


class Canvas:
    """Inch-based drawing surface with word-wrapped rich text."""

    def __init__(self, width, height=30.0):
        apply_style()
        self.W = width
        self.fig = plt.figure(figsize=(width, height), dpi=100)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, width)
        self.ax.set_ylim(0, height)
        self.ax.axis("off")
        self.H = height
        self.r = self.fig.canvas.get_renderer()
        self.ymin = height

    # ---- text measurement -------------------------------------------------
    def _w(self, s, size, weight="normal", style="normal"):
        from matplotlib.font_manager import FontProperties
        fp = FontProperties(family=[FONT, "DejaVu Sans"], size=size, weight=weight, style=style)
        w, h, d = self.r.get_text_width_height_descent(s, fp, ismath=False)
        return w / self.fig.dpi

    def wrap(self, segs, width, size):
        """segs: list of (text, weight, style, color). Returns list of lines; line = [(word,w,weight,style,color)]."""
        words = []
        for text, wt, st, col in segs:
            for i, tok in enumerate(text.split(" ")):
                if tok == "":
                    continue
                words.append((tok, self._w(tok, size, wt, st), wt, st, col))
        space = self._w("a a", size) - self._w("aa", size)
        lines, cur, curw = [], [], 0.0
        for wd in words:
            add = wd[1] + (space if cur else 0)
            if cur and curw + add > width:
                lines.append(cur)
                cur, curw = [wd], wd[1]
            else:
                cur.append(wd)
                curw += add
        if cur:
            lines.append(cur)
        return lines, space

    def para(self, x, ytop, width, segs, size=8, align="left", lh=1.26, draw=True, color=None):
        """Draw (or just measure) a wrapped paragraph. x = left edge (align left/center uses box [x, x+width]).
        Returns height in inches."""
        if isinstance(segs, str):
            segs = [(segs, "normal", "normal", color or INK)]
        segs = [(t, w, s, (c or color or INK)) for (t, w, s, c) in segs]
        lines, space = self.wrap(segs, width, size)
        lhin = size * lh / 72.0
        if draw:
            for i, ln in enumerate(lines):
                tw = sum(w[1] for w in ln) + space * (len(ln) - 1)
                if align == "center":
                    cx = x + (width - tw) / 2
                elif align == "right":
                    cx = x + width - tw
                else:
                    cx = x
                yb = ytop - (i + 0.82) * lhin
                for (tok, w, wt, st, col) in ln:
                    self.ax.text(cx, yb, tok, fontsize=size, fontweight=wt, fontstyle=st,
                                 color=col, ha="left", va="baseline", zorder=6)
                    cx += w + space
        h = len(lines) * lhin
        if draw:
            self.ymin = min(self.ymin, ytop - h)
        return h

    # ---- shapes -----------------------------------------------------------
    def rect(self, x, ytop, w, h, fc="white", ec=STEEL_EDGE, lw=0.8, ls="-", z=2, hatch=None):
        p = Rectangle((x, ytop - h), w, h, facecolor=fc, edgecolor=ec, linewidth=lw, linestyle=ls,
                      zorder=z, hatch=hatch, joinstyle="miter")
        self.ax.add_patch(p)
        self.ymin = min(self.ymin, ytop - h)
        return p

    def line(self, pts, color=STEEL_EDGE, lw=0.9, ls="-", z=3):
        xs, ys = zip(*pts)
        self.ax.plot(xs, ys, color=color, lw=lw, ls=ls, zorder=z, solid_capstyle="butt",
                     dash_capstyle="butt")
        self.ymin = min(self.ymin, min(ys))

    def arrow(self, p0, p1, color=INK, lw=0.9, ls="-", z=4, ms=7):
        a = FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=ms, color=color, lw=lw,
                            linestyle=ls, shrinkA=0, shrinkB=0, zorder=z)
        self.ax.add_patch(a)
        self.ymin = min(self.ymin, p0[1], p1[1])

    def finish(self, path, top=None):
        top = top if top is not None else self.H
        bottom = self.ymin - 0.03
        self.ax.set_ylim(bottom, top)
        self.fig.set_size_inches(self.W, top - bottom)
        save(self.fig, path)
        plt.close(self.fig)
