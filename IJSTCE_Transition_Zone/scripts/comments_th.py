# -*- coding: utf-8 -*-
# Review comments (Thai) inserted as yellow-highlighted [AI-nn ...] runs.
# Each entry: (text that identifies the paragraph, text after which the comment is inserted or None = paragraph end, comment).
# Labels: ไม่ชัดเจน = unclear in the text; ไม่สอดคล้อง = inconsistent; ข้อมูลขาด = missing information;
#         ข้อเสนอแนะ = AI recommendation (author decides); ตรวจสอบ = needs checking; สำคัญ = likely reviewer concern.
COMMENTS = [
 ("Version 1 draft for Iranian Journal", None,
  "ชื่อเรื่อง – ไม่ชัดเจน/ข้อเสนอแนะ: (1) คำว่า “Short” ยังไม่มีนิยามเชิงปริมาณ (สั้นเท่าใด – ช่วง PU รวม 15 m หรือช่วงสะพาน ≈ 22 m?); (2) ชื่อเรื่องใช้ “Zones” (พหูพจน์) แต่งานศึกษาโครงสร้างเดียว ขณะที่บทคัดย่อใช้ “a short … transition zone”; (3) ชื่อยาว 20 คำ ควรกระชับขึ้น เช่น “Numerical assessment of stiffness-modification measures for a short meter-gauge railway bridge transition zone” (เป็นข้อเสนอของ AI ผู้เขียนตัดสินใจเอง)"),

 ("Stiffness discontinuity between ballasted track and a bridge", "was computed at 60–120 km/h.",
  "บทคัดย่อ – ไม่ชัดเจน: ค่า peak contact force (เช่น 69.17 kN) ต่ำกว่าแรงล้อสถิต 98.2 kN (ดู Sect. 3.3 และ CONFIRM-10) แต่บทคัดย่อไม่แจ้งข้อจำกัดนี้ ผู้อ่านอาจเข้าใจว่าเป็นแรงสัมผัสรวมของล้อ ควรเติมสั้น ๆ ว่าใช้เปรียบเทียบสัมพัทธ์ระหว่างแบบจำลองเท่านั้น"),

 ("Stiffness discontinuity between ballasted track and a bridge", "between 4.26 and 3.43.",
  "บทคัดย่อ – ไม่ชัดเจน: “peak approach-side stiffness” ยังไม่ได้นิยาม (ค่าสูงสุดตามแนวรางที่ตำแหน่งใด?) และอัตราส่วน 6.0 → 4.26–3.43 คำนวณจากค่า peak ไม่ใช่ค่า ณ รอยต่อกับสะพาน (ดูความเห็นที่ Eq. 2 ใน Sect. 2.4)"),

 ("Stiffness discontinuity between ballasted track and a bridge", None,
  "บทคัดย่อ – ข้อเสนอแนะ: ปัจจุบัน {n_words} คำ และมีตัวเลขหนาแน่นมาก ควรตรวจเพดานจำนวนคำใน Instructions for Authors ของ IJST-TCE (ยังไม่ได้ตรวจในรอบนี้) และพิจารณาย้ายตัวเลขรอง (เช่น 4.26/3.43 หรือ % ของ M3–M5) ไปไว้ในเนื้อหา"),

 ("The State Railway of Thailand operates a meter-gauge network", "Transition-zone studies in this setting remain limited.",
  "บทนำ – ไม่ชัดเจน: คำว่า “short transition zone” ไม่ได้นิยามในบทนำ ควรอธิบายว่า “สั้น” หมายถึงอะไร (ความยาวช่วงสะพาน ≈ 22 m หรือความยาวโซน PU 15 m) และเหตุใดทาง meter-gauge/สะพานช่วงสั้นของ SRT จึงต้องศึกษาแยกจากงานเดิม (เช่น น้ำหนักเพลา ความเร็ว โครงสร้างสะพาน) เพื่อให้ช่องว่างงานวิจัยชัดขึ้น"),

 ("The State Railway of Thailand operates a meter-gauge network", "[CONFIRM-15].",
  "บทนำ – ข้อเสนอแนะ: ช่องว่างงานวิจัยปรากฏเพียงประโยคเดียวท้ายย่อหน้า และเป็นความใหม่เชิง “ชุดมาตรการ” มากกว่าคำถามวิจัยทางวิทยาศาสตร์ ควรระบุว่างานเดิมตอบอะไรไม่ได้ (เช่น สัดส่วนผลของ PU เทียบกับมาตรการเสริมต่อแรงสัมผัสที่ความเร็วสูงในรางแคบ) การอ้างว่า “ยังไม่มีผู้เปรียบเทียบ” ต้องอาศัยการค้นวรรณกรรมเชิงระบบ (CONFIRM-15)"),

 ("The objectives of this study are", None,
  "บทนำ – ไม่สอดคล้อง: วัตถุประสงค์ (i) ใช้คำว่า “calibrate and verify” แต่ Sect. 2.4 และ 3.1 ระบุว่าไม่มี validation และค่าเป้าหมายถูกใช้ทั้ง calibrate และรายงานผล ผู้ตรวจอาจมองว่าวัตถุประสงค์เกินกว่าสิ่งที่ทำได้ — พิจารณาปรับเป็น “build and calibrate … and check its internal consistency” และให้ (ii)–(iii) สะท้อนคำถามวิจัยที่ทดสอบ"),

 ("Research workflow of the study.", None,
  "Fig. 1 – ตรวจสอบ: (1) รูปเดิมระบุ Outputs เป็น “stiffness profile (Fig. 3)” แต่ Fig. 3 แสดงเฉพาะค่า peak (Sect. 3.2 ระบุว่าไม่แสดงโปรไฟล์) รูปใหม่จึงเปลี่ยนเป็น “peak k_d and ρ (Fig. 3, Table 5)” และเติมการอ้างสมการ/ตารางใน flowchart โปรดยืนยัน; (2) caption เขียน “Kd” (K ตัวใหญ่) แต่สมการและเนื้อหาใช้ k_d — ควรแก้ให้ตรงกัน; (3) “interface settlement” ในรูปเดิมเปลี่ยนเป็น “interface compatibility” ให้ตรงกับ Sect. 2.4 และ 3.1"),

 ("The baseline model represents a meter-gauge", "over a sub-ballast layer.",
  "Sect. 2.2 – ข้อมูลขาด: เรขาคณิตยังไม่ครบสำหรับทำซ้ำ — ความหนา sub-ballast, ชั้นดินใต้ sub-ballast และเงื่อนไขขอบล่าง, ขนาดหมอน (ยาว/กว้าง/หนา), หน้าตัดรางที่แน่นอน (source ระบุทั้ง UIC54 และ 100 lb/yd — ดู Drafting notes ส่วน B), ความหนาและชนิดสะพาน/ที่รองรับ ควรเพิ่มตารางหรือรูปแสดงเรขาคณิตของแบบจำลอง"),

 ("The baseline model represents a meter-gauge", "simply supported concrete bridge.",
  "Sect. 2.2 – ไม่ชัดเจน: บนสะพานมีหินโรยทางหรือวางหมอนบนพื้นสะพานโดยตรง (Fig. 2 วาดแบบหลัง ตามภาพเดิม) — มีผลโดยตรงต่อความแข็งเกร็ง 264 kN/mm และต่อความหมายของ “bridge–approach” ควรระบุให้ชัด"),

 ("The baseline model represents a meter-gauge", "approach sections on both sides [CONFIRM-3].",
  "Sect. 2.2 – ไม่ชัดเจน: ทางโรยหินมีสองฝั่ง แต่ PU 3 × 5 m ปรากฏเฉพาะฝั่งทางเข้า (Fig. 2) — ฝั่งขาออกไม่มีมาตรการ หรือสมมาตร? และแรงสัมผัสสูงสุด “near the bridge end” (Sect. 2.5) วัดที่ปลายสะพานด้านใด"),

 ("The baseline model represents a meter-gauge", "to be described here] [CONFIRM-5].",
  "Sect. 2.2 – ข้อมูลขาด (สำคัญ): ช่องว่างนี้เป็นจุดอ่อนใหญ่ของ Methods — ต้องเติมชนิดเอลิเมนต์ ขนาด mesh ใต้ราง/หมอน เงื่อนไขขอบล่าง/ข้าง/ปลาย ตำแหน่งให้แรง ชนิด contact/tie และเหตุผลว่าความยาวโมเดล 70 m เพียงพอ (ไม่มีผลของขอบ) รวมถึงผล mesh-convergence ถ้ามี"),

 ("Material properties used in the finite element model", None,
  "Table 1 – ข้อมูลขาด: (1) ที่มาของพารามิเตอร์ PU (E = 360 MPa, ν = 0.33, ρ = 2000 kg/m³) ไม่ระบุ ทั้งที่ผลทุกข้อขึ้นกับค่านี้โดยตรง; (2) ไม่มีชั้นดินใต้ sub-ballast และไม่มีสมบัติของ auxiliary rail กับ enlarged sleepers; (3) rail pad 400 MPa ควรบอกว่าเป็นโมดูลัสของวัสดุหรือความแข็งเกร็งเทียบเท่า"),

 ("The PU scheme injects the ballast layer", "(Fig. 2) [CONFIRM-7].",
  "Sect. 2.3 – ไม่ชัดเจน: (1) ตำแหน่งแนวดิ่งของ PU ในชั้นหินโรยทาง — Fig. 2 (ตามภาพเดิม) วาด PU ไว้ด้านล่างติดชั้น sub-ballast โดยมีหินโรยทางที่ไม่ฉีดอยู่ด้านบน (โซน 30 cm เหลือ 10 cm) ซึ่งต่างจากการฉีด PU จากผิวบนที่เข้าใจกันทั่วไป (ข้อสังเกตของ AI ยังไม่ได้ตรวจกับแบบจำลอง) โปรดยืนยันจาก ABAQUS; (2) “ความกว้าง” ของ PU ในแบบจำลองหลักไม่ระบุ (Table 4 ใช้ 3.0/2.7/1.9 m)"),

 ("The PU scheme injects the ballast layer", "along part of the PU zone [CONFIRM-6].",
  "Sect. 2.3 – ไม่สอดคล้อง/ข้อมูลขาด: Fig. 2 (ตามภาพเดิม) แสดง auxiliary rail และ enlarged sleepers ครอบคลุมโซน PU 1–2 (≈ 10 m) แต่ source กล่าวถึงเพียง 4–5 หมอน (≈ 2.4–3.0 m ที่ระยะ 0.60 m; CONFIRM-6) รูปจึงวาดเป็นเส้นประแบบ “indicative”; ต้องระบุขนาด วัสดุ ความยาวจริง และคำว่า “enlarged” หมายถึงเพิ่มพื้นที่ฐานในแปลน ความยาว หรือความหนา แล้วแก้รูป/ข้อความให้ตรงกัน"),

 ("Track configurations", None,
  "Table 2 – ข้อเสนอแนะ: การออกแบบกรณีไม่สมบูรณ์ — ไม่มี AR-only / ES-only (ไม่มี PU) จึงแยกผลของ AR และ ES ออกจาก PU ไม่ได้ (ยอมรับใน Sect. 4.3–4.4) ควรอธิบายเหตุผลของการเลือกชุดโมเดลนี้ใน Methods เพื่อไม่ให้ผู้ตรวจเข้าใจว่าเป็นการละเลย"),

 ("Schematic longitudinal section of the modified track", None,
  "Fig. 2 – ตรวจสอบ: รูปถูกวาดใหม่ตามภาพเดิม โดย (1) ความหนา PU/ballast ใช้สัดส่วนแนวดิ่งเดียวกัน (1 in = 1 m) แต่ไม่ตามมาตราส่วนจริงในแนวนอน; (2) ลำดับโซน (30 cm ชิดสะพาน) และตำแหน่ง PU ด้านล่างชั้นหินโรยทางเป็นข้อสมมติเดิมที่ยังไม่ได้ยืนยัน (CONFIRM-7); (3) ไม่แสดงค่า E ของสะพานเพราะยังไม่ยืนยัน (CONFIRM-4)"),

 ("The model was verified, that is, checked", "44 on the ballasted track [CONFIRM-16].",
  "Sect. 2.4 – ไม่ชัดเจน: “trial and error” — ระบุว่าปรับพารามิเตอร์ใด (E ของ ballast / sub-ballast / สะพาน?) ช่วงที่ปรับ ค่าเริ่มต้นและค่าสุดท้าย เกณฑ์ยอมรับ (เช่น ±1%) และจำนวนรอบ; ค่า 264 และ 44 ควรมีหน่วย kN/mm ในประโยคนี้ (CONFIRM-17); และต้องบอกที่มาของค่าเป้าหมาย (CONFIRM-16) เพราะผลเปรียบเทียบทั้งหมดอิงค่าเหล่านี้"),

 ("The model was verified, that is, checked", "cannot also serve as validation data.",
  "Sect. 2.4 – ข้อเสนอแนะ: การตรวจ force equilibrium และ interface compatibility เป็นการตรวจความถูกต้องภายในของแบบจำลองเชิงเส้น (ย่อมสมดุลอยู่แล้ว และ tie constraint ย่อมให้การเคลื่อนที่ต่อเนื่อง) ผู้ตรวจระดับ Q1 มักคาดหวังหลักฐานที่หนักกว่า เช่น (a) mesh-convergence, (b) เปรียบเทียบ k_d หรือ deflection ใต้ล้อกับคำตอบเชิงวิเคราะห์ (beam on elastic foundation), (c) เปรียบเทียบกับช่วงค่าที่รายงานในวรรณกรรม — เป็นข้อเสนอของ AI ไม่ใช่ข้อกำหนดของวารสาร"),

 ("\\frac{\\sum Q_i}{\\sum w_j}", None,
  "สมการ (1)–(3) – ตรวจสอบรูปแบบ: ในไฟล์ Word นี้สมการเป็นข้อความ LaTeX ดิบในสไตล์ “Code” (เช่น k_d = \\frac{\\sum Q_i}{\\sum w_j}) ไม่ใช่ Word Equation จึงจะแสดงเป็นโค้ดในไฟล์ที่ส่งวารสาร ควรแปลงเป็น Word Equation (OMML) ก่อนส่ง — รอบนี้ไม่ได้แก้เพราะอยู่นอกขอบเขตที่สั่ง แต่ทำได้โดยคงเนื้อหาเดิม"),

 ("where Q_i is the vertical load applied at rail seat i", "[CONFIRM-17].",
  "Eq. (1) – ไม่ชัดเจน: (1) ΣQ_i คือแรงที่ให้ (98.164 kN จุดเดียว) ผลรวมปฏิกิริยา 5 หมอน (Table 3 = 98.164 kN) หรือแรงที่ให้ห้าตำแหน่ง (= 5 × 98.164 kN)? ผลต่อ k_d ต่างกัน 5 เท่า (CONFIRM-9); (2) เหตุผลที่เลือกห้าหมอน และผลของการเลือกต่อค่า k_d; (3) ใช้ดัชนี i และ j ต่างกันทั้งที่รวมห้าหมอนเหมือนกัน ทั้งยังซ้ำกับ i ใน Eq. (2)–(3) ที่หมายถึงหมายเลขแบบจำลอง — ควรเปลี่ยนสัญลักษณ์"),

 ("To express how abrupt the stiffness change is", None,
  "Eq. (2) – ไม่ชัดเจน: “peak approach-side stiffness” คือค่าสูงสุดตลอดแนวทางเข้า — ตำแหน่งที่เกิดค่าสูงสุดอยู่ที่ใด (ติดสะพานหรือกลางโซน PU)? ถ้าไม่ติดรอยต่อ ρ จากค่า peak จะไม่สะท้อนความฉับพลันของการเปลี่ยนความแข็งเกร็งที่รอยต่อจริง ควรนิยามเพิ่ม (เช่น อัตราส่วนระหว่างช่วงที่อยู่ติดกัน หรือ stiffness gradient) และเชื่อมกับ CONFIRM-12"),

 ("Wheel–rail contact forces were computed with the multibody software", "at 60, 80, 100, and 120 km/h [CONFIRM-10].",
  "Sect. 2.5 – ไม่ชัดเจน: “a single car of the Thai power car type” คือหัวรถจักรหรือรถดีเซลราง รุ่นใด มวล จำนวนเพลา/โบกี้เท่าใด และ 20-t axle load ใช้กับทุกล้อหรือไม่? (เรื่องแรงต่ำกว่าแรงสถิต ดูความเห็นที่ Sect. 3.3)"),

 ("Wheel–rail contact forces were computed with the multibody software", "was extracted at each speed.",
  "Sect. 2.5 – ข้อมูลขาด (สำคัญ): ยังไม่อธิบายวิธีนำ “โปรไฟล์ความแข็งเกร็งสถิต” จาก ABAQUS เข้าแบบจำลองหลายวัตถุใน UM — แปลงเป็นสปริงใต้ราง/หมอนอย่างไร ใช้ damping เท่าใด มวลรางและหมอน ความไม่เรียบของราง แบบจำลองสัมผัสล้อ–ราง และนิยาม “peak contact force” (ค่าสูงสุดในช่วงใด) หากไม่ชี้แจง ผล Sect. 3.3–3.4 ทำซ้ำไม่ได้ (CONFIRM-10)"),

 ("The authors used Claude (Anthropic) to assist", "[CONFIRM-11].",
  "Sect. 2.6 – ตรวจสอบ: หลังปรับรูปรอบนี้ รูป Figs. 1–6 ทั้งหมด (ไม่ใช่เฉพาะ 1 และ 2) ถูกวาดด้วยสคริปต์ Python/matplotlib จากตัวเลขในตาราง 5–7 โดยใช้ AI ช่วยเขียนสคริปต์ — ต้องแก้ข้อความให้ตรงกับการใช้จริง และตรวจนโยบายเรื่อง AI/รูปภาพของ Springer และ IJST-TCE ล่าสุดก่อนยื่น (ยังไม่ได้ตรวจในรอบนี้)"),

 ("Force equilibrium was satisfied.", "(interpretation).",
  "Sect. 3.1 – ข้อสังเกตทางวิศวกรรม (ยังไม่ได้ตรวจสอบ): หมอนใต้ล้อรับ 93.7% ของแรงและหมอนข้างเคียงรับเพียง 3.7% ต่อหมอน กระจุกตัวมากกว่าที่คาดจากทฤษฎี beam-on-elastic-foundation ของทางหินโรยทางทั่วไป (ตามตำราออกแบบทางมักราวครึ่งหนึ่งของแรงล้อ; ยังไม่ได้ตรวจกับแหล่งอ้างอิงเฉพาะ) รวมทั้งปฏิกิริยาลบ −563 N ที่หมอนนอก — อาจสะท้อนความแข็งดัดของรางที่จำลอง จุดให้แรง หรือความแข็ง rail pad (400 MPa) ควรอธิบายหรือตรวจสอบ เพราะมีผลต่อ k_d (Eq. 1)"),

 ("Reaction forces at the five sleepers beneath the loaded rail seat", None,
  "Table 3 – ไม่ชัดเจน: แถว “Sum of reactions (as reported) 98,164.8” ไม่เท่าผลรวมของแถวบน (98,164.9; ต่างกัน 0.1 N จากการปัดเศษ) และ “Residual 0” ควรเป็น “< 0.1 N” — ควรใส่หมายเหตุใต้ตารางและระบุจำนวนทศนิยมจริงจาก ABAQUS แทนการอธิบายยาวในเนื้อหา"),

 ("Interface compatibility in the three PU test models", None,
  "Table 4 – ไม่ชัดเจน: ไม่ระบุแรงที่ใช้ในโมเดลทดสอบ (98.164 kN?) และ “width” ของ PU (3.0/2.7/1.9 m) เป็นความกว้างตามขวางหรือความยาวตามราง; ไม่มีเหตุผลที่โมเดล 3.0 m/10 cm ไม่ถูกรายงาน (CONFIRM-8) — และเมื่อเป็น tie constraint การตรวจนี้ยืนยันเพียงการเขียนเงื่อนไข (ตามที่เนื้อหายอมรับ) จึงมีน้ำหนักน้อยในฐานะ verification พิจารณาย้ายเป็น Supplementary หรือย่อเหลือหนึ่งประโยค"),

 ("Stepped PU supplied most of the added stiffness.", "the profiles along the track are not reproduced [CONFIRM-12].",
  "Sect. 3.2 – ข้อเสนอแนะ (สำคัญ): ผลหลักของงานคือ “การไล่ระดับความแข็งเกร็ง” แต่รายงานเฉพาะค่า peak — ผู้ตรวจ Q1 มักคาดหวังโปรไฟล์ k_d ตามระยะจากสะพาน (M1–M5) เป็นรูปหลักของบทความ ถ้าไม่มีจะตอบไม่ได้ว่าการเปลี่ยนแปลงราบรื่นจริงหรือไม่ — AI ไม่ได้สร้างรูปนี้เพราะไม่มีข้อมูล และจะไม่สร้างข้อมูลขึ้นเอง กรุณาจัดหาโปรไฟล์จาก ABAQUS (CONFIRM-12)"),

 ("The three combined schemes differed by no more than 0.8 kN", "[CONFIRM-13].",
  "Sect. 3.3 – ไม่ชัดเจน: ความต่างระหว่าง M3–M5 ≤ 0.8 kN (≈ 1.5%) อาจอยู่ในระดับความไม่แน่นอนเชิงตัวเลข (time step, mesh) จึงไม่ควรตีความเชิงกายภาพว่า “ลำดับต่ำสุดสลับกัน” ถ้ายังไม่มี tolerance หรือการทดสอบความไว; และ CONFIRM-13 (สลับ M3/M4) ต้องยืนยันก่อน เพราะกระทบข้อสรุปเรื่องผลของ AR เทียบกับ ES"),

 ("The three combined schemes differed by no more than 0.8 kN", "only the comparison between models is used in the following sections [CONFIRM-10].",
  "Sect. 3.3 – สำคัญ: ข้อความว่าแรงสูงสุด 49–69 kN ต่ำกว่าแรงล้อสถิต 98.2 kN ทำให้ความน่าเชื่อถือของ Sect. 3.3–3.4 ลดลงมาก แม้ใช้เชิงเปรียบเทียบ ผู้ตรวจอาจไม่ยอมรับ เพราะแรงสัมผัสสูงสุดของล้อไม่ควรต่ำกว่าแรงสถิต หากนิยามเป็นแรงล้อรวม — ควรแก้ที่ต้นเหตุ (ตรวจแบบจำลอง UM หรือนิยามปริมาณที่รายงาน) มากกว่าปรับถ้อยคำ"),

 ("Peak wheel–rail contact force against train speed", None,
  "Fig. 4 – แก้ไข caption: เพิ่มประโยค “The inset shows an enlarged view of M3–M5.” ให้ตรงกับรูปใหม่ที่เพิ่มกรอบขยาย เพราะเส้น M3–M5 ซ้อนกัน (ข้อมูลไม่เปลี่ยน) โปรดตรวจและยืนยัน"),

 ("All modified models reduced the peak force relative to M1", "follows directly from the data in Table 6.",
  "Sect. 3.4 – ไม่ชัดเจน: ประโยคนี้อธิบายเชิงเลขคณิต (เพราะ M1 เพิ่มเร็วกว่า) ไม่ใช่เชิงกลไก — ควรอธิบายว่าเหตุใดแรงของ M1 จึงเพิ่มตามความเร็วเร็วกว่ารางที่ปรับปรุง (เช่น พลศาสตร์รถ–ราง ผลของมวลไม่สปริง) หรือยอมรับว่ายังอธิบายกลไกไม่ได้"),

 ("Reduction in peak contact force relative to M1 (%) at four train speeds", None,
  "Table 7 – ไม่ชัดเจน: ค่าในตารางต่างจากการคำนวณด้วย Eq. (3) จาก Table 6 (ค่าปัดเศษ 2 ตำแหน่ง) ที่ทศนิยมตำแหน่งที่สอง ±0.01 จำนวน 8 จาก 16 ค่า (เช่น M2 ที่ 80 km/h: คำนวณ 7.33 ตาราง 7.32; M5 ที่ 120 km/h: 23.70 กับ 23.69) น่าจะเกิดจากใช้ค่าดิบก่อนปัดเศษ — ควรเขียนหมายเหตุใต้ตารางว่าคำนวณจากค่าดิบ หรือทำให้ตัวเลขสองตารางสอดคล้องกัน"),

 ("Reduction in peak wheel–rail contact force relative to M1 at four train speeds", None,
  "Fig. 5 – แก้ไข caption: (เดิม) “The values above the bars are those at 120 km/h.” → รูปใหม่ใส่ค่าทุกแท่ง (ทศนิยม 1 ตำแหน่ง; 2 ตำแหน่งอยู่ใน Table 7) จึงปรับประโยคและเพิ่มนิยาม AR/ES ให้รูปอ่านได้ด้วยตัวเอง (ข้อมูลไม่เปลี่ยน) โปรดตรวจและยืนยัน"),

 ("The peak force at 120 km/h decreased as the peak approach-side stiffness increased", "gave a force 0.21 kN higher than M3 (72 kN/mm).",
  "Sect. 3.4 – ไม่ชัดเจน: อัตรา 0.66 / 0.39 / 0.11 kN ต่อ kN/mm เป็นความชันของเส้นทาง M1→M2→M3→M5 (ข้าม M4) ขั้น M4→M5 ให้ (53.56 − 52.78)/1 = 0.78 kN ต่อ kN/mm ซึ่งไม่ได้ลดลง ข้อสรุป “diminishing rate” จึงขึ้นกับการเลือกเส้นทางและมีสัญญาณรบกวนเชิงตัวเลขขนาดใกล้เคียง (≤ 0.8 kN) — ควรเขียนอย่างระมัดระวัง"),

 ("Peak contact force at 120 km/h against the peak approach-side stiffness", None,
  "Fig. 6 – แก้ไข caption: เพิ่มประโยคอธิบายเส้นประและตัวเลขความชันที่เพิ่มในรูปใหม่ (ค่า 0.66/0.39/0.11 ตรงกับเนื้อหา และคำนวณซ้ำจาก Tables 5–6 แล้ว); M4 ไม่ถูกเชื่อมเพราะไม่เรียงในเส้นทางเดียวกัน (แรงสูงกว่า M3) โปรดตรวจและยืนยัน"),

 ("This explanation is an interpretation", "are not reproduced here.",
  "Sect. 4.1 – ไม่ชัดเจน: คำอธิบาย “ล้อพบตัวรองรับที่แข็งขึ้นก่อนถึงสะพาน” ขึ้นกับสมมติฐานว่าโซน 30 cm ชิดสะพาน (CONFIRM-7) และกับทิศทางวิ่ง (ทางโรยหิน → สะพาน) — ฝั่งขาออก (สะพาน → ทางโรยหิน) และทิศทางวิ่งไม่ได้ศึกษา (Sañudo et al. 2016b ศึกษาอิทธิพลของทิศทางวิ่งต่อ transition zone) ควรระบุเป็นข้อจำกัด"),

 ("The 40.9% rise in peak stiffness with stepped PU", "is of a plausible magnitude.",
  "Sect. 4.2 – ไม่ชัดเจน: ค่าเพิ่ม 40.9% เป็นผลลัพธ์ที่ขึ้นกับ E ของ PU = 360 MPa ที่ผู้เขียนกำหนด (ไม่ทราบที่มา; Table 1) การเทียบกับ Woodward et al. (2014a) จึงมีลักษณะวนกลับ (circular) และยืนยันไม่ได้ว่า E ของ PU สมเหตุสมผล — หากงานนั้นมีค่าโมดูลัสของ PU–ballast ควรเทียบที่ระดับพารามิเตอร์วัสดุ หรือทำ sensitivity ต่อ E ของ PU"),

 ("Fifth, settlement, ballast degradation", "Woodward et al. 2014a).",
  "Sect. 4.4 – ข้อเสนอแนะ: ข้อจำกัดควรเพิ่ม (a) ความไวต่อ E ของ PU และความยาว/ความหนาของโซน PU (sensitivity/parametric), (b) ทิศทางวิ่งและฝั่งขาออก, (c) วัสดุเชิงเส้น (ไม่มี nonlinearity ของ ballast, hanging sleepers), (d) การเชื่อม FE สถิต → UM แบบทางเดียว, (e) ความไม่แน่นอนของค่าเป้าหมายการ calibrate"),

 ("The finite element model satisfied force equilibrium", None,
  "Conclusions ข้อ 1 – ข้อเสนอแนะ: “satisfied force equilibrium and interface compatibility” เป็นการตรวจภายใน ไม่ใช่ข้อค้นพบ ควรลดน้ำหนักหรือย้ายไป Methods และให้ข้อสรุปตอบวัตถุประสงค์ (i)–(iii) ตามลำดับ"),

 ("Field measurements of track stiffness and wheel", None,
  "Conclusions ข้อ 5 – ข้อเสนอแนะ: ข้อนี้เป็นข้อเสนอแนะงานต่อ ไม่ใช่ข้อสรุป — ย้ายไป Sect. 4.4 และให้บทสรุปมีเฉพาะผลที่ตอบวัตถุประสงค์ (ตรวจแนวทางการเขียน Conclusions ของวารสารด้วย)"),

 ("Zakeri JA, Ghorbani V (2011)", None,
  "References – ตรวจสอบ: AI ไม่ได้ตรวจรายการอ้างอิงซ้ำในรอบนี้ — ตาม Drafting notes ส่วน C มี 11 รายการที่ตรวจผ่านแหล่งรองและ 2 รายการที่ยังไม่สมบูรณ์ (OTP 2018; Paoleng et al. 2018b) ควรเปิด DOI ทุกรายการอีกครั้ง และตรวจรูปแบบอ้างอิงกับ Instructions for Authors ของ IJST-TCE ก่อนยื่น"),
]
