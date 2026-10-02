"""Shared data layer for the PRP 2569 report (all numbers come from data/*.csv,
which were parsed from the original DRAFT docx by extract_data.py)."""
import os, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

# --- canonical mix labels -------------------------------------------------
S1_MAP = {"NA (อ้างอิง)": "NA", "RA (ไบโอชาร์ 0%)": "RA", "ไบโอชาร์ 5%": "Rab5",
          "ไบโอชาร์ 10%": "Rab10", "ไบโอชาร์ 15%": "Rab15", "Rab5%": "Rab5"}
S2_MAP = {"RCA 0%": "RCA0", "RCA 5%": "RCA5", "RCA 10%": "RCA10", "RCA 15%": "RCA15"}
S1_ORDER = ["NA", "RA", "Rab5", "Rab10", "Rab15"]
S2_ORDER = ["RCA0", "RCA5", "RCA10", "RCA15"]
S1_BIOCHAR = {"NA": 0, "RA": 0, "Rab5": 5, "Rab10": 10, "Rab15": 15}
S2_RCA = {"RCA0": 0, "RCA5": 5, "RCA10": 10, "RCA15": 15}

# Specimens whose original record is missing (Appendix B item B-4 of the draft).
# Table 4-2 of the draft shows a number in these cells, but the reported mean matches n=2,
# so the displayed value is treated as a PLACEHOLDER and is excluded from every statistic.
PLACEHOLDER_SPECIMENS = {("NA", 14, "s1"), ("RA", 7, "s3"), ("RA", 14, "s2")}

def _read(name):
    return pd.read_csv(os.path.join(DATA, name))

def strength_long():
    """Return tidy per-specimen compressive strength (series, mix, age, spec, MPa, placeholder flag)."""
    rows = []
    s1 = _read("strength_series1.csv"); s2 = _read("strength_series2.csv")
    for series, df, mp in (("I", s1, S1_MAP), ("II", s2, S2_MAP)):
        for _, r in df.iterrows():
            mix = mp[r["mix"]]
            for k in ("s1", "s2", "s3"):
                ph = (mix, int(r["age_d"]), k) in PLACEHOLDER_SPECIMENS
                rows.append(dict(series=series, mix=mix, age=int(r["age_d"]), spec=k,
                                 fc=r[k], placeholder=ph, mean_reported=r["mean_reported"]))
    return pd.DataFrame(rows)

def strength_summary():
    L = strength_long()
    rec = L[~L.placeholder]
    g = rec.groupby(["series", "mix", "age"])
    out = g["fc"].agg(n="count", mean="mean", sd=lambda x: x.std(ddof=1) if len(x) > 1 else np.nan,
                      mn="min", mx="max").reset_index()
    rep = L.groupby(["series", "mix", "age"])["mean_reported"].first().reset_index()
    out = out.merge(rep, on=["series", "mix", "age"])
    out["cv_pct"] = out["sd"] / out["mean"] * 100
    from scipy import stats
    out["ci95"] = [stats.t.ppf(0.975, n - 1) * sd / np.sqrt(n) if n > 1 else np.nan
                   for n, sd in zip(out["n"], out["sd"])]
    return out

def absorption_long():
    a1 = _read("absorption_series1_rab5.csv")
    a2 = _read("absorption_series2.csv")
    rows = []
    for _, r in a1.iterrows():
        rows.append(dict(series="I", mix="Rab5", age=int(r["age_d"]), spec=f"{len(rows)%3+1}", ab=r["abs_pct"],
                         wet=r["wet_kg"], dry=r["dry_kg"]))
    for _, r in a2.iterrows():
        for k in ("s1", "s2", "s3"):
            rows.append(dict(series="II", mix=S2_MAP[r["mix"]], age=int(r["age_d"]), spec=k, ab=r[k], wet=np.nan, dry=np.nan))
    return pd.DataFrame(rows)

def density_long():
    a = _read("appendixA1_density_per_specimen.csv")
    a["mix"] = a["mix"].map(S1_MAP)
    return a

def mix_design():
    m = _read("mix_design_table3-1.csv")
    names = ["CONTROL1", "Rab5", "Rab10", "Rab15", "Rab20", "Rab25", "CONTROL2", "RCA5", "RCA10", "RCA15"]
    m["code"] = names
    return m

BLOCK_VOLUME_M3 = 0.00156     # reported in Appendix A (260 cm2 x 6 cm)
BLOCKS_PER_M2 = 40            # draft sec. 2.3: ~40 zig-zag blocks per m2
TIS827_MPa = 35.0
TIS2035_MPa = 50.0
