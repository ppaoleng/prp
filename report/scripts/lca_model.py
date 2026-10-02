"""Screening (cradle-to-gate, A1-A3-type) carbon-footprint model for the PRP paving-block mixes.

What is DATA-DERIVED (firm):   the inventory (kg of each constituent per m3 of block) is computed from the
                               batch masses in Table 3-1 divided by the block volume 0.00156 m3 (Appendix A).
What is ASSUMED (placeholder): every emission factor in FACTORS below.  They are typical screening values
                               that MUST be replaced by Thai LCI / TGO / ecoinvent values before publication.
Not modelled: transport, mixing/forming electricity, curing, use-phase, end-of-life, water (all excluded,
              as in the cradle-to-gate scope used by Pizon et al. 2026 for comparability).
"""
import os, sys, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from prp_data import *

# kg CO2e per kg of material  (mode, low, high)  -- ASSUMED, to be replaced
FACTORS = {
    "cement":  (0.76, 0.63, 0.90),   # mode: Thai OPC 0.76 t/t (Khongprom & Suwanmanee 2017); low 0.63 (Wang et al. 2026); high ASSUMED
    "sand":    (0.004, 0.002, 0.008),
    "stone":   (0.005, 0.003, 0.009),
    "rca":     (0.006, 0.003, 0.012),   # crushing only (cut-off: waste enters burden-free)
    "biochar": (0.25, 0.05, 0.60),      # pyrolysis process burden, biogenic carbon NOT credited
}
C_FRAC = (0.65, 0.75, 0.85)    # carbon mass fraction of bamboo biochar  (low, mode, high)  ASSUMED
PERMANENCE = (0.50, 0.80, 0.95)  # fraction of carbon remaining stored over 100 y  ASSUMED
CO2_PER_C = 44.0 / 12.0

def inventory():
    """kg per m3 of block for every mix (batch grams / 1000 / block volume)."""
    m = mix_design().copy()
    m = m.set_index("code")
    inv = {}
    # all-natural reference NA: sand+RCA = 1800 g of natural sand (inferred from 1:3:1.5; not printed in Table 3-1)
    inv["NA"] = dict(cement=600, sand=1800, stone=900, rca=0, biochar=0)
    inv["RA"] = dict(cement=600, sand=900, stone=900, rca=900, biochar=0)
    for k in ("Rab5", "Rab10", "Rab15", "Rab20", "Rab25"):
        r = m.loc[k]; inv[k] = dict(cement=r.cement_g, sand=r.sand_g, stone=r.stone_g, rca=r.rca_g, biochar=r.biochar_g)
    inv["RCA0"] = dict(cement=600, sand=900, stone=1800, rca=0, biochar=48)
    for k in ("RCA5", "RCA10", "RCA15"):
        r = m.loc[k]; inv[k] = dict(cement=r.cement_g, sand=r.sand_g, stone=r.stone_g, rca=r.rca_g, biochar=r.biochar_g)
    df = pd.DataFrame(inv).T[["cement", "sand", "stone", "rca", "biochar"]]
    df = df / 1000.0 / BLOCK_VOLUME_M3          # kg per m3
    df.index.name = "mix"
    return df

def gwp_point(inv, scen="A"):
    f = {k: v[0] for k, v in FACTORS.items()}
    contrib = pd.DataFrame({k: inv[k] * f[k] for k in f})
    if scen == "B":   # add biogenic-carbon storage credit
        credit = inv["biochar"] * C_FRAC[1] * PERMANENCE[1] * CO2_PER_C
        contrib["biochar"] = contrib["biochar"] - credit
    contrib["total"] = contrib.sum(axis=1)
    return contrib

def monte_carlo(inv, n=20000, seed=7):
    rng = np.random.default_rng(seed)
    d = {k: rng.triangular(v[1], v[0], v[2], n) for k, v in FACTORS.items()}
    cfr = rng.uniform(C_FRAC[0], C_FRAC[2], n); per = rng.uniform(PERMANENCE[0], PERMANENCE[2], n)
    out = {}
    for scen in ("A", "B"):
        res = {}
        for mix in inv.index:
            g = sum(inv.loc[mix, k] * d[k] for k in d)
            if scen == "B":
                g = g - inv.loc[mix, "biochar"] * cfr * per * CO2_PER_C
            res[mix] = g
        out[scen] = pd.DataFrame(res)
    return out

