"""Three LLM-agent patterns for structural-engineering tasks: (a) single agent, (b) pair, (c) team.

Redraw of the author's own schematic. Blue = LLM-based agent(s), brown = structural solver
(external tool), grey = request / output. Arrow colour follows the source of the arrow.
"""
import os
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

from fig_style import (apply_style, save, INK, INK_SEC, LINE, PANEL_FILL,
                       ACCENT_EDGE, ACCENT_TINT, WARM_EDGE, WARM_TINT)

apply_style()

W, H = 100.0, 59.5
U = 0.072
FS_B, FS_L, FS_T = 7.5, 7.0, 9.0
PITCH = 2.1

fig = plt.figure(figsize=(W * U, H * U))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")
checks = []

KINDS = {
    "io":     dict(fill=PANEL_FILL, edge=INK_SEC),
    "llm":    dict(fill=ACCENT_TINT, edge=ACCENT_EDGE),
    "solver": dict(fill=WARM_TINT, edge=WARM_EDGE),
}
BLUE, BROWN, GREY = ACCENT_EDGE, WARM_EDGE, INK_SEC


def rect(x0, y0, x1, y1, fc, ec, lw=0.9, z=3, ls="-"):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=fc, edgecolor=ec, linewidth=lw,
                           linestyle=ls, zorder=z, joinstyle="miter"))


def lines_in(x0, y0, x1, y1, lines, fs=FS_B, color=INK):
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    span = PITCH * (len(lines) - 1)
    base = cy + span / 2 - 0.36
    for i, ln in enumerate(lines):
        t = ax.text(cx, base - i * PITCH, ln, ha="center", va="baseline", fontsize=fs, color=color, zorder=6)
        checks.append((t, (x0, y0, x1, y1)))


def box(cx, cy, w, h, kind, lines):
    k = KINDS[kind]
    rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, k["fill"], k["edge"])
    lines_in(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, lines)
    return dict(l=cx - w / 2, r=cx + w / 2, b=cy - h / 2, t=cy + h / 2, cx=cx, cy=cy)


def arrow(pts, color, lw=1.0, L=1.7, hw=0.8):
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    xs = [p[0] for p in pts[:-1]] + [x2 - ux * (L - 0.5)]
    ys = [p[1] for p in pts[:-1]] + [y2 - uy * (L - 0.5)]
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="butt", solid_joinstyle="miter", zorder=1)
    bx, by = x2 - ux * L, y2 - uy * L
    ax.add_patch(Polygon([[x2, y2], [bx - uy * hw, by + ux * hw], [bx + uy * hw, by - ux * hw]],
                         closed=True, facecolor=color, edgecolor=color, lw=0.3, zorder=5))


# ------------------------------------------------------------------ geometry
PW, PG, MX = 31.6, 2.0, 0.6
X0 = [MX + i * (PW + PG) for i in range(3)]
BW, BH = 22.0, 6.6
Y_REQ, Y_BAND, Y_SOLV, Y_OUT = 48.5, 32.2, 15.9, 4.3
Y_TITLE = 56.8
TITLES = ["(a) Single agent with tools", "(b) Two-agent pair", "(c) Multi-agent team"]
for x0, t in zip(X0, TITLES):
    ax.text(x0, Y_TITLE, t, ha="left", va="center", fontsize=FS_T, fontweight="bold", color=INK, zorder=6)

# ================================================================== (a) single agent with tools
cx = X0[0] + PW / 2 - 3.2
req = box(cx, Y_REQ, BW, BH, "io", ["Engineering request"])
llm = box(cx, Y_BAND, BW, 9.4, "llm", ["LLM agent", "plans and writes", "script or tool call"])
sol = box(cx, Y_SOLV, BW, BH, "solver", ["Structural solver"])
out = box(cx, Y_OUT, BW, BH, "io", ["Output and messages"])
arrow([(cx, req["b"]), (cx, llm["t"])], BLUE)
arrow([(cx, llm["b"]), (cx, sol["t"])], BLUE)
arrow([(cx, sol["b"]), (cx, out["t"])], BROWN)
xl = out["r"] + 3.6
arrow([(out["r"], out["cy"]), (xl, out["cy"]), (xl, llm["cy"]), (llm["r"], llm["cy"])], GREY)
t = ax.text(xl + 1.9, (out["cy"] + llm["cy"]) / 2, "feedback", rotation=90, ha="center", va="center",
            fontsize=FS_L, color=GREY, zorder=6)

