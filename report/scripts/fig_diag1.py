import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from diag import *

# =========== Research flowchart (Fig 3-1) ===========
def flow_method():
    fig, ax = canvas(6.7, 7.9, 100, 118)
    cur = [117.0]
    def group(no, th, en, inner_h, fc="paper", head=6.2):
        top = cur[0]; hgt = head + inner_h + 1.6; y0 = top - hgt
        box(ax, 6, y0, 88, hgt, fc=fc)
        label(ax, 8.2, top - 3.2, f"{no}.", 8.4, "left", "center", INK, EN, "bold")
        label(ax, 12.0, top - 3.2, th, 8.2, "left", "center", INK, TH, "bold")
        label(ax, 92, top - 3.2, en, 6.4, "right", "center", INK_SEC, EN)
        cur[0] = y0
        return y0 + 1.0, inner_h - 0.0          # inner boxes start at y0+1.0 (height inner_h)
    def gap(g=3.2):
        arrow(ax, 50, cur[0], 50, cur[0] - g); cur[0] -= g
    # 1
    y, h = group(1, "ทบทวนวรรณกรรมและวิเคราะห์ช่องว่างงานวิจัย", "Literature review and gap analysis", 3.4, "gray")
    label(ax, 50, y + 1.7, "ไบโอชาร์ในวัสดุซีเมนต์  ·  คอนกรีตรีไซเคิล (RCA)  ·  คอนกรีตบล็อกปูพื้น  ·  ความต้านทานการลื่นไถล  ·  LCA", 6.6, "center", "center", INK_SEC, THL)
    gap()
    # 2
    y, h = group(2, "เตรียมวัสดุ", "Materials", 9.0)
    mats = [("ปูนซีเมนต์\nปอร์ตแลนด์ประเภท 1", "OPC Type I"), ("ทราย\n(ผ่านตะแกรงเบอร์ 4)", "Fine aggregate"), ("หินเกล็ด", "Crushed stone"),
            ("เศษคอนกรีต (RCA)\n0.30–2.36 มม.", "Lab-waste concrete"), ("ถ่านชีวภาพไม้ไผ่\n(เบอร์ 100 / 200)", "Bamboo biochar")]
    for i, (t, e) in enumerate(mats):
        fcc = "warm" if i == 3 else ("blue" if i == 4 else "white")
        box(ax, 8 + i * 17.2, y, 16, h, [L(t, 6.3), LE(e, 5.5)], fc=fcc, lw=0.7)
    gap()
    # 3
    y, h = group(3, "ออกแบบอัตราส่วนผสม (ซีเมนต์ : ทราย : หิน)", "Mix design", 10.0)
    box(ax, 8, y, 41, h, [L("ชุดที่ 1  ·  RCA 50% ของมวลรวมละเอียด", 6.7, "bold"), L("ลดซีเมนต์ด้วยไบโอชาร์ 5–25 %", 6.5), LE("designed 5–25 %; tested 0–15 %", 5.6)], fc="blue", lw=0.7)
    box(ax, 51, y, 41, h, [L("ชุดที่ 2  ·  ไบโอชาร์คงที่ 48 ก.", 6.7, "bold"), L("RCA แทนทราย 0, 5, 10, 15 %", 6.5), LE("constant biochar; RCA 0–15 %", 5.6)], fc="warm", lw=0.7)
    gap()
    # 4
    y, h = group(4, "ผสม ขึ้นรูป และบ่ม", "Mixing, forming and curing", 8.0)
    for i, (t, e) in enumerate([("ผสมด้วยเครื่องผสมมอร์ตาร์", "mechanical mixing"), ("อัดขึ้นรูปบล็อกคดกริช หนา 6 ซม.", "hand-tamped zig-zag block"), ("บ่ม 7 · 14 · 28 วัน", "3 blocks per age")]):
        box(ax, 8 + i * 28.9, y, 27.5, h, [L(t, 6.4), LE(e, 5.6)], fc="white", lw=0.7)
    gap()
    # 5
    y, h = group(5, "ทดสอบสมบัติของบล็อก", "Testing", 10.4)
    tests = [("ความหนาแน่น", "Density"), ("กำลังต้านทานแรงอัด", "Compressive strength\n(TIS 827-2565)"), ("การดูดซึมน้ำ 72 ชม.", "Water absorption"), ("ความต้านทาน\nการลื่นไถล (BPT)", "Slip resistance, dry / wet")]
    for i, (t, e) in enumerate(tests):
        fcc = "green" if i == 3 else "white"
        box(ax, 8 + i * 21.7, y, 20.6, h, [L(t, 6.4, "bold" if i == 3 else "normal"), LE(e, 5.5)], fc=fcc, lw=0.7)
    gap()
    # 6
    y, h = group(6, "วิเคราะห์ผลและประเมินวัฏจักรชีวิตเบื้องต้น (LCA)", "Analysis and screening LCA", 8.0)
    for i, (t, e) in enumerate([("สถิติ ANOVA / Tukey", "statistics"), ("แบบจำลองกลศาสตร์วัสดุ", "porosity–strength, maturity"), ("GWP ต่อ 1 ลบ.ม. และ ci", "cradle-to-gate")]):
        box(ax, 8 + i * 28.9, y, 27.5, h, [L(t, 6.4), LE(e, 5.6)], fc="white", lw=0.7)
    gap()
    box(ax, 6, cur[0] - 8.4, 88, 8.4, [L("สรุปสูตรที่เหมาะสม เปรียบเทียบเกณฑ์มาตรฐานและงานวิจัยอื่น และข้อเสนอแนะ", 7.2, "bold", "white"), LE("Optimum mix · benchmarking · recommendations", 5.8, "normal", "#d9dde2")], fc="dblue", ec="#1d374a")
    ax.set_ylim(cur[0] - 9.5, 118)
    save(fig, "s_flow_method")

