"""Graphical summary and SDG infographic (numbers are pulled from the data layer, not typed)."""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from diag import *
import rnum
N = rnum.load()

def minibars(ax, x0, y0, w, h, vals, labels, vmax, cols, lines=(), fmt="{:.1f}", fs=5.6, labfs=5.3, ph=False):
    n = len(vals); bw = w / (n * 1.5 + 0.5); gap = bw * 0.5
    ax.plot([x0, x0 + w], [y0, y0], color=LINE, lw=0.7, zorder=3)
    for i, (v, l, c) in enumerate(zip(vals, labels, cols)):
        x = x0 + gap + i * (bw + gap); bh = max(v, 0) / vmax * h
        ax.add_patch(Rectangle((x, y0), bw, bh, facecolor=c, edgecolor=LINE, lw=0.6, zorder=4))
        ax.text(x + bw / 2, y0 + bh + 0.7, fmt.format(v), ha="center", va="bottom", fontsize=fs, family=EN, color=RED_PH if ph else INK, fontweight="bold" if ph else "normal", zorder=6)
        ax.text(x + bw / 2, y0 - 0.8, l, ha="center", va="top", fontsize=labfs, family=EN, color=INK_SEC, zorder=6)
    for v, t, ls_ in lines:
        yy = y0 + v / vmax * h
        ax.plot([x0, x0 + w], [yy, yy], color=INK_SEC, lw=0.7, ls=ls_, zorder=5)
        ax.text(x0 + w, yy + 0.5, t, ha="right", va="bottom", fontsize=4.9, family=EN, color=INK_SEC, zorder=6)

def card(ax, x, y, w, h, title, sub=None, fc="white"):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=FILL.get(fc, fc), edgecolor=LINE, lw=0.8, zorder=2))
    label(ax, x + 1.5, y + h - 2.6, title, 7.0, "left", wt="bold")
    if sub: label(ax, x + 1.5, y + h - 5.3, sub, 5.2, "left", color=INK_SEC, fam=EN)

