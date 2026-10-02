import os, sys, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from fig_style import *
from prp_data import *
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
apply_style()
S = strength_summary()
B = pd.read_csv(os.path.join(DATA, "bpn_PLACEHOLDER.csv"), keep_default_na=False)
ALL = S1_ORDER + S2_ORDER
THR_A, THR_B = 45, 60     # levels quoted in the 2568 reference report (EN 1338) and in draft Table 2-1 -- BOTH TO BE VERIFIED

# ---------- BPN at 28 d: dry vs wet ----------
def fig_bpn_bars():
    fig, ax = plt.subplots(figsize=(6.6, 3.2)); w = 0.36
    xs = np.array([0, 1, 2, 3, 4, 5.8, 6.8, 7.8, 8.8])
    for i, m in enumerate(ALL):
        r = B[(B.mix == m) & (B.age == 28)].iloc[0]
        ax.bar(xs[i] - w / 2, r.bpn_dry, w, color=MIXCOL[m], edgecolor=LINE, yerr=r.sd_dry, capsize=2, error_kw=dict(lw=0.8), zorder=3)
        ax.bar(xs[i] + w / 2, r.bpn_wet, w, color=MIXCOL[m], edgecolor=LINE, hatch="////", yerr=r.sd_wet, capsize=2, error_kw=dict(lw=0.8), zorder=3)
        ax.text(xs[i] - w / 2, r.bpn_dry + r.sd_dry + 0.8, f"{r.bpn_dry:.1f}", ha="center", fontsize=6.4, rotation=90, va="bottom", zorder=6)
        ax.text(xs[i] + w / 2, r.bpn_wet + r.sd_wet + 0.8, f"{r.bpn_wet:.1f}", ha="center", fontsize=6.4, rotation=90, va="bottom", zorder=6)
    ax.axhline(THR_A, color=INK, ls="--", lw=0.9); ax.axhline(THR_B, color=WARM_EDGE, ls="-.", lw=0.9)
    ax.set_xticks(xs); ax.set_xticklabels([LAB[m] for m in ALL], rotation=0, fontsize=7.4); ax.set_ylim(30, 94); ax.set_xlim(-0.7, 9.5)
    ax.set_ylabel("British Pendulum Number, 28 d (BPN)"); ax.yaxis.grid(True, color=GRID, lw=0.5, zorder=0)
    ax.axvline(4.9, color=GRID, lw=1.0); ax.text(2, 91.5, "Series I", ha="center", fontsize=7.6, fontweight="bold"); ax.text(7.3, 91.5, "Series II", ha="center", fontsize=7.6, fontweight="bold")
    h = [Patch(facecolor="white", edgecolor=LINE, label="Dry"), Patch(facecolor="white", edgecolor=LINE, hatch="////", label="Wet"),
         Line2D([], [], color=INK, ls="--", lw=0.9, label="45 BPN [to be verified]"), Line2D([], [], color=WARM_EDGE, ls="-.", lw=0.9, label="60 BPN [to be verified]")]
    ax.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=4, fontsize=7.0, frameon=False); ph_tag(ax, loc="upper left")
    fig.tight_layout(); save(fig, "r_bpn_bars")

