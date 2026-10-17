"""Build LCEC_V2.docx from the V1 package (working copy in scratchpad/v2/unpacked)."""
import re, shutil, os, sys
from PIL import Image

SCR = "/tmp/claude-0/-home-user-prp/fbf7b5d0-c21c-5a62-8407-1d5339d6feff/scratchpad"
PKG = f"{SCR}/v2/unpacked"
FIG = "/home/user/prp/lcec_v2/figures"
DOC = f"{PKG}/word/document.xml"

import subprocess, glob
if os.path.isdir(PKG):
    shutil.rmtree(PKG)
shutil.copytree(f"{SCR}/orig/unpacked", PKG)
SK = glob.glob("/root/.claude/skills/synced/*/docx")[0]
subprocess.run(["python3", f"{SK}/scripts/merge_runs.py", PKG + "/"], check=True)
x = open(DOC, encoding="utf8").read()


# ----------------------------------------------------------------- helpers
def ybr(text, sz=20):
    """Yellow-highlighted Thai comment run: ' [text]'."""
    text = text.replace("&", "&amp;")
    return ('<w:r><w:rPr><w:rFonts w:cstheme="minorBidi" w:hint="cs"/>'
            f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/><w:highlight w:val="yellow"/>'
            '<w:lang w:bidi="th-TH"/></w:rPr>'
            f'<w:t xml:space="preserve"> [{text}]</w:t></w:r>')


def once(s, sub):
    n = s.count(sub)
    assert n == 1, f"anchor occurs {n}x: {sub[:70]!r}"
    return s.index(sub)


def insert_after(s, anchor, runxml):
    """Insert runxml right after `anchor` text (anchor must lie inside one <w:t>)."""
    i = once(s, anchor)
    end = i + len(anchor)
    t_start = s.rfind("<w:t", 0, i)
    assert s.find("</w:t>", t_start) > i, "anchor crosses a run boundary"
    t_close = s.index("</w:t>", end)
    remainder = s[end:t_close]
    run_start = max(s.rfind("<w:r>", 0, i), s.rfind("<w:r ", 0, i))
    run_end = s.index("</w:r>", end) + len("</w:r>")
    prefix = s[run_start:t_start]
    rpr = re.search(r"<w:rPr>.*?</w:rPr>", prefix, flags=re.S)
    rpr = rpr.group(0) if rpr else ""
    if remainder == "":
        return s[:run_end] + runxml + s[run_end:]
    new = (s[:end] + "</w:t></w:r>" + runxml + "<w:r>" + rpr +
           '<w:t xml:space="preserve">' + remainder + s[t_close:])
    return new


def replace_once(s, old, new):
    i = once(s, old)
    return s[:i] + new + s[i + len(old):]


# ----------------------------------------------------------------- 1. header line
x = replace_once(x, "Version 1 (17 October 2026)", "Version 2 (17 October 2026)")
x = insert_after(x, "Version 2 (17 October 2026)", ybr(
    "ความเห็น: ใต้ชื่อเรื่องยังไม่มีรายชื่อผู้เขียน สังกัด และ corresponding author — เพิ่มตามรูปแบบของวารสารเป้าหมาย "
    "(หรือแยกเป็น title page หากวารสารใช้ double-blind) และลบบรรทัด 'Manuscript type … Version 2' ก่อนส่งจริง"))
x = insert_after(x, "Version 2 (17 October 2026)", ybr(
    "คำอธิบาย: ข้อความในวงเล็บพื้นเหลืองทั้งหมดเป็นความเห็นของผู้ช่วยวิจัย AI เพื่อให้ผู้เขียนพิจารณา "
    "ไม่ใช่เนื้อหาของต้นฉบับ — ตรวจและลบออกให้หมดก่อนส่งวารสาร"))
# (second insert lands before the first because both anchor on the same text -> reorder not needed; both present)

