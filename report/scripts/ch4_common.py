"""Helpers shared by the Chapter 4 modules (numbers are computed from data/*.csv, never typed by hand)."""
import numpy as np, pandas as pd
from scipy import stats
from content_common import *
from prp_data import *
import rnum

N = rnum.load()
S = strength_summary()
D = density_long()

def pct(a, b):                     # percentage change of a relative to b
    return (a / b - 1) * 100

def cld(series, age, order):
    """Compact letter display from the Tukey HSD table (split-and-absorb algorithm)."""
    tk = N["tukey"]; tk = tk[(tk.series == series) & (tk.age == age)]
    sig = [(r.g1, r.g2) for r in tk.itertuples() if bool(r.reject)]
    groups = [frozenset(order)]
    for a, b in sig:
        nxt = []
        for g in groups:
            if a in g and b in g:
                nxt.append(g - {a}); nxt.append(g - {b})
            else:
                nxt.append(g)
        groups = [g for g in set(nxt) if g and not any(g < h for h in nxt)]
    groups = sorted(set(groups), key=lambda g: min(order.index(m) for m in g))
    letters = "abcdefgh"
    return {m: "".join(letters[i] for i, g in enumerate(groups) if m in g) for m in order}

def dens_fit():
    sub = D[D.mix != "NA"]
    sl, ic, r, p, se = stats.linregress(sub.mix.map(S1_BIOCHAR), sub.density)
    return sl, r ** 2, p

def dens_anova(age):
    sub = D[D.age_d == age]; g = [x.density.values for _, x in sub.groupby("mix")]
    F, p = stats.f_oneway(*g); return F, p

def f1(x): return f"{x:.1f}"
def f2(x): return f"{x:.2f}"
def d0(x): return f"{x:,.0f}"
def pv(p): return "< 0.001" if p < 0.001 else f"{p:.3f}"

def tp(series, age, g1, g2):
    """Tukey-adjusted p value of one pair (order-insensitive)."""
    t = N["tukey"]; t = t[(t.series == series) & (t.age == age) & (((t.g1 == g1) & (t.g2 == g2)) | ((t.g1 == g2) & (t.g2 == g1)))]
    return float(t.p_adj.iloc[0])
