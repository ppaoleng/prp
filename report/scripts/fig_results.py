import os, sys, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from fig_style import *
from prp_data import *
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
apply_style()
S = strength_summary()
L = strength_long()
D = density_long()

def age_legend(ax, loc="upper right", ncol=3):
    h = [Patch(facecolor="white", edgecolor=LINE, hatch=AGEHATCH[a], label=f"{a} d") for a in (7, 14, 28)]
    return ax.legend(handles=h, loc=loc, ncol=ncol, title="Curing age", title_fontsize=7.6, handlelength=1.8, columnspacing=1.0)

# ---------- Fig: density (series I) ----------
def fig_density():
    fig, ax = plt.subplots(1, 2, figsize=(6.5, 3.0), gridspec_kw={"width_ratios": [1.15, 1]})
    g = D.groupby(["mix", "age_d"]).density.agg(["mean", "std"]).reset_index()
    # (a) bars by mix & age
    a = ax[0]; w = 0.26; x = np.arange(len(S1_ORDER))
    for j, age in enumerate((7, 14, 28)):
        sub = g[g.age_d == age].set_index("mix").reindex(S1_ORDER)
        a.bar(x + (j - 1) * w, sub["mean"], w, yerr=sub["std"], color=[MIXCOL[m] for m in S1_ORDER], edgecolor=LINE,
              hatch=AGEHATCH[age], capsize=2, error_kw=dict(lw=0.8, capthick=0.8), zorder=3)
    a.set_xticks(x); a.set_xticklabels([LAB[m] for m in S1_ORDER], rotation=0)
    a.set_ylim(1800, 2400); a.set_ylabel("Density (kg/m$^3$)"); a.yaxis.grid(True, color=GRID, lw=0.5, zorder=0)
    age_legend(a, "upper right"); panel(a, "(a)")
    # (b) density vs biochar content (all ages pooled mean) + linear fit
    b = ax[1]
    pooled = D.groupby("mix").density.agg(["mean", "std", "count"]).reindex(S1_ORDER)
    xs = np.array([S1_BIOCHAR[m] for m in S1_ORDER])
    b.errorbar(xs[1:], pooled["mean"].iloc[1:], yerr=pooled["std"].iloc[1:], fmt="o", color=ACCENT_EDGE, mfc=ACCENT, capsize=2.5, zorder=4, label="RCA 50 % series (RA, Rab)")
    b.errorbar([-4.2], pooled["mean"].iloc[0], yerr=pooled["std"].iloc[0], fmt="D", color=INK, mfc="white", capsize=2.5, zorder=4, label="NA (all-natural)")
    from scipy import stats
    sl, ic, r, p, se = stats.linregress(D[D.mix != "NA"].mix.map(S1_BIOCHAR), D[D.mix != "NA"].density)
    xx = np.linspace(0, 15, 50); b.plot(xx, ic + sl * xx, "--", color=ACCENT_EDGE, lw=1.0, label=f"Linear fit (R$^2$={r**2:.2f})")
    b.set_xlim(-6, 17); b.set_ylim(1900, 2350); b.set_xlabel("Cement reduction / biochar level (nominal, %)"); b.set_ylabel("Density (kg/m$^3$)")
    b.yaxis.grid(True, color=GRID, lw=0.5, zorder=0); b.legend(loc="upper right", fontsize=7); panel(b, "(b)")
    fig.tight_layout(w_pad=1.2)
    save(fig, "r_density_s1")
    return sl, r**2, p