# ----------------------------------------------------------------- 2. abstract
x = insert_after(x, "make explicit the observations and assumptions behind a competence claim.", ybr(
    "ความเห็น: Abstract ยาวประมาณ 285 คำ (นับจากไฟล์ V1) ซึ่งอาจเกินเพดานของวารสารเป้าหมาย "
    "(โดยทั่วไปมักอยู่ราว 150–250 คำ แต่ยังไม่ได้ตรวจกับ Author Guidelines ของวารสารใด) — "
    "ลดรายละเอียดเชิงตัวเลขของ corpus (76/35/39/1/1) ให้เหลือเฉพาะ 76 รายงานและ 35 core cases ได้"))

# ----------------------------------------------------------------- 3. introduction
x = insert_after(x, "and no study measured results (Level 4).", ybr(
    "ความเห็น: ประโยคใช้คำว่า 'fewer authors' แต่รูปแสดง 'frequency of usage' — ควรใช้หน่วยให้ตรงกับ Toyoda et al. (2022) "
    "(จำนวนการศึกษา หรือจำนวนครั้งที่ใช้แต่ละระดับ) และตรวจตัวเลข 36/36/6/0 กับตัวบทความต้นฉบับอีกครั้ง"))
x = insert_after(x, "the levels that were least often assessed in that review.", ybr(
    "ความเห็น: 'usually concern behaviour or results' เป็นข้อสรุปเหมารวมที่ยังไม่มีแหล่งอ้างอิง — "
    "เพิ่มการอ้างอิงที่สนับสนุน หรือระบุให้ชัดว่าเป็นการตีความของผู้เขียน"))
x = insert_after(x, "The name denotes three analytical units: learning configuration (LC), assessment evidence (E) and competence claim (C).", ybr(
    "ความเห็น: ชื่อ 'LCEC' มี 4 ตัวอักษรแต่มีเพียง 3 หน่วย (LC, E, C) จนต้องอธิบายซ้ำใน §3.8 — ผู้อ่านและผู้ประเมินอาจสับสน; "
    "พิจารณาเขียนเป็น 'LC–E–C Framework' หรือเปลี่ยนชื่อ แล้วใช้ให้สม่ำเสมอทั้งเอกสารและรูปที่ 4, 6, 7"))

# ----------------------------------------------------------------- 4. methods
x = insert_after(x, "with decisions of 37 INCLUDE, 38 BACKGROUND and one EXCLUDE.", ybr(
    "ความเห็น: 'R2' ปรากฏครั้งแรกใน Fig. 2 และ §2.2 แต่นิยามอยู่ใน §2.3 — ควรนิยามตั้งแต่ครั้งแรก "
    "และอธิบายที่มาของ R2 ให้ชัด (ใคร/เครื่องมือใดเป็นผู้ประเมิน และ R1 คืออะไร) เพราะ Declarations ระบุว่ามี GPT/Codex ช่วยสรุปและเปรียบเทียบการลงรหัส"))
x = insert_after(x, "these outputs were not automatically added to the analytic collection.", ybr(
    "ความเห็น: ไม่ชัดเจนว่า 30 รายการจาก SciSpace ถูกใช้อย่างไรในที่สุด (เป็น conceptual references ที่อ้างในบทความ? "
    "ถูกตัดออก?) — ระบุผลลัพธ์ให้ตรวจสอบย้อนกลับได้"))
x = insert_after(x, "before they were incorporated into the synthesis.", ybr(
    "ความเห็น: ควรระบุจำนวน คุณสมบัติ และความเป็นอิสระของผู้เชี่ยวชาญ (เป็นผู้เขียนหรือไม่) "
    "และขอบเขตของการ 'refined' (แก้ไขสัดส่วนเท่าใดของรายการ) เพราะเป็นหลักฐานหลักของความน่าเชื่อถือของการลงรหัส"))
