import sys, os, json, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from prp_data import *
from scipy import stats
pd.set_option("display.width", 220); pd.set_option("display.max_columns", 30)
S = strength_summary()
print("=== strength summary (placeholders excluded) ===")
print(S.round(2).to_string())
# 1. Reported mean vs recomputed mean
S["d_mean"] = S["mean"] - S["mean_reported"]
print("\n=== |recomputed - reported| > 0.05 MPa ===")
print(S[S["d_mean"].abs() > 0.05][["series","mix","age","n","mean","mean_reported","d_mean"]].round(2).to_string())
# 2. threshold compliance
print("\n=== 7 d, 14 d, 28 d: specimens below 35 MPa / mean below 35 ===")
for age in (7, 14, 28):
    sub = S[S.age == age]
    print(age, "d mean<35:", list(sub[sub["mean"] < 35].mix), "| mean>=50:", list(sub[sub["mean"] >= 50].mix))
L = strength_long(); L = L[~L.placeholder]
print("min specimen <35 at 28d:", L[(L.age==28)&(L.fc<35)][["series","mix","fc"]].values.tolist())
# 3. growth ratios
piv = S.pivot_table(index=["series","mix"], columns="age", values="mean")
piv["r14_7"] = piv[14]/piv[7]; piv["r28_14"] = piv[28]/piv[14]; piv["f7_28"]=piv[7]/piv[28]; piv["f14_28"]=piv[14]/piv[28]
print("\n=== growth ratios ===\n", piv.round(3).to_string())
# 4. ANOVA / Tukey at 28 d per series
for series in ("I","II"):
    sub = L[(L.series==series)&(L.age==28)]
    groups = [g.fc.values for _, g in sub.groupby("mix")]
    F, p = stats.f_oneway(*groups)
    print(f"\n28 d ANOVA series {series}: F={F:.2f}, p={p:.2e}")
    try:
        order = (S1_ORDER if series=="I" else S2_ORDER)
        gs = [sub[sub.mix==m].fc.values for m in order]
        res = stats.tukey_hd(*gs)
        print(order); print(np.round(res.pvalue,4))
    except Exception as e:
        print("tukey failed", e)
# 5. density
D = density_long()
Dg = D.groupby(["mix","age_d"]).agg(rho=("density","mean"), n=("density","count"), sd=("density","std")).reset_index()
print("\n=== density per mix-age (recomputed from per-specimen) ===\n", Dg.round(1).to_string())
rep = pd.read_csv(os.path.join(DATA,"density_table4-1.csv"))
print(rep)
# recompute density from mass/volume
D["rho_calc"] = D["mass_kg"]/D["volume_m3"]
print("max |rho_reported_specimen - m/V| =", (D["rho_calc"]-D["density"]).abs().max())
# 6. absorption: quantization check
A = absorption_long()
print("\n=== absorption ===\n", A.groupby(["series","mix","age"]).ab.agg(["count","mean","std","min","max"]).round(3).to_string())
a1 = A[A.series=="I"].copy(); a1["calc"] = (a1.wet-a1.dry)/a1.dry*100
print((a1[["age","wet","dry","ab","calc"]]).round(3))
# 7. Strength vs density regression (series I, per mix-age means)
m = S[S.series=="I"].merge(Dg.rename(columns={"age_d":"age"}), on=["mix","age"])
x = np.log(m.rho); y = np.log(m["mean"])
sl, ic, r, p, se = stats.linregress(x, y)
print(f"\nlog-log fc = a*rho^b: b={sl:.2f}, R2={r**2:.3f}, p={p:.3g}, n={len(m)}")
m28 = m[m.age==28]
sl28, ic28, r28, p28, se28 = stats.linregress(np.log(m28.rho), np.log(m28["mean"]))
print(f"28 d only: b={sl28:.2f} R2={r28**2:.3f} p={p28:.3g} n={len(m28)}")
