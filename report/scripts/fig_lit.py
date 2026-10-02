"""Literature positioning figures. ONLY statements that a verification agent actually saw in a source are used
(see data/lit_evidence_points.csv, which carries the quote and reference key for every row)."""
import os, sys, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from fig_style import *
from prp_data import *
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle
apply_style()

UP = "#7f9f8a"; NEUT = "#b9b9b2"; DOWN = "#c49a6c"; UNK = "#ffffff"
CAT = {"up": UP, "neutral": NEUT, "down": DOWN, "unknown": UNK}

# (study label, key, [(lo, hi, effect, note)])   dose = biochar mass as % of cement mass, as reported by each study
BIOCHAR = [
    ("Wang et al. 2020 (wood BC, CO$_2$ cured)", "wang2020", [(1, 1, "up", "+8.9 % strength"), (5, 5, "down", "strength reduced")]),
    ("Gupta & Kua 2019 (micro-filler)", "gupta2019", [(1, 2, "up", "")]),
    ("Suarez-Riera et al. 2020", "suarez2020", [(2, 2, "up", "filler: ↑; substitute: ≈")]),
    ("Ling et al. 2023", "ling2023", [(3, 3, "up", "hydration ↑")]),
    ("Sacdalan et al. 2023 (bamboo BC)", "sacdalan2023", [(2, 8, "up", "28 d ↑")]),
    ("Legan et al. 2025 (wood BC, cement repl.)", "legan2025", [(5, 5, "up", "+6 % (28 d)"), (10, 15, "down", "≤ control")]),
    ("Chin et al. 2025 (bamboo BC)", "chin2025", [(6, 6, "up", "optimum, 47.0 MPa")]),
    ("Ambaye et al. 2026 (MSW BC)", "ambaye2026", [(5, 5, "up", "optimum")]),
    ("Hylton et al. 2024 (selected BC)", "hylton2024", [(10, 10, "neutral", "no loss")]),
    ("Abbas & Thapa 2025", "abbas2025", [(5, 60, "unknown", "tested 5–60 %; block use")]),
]
def fig_biochar():
    fig, ax = plt.subplots(figsize=(6.7, 4.1))
    n = len(BIOCHAR); ys = np.arange(n + 1)[::-1] + 0.0
    for y, (lab, key, segs) in zip(ys[:-1], BIOCHAR):
        for lo, hi, eff, note in segs:
            a, b = lo / 1.12, hi * 1.12
            ax.add_patch(Rectangle((a, y - 0.3), b - a, 0.6, facecolor=CAT[eff], edgecolor=LINE, lw=0.8, hatch="////" if eff == "unknown" else None, zorder=3))
    # this study
    y0 = ys[-1]
    for dose, d, lab in ((7.5, -14, "Rab5"), (15, -35, "Rab10"), (22.5, -37, "Rab15")):
        ax.add_patch(Rectangle((dose / 1.12, y0 - 0.3), dose * 1.12 - dose / 1.12, 0.6, facecolor=DOWN, edgecolor=LINE, lw=0.8, zorder=3))
        ax.text(dose, y0 - 0.42, f"{d:+d} %", ha="center", va="top", fontsize=6.6, fontweight="bold")
    ax.axhline(y0 + 0.5, color=GRID, lw=1.0)
    ax.set_xscale("log"); ax.set_xlim(0.7, 90); ax.set_ylim(-0.9, n + 0.6)
    ax.set_xticks([1, 2, 5, 10, 20, 50]); ax.set_xticklabels(["1", "2", "5", "10", "20", "50"])
    ax.set_yticks(ys); ax.set_yticklabels([b[0] for b in BIOCHAR] + ["This study, Series I (28 d vs RA)"], fontsize=7.2)
    ax.get_yticklabels()[-1].set_fontweight("bold")
    ax.set_xlabel("Biochar dose (% of cement mass, as reported / as designed)")
    ax.xaxis.grid(True, color=GRID, lw=0.5, zorder=0, which="both")
    h = [Patch(facecolor=UP, edgecolor=LINE, label="Strength / hydration improved"), Patch(facecolor=NEUT, edgecolor=LINE, label="Maintained"),
         Patch(facecolor=DOWN, edgecolor=LINE, label="Reduced"), Patch(facecolor="white", edgecolor=LINE, hatch="////", label="Range tested, effect not extracted")]
    ax.legend(handles=h, loc="upper center", bbox_to_anchor=(0.36, -0.13), ncol=2, fontsize=6.8, frameon=False)
    fig.tight_layout(); save(fig, "r_lit_biochar")

RCA = [
    ("Wang et al. 2019 (coarse RCA)", [(60, 60, "up", "suggested")]),
    ("Wang et al. 2019 (fine RCA)", [(20, 20, "up", "suggested")]),
    ("Contreras Llanes et al. 2022", [(0.5, 50, "up", "feasible")]),
    ("Rodríguez et al. 2017", [(15, 15, "up", ""), (30, 30, "up", "")]),
    ("Namarak et al. 2018 (CCR–FA binder)", [(100, 100, "up", "41.4 MPa, 28 d")]),
    ("This study, Series II (RCA/sand)", [(5, 15, "up", "")]),
    ("This study, Series I (RCA/fine agg.)", [(50, 50, "up", "")]),
]
def fig_rca():
    fig, ax = plt.subplots(figsize=(6.7, 3.0)); n = len(RCA); ys = np.arange(n)[::-1]
    for y, (lab, segs) in zip(ys, RCA):
        for lo, hi, eff, note in segs:
            w = max(hi - lo, 0) + 3.0
            ax.add_patch(Rectangle((lo - 1.5, y - 0.28), w, 0.56, facecolor=UP if "This" not in lab else "#5f8a70", edgecolor=LINE, lw=0.8, zorder=3))
            if note: ax.text(hi + 3.2, y, note, va="center", fontsize=6.4, color=INK_SEC)
    ax.set_yticks(ys); ax.set_yticklabels([r[0] for r in RCA], fontsize=7.2)
    for t in ax.get_yticklabels()[-2:]: t.set_fontweight("bold")
    ax.set_xlim(-2, 128); ax.set_ylim(-0.7, n - 0.3); ax.set_xlabel("RCA replacement (% of natural aggregate, as defined in each study)")
    ax.axhline(1.5, color=GRID, lw=1.0); ax.xaxis.grid(True, color=GRID, lw=0.5, zorder=0); fig.tight_layout(); save(fig, "r_lit_rca")

if __name__ == "__main__":
    fig_biochar(); fig_rca()
    rows = []
    for lab, key, segs in BIOCHAR:
        for lo, hi, eff, note in segs: rows.append(dict(topic="biochar", study=lab, key=key, dose_lo=lo, dose_hi=hi, effect=eff, note=note))
    pd.DataFrame(rows).to_csv(os.path.join(DATA, "lit_evidence_points_biochar.csv"), index=False)