x = insert_after(x, "Claim-specific implications of inferential appraisal", ybr(
    "ความเห็น: Table 1 เป็นผลการประเมินรายกรณี (ลักษณะเป็นผลลัพธ์) แต่อยู่ใน Methods — พิจารณาย้ายไป §3 "
    "หรือระบุเกณฑ์การเลือก 6 กรณีนี้ (รวม Coronado et al. ซึ่งเป็น contextual ไม่ใช่ core)"))

# ----------------------------------------------------------------- 5. results
x = insert_after(x, "should not be read as a representative map of institutions, countries or learners.", ybr(
    "ความเห็น: Results ยังไม่มีข้อมูลพรรณนาของ 35 core reports (ปี ประเทศ ระดับการศึกษา ประเภทงานวิจัย) ซึ่งผู้ประเมินมักคาดหวัง — "
    "แม้ไม่อ้างความเป็นตัวแทน ควรสรุปเป็นตารางสั้น ๆ หรือชี้ไปยัง S1 (ยังไม่ได้ตรวจ S1 จึงไม่ทราบว่ามีอยู่แล้วหรือไม่)"))
x = insert_after(x, "rather than on sophisticated equipment alone.", ybr(
    "ความเห็น: ผู้อ่านแยกไม่ได้ว่างานที่อ้างใน §3.2–3.6 เป็น core (35) หรือ contextual (39) — "
    "พิจารณาทำเครื่องหมายใน References (เช่น *) หรือระบุในประโยคที่อ้าง เพื่อให้ตรวจสอบย้อนกลับได้"))
x = insert_after(x, "combined achievement tests with suitability and satisfaction measures (Saekram et al., 2023).", ybr(
    "ความเห็น: ผู้เขียน Saekram et al. (2023) มีชื่อย่อ S. Saekram และ S. Maneekeaw ซึ่งตรงกับชื่อในรายชื่อผู้เขียนต้นฉบับนี้ "
    "(เทียบจากชื่อย่อเท่านั้น ยังไม่ยืนยัน) — หากเป็นบุคคลเดียวกัน ควรระบุว่าเป็น self-citation/งานของผู้เขียนเอง "
    "และพิจารณาในส่วน Limitations และ Conflict of interest"))
x = insert_after(x, "Figure 5 summarises the bands and the missing links between them.", ybr(
    "ความเห็น: Fig. 5, Table 3 และ Table 4 มีเนื้อหาซ้อนกันมาก (5 bands + missing links ชุดเดียวกัน; ตรวจเทียบแล้วตรงกัน) — "
    "พิจารณาคงรูป + ตารางอย่างละ 1 และย้าย Table 4 ไป Supplementary เพื่อลดความยาว"))
x = insert_after(x, "Illustrative configurations, evidence and competence interpretations", ybr(
    "ความเห็น: Table 5 แสดงเพียง 5 จาก 35 core cases — ควรระบุเกณฑ์ที่ใช้เลือก (เช่น ครอบคลุมทั้ง 5 กลุ่มใน Table 2) "
    "และชี้ว่าตารางเต็มอยู่ที่ S1 ส่วนใด"))
x = insert_after(x, "rather than relationships demonstrated by the present review.", ybr(
    "ความเห็น: ควรระบุว่าแต่ละข้อเสนอสืบเนื่องจากผลใน §3.2–3.6 ส่วนใดโดยเฉพาะ (ตอนนี้บอกเพียงว่า 'follow from the synthesis') "
    "เพื่อให้ตรวจสอบย้อนกลับได้"))
x = insert_after(x, "Figure 7 illustrates the example.", ybr(
    "ความเห็น: Fig. 7 แสดง 5 claims (Team performance, Individual capability, Situated judgement, External alignment, Transfer) "
    "ซึ่งไม่ตรงกับ 5 bands ใน Table 3 (Team performance และ Individual capability ไม่ใช่ band) — "
    "ชี้แจงในเนื้อหา/คำบรรยายรูป หรือจัดให้สอดคล้องกัน เพื่อไม่ให้ผู้อ่านเข้าใจว่าเป็นชุดเดียวกัน"))

