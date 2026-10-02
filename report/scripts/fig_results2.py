import os, sys, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from fig_style import *
from prp_data import *
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
apply_style()
S = strength_summary(); L = strength_long(); A = absorption_long()
fits = pd.read_csv(os.path.join(DATA, "stats_maturity_fits.csv"), keep_default_na=False)

# ---------------- water absorption ----------------
def fig_abs():
    fig, ax = plt.subplots(1, 2, figsize=(6.6, 3.1), gridspec_kw={"width_ratios": [1.1, 1]})
    a = ax[0]; w = 0.26; x = np.arange(4)
    for j, age in enumerate((7, 14, 28)):
        sub = A[(A.series == "II") & (A.age == age)]
        means = [sub[sub.mix == m].ab.mean() for m in S2_ORDER]
        a.bar(x + (j - 1) * w, means, w, color=[MIXCOL[m] for m in S2_ORDER], edgecolor=LINE, hatch=AGEHATCH[age], zorder=3)
        for i, m in enumerate(S2_ORDER):
            v = sub[sub.mix == m].ab.values
            a.plot(np.full(len(v), x[i] + (j - 1) * w) + np.linspace(-0.05, 0.05, len(v)), v, "k.", ms=3, zorder=5)
    a.axhline(5.0, color=INK, ls="--", lw=0.9); a.text(3.45, 5.08, "5 % (ASTM C936 / TIS 2035 as listed in Table 2-1)", ha="right", va="bottom", fontsize=6.4, bbox=whitebox())
    a.set_ylim(0, 6.2); a.set_xticks(x); a.set_xticklabels([LAB[m] for m in S2_ORDER]); a.set_ylabel("72-h water absorption (%)")
    a.set_xlabel("Sand replaced by RCA (%)"); a.yaxis.grid(True, color=GRID, lw=0.5, zorder=0)
    h = [Patch(facecolor="white", edgecolor=LINE, hatch=AGEHATCH[g], label=f"{g} d") for g in (7, 14, 28)]
    a.legend(handles=h, loc="upper left", ncol=3, fontsize=7, handlelength=1.5, columnspacing=0.8); panel(a, "(a)")
    # (b) quantisation strip: all series-II values vs 0.30 % grid
    b = ax[1]; vals = np.sort(A[A.series == "II"].ab.values); step = 0.01 / 3.33 * 100
    for k in range(0, 10): b.axvline(k * step, color=GRID, lw=0.7, zorder=0)
    ages = A[A.series == "II"].sort_values("ab")
    mk = {7: "o", 14: "s", 28: "^"}
    for age in (7, 14, 28):
        v = ages[ages.age == age].ab.values
        b.scatter(v, np.full(len(v), age) + np.random.default_rng(3).uniform(-1.4, 1.4, len(v)), marker=mk[age], s=16, facecolor="white" if age != 28 else INK_SEC,
                  edgecolor=LINE, lw=0.8, zorder=4)
    b.set_yticks([7, 14, 28]); b.set_yticklabels(["7 d", "14 d", "28 d"]); b.set_ylim(2, 33); b.set_xlim(-0.1, 3.0)
    b.set_xlabel("Absorption (%)  [grid = 0.01 kg / 3.33 kg = 0.30 %]"); panel(b, "(b)")
    fig.tight_layout(w_pad=1.2); save(fig, "r_abs_s2")