def tornado(inv, mix="Rab5"):
    base = gwp_point(inv, "A").loc[mix, "total"]
    rows = []
    for k, (mode, lo, hi) in FACTORS.items():
        def total(val):
            f = {kk: vv[0] for kk, vv in FACTORS.items()}; f[k] = val
            return sum(inv.loc[mix, kk] * f[kk] for kk in f)
        rows.append(dict(parameter=k, low_value=lo, high_value=hi, gwp_low=total(lo), gwp_high=total(hi), base=base))
    return pd.DataFrame(rows)

def run():
    inv = inventory()
    FAC = pd.DataFrame(FACTORS, index=["mode", "low", "high"]).T
    FAC["status"] = "ASSUMED - replace with Thai LCI/TGO/ecoinvent value"
    FAC.loc["biogenic C fraction"] = list(C_FRAC[1:2]) + [C_FRAC[0], C_FRAC[2], "ASSUMED"]
    FAC.loc["permanence (100 y)"] = list(PERMANENCE[1:2]) + [PERMANENCE[0], PERMANENCE[2], "ASSUMED"]
    FAC.to_csv(os.path.join(DATA, "lca_factors_ASSUMED.csv"))
    inv.round(2).to_csv(os.path.join(DATA, "lca_inventory_kg_per_m3.csv"))
    A = gwp_point(inv, "A"); B = gwp_point(inv, "B")
    S = strength_summary().query("age==28").set_index("mix")["mean_reported"]
    res = inv.copy()
    res["binder_cement"] = inv["cement"]
    res["virgin_agg"] = inv["sand"] + inv["stone"]
    res["secondary"] = inv["rca"] + inv["biochar"]
    res["total_mass"] = inv[["cement", "sand", "stone", "rca", "biochar"]].sum(axis=1)
    res["recycled_share_pct"] = res["secondary"] / res["total_mass"] * 100
    res["gwp_A"] = A["total"]; res["gwp_B"] = B["total"]
    for c in ("cement", "sand", "stone", "rca", "biochar"):
        res[f"gwpA_{c}"] = A[c]
    res["fc28"] = S.reindex(res.index)
    res["gwpA_per_MPa"] = res["gwp_A"] / res["fc28"]
    res["gwpB_per_MPa"] = res["gwp_B"] / res["fc28"]
    res["cement_per_MPa"] = res["cement"] / res["fc28"]
    ctrl = {"I": "RA", "II": "RCA0"}
    res["gwp_A_vs_ctrl_pct"] = np.nan
    for mix in res.index:
        s = "I" if mix in ("NA", "RA", "Rab5", "Rab10", "Rab15", "Rab20", "Rab25") else "II"
        res.loc[mix, "gwp_A_vs_ctrl_pct"] = (res.loc[mix, "gwp_A"] / res.loc[ctrl[s], "gwp_A"] - 1) * 100
    res.round(3).to_csv(os.path.join(DATA, "lca_results_screening.csv"))
    mc = monte_carlo(inv)
    summ = []
    for scen in ("A", "B"):
        for mix in inv.index:
            x = mc[scen][mix]
            summ.append(dict(scenario=scen, mix=mix, mean=x.mean(), p2_5=np.percentile(x, 2.5), p97_5=np.percentile(x, 97.5)))
    pd.DataFrame(summ).round(2).to_csv(os.path.join(DATA, "lca_montecarlo_summary.csv"), index=False)
    # paired probability that a mix is lower than its series control
    pr = []
    for scen in ("A", "B"):
        for mix in inv.index:
            s = "I" if mix in ("NA", "RA", "Rab5", "Rab10", "Rab15", "Rab20", "Rab25") else "II"
            pr.append(dict(scenario=scen, mix=mix, control=ctrl[s], p_lower=float((mc[scen][mix] < mc[scen][ctrl[s]]).mean())))
    pd.DataFrame(pr).round(3).to_csv(os.path.join(DATA, "lca_prob_lower_than_control.csv"), index=False)
    tornado(inv, "Rab5").round(4).to_csv(os.path.join(DATA, "lca_tornado_Rab5.csv"), index=False)
    return inv, res

if __name__ == "__main__":
    inv, res = run()
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
    print(inv.round(1)); print(res[["total_mass","recycled_share_pct","gwp_A","gwp_B","fc28","gwpA_per_MPa","cement_per_MPa","gwp_A_vs_ctrl_pct"]].round(2))
    print(pd.read_csv(os.path.join(DATA,"lca_prob_lower_than_control.csv")).pivot(index="mix",columns="scenario",values="p_lower"))