# ================================================================== (b) two-agent pair
cxb = X0[1] + PW / 2
req = box(cxb, Y_REQ, BW, BH, "io", ["Engineering request"])
PWB, GAPB, PBH = 11.8, 6.4, 9.4
xa = X0[1] + (PW - (2 * PWB + GAPB)) / 2 + PWB / 2
xe = xa + PWB + GAPB
asst = box(xa, Y_BAND, PWB, PBH, "llm", ["Assistant", "LLM agent", "writes code"])
exe = box(xe, Y_BAND, PWB, PBH, "llm", ["Executor or", "proxy agent", "runs code"])
sol = box(cxb, Y_SOLV, BW, BH, "solver", ["Structural solver"])
out = box(cxb, Y_OUT, BW, BH, "io", ["Output and error messages"])
arrow([(asst["cx"], req["b"]), (asst["cx"], asst["t"])], BLUE)
yf, yr = Y_BAND + 1.9, Y_BAND - 1.9
arrow([(asst["r"], yf), (exe["l"], yf)], BLUE)
arrow([(exe["l"], yr), (asst["r"], yr)], GREY)
gx = (asst["r"] + exe["l"]) / 2
for txt, y in (("code", yf + 2.2), ("errors", yr - 2.3)):
    t = ax.text(gx, y, txt, ha="center", va="center", fontsize=FS_L, color=GREY, zorder=6)
arrow([(exe["cx"], exe["b"]), (exe["cx"], sol["t"])], BLUE)
arrow([(cxb, sol["b"]), (cxb, out["t"])], BROWN)

# ================================================================== (c) multi-agent team
cxc = X0[2] + PW / 2
req = box(cxc, Y_REQ, BW, BH, "io", ["Engineering request"])
GW = PW - 1.6
gx0, gx1, gy0, gy1 = cxc - GW / 2, cxc + GW / 2, Y_BAND - 8.2, Y_BAND + 8.2
rect(gx0, gy0, gx1, gy1, "none", ACCENT_EDGE, lw=1.0, z=2, ls=(0, (5, 3)))
RW, RG, RH = 8.6, 1.4, 7.8
ry = gy1 - 1.2 - RH / 2
for i, name in enumerate(["Planner", "Modeller", "Reviewer"]):
    box(gx0 + 0.8 + RW / 2 + i * (RW + RG), ry, RW, RH, "llm", [name, "role"])
lines_in(gx0, gy0, gx1, gy1 - 1.2 - RH - 0.5, ["shared conversation and", "mutual correction"],
         fs=FS_L, color=ACCENT_EDGE)
sol = box(cxc, Y_SOLV, BW, BH, "solver", ["Structural solver"])
out = box(cxc, Y_OUT, BW, BH, "io", ["Output and messages"])
arrow([(cxc, req["b"]), (cxc, gy1)], BLUE)
arrow([(cxc, gy0), (cxc, sol["t"])], BLUE)
arrow([(cxc, sol["b"]), (cxc, out["t"])], BROWN)

# ------------------------------------------------------------------ overflow check
fig.canvas.draw()
inv = ax.transData.inverted()
bad = 0
for t, (x0, y0, x1, y1) in checks:
    bb = t.get_window_extent()
    (a0, b0), (a1, b1) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    if a0 < x0 + 0.7 or a1 > x1 - 0.7 or b0 < y0 + 0.3 or b1 > y1 - 0.3:
        bad += 1
        print(f"OVERFLOW {t.get_text()!r} x[{a0:.1f},{a1:.1f}] y[{b0:.1f},{b1:.1f}] in x[{x0:.1f},{x1:.1f}] y[{y0:.1f},{y1:.1f}]")
for t in ax.texts:
    bb = t.get_window_extent()
    (a0, b0), (a1, b1) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    if a0 < 0.2 or a1 > W - 0.2 or b0 < 0.2 or b1 > H - 0.2:
        bad += 1
        print("EDGE", repr(t.get_text()), round(a0, 1), round(a1, 1))
print(f"figure {W * U:.2f} x {H * U:.2f} in ; issues = {bad}")

os.makedirs("out", exist_ok=True)
save(fig, "out/fig_agent_patterns")
