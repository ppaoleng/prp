"""Adapted redraw of a published comparison figure (ReAct, Yao et al., ICLR 2023, Fig. 1).

Content (labels, trajectories, highlights) follows the supplied image; only the visual
presentation is redrawn. Trajectory text is monospaced so highlight boxes align exactly.
See notes delivered with the figure for the two label corrections and attribution requirements.
"""
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from fig_style import apply_style, save, INK, INK_SEC, LINE, NEUTRAL_FILL, ACCENT_EDGE

apply_style()
plt.rcParams["svg.fonttype"] = "path"      # keep monospace alignment independent of installed fonts

MONO, SANS = "Liberation Mono", "Liberation Sans"
HL = {"err": "#e9a090", "ok": "#cfe6bf", "think": "#cfdff0"}     # CVD-checked (protan/deutan dE >= ~15)
FAIL, GOOD = "#b4493b", "#3f7d5a"

W = 7.2
FS = 6.4                         # trajectory font size (pt)
CW = 0.6 * FS / 72               # monospace advance (in)
LP = 0.114                       # line pitch (in)
SP = 0.55                        # spacer height as fraction of a line
HDR, PADX, PADY, G = 0.20, 0.07, 0.055, 0.10

# ------------------------------------------------------------------ mini-markup -> runs
# {b:..} bold, {k:..} action keyword (blue), {e:..} error hl, {g:..} correct hl,
# {t:..} reasoning hl, {tk:..} reasoning hl + keyword, {n:..} italic note
TAGS = {"b": dict(bold=1), "k": dict(kw=1), "e": dict(hl="err"), "g": dict(hl="ok"),
        "t": dict(hl="think"), "tk": dict(hl="think", kw=1), "n": dict(note=1)}


def runs(markup):
    out, i = [], 0
    while i < len(markup):
        if markup[i] == "{":
            j = markup.index(":", i)
            tag = markup[i + 1:j]
            k = markup.index("}", j)
            out.append((markup[j + 1:k], tuple(sorted(TAGS[tag].items()))))
            i = k + 1
        else:
            j = markup.find("{", i)
            j = len(markup) if j < 0 else j
            out.append((markup[i:j], ()))
            i = j
    return out


def wrap(rs, width):
    """Greedy word wrap of styled runs (monospace -> width in characters)."""
    toks, cur = [], []
    for text, fl in rs:
        for ch in text:
            if ch == " ":
                if cur:
                    toks.append(("w", cur)); cur = []
                toks.append(("s", [(" ", fl)]))
            elif cur and cur[-1][1] == fl:
                cur[-1] = (cur[-1][0] + ch, fl)
            else:
                cur.append((ch, fl))
    if cur:
        toks.append(("w", cur))
    lines, n = [[]], 0

    def strip_tail():
        nonlocal n
        while lines[-1] and lines[-1][-1][0].strip() == "":
            n -= len(lines[-1][-1][0]); lines[-1].pop()
    for kind, parts in toks:
        L = sum(len(t) for t, _ in parts)
        if kind == "s":
            if n:
                lines[-1].extend(parts); n += 1
        else:
            if n + L > width and n:
                strip_tail(); lines.append([]); n = 0
            lines[-1].extend(parts); n += L
    strip_tail()
    return lines


def block(*paras, width):
    """paras: markup strings, or None for a spacer. Returns list of lines / None."""
    out = []
    for p in paras:
        out.extend([None] if p is None else wrap(runs(p), width))
    return out


def nchars(w):
    return int((w - 2 * PADX) / CW + 1e-6)


def panel_h(lines):
    return HDR + 2 * PADY + sum(SP * LP if ln is None else LP for ln in lines)


# ------------------------------------------------------------------ content
WL, GAP_X = 3.57, 0.10
X0 = 0.03
W1 = 1.70
W2 = WL - W1 - G
XR = X0 + WL + GAP_X
WR = W - 0.03 - XR