def fig_bpn_age():
    fig, ax = plt.subplots(1, 2, figsize=(6.6, 3.0), sharey=True)
    for k, (series, order) in enumerate((("I", S1_ORDER), ("II", S2_ORDER))):
        a = ax[k]
        for m in order:
            g = B[B.mix == m].sort_values("age")
            c = MIXCOL[m]
            a.errorbar(g.age, g.bpn_dry, yerr=g.sd_dry, color=c if m not in ("RA", "RCA0") else STEEL_EDGE, mfc=c, mec=LINE, marker="o", capsize=1.8, lw=1.1, label=LAB[m], zorder=4)
            a.plot(g.age, g.bpn_wet, color=c if m not in ("RA", "RCA0") else STEEL_EDGE, mfc="white", mec=LINE, marker="s", ls="--", lw=0.9, zorder=3)
        a.axhline(THR_A, color=INK, ls=":", lw=0.9); a.set_xticks([7, 14, 28]); a.set_xlim(4, 31); a.set_ylim(40, 83)
        a.set_xlabel("Curing age (d)"); a.legend(loc="upper left", fontsize=6.6, ncol=3, columnspacing=0.8); panel(a, "(a)" if k == 0 else "(b)"); a.yaxis.grid(True, color=GRID, lw=0.5)
        ph_tag(a, loc="lower left")
    ax[0].set_ylabel("BPN"); 
    h = [Line2D([], [], color=INK_SEC, marker="o", mfc=INK_SEC, label="Dry"), Line2D([], [], color=INK_SEC, marker="s", mfc="white", ls="--", label="Wet")]
    ax[1].legend(handles=h + ax[1].get_legend_handles_labels()[0][:0], loc="upper right", fontsize=6.6)
    fig.tight_layout(w_pad=0.8); save(fig, "r_bpn_age")

def fig_bpn_corr():
    fig, ax = plt.subplots(1, 3, figsize=(6.8, 2.7))
    g28 = B[B.age == 28].set_index("mix").reindex(ALL)
    s28 = S[S.age == 28].set_index("mix")["mean_reported"].reindex(ALL)
    # (a) wet vs dry
    a = ax[0]
    for m in ALL:
        a.plot(g28.loc[m, "bpn_dry"], g28.loc[m, "bpn_wet"], "o", mfc=MIXCOL[m], mec=LINE, ms=5.2)
    xx = np.array([50, 75]); [a.plot(xx, xx - d, color=GRID, lw=0.8, zorder=0) for d in (8, 10, 12)]
    a.text(74.5, 74.5 - 8.3, "−8", fontsize=6.4, color=INK_SEC, ha="right"); a.text(74.5, 74.5 - 10.3, "−10", fontsize=6.4, color=INK_SEC, ha="right"); a.text(74.5, 74.5 - 12.3, "−12", fontsize=6.4, color=INK_SEC, ha="right")
    a.set_xlim(55, 75); a.set_ylim(45, 70); a.set_xlabel("Dry BPN"); a.set_ylabel("Wet BPN"); panel(a, "(a)")
    # (b) wet BPN vs fc28
    b = ax[1]
    for m in ALL: b.plot(s28[m], g28.loc[m, "bpn_wet"], "o", mfc=MIXCOL[m], mec=LINE, ms=5.2)
    sl, ic, r, p, se = stats.linregress(s28.values, g28.bpn_wet.values); xx = np.linspace(35, 95, 20); b.plot(xx, ic + sl * xx, "--", color=INK, lw=0.9)
    b.text(0.96, 0.05, f"$R^2$ = {r**2:.2f}\n(n = 9)", transform=b.transAxes, fontsize=7, va="bottom", ha="right", bbox=whitebox())
    b.set_xlabel("$f_{c,28}$ (MPa)"); b.set_ylabel("Wet BPN, 28 d"); panel(b, "(b)")
    # (c) wet BPN vs density (series I)
    c = ax[2]
    dens = density_long().query("age_d==28").groupby("mix").density.mean().reindex(S1_ORDER)
    for m in S1_ORDER: c.plot(dens[m], g28.loc[m, "bpn_wet"], "o", mfc=MIXCOL[m], mec=LINE, ms=5.2)
    sl2, ic2, r2, p2, se2 = stats.linregress(dens.values, g28.loc[S1_ORDER, "bpn_wet"].values); xx = np.linspace(1990, 2300, 20); c.plot(xx, ic2 + sl2 * xx, "--", color=INK, lw=0.9)
    c.text(0.96, 0.05, f"$R^2$ = {r2**2:.2f}\n(n = 5)", transform=c.transAxes, fontsize=7, va="bottom", ha="right", bbox=whitebox())
    c.set_xlabel("Density, 28 d (kg/m$^3$)"); c.set_ylabel("Wet BPN, 28 d"); panel(c, "(c)")
    for aa in ax: ph_tag(aa, loc="upper left", fs=6.2)
    h = [Line2D([], [], marker="o", ls="", mfc=MIXCOL[m], mec=LINE, label=LAB[m]) for m in ALL]
    fig.legend(handles=h, loc="lower center", ncol=9, fontsize=6.4, handletextpad=0.1, columnspacing=0.8, frameon=False, bbox_to_anchor=(0.5, -0.07))
    fig.tight_layout(w_pad=1.2); save(fig, "r_bpn_corr")