# ---------- helper: grouped strength bars ----------
def bars(series, order, xlab, fname, ymax, lines=True):
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    w = 0.26; x = np.arange(len(order))
    for j, age in enumerate((7, 14, 28)):
        sub = S[(S.series == series) & (S.age == age)].set_index("mix").reindex(order)
        ax.bar(x + (j - 1) * w, sub["mean"], w, yerr=sub["sd"], color=[MIXCOL[m] for m in order], edgecolor=LINE,
               hatch=AGEHATCH[age], capsize=2, error_kw=dict(lw=0.8, capthick=0.8), zorder=3)
        if age == 28:
            for xi, v, sd in zip(x + (j - 1) * w, sub["mean"], sub["sd"]):
                ax.text(xi, v + sd + ymax * 0.012, f"{v:.1f}", ha="center", va="bottom", fontsize=7, zorder=6)
    ax.axhline(TIS827_MPa, color=INK, ls="--", lw=0.9, zorder=2)
    ax.axhline(TIS2035_MPa, color=WARM_EDGE, ls="-.", lw=0.9, zorder=2)
    ax.text(len(order) - 0.52, TIS827_MPa - ymax * 0.012, "TIS 827-2565: 35 MPa", ha="right", va="top", fontsize=6.8, bbox=whitebox(), zorder=7)
    ax.text(len(order) - 0.52, TIS2035_MPa + ymax * 0.012, "TIS 2035-2565: 50 MPa", ha="right", va="bottom", fontsize=6.8, color=WARM_EDGE, bbox=whitebox(), zorder=7)
    ax.set_xticks(x); ax.set_xticklabels([LAB[m] for m in order]); ax.set_ylim(0, ymax)
    ax.set_ylabel("Compressive strength (MPa)"); ax.set_xlabel(xlab); ax.yaxis.grid(True, color=GRID, lw=0.5, zorder=0)
    age_legend(ax, "upper right")
    fig.tight_layout(); save(fig, fname)

# ---------- Strength development curves ----------
def dev(series, order, fname, ymax, cols):
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    for m in order:
        sub = S[(S.series == series) & (S.mix == m)].sort_values("age")
        ax.errorbar(sub.age, sub["mean"], yerr=sub["sd"], marker="o", color=cols[m], mec=LINE, mfc=cols[m], capsize=2,
                    lw=1.2, label=LAB[m], zorder=4)
    ax.axhline(TIS827_MPa, color=INK, ls="--", lw=0.9); ax.axhline(TIS2035_MPa, color=WARM_EDGE, ls="-.", lw=0.9)
    ax.set_xticks([7, 14, 28]); ax.set_xlim(5, 30); ax.set_ylim(0, ymax)
    ax.set_xlabel("Curing age (d)"); ax.set_ylabel("Compressive strength (MPa)"); ax.yaxis.grid(True, color=GRID, lw=0.5)
    ax.legend(loc="lower right", ncol=2, fontsize=7.4); fig.tight_layout(); save(fig, fname)

# ---------- Relative strength vs replacement ----------
def rel_s1():
    fig, ax = plt.subplots(1, 2, figsize=(6.5, 3.0))
    ctrl = S[(S.mix == "RA") & (S.age == 28)]["mean_reported"].iloc[0]
    for age in (7, 14, 28):
        sub = S[(S.series == "I") & (S.age == age) & (S.mix != "NA")].set_index("mix").reindex(["RA", "Rab5", "Rab10", "Rab15"])
        c28 = sub.loc["RA", "mean_reported"]
        ax[0].plot([0, 5, 10, 15], sub["mean_reported"] / c28 * 100, marker=AGEMARK[age], color=ACCENT_EDGE, mfc=ACCENT if age == 28 else "white",
                   label=f"{age} d", lw=1.1)
    ax[0].axhline(100, color=INK_SEC, lw=0.7, ls=":")
    ax[0].set_xlabel("Cement reduction (nominal %)"); ax[0].set_ylabel("Strength relative to RA at same age (%)")
    ax[0].set_ylim(50, 150); ax[0].set_xticks([0, 5, 10, 15]); ax[0].legend(loc="upper right"); panel(ax[0], "(a)")
    ax[0].yaxis.grid(True, color=GRID, lw=0.5)
    # (b) cement efficiency: MPa per 100 kg cement (28 d)
    inv = pd.read_csv(os.path.join(DATA, "lca_inventory_kg_per_m3.csv"), keep_default_na=False).set_index("mix")
    s28 = S[(S.age == 28)].set_index("mix")["mean_reported"]
    xs = ["RA", "Rab5", "Rab10", "Rab15"]
    eff = [s28[m] / inv.loc[m, "cement"] * 100 for m in xs]
    ax[1].bar(range(4), eff, 0.55, color=[MIXCOL[m] for m in xs], edgecolor=LINE, zorder=3)
    for i, e in enumerate(eff): ax[1].text(i, e + 0.3, f"{e:.1f}", ha="center", fontsize=7.5)
    ax[1].set_xticks(range(4)); ax[1].set_xticklabels([LAB[m] for m in xs]); ax[1].set_ylim(0, 20)
    ax[1].set_ylabel("28-d strength per 100 kg cement (MPa)"); ax[1].yaxis.grid(True, color=GRID, lw=0.5, zorder=0); panel(ax[1], "(b)")
    fig.tight_layout(w_pad=1.4); save(fig, "r_fc_s1_rel")

