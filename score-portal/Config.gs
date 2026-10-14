/**
 * Score Portal — ค่าตั้งต้นของระบบ
 *
 * ค่าที่ผู้สอนปรับได้ระหว่างใช้งานอยู่ในแท็บ "Settings" ของชีตฐานข้อมูล
 * (สร้างให้อัตโนมัติเมื่อรัน setup) ไม่ต้องแก้โค้ดไฟล์นี้ ยกเว้นค่าคงที่ด้านล่าง
 */

var CONFIG = {
  // ค่าตั้งต้นของ Settings.pdf_folder_id — เว้นว่างไว้โดยตั้งใจ (ไม่เก็บ ID โฟลเดอร์จริงใน git)
  // ให้ผู้สอนวาง ID โฟลเดอร์ PDF ในแท็บ Settings หลังรัน "ตั้งค่าเริ่มต้น"
  PDF_FOLDER_ID: '',

  // ชื่อแท็บในชีตคะแนน (ไฟล์ "สรุปคะแนน_ข้อสอบปลายภาค ป.โท (ร่าง).xlsx" ที่แปลงเป็น Google Sheets)
  TAB_SUMMARY: 'สรุปคะแนน',
  TAB_MCQ: 'ปรนัยรายข้อ',
  TAB_WRITTEN: 'อัตนัยรายข้อ',
  TAB_FEEDBACK: 'ข้อควรพิจารณา',

  // ชื่อแท็บในชีตฐานข้อมูล (ชีตที่ผูกกับสคริปต์นี้)
  TAB_SETTINGS: 'Settings',
  TAB_USERS: 'Users',
  TAB_CODES: 'Codes',
  TAB_AUDIT: 'Audit',

  // เกณฑ์ปรนัยตามที่ระบุในไฟล์สรุปคะแนน: ถูก +3 / ผิด -2 / ไม่ตอบ -1 (ใช้แสดงผลรายข้อเท่านั้น
  // คะแนนรวมอ่านจากชีตโดยตรง)
  MCQ_POINTS: { correct: 3, wrong: -2, blank: -1 },
  MCQ_CAP_DEFAULT: 40,
  WRITTEN_MAX_DEFAULT: 20,
  TOTAL_MAX_DEFAULT: 100,

  // การเข้ารหัสรหัสผ่าน (PBKDF2-HMAC-SHA256) จำนวนรอบเก็บไว้ในแถวของผู้ใช้แต่ละคน
  KDF_ITERATIONS: 1000,

  // ล็อกบัญชีชั่วคราวเมื่อกรอกผิดติดกัน
  MAX_FAILED_LOGINS: 5,
  LOCK_MINUTES: 15,

  // จำกัดจำนวนครั้งลงทะเบียนต่อรหัสนักศึกษา ต่อช่วงเวลา
  MAX_REGISTER_ATTEMPTS: 10,
  REGISTER_WINDOW_SECONDS: 900,

  // อายุแคช
  CACHE_DATA_SECONDS: 300,
  CACHE_PDFMAP_SECONDS: 600,
  CACHE_SETTINGS_SECONDS: 30,

  // ขนาด PDF สูงสุดที่ยอมส่งให้เบราว์เซอร์ (ไบต์)
  MAX_PDF_BYTES: 25 * 1024 * 1024
};

/** ค่าตั้งต้นของแท็บ Settings: [key, value, คำอธิบาย] */
var SETTINGS_DEFAULTS = [
  ['published', false, 'TRUE = เปิดประกาศผลให้นักศึกษาเห็นคะแนน / FALSE = ล็อกไว้ (ลงทะเบียนได้ แต่ยังไม่เห็นผล)'],
  ['scores_spreadsheet_id', '', 'ID ของ Google Sheets สรุปคะแนน (เปิดไฟล์ .xlsx ใน Drive แล้ว File > Save as Google Sheets จากนั้นคัดลอก ID จาก URL)'],
  ['pdf_folder_id', CONFIG.PDF_FOLDER_ID, 'ID โฟลเดอร์ Drive ที่เก็บ PDF ที่ตรวจแล้ว'],
  ['course_title', '020325201 ADV.STRUCTURAL', 'ชื่อวิชาที่แสดงบนหน้าเว็บ'],
  ['course_subtitle', 'ข้อสอบปลายภาค · ระดับ ป.โท', 'บรรทัดรองใต้ชื่อวิชา'],
  ['notice', '', 'ข้อความประกาศถึงนักศึกษา (เว้นว่างได้) แสดงที่หน้าเข้าสู่ระบบและหน้าผลคะแนน'],
  ['total_mode', 'official', 'คะแนนรวมที่ใช้แสดงและจัดอันดับ: official = ตามที่ข้อสอบกำหนด | mcq_floor0 = ปรนัยขั้นต่ำ 0 | no_partial_q2 = ข้อ 2 ไม่ให้คะแนนบางส่วน'],
  ['register_verify', 'name', 'วิธียืนยันตัวตนตอนลงทะเบียน: name = รหัส + ชื่อ-สกุล | code = รหัสยืนยันที่ผู้สอนแจกรายคน (แท็บ Codes)'],
  ['show_leaderboard', true, 'แสดงกราฟกระจายคะแนนและอันดับของห้อง (ไม่แสดงชื่อเพื่อน)'],
  ['show_feedback', false, 'แสดงความเห็นรายข้อของนักศึกษาคนนั้น (ควรตรวจทานข้อความในแท็บ ข้อควรพิจารณา ก่อนเปิด)'],
  ['show_pdf', true, 'แสดงไฟล์ PDF ที่ตรวจแล้วของนักศึกษา'],
  ['session_hours', 2, 'อายุการเข้าสู่ระบบ (ชั่วโมง, สูงสุด 6)'],
  ['min_password_length', 8, 'ความยาวรหัสผ่านขั้นต่ำ']
];
