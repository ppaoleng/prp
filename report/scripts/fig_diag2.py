import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from diag import *

def cycle():
    fig, ax = canvas(6.7, 4.9, 100, 73)
    cx, cy, rx, ry = 50, 36, 33, 25
    nodes = [("ชีวมวลเหลือทิ้ง", "ไม้ไผ่ · เศษเกษตร", "Biomass residues", 90, "green"),
             ("ไพโรไลซิส", "400–900 °C ไร้ออกซิเจน", "Pyrolysis", 30, "gray"),
             ("ถ่านชีวภาพ", "กักเก็บคาร์บอนระยะยาว", "Biochar", -30, "blue"),
             ("วัสดุก่อสร้าง", "ซีเมนต์ · คอนกรีต · บล็อก", "Construction materials", -90, "paper"),
             ("ใช้งานและรื้อถอน", "เศษคอนกรีตเหลือทิ้ง", "Service life and demolition", -150, "warm"),
             ("รีไซเคิล", "บด คัดขนาด เป็น RCA", "Recycling", 150, "warm")]
    patches = []
    for t, s, e, ang, fc in nodes:
        x = cx + rx * np.cos(np.radians(ang)); y = cy + ry * np.sin(np.radians(ang))
        patches.append(box(ax, x - 13, y - 6, 26, 12, [L(t, 7.4, "bold"), L(s, 6.0), LE(e, 5.6)], fc=fc, lw=0.8, zorder=4))
    cen = [(cx + rx * np.cos(np.radians(n[3])), cy + ry * np.sin(np.radians(n[3]))) for n in nodes]
    for i in range(6):
        j = (i + 1) % 6
        arrow(ax, cen[i][0], cen[i][1], cen[j][0], cen[j][1], lw=1.0, ms=8, conn="arc3,rad=-0.18", patchA=patches[i], patchB=patches[j], zorder=3)
    box(ax, 34, 29, 32, 14, [L("เศรษฐกิจหมุนเวียน", 8.0, "bold"), L("และความเป็นกลางทางคาร์บอน", 7.0), LE("Circular economy · carbon neutrality", 5.8)], fc="white", lw=0.8, zorder=4, ls="--")
    save(fig, "s_biochar_cycle")

def pyrolysis():
    fig, ax = canvas(6.7, 4.2, 100, 62.7)
    label(ax, 12, 58.5, "วัตถุดิบชีวมวล", 7.6, wt="bold"); label(ax, 12, 55.7, "Feedstock", 6, fam=EN, color=INK_SEC)
    feeds = ["ไม้ไผ่", "เศษไม้ · เปลือกไม้", "ซังข้าวโพด · แกลบ", "ชานอ้อย", "กะลาปาล์ม"]
    for i, f in enumerate(feeds):
        box(ax, 2, 44 - i * 9.4, 20, 7.4, [L(f, 6.6)], fc="green", lw=0.7)
        arrow(ax, 22, 47.7 - i * 9.4, 30, 33, lw=0.5)
    label(ax, 52, 58.5, "กระบวนการเปลี่ยนรูป", 7.6, wt="bold"); label(ax, 52, 55.7, "Thermochemical routes", 6, fam=EN, color=INK_SEC)
    routes = [("ไพโรไลซิส", "Pyrolysis", "400–900 °C · ไร้ออกซิเจน", 41.5, "blue"), ("แก๊สซิฟิเคชัน", "Gasification", "ออกซิเจนจำกัด", 28, "gray"), ("คาร์บอไนเซชันด้วยไฮโดรเทอร์มัล (HTC)", "Hydrothermal carbonisation", "ชีวมวลเปียก · ความดัน", 14.5, "gray")]
    for t, e, s, y, fc in routes:
        box(ax, 30, y - 5, 44, 11, [L(t, 6.9, "bold"), LE(e, 5.6), L(s, 6.0)], fc=fc, lw=0.8)
        arrow(ax, 74, y, 80, y, lw=0.8)
    label(ax, 90, 58.5, "ผลิตภัณฑ์", 7.6, wt="bold"); label(ax, 90, 55.7, "Products", 6, fam=EN, color=INK_SEC)
    box(ax, 80, 36.5, 19, 11, [L("ถ่านชีวภาพ", 7.0, "bold"), LE("Biochar (solid)", 5.8)], fc="#c8d3dc", lw=0.9)
    box(ax, 80, 23, 19, 11, [L("น้ำมันชีวภาพ", 6.6), LE("Bio-oil (liquid)", 5.6)], fc="white", lw=0.7)
    box(ax, 80, 9.5, 19, 11, [L("แก๊สสังเคราะห์", 6.6), LE("Syngas (gas)", 5.6)], fc="white", lw=0.7)
    ax.add_patch(Rectangle((2, 0.8), 96, 4.8, facecolor="#f4f2ec", edgecolor=LINE, lw=0.7, zorder=2))
    label(ax, 50, 3.2, "ปัจจัยควบคุม: อุณหภูมิ · อัตราการให้ความร้อน · ระยะเวลา · ความดัน · ชนิดวัตถุดิบ  กำหนดขนาดรูพรุน พื้นที่ผิว และความสามารถดูดซับน้ำ", 6.2, color=INK_SEC, fam=THL)
    save(fig, "s_pyrolysis")