# ----------------------------------------------------------------- 6. discussion / conclusions
x = insert_after(x, "LCEC gives this distinction a practical structure for design, laboratory, capstone and vocational learning.", ybr(
    "ความเห็น: 'practical structure' อาจเกินหลักฐาน เพราะ LCEC ยังไม่ได้ทดสอบกับผู้ใช้/ในสถานการณ์จริง "
    "(ขัดกับท่าทีของบทความที่ว่าเป็น provisional synthesis) — พิจารณา 'a proposed structure'"))
x = insert_after(x, "Extension beyond the reviewed settings remains an empirical question.", ybr(
    "ความเห็น: ประโยคเชิงปฏิเสธ/ระมัดระวังซ้ำมากทั้งบทความ (นับคร่าว ๆ จากเนื้อหาก่อน References: 'rather than' ≈ 33, "
    "'does not' ≈ 24, 'not establish' ≈ 17 ครั้ง) — ผู้ประเมินอาจมองว่าซ้ำและบั่นทอนข้อเสนอเชิงบวก; "
    "พิจารณารวม/ตัดประโยคปฏิเสธที่ซ้ำ โดยคงไว้เฉพาะใน Abstract, §2 และ §4.5"))
x = insert_after(x, "The proposed mechanism becomes testable when judgement is specified at a suitable level of detail.", ybr(
    "ความเห็น: คำว่า 'mechanism' สื่อถึงกลไกเชิงเหตุผล ขัดกับข้อความอื่นที่ระบุว่า LCEC ไม่ใช่ causal model "
    "(Abstract, §3.8, Fig. 4) — พิจารณาใช้ 'proposed interpretive account' หรือคำที่เป็นกลางกว่า"))
x = insert_after(x, "limit the reproducibility and authority of the cross-case interpretation.", ybr(
    "ความเห็น: Limitations ยังไม่กล่าวถึงบทบาทของเครื่องมือ AI ในการสรุป/เปรียบเทียบการลงรหัส (ตาม Declarations) — "
    "ควรเพิ่มประโยคเรื่องความเสี่ยงต่อข้อผิดพลาดจากการสรุปด้วย AI และวิธีตรวจสอบที่ทำจริง"))
x = insert_after(x, "The three objectives of this review lead to the following conclusions.", ybr(
    "ความเห็น: ข้อสรุป (i)–(iii) ซ้ำกับ §3.7 เกือบทั้งหมด — ย่อ §3.7 หรือให้ Conclusions เน้นนัยเชิงปฏิบัติ ข้อจำกัด "
    "และงานวิจัยต่อไป เพื่อลดความซ้ำ"))

# ----------------------------------------------------------------- 7. figures: captions
def caption_para(label, text, extra=""):
    return ('<w:p><w:pPr><w:keepLines/><w:spacing w:before="40" w:after="200"/><w:jc w:val="left"/></w:pPr>'
            f'<w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">{label} </w:t></w:r>'
            f'<w:r><w:rPr><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">{text}</w:t></w:r>{extra}</w:p>')


# Fig 1 caption paragraph (replace whole paragraph that contains the old caption + Thai notes)
i = once(x, "Figure 1. ")
p0 = x.rfind("<w:p ", 0, i)
p1 = x.index("</w:p>", i) + len("</w:p>")
fig1_caption = caption_para(
    "Figure 1.",
    "Distribution of the outcome(s) measured, based on Kirkpatrick’s training evaluation model, in "
    "virtual-reality-based health and safety training for high-risk engineering industries. Adapted from "
    "Toyoda et al. (2022, Fig. 7), which is published under a Creative Commons Attribution 4.0 licence (CC BY 4.0). "
    "The frequencies (36, 36, 6 and 0 for Levels 1–4) were read from the original figure and re-plotted; "
    "the level names and the bracket over Levels 3 and 4 were added by the present authors.",
    ybr("ความเห็น: ค่า 36/36/6/0 อ่านจากรูปต้นฉบับ (Toyoda et al., 2022, Fig. 7) โดยวัดพิกเซลเทียบเส้นกริด "
        "ยังไม่ได้เทียบกับตัวบทความโดยตรง (เข้าถึงบทความออนไลน์จากสภาพแวดล้อมนี้ไม่ได้) — โปรดตรวจกับต้นฉบับ "
        "รวมทั้งชื่อระดับ Reaction/Learning/Behaviour/Results และวงเล็บเหนือ Level 3–4 ซึ่งเป็นส่วนที่เพิ่มขึ้นมาใหม่"))