q = block("{b:Question:} Aside from the Apple Remote, what other device can control the program "
          "Apple Remote was originally designed to interact with?", width=nchars(WL))
a1 = block("{b:Answer:} iPod", width=nchars(W1))
b1 = block("{b:Thought:} Let's think step by step. {e:Apple Remote was originally designed to interact "
           "with Apple TV. Apple TV can be controlled by iPhone, iPad, and iPod Touch.} "
           "So the answer is iPhone, iPad, and iPod Touch.", None,
           "{b:Answer:} iPhone, iPad, iPod Touch", width=nchars(W1))
c1 = block("{b:Act 1:} {k:Search}[Apple Remote]", "{b:Obs 1:} The Apple Remote is a remote control …", None,
           "{b:Act 2:} {k:Search}[Front Row]", "{b:Obs 2:} Could not find [Front Row]. Similar: …", None,
           "{b:Act 3:} {k:Search}[{g:Front Row (software)}]",
           "{b:Obs 3:} Front Row is a discontinued media center software …", None,
           "{b:Act 4:} {k:Finish}[{e:yes}]", width=nchars(W2))
d1 = block("{b:Thought 1:} I need to search Apple Remote and find the program it was originally designed "
           "to interact with.",
           "{b:Act 1:} {k:Search}[Apple Remote]",
           "{b:Obs 1:} The Apple Remote is a remote control introduced in October 2005 by Apple … "
           "originally designed to control the {g:Front Row media center} program …", None,
           "{b:Thought 2:} Apple Remote was originally designed to control the Front Row media center "
           "program. I need to search {g:Front Row} next and find what other device can control it.",
           "{b:Act 2:} {k:Search}[Front Row]",
           "{b:Obs 2:} Could not find [Front Row]. Similar: ['Front Row Seat to Earth', "
           "'Front Row Motorsports', '{g:Front Row (software)}', …]", None,
           "{b:Thought 3:} Front Row is not found. I need to search {g:Front Row (software)}.",
           "{b:Act 3:} {k:Search}[{g:Front Row (software)}]",
           "{b:Obs 3:} Front Row is a discontinued media center software …", None,
           "{b:Thought 4:} {g:Front Row (software) is controlled by an Apple Remote or the keyboard "
           "function keys.} So the answer is keyboard function keys.",
           "{b:Act 4:} {k:Finish}[{g:keyboard function keys}]", width=nchars(WR))
d2 = block("You are in the middle of a room. Looking quickly around you, you see a cabinet 6, a cabinet 1, "
           "a coffee machine 1, a countertop 3, a stove burner 1, and a toaster 1. "
           "{b:Your task is to:} Put some pepper shaker on a drawer.", width=nchars(WL))
a2 = block("{b:Act 1:} Go to drawer 1", "{b:Obs 1:} The drawer 1 is closed.", None,
           "{b:Act 2:} Open drawer 1",
           "{b:Obs 2:} You open the drawer 1. The drawer 1 is open. In it, you see a dishsponge 2, "
           "and a spoon 1.", None,
           "{b:Act 3:} Go to sinkbasin 1",
           "{b:Obs 3:} On the sinkbasin 1, you see a dishsponge 3, a spatula 1, and a spoon 2.", None,
           "{b:Act 4:} Take peppershaker 1 from sinkbasin 1", "{b:Obs 4:} {e:Nothing happens.}", None,
           "{b:Act 5:} {e:Take peppershaker 1 from sinkbasin 1}", "{b:Obs 5:} {e:Nothing happens.}",
           width=nchars(WL))
