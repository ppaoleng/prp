"""Fig. 5 - evidence-claim bands and the missing links between them."""
from fig_style import *

B, N, I = "bold", "normal", "normal"
c = Canvas(W_TEXT)
ax = c.ax
top = c.H - 0.05
NX = 0.0                  # numeral column
BX, BW = 0.36, 3.95
BH = 0.60
LINKH = 0.40
SZ = 8.2

bands = [
    ("5", "Transfer", "Performance under changed task or work conditions", None),
    ("4", "External alignment", "Work judged against explicit and defensible professional criteria", "Classroom endorsement is not application in another context"),
    ("3", "Situated judgement", "Artefacts, reasons, critique and linked revision traces", "Local criteria may not represent occupational standards"),
    ("2", "Task learning", "Knowledge or performance assessed on a defined task", "A correct product may conceal its reasoning"),
    ("1", "Learner response", "Experience, confidence, usability or satisfaction", "Perceived ease is not demonstrated knowledge"),
]
y = top
tops = []
for k, (num, name, desc, link) in enumerate(bands):
    if k > 0:
        # missing-link connector between band k-1 (above) and band k (below): arrow points up
        y_gap_top = y
        y_gap_bot = y - LINKH
        xa = BX + 0.42
        c.arrow((xa, y_gap_bot), (xa, y_gap_top), color=WARM_EDGE, lw=0.9, ls=(0, (2.4, 1.8)), ms=6.5)
        # the link text belongs to the arrow between band k (below) and band k-1 (above)
        txt = bands[k][3]
        c.para(xa + 0.14, y_gap_top - 0.055, BX + BW - xa - 0.2, [("Missing link: ", B, I, WARM_EDGE), (txt, N, "italic", INK_SEC)], size=7.6)
        y -= LINKH
    c.rect(BX, y, BW, BH, fc=PANEL, ec=STEEL_EDGE, lw=0.9, z=2)
    c.ax.text(NX + 0.12, y - BH / 2 - 0.06, num, fontsize=16, fontweight="bold", color=INK, ha="center", va="baseline", zorder=6)
    c.para(BX + 0.12, y - 0.085, BW - 0.24, [(name, B, I, INK)], size=8.8)
    c.para(BX + 0.12, y - 0.265, BW - 0.24, [(desc, N, I, INK)], size=SZ)
    tops.append(y)
    y -= BH
bottom = y

# right-hand cross-cutting bracket (dashed)
RX = BX + BW + 0.32
RW = W_TEXT - RX
c.rect(RX, top, RW, top - bottom, fc="white", ec=STEEL_EDGE, lw=0.9, ls=(0, (4, 2.4)), z=1)
yc = (top + bottom) / 2
items = ["Independence", "Support", "Context change", "Timing"]
hh = 0.17 + 4 * 0.17 + 0.09 + c.para(0, 0, RW - 0.24, [("Immediate to durable application: delayed assessment, with context change examined separately", N, "italic", INK_SEC)], size=7.6, draw=False)
yy = yc + hh / 2
c.para(RX + 0.12, yy, RW - 0.24, [("Cut across all bands", B, I, INK)], size=8.8, align="center")
yy -= 0.30
for t in items:
    c.para(RX + 0.12, yy, RW - 0.24, [(t, N, I, INK)], size=SZ, align="center")
    yy -= 0.17
yy -= 0.07
c.para(RX + 0.12, yy, RW - 0.24, [("Immediate to durable application: delayed assessment, with context change examined separately", N, "italic", INK_SEC)], size=7.6, align="center")
c.finish("fig5_bands.png", top=top + 0.02)
