"""Fig. 6 - research propositions P1-P3 as contrasts in LC, evidence to collect (E) and interpretation to test (C)."""
from fig_style import *

B, N, I = "bold", "normal", "normal"
c = Canvas(W_TEXT)
ax = c.ax
top = c.H - 0.05
LBL_W = 0.42
GAPX = 0.30
CW = (W_TEXT - LBL_W - 2 * GAPX) / 3
xs = [LBL_W + k * (CW + GAPX) for k in range(3)]
HEAD_H = 0.46
SZ = 7.9
PAD = 0.10
ROWGAP = 0.13

heads = [("LC", "Configuration contrast", ACCENT, ACCENT_EDGE, ACCENT_TINT),
         ("E", "Evidence to collect", GREEN, GREEN_EDGE, GREEN_TINT),
         ("C", "Interpretation to test", WARM, WARM_EDGE, WARM_TINT)]
for (code, name, col, edge, tint), x in zip(heads, xs):
    c.rect(x, top, CW, HEAD_H, fc=tint, ec=col, lw=1.2, z=2)
    cw = c._w(code, 12.5, "bold")
    base = top - HEAD_H / 2 - 0.043
    ax.text(x + 0.12, base, code, fontsize=12.5, fontweight="bold", color=edge, ha="left", va="baseline", zorder=6)
    ax.text(x + 0.12 + cw + 0.10, base, name, fontsize=8.6, fontweight="bold", color=INK, ha="left", va="baseline", zorder=6)

rows = [
    ("P1",
     "Tasks that require resolving conflicting representations, compared with parallel division of labour (technical problem, time and criteria held as constant as possible)",
     "Whether learners state a reason, evaluate an alternative, challenge a proposal and make a linked revision; team-level dependence; quality of an episode, not only its frequency",
     "More substantively justified joint evaluation (expected, not demonstrated)"),
    ("P2",
     "Feedback that requires a revision and an explanation of its rationale",
     "Linked feedback, revision and rationale records compared with final products; independently scored related task; agreement between assessors",
     "Evaluative development made more assessable than by a final artefact alone (expected, not demonstrated)"),
    ("P3",
     "Performance judged against explicit professional criteria",
     "Experience ratings, calibrated external assessments and a separately scored changed-context task; prior attainment, support and opportunity to perform",
     "Information about changed-task performance that experience ratings alone do not provide (expected, not demonstrated)"),
]
edges = [(ACCENT, ACCENT_EDGE), (GREEN, GREEN_EDGE), (WARM, WARM_EDGE)]
y = top - HEAD_H - 0.16
for label, *cells in rows:
    hs = [c.para(0, 0, CW - 2 * PAD, [(t, N, I, INK)], size=SZ, draw=False) for t in cells]
    RH = max(hs) + 2 * PAD + 0.04
    ymid = y - RH / 2
    ax.text(0.0, ymid - 0.05, label, fontsize=11, fontweight="bold", color=INK, ha="left", va="baseline", zorder=6)
    for k, (t, x) in enumerate(zip(cells, xs)):
        c.rect(x, y, CW, RH, fc="white", ec=edges[k][0], lw=1.0, z=2)
        h = c.para(x + PAD, 0, CW - 2 * PAD, [(t, N, I, INK)], size=SZ, draw=False)
        c.para(x + PAD, ymid + h / 2, CW - 2 * PAD, [(t, N, I, INK)], size=SZ)
    c.arrow((xs[0] + CW, ymid), (xs[1], ymid), color=INK, lw=1.1, ms=7)
    c.arrow((xs[1] + CW, ymid), (xs[2], ymid), color=INK, lw=1.1, ls=(0, (3.2, 2.2)), ms=7)
    y -= RH + ROWGAP
c.finish("fig6_propositions.png", top=top + 0.02)
