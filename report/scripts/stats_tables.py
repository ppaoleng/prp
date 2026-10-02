"""Statistical tables (ANOVA, Tukey HSD, maturity-model fits, regressions) -> data/stats_*.csv"""
import os, sys, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from prp_data import *
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

L = strength_long(); L = L[~L.placeholder]
S = strength_summary()
rows = []; tuk = []
for series, order in (("I", S1_ORDER), ("II", S2_ORDER)):
    for age in (7, 14, 28):
        sub = L[(L.series == series) & (L.age == age)]
        groups = [sub[sub.mix == m].fc.values for m in order]
        F, p = stats.f_oneway(*groups)
        dfb = len(order) - 1; dfw = len(sub) - len(order)
        # eta-squared
        grand = sub.fc.mean(); ssb = sum(len(g) * (g.mean() - grand) ** 2 for g in groups); sst = ((sub.fc - grand) ** 2).sum()
        rows.append(dict(series=series, age=age, F=F, df1=dfb, df2=dfw, p=p, eta2=ssb / sst))
        th = pairwise_tukeyhsd(sub.fc.values, sub.mix.values, alpha=0.05)
        for r in th.summary().data[1:]:
            tuk.append(dict(series=series, age=age, g1=r[0], g2=r[1], meandiff=r[2], p_adj=r[3], lower=r[4], upper=r[5], reject=r[6]))
pd.DataFrame(rows).to_csv(os.path.join(DATA, "stats_anova.csv"), index=False)
pd.DataFrame(tuk).to_csv(os.path.join(DATA, "stats_tukey.csv"), index=False, na_rep="")
print(pd.DataFrame(rows).round(4).to_string())

# --- maturity fits: ln(f/f28) = s*(1 - sqrt(28/t))   (EN 1992-1-1 form of beta_cc(t)) ---
fits = []
for (series, mix), g in S.groupby(["series", "mix"]):
    g = g.set_index("age")["mean_reported"]
    x = np.array([1 - np.sqrt(28 / 7), 1 - np.sqrt(28 / 14)]); y = np.log(np.array([g[7] / g[28], g[14] / g[28]]))
    s_hat = float((x * y).sum() / (x * x).sum())
    pred7 = np.exp(s_hat * x[0]); pred14 = np.exp(s_hat * x[1])
    s7 = -np.log(g[7] / g[28]); s14 = -np.log(g[14] / g[28]) / (np.sqrt(28 / 14) - 1)
    fits.append(dict(series=series, mix=mix, s_fit=s_hat, s_from_7d=s7, s_from_14d=s14, f7_f28=g[7] / g[28], f14_f28=g[14] / g[28],
                     pred_f7=pred7, pred_f14=pred14))
F = pd.DataFrame(fits)
F.to_csv(os.path.join(DATA, "stats_maturity_fits.csv"), index=False)
print(F.round(3).to_string())

# --- regressions ---
Dg = density_long().groupby(["mix", "age_d"]).density.mean().reset_index().rename(columns={"age_d": "age"})
m = S[S.series == "I"].merge(Dg, on=["mix", "age"])
out = []
sl, ic, r, p, se = stats.linregress(np.log(m.rho if 'rho' in m else m.density), np.log(m["mean_reported"]))
out.append(dict(model="ln fc = ln a + b ln(rho), series I, all ages", n=len(m), slope=sl, intercept=ic, r2=r ** 2, p=p, se=se))
m28 = m[m.age == 28]
sl, ic, r, p, se = stats.linregress(np.log(m28.density), np.log(m28["mean_reported"]))
out.append(dict(model="ln fc = ln a + b ln(rho), series I, 28 d", n=len(m28), slope=sl, intercept=ic, r2=r ** 2, p=p, se=se))
# cement content vs strength (series I, 28 d)
inv = pd.read_csv(os.path.join(DATA, "lca_inventory_kg_per_m3.csv"), keep_default_na=False).set_index("mix")
m28 = m28.assign(cement=m28.mix.map(inv.cement))
sl, ic, r, p, se = stats.linregress(m28[m28.mix != "NA"].cement, m28[m28.mix != "NA"]["mean_reported"])
out.append(dict(model="fc28 = a + b*cement (kg/m3), RA & Rab series", n=len(m28[m28.mix != "NA"]), slope=sl, intercept=ic, r2=r ** 2, p=p, se=se))
# series II: fc28 vs RCA %
s2 = S[(S.series == "II") & (S.age == 28)]; xs = s2.mix.map(S2_RCA)
sl, ic, r, p, se = stats.linregress(xs, s2["mean_reported"]); out.append(dict(model="fc28 = a + b*RCA% (series II)", n=len(s2), slope=sl, intercept=ic, r2=r ** 2, p=p, se=se))
pd.DataFrame(out).to_csv(os.path.join(DATA, "stats_regressions.csv"), index=False)
print(pd.DataFrame(out).round(4).to_string())