x = x[:p0] + fig1_caption + x[p1:]

# Fig 2 caption: drop the author's Thai to-do note (done in V2)
i = once(x, "Figure 2. ")
p0 = x.rfind("<w:p ", 0, i)
p1 = x.index("</w:p>", i) + len("</w:p>")
fig2_caption = caption_para(
    "Figure 2.",
    "Procedure of the critical integrative review. Boxes record the principal steps, the diamond marks the "
    "iterative revision of sensitising categories, and grey labels give the sheet of Supplementary Material S1 "
    "in which each step is documented. The dashed box lists procedures that were not performed or claimed.")
x = x[:p0] + fig2_caption + x[p1:]

# Fig 3 caption
i = once(x, "Figure 3. ")
p0 = x.rfind("<w:p ", 0, i)
p1 = x.index("</w:p>", i) + len("</w:p>")
fig3_caption = caption_para(
    "Figure 3.",
    "Disposition of the retained report collection (n = 76). The original R2 decisions (left) and the corrected "
    "disposition after subsequent factual corrections (right) are distinguished; band widths are proportional to "
    "the number of reports, and the two brown bands mark the corrections to INCLUDE decisions. Counts refer to "
    "reports, not verified independent studies; the historical 3,020-row discovery registry is not a verified "
    "search denominator, and this is not a PRISMA identification and screening flow.",
    ybr("ความเห็น: รูปนี้จับคู่ 'EXCLUDE 1' กับ 'Outside the educational focus 1' ตามผลรวมในข้อความ "
        "(37−2 = 35; 38+1 = 39; 1; 1 รวม 76) ซึ่งเป็นการอนุมานจากตัวเลขใน §2.2 ไม่ได้ระบุตรง ๆ — โปรดยืนยันว่าเป็นรายงานเดียวกัน"))
x = x[:p0] + fig3_caption + x[p1:]

# ----------------------------------------------------------------- 8. figures: images
imgs = {  # rId -> (media file, new png, width in)
    "rId8": ("image1.png", "fig1_kirkpatrick.png", 4.4),
    "rId9": ("image2.png", "fig2_flowchart.png", 6.3),
    "rId10": ("image3.png", "fig3_disposition.png", 6.3),
    "rId11": ("image4.png", "fig4_lcec_framework.png", 6.3),
    "rId12": ("image5.png", "fig5_bands.png", 6.3),
    "rId13": ("image6.png", "fig6_propositions.png", 6.3),
    "rId14": ("image7.png", "fig7_worked_example.png", 6.3),
}
alt = {
    "rId8": "Bar chart of the frequency of use of Kirkpatrick evaluation levels: Level 1 (reaction) 36, Level 2 (learning) 36, Level 3 (behaviour) 6, Level 4 (results) 0.",
    "rId9": "Flowchart of the review procedure from the retained collection of 76 report records to the synthesis outputs, with an iterative loop for revising sensitising categories.",
    "rId10": "Flow diagram from recorded R2 decisions (37 INCLUDE, 38 BACKGROUND, 1 EXCLUDE) to the corrected disposition (35 core, 1 without a matched full text, 39 contextual or foundational, 1 outside the educational focus).",
    "rId11": "Diagram of the LCEC Framework: learning configuration, assessment evidence and competence claim, linked by an LC-E link and an E-C link, with a feedback loop from evidence to configuration.",
    "rId12": "Diagram of five evidence-claim bands from learner response to transfer, with the missing link between each pair of bands and the factors that cut across all bands.",
    "rId13": "Diagram of research propositions P1 to P3, each linking a configuration contrast, the evidence to collect and the interpretation to test.",
    "rId14": "Diagram of the worked example: one learning configuration and its assessment evidence support five distinct competence claims.",
}
for rid, (media, png, w_in) in imgs.items():
    shutil.copyfile(f"{FIG}/{png}", f"{PKG}/word/media/{media}")
    w, h = Image.open(f"{FIG}/{png}").size
    cx = int(round(w_in * 914400))
    cy = int(round(cx * h / w))
    m = re.search(r"<w:drawing>(?:(?!</w:drawing>).)*?r:embed=\"%s\".*?</w:drawing>" % rid, x, flags=re.S)
    d = m.group(0)
    d2 = re.sub(r'<wp:extent cx="\d+" cy="\d+"/>', f'<wp:extent cx="{cx}" cy="{cy}"/>', d)
    d2 = re.sub(r'<a:ext cx="\d+" cy="\d+"/>', f'<a:ext cx="{cx}" cy="{cy}"/>', d2)
    d2 = re.sub(r'(<wp:docPr id="\d+" name="[^"]*")( descr="[^"]*")?', lambda mm: mm.group(1) + f' descr="{alt[rid]}"', d2)
    x = x.replace(d, d2)