def summary():
    fig, ax = canvas(6.7, 5.5, 100, 82)
    # inputs
    box(ax, 1.5, 68, 22, 12, [L("ไม้ไผ่เหลือทิ้ง", 6.6, "bold"), L("ไพโรไลซิส เป็นถ่านชีวภาพ", 5.6, "normal", INK_SEC, THL), L("ทดแทนซีเมนต์ 5–15 %", 5.4, "normal", INK_SEC, THL)], fc="green")
    box(ax, 1.5, 53, 22, 12, [L("เศษคอนกรีตเหลือทิ้ง", 6.6, "bold"), L("บดย่อยเป็น RCA", 5.6, "normal", INK_SEC, THL), L("แทนทราย 0–15 % / มวลรวมละเอียด 50 %", 5.0, "normal", INK_SEC, THL)], fc="warm")
    arrow(ax, 23.5, 74, 28, 68, lw=0.9); arrow(ax, 23.5, 59, 28, 66, lw=0.9)
    box(ax, 28, 59, 18, 17, [L("คอนกรีตบล็อก\nปูพื้นรูปคดกริช", 6.6, "bold"), L("อายุ 7 · 14 · 28 วัน", 5.4, "normal", INK_SEC, THL), L("2 ชุดทดลอง · 9 สูตร", 5.4, "normal", INK_SEC, THL)], fc="blue")
    # card 1: S1 strength
    card(ax, 50, 50, 24, 30, "กำลังอัด 28 วัน ชุดที่ 1", "MPa · biochar replaces cement")
    mix1 = ["RA", "Rab5", "Rab10", "Rab15"]
    minibars(ax, 52, 58, 20, 16, [N[f"fc28_{m}"] for m in mix1], ["RA", "5%", "10%", "15%"], 70, [MIXCOL[m] for m in mix1], lines=[(35, "35", "--"), (50, "50", "-.")], fmt="{:.0f}")
    # card 2: S2 strength
    card(ax, 75.5, 50, 23, 30, "กำลังอัด 28 วัน ชุดที่ 2", "MPa · RCA replaces sand")
    mix2 = ["RCA0", "RCA5", "RCA10", "RCA15"]
    minibars(ax, 77, 58, 19.5, 16, [N[f"fc28_{m}"] for m in mix2], ["0%", "5%", "10%", "15%"], 70, [MIXCOL[m] for m in mix2], lines=[(35, "35", "--"), (50, "50", "-.")], fmt="{:.0f}")
    # card 3: physical
    card(ax, 1.5, 24, 30, 24, "สมบัติกายภาพ (ค่าที่วัด)", None)
    label(ax, 3, 39.2, f"{N['rho_all_Rab15']:,.0f}–{N['rho_all_NA']:,.0f}", 9.0, "left", wt="bold", fam=EN); label(ax, 3, 35.2, "ความหนาแน่น กก./ม.³ (ชุดที่ 1) ลดตามการเติมไบโอชาร์", 5.2, "left", color=INK_SEC, fam=THL)
    label(ax, 3, 30.2, "0.3–2.7 %", 9.0, "left", wt="bold", fam=EN); label(ax, 3, 26.4, "การดูดซึมน้ำ 72 ชม. ต่ำกว่าเกณฑ์ 5 % ทุกค่า", 5.2, "left", color=INK_SEC, fam=THL)
    # card 4: slip placeholder
    card(ax, 33, 24, 30, 24, "ความต้านทานการลื่นไถล", None)
    label(ax, 48, 37.5, "[Place Holder]", 10.0, wt="bold", color=RED_PH, fam=EN)
    label(ax, 48, 31.5, "ยังไม่มีผลวัดจริง\nแสดงเฉพาะกรอบวิเคราะห์", 5.4, color=INK_SEC, fam=THL)
    label(ax, 48, 26.7, "BPN เปียก/แห้ง · เกณฑ์ 45 / 60 ยังไม่ยืนยัน", 5.0, color=RED_PH, fam=THL)
    # card 5: carbon
    card(ax, 64.5, 2, 34, 46, "GWP เบื้องต้น (kg CO2e/ม.³)", "cradle-to-gate · screening")
    mix = ["RA", "Rab5", "Rab10", "Rab15"]
    minibars(ax, 67, 24, 13.5, 12, [N[f"gwpA_{m}"] for m in mix], ["RA", "5", "10", "15"], 330, [MIXCOL[m] for m in mix], fmt="{:.0f}", fs=5.2)
    minibars(ax, 83, 24, 13.5, 12, [N[f"gwpB_{m}"] for m in mix], ["RA", "5", "10", "15"], 330, [MIXCOL[m] for m in mix], fmt="{:.0f}", fs=5.2)
    label(ax, 73.8, 19.6, "กรณี A ไม่หักเครดิต", 5.4, fam=THL); label(ax, 89.8, 19.6, "กรณี B หักเครดิต*", 5.4, fam=THL)
    label(ax, 81.5, 12.2, f"ซีเมนต์ = {N['share_min']:.0f}–{N['share_max']:.0f} % ของ GWP", 5.8, wt="bold", fam=THL)
    label(ax, 81.5, 6.2, "*ตัวประกอบสมมติ [Place Holder]", 5.0, color=RED_PH, fam=THL)
    # recommendation
    ax.add_patch(Rectangle((1.5, 2), 61, 20, facecolor="#e0e8e1", edgecolor=LINE, lw=0.8, zorder=2))
    label(ax, 3, 19.0, "สูตรที่แนะนำจากผลที่วัดได้", 7.0, "left", wt="bold")
    rec = [("งานทั่วไป มอก. 827-2565", "ชุดที่ 1 ลดซีเมนต์ได้ถึง 15 % (≥ 35 MPa)"), ("งานหนัก มอก. 2035-2565", "ชุดที่ 1 ไม่เกิน 5 % (≥ 50 MPa) หรือ ชุดที่ 2 RCA 10–15 %"), ("ต้องยืนยันก่อนใช้", "BPN จริง · ดูดซึมน้ำที่ผิดปกติ · วัสดุตั้งต้น")]
    for i, (a, b) in enumerate(rec):
        label(ax, 3, 14.2 - i * 4.4, a, 5.8, "left", wt="bold", color=RED_PH if i == 2 else INK, fam=THL); label(ax, 24, 14.2 - i * 4.4, b, 5.5, "left", color=INK_SEC, fam=THL)
    save(fig, "s_summary")

