"""Group summary data used to redraw the figures.

PROVENANCE (important)
----------------------
Specimen-level records were not supplied with the v2 manuscript. Every number below comes from
(1) the manuscript tables/text (Tables 3, 7, 9; Sections 3.3-3.8), or
(2) group means / SDs read from the v2 Fig. 3 bitmap (marked DIGITISED), which were cross-checked:
    - epoxy group means reproduce the nine values quoted in Section 3.3 (within 0.01 MPa);
    - the pooled mean/SD per agent x strength reproduce Table 3 (mean within 0.01, SD within 0.02 MPa).
Replace the DIGITISED block with the raw specimen file when available (see README).
"""
import numpy as np
LE = 140.0            # bonded length, mm
FC = [4.9, 14.7, 23.5]
DB = [6, 9, 12]

# ---- plain bars: tau mean, SD (MPa) for each diameter at fc = 4.9, 14.7, 23.5 (n = 5) -------------
EPOXY = {6: [(0.17, .25), (1.15, 1.00), (2.19, 1.43)],
         9: [(0.20, .23), (2.02, .71), (1.98, .68)],
         12: [(2.61, 1.28), (1.33, .78), (5.23, .69)]}            # means: text Sec. 3.3; SD DIGITISED
GROUT = {6: [(0.00, .16), (0.61, .66), (0.34, .30)],
         9: [(1.07, .38), (0.00, .10), (0.50, .16)],
         12: [(0.58, .44), (0.50, .48), (0.29, .27)]}             # DIGITISED
MORTAR = {6: [(0.00, 0), (0.00, 0), (0.00, 0)],
          9: [(0.00, 0), (0.09, 0), (0.02, 0)],
          12: [(0.00, 0), (0.00, 0), (0.05, 0)]}                  # DIGITISED; SD < 0.1, inside marker
PLAIN = {"Epoxy": EPOXY, "Non-shrink grout": GROUT, "Cement mortar": MORTAR}

# Table 3 (pooled over diameters, n = 15): mean, SD
TABLE3 = {"Epoxy": [(1.00, 1.37), (1.50, 0.86), (3.13, 1.78)],
          "Non-shrink grout": [(0.55, 0.54), (0.37, 0.50), (0.37, 0.23)],
          "Cement mortar": [(0.00, 0.00), (0.04, 0.08), (0.03, 0.04)]}
ZERO_PCT = {"Epoxy": [33, 0, 7], "Non-shrink grout": [40, 53, 13], "Cement mortar": [100, 73, 67]}  # Fig. 4c labels

def pooled(groups):
    """Exact pooling of equal-size groups -> (mean, SD)."""
    m = np.array([g[0] for g in groups]); s = np.array([g[1] for g in groups]); k = len(m)
    M = m.mean(); n = 5
    var = ((n - 1) * (s ** 2).sum() + n * ((m - M) ** 2).sum()) / (k * n - 1)
    return M, var ** .5

# ---- GFRP (Table 7): {db: [(Pmean, Psd, Pmin, Pmax, splitting) for fc in FC]} ---------------------
GFRP = {6: [(11.1, .2, 10.9, 11.3, 0), (21.4, .7, 20.4, 22.2, 3), (17.9, 2.6, 14.3, 20.4, 3)],
        9: [(14.5, .4, 14.1, 15.0, 2), (20.8, .7, 19.9, 21.7, 3), (19.1, 3.6, 14.9, 24.2, 3)],
        12: [(15.3, .6, 14.4, 16.1, 3), (21.7, 1.6, 19.9, 23.4, 3), (23.8, 1.3, 22.6, 25.8, 3)]}
GFRP_B = {4.9: 0.47, 14.7: 0.01, 23.5: 0.41}
ACI_N = {6: 0.99, 9: 1.06, 12: 1.19}
POOLED_PLATEAU = (20.8, 2.7)

def tau_from_P(P, d): return P * 1e3 / (np.pi * d * LE)

def gfrp_N(d, i):
    P, s = GFRP[d][i][0], GFRP[d][i][1]
    f = FC[i]
    return tau_from_P(P, d) / f ** .5, tau_from_P(s, d) / f ** .5

def epoxy_mean_P(d, i):
    return EPOXY[d][i][0] * np.pi * d * LE / 1e3