# ---------------- maturity kinetics ----------------
def fig_kinetics():
    fig, ax = plt.subplots(1, 2, figsize=(6.6, 3.0), sharey=True)
    t = np.linspace(3, 29, 100)
    for k, (series, order) in enumerate((("I", S1_ORDER), ("II", S2_ORDER))):
        a = ax[k]
        lo = np.exp(0.20 * (1 - np.sqrt(28 / t))); hi = np.exp(0.38 * (1 - np.sqrt(28 / t)))
        a.fill_between(t, hi, lo, color="#e1dfd6", zorder=0)
        a.plot(t, np.exp(0.25 * (1 - np.sqrt(28 / t))), color=INK_SEC, lw=0.8, ls="--", zorder=1)
        for m in order:
            g = S[(S.series == series) & (S.mix == m)].set_index("age")["mean_reported"]
            a.plot([7, 14, 28], [g[7] / g[28], g[14] / g[28], 1.0], marker="o", color=MIXCOL[m] if m not in ("RA", "RCA0") else STEEL_EDGE, mec=LINE,
                   mfc=MIXCOL[m], lw=1.1, label=LAB[m], zorder=4)
        a.set_xticks([7, 14, 28]); a.set_xlim(3, 30); a.set_ylim(0.3, 1.1); a.set_xlabel("Curing age (d)")
        a.legend(loc="lower right", fontsize=6.8, ncol=1); panel(a, "(a)" if k == 0 else "(b)")
    ax[0].set_ylabel("$f_c(t)$ / $f_{c,28}$ (–)"); fig.tight_layout(w_pad=0.8); save(fig, "r_kinetics")

# ---------------- strength vs density, cement content ----------------
def fig_fc_density():
    Dg = density_long().groupby(["mix", "age_d"]).density.mean().reset_index().rename(columns={"age_d": "age"})
    m = S[S.series == "I"].merge(Dg, on=["mix", "age"])
    fig, ax = plt.subplots(1, 2, figsize=(6.6, 3.0))
    a = ax[0]
    for mix in S1_ORDER:
        s = m[m.mix == mix]
        a.scatter(s.density, s["mean_reported"], marker="o", s=26, facecolor=MIXCOL[mix], edgecolor=LINE, lw=0.7, zorder=4, label=LAB[mix])
    sl, ic, r, p, se = stats.linregress(np.log(m.density), np.log(m["mean_reported"]))
    xx = np.linspace(1950, 2350, 80); a.plot(xx, np.exp(ic) * xx ** sl, color=INK, lw=1.0, ls="--", zorder=3)
    a.text(0.97, 0.06, f"$f_c \\propto \\rho^{{{sl:.1f}}}$\n$R^2$ = {r**2:.2f}, n = {len(m)}", transform=a.transAxes, ha="right", va="bottom", fontsize=7.3, bbox=whitebox())
    a.set_xlabel("Density (kg/m$^3$)"); a.set_ylabel("Compressive strength (MPa)"); a.legend(loc="upper left", fontsize=6.8, ncol=1); panel(a, "(a)")
    a.yaxis.grid(True, color=GRID, lw=0.5, zorder=0)
    b = ax[1]
    inv = pd.read_csv(os.path.join(DATA, "lca_inventory_kg_per_m3.csv"), keep_default_na=False).set_index("mix")
    s28 = S[(S.series == "I") & (S.age == 28)].set_index("mix")
    xs = [inv.loc[mm, "cement"] for mm in S1_ORDER]; ys = [s28.loc[mm, "mean_reported"] for mm in S1_ORDER]
    for mm, xv, yv in zip(S1_ORDER, xs, ys):
        b.errorbar(xv, yv, yerr=s28.loc[mm, "sd"], marker="o", color=LINE, mfc=MIXCOL[mm], capsize=2.4, zorder=4, ms=5.4)
        b.annotate(LAB[mm], (xv, yv), xytext=(4, 5), textcoords="offset points", fontsize=7)
    xr = np.array([inv.loc[mm, "cement"] for mm in S1_ORDER if mm != "NA"]); yr = np.array([s28.loc[mm, "mean_reported"] for mm in S1_ORDER if mm != "NA"])
    sl2, ic2, r2, p2, se2 = stats.linregress(xr, yr); xx = np.linspace(320, 392, 20); b.plot(xx, ic2 + sl2 * xx, "--", color=ACCENT_EDGE, lw=1.0)
    b.text(0.04, 0.95, f"RA\u2192Rab15: {sl2:.2f} MPa per kg/m$^3$\n$R^2$ = {r2**2 if False else r2**2:.2f} (n = 4)", transform=b.transAxes, va="top", fontsize=7.2, bbox=whitebox())
    b.set_xlabel("Cement content (kg/m$^3$ of block)"); b.set_ylabel("28-d compressive strength (MPa)"); b.yaxis.grid(True, color=GRID, lw=0.5, zorder=0); panel(b, "(b)")
    fig.tight_layout(w_pad=1.3); save(fig, "r_fc_density")

