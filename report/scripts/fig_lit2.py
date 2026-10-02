import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from diag import *
import sysrev
from collections import Counter
refs = json.load(open(os.path.join(os.path.dirname(__file__), "..", "data", "refs_master.json")))["refs"]
ROWS = sysrev.ROWS

def evidence_map():
    fig, ax = plt.subplots(1, 3, figsize=(6.8, 2.7), gridspec_kw={"width_ratios": [1.0, 1.0, 1.25]})
    # (a) per theme
    th = Counter(r[0] for r in ROWS); names = ["Biochar in\ncementitious", "RCA and waste\nin paving blocks", "Slip and\nfriction", "LCA and\ncarbon"]
    a = ax[0]; a.barh(range(4)[::-1], [th[k] for k in "ABCD"], 0.6, color=["#86a3ba", "#b99d74", "#9aa0a8", "#7f9f8a"], edgecolor=LINE, zorder=3)
    for i, k in enumerate("ABCD"): a.text(th[k] + 0.2, 3 - i, str(th[k]), va="center", fontsize=7.5)
    a.set_yticks(range(4)[::-1]); a.set_yticklabels(names, fontsize=7); a.set_xlabel("Studies in synthesis table"); a.set_xlim(0, 14); a.xaxis.grid(True, color=GRID, lw=0.5, zorder=0); panel(a, "(a)")
    # (b) by period
    yrs = [refs[r[1]]["year"] for r in ROWS]; bins = [(0, 2015, "≤ 2015"), (2016, 2020, "2016–2020"), (2021, 2023, "2021–2023"), (2024, 2026, "2024–2026")]
    cnt = [sum(1 for y in yrs if lo <= y <= hi) for lo, hi, _ in bins]
    b = ax[1]; b.bar(range(4), cnt, 0.6, color="#cfcbc0", edgecolor=LINE, zorder=3, hatch="..")
    for i, c in enumerate(cnt): b.text(i, c + 0.25, str(c), ha="center", fontsize=7.5)
    b.set_xticks(range(4)); b.set_xticklabels([x[2] for x in bins], fontsize=6.8, rotation=20); b.set_ylabel("Studies"); b.set_ylim(0, 17); b.yaxis.grid(True, color=GRID, lw=0.5, zorder=0); panel(b, "(b)")
    # (c) feature coverage
    c = ax[2]; feats = sysrev.FEATS; counts = [sum(1 for r in ROWS if f in r[5]) for f, _ in feats]
    en = ["Biochar", "RCA", "Paving block", "Slip resistance", "LCA", "Mechanics"]
    c.barh(range(6)[::-1], counts, 0.6, color="white", edgecolor=LINE, hatch="////", zorder=3, label="Other studies")
    c.barh(range(6)[::-1], [1] * 6, 0.6, left=counts, color=ACCENT, edgecolor=LINE, zorder=3, label="This study")
    for i, v in enumerate(counts): c.text(v + 1.2, 5 - i, str(v), va="center", fontsize=7.2)
    c.set_yticks(range(6)[::-1]); c.set_yticklabels(en, fontsize=7); c.set_xlim(0, 22); c.set_xlabel("Studies addressing the topic"); c.legend(loc="lower right", fontsize=6.4); c.xaxis.grid(True, color=GRID, lw=0.5, zorder=0); panel(c, "(c)")
    fig.tight_layout(w_pad=1.0); save(fig, "s_evidence_map")
    return th, cnt, counts

def gap_matrix():
    pick = ["wang2020", "legan2025", "chin2025", "wangx2019", "contreras2022", "rodriguez2017", "namarak2018", "gierasimiuk2021", "pizon2026", "wangd2026", "ambaye2026", "knoeri2013"]
    rows = [r for k in pick for r in ROWS if r[1] == k]
    fig, ax = plt.subplots(figsize=(6.4, 3.9)); n = len(rows) + 1
    feats = sysrev.FEATS; en = ["Biochar", "RCA", "Paving\nblock", "Slip\nresistance", "LCA", "Mechanics\nmodelling"]
    for j in range(len(feats)): ax.axvline(j, color=GRID, lw=0.5, zorder=0)
    labels = []
    for i, r in enumerate(rows):
        y = n - 1 - i
        au = refs[r[1]]["authors"].split(",")[0].split(" and ")[0]; labels.append(f"{au} {refs[r[1]]['year']}")
        for j, (f, _) in enumerate(feats):
            ax.scatter(j, y, s=110, marker="s", facecolor="#6f7e8c" if f in r[5] else "white", edgecolor=LINE, lw=0.9, zorder=3)
    for j in range(len(feats)): ax.scatter(j, 0, s=110, marker="s", facecolor=ACCENT_EDGE, edgecolor=LINE, lw=0.9, zorder=3)
    labels.append("This study"); ax.axhline(0.5, color=LINE, lw=0.8)
    ax.set_yticks(range(n)[::-1]); ax.set_yticklabels(labels, fontsize=7.4); ax.get_yticklabels()[-1].set_fontweight("bold")
    ax.set_xticks(range(len(feats))); ax.set_xticklabels(en, fontsize=7.2); ax.xaxis.tick_top(); ax.set_xlim(-0.5, 5.5); ax.set_ylim(-0.7, n - 0.3)
    ax.tick_params(top=False, right=False)
    from matplotlib.lines import Line2D
    h = [Line2D([], [], marker="s", ls="", mfc="#6f7e8c", mec=LINE, ms=7, label="addressed (per extracted information)"), Line2D([], [], marker="s", ls="", mfc="white", mec=LINE, ms=7, label="not seen in extracted information")]
    ax.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, -0.03), ncol=2, fontsize=6.8, frameon=False)
    fig.tight_layout(); save(fig, "s_gap_matrix")

if __name__ == "__main__":
    print(evidence_map()); gap_matrix()