def rel_s2():
    fig, ax = plt.subplots(1, 2, figsize=(6.5, 3.0))
    x = [0, 5, 10, 15]; order = S2_ORDER
    for age in (7, 14, 28):
        sub = S[(S.series == "II") & (S.age == age)].set_index("mix").reindex(order)
        ax[0].plot(x, sub["mean_reported"] / sub.loc["RCA0", "mean_reported"] * 100, marker=AGEMARK[age], color=WARM_EDGE,
                   mfc=WARM if age == 28 else "white", label=f"{age} d", lw=1.1)
    ax[0].axhline(100, color=INK_SEC, lw=0.7, ls=":"); ax[0].set_ylim(80, 160)
    ax[0].set_xlabel("Sand replaced by RCA (%)"); ax[0].set_ylabel("Strength relative to RCA0% at same age (%)")
    ax[0].set_xticks(x); ax[0].legend(loc="upper left"); ax[0].yaxis.grid(True, color=GRID, lw=0.5); panel(ax[0], "(a)")
    # (b) strength gain ratios
    gain = []
    for m in order:
        s = S[(S.series == "II") & (S.mix == m)].set_index("age")["mean_reported"]
        gain.append((s[14] / s[7], s[28] / s[14]))
    w = 0.34; xi = np.arange(4)
    ax[1].bar(xi - w / 2, [g[0] for g in gain], w, color="white", edgecolor=LINE, hatch="....", label="14 d / 7 d", zorder=3)
    ax[1].bar(xi + w / 2, [g[1] for g in gain], w, color=[MIXCOL[m] for m in order], edgecolor=LINE, label="28 d / 14 d", zorder=3)
    ax[1].axhspan(1.10, 1.35, color="#e6e4dc", zorder=0)
    ax[1].text(-0.45, 0.2, "shaded: 1.10\u20131.35 (indicative\nrange, see Sec. 4.3.3)", ha="left", va="bottom", fontsize=6.6, color=INK_SEC, bbox=whitebox(), zorder=8)
    ax[1].set_xticks(xi); ax[1].set_xticklabels([LAB[m] for m in order]); ax[1].set_ylim(0, 2.6)
    ax[1].set_ylabel("Strength ratio between ages (–)"); ax[1].legend(loc="upper right", fontsize=7); panel(ax[1], "(b)")
    fig.tight_layout(w_pad=1.4); save(fig, "r_fc_s2_rel")

if __name__ == "__main__":
    import lca_model; lca_model.run()
    print(fig_density())
    bars("I", S1_ORDER, "Mix (cement reduced / replaced by biochar, nominal %)", "r_fc_s1_bars", 125)
    dev("I", S1_ORDER, "r_fc_s1_dev", 115, MIXCOL)
    rel_s1()
    bars("II", S2_ORDER, "Sand replaced by RCA (%)", "r_fc_s2_bars", 85)
    dev("II", S2_ORDER, "r_fc_s2_dev", 80, MIXCOL)
    rel_s2()