# Fig 1: take the picture out of the dashed grey table and centre it like the other figures
m = re.search(r"<w:tbl>.*?</w:tbl>", x[x.index("Evidence from an adjacent field"):], flags=re.S)
tbl = m.group(0)
assert "r:embed=\"rId8\"" in tbl
drawing = re.search(r"<w:drawing>.*?</w:drawing>", tbl, flags=re.S).group(0)
fig1_para = ('<w:p><w:pPr><w:keepNext/><w:spacing w:before="120" w:after="40"/><w:jc w:val="center"/></w:pPr>'
             f'<w:r><w:rPr><w:noProof/></w:rPr>{drawing}</w:r></w:p>')
x = x.replace(tbl, fig1_para)

# ----------------------------------------------------------------- 9. back matter + references heading
a0 = x.rfind("<w:p ", 0, once(x, "<w:t>Acknowledgement</w:t>"))
ref_i = once(x, "<w:t>References</w:t>")
a1 = x.index("</w:p>", ref_i) + len("</w:p>")
old_back = x[a0:a1]
assert "ช่วยเรียบเรียงที่ไฮไลต์เหลืองให้ด้วยครับ" in old_back and "Author Contribution" in old_back

# remove the older plain 'Ethics statement' paragraph in Declarations (merged into the final one below)
e_i = once(x, "Ethics statement. ")
e0 = x.rfind("<w:p ", 0, e_i)
e1 = x.index("</w:p>", e_i) + len("</w:p>")
old_eth = x[e0:e1]
assert "Not applicable. This review analysed published reports" in old_eth


def runin(head, body, extra=""):
    return ('<w:p><w:r><w:rPr><w:b/></w:rPr>'
            f'<w:t xml:space="preserve">{head} </w:t></w:r>'
            f'<w:r><w:t xml:space="preserve">{body}</w:t></w:r>{extra}</w:p>')


ack = runin("Acknowledgements.", "", ybr(
    "ความเห็น: ต้นฉบับมีเฉพาะหัวข้อ ไม่มีเนื้อหา — ใส่ชื่อบุคคล/หน่วยงานที่ต้องการขอบคุณ (เช่น ผู้เชี่ยวชาญที่ทบทวน R2 "
    "หากไม่ได้เป็นผู้เขียน) หรือหากไม่มี ให้ใช้ 'The authors have no acknowledgements to declare.' หรือตัดหัวข้อออกตามที่วารสารกำหนด; "
    "ไม่ได้เติมข้อความแทนผู้เขียน"))