def roadmap():
    fig, ax = canvas(6.7, 3.8, 100, 56.7)
    chap = [("บทที่ 1", "บทนำ", "ที่มา ช่องว่างงานวิจัย\nวัตถุประสงค์ ขอบเขต", "gray"),
            ("บทที่ 2", "ทฤษฎีและ\nงานวิจัยที่เกี่ยวข้อง", "ไบโอชาร์ · RCA · บล็อกปูพื้น\nการลื่นไถล · LCA\nตารางทบทวนเชิงระบบ", "blue"),
            ("บทที่ 3", "วิธีวิจัย", "วัสดุ · ส่วนผสม · การทดสอบ\nBPT · ขอบเขต LCA", "warm"),
            ("บทที่ 4", "ผลและอภิปราย", "ความหนาแน่น · กำลังอัด\nการดูดซึมน้ำ · BPN\nLCA · เทียบงานอื่น", "green"),
            ("บทที่ 5", "สรุปและ\nข้อเสนอแนะ", "สูตรที่เหมาะสม\nข้อจำกัด งานต่อไป", "gray")]
    for i, (a, b, c, fc) in enumerate(chap):
        x = 2 + i * 19.6
        box(ax, x, 22, 18, 30, [L(a, 7.0, "bold", INK, TH), L(b, 7.4, "bold"), L(c, 5.9, "normal", INK_SEC, THL)], fc=fc, lw=0.8)
        if i < 4: arrow(ax, x + 18, 37, x + 19.6, 37, lw=0.9, ms=6)
    ax.add_patch(Rectangle((2, 2), 96, 15, facecolor="white", edgecolor=LINE, lw=0.8, ls="--", zorder=2))
    label(ax, 4, 14, "ส่วนท้ายเล่ม", 6.8, "left", wt="bold")
    for i, t in enumerate(["บรรณานุกรม", "ภาคผนวก ก ข้อมูลรายตัวอย่าง", "ภาคผนวก ข การตรวจสอบข้อมูล", "ภาคผนวก ค พารามิเตอร์ LCA", "ภาคผนวก ง ทะเบียนค่าสมมติ"]):
        box(ax, 4 + i * 18.9, 4, 18, 7.3, [L(t, 5.7)], fc="white", lw=0.6)
    save(fig, "s_roadmap")

def rca_qc():
    fig, ax = canvas(6.7, 3.5, 100, 52.2)
    steps = [("เศษคอนกรีตเหลือทิ้ง", "Waste concrete", "รื้อถอน · ทดสอบวัสดุ", "warm"), ("คัดแยกและตรวจสอบ", "Sorting and inspection", "ตัดสิ่งเจือปน", "white"),
             ("บดย่อย", "Crushing", "ขากรรไกร / กระแทก", "white"), ("ร่อนคัดขนาด", "Sieving", "0.30–2.36 มม. (งานนี้)", "blue"), ("ปรับสภาพ (ถ้ามี)", "Treatment (optional)", "ล้าง · อบ · ลดมอร์ตาร์เดิม", "gray"),
             ("ควบคุมความชื้น", "Moisture control", "ชดเชยการดูดซึมน้ำ", "white"), ("ออกแบบส่วนผสม", "Mix design", "แทนที่ทราย 5–50 %", "green")]
    w = 11.8; gapw = 2.2
    for i, (t, e, s, fc) in enumerate(steps):
        x = 1.5 + i * (w + gapw)
        box(ax, x, 22, w, 20, [L(t, 6.0, "bold"), LE(e, 5.1), L(s, 5.2, "normal", INK_SEC, THL)], fc=fc, lw=0.8, ls="--" if i in (4,) else "-")
        if i < len(steps) - 1: arrow(ax, x + w, 32, x + w + gapw, 32, lw=0.9, ms=6)
    ax.add_patch(Rectangle((1.5, 4), 97, 13, facecolor="#f4f2ec", edgecolor=LINE, lw=0.7, zorder=2))
    label(ax, 3.5, 13.8, "ผลต่อสมบัติ RCA", 6.6, "left", wt="bold")
    label(ax, 3.5, 8.3, "มอร์ตาร์เดิมที่เกาะผิวทำให้ความพรุนสูง ดูดซึมน้ำมาก ความหนาแน่นต่ำ  ·  การปรับสภาพ (ball milling, carbonation, polymer ฯลฯ) ช่วยลดผลเสียดังกล่าว", 6.0, "left", color=INK_SEC, fam=THL)
    ax.text(3.6, 20.2, "เส้นประ = ขั้นตอนที่ไม่ได้ใช้ในงานนี้ (ยืนยันกับผู้วิจัย)", fontsize=5.8, family=THL, color=INK_SEC, va="center")
    ax.set_ylim(3, 46); save(fig, "s_rca_qc")

