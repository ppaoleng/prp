import os, sys, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from fig_style import *
from prp_data import *
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
apply_style()
S = strength_summary()
COMP = {"cement": "#8a6a45", "sand": "#d8cdb4", "stone": "#a9a9a2", "rca": "#6f7e8c", "biochar": "#2b2b28"}
HATCH = {"cement": "", "sand": "..", "stone": "xx", "rca": "//", "biochar": ""}

def fig_mix():
    import lca_model
    inv = lca_model.inventory() * lca_model.BLOCK_VOLUME_M3 * 1000     # g per batch
    order = ["NA", "RA", "Rab5", "Rab10", "Rab15", "Rab20", "Rab25", "RCA0", "RCA5", "RCA10", "RCA15"]
    fig, ax = plt.subplots(figsize=(6.6, 3.5)); ys = np.arange(len(order))[::-1]
    for y, m in zip(ys, order):
        left = 0
        for c in ("cement", "biochar", "sand", "stone", "rca"):
            v = inv.loc[m, c]
            if v > 0:
                ax.barh(y, v, 0.62, left=left, color=COMP[c], edgecolor=LINE, lw=0.6, hatch=HATCH[c], zorder=3)
                if v >= 120: ax.text(left + v / 2, y, f"{v:.0f}", ha="center", va="center", fontsize=6.2, color="white" if c in ("cement", "biochar", "rca") else INK, zorder=6, bbox=None if c in ("cement", "biochar", "rca") else whitebox(alpha=0.85, boxstyle="square,pad=0.12"))
            left += v
        ax.text(left + 25, y, f"{left:.0f}", va="center", fontsize=6.6, color=INK_SEC)
    ax.set_yticks(ys); ax.set_yticklabels([LAB[m] + ("*" if m in ("Rab20", "Rab25") else "") for m in order], fontsize=7.4)
    ax.axhline(4.5 + 0.0 + (len(order) - 11), color=GRID, lw=0)
    ax.axhline(len(order) - 7.5 + 0.0, color=GRID, lw=1.0); ax.axhline(3.5, color=GRID, lw=1.0)
    ax.set_xlim(0, 3800); ax.set_xlabel("Dry batch mass per block (g)"); ax.xaxis.grid(True, color=GRID, lw=0.4, zorder=0)
    h = [Patch(facecolor=COMP[c], edgecolor=LINE, hatch=HATCH[c], label=l) for c, l in (("cement", "Cement"), ("biochar", "Biochar"), ("sand", "Sand"), ("stone", "Stone"), ("rca", "RCA"))]
    ax.legend(handles=h, loc="lower center", bbox_to_anchor=(0.5, -0.26), ncol=5, fontsize=7, frameon=False)
    fig.tight_layout(); save(fig, "r_mix_design")

def fig_porosity():
    Dg = density_long().query("age_d==28").groupby("mix").density.mean()
    s28 = S[S.age == 28].set_index("mix")
    order = S1_ORDER
    x = np.array([Dg[m] / Dg["NA"] for m in order]); y = np.array([s28.loc[m, "mean_reported"] / s28.loc["NA", "mean_reported"] for m in order])
    sl, ic, r, p, se = stats.linregress(np.log(x), np.log(y))
    fig, ax = plt.subplots(figsize=(4.9, 3.2))
    xx = np.linspace(0.86, 1.01, 60)
    for n, ls in ((4, ":"), (6, "--"), (8, "-.")):
        ax.plot(xx, xx ** n, color=GRID if n != 6 else INK_SEC, ls=ls, lw=1.0, label=f"f/f$_{{NA}}$ = (ρ/ρ$_{{NA}}$)$^{{{n}}}$")
    ax.plot(xx, np.exp(ic) * xx ** sl, color=ACCENT_EDGE, lw=1.4, label=f"fit: exponent {sl:.1f} (R$^2$ = {r**2:.2f})")
    for xi, yi, m in zip(x, y, order):
        ax.plot(xi, yi, "o", mfc=MIXCOL[m], mec=LINE, ms=7, zorder=5); ax.annotate(LAB[m], (xi, yi), xytext=(5, -9 if m != "Rab10" else 6), textcoords="offset points", fontsize=7)
    ax.set_xlabel("Relative density at 28 d, ρ/ρ$_{NA}$ (–)"); ax.set_ylabel("Relative strength at 28 d, f/f$_{NA}$ (–)"); ax.set_xlim(0.86, 1.015); ax.set_ylim(0.3, 1.1)
    ax.legend(loc="upper left", fontsize=6.8); ax.yaxis.grid(True, color=GRID, lw=0.5)
    fig.tight_layout(); save(fig, "r_porosity_model")
    return sl, r ** 2, p