# ---------------- market comparison and shape effect ----------------
def fig_market():
    mk = pd.read_csv(os.path.join(DATA, "market_table4-7.csv"))
    names = ["This study\n(RCA0%)", "Commercial\nproduct A", "Commercial\nproduct B"]
    fig, ax = plt.subplots(1, 2, figsize=(6.6, 3.0), gridspec_kw={"width_ratios": [1.05, 1]})
    a = ax[0]; cols = [MIXCOL["RCA0"], STEEL, "#d0cdc4"]
    for i, (_, r) in enumerate(mk.iterrows()):
        v = np.array([r.s1, r.s2, r.s3]); a.bar(i, v.mean(), 0.55, color=cols[i], edgecolor=LINE, zorder=3, yerr=v.std(ddof=1), capsize=3)
        a.plot(np.full(3, i) + np.array([-0.1, 0, 0.1]), v, "k.", ms=3.4, zorder=6)
        a.text(i, v.mean() + v.std(ddof=1) + 1.4, f"{v.mean():.1f}", ha="center", fontsize=7.5)
    a.axhline(TIS827_MPa, color=INK, ls="--", lw=0.9); a.text(1.0, 36, "35 MPa (TIS 827-2565)", ha="center", va="bottom", fontsize=6.8, bbox=whitebox())
    a.set_xticks(range(3)); a.set_xticklabels(names, fontsize=7.6); a.set_ylim(0, 72); a.set_ylabel("Compressive strength (MPa)"); a.yaxis.grid(True, color=GRID, lw=0.5, zorder=0); panel(a, "(a)")
    # shape effect
    b = ax[1]
    cube = pd.read_csv(os.path.join(DATA, "appendixA3_cube_per_specimen.csv"))
    cube["mixk"] = cube.mix.map({"RCA 0%": "RCA0", "RCA 10%": "RCA10"})
    pav = S[(S.series == "II") & (S.age == 28)].set_index("mix")
    w = 0.34
    for i, mm in enumerate(("RCA0", "RCA10")):
        cv = cube[cube.mixk == mm].strength_MPa.values
        b.bar(i - w / 2, cv.mean(), w, color="white", edgecolor=LINE, hatch="////", zorder=3, yerr=cv.std(ddof=1), capsize=2.5)
        pv = pav.loc[mm, "mean"]; b.bar(i + w / 2, pv, w, color=MIXCOL[mm], edgecolor=LINE, zorder=3, yerr=pav.loc[mm, "sd"], capsize=2.5)
        b.text(i - w / 2, cv.mean() + 3.5, f"{cv.mean():.1f}", ha="center", fontsize=7.5); b.text(i + w / 2, pv + 4.2, f"{pv:.1f}", ha="center", fontsize=7.5)
        b.text(i, 8, f"\u00d7{pv/cv.mean():.2f}", ha="center", fontsize=8, fontweight="bold", bbox=whitebox(), zorder=8)
    b.set_xticks([0, 1]); b.set_xticklabels(["RCA0%", "RCA10%"]); b.set_ylim(0, 80); b.set_ylabel("28-d compressive strength (MPa)")
    h = [Patch(facecolor="white", edgecolor=LINE, hatch="////", label="Cube (specimen)"), Patch(facecolor=MIXCOL["RCA10"], edgecolor=LINE, label="Zig-zag block")]
    b.legend(handles=h, loc="upper left", fontsize=7); b.yaxis.grid(True, color=GRID, lw=0.5, zorder=0); panel(b, "(b)")
    fig.tight_layout(w_pad=1.3); save(fig, "r_market_shape")

if __name__ == "__main__":
    fig_abs(); fig_kinetics(); fig_fc_density(); fig_market()