def lca_stages():
    fig, ax = canvas(6.7, 3.6, 100, 53.7)
    box(ax, 2, 40, 28, 11, [L("1. เป้าหมายและขอบเขต", 7.0, "bold"), LE("Goal and scope", 5.8), L("หน่วยหน้าที่ · ขอบเขตระบบ", 5.8, "normal", INK_SEC, THL)], fc="blue")
    box(ax, 36, 40, 28, 11, [L("2. บัญชีรายการ (LCI)", 7.0, "bold"), LE("Inventory analysis", 5.8), L("มวลวัสดุ · ตัวประกอบการปล่อย", 5.8, "normal", INK_SEC, THL)], fc="blue")
    box(ax, 70, 40, 28, 11, [L("3. ประเมินผลกระทบ (LCIA)", 7.0, "bold"), LE("Impact assessment", 5.8), L("GWP100 · ผลกระทบอื่น", 5.8, "normal", INK_SEC, THL)], fc="blue")
    box(ax, 36, 14, 28, 11, [L("4. การแปลผล", 7.0, "bold"), LE("Interpretation", 5.8), L("ความไว · ความไม่แน่นอน", 5.8, "normal", INK_SEC, THL)], fc="green")
    arrow(ax, 30, 45.5, 36, 45.5); arrow(ax, 64, 45.5, 70, 45.5)
    arrow(ax, 84, 40, 64, 22, conn="arc3,rad=0.15"); arrow(ax, 50, 40, 50, 25, style="<|-|>"); arrow(ax, 16, 40, 36, 22, conn="arc3,rad=-0.15", style="<|-")
    box(ax, 2, 14, 28, 11, [L("การประยุกต์ใช้โดยตรง", 6.6, "bold"), L("พัฒนาสูตร · เทียบเกณฑ์\nสื่อสารนโยบาย", 5.8, "normal", INK_SEC, THL)], fc="white", ls="--")
    box(ax, 70, 14, 28, 11, [L("ข้อกำหนดที่ใช้", 6.6, "bold"), LE("ISO 14040 / 14044 (2006)", 5.8), L("cut-off · cradle-to-gate", 5.8, "normal", INK_SEC, THL)], fc="white", ls="--")
    arrow(ax, 36, 19.5, 30, 19.5, style="-|>"); arrow(ax, 64, 19.5, 70, 19.5, style="<|-")
    save(fig, "s_lca_stages")

def system_boundary():
    fig, ax = canvas(6.7, 4.1, 100, 61.2)
    ax.add_patch(Rectangle((1.5, 4), 66, 52, facecolor="none", edgecolor=ACCENT_EDGE, lw=1.3, ls="--", zorder=2))
    label(ax, 3, 53.4, "ขอบเขตระบบ (cradle-to-gate, A1–A3)", 7.0, "left", wt="bold", color=ACCENT_EDGE)
    mats = [("ปูนซีเมนต์", "Portland cement", "gray"), ("ทรายธรรมชาติ", "Natural sand", "gray"), ("หินเกล็ด", "Crushed stone", "gray"), ("เศษคอนกรีต (RCA)", "burden-free; crushing only", "warm"), ("ถ่านชีวภาพไม้ไผ่", "pyrolysis burden; residues cut-off", "blue"), ("น้ำ", "excluded as negligible", "white")]
    for i, (t, e, fc) in enumerate(mats):
        box(ax, 3.5, 44 - i * 7.4, 24, 6.3, [L(t, 6.3, "bold"), LE(e, 5.1)], fc=fc, lw=0.7)
        arrow(ax, 27.5, 47.1 - i * 7.4, 36, 28, lw=0.5)
    box(ax, 36, 18, 28, 20, [L("ผลิตบล็อก 1 ลบ.ม.", 7.2, "bold"), LE("Batching · mixing · forming", 5.8), L("ซีเมนต์ + มวลรวม + ไบโอชาร์", 6.0, "normal", INK_SEC, THL)], fc="white", lw=1.0)
    label(ax, 50, 11.5, "หน่วยหน้าที่: บล็อกคอนกรีต 1 ลบ.ม.\n(และ 1 ตร.ม. ทางเท้า ≈ 40 ก้อน)", 6.0, color=INK_SEC, fam=THL)
    # outside
    label(ax, 83, 53.4, "นอกขอบเขต", 7.0, wt="bold", color=INK_SEC)
    outs = [("การขนส่ง", "Transport (A2)"), ("ไฟฟ้าและเชื้อเพลิงการผสม", "Plant energy"), ("การก่อสร้างและใช้งาน", "Use stage"), ("การรื้อถอน / รีไซเคิล", "End of life")]
    for i, (t, e) in enumerate(outs):
        box(ax, 71, 42 - i * 10.4, 27, 8.6, [L(t, 6.2), LE(e, 5.3)], fc="white", ec="#8d8d88", lw=0.7, ls="--", hatch="//")
    arrow(ax, 64, 28, 71, 28, lw=0.7, ls="--")
    save(fig, "s_system_boundary")

