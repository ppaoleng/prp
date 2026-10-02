"""All numbers quoted in the report text are computed here from data/*.csv (no hand-typed results)."""
import os, sys, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from prp_data import *
import lca_model, placeholder_bpn

def load():
    N = {}
    S = strength_summary(); L = strength_long()
    for age in (7, 14, 28):
        for _, r in S[S.age == age].iterrows():
            N[f"fc{age}_{r.mix}"] = r.mean_reported; N[f"sd{age}_{r.mix}"] = r.sd; N[f"cv{age}_{r.mix}"] = r.cv_pct; N[f"mean{age}_{r.mix}"] = r["mean"]
    dens = pd.read_csv(os.path.join(DATA, "density_table4-1.csv"))
    mp = dict(zip(dens.mix, ["NA", "RA", "Rab5", "Rab10", "Rab15"]))
    for _, r in dens.iterrows():
        m = mp[r.mix]; N[f"rho_all_{m}"] = r.overall_reported; N[f"rho7_{m}"] = r.d7; N[f"rho14_{m}"] = r.d14; N[f"rho28_{m}"] = r.d28
    A = absorption_long()
    for (s, m, a), g in A.groupby(["series", "mix", "age"]): N[f"ab{a}_{m}"] = g.ab.mean()
    N["ab_rab5_all"] = A[(A.mix == "Rab5")].ab.mean()
    an = pd.read_csv(os.path.join(DATA, "stats_anova.csv"))
    for _, r in an.iterrows(): N[f"F_{r.series}_{int(r.age)}"] = r.F; N[f"p_{r.series}_{int(r.age)}"] = r.p; N[f"eta_{r.series}_{int(r.age)}"] = r.eta2; N[f"df2_{r.series}_{int(r.age)}"] = int(r.df2)
    tk = pd.read_csv(os.path.join(DATA, "stats_tukey.csv"), keep_default_na=False)
    N["tukey"] = tk
    fit = pd.read_csv(os.path.join(DATA, "stats_maturity_fits.csv"), keep_default_na=False)
    for _, r in fit.iterrows():
        N[f"s_{r.mix}"] = r.s_fit; N[f"s7_{r.mix}"] = r.s_from_7d; N[f"s14_{r.mix}"] = r.s_from_14d
    reg = pd.read_csv(os.path.join(DATA, "stats_regressions.csv"))
    N["reg"] = reg
    N["b_rho_all"] = reg.iloc[0].slope; N["r2_rho_all"] = reg.iloc[0].r2; N["b_rho_28"] = reg.iloc[1].slope; N["r2_rho_28"] = reg.iloc[1].r2
    N["b_cem"] = reg.iloc[2].slope; N["r2_cem"] = reg.iloc[2].r2; N["b_rca"] = reg.iloc[3].slope; N["r2_rca"] = reg.iloc[3].r2
    # market + shape
    mk = pd.read_csv(os.path.join(DATA, "market_table4-7.csv"))
    N["mk_this"] = mk.iloc[0][["s1", "s2", "s3"]].mean(); N["mk_A"] = mk.iloc[1][["s1", "s2", "s3"]].mean(); N["mk_B"] = mk.iloc[2][["s1", "s2", "s3"]].mean()
    cube = pd.read_csv(os.path.join(DATA, "appendixA3_cube_per_specimen.csv"))
    N["cube0"] = cube[cube.mix == "RCA 0%"].strength_MPa.mean(); N["cube10"] = cube[cube.mix == "RCA 10%"].strength_MPa.mean()
    N["shape0"] = N["fc28_RCA0"] / N["cube0"]; N["shape10"] = N["fc28_RCA10"] / N["cube10"]
    # LCA
    inv, res = lca_model.run()
    N["inv"] = inv; N["lca"] = res
    for m in res.index:
        N[f"gwpA_{m}"] = res.loc[m, "gwp_A"]; N[f"gwpB_{m}"] = res.loc[m, "gwp_B"]; N[f"ciA_{m}"] = res.loc[m, "gwpA_per_MPa"]; N[f"ciB_{m}"] = res.loc[m, "gwpB_per_MPa"]
        N[f"cem_{m}"] = inv.loc[m, "cement"]; N[f"bi_{m}"] = res.loc[m, "cement_per_MPa"]
    tested = ["NA", "RA", "Rab5", "Rab10", "Rab15", "RCA0", "RCA5", "RCA10", "RCA15"]
    share = (res.loc[tested, "gwpA_cement"] / res.loc[tested, "gwp_A"] * 100)
    N["share_min"] = share.min(); N["share_max"] = share.max()
    N["share_RA"] = share["RA"]
    mc = pd.read_csv(os.path.join(DATA, "lca_montecarlo_summary.csv"), keep_default_na=False); N["mc"] = mc
    pr = pd.read_csv(os.path.join(DATA, "lca_prob_lower_than_control.csv"), keep_default_na=False); N["pr"] = pr
    tor = pd.read_csv(os.path.join(DATA, "lca_tornado_Rab5.csv")); N["tor"] = tor
    cost = pd.read_csv(os.path.join(DATA, "cost_screening_relative.csv")) if os.path.exists(os.path.join(DATA, "cost_screening_relative.csv")) else None
    N["cost"] = cost
    # BPN placeholders
    B = placeholder_bpn.build(); N["bpn"] = B
    for _, r in B.iterrows():
        N[f"bd{r.age}_{r.mix}"] = r.bpn_dry; N[f"bw{r.age}_{r.mix}"] = r.bpn_wet
    N["wetdrop_mean"] = B.wet_drop.mean(); N["wetdrop_min"] = B.wet_drop.min(); N["wetdrop_max"] = B.wet_drop.max()
    N["bpn_wet_min"] = B.bpn_wet.min(); N["bpn_wet_max"] = B.bpn_wet.max(); N["bpn_dry_min"] = B.bpn_dry.min(); N["bpn_dry_max"] = B.bpn_dry.max()
    return N

if __name__ == "__main__":
    N = load()
    for k in ("fc28_RA", "fc28_Rab5", "gwpA_RA", "share_min", "share_max", "ciA_RA", "ciA_Rab15", "shape0", "shape10", "wetdrop_mean", "b_rho_28", "F_I_28", "p_I_28"):
        print(k, N[k])
