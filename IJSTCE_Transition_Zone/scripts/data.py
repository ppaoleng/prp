"""Numerical data transcribed from the manuscript tables (no new data).

Table 5: peak approach-side static stiffness (kN/mm) and stiffness ratio.
Table 6: peak wheel-rail contact force (kN) at 60/80/100/120 km/h.
Table 7: reduction in peak contact force relative to M1 (%).
"""
MODELS = ["M1", "M2", "M3", "M4", "M5"]
SPEEDS = [60, 80, 100, 120]
K_BRIDGE = 264.0

# Table 5
KD = {"M1": 44, "M2": 62, "M3": 72, "M4": 76, "M5": 77}
RHO = {"M1": 6.00, "M2": 4.26, "M3": 3.67, "M4": 3.47, "M5": 3.43}
KD_INCREASE = {"M1": None, "M2": 40.9, "M3": 63.6, "M4": 72.7, "M5": 75.0}

# Table 6
FORCE = {
    "M1": [55.00, 58.11, 64.45, 69.17],
    "M2": [51.50, 53.85, 56.80, 57.21],
    "M3": [49.49, 50.75, 51.02, 53.35],
    "M4": [50.06, 50.74, 51.08, 53.56],
    "M5": [49.55, 50.15, 51.08, 52.78],
}
FORCE_MEAN = {"M1": 61.68, "M2": 54.84, "M3": 51.15, "M4": 51.36, "M5": 50.89}
FORCE_RISE = {"M1": 25.8, "M2": 11.1, "M3": 7.8, "M4": 7.0, "M5": 6.5}

# Table 7
REDUCTION = {
    "M2": [6.37, 7.32, 11.87, 17.29],
    "M3": [10.02, 12.66, 20.84, 22.87],
    "M4": [8.98, 12.68, 20.74, 22.56],
    "M5": [9.90, 13.69, 20.75, 23.69],
}