def sdg():
    fig, ax = canvas(6.7, 3.6, 100, 53.7)
    inv = N["inv"]; res = N["lca"]
    cols = [("SDG 9", "อุตสาหกรรม นวัตกรรม และโครงสร้างพื้นฐาน", "green",
             f"{N['fc28_Rab15']:.0f}–{N['fc28_RCA15']:.0f}", "MPa", "กำลังอัด 28 วันของบล็อก RCA + ไบโอชาร์\nผ่านเกณฑ์ 35 MPa ทุกสูตร",
             "ผ่านเกณฑ์งานหนัก (50 MPa):\nNA, RA, Rab5% และชุดที่ 2 ทุกสูตร"),
            ("SDG 12", "การผลิตและการบริโภคอย่างยั่งยืน", "warm",
             f"{inv.loc['RA','rca']:.0f}", "กก./ม.³", "RCA ในสูตร RA ต่อบล็อก 1 ลบ.ม.\n(ร้อยละ " + f"{res.loc['RA','recycled_share_pct']:.0f} ของมวลวัสดุ)",
             f"ไบโอชาร์ {inv.loc['Rab5','biochar']:.0f}–{inv.loc['Rab15','biochar']:.0f} กก./ม.³ จากชีวมวลเหลือทิ้ง\nที่ระดับ Rab5–15%"),
            ("SDG 13", "การรับมือการเปลี่ยนแปลงสภาพภูมิอากาศ", "blue",
             f"{abs(res.loc['Rab5','gwp_A_vs_ctrl_pct']):.1f}–{abs(res.loc['Rab15','gwp_A_vs_ctrl_pct']):.1f}", "% ลดลง", "GWP กรณี A เมื่อซีเมนต์ลด 5–15 %\n(ไม่หักเครดิตคาร์บอน)",
             f"กรณี B (หักเครดิต ค่าสมมติ)\nลดได้ถึง {abs((res.loc['Rab15','gwp_B']/res.loc['RA','gwp_B']-1)*100):.0f} % ที่ Rab15%")]
    w = 31; gapw = 2.5
    for i, (s, t, fc, big, unit, d1, d2) in enumerate(cols):
        x = 1.5 + i * (w + gapw)
        ax.add_patch(Rectangle((x, 6), w, 44, facecolor=FILL[fc], edgecolor=LINE, lw=0.8, zorder=2))
        ax.add_patch(Rectangle((x, 40), w, 10, facecolor=FILL["dblue"] if i != 1 else FILL["dwarm"], edgecolor=LINE, lw=0.8, zorder=3))
        label(ax, x + 2, 46.2, s, 8.6, "left", wt="bold", color="white", fam=EN); label(ax, x + 2, 42.4, t, 4.7, "left", color="white", fam=THL)
        label(ax, x + w / 2 - 2.5, 33.5, big, 11.0 if len(big) < 9 else 9.0, wt="bold", fam=EN)
        ax.text(x + w / 2 + (len(big) * 1.15 if len(big) < 9 else 9.5), 33.2, unit, fontsize=6.4, family=THL, color=INK_SEC, va="center", ha="left", zorder=8)
        label(ax, x + w / 2, 24.6, d1, 5.3, color=INK, fam=THL)
        ax.plot([x + 3, x + w - 3], [18.4, 18.4], color=GRID, lw=0.8, zorder=3)
        label(ax, x + w / 2, 12.6, d2, 5.2, color=INK_SEC, fam=THL)
    ax.text(50, 2.4, "ตัวเลขเป็นผลทดสอบในห้องปฏิบัติการหรือการคำนวณเบื้องต้น ไม่ใช่ผลกระทบเชิงระบบ  ·  ค่า GWP ใช้ตัวประกอบสมมติ [Place Holder]", ha="center", fontsize=5.0, family=THL, color=RED_PH)
    save(fig, "s_sdg_impact")

if __name__ == "__main__":
    summary(); sdg()
