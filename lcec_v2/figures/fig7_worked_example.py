"""Fig. 7 - worked example: one learning configuration, several kinds of evidence, distinct claims."""
from fig_style import *

B, N, I = "bold", "normal", "normal"
c = Canvas(W_TEXT)
ax = c.ax
top = c.H - 0.05
PW1, G1, PW2, G2 = 1.80, 0.24, 1.80, 0.50
CX = PW1 + G1 + PW2 + G2
CWd = W_TEXT - CX
X1, X2 = 0.0, PW1 + G1
HEAD_H = 0.46
SZ = 8.0
PAD = 0.11

claims = [("Team performance", "Correct group product"),
          ("Individual capability", "Independent explanation or related-task performance"),
          ("Situated judgement", "Recorded critique and justified revision"),
          ("External alignment", "Calibrated practitioner assessment against explicit criteria"),
          ("Transfer", "Changed task conditions, support documented; delayed repetition shows retention only")]
CGAP = 0.07
chs = []
for nm, sub in claims:
    h = 0.07 + 0.145 + c.para(0, 0, CWd - 2 * PAD, [(sub, N, I, INK)], size=7.7, draw=False) + 0.07
    chs.append(h)
STACK = sum(chs) + CGAP * (len(claims) - 1)

heads = [("LC", "Learning configuration", ACCENT, ACCENT_EDGE, ACCENT_TINT, X1, PW1),
         ("E", "Assessment evidence", GREEN, GREEN_EDGE, GREEN_TINT, X2, PW2),
         ("C", "Competence claim", WARM, WARM_EDGE, WARM_TINT, CX, CWd)]
for code, name, col, edge, tint, x, w in heads:
    c.rect(x, top, w, HEAD_H, fc=tint, ec=col, lw=1.2, z=2)
    cw = c._w(code, 12.5, "bold")
    base = top - HEAD_H / 2 - 0.043
    ax.text(x + 0.12, base, code, fontsize=12.5, fontweight="bold", color=edge, ha="left", va="baseline", zorder=6)
    nm_w = c._w(name, 8.3, "bold")
    if x + 0.12 + cw + 0.10 + nm_w > x + w - 0.04:      # two-line name
        c.para(x + 0.12 + cw + 0.10, top - 0.095, w - cw - 0.26, [(name, B, I, INK)], size=8.6)
    else:
        ax.text(x + 0.12 + cw + 0.10, base, name, fontsize=8.3, fontweight="bold", color=INK, ha="left", va="baseline", zorder=6)

ybody = top - HEAD_H - 0.06
lc = ["A team resolves a conflict between a service route and a structural element under cost, access and construction-sequence constraints.",
      "Responsibilities and available support are defined.",
      "A shared BIM model or annotated drawings make the conflict visible."]
ev = ["Annotated alternatives, a short recorded critique and linked versions of the design.",
      "Criteria: technical reasoning, treatment of constraints and justification of the revision.",
      "Individual evidence where needed: an independently explained decision or performance on a related task."]
for items, x, w, col in [(lc, X1, PW1, ACCENT), (ev, X2, PW2, GREEN)]:
    c.rect(x, ybody, w, STACK, fc="white", ec=col, lw=1.0, z=1)
    hs = [c.para(0, 0, w - 2 * PAD, [(t, N, I, INK)], size=SZ, draw=False) for t in items]
    gap = 0.09
    tot = sum(hs) + gap * (len(items) - 1)
    yy = ybody - (STACK - tot) / 2
    for k, t in enumerate(items):
        h = c.para(x + PAD, yy, w - 2 * PAD, [(t, N, I, INK)], size=SZ)
        yy -= h + gap

# claim boxes
yy = ybody
mids = []
for (nm, sub), h in zip(claims, chs):
    c.rect(CX, yy, CWd, h, fc="white", ec=WARM, lw=1.0, z=2)
    c.para(CX + PAD, yy - 0.065, CWd - 2 * PAD, [(nm, B, I, INK)], size=8.4)
    c.para(CX + PAD, yy - 0.065 - 0.15, CWd - 2 * PAD, [(sub, N, I, INK)], size=7.7)
    mids.append(yy - h / 2)
    yy -= h + CGAP

# arrows
ymid = ybody - STACK / 2
c.arrow((X1 + PW1, ymid), (X2, ymid), color=INK, lw=1.1, ms=7)
xe = X2 + PW2
xt = xe + G2 * 0.45
c.line([(xe, ymid), (xt, ymid)], color=INK, lw=1.0, ls=(0, (3.2, 2.2)))
c.line([(xt, mids[0]), (xt, mids[-1])], color=INK, lw=1.0, ls=(0, (3.2, 2.2)))
for m in mids:
    c.arrow((xt, m), (CX, m), color=INK, lw=1.0, ls=(0, (3.2, 2.2)), ms=6.5)
c.finish("fig7_worked_example.png", top=top + 0.02)
