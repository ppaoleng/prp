"""Fig. 2 - review procedure flowchart (full text width). Content follows the V1 figure."""
from fig_style import *

B, N, I = "bold", "normal", "normal"
c = Canvas(W_TEXT)
ax = c.ax
X0, BW = 0.05, 4.45            # main column
XC = X0 + BW / 2
LX = 5.02                       # S1-sheet label column
SZ = 8.2
PAD = 0.085
GAP = 0.20
y = c.H - 0.05

# column header for the S1 sheet labels
c.para(LX, y - 0.0, W_TEXT - LX, [("Documented in", N, "italic", INK_SEC)], size=7.2)
c.para(LX, y - 0.12, W_TEXT - LX, [("Supplementary Material S1", N, "italic", INK_SEC)], size=7.2)
y -= 0.40

def step(y, segs, sheet=None, fc="white", ec=STEEL_EDGE, lw=0.9, ls="-", tc=INK, sheet_sz=7.8):
    segs = [(t, w, s, tc) for (t, w, s, _c) in segs] if tc != INK else segs
    h = c.para(X0 + PAD, y - PAD, BW - 2 * PAD, segs, size=SZ, align="center", draw=False) + 2 * PAD
    c.rect(X0, y, BW, h, fc=fc, ec=ec, lw=lw, ls=ls)
    c.para(X0 + PAD, y - PAD, BW - 2 * PAD, segs, size=SZ, align="center")
    if sheet:
        sh = c.para(LX, 0, W_TEXT - LX - 0.02, [(sheet, N, I, INK_SEC)], size=sheet_sz, draw=False)
        c.para(LX, y - h / 2 + sh / 2, W_TEXT - LX - 0.02, [(sheet, N, I, INK_SEC)], size=sheet_sz)
    return h

def down(y_from, y_to, x=XC, color=STEEL_EDGE):
    c.arrow((x, y_from), (x, y_to), color=color, lw=0.9, ms=6.5)

steps = [
    ([("Retained collection: ", B, I, INK), ("76 report records (R2 analytic collection). The merged discovery registry of 3,020 rows is kept as provenance only, not as a verified search denominator", N, I, INK)], "Corpus 76", {}),
    ([("Recorded R2 assessment: ", B, I, INK), ("37 INCLUDE, 38 BACKGROUND, 1 EXCLUDE", N, I, INK)], "Recorded Flags", {}),
    ([("Factual corrections logged: ", B, I, INK), ("RPT-000069 (published 2010) retained as background; RPT-000065 PDF mismatch, not counted as a core full text", N, I, INK)], "Corpus 76", {}),
    ([("Corrected disposition: ", B, I, INK), ("35 core, 39 contextual or foundational, 1 outside the educational focus, 1 without a matched full text", N, I, INK)], "Summary", dict(fc=ACCENT_TINT, ec=ACCENT, lw=1.1)),
    ([("Expert review of R2 summaries and targeted source checks ", B, I, INK), ("(logged 16 October 2026); unresolved fields kept explicit", N, I, INK)], "Source Audit, Inherited Checks", {}),
]
coding = ([("Coding and inferential appraisal: ", B, I, INK), ("sensitising categories (task conditions, collaborative judgement, technological mediation, assessment evidence, competence claims); appraisal of sampling, comparison, measurement source, unit, timing, alternative explanations and applicability", N, I, INK)], "LCEC Coding Guide", {})
after = [
    ([("Within-report interpretation and cross-report comparison ", B, I, INK), ("across five presentation groups; contrasting cases retained; no effects pooled", N, I, INK)], "Core Evidence", {}),
    ([("Synthesis outputs: ", B, I, INK), ("LCEC Framework, evidence-claim bands, configuration matrix and three research propositions", N, I, INK)], "Synthesis Map", dict(fc=WARM_TINT, ec=WARM, lw=1.1)),
]

for segs, sheet, kw in steps:
    h = step(y, segs, sheet, **kw)
    down(y - h, y - h - GAP + 0.01)
    y -= h + GAP

# coding box (loop re-enters here)
h = step(y, coding[0], coding[1])
coding_top, coding_h = y, h
down(y - h, y - h - GAP + 0.01)
y -= h + GAP

# decision diamond
DW, DH = 2.35, 0.95
cy = y - DH / 2
pts = [(XC, y), (XC + DW / 2, cy), (XC, y - DH), (XC - DW / 2, cy)]
ax.add_patch(Polygon(pts, closed=True, facecolor=GREEN_TINT, edgecolor=GREEN, lw=1.1, zorder=2, joinstyle="miter"))
th = c.para(XC - 0.85, 0, 1.7, [("Categories fit the evidence", B, I, INK)], size=SZ, align="center", draw=False)
c.para(XC - 0.85, cy + th / 2, 1.7, [("Categories fit the evidence", B, I, INK)], size=SZ, align="center")
c.ymin = min(c.ymin, y - DH)

# loop: No -> revise categories (right side, back to the coding box)
LXV = X0 + BW + 0.2
yin = coding_top - coding_h * 0.5
c.line([(XC + DW / 2, cy), (LXV, cy), (LXV, yin)], color=GREEN, lw=1.0, ls=(0, (4, 2.2)))
c.arrow((LXV, yin), (X0 + BW, yin), color=GREEN, lw=1.0, ms=6.5)
c.para(XC + DW / 2 + 0.05, cy + 0.20, LXV - (XC + DW / 2) - 0.05, [("No: revise categories", B, I, GREEN)], size=7.6, align="center")
# yes
YG = 0.26
down(y - DH, y - DH - YG + 0.01, color=STEEL_EDGE)
c.para(XC + 0.08, y - DH - 0.02, 0.5, [("Yes", B, I, GREEN)], size=7.6)
y -= DH + YG

for segs, sheet, kw in after:
    h = step(y, segs, sheet, **kw)
    if segs is not after[-1][0]:
        down(y - h, y - h - GAP + 0.01)
    y -= h + GAP

# not performed / claimed
segs = [("Not performed or claimed: ", B, I, INK_SEC), ("exhaustive systematic search; inter-reviewer agreement statistics; standardised risk-of-bias or certainty grading; pooling of effects", N, I, INK_SEC)]
y -= 0.03
h = c.para(X0 + PAD, y - PAD, BW - 2 * PAD, segs, size=SZ, align="center", draw=False) + 2 * PAD
c.rect(X0, y, BW, h, fc=GREY_TINT, ec=STEEL, lw=0.9, ls=(0, (4, 2.2)))
c.para(X0 + PAD, y - PAD, BW - 2 * PAD, segs, size=SZ, align="center")

c.finish("fig2_flowchart.png", top=c.H - 0.02)