def hypotheses():
    fig, ax = canvas(6.7, 4.0, 100, 59.7)
    label(ax, 15, 56.2, "ตัวแปรต้น", 7.4, wt="bold"); label(ax, 52, 56.2, "กลไกที่คาดว่าเกิดขึ้น", 7.4, wt="bold"); label(ax, 87, 56.2, "ผลลัพธ์ที่วัด", 7.4, wt="bold")
    box(ax, 2, 36, 26, 14, [L("ไบโอชาร์แทนซีเมนต์", 7.0, "bold"), LE("Series I: 5–25 %", 5.8), L("ซีเมนต์ลดลง · อนุภาคพรุนเพิ่ม", 5.8, "normal", INK_SEC, THL)], fc="blue")
    box(ax, 2, 12, 26, 14, [L("RCA แทนทราย", 7.0, "bold"), LE("Series II: 5–15 %", 5.8), L("มวลรวมเหลี่ยมมุม · มอร์ตาร์เดิม", 5.8, "normal", INK_SEC, THL)], fc="warm")
    mech = [("เจือจางซีเมนต์ + ความพรุนเพิ่ม", 46.5, "blue"), ("ผิวขรุขระ ยึดเกาะเชิงกลดีขึ้น", 33, "warm"), ("ผิวหน้าเรียบ/พรุน ไมโครเท็กซ์เจอร์เปลี่ยน", 19.5, "green"), ("ซีเมนต์ลดลง ภาระ CO2 ลดลง", 6.5, "gray")]
    for t, y, fc in mech:
        box(ax, 36, y - 4.3, 32, 8.6, [L(t, 6.0)], fc=fc, lw=0.7)
    outs = [("H1  ความหนาแน่นและกำลังอัด", "ลดลงเมื่อไบโอชาร์เพิ่ม", 47), ("H2  กำลังอัด (ชุดที่ 2)", "เพิ่มขึ้นเมื่อ RCA เพิ่ม", 36), ("H3  BPN", "แห้ง > เปียก; ลดลงตามไบโอชาร์", 25), ("H4  GWP ต่อ ม.³", "ลดลงตามซีเมนต์ที่ลด", 14), ("H5  ci (GWP/MPa)", "ขึ้นกับสมดุลกำลัง-ซีเมนต์", 3.5)]
    for t, s, y in outs:
        box(ax, 74, y - 4.0, 25, 8.0, [L(t, 6.0, "bold"), L(s, 5.4, "normal", INK_SEC, THL)], fc="white", lw=0.7)
    arrow(ax, 28, 46, 36, 46.5, lw=0.8); arrow(ax, 28, 40, 36, 19.5, lw=0.7); arrow(ax, 28, 38, 36, 8, lw=0.7)
    arrow(ax, 28, 21, 36, 33, lw=0.8); arrow(ax, 28, 17, 36, 19.5, lw=0.7)
    arrow(ax, 68, 46.5, 74, 47, lw=0.8); arrow(ax, 68, 33, 74, 36, lw=0.8); arrow(ax, 68, 19.5, 74, 25, lw=0.8); arrow(ax, 68, 6.5, 74, 14, lw=0.8); arrow(ax, 68, 6.5, 74, 3.5, lw=0.8)
    ax.set_ylim(-1.5, 59.7); save(fig, "s_hypotheses")

if __name__ == "__main__":
    cycle(); pyrolysis(); roadmap(); rca_qc(); lca_stages(); system_boundary(); hypotheses()
