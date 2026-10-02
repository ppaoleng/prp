"""Front matter: cover (kept), revised Thai/English abstracts, acknowledgements (kept), TOC / list of tables / list of figures."""
from ch4_common import *
from docx_builder import mk_p, toc_paragraphs
from docx.oxml import OxmlElement


def marker(b):
    p = OxmlElement("w:p"); b.add(p); return p


def build(b, N):
    res = N["lca"]
    b.keep(0, 27)                                  # cover pages and "บทคัดย่อ" heading (unchanged)
    th = [
        "คอนกรีตบล็อกปูพื้นใช้อย่างแพร่หลายในงานทางเดินเท้า ถนน พื้นที่อุตสาหกรรม และลานอเนกประสงค์ แต่การผลิตซีเมนต์ซึ่งเป็นวัสดุประสานหลักปล่อยก๊าซคาร์บอนไดออกไซด์ปริมาณสูง ขณะที่เศษคอนกรีตเหลือทิ้งจากห้องปฏิบัติการทดสอบวัสดุและงานรื้อถอนเป็นของเสียปริมาณมาก งานวิจัยนี้จึงพัฒนาคอนกรีตบล็อกปูพื้นที่ใช้เศษคอนกรีตเหลือทิ้ง (Recycled Concrete Aggregate: RCA) ร่วมกับถ่านชีวภาพจากไม้ไผ่ (Bamboo biochar) ตามแนวทางเป้าหมายการพัฒนาที่ยั่งยืน",
        "การทดลองมี 2 ชุด ชุดที่ 1 คุมการแทนที่มวลรวมละเอียดด้วย RCA ร้อยละ 50 และใช้ไบโอชาร์ทดแทนซีเมนต์ร้อยละ 0 5 10 และ 15 ชุดที่ 2 คุมไบโอชาร์ 48 กรัมต่อก้อนและแทนที่ทรายด้วย RCA ร้อยละ 0 ถึง 15 ขึ้นรูปเป็นบล็อกรูปคดกริช บ่ม 7 14 และ 28 วัน ทดสอบความหนาแน่น กำลังอัด และการดูดซึมน้ำ 72 ชั่วโมงตาม มอก. 827-2565 วิเคราะห์ด้วย ANOVA และ Tukey HSD ประเมินการปล่อยก๊าซเรือนกระจกเบื้องต้นแบบ cradle-to-gate และเทียบกับงานวิจัยอื่นที่ตรวจสอบแล้ว ความต้านทานการลื่นไถลอยู่ระหว่างการทดสอบ ค่าในรายงานเป็นค่าสมมติ " + PH,
        f"ในชุดที่ 1 ความหนาแน่นและกำลังอัดลดลงเมื่อไบโอชาร์ทดแทนซีเมนต์มากขึ้น ที่ 28 วัน สูตรที่ใช้ไบโอชาร์ร้อยละ 0 5 10 และ 15 มีกำลังอัดเฉลี่ย {f2(N['fc28_RA'])} {f2(N['fc28_Rab5'])} {f2(N['fc28_Rab10'])} และ {f2(N['fc28_Rab15'])} เมกะปาสคาล ผ่านเกณฑ์ 35 เมกะปาสคาลของ มอก. 827-2565 ทุกสูตร และสูตรร้อยละ 5 ผ่านเกณฑ์ 50 เมกะปาสคาลของ มอก. 2035-2565 ด้วย กำลังที่ลดลงส่วนใหญ่อธิบายได้ด้วยซีเมนต์ที่ลดลงและความหนาแน่นที่ลดลง ในชุดที่ 2 กำลังอัดเพิ่มจาก {f2(N['fc28_RCA0'])} เป็น {f2(N['fc28_RCA15'])} เมกะปาสคาลเมื่อ RCA เพิ่ม (ร้อยละ {pct(N['fc28_RCA15'], N['fc28_RCA0']):.0f}) ซึ่งตรงข้ามกับงานส่วนใหญ่ จึงต้องยืนยันกลไก การดูดซึมน้ำทุกสูตรต่ำกว่าร้อยละ 3 แต่ 3 ค่าของชุดที่ 2 ต้องทดสอบซ้ำ ซีเมนต์คิดเป็นร้อยละ {N['share_min']:.0f}–{N['share_max']:.0f} ของการปล่อยก๊าซเรือนกระจกที่ประเมิน การลดซีเมนต์ร้อยละ 5–15 ลดค่านี้เพียงร้อยละ {abs(res.loc['Rab5','gwp_A_vs_ctrl_pct']):.1f}–{abs(res.loc['Rab15','gwp_A_vs_ctrl_pct']):.1f} เมื่อไม่หักเครดิตคาร์บอนของไบโอชาร์",
        "บล็อกที่พัฒนามีกำลังอัดสูงกว่าผลิตภัณฑ์ท้องตลาดสองแหล่งที่ทดสอบ (แหล่งละ 3 ก้อน) ผลสนับสนุนการใช้ไบโอชาร์ทดแทนซีเมนต์ไม่เกินร้อยละ 5 สำหรับงานหนักและไม่เกินร้อยละ 15 สำหรับงานทั่วไป และการใช้ RCA ร้อยละ 10–15 ของทราย โดยขึ้นกับการยืนยันค่าความต้านทานการลื่นไถลจริง ผลงานเชื่อมโยงกับเป้าหมายการพัฒนาที่ยั่งยืนข้อ 9 12 และ 13 ในระดับห้องปฏิบัติการ",
    ]
    for t in th:
        b.p(t)
    b.add(mk_p("<b>คำสำคัญ : </b>คอนกรีตบล็อกปูพื้น, เศษคอนกรีตรีไซเคิล, ถ่านชีวภาพจากไม้ไผ่, กำลังต้านทานแรงอัด, ความต้านทานการลื่นไถล, การประเมินคาร์บอน, เป้าหมายการพัฒนาที่ยั่งยืน", before=160, first=True))
    b.keep(32, 7)                                   # page break, English title block, "Abstract" heading
    en = [
        "Concrete paving blocks are widely used in footpaths, roads, industrial yards and multipurpose areas, yet Portland cement, their principal binder, is a major source of CO2 emissions, and waste concrete from testing laboratories and demolition remains a large waste stream. This study examined paving blocks that combine recycled concrete aggregate (RCA) with bamboo biochar, in alignment with the Sustainable Development Goals.",
        f"Two series were tested. In Series I, RCA replaced 50% of the fine aggregate and biochar replaced 0, 5, 10 and 15% of the cement. In Series II, biochar was fixed at 48 g per block and RCA replaced 0 to 15% of the sand. Zigzag blocks were air-cured for 7, 14 and 28 days and tested for density, compressive strength and 72-hour water absorption according to TIS 827-2565. Data were analysed by ANOVA with Tukey's HSD, and a screening cradle-to-gate assessment of global warming potential (GWP) was added. Slip resistance is still under test; the values shown are placeholders {PH}.",
        f"In Series I, density and strength decreased as biochar replaced more cement. At 28 days the mean strengths were {f2(N['fc28_RA'])}, {f2(N['fc28_Rab5'])}, {f2(N['fc28_Rab10'])} and {f2(N['fc28_Rab15'])} MPa at 0, 5, 10 and 15% biochar. All mixes exceeded the 35 MPa limit of TIS 827-2565, and the 5% mix also exceeded the 50 MPa limit of TIS 2035-2565. Most of the loss was explained by the lower cement content and density. In Series II, strength rose from {f2(N['fc28_RCA0'])} to {f2(N['fc28_RCA15'])} MPa ({pct(N['fc28_RCA15'], N['fc28_RCA0']):+.0f}%) as RCA increased, contrary to most published results, so the mechanism needs confirmation. Water absorption was below 3% for all mixes, although three Series II values need re-testing. Cement accounted for {N['share_min']:.0f}–{N['share_max']:.0f}% of the estimated GWP; replacing 5–15% of cement lowered it by only {abs(res.loc['Rab5','gwp_A_vs_ctrl_pct']):.1f}–{abs(res.loc['Rab15','gwp_A_vs_ctrl_pct']):.1f}% when no carbon-storage credit was applied.",
        "The blocks reached higher strength than two commercial products (three blocks each). The results support replacing up to 5% of cement with biochar in heavy-duty blocks, up to 15% in general-purpose blocks, and 10–15% of sand with RCA, subject to confirmation of slip resistance. The work is linked to SDG 9, 12 and 13 at laboratory scale.",
    ]
    for t in en:
        b.p(t)
    b.add(mk_p("<b>Keywords : </b>Concrete paving block; Recycled concrete aggregate; Bamboo biochar; Compressive strength; Slip resistance; Carbon footprint; Sustainable Development Goals", before=160, first=True))
    b.keep(44, 9)                                   # page break + acknowledgements (46-51) + page break
    b.keep(53, 1)                                   # "สารบัญ" heading
    m_toc = marker(b)
    b.keep(55, 2)                                   # page break + "สารบัญตาราง"
    m_tab = marker(b)
    b.keep(73, 2)                                   # page break + "สารบัญภาพ"
    m_fig = marker(b)
    b.keep(110, 1)                                  # section break (front matter: Thai-letter page numbers)
    return dict(toc=m_toc, tab=m_tab, fig=m_fig)


def finish(b, markers, pages):
    items = b.toc_items
    heads = [e for e in items if e[0] in ("h1", "h2")]
    tabs = [e for e in items if e[0] == "tab"]
    figs = [e for e in items if e[0] == "fig"]
    for key, instr, ents in (("toc", ' TOC \\o "1-2" \\h \\z \\u ', heads), ("tab", ' TOC \\h \\z \\t "TabCaption,1" ', tabs), ("fig", ' TOC \\h \\z \\t "FigCaption,1" ', figs)):
        m = markers[key]
        for p in toc_paragraphs(instr, ents, pages):
            m.addprevious(p)
        m.getparent().remove(m)