def fig_bpn_risk():
    fig, ax = plt.subplots(figsize=(6.6, 2.9))
    ax.axvspan(0, 24.5, color="#e9d9cc", zorder=0); ax.axvspan(24.5, 35.5, color="#eee7d3", zorder=0); ax.axvspan(35.5, 100, color="#dde6e0", zorder=0)
    ax.text(12, len(ALL) + 0.55, "high", ha="center", fontsize=7.2); ax.text(30, len(ALL) + 0.55, "moderate", ha="center", fontsize=7.2); ax.text(68, len(ALL) + 0.55, "low slip potential (wet PTV ≥ 36, UKSRG)", ha="center", fontsize=7.2)
    g = B[B.age == 28].set_index("mix").reindex(ALL)
    for i, m in enumerate(ALL[::-1]):
        r = g.loc[m]
        ax.errorbar(r.bpn_wet, i, xerr=r.sd_wet, fmt="s", mfc="white", mec=LINE, color=LINE, capsize=2, ms=5, zorder=4)
        ax.errorbar(r.bpn_dry, i, xerr=r.sd_dry, fmt="o", mfc=MIXCOL[m], mec=LINE, color=LINE, capsize=2, ms=5, zorder=4)
    ax.axvline(THR_A, color=INK, ls="--", lw=0.9); ax.axvline(THR_B, color=WARM_EDGE, ls="-.", lw=0.9)
    ax.text(THR_A, -0.9, "45 [to be verified]", ha="center", va="top", fontsize=6.4); ax.text(THR_B, -0.9, "60 [to be verified]", ha="center", va="top", fontsize=6.4, color=WARM_EDGE)
    ax.set_yticks(range(len(ALL))); ax.set_yticklabels([LAB[m] for m in ALL[::-1]], fontsize=7.4); ax.set_xlim(0, 85); ax.set_ylim(-1.4, len(ALL) + 1.0)
    ax.set_xlabel("Pendulum value at 28 d (BPN / PTV scale)")
    h = [Line2D([], [], marker="o", ls="", mfc=INK_SEC, mec=LINE, label="Dry"), Line2D([], [], marker="s", ls="", mfc="white", mec=LINE, label="Wet")]
    ax.legend(handles=h, loc="lower right", fontsize=7); ph_tag(ax, loc="upper left" if False else "lower left")
    fig.tight_layout(); save(fig, "r_bpn_risk")

# ---------------- LCA ----------------
RES = pd.read_csv(os.path.join(DATA, "lca_results_screening.csv"), keep_default_na=False).set_index("mix")
for c in RES.columns:
    RES[c] = pd.to_numeric(RES[c], errors="coerce")
COMP = {"cement": "#8a6a45", "sand": "#d8cdb4", "stone": "#a9a9a2", "rca": "#6f7e8c", "biochar": "#2b2b28"}
TEST = ["NA", "RA", "Rab5", "Rab10", "Rab15", "RCA0", "RCA5", "RCA10", "RCA15"]