# =========== Conceptual framework (Ch.1) ===========
def framework():
    fig, ax = canvas(6.7, 4.5, 100, 67)
    # left: waste streams
    label(ax, 14, 63.5, "วัสดุเหลือทิ้ง", 8.2, wt="bold"); label(ax, 14, 60.6, "Waste streams", 6.4, fam=EN, color=INK_SEC)
    box(ax, 2, 41, 24, 15.5, [L("เศษไม้ไผ่ / ชีวมวล", 7.2, "bold"), L("ไพโรไลซิส 400–900 °C", 6.4), LE("pyrolysis", 5.8), L("ได้ถ่านชีวภาพ (biochar)", 6.6, "bold")], fc="blue")
    box(ax, 2, 20, 24, 15.5, [L("เศษคอนกรีตจากห้องปฏิบัติการ", 6.8, "bold"), L("บด · ร่อน 0.30–2.36 มม.", 6.4), LE("crushing and sieving", 5.8), L("ได้มวลรวมรีไซเคิล (RCA)", 6.6, "bold")], fc="warm")
    # center: block
    label(ax, 50, 63.5, "คอนกรีตบล็อกปูพื้น", 8.2, wt="bold"); label(ax, 50, 60.6, "Zig-zag paving block (60 mm)", 6.4, fam=EN, color=INK_SEC)
    ax.add_patch(Rectangle((36, 22), 28, 34, facecolor="white", edgecolor=LINE, lw=1.0, zorder=3))
    for k, (t, e, yy, fcc) in enumerate([("ซีเมนต์ (ลด 5–25 %)", "cement reduced · Series I", 49, "blue"), ("ทราย (แทนด้วย RCA 5–50 %)", "sand partly replaced", 41, "warm"), ("หิน · น้ำ · ผสมและอัดแรงคน", "stone, water, hand tamping", 33, "gray")]):
        box(ax, 38, yy - 3.5, 24, 7.6, [L(t, 6.6, "bold"), LE(e, 5.6)], fc=fcc, lw=0.6, zorder=5)
    label(ax, 50, 26.2, "ชุดที่ 1 และ 2  ·  7 · 14 · 28 วัน", 6.5, color=INK_SEC)
    arrow(ax, 26, 49, 36, 49); arrow(ax, 26, 28, 36, 40)
    # right: outcomes
    label(ax, 86, 63.5, "ผลลัพธ์ที่ประเมิน", 8.2, wt="bold"); label(ax, 86, 60.6, "Outcomes evaluated", 6.4, fam=EN, color=INK_SEC)
    outs = [("สมบัติกล", "ความหนาแน่น · กำลังอัด", 51.5), ("สมบัติกายภาพ", "การดูดซึมน้ำ", 43), ("ความปลอดภัย", "ต้านทานการลื่นไถล (BPN)", 34.5), ("สิ่งแวดล้อม", "LCA: GWP · ci", 26)]
    for t, e, yy in outs:
        box(ax, 72, yy - 3.8, 26, 8.2, [L(t, 6.9, "bold"), L(e, 6.2)], fc="green", lw=0.7)
        arrow(ax, 64, 39, 72, yy, lw=0.6)
    # bottom SDG strip
    ax.add_patch(Rectangle((2, 2), 96, 12.5, facecolor="#f4f2ec", edgecolor=LINE, lw=0.8, zorder=2))
    label(ax, 4, 11, "สอดคล้องกับ SDGs", 7.2, "left", wt="bold")
    for i, (n, t) in enumerate([("SDG 9", "นวัตกรรมและโครงสร้างพื้นฐาน"), ("SDG 12", "การผลิตและบริโภคอย่างยั่งยืน"), ("SDG 13", "การรับมือสภาพภูมิอากาศ")]):
        box(ax, 30 + i * 22.6, 4.2, 21.4, 8.4, [L(n, 7.0, "bold", INK, EN), L(t, 5.5, "normal", INK_SEC)], fc="white", lw=0.7, zorder=4)
    save(fig, "s_framework")

if __name__ == "__main__":
    flow_method(); framework()
