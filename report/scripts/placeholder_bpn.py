"""[Place Holder] British Pendulum Number (BPN) dataset.

IMPORTANT: NONE of these numbers is a measurement.  They are a *hypothetical, mechanics-consistent*
stand-in for the slip-resistance tests that are still in progress, to be replaced by the laboratory
record.  Construction rules (all documented in the report, Section 4.5.1):
  * 28-d dry/wet anchors = the example values already printed in the draft Table 4-6
    (user confirmed they are example values); NA anchor added by the same logic.
  * age effect: BPN(t) = BPN28 - K_AGE * (1 - fc(t)/fc28), where fc(t)/fc28 is the MEASURED
    strength-development ratio of the same mix (Section 4.3).  K_AGE = 6.5 BPN per unit strength
    deficit (calibrated on the 3->28 d trend printed in the 2568 reference report).
  * dry-wet reduction: dw(mix) = 28-d anchor difference, +/- small noise.
  * between-block scatter: SD ~ 1.0-2.2 BPN (pendulum repeatability magnitude), deterministic seed.
"""
import os, sys, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from prp_data import *

K_AGE = 6.5
SEED = 20690101   # fixed seed -> reproducible placeholders (a fresh generator is created on every build() call)

ANCHOR = {  # (dry28, wet28) -- Table 4-6 of the draft (example values) ; NA is an added placeholder
    "NA":   (68.6, 59.1),
    "RA":   (69.5, 58.8), "Rab5": (67.2, 58.2), "Rab10": (65.5, 55.6), "Rab15": (63.4, 53.7),
    "RCA0": (68.7, 59.4), "RCA5": (67.6, 56.3), "RCA10": (62.4, 54.7), "RCA15": (61.7, 52.5),
}
SERIES = {m: "I" for m in S1_ORDER} | {m: "II" for m in S2_ORDER}

def build():
    rng = np.random.default_rng(SEED)
    S = strength_summary().set_index(["mix", "age"])
    rows = []
    for mix, (d28, w28) in ANCHOR.items():
        dw28 = d28 - w28
        for age in (7, 14, 28):
            fr = S.loc[(mix, age), "mean_reported"] / S.loc[(mix, 28), "mean_reported"]
            dry = d28 - K_AGE * (1 - fr)
            dw = dw28 + (rng.normal(0, 0.35) if age != 28 else 0.0)
            wet = dry - dw
            if age != 28:
                dry += rng.normal(0, 0.25); wet += rng.normal(0, 0.25)
            sd_d = rng.uniform(1.0, 1.8); sd_w = rng.uniform(1.2, 2.2)
            rows.append(dict(series=SERIES[mix], mix=mix, age=age,
                             bpn_dry=round(dry, 1), sd_dry=round(sd_d, 1),
                             bpn_wet=round(wet, 1), sd_wet=round(sd_w, 1),
                             n_blocks=3, status="PLACEHOLDER"))
    df = pd.DataFrame(rows)
    df["wet_drop"] = (df.bpn_dry - df.bpn_wet).round(1)
    df["wet_ratio"] = (df.bpn_wet / df.bpn_dry).round(3)
    return df

if __name__ == "__main__":
    df = build()
    df.to_csv(os.path.join(DATA, "bpn_PLACEHOLDER.csv"), index=False)
    print(df.to_string())