def fig_lca_contrib():
    fig, ax = plt.subplots(1, 2, figsize=(6.7, 3.1), gridspec_kw={"width_ratios": [1.15, 1]})
    a = ax[0]; xs = np.arange(len(TEST)); bottom = np.zeros(len(TEST))
    for c in ("cement", "stone", "sand", "rca", "biochar"):
        v = RES.loc[TEST, f"gwpA_{c}"].values
        a.bar(xs, v, 0.62, bottom=bottom, color=COMP[c], edgecolor=LINE, lw=0.6, label=c.capitalize() if c != "rca" else "RCA (crushing)", hatch={"sand": "..", "stone": "xx", "rca": "//", "biochar": "", "cement": ""}[c], zorder=3)
        bottom += v
    for xi, t in zip(xs, bottom): a.text(xi, t + 4, f"{t:.0f}", ha="center", fontsize=7)
    a.set_xticks(xs); a.set_xticklabels([LAB[m] for m in TEST], rotation=45, ha="right", fontsize=7.2); a.set_ylim(0, 420); a.set_ylabel("GWP, cradle-to-gate (kg CO$_2$e per m$^3$)")
    a.axvline(4.5, color=GRID, lw=1.0); a.legend(loc="upper left", fontsize=6.6, ncol=2); panel(a, "(a)"); a.yaxis.grid(True, color=GRID, lw=0.5, zorder=0)
    b = ax[1]; bottom = np.zeros(len(TEST))
    for c in ("stone", "sand", "rca", "biochar"):
        v = RES.loc[TEST, f"gwpA_{c}"].values
        b.bar(xs, v, 0.62, bottom=bottom, color=COMP[c], edgecolor=LINE, lw=0.6, hatch={"sand": "..", "stone": "xx", "rca": "//", "biochar": ""}[c], zorder=3); bottom += v
    b.set_xticks(xs); b.set_xticklabels([LAB[m] for m in TEST], rotation=45, ha="right", fontsize=7.2); b.set_ylabel("Non-cement GWP (kg CO$_2$e per m$^3$)")
    share = (RES.loc[TEST, "gwpA_cement"] / RES.loc[TEST, "gwp_A"] * 100)
    b.text(0.03, 0.96, f"Cement share of GWP:\n{share.min():.1f}–{share.max():.1f} %", transform=b.transAxes, va="top", fontsize=7.2, bbox=whitebox()); panel(b, "(b)")
    b.yaxis.grid(True, color=GRID, lw=0.5, zorder=0); fig.tight_layout(w_pad=1.2); save(fig, "r_lca_contrib")