fund = runin("Funding.", "This research received no external funding.")
coi = runin("Conflict of interest.", "The authors declare no conflict of interest.", ybr(
    "ความเห็น: หาก Saekram et al. (2023) เป็นงานของผู้เขียนเอง ควรพิจารณาเปิดเผยในข้อนี้ — ดูหมายเหตุที่ §3.4"))
auth = runin(
    "Author contributions.",
    "Study conception and design: Piyarat Paoleng. Analysis and interpretation of results: Siriphat Maneekeaw and "
    "Piyarat Paoleng. Draft manuscript preparation and supervision: Piyarat Paoleng. Review and editing: Siriphat "
    "Maneekeaw, Krairoj Mahannopkul, Phuwadon Yaiyindee and Surawut Saekram. All authors reviewed the results and "
    "approved the final version of the manuscript.",
    ybr("ความเห็น: (1) เรียบเรียงเป็นประโยคสั้นและใช้ 'Author contributions' ตามรูปแบบทั่วไป เนื้อหาและชื่อเดิมครบ — "
        "หากวารสารกำหนด CRediT taxonomy ให้เปลี่ยนตามนั้น; (2) AI statement ระบุว่า GPT/Codex ช่วย 'substantive drafting' "
        "แต่ข้อนี้ระบุว่า Piyarat Paoleng เป็นผู้เตรียมร่างต้นฉบับ — ควรปรับให้สอดคล้องกัน และตรวจนโยบาย AI ของวารสารเป้าหมาย"))
eth = runin(
    "Ethics statement.",
    "Not applicable. This review analysed published reports and involved no human participants, human data or animal subjects.",
    ybr("ความเห็น: รวม 'Ethics statement' สองข้อที่ซ้ำกันให้เหลือข้อเดียว และเปลี่ยน 'curriculum documents' (ในข้อความไฮไลต์เดิม) "
        "เป็น 'published reports' ให้ตรงกับ §2.2 และ Declarations — โปรดยืนยันว่าถูกต้อง (หากงานวิเคราะห์เอกสารหลักสูตรจริง ต้องแก้ Methods ด้วย)"))
refs = ('<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>References</w:t></w:r></w:p>'
        '<w:p><w:pPr><w:jc w:val="left"/></w:pPr>' + ybr(
            "ความเห็น: ตรวจเบื้องต้นแบบอัตโนมัติ (จับคู่ชื่อผู้เขียนแรก–ปี) พบว่า 110 รายการใน References ทุกรายการถูกอ้างในเนื้อหา "
            "และการอ้างในเนื้อหามีรายการใน References ครบ แต่ยังไม่ได้ตรวจความถูกต้องของ DOI/เล่ม/หน้า — "
            "ควรตรวจรูปแบบรายการที่ผิดปกติ เช่น Lozano et al. (2025) ไม่มีเล่ม/ฉบับ, Salman et al. (2025) 'sp(VII)', "
            "Fawns et al. (2026) advance online (อัปเดตเมื่อตีพิมพ์) และจัดรูปแบบตามวารสารเป้าหมาย") + '</w:p>')
x = x.replace(old_back, ack + fund + coi + auth + eth + refs)
x = x.replace(old_eth, "")

# AI statement: V2 update + consistency note
x = insert_after(x, "The authors are responsible for the classifications, interpretations, references and submitted text.", ybr(
    "ความเห็น: ข้อความระบุบทบาทของ Claude เฉพาะ 'Version 1' — ปรับให้ครอบคลุมงานรอบ V2 ตามจริง "
    "(ออกแบบรูปใหม่ ปรับ Declarations และให้ข้อเสนอแนะ) และเปิดเผยให้ตรงกับนโยบาย AI ของวารสารเป้าหมาย; ไม่ได้แก้ข้อความของผู้เขียนเอง"))

open(DOC, "w", encoding="utf8").write(x)
print("document.xml written", len(x))
