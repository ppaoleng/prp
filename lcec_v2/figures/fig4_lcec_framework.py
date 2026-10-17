"""Fig. 4 - the LCEC Framework (three analytical units, two links, feedback loop)."""
from fig_style import *

B, N, I = "bold", "normal", "normal"
c = Canvas(W_TEXT)
ax = c.ax
top = c.H - 0.05
PW, GAP = 1.95, 0.26
xs = [0.0, PW + GAP, 2 * (PW + GAP)]
HEAD_H = 0.52
SZ = 8.2

units = [
    ("LC", "Learning configuration", ACCENT, ACCENT_EDGE, ACCENT_TINT,
     ["Task constraints and representations", "Individual or joint action", "Instructional support and feedback", "Tools, access and resources"]),
    ("E", "Assessment evidence", GREEN, GREEN_EDGE, GREEN_TINT,
     ["Products, performances and process records", "Criteria, assessors and units", "Timing and source limitations", "Alternative explanations"]),
    ("C", "Competence claim", WARM, WARM_EDGE, WARM_TINT,
     ["Capability inferred", "Learner or team concerned", "Task or application context", "Support, timing and scope"]),
]

y_head = top - 0.45                # leave room for the feedback loop
# measure body height (max over panels)
pad, itemgap = 0.11, 0.075
def body_h(items):
    return pad * 2 + sum(c.para(0, 0, PW - 2 * pad, [(t, N, I, INK)], size=SZ, draw=False) for t in items) + itemgap * (len(items) - 1)
BH = max(body_h(u[5]) for u in units) + 0.12
for (code, name, col, edge, tint, items), x in zip(units, xs):
    c.rect(x, y_head, PW, HEAD_H, fc=tint, ec=col, lw=1.2, z=2)
    # header: code + name
    cw = c._w(code, 13, "bold")
    base = y_head - HEAD_H / 2 - 0.045
    c.ax.text(x + 0.12, base, code, fontsize=13, fontweight="bold", color=edge, ha="left", va="baseline", zorder=6)
    c.ax.text(x + 0.12 + cw + 0.10, base, name, fontsize=8.8, fontweight="bold", color=INK, ha="left", va="baseline", zorder=6)
    c.rect(x, y_head - HEAD_H, PW, BH, fc="white", ec=col, lw=1.0, z=1)
    yy = y_head - HEAD_H - pad
    for k, t in enumerate(items):
        h = c.para(x + pad, yy, PW - 2 * pad, [(t, N, I, INK)], size=SZ)
        yy -= h
        if k < len(items) - 1:
            c.line([(x + pad, yy - itemgap / 2), (x + PW - pad, yy - itemgap / 2)], color="#d6d6d1", lw=0.5, z=2)
        yy -= itemgap

ymid = y_head - HEAD_H - BH / 2
# links between panels
c.arrow((xs[0] + PW, ymid), (xs[1], ymid), color=INK, lw=1.1, ms=7)
c.arrow((xs[1] + PW, ymid), (xs[2], ymid), color=INK, lw=1.1, ls=(0, (3.2, 2.2)), ms=7)

# feedback loop above (E -> LC)
fy = top - 0.19
c.line([(xs[1] + PW / 2, y_head), (xs[1] + PW / 2, fy), (xs[0] + PW / 2, fy)], color=INK_SEC, lw=0.9, ls=(0, (3.2, 2.2)))
c.arrow((xs[0] + PW / 2, fy), (xs[0] + PW / 2, y_head), color=INK_SEC, lw=0.9, ms=6.5)
c.para(xs[0] + PW / 2 + 0.1, top + 0.02, 3.2, [("Feedback may inform subsequent configuration", N, "italic", INK_SEC)], size=7.8)

# bracketed link definitions underneath
yb = y_head - HEAD_H - BH - 0.14
def bracket(xa, xb, ytop_):
    c.line([(xa, ytop_), (xa, ytop_ - 0.06), (xb, ytop_ - 0.06), (xb, ytop_)], color=INK_SEC, lw=0.8)
bracket(xs[0] + PW / 2, xs[1] + PW / 2 - 0.06, yb)
bracket(xs[1] + PW / 2 + 0.06, xs[2] + PW / 2, yb)
w1, w2 = 2.45, 2.05
c1 = (xs[0] + PW / 2 + xs[1] + PW / 2 - 0.06) / 2
c2 = (xs[1] + PW / 2 + 0.06 + xs[2] + PW / 2) / 2
c.para(c1 - w1 / 2, yb - 0.11, w1, [("LC–E link: ", B, I, INK), ("what the activity makes observable, and how observations are sampled", N, I, INK)], size=7.9, align="center")
c.para(c2 - w2 / 2, yb - 0.11, w2, [("E–C link: ", B, I, INK), ("what the evidence justifies", N, I, INK)], size=7.9, align="center")
c.finish("fig4_lcec_framework.png", top=top + 0.17)