def fig_lca_eco():
    fig, ax = plt.subplots(1, 2, figsize=(6.7, 3.1), gridspec_kw={"width_ratios": [1.15, 1]})
    a = ax[0]
    g = RES.loc[TEST, "gwp_A"]; x0, x1 = np.floor(g.min() - 6), np.ceil(g.max() + 8)
    xx = np.linspace(x0, x1, 50)
    for ci, ls in ((3, ":"), (4, ":"), (5, ":"), (6, "--"), (8, ":"), (10, ":")):
        a.plot(xx, xx / ci, color=GRID if ci != 6 else INK_SEC, lw=0.8, ls=ls, zorder=1)
        yy = (x1 - 1) / ci
        if 32 < yy < 98: a.text(x1 - 1, yy, f"ci={ci}", fontsize=6.0, color=INK_SEC, ha="right", va="bottom", bbox=whitebox(alpha=0.7))
    offs = {"NA": (5, 3), "RA": (-5, 6), "Rab5": (5, -9), "Rab10": (5, -9), "Rab15": (-6, -11), "RCA0": (5, -9), "RCA15": (5, 5)}
    for m in TEST:
        r = RES.loc[m]; a.plot(r.gwp_A, r.fc28, "o", mfc=MIXCOL[m], mec=LINE, ms=6.4, zorder=5)
        if m in offs: a.annotate(LAB[m] if m != "RCA15" else "RCA5\u201315%", (r.gwp_A, r.fc28), xytext=offs[m], textcoords="offset points", fontsize=6.8, zorder=6, ha="left" if offs[m][0] > 0 else "right")
    a.set_xlim(x0, x1); a.set_ylim(30, 100); a.set_xlabel("GWP, scenario A (kg CO$_2$e per m$^3$)"); a.set_ylabel("28-d compressive strength (MPa)"); panel(a, "(a)")
    a.text(0.02, 0.04, "dotted: ci = GWP / $f_c$ (kg CO$_2$e m$^{-3}$ MPa$^{-1}$)", transform=a.transAxes, ha="left", fontsize=6.2, color=INK_SEC, bbox=whitebox())
    b = ax[1]; xs = np.arange(len(TEST)); w = 0.38
    b.bar(xs - w / 2, RES.loc[TEST, "gwpA_per_MPa"], w, color=[MIXCOL[m] for m in TEST], edgecolor=LINE, zorder=3)
    b.bar(xs + w / 2, RES.loc[TEST, "gwpB_per_MPa"].clip(lower=0), w, color="white", edgecolor=LINE, hatch="////", zorder=3)
    b.set_xticks(xs); b.set_xticklabels([LAB[m] for m in TEST], rotation=45, ha="right", fontsize=7.2); b.set_ylabel("Carbon intensity, ci (kg CO$_2$e m$^{-3}$ MPa$^{-1}$)")
    h = [Patch(facecolor=STEEL, edgecolor=LINE, label="Scenario A (no credit)"), Patch(facecolor="white", edgecolor=LINE, hatch="////", label="Scenario B (storage credit)")]
    b.legend(handles=h, loc="upper left", fontsize=6.5); panel(b, "(b)"); b.set_ylim(0, 11.5); b.yaxis.grid(True, color=GRID, lw=0.5, zorder=0)
    fig.tight_layout(w_pad=1.2); save(fig, "r_lca_eco")

def fig_lca_uncert():
    mc = pd.read_csv(os.path.join(DATA, "lca_montecarlo_summary.csv"), keep_default_na=False)
    pr = pd.read_csv(os.path.join(DATA, "lca_prob_lower_than_control.csv"), keep_default_na=False)
    tor = pd.read_csv(os.path.join(DATA, "lca_tornado_Rab5.csv"))
    fig, ax = plt.subplots(1, 2, figsize=(6.7, 3.0), gridspec_kw={"width_ratios": [1.2, 1]})
    a = ax[0]
    for i, m in enumerate(TEST[::-1]):
        r = mc[(mc.scenario == "A") & (mc["mix"] == m)].iloc[0]
        a.errorbar(r["mean"], i, xerr=[[r["mean"] - r.p2_5], [r.p97_5 - r["mean"]]], fmt="o", mfc=MIXCOL[m], mec=LINE, color=LINE, capsize=2.2, ms=5, zorder=4)
    a.set_yticks(range(len(TEST))); a.set_yticklabels([LAB[m] for m in TEST[::-1]], fontsize=7.4); a.set_xlabel("GWP, scenario A, mean and 95 % interval (kg CO$_2$e per m$^3$)\nP = probability of being lower than the series control"); a.set_ylim(-0.7, len(TEST) - 0.3)
    a.xaxis.grid(True, color=GRID, lw=0.5, zorder=0); panel(a, "(a)")
    # annotate P(lower than control)
    for i, m in enumerate(TEST[::-1]):
        if m in ("NA", "RA", "RCA0"): continue
        p = pr[(pr.scenario == "A") & (pr["mix"] == m)].p_lower.iloc[0]
        a.text(1.015, i, f"P = {p:.2f}", transform=a.get_yaxis_transform(), ha="left", va="center", fontsize=6.4, color=INK_SEC, clip_on=False)
    b = ax[1]; tor = tor.assign(span=(tor.gwp_high - tor.gwp_low).abs()).sort_values("span")
    base = tor.base.iloc[0]
    for i, r in enumerate(tor.itertuples()):
        lo, hi = sorted([r.gwp_low, r.gwp_high]); b.barh(i, hi - lo, left=lo, height=0.5, color=COMP[r.parameter], edgecolor=LINE, zorder=3)
    b.axvline(base, color=INK, lw=0.9); b.set_xlim(min(tor.gwp_low.min(), tor.gwp_high.min()) - 6, max(tor.gwp_low.max(), tor.gwp_high.max()) + 6); b.set_yticks(range(len(tor))); b.set_yticklabels([p.capitalize() if p != "rca" else "RCA" for p in tor.parameter], fontsize=7.4)
    b.set_xlabel("GWP of Rab5% (kg CO$_2$e per m$^3$)"); panel(b, "(b)"); b.xaxis.grid(True, color=GRID, lw=0.5, zorder=0)
    fig.tight_layout(w_pad=1.2); save(fig, "r_lca_uncert")