b2 = block("{b:Act 1:} {tk:Think}{t:[First I need to find a pepper shaker…more likely to appear in "
           "cabinets (1-6), countertops (1-3), … ]}",
           "{b:Act 2:} Go to cabinet 1", "{b:Obs 2:} On the cabinet 1, you see a vase 2.",
           "{n:(Here the agent goes to cabinet 1, then cabinet 2, 3, then countertop 1 and 2)}",
           "{b:Act 6:} Go to countertop 3",
           "{b:Obs 6:} On the countertop 3, you see a apple 1, a bread 1, … a pepper shaker 1, "
           "and a vase 3.", None,
           "{b:Act 7:} Take pepper shaker 1 from countertop 3",
           "{b:Obs 7:} You pick up the pepper shaker 1 from the countertop 3.", None,
           "{b:Act 8:} {tk:Think}{t:[Now I find a pepper shaker 1. Next, I need to put it in/on drawer 1. ]}",
           "{b:Act 9:} Go to drawer 1", "{b:Obs 9:} Drawer 1 is closed.", None,
           "{b:Act 10:} Open drawer 1", "{b:Obs 10:} You open Drawer 1 …", None,
           "{b:Act 11:} Put pepper shaker 1 in/on drawer 1",
           "{b:Obs 11:} {g:You put pepper shaker 1 in/on the drawer 1.}", width=nchars(WR))

# ------------------------------------------------------------------ vertical layout
Y0 = 0.03
hq, h1a, h1b, h1c, h1d = (panel_h(x) for x in (q, a1, b1, c1, d1))
y_sub = Y0 + hq + G
row1_bot = max(y_sub + max(h1a + G + h1b, h1c), Y0 + h1d)
SEP = 0.26
Y1 = row1_bot + SEP
h2, h2a, h2b = (panel_h(x) for x in (d2, a2, b2))
y_sub2 = Y1 + h2 + G
row2_bot = max(y_sub2 + h2a, Y1 + h2b)
LEG_Y = row2_bot + 0.13
H = LEG_Y + 0.17

fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.axis("off")


# ------------------------------------------------------------------ drawing
def mark(kind, x, y, s=0.042):
    if kind == "fail":
        for d in (1, -1):
            ax.plot([x - s, x + s], [y - d * s, y + d * s], color=FAIL, lw=1.7, solid_capstyle="butt", zorder=7)
    else:
        ax.plot([x - s * 1.1, x - s * 0.25, x + s * 1.2], [y + 0.0, y + s * 0.95, y - s * 0.95],
                color=GOOD, lw=1.7, solid_capstyle="butt", solid_joinstyle="miter", zorder=7)


def draw_line(x, ytop, line):
    col = 0
    # highlights first (merged contiguous runs)
    run_hl = []
    for text, fl in line:
        run_hl.append((col, col + len(text), dict(fl).get("hl")))
        col += len(text)
    i = 0
    while i < len(run_hl):
        a, b, h = run_hl[i]
        if h:
            j = i
            while j + 1 < len(run_hl) and run_hl[j + 1][2] == h:
                j += 1
            b = run_hl[j][1]
            ax.add_patch(Rectangle((x + a * CW, ytop + 0.004), (b - a) * CW, LP - 0.008,
                                   facecolor=HL[h], edgecolor="none", zorder=3))
            i = j + 1
        else:
            i += 1
    col = 0
    base = ytop + LP / 2 + 0.33 * FS / 72
    for text, fl in line:
        f = dict(fl)
        color = ACCENT_EDGE if f.get("kw") else (INK_SEC if f.get("note") else INK)
        ax.text(x + col * CW, base, text, ha="left", va="baseline", fontsize=FS, family=MONO,
                fontweight="bold" if f.get("bold") else "normal",
                fontstyle="italic" if f.get("note") else "normal", color=color, zorder=5)
        col += len(text)


