# -*- coding: utf-8 -*-
# Round-2 review comments (Thai), calibrated for a Q3 journal. Inserted as yellow-highlighted [AI2-nn ...] runs.
# Tiers:  ต้องแก้ = error / inconsistency / likely to mislead the reader, fix before submission
#         ควรแก้  = clarity or missing essentials that Q3 reviewers usually ask about
#         ตัวเลือก = nice to have; not expected at Q3 (author decides)
# Entry: (text identifying the paragraph, text after which the comment is inserted or None = paragraph end, comment)
COMMENTS = [
 ("Version 2 draft", None,
  "ภาษา – ควรแก้ (เล็ก): ทั้งฉบับสะกดแบบอังกฤษ (behaviour, analysed, modelled, optimised, discretisation) แต่ใช้ “meter-gauge” (แบบอเมริกัน) 10 ครั้ง รวมในชื่อเรื่อง — เลือกแบบเดียว ถ้าใช้อังกฤษให้เป็น “metre-gauge” (ในรูป Fig. 1 มีคำว่า “meter gauge” ด้วย) และตรวจนโยบายภาษาของวารสาร (AI ยังยืนยันไม่ได้)"),

 ("Stiffness discontinuity between ballasted track and a bridge", None,
  "บทคัดย่อ – ตัวเลือก: ตอนนี้ 248 คำ ใกล้เพดาน 250 ตามที่ Drafting notes ระบุ (AI ยืนยันเพดานจากเว็บไซต์วารสารไม่ได้ เพราะเข้า springer.com ไม่ได้ในรอบนี้) ถ้าแก้เพิ่ม ให้ตัดตัวเลขรอง เช่น % ของ M3–M5 ก่อน และนับคำใหม่ทุกครั้ง"),

 ("The State Railway of Thailand operates a meter-gauge network", "cannot be transferred directly to this case.",
  "Intro – ควรแก้ (เล็ก): ประโยคนิยาม “short transition zone” แทรกกลางย่อหน้าที่เล่าเรื่อง SRT และมาตรฐานไทย ทำให้ลำดับความคิดสะดุด — ย้ายไปต้นย่อหน้าถัดไปหรือก่อนวัตถุประสงค์ (ค่า 15 m, 20-t, 60–120 km/h ตรงกับ Sect. 2.3 แล้ว)"),

 ("The State Railway of Thailand operates a meter-gauge network", None,
  "Intro – ควรแก้: คำถามวิจัยถามว่า PU “provides alone” กี่ส่วนเทียบกับมาตรการเสริม แต่ AR/ES ไม่ได้ทดสอบแยกจาก PU และผลไม่เป็น additive (Sect. 3.4) ตัวเลข 73% จึงขึ้นกับลำดับ “PU ก่อน แล้วเติม AR/ES” — ปรับถ้อยคำเป็น “the reduction obtained with stepped PU alone relative to that with all three measures” เพื่อไม่ให้อ่านเป็นการแบ่งสัดส่วนเชิงสาเหตุ"),

 ("The baseline model represents a meter-gauge", "available from the corresponding author on request.",
  "Sect. 2.2 – ควรแก้: ผู้ตรวจไม่เห็นไฟล์โมเดล การเขียนว่า “อยู่ในไฟล์โมเดล” จึงเหมือนข้อมูลหาย ควรเขียนอย่างน้อย 3–4 ประโยค (ชนิดเอลิเมนต์/ขนาด mesh ใต้ราง–หมอน, เงื่อนไขขอบล่างและปลาย, จุดให้แรง, ชนิด tie/contact) และใส่ขนาดหมอนกับความหนา sub-ballast ใน Table 1 หรือตารางเล็ก ๆ — ถ้าไม่มีข้อมูลจริงจากไฟล์ ไม่ควรเติมเอง"),

 ("The baseline model represents a meter-gauge", "A mesh-convergence study is not reported (Sect. 4.4).",
  "Sect. 2.2 – ตัวเลือก: ประโยคนี้ซ้ำกับ Sect. 2.4 และ 4.4 — สำหรับ Q3 ไม่จำเป็นต้องมี mesh-convergence เป็นเงื่อนไข (ดุลยพินิจของ AI ไม่ใช่ข้อกำหนดที่ยืนยันจากวารสาร) ควรคงไว้ครั้งเดียวใน 4.4 เพื่อไม่ให้ Methods ฟังดูแก้ตัว"),

 ("The values of E are material moduli", None,
  "Table 1 – ควรแก้: (1) หมายเหตุเขียนว่า “ที่มาของค่า PU ไม่มีเอกสาร” ในตัวบทที่จะตีพิมพ์ ทำให้ผลหลักดูไม่มีฐาน — ระบุตรง ๆ ว่าเป็นค่าสมมติ/ค่าทดสอบ/อ้างอิงใด และเหตุผล (E_PU = 3.6 × E_ballast); (2) แถว Bridge: E = 395 MPa คู่กับความหนาแน่น 2400 kg/m³ ของคอนกรีต ผู้อ่านจะสงสัย — เพิ่มหมายเหตุว่าเป็นค่าสมมูลที่ปรับให้ได้ 264 kN/mm (ถ้ารวมผลของที่รองรับ ให้บอกด้วย) ไม่ใช่โมดูลัสของคอนกรีต (CONFIRM-4)"),

 ("They form a sequence in which stepped PU", "only their position relative to the PU zones is shown schematically in Fig. 2.",
  "Sect. 2.3 – ควรแก้ (สำคัญ): M3–M5 ต่างจาก M2 เพียงสองมาตรการนี้ แต่ผู้อ่านไม่ทราบขนาด ความยาว หรือวัสดุเลย (บอกเพียง “อยู่ในไฟล์โมเดล”) ทำซ้ำผลหลักไม่ได้ — ให้อย่างน้อย: ความยาวและหน้าตัดของ auxiliary rail, ขนาดหมอนปกติเทียบหมอน enlarged, จำนวนหมอนที่ครอบคลุม (source กล่าวถึง 4–5 หมอน; CONFIRM-6) แล้วแก้ Fig. 2 ให้ตรงกัน (รูปตอนนี้แสดงช่วง ≈ 10 m แบบ indicative)"),

 ("The model was verified, that is, checked", "are not documented here (Sect. 4.4).",
  "Sect. 2.4 – ควรแก้: ค่าเป้าหมาย 44 และ 264 kN/mm เป็นฐานของทั้งบทความ ควรบอกที่มาในหนึ่งประโยค (ต้นฉบับระบุว่า “per reference research” — ถ้ามีเอกสารจริงให้ใส่อ้างอิง; CONFIRM-16) บอกว่าปรับพารามิเตอร์ตัวใด (ประโยคก่อนหน้าระบุเพียง “properties of the bridge and ballasted sections”) และเกณฑ์ที่ยอมรับ — ข้อมูลสั้น ๆ ดีกว่าการเขียนว่า “not documented”"),

 ("is the settlement of sleeper", "(s = 1 to 5).",
  "Eq. (1) – ควรแก้ (เล็ก): “ΣQ” ยังตีความได้หลายแบบ — ระบุตรง ๆ ว่า ΣQ = 98.164 kN (แรงล้อเดียว เท่ากับผลรวมปฏิกิริยา 5 หมอนใน Table 3) และตรวจเลขให้ตรงกัน: Sect. 2.4 ใช้ 98,164.8 N (= 98.165 kN เมื่อปัดเศษ) แต่ประโยคถัดไปเขียน 98.164 kN (CONFIRM-9)"),

 ("Wheel–rail contact forces were computed with the multibody software", "The vehicle mass and the arrangement of axles and bogies are not reported here.",
  "Sect. 2.5 – ควรแก้ (สำคัญ): “a type developed for use in Thailand” ไม่เฉพาะเจาะจงพอ — ระบุประเภท (หัวรถจักรหรือรถดีเซลราง), มวล, จำนวนเพลา–โบกี้ และแหล่งข้อมูล (Drafting notes ข้อ 10 ระบุว่าแหล่งคือ Songsak 2018 ซึ่งไม่อยู่ใน reference list — ถ้าใช้เป็นแหล่งข้อมูลรถ ให้ใส่ในเอกสารอ้างอิง)"),

 ("Wheel–rail contact forces were computed with the multibody software", "so the dynamic results can be reproduced only from those files.",
  "Sect. 2.5 – ควรแก้: ผู้อ่านต้องรู้อย่างน้อยว่าโปรไฟล์ k_d ถูกแปลงเป็นสปริง/หน่วงใต้รางอย่างไร และ “peak force” คือค่าสูงสุดของแรงต่อล้อ (ล้อใด ช่วงใด) — เขียนสั้น ๆ 2–3 ประโยค ส่วนรายละเอียดอื่น (มวลราง, damping, ความไม่เรียบของราง) ใส่ตารางพารามิเตอร์หรือ Supplementary ได้ และควรตัดวลี “reproduced only from those files” เพราะบอกว่าอ่านบทความอย่างเดียวทำซ้ำไม่ได้"),

 ("Wheel–rail contact forces were computed with the multibody software", "so it is used only to compare the models with one another [CONFIRM-10].",
  "Sect. 2.5 – ต้องแก้: แรงสัมผัสสูงสุด 49–69 kN ต่ำกว่าแรงล้อสถิต 98.2 kN เป็นสิ่งที่ผู้อ่านสายวิศวกรรมสะดุดทันที แม้ใช้เชิงเปรียบเทียบ — ควรมีอย่างน้อยหนึ่งประโยคบอกว่าปริมาณที่รายงานคืออะไรและทำไมจึงต่ำกว่าสถิต (เช่น นิยาม output ใน UM หรือมวลรถที่ใช้) ถ้าหาสาเหตุไม่ได้ ให้คงการระบุเป็นข้อจำกัดอย่างชัดเจนตามที่ทำใน Abstract และ Sect. 3.3 แล้ว (ผู้ตรวจอาจยังถามความถูกต้องของแบบจำลอง)"),

 ("Interface compatibility was also satisfied.", "The check therefore carries little weight as verification.",
  "Sect. 3.1 – ควรแก้ (ถ้อยคำ): “carries little weight as verification” ในบท Results ฟังดูลดค่างานตัวเอง ใช้ถ้อยคำเป็นกลาง เช่น “This check confirms the implementation of the constraints only.” ย้ายการประเมินน้ำหนักไป Sect. 4.4 (มีอยู่แล้ว) และพิจารณาย่อประโยค “were not investigated” ในย่อหน้าแรกของ 3.1 ในทำนองเดียวกัน"),

 ("The load applied to the test models", None,
  "Table 4 – ควรแก้ (เล็ก): ระบุแรงที่ใช้และทิศทางของ “width” ในหนึ่งประโยคแทนการอ้างไฟล์โมเดล (ถ้าเป็น 98.164 kN และความกว้างตามขวาง ก็เขียนตรง ๆ)"),

 ("As a result, this study does not show whether the stiffness changes smoothly", "limited to the peak value and the ratio ρ.",
  "Sect. 3.2 – ตัวเลือก (ลดระดับจากรอบแรก): โปรไฟล์ k_d ตามระยะจากสะพานจะทำให้บทความแน่นขึ้นมาก แต่สำหรับ Q3 ไม่จำเป็น — การเขียนข้อจำกัดไว้ชัดเจนเท่าที่ทำใน V2 ยอมรับได้ ถ้ามีข้อมูลจาก ABAQUS อยู่แล้ว การเพิ่มเป็นรูปใหม่ทำได้ (AI ไม่สร้างข้อมูลเอง)"),

 ("Stepped PU, the first measure in the sequence from M1 to M5", "were not analysed (Sañudo et al. 2016b).",
  "Sect. 4.1 – ควรแก้ (เล็ก): การอ้าง Sañudo et al. (2016b) ท้ายประโยค “…were not analysed” อ่านได้ว่างานนั้นไม่ได้วิเคราะห์ ควรแยกอ้าง เช่น “…were not analysed here; the influence of running direction has been studied by Sañudo et al. (2016b).” (อ้างตามชื่อเรื่องของงานนั้น AI ยังไม่ได้อ่านเนื้อหา)"),

 ("Stepped PU, the first measure in the sequence from M1 to M5", "(0.26 to 0.39 kN per kN/mm; Fig. 6).",
  "Sect. 4.1 – ควรแก้ (เล็ก): ช่วง 0.26–0.39 อ่านจาก Fig. 6 ไม่ได้ (รูปแสดง 0.66/0.39/0.11 ตามเส้น M1→M2→M3→M5) ส่วน 0.26 = M2→M4 และ 0.30 = M2→M5 คำนวณจาก Tables 5–6 (AI คำนวณซ้ำแล้ว: 0.26, 0.30, 0.39) — เปลี่ยนเป็น “calculated from Tables 5 and 6” หรือเพิ่มในรูป"),

 ("The study has several limitations.", None,
  "Sect. 4.4 – ควรแก้ (รูปแบบ): ย่อหน้ายาว 374 คำ รวมข้อจำกัดมากกว่า 20 ประเด็น — แยกเป็นข้อสั้น ๆ ตามความสำคัญ (ไม่มี validation/ที่มาของค่าเป้าหมาย; ค่าสมมูลของสะพานและ PU; นิยามแรงสัมผัส/ข้อมูลรถ; ทิศทางเดียว/รูปแบบเดียว; ไม่มี settlement) ส่วน mesh-convergence, หน้าต่างห้าหมอน, การกระจายแรงใน Table 3 เป็นข้อ ตัวเลือก สำหรับ Q3 ย่อเหลือครึ่งประโยคหรือตัดได้ (ดุลยพินิจของ AI)"),

 ("Zakeri JA, Ghorbani V (2011)", None,
  "References – ตรวจสอบ: เลขบทความที่ V2 เพิ่ม (Gundavaram 04023019; Sajjad 04023063) AI ตรวจไม่ได้ในรอบนี้เพราะ crossref.org ถูกบล็อก (V2 ระบุว่าตรวจกับ Crossref แล้ว) — เปิด DOI ตรวจอีกครั้งตอนส่ง และตรวจรูปแบบอ้างอิงกับ Instructions for Authors ของวารสาร"),
]