def fig_lca_dose():
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    dose = [0, 5, 10, 15, 20, 25]; names = ["RA", "Rab5", "Rab10", "Rab15", "Rab20", "Rab25"]
    A_ = [RES.loc[m, "gwp_A"] for m in names]; B_ = [RES.loc[m, "gwp_B"] for m in names]
    ax.plot(dose[:4], A_[:4], "o-", color=ACCENT_EDGE, mfc=ACCENT, label="Scenario A (no credit)"); ax.plot(dose[3:], A_[3:], "o--", color=ACCENT_EDGE, mfc="white")
    ax.plot(dose[:4], B_[:4], "s-", color=WARM_EDGE, mfc=WARM, label="Scenario B (storage credit)"); ax.plot(dose[3:], B_[3:], "s--", color=WARM_EDGE, mfc="white")
    ax.axhline(0, color=INK, lw=0.8); ax.axvspan(17.5, 27, color="#ece9df", zorder=0)
    ax.text(22.3, 330, "mixes designed,\nnot yet tested", ha="center", fontsize=6.8, color=INK_SEC)
    ax.set_xlabel("Cement reduction (nominal %)"); ax.set_ylabel("GWP (kg CO$_2$e per m$^3$)"); ax.set_xticks(dose); ax.legend(loc="lower left", fontsize=7); ax.yaxis.grid(True, color=GRID, lw=0.5)
    fig.tight_layout(); save(fig, "r_lca_dose")

def fig_standards():
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    s28 = S[S.age == 28].set_index("mix").reindex(ALL)
    ys = np.arange(len(ALL))[::-1]
    for y, m in zip(ys, ALL):
        r = s28.loc[m]; ax.barh(y, r["mean"], 0.58, color=MIXCOL[m], edgecolor=LINE, xerr=r.sd, capsize=2, zorder=3, error_kw=dict(lw=0.8))
        ax.text(r["mean"] + r.sd + 1, y, f"{r['mean']:.1f}", va="center", fontsize=7)
    crit = [(20, "JIEPA", ":"), (30, "IS 15658", ":"), (35, "TIS 827-2565", "--"), (50, "TIS 2035-2565", "-."), (55, "ASTM C936", ":")]
    for x, t, ls in crit:
        ax.axvline(x, color=INK_SEC, ls=ls, lw=0.9, zorder=2); ax.text(x, len(ALL) - 0.3, f"{t}: {x}", rotation=90, ha="center", va="bottom", fontsize=6.2, color=INK_SEC)
    ax.set_yticks(ys); ax.set_yticklabels([LAB[m] for m in ALL], fontsize=7.4); ax.set_xlim(0, 112); ax.set_ylim(-0.6, len(ALL) + 1.9)
    ax.set_xlabel("28-d compressive strength (MPa)"); ax.xaxis.grid(True, color=GRID, lw=0.4, zorder=0); fig.tight_layout(); save(fig, "r_standards")

if __name__ == "__main__":
    fig_bpn_bars(); fig_bpn_age(); fig_bpn_corr(); fig_bpn_risk()
    fig_lca_contrib(); fig_lca_eco(); fig_lca_uncert(); fig_lca_dose(); fig_standards()