def panel(x, y0, w, y1, title, lines, outcome=None):
    ax.add_patch(Rectangle((x, y0), w, y1 - y0, facecolor="white", edgecolor=LINE, linewidth=0.8, zorder=2))
    ax.add_patch(Rectangle((x, y0), w, HDR, facecolor=NEUTRAL_FILL, edgecolor=LINE, linewidth=0.8, zorder=2))
    ax.text(x + PADX, y0 + HDR / 2, title, ha="left", va="center_baseline", fontsize=7.6, family=SANS,
            fontweight="bold", color=INK, zorder=6)
    if outcome:
        mark(outcome, x + w - 0.13, y0 + HDR / 2)
    y = y0 + HDR + PADY
    for ln in lines:
        if ln is None:
            y += SP * LP
        else:
            draw_line(x + PADX, y, ln)
            y += LP


# row 1
panel(X0, Y0, WL, Y0 + hq, "(1) HotpotQA", q)
panel(X0, y_sub, W1, y_sub + h1a, "(1a) Standard", a1, "fail")
panel(X0, y_sub + h1a + G, W1, row1_bot, "(1b) CoT (Reason Only)", b1, "fail")
panel(X0 + W1 + G, y_sub, W2, row1_bot, "(1c) Act-Only", c1, "fail")
panel(XR, Y0, WR, row1_bot, "(1d) ReAct (Reason + Act)", d1, "ok")
# separator
ax.plot([0.03, W - 0.03], [row1_bot + SEP / 2] * 2, color=INK_SEC, lw=0.8, linestyle=(0, (5, 3)), zorder=1)
# row 2
panel(X0, Y1, WL, Y1 + h2, "(2) ALFWorld", d2)
panel(X0, y_sub2, WL, row2_bot, "(2a) Act-Only", a2, "fail")
panel(XR, Y1, WR, row2_bot, "(2b) ReAct (Reason + Act)", b2, "ok")

# ------------------------------------------------------------------ legend
lx, ly = X0, LEG_Y + 0.085
for key, label in [("err", "Erroneous or failed step"), ("ok", "Correct or key step"), ("think", "Reasoning (Think)")]:
    ax.add_patch(Rectangle((lx, ly - 0.045), 0.17, 0.09, facecolor=HL[key], edgecolor="none", zorder=3))
    t = ax.text(lx + 0.23, ly, label, ha="left", va="center_baseline", fontsize=7.0, family=SANS, color=INK)
    fig.canvas.draw()
    lx = ax.transData.inverted().transform((t.get_window_extent().x1, 0))[0] + 0.22
for kind, label in [("fail", "Failure"), ("ok", "Success")]:
    mark(kind, lx + 0.05, ly, s=0.036)
    t = ax.text(lx + 0.16, ly, label, ha="left", va="center_baseline", fontsize=7.0, family=SANS, color=INK)
    fig.canvas.draw()
    lx = ax.transData.inverted().transform((t.get_window_extent().x1, 0))[0] + 0.22

# ------------------------------------------------------------------ overflow check (text vs. panel width)
inv = ax.transData.inverted()
bad = 0
fig.canvas.draw()
for t in ax.texts:
    bb = t.get_window_extent()
    (a0, _), (a1_, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    if a1_ > W - 0.02 or a0 < 0.02:
        bad += 1
        print("EDGE:", repr(t.get_text()), round(a0, 2), round(a1_, 2))
# per-panel: every mono text must end inside its panel's right edge
panels = [(X0, WL), (X0, W1), (X0 + W1 + G, W2), (XR, WR)]
for t in ax.texts:
    if t.get_fontfamily()[0] != MONO:
        continue
    bb = t.get_window_extent()
    (a0, _), (a1_, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    ok = any(px <= a0 + 1e-6 and a1_ <= px + pw - PADX / 2 + 1e-6 for px, pw in panels)
    if not ok:
        bad += 1
        print("OVERFLOW:", repr(t.get_text()), round(a0, 2), round(a1_, 2))
print(f"figure {W:.2f} x {H:.2f} in ; chars/line: 1b={nchars(W1)} 1c={nchars(W2)} 1d={nchars(WR)} ; issues = {bad}")

os.makedirs("out", exist_ok=True)
save(fig, "out/fig_react_prompting")