def fig_cost():
    """Relative material-cost screening. Price unit = cement price per kg (=1). Draft sec. 1.1: cement ~10x sand price -> sand, stone = 0.1.
    Biochar price ratio r is the unknown parameter; RCA treated as free (lab waste, crushing cost excluded)."""
    import lca_model
    inv = lca_model.inventory()
    fc = S[S.age == 28].set_index("mix")["mean_reported"]
    r = np.linspace(0, 1.2, 50)
    fig, ax = plt.subplots(1, 2, figsize=(6.6, 3.0)); a, b = ax
    def cost(m, rr): return inv.loc[m, "cement"] * 1 + (inv.loc[m, "sand"] + inv.loc[m, "stone"]) * 0.1 + inv.loc[m, "biochar"] * rr
    for m in ("Rab5", "Rab10", "Rab15"):
        a.plot(r, (cost(m, r) / cost("RA", 0) - 1) * 100, color=MIXCOL[m], lw=1.3, label=LAB[m])
    a.axhline(0, color=INK, lw=0.8); a.axvline(2 / 3, color=INK_SEC, ls="--", lw=0.8)
    a.text(2 / 3 + 0.02, 7.5, "break-even\nr = Δcement / biochar\n= 0.67", fontsize=6.4, color=INK_SEC, va="top")
    a.set_xlabel("Biochar price relative to cement, r (–)"); a.set_ylabel("Material cost vs RA (%)"); a.legend(loc="upper left", fontsize=6.8); panel(a, "(a)")
    a.yaxis.grid(True, color=GRID, lw=0.5)
    for m in ("RA", "Rab5", "Rab10", "Rab15"):
        b.plot(r, (cost(m, r) / fc[m]) / (cost("RA", 0) / fc["RA"]) * 100, color=MIXCOL[m] if m != "RA" else INK_SEC, lw=1.3, label=LAB[m], ls="--" if m == "RA" else "-")
    b.axhline(100, color=INK, lw=0.8); b.set_xlabel("Biochar price relative to cement, r (–)"); b.set_ylabel("Material cost per MPa vs RA (%)")
    b.set_ylim(90, 260); b.legend(loc="upper left", fontsize=6.8); panel(b, "(b)"); b.yaxis.grid(True, color=GRID, lw=0.5)
    fig.tight_layout(w_pad=1.3); save(fig, "r_cost")
    rows = []
    for m in ("RA", "Rab5", "Rab10", "Rab15"):
        for rr in (0, 0.5, 1.0):
            rows.append(dict(mix=m, r=rr, rel_cost_vs_RA=cost(m, rr) / cost("RA", 0), rel_cost_per_MPa_vs_RA=(cost(m, rr) / fc[m]) / (cost("RA", 0) / fc["RA"])))
    pd.DataFrame(rows).round(4).to_csv(os.path.join(DATA, "cost_screening_relative.csv"), index=False)
    return pd.DataFrame(rows)

if __name__ == "__main__":
    fig_mix(); print(fig_porosity()); print(fig_cost().round(3).to_string())
