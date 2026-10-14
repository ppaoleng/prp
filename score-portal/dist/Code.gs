/**
 * Score Portal — ไฟล์รวม สร้างอัตโนมัติด้วย dev/bundle.js
 * ห้ามแก้ไฟล์นี้โดยตรง: แก้ที่ไฟล์ต้นทางแล้วรัน node dev/bundle.js ใหม่
 */

/* ===== Config.gs ===== */
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

/* ===== Lib.gs ===== */
/**
 * ฟังก์ชันล้วน (ไม่เรียกบริการของ Google) — ทดสอบด้วย Node ได้ที่ tests/
 * ชื่อที่ลงท้าย _ เป็น private: เรียกจากหน้าเว็บผ่าน google.script.run ไม่ได้
 */

var THAI_DIGITS_ = '๐๑๒๓๔๕๖๗๘๙';

function normalizeDigits_(s) {
  return String(s == null ? '' : s).replace(/[๐-๙]/g, function (c) {
    return String(THAI_DIGITS_.indexOf(c));
  });
}

/** รหัสนักศึกษา -> ตัวเลขล้วน (รับทั้ง 69-020328-4601-3, 6902032846013, เลขไทย) */
function normalizeId_(s) {
  return normalizeDigits_(s).replace(/\D/g, '');
}

/** ชื่อ-สกุล -> รูปเทียบ: ตัด คำนำหน้า ช่องว่าง จุด และอักขระล่องหน */
function normalizeName_(s) {
  var t = String(s == null ? '' : s);
  if (t.normalize) t = t.normalize('NFC');
  t = t.replace(/[\s​-‍﻿.]/g, '').toLowerCase();
  return t.replace(/^(นางสาว|นาง|นาย|นส|เด็กชาย|เด็กหญิง|ดช|ดญ|mrs|mr|ms|miss)/, '');
}

/** ชื่อไฟล์ -> รูปเทียบ (รองรับ \_ ที่หลุดมาจากการ export, NFC, ช่องว่างซ้ำ) */
function normalizeFileName_(s) {
  var t = String(s == null ? '' : s);
  if (t.normalize) t = t.normalize('NFC');
  return t.replace(/\\_/g, '_').replace(/\s+/g, ' ').trim().toLowerCase();
}

function cell_(v) {
  return String(v == null ? '' : v).replace(/\s+/g, ' ').trim();
}

function toNum_(v) {
  if (typeof v === 'number') return isFinite(v) ? v : null;
  if (v == null) return null;
  var s = String(v).replace(/,/g, '').trim();
  if (s === '' || !/^[-+]?\d*\.?\d+$/.test(s)) return null;
  return parseFloat(s);
}

function asBool_(v, dflt) {
  if (v === true || v === false) return v;
  if (v == null || v === '') return dflt;
  var s = String(v).trim().toLowerCase();
  if (s === 'true' || s === '1' || s === 'yes' || s === 'y') return true;
  if (s === 'false' || s === '0' || s === 'no' || s === 'n') return false;
  return dflt;
}

function round_(x, d) {
  if (x == null || !isFinite(x)) return null;
  var p = Math.pow(10, d == null ? 2 : d);
  return Math.round(x * p) / p;
}

/* ---------- สถิติ ---------- */

function sum_(a) {
  var s = 0;
  for (var i = 0; i < a.length; i++) s += a[i];
  return s;
}

function mean_(a) {
  return a.length ? sum_(a) / a.length : null;
}

function median_(a) {
  if (!a.length) return null;
  var b = a.slice().sort(function (x, y) { return x - y; });
  var m = Math.floor(b.length / 2);
  return b.length % 2 ? b[m] : (b[m - 1] + b[m]) / 2;
}

/** ส่วนเบี่ยงเบนมาตรฐานประชากร (หารด้วย N) */
function sd_(a) {
  if (!a.length) return null;
  var m = mean_(a), s = 0;
  for (var i = 0; i < a.length; i++) s += (a[i] - m) * (a[i] - m);
  return Math.sqrt(s / a.length);
}

function onlyNums_(a) {
  var out = [];
  for (var i = 0; i < a.length; i++) if (typeof a[i] === 'number' && isFinite(a[i])) out.push(a[i]);
  return out;
}

/** อันดับแบบแข่งขัน (1,2,2,4): คะแนนเท่ากันได้อันดับเดียวกัน; null = ไม่มีคะแนน */
function competitionRanks_(values) {
  var ranks = [];
  for (var i = 0; i < values.length; i++) {
    if (values[i] == null) { ranks.push(null); continue; }
    var higher = 0;
    for (var j = 0; j < values.length; j++) {
      if (values[j] != null && values[j] > values[i]) higher++;
    }
    ranks.push(higher + 1);
  }
  return ranks;
}

/** สัดส่วน (0-100) ของเพื่อนคนอื่นที่คะแนนต่ำกว่า "ฉัน" อย่างเคร่งครัด; null ถ้าห้องมีคนเดียว */
function percentAbove_(score, values) {
  var others = 0, lower = 0, skipped = false;
  for (var i = 0; i < values.length; i++) {
    if (values[i] == null) continue;
    if (!skipped && values[i] === score) { skipped = true; continue; }
    others++;
    if (values[i] < score) lower++;
  }
  return others ? Math.round((lower / others) * 100) : null;
}

/** ฮิสโตแกรมช่วงละ width คะแนน ครอบคลุมตั้งแต่ช่วงที่ต่ำสุดถึงสูงสุดของห้อง */
function buildHistogram_(values, width) {
  var v = onlyNums_(values);
  if (!v.length) return { width: width, bins: [] };
  var lo = Math.floor(Math.min.apply(null, v) / width) * width;
  var hi = Math.floor(Math.max.apply(null, v) / width) * width + width;
  var bins = [];
  for (var s = lo; s < hi; s += width) bins.push({ from: s, to: s + width - 1, count: 0 });
  for (var i = 0; i < v.length; i++) bins[Math.floor((v[i] - lo) / width)].count++;
  return { width: width, bins: bins };
}

function binIndexFor_(hist, score) {
  if (!hist.bins.length || score == null) return -1;
  var lo = hist.bins[0].from;
  var k = Math.floor((score - lo) / hist.width);
  return k >= 0 && k < hist.bins.length ? k : -1;
}

/* ---------- รหัสผ่าน / ความปลอดภัย ---------- */

/** คืนข้อความผิดพลาด หรือ '' ถ้าผ่าน */
function validatePassword_(pw, studentIdKey, minLen) {
  pw = String(pw == null ? '' : pw);
  if (pw.length < minLen) return 'รหัสผ่านต้องยาวอย่างน้อย ' + minLen + ' ตัวอักษร';
  if (pw.length > 128) return 'รหัสผ่านยาวเกินไป (สูงสุด 128 ตัวอักษร)';
  if (!/[A-Za-z฀-๿]/.test(pw) || !/[0-9๐-๙]/.test(pw)) {
    return 'รหัสผ่านต้องมีทั้งตัวอักษรและตัวเลข';
  }
  if (/^(.)\1+$/.test(pw)) return 'รหัสผ่านง่ายเกินไป';
  var digits = normalizeId_(pw);
  if (studentIdKey && (digits === studentIdKey || (digits.length >= 8 && studentIdKey.indexOf(digits) !== -1))) {
    return 'ห้ามใช้รหัสนักศึกษาเป็นรหัสผ่าน';
  }
  return '';
}

/** เปรียบเทียบสตริงแบบเวลาคงที่ */
function safeEqual_(a, b) {
  a = String(a == null ? '' : a);
  b = String(b == null ? '' : b);
  var diff = a.length ^ b.length, n = Math.max(a.length, b.length);
  for (var i = 0; i < n; i++) diff |= (a.charCodeAt(i) || 0) ^ (b.charCodeAt(i) || 0);
  return diff === 0;
}

function bytesToHex_(bytes) {
  var out = '';
  for (var i = 0; i < bytes.length; i++) {
    var h = (bytes[i] & 0xff).toString(16);
    out += h.length === 1 ? '0' + h : h;
  }
  return out;
}

/** ตัด HTML/สคริปต์ออกจากข้อความที่จะแสดง (ชั้นแรก; หน้าเว็บ escape อีกชั้น) */
function cleanText_(s) {
  return String(s == null ? '' : s).replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, '').trim();
}

/* ===== Data.gs ===== */
/**
 * อ่านและแปลงข้อมูลจากชีตสรุปคะแนน (แท็บ สรุปคะแนน / ปรนัยรายข้อ / อัตนัยรายข้อ / ข้อควรพิจารณา)
 * ฟังก์ชัน parse*_ รับอาร์เรย์ 2 มิติ (getValues) จึงทดสอบนอก Google ได้
 * การหาคอลัมน์ใช้ "ข้อความหัวตาราง" ไม่ใช้ตำแหน่ง ผู้สอนเพิ่ม/ย้ายคอลัมน์ได้
 *
 * หมายเหตุความเป็นส่วนตัว: คอลัมน์ "ข้อควรพิจารณา" ในแท็บสรุปคะแนน (บันทึกภายในถึงผู้สอน)
 * ไม่ถูกอ่านเข้าระบบเลย
 */

var INTERNAL_COMMENT_RE_ = /ผู้สอน|ลำดับที่\s*\d+|คัดลอก|ผู้ช่วยตรวจ/;

function findHeaderRow_(values, pred, maxScan) {
  var n = Math.min(values.length, maxScan || 40);
  for (var r = 0; r < n; r++) {
    if (pred((values[r] || []).map(cell_))) return r;
  }
  return -1;
}

function colWhere_(head, pred) {
  for (var i = 0; i < head.length; i++) if (pred(head[i], i)) return i;
  return -1;
}

function colStarts_(head, prefix) {
  return colWhere_(head, function (c) { return c.indexOf(prefix) === 0; });
}

/** ดึงคะแนนเต็มจากหัวคอลัมน์ เช่น "อัตนัยข้อ 1 (20)" "ปรนัยที่ใช้ (สูงสุด 40)" */
function maxFromHeader_(text, fallback) {
  var m = /\((?:สูงสุด\s*)?(\d+(?:\.\d+)?)\)/.exec(String(text || ''));
  return m ? parseFloat(m[1]) : fallback;
}

function isSeq_(v) {
  var n = toNum_(v);
  return n != null && n > 0 && Math.floor(n) === n;
}

/* ---------- แท็บ สรุปคะแนน ---------- */

function parseSummary_(values) {
  var h = findHeaderRow_(values, function (row) { return row.indexOf('รหัสนักศึกษา') !== -1; });
  if (h < 0) throw new Error('แท็บ "' + CONFIG.TAB_SUMMARY + '": ไม่พบหัวคอลัมน์ "รหัสนักศึกษา"');
  var head = values[h].map(cell_);
  var col = {
    seq: head.indexOf('ลำดับ'),
    id: head.indexOf('รหัสนักศึกษา'),
    name: head.indexOf('ชื่อ-สกุล'),
    group: colStarts_(head, 'กลุ่ม'),
    mcqCorrect: head.indexOf('ปรนัยถูก'),
    mcqWrong: head.indexOf('ปรนัยผิด'),
    mcqBlank: head.indexOf('ไม่ตอบ'),
    mcqFormula: colStarts_(head, 'ปรนัยตามสูตร'),
    mcqUsed: colStarts_(head, 'ปรนัยที่ใช้'),
    w1: colStarts_(head, 'อัตนัยข้อ 1'),
    w2: colStarts_(head, 'อัตนัยข้อ 2'),
    w3: colStarts_(head, 'อัตนัยข้อ 3'),
    wTotal: colStarts_(head, 'อัตนัยรวม'),
    tOfficial: colStarts_(head, 'คะแนนรวม'),
    tFloor0: colStarts_(head, 'รวม ถ้าปรนัย'),
    tNoPartial: colStarts_(head, 'รวม ถ้าข้อ 2'),
    pdf: colStarts_(head, 'ไฟล์ PDF')
  };
  var labels = { id: 'รหัสนักศึกษา', name: 'ชื่อ-สกุล', mcqUsed: 'ปรนัยที่ใช้', w1: 'อัตนัยข้อ 1', w2: 'อัตนัยข้อ 2', w3: 'อัตนัยข้อ 3', tOfficial: 'คะแนนรวม' };
  var missing = [];
  Object.keys(labels).forEach(function (k) { if (col[k] < 0) missing.push(labels[k]); });
  if (missing.length) {
    throw new Error('แท็บ "' + CONFIG.TAB_SUMMARY + '": ไม่พบหัวคอลัมน์ ' + missing.join(', '));
  }

  var max = {
    mcq: maxFromHeader_(head[col.mcqUsed], CONFIG.MCQ_CAP_DEFAULT),
    w: [
      maxFromHeader_(head[col.w1], CONFIG.WRITTEN_MAX_DEFAULT),
      maxFromHeader_(head[col.w2], CONFIG.WRITTEN_MAX_DEFAULT),
      maxFromHeader_(head[col.w3], CONFIG.WRITTEN_MAX_DEFAULT)
    ],
    total: maxFromHeader_(head[col.tOfficial], CONFIG.TOTAL_MAX_DEFAULT)
  };
  max.written = col.wTotal >= 0 ? maxFromHeader_(head[col.wTotal], sum_(max.w)) : sum_(max.w);

  function num(row, c) { return c >= 0 ? toNum_(row[c]) : null; }
  var students = [];
  for (var r = h + 1; r < values.length; r++) {
    var row = values[r] || [];
    var idKey = normalizeId_(row[col.id]);
    if (idKey.length < 8) continue; // แถวสถิติท้ายตาราง (เฉลี่ย/สูงสุด/ต่ำสุด) ไม่มีรหัสนักศึกษา
    var w = [num(row, col.w1), num(row, col.w2), num(row, col.w3)];
    var wTotal = num(row, col.wTotal);
    if (wTotal == null && w.every(function (x) { return x != null; })) wTotal = sum_(w);
    var used = num(row, col.mcqUsed);
    var official = num(row, col.tOfficial);
    if (official == null && used != null && wTotal != null) official = used + wTotal;
    var floor0 = num(row, col.tFloor0);
    if (floor0 == null && used != null && wTotal != null) floor0 = Math.max(0, used) + wTotal;
    students.push({
      seq: col.seq >= 0 && isSeq_(row[col.seq]) ? toNum_(row[col.seq]) : students.length + 1,
      id: cell_(row[col.id]),
      idKey: idKey,
      name: cell_(row[col.name]),
      group: col.group >= 0 ? cell_(row[col.group]) : '',
      pdfName: col.pdf >= 0 ? cell_(row[col.pdf]) : '',
      mcq: {
        correct: num(row, col.mcqCorrect), wrong: num(row, col.mcqWrong), blank: num(row, col.mcqBlank),
        formula: num(row, col.mcqFormula), used: used
      },
      w: w,
      wTotal: wTotal,
      totals: { official: official, mcq_floor0: floor0, no_partial_q2: num(row, col.tNoPartial) }
    });
  }
  return { students: students, max: max };
}

/* ---------- แท็บ ปรนัยรายข้อ ---------- */

var MCQ_CHOICES_ = 'กขคงจ';

function cleanChoice_(v) {
  var c = cell_(v).charAt(0);
  return c && MCQ_CHOICES_.indexOf(c) !== -1 ? c : null;
}

function parseMcq_(values) {
  var h = findHeaderRow_(values, function (row) {
    return row.indexOf('ชื่อ-สกุล') !== -1 && row.some(function (c) { return /^ข้อ ?1$/.test(c); });
  });
  if (h < 0) throw new Error('แท็บ "' + CONFIG.TAB_MCQ + '": ไม่พบหัวตาราง (ชื่อ-สกุล, ข้อ 1, ข้อ 2, ...)');
  var head = values[h].map(cell_);
  var cols = [];
  head.forEach(function (c, i) {
    var m = /^ข้อ ?(\d+)$/.exec(c);
    if (m) cols.push({ no: parseInt(m[1], 10), col: i });
  });
  cols.sort(function (a, b) { return a.no - b.no; });
  var colSeq = head.indexOf('ลำดับ'), colName = head.indexOf('ชื่อ-สกุล');

  // แถวเฉลย: แถวใต้หัวตารางที่มีคำว่า "เฉลย"
  var key = {};
  for (var r = h + 1; r < Math.min(values.length, h + 8); r++) {
    var row = values[r] || [];
    var hasLabel = row.some(function (c) { return cell_(c).indexOf('เฉลย') !== -1; });
    if (!hasLabel) continue;
    cols.forEach(function (c) {
      var ch = cleanChoice_(row[c.col]);
      if (ch) key[c.no] = ch;
    });
    if (Object.keys(key).length < cols.length) { // เฉลยไม่ตรงคอลัมน์ -> ไล่ตัวเลือกตามลำดับ
      var letters = [];
      row.forEach(function (c) { if (/^[กขคงจ]$/.test(cell_(c))) letters.push(cell_(c)); });
      if (letters.length === cols.length) {
        key = {};
        cols.forEach(function (c, k) { key[c.no] = letters[k]; });
      }
    }
    break;
  }

  var rows = {};
  for (var q = h + 1; q < values.length; q++) {
    var rw = values[q] || [];
    if (colSeq < 0 || !isSeq_(rw[colSeq]) || !cell_(rw[colName])) continue;
    rows[toNum_(rw[colSeq])] = {
      name: cell_(rw[colName]),
      answers: cols.map(function (c) { return cleanChoice_(rw[c.col]); })
    };
  }
  return { items: cols.map(function (c) { return c.no; }), key: key, rows: rows };
}

/* ---------- แท็บ อัตนัยรายข้อ ---------- */

function parseWritten_(values) {
  var h = findHeaderRow_(values, function (row) {
    return row.indexOf('ชื่อ-สกุล') !== -1 && row.some(function (c) { return /^ข้อ ?\d+ .+/.test(c); });
  });
  if (h < 0) throw new Error('แท็บ "' + CONFIG.TAB_WRITTEN + '": ไม่พบหัวตาราง (ชื่อ-สกุล, ข้อ1 ..., ข้อ 1 รวม)');
  var head = values[h].map(cell_);
  var qs = {};
  head.forEach(function (c, i) {
    var m = /^ข้อ ?(\d+) (.+)$/.exec(c);
    if (!m) return;
    var no = parseInt(m[1], 10);
    var q = qs[no] || (qs[no] = { no: no, items: [], totalCol: -1 });
    if (m[2].trim() === 'รวม') q.totalCol = i;
    else q.items.push({ label: m[2].trim(), col: i });
  });
  var questions = Object.keys(qs).map(function (k) { return qs[k]; }).sort(function (a, b) { return a.no - b.no; });
  var colSeq = head.indexOf('ลำดับ'), colName = head.indexOf('ชื่อ-สกุล');
  var colTotal = colStarts_(head, 'อัตนัยรวม');

  // แถว "คะแนนเต็ม" ใต้หัวตาราง
  var maxRow = null;
  for (var r = h + 1; r < Math.min(values.length, h + 6); r++) {
    var rr = values[r] || [];
    if (rr.some(function (c) { return cell_(c).indexOf('คะแนนเต็ม') !== -1; })) { maxRow = rr; break; }
  }
  questions.forEach(function (q) {
    q.items.forEach(function (it) { it.max = maxRow ? toNum_(maxRow[it.col]) : null; });
    var tm = maxRow && q.totalCol >= 0 ? toNum_(maxRow[q.totalCol]) : null;
    var itemSum = sum_(onlyNums_(q.items.map(function (it) { return it.max; })));
    q.max = tm != null ? tm : (itemSum || CONFIG.WRITTEN_MAX_DEFAULT);
  });

  var rows = {};
  for (var s = h + 1; s < values.length; s++) {
    var rw = values[s] || [];
    if (colSeq < 0 || !isSeq_(rw[colSeq]) || !cell_(rw[colName])) continue;
    rows[toNum_(rw[colSeq])] = {
      name: cell_(rw[colName]),
      q: questions.map(function (q) {
        var items = q.items.map(function (it) { return toNum_(rw[it.col]); });
        var total = q.totalCol >= 0 ? toNum_(rw[q.totalCol]) : null;
        if (total == null && items.length && items.every(function (x) { return x != null; })) total = sum_(items);
        return { items: items, total: total };
      })
    };
  }
  return {
    questions: questions.map(function (q) {
      return { no: q.no, max: q.max, items: q.items.map(function (it) { return { label: it.label, max: it.max }; }) };
    }),
    rows: rows
  };
}

/* ---------- แท็บ ข้อควรพิจารณา (ความเห็นรายข้อ) ---------- */

function parseFeedback_(values) {
  var h = findHeaderRow_(values, function (row) {
    return row.indexOf('ชื่อ-สกุล') !== -1 && row.indexOf('ความเห็น') !== -1;
  });
  if (h < 0) throw new Error('แท็บ "' + CONFIG.TAB_FEEDBACK + '": ไม่พบหัวตาราง (ชื่อ-สกุล, ข้อ, ความเห็น)');
  var head = values[h].map(cell_);
  var cSeq = head.indexOf('ลำดับ'), cScope = head.indexOf('ข้อ'), cText = head.indexOf('ความเห็น');
  var bySeq = {};
  for (var r = h + 1; r < values.length; r++) {
    var row = values[r] || [];
    if (cSeq < 0 || !isSeq_(row[cSeq])) continue;
    var scope = cell_(row[cScope]);
    var text = cleanText_(row[cText]);
    // เฉพาะความเห็นรายข้อ; ข้ามบันทึกภายใน ("ข้อควรพิจารณา") และข้อความที่พูดถึงผู้สอน/นักศึกษาคนอื่น
    var isItem = scope.indexOf('อัตนัย') === 0 || scope.indexOf('ปรนัยข้อ') === 0;
    if (!isItem || !text || INTERNAL_COMMENT_RE_.test(text)) continue;
    var seq = toNum_(row[cSeq]);
    (bySeq[seq] = bySeq[seq] || []).push({ scope: scope, text: text });
  }
  return bySeq;
}

/* ---------- รวมทุกแท็บเป็นข้อมูลห้อง ---------- */

function buildClassData_(summary, mcq, written, feedback) {
  var warnings = [];
  var seen = {};

  function lookup(rows, s, label) {
    if (!rows) return null;
    var r = rows[s.seq];
    if (r && normalizeName_(r.name) === normalizeName_(s.name)) return r;
    var hit = null;
    Object.keys(rows).forEach(function (k) {
      if (!hit && normalizeName_(rows[k].name) === normalizeName_(s.name)) hit = rows[k];
    });
    if (!hit) warnings.push('ไม่พบ "' + s.name + '" ในแท็บ' + label);
    else if (r) warnings.push('ลำดับของ "' + s.name + '" ในแท็บ' + label + ' ไม่ตรงกับแท็บสรุปคะแนน (จับคู่ด้วยชื่อ)');
    return hit;
  }

  var students = [];
  summary.students.forEach(function (s) {
    if (seen[s.idKey]) { warnings.push('รหัสนักศึกษาซ้ำ: ' + s.id + ' (ใช้แถวแรก)'); return; }
    seen[s.idKey] = true;
    var m = lookup(mcq && mcq.rows, s, CONFIG.TAB_MCQ);
    var w = lookup(written && written.rows, s, CONFIG.TAB_WRITTEN);
    var fb = (feedback && feedback[s.seq]) || [];
    students.push({
      seq: s.seq, id: s.id, idKey: s.idKey, name: s.name, group: s.group, pdfName: s.pdfName,
      mcq: s.mcq, w: s.w, wTotal: s.wTotal, totals: s.totals,
      answers: m ? m.answers : null,
      wd: w ? w.q : null,
      feedback: fb
    });
  });
  return {
    builtAt: new Date().toISOString(),
    students: students,
    max: summary.max,
    mcq: mcq ? { items: mcq.items, key: mcq.key } : null,
    written: written ? { questions: written.questions } : null,
    warnings: warnings
  };
}

/* ---------- สร้างข้อมูลหน้า Dashboard ของนักศึกษา 1 คน ---------- */

var TOTAL_LABELS_ = {
  official: { label: 'คะแนนรวม', note: '' },
  mcq_floor0: { label: 'คะแนนรวม', note: 'คำนวณโดยให้คะแนนปรนัยต่ำสุดเป็น 0' },
  no_partial_q2: { label: 'คะแนนรวม', note: 'คำนวณโดยข้อ 2 ไม่ให้คะแนนบางส่วน' }
};

function totalFor_(s, mode) {
  var t = s.totals[mode];
  return t == null ? s.totals.official : t;
}

function findStudent_(D, idKey) {
  for (var i = 0; i < D.students.length; i++) if (D.students[i].idKey === idKey) return i;
  return -1;
}

function statBlock_(values) {
  var v = onlyNums_(values);
  return {
    n: v.length,
    mean: round_(mean_(v), 2),
    median: round_(median_(v), 2),
    sd: round_(sd_(v), 2),
    max: v.length ? Math.max.apply(null, v) : null,
    min: v.length ? Math.min.apply(null, v) : null
  };
}

function buildDashboard_(D, idKey, settings) {
  var idx = findStudent_(D, idKey);
  if (idx < 0) return null;
  var me = D.students[idx];
  var mode = TOTAL_LABELS_[settings.total_mode] ? settings.total_mode : 'official';

  var totals = D.students.map(function (s) { return totalFor_(s, mode); });
  var ranks = competitionRanks_(totals);
  var myTotal = totals[idx];
  var tstat = statBlock_(totals);
  var ties = 0;
  totals.forEach(function (t, i) { if (i !== idx && t != null && t === myTotal) ties++; });

  var hist = buildHistogram_(totals, 10);
  var floor0 = mode === 'mcq_floor0';
  function mcqUsed(s) { return s.mcq.used == null ? null : (floor0 ? Math.max(0, s.mcq.used) : s.mcq.used); }

  function comp(key, label, max, getter) {
    var vals = D.students.map(getter);
    var st = statBlock_(vals);
    return { key: key, label: label, score: getter(me), max: max, mean: st.mean, best: st.max, low: st.min };
  }
  var components = [
    comp('mcq', 'ปรนัย', D.max.mcq, mcqUsed),
    comp('q1', 'อัตนัยข้อ 1', D.max.w[0], function (s) { return s.w[0]; }),
    comp('q2', 'อัตนัยข้อ 2', D.max.w[1], function (s) { return s.w[1]; }),
    comp('q3', 'อัตนัยข้อ 3', D.max.w[2], function (s) { return s.w[2]; })
  ];
  var writtenComp = comp('written', 'อัตนัยรวม', D.max.written, function (s) { return s.wTotal; });

  // ปรนัยรายข้อ
  var mcqBlock = null;
  if (D.mcq && me.answers) {
    var items = D.mcq.items.map(function (no, k) {
      var ans = me.answers[k], key = D.mcq.key[no] || null;
      var result = ans == null ? 'blank' : (ans === key ? 'correct' : 'wrong');
      var answered = 0, right = 0;
      D.students.forEach(function (s) {
        if (!s.answers) return;
        answered++;
        if (key && s.answers[k] === key) right++;
      });
      return {
        no: no, key: key, answer: ans, result: result,
        points: CONFIG.MCQ_POINTS[result],
        classCorrectPct: answered ? Math.round((right / answered) * 100) : null
      };
    });
    mcqBlock = {
      items: items,
      correct: me.mcq.correct, wrong: me.mcq.wrong, blank: me.mcq.blank,
      formula: me.mcq.formula, used: mcqUsed(me), cap: D.max.mcq,
      points: CONFIG.MCQ_POINTS
    };
  }

  // อัตนัยรายหัวข้อ
  var writtenBlock = null;
  if (D.written && me.wd) {
    writtenBlock = D.written.questions.map(function (q, qi) {
      var mine = me.wd[qi];
      var qTotals = D.students.map(function (s) { return s.wd ? s.wd[qi].total : null; });
      return {
        no: q.no, label: 'อัตนัยข้อ ' + q.no, max: q.max,
        score: mine.total, classMean: round_(mean_(onlyNums_(qTotals)), 2),
        items: q.items.map(function (it, k) {
          var col = D.students.map(function (s) { return s.wd ? s.wd[qi].items[k] : null; });
          return { label: it.label, max: it.max, score: mine.items[k], classMean: round_(mean_(onlyNums_(col)), 2) };
        })
      };
    });
  }

  var leaderboard = null;
  if (settings.show_leaderboard) {
    leaderboard = [];
    totals.forEach(function (t, i) {
      if (t != null) leaderboard.push({ rank: ranks[i], score: t, you: i === idx });
    });
    leaderboard.sort(function (a, b) { return a.rank - b.rank || (a.you ? -1 : 0); });
    leaderboard = leaderboard.slice(0, 100);
  }

  return {
    student: { id: me.id, name: me.name, seq: me.seq, group: me.group },
    total: {
      label: TOTAL_LABELS_[mode].label, note: TOTAL_LABELS_[mode].note, mode: mode,
      score: myTotal, max: D.max.total,
      rank: ranks[idx], of: tstat.n, ties: ties,
      percentAbove: myTotal == null ? null : percentAbove_(myTotal, totals),
      mean: tstat.mean, median: tstat.median, sd: tstat.sd, best: tstat.max, low: tstat.min
    },
    components: components,
    written: writtenComp,
    distribution: settings.show_leaderboard ? { width: hist.width, bins: hist.bins, you: binIndexFor_(hist, myTotal) } : null,
    leaderboard: leaderboard,
    mcq: mcqBlock,
    writtenDetail: writtenBlock,
    feedback: settings.show_feedback ? me.feedback : null,
    hasPdf: !!settings.show_pdf && !!me.pdfName,
    builtAt: D.builtAt
  };
}

/* ---------- จับคู่ไฟล์ PDF กับนักศึกษา ---------- */

/** map: { ชื่อไฟล์แบบ normalize -> fileId } ; คืน fileId หรือ null */
function resolvePdfId_(student, map) {
  if (student.pdfName) {
    var hit = map[normalizeFileName_(student.pdfName)];
    if (hit) return hit;
  }
  // สำรอง: ตรวจแล้ว_<ลำดับ 2 หลัก>_<ชื่อ>.pdf
  var pad = (student.seq < 10 ? '0' : '') + student.seq;
  var prefix = normalizeFileName_('ตรวจแล้ว_' + pad + '_');
  var nameKey = normalizeName_(student.name);
  var found = null, count = 0;
  Object.keys(map).forEach(function (k) {
    if (k.indexOf(prefix) === 0 && normalizeName_(k.slice(prefix.length).replace(/\.pdf$/, '')) === nameKey) {
      found = map[k]; count++;
    }
  });
  return count === 1 ? found : null;
}

/* ===== Store.gs ===== */
/**
 * ชั้นเก็บข้อมูล: แคช, ตั้งค่า, ชีตฐานข้อมูล (Users/Codes/Audit), โหลดข้อมูลห้อง และรายการไฟล์ PDF
 */

/* ---------- แคช (แบ่งก้อนเพราะ CacheService จำกัด ~100KB ต่อค่า) ---------- */

var CACHE_CHUNK_ = 30000;

function cachePutJson_(key, obj, ttl) {
  try {
    var s = JSON.stringify(obj);
    var n = Math.max(1, Math.ceil(s.length / CACHE_CHUNK_));
    var map = {};
    for (var i = 0; i < n; i++) map[key + ':' + i] = s.substr(i * CACHE_CHUNK_, CACHE_CHUNK_);
    map[key + ':n'] = String(n);
    CacheService.getScriptCache().putAll(map, ttl);
  } catch (e) { /* แคชพลาดไม่เป็นไร ระบบอ่านจากชีตตรงๆ ได้ */ }
}

function cacheGetJson_(key) {
  try {
    var cache = CacheService.getScriptCache();
    var n = parseInt(cache.get(key + ':n'), 10);
    if (!n) return null;
    var keys = [];
    for (var i = 0; i < n; i++) keys.push(key + ':' + i);
    var got = cache.getAll(keys), s = '';
    for (var j = 0; j < n; j++) {
      if (got[keys[j]] == null) return null;
      s += got[keys[j]];
    }
    return JSON.parse(s);
  } catch (e) { return null; }
}

function cacheRemoveJson_(key) {
  try { CacheService.getScriptCache().remove(key + ':n'); } catch (e) { /* ignore */ }
}

function clearAllCaches_() {
  ['classdata', 'settings', 'pdfmap'].forEach(cacheRemoveJson_);
}

/* ---------- ชีตฐานข้อมูล ---------- */

function getDb_() {
  var id = PropertiesService.getScriptProperties().getProperty('DB_ID');
  if (id) return SpreadsheetApp.openById(id);
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  if (!ss) throw new Error('ยังไม่ได้ตั้งค่าชีตฐานข้อมูล: เปิดชีตที่ผูกกับสคริปต์แล้วเมนู Score Portal > ตั้งค่าเริ่มต้น');
  return ss;
}

function getTab_(name) {
  var sh = getDb_().getSheetByName(name);
  if (!sh) throw new Error('ไม่พบแท็บ "' + name + '" — รันเมนู Score Portal > ตั้งค่าเริ่มต้น');
  return sh;
}

/* ---------- ตั้งค่า (แท็บ Settings) ---------- */

function getSettings_() {
  var cached = cacheGetJson_('settings');
  if (cached) return cached;
  var out = {}, defaults = {};
  SETTINGS_DEFAULTS.forEach(function (d) { defaults[d[0]] = d[1]; out[d[0]] = d[1]; });
  var sh = getDb_().getSheetByName(CONFIG.TAB_SETTINGS);
  if (sh) {
    var rows = sh.getDataRange().getValues();
    for (var r = 0; r < rows.length; r++) {
      var key = cell_(rows[r][0]);
      if (!Object.prototype.hasOwnProperty.call(defaults, key)) continue;
      var raw = rows[r][1], d = defaults[key];
      if (typeof d === 'boolean') out[key] = asBool_(raw, d);
      else if (typeof d === 'number') { var n = toNum_(raw); out[key] = n == null ? d : n; }
      else out[key] = cell_(raw);
    }
  }
  if (!{ official: 1, mcq_floor0: 1, no_partial_q2: 1 }[out.total_mode]) out.total_mode = 'official';
  if (!{ name: 1, code: 1 }[out.register_verify]) out.register_verify = 'name';
  out.session_hours = Math.min(6, Math.max(0.25, out.session_hours));
  out.min_password_length = Math.max(6, Math.floor(out.min_password_length));
  cachePutJson_('settings', out, CONFIG.CACHE_SETTINGS_SECONDS);
  return out;
}

/* ---------- Audit log (ไม่บันทึกรหัสผ่าน) ---------- */

function audit_(studentKey, event, detail) {
  try {
    getTab_(CONFIG.TAB_AUDIT).appendRow([new Date().toISOString(), studentKey || '', event, detail || '']);
  } catch (e) { /* ล็อกพลาดต้องไม่ทำให้ระบบล่ม */ }
}

/* ---------- โหลดข้อมูลห้องจากชีตคะแนน ---------- */

function getScoresSpreadsheet_(settings) {
  if (!settings.scores_spreadsheet_id) {
    throw new Error('ยังไม่ได้ตั้งค่า scores_spreadsheet_id ในแท็บ Settings');
  }
  return SpreadsheetApp.openById(settings.scores_spreadsheet_id);
}

function findSheet_(ss, name) {
  var exact = ss.getSheetByName(name);
  if (exact) return exact;
  var all = ss.getSheets();
  for (var i = 0; i < all.length; i++) if (all[i].getName().indexOf(name) !== -1) return all[i];
  return null;
}

function readTab_(ss, name, required) {
  var sh = findSheet_(ss, name);
  if (!sh) {
    if (required) throw new Error('ไม่พบแท็บ "' + name + '" ในชีตคะแนน');
    return null;
  }
  return sh.getDataRange().getValues();
}

/** อ่านชีตคะแนนทั้งหมด (ไม่ใช้แคช) -> ข้อมูลห้อง */
function readClassData_(settings) {
  var ss = getScoresSpreadsheet_(settings);
  var extra = [];
  var summary = parseSummary_(readTab_(ss, CONFIG.TAB_SUMMARY, true));

  function optional(tab, fn) {
    var v = readTab_(ss, tab, false);
    if (!v) { extra.push('ไม่พบแท็บ "' + tab + '" (ข้ามส่วนนี้)'); return null; }
    try { return fn(v); } catch (e) { extra.push(String(e.message || e)); return null; }
  }
  var mcq = optional(CONFIG.TAB_MCQ, parseMcq_);
  var written = optional(CONFIG.TAB_WRITTEN, parseWritten_);
  var feedback = optional(CONFIG.TAB_FEEDBACK, parseFeedback_);
  var D = buildClassData_(summary, mcq, written, feedback);
  D.warnings = extra.concat(D.warnings);
  return D;
}

function loadClassData_(settings, forceFresh) {
  if (!forceFresh) {
    var cached = cacheGetJson_('classdata');
    if (cached) return cached;
  }
  var D = readClassData_(settings);
  cachePutJson_('classdata', D, CONFIG.CACHE_DATA_SECONDS);
  return D;
}

/* ---------- รายการไฟล์ PDF ในโฟลเดอร์ ---------- */

function listPdfMap_(settings, forceFresh) {
  if (!forceFresh) {
    var cached = cacheGetJson_('pdfmap');
    if (cached) return cached;
  }
  if (!settings.pdf_folder_id) throw new Error('ยังไม่ได้ตั้งค่า pdf_folder_id ในแท็บ Settings');
  var map = {};
  var files = DriveApp.getFolderById(settings.pdf_folder_id).getFiles();
  while (files.hasNext()) {
    var f = files.next();
    if (f.getMimeType() === 'application/pdf') map[normalizeFileName_(f.getName())] = f.getId();
  }
  cachePutJson_('pdfmap', map, CONFIG.CACHE_PDFMAP_SECONDS);
  return map;
}

/* ===== Auth.gs ===== */
/**
 * ลงทะเบียน / เข้าสู่ระบบ / เซสชัน
 *
 * - รหัสผ่านเก็บเป็น PBKDF2-HMAC-SHA256 + salt รายคน + pepper (เก็บใน Script Properties ไม่อยู่ในชีต)
 * - ล็อกบัญชีชั่วคราวเมื่อกรอกผิดติดกัน; จำกัดจำนวนครั้งลงทะเบียนต่อรหัสนักศึกษา
 * - เซสชันเก็บฝั่งเซิร์ฟเวอร์ (CacheService) เพิกถอนได้ ไม่ใช้คุกกี้
 */

var USER_COLS_ = ['studentId', 'name', 'salt', 'hash', 'iter', 'registeredAt', 'lastLoginAt', 'failed', 'lockedUntil'];
var CODE_COLS_ = ['studentId', 'name', 'code', 'issuedAt', 'usedAt'];
var GENERIC_LOGIN_ERROR_ = 'รหัสนักศึกษาหรือรหัสผ่านไม่ถูกต้อง (ถ้ายังไม่เคยลงทะเบียน ให้ไปที่แท็บ "ลงทะเบียน" ก่อน)';

function fail_(msg, extra) {
  var r = { ok: false, error: msg };
  if (extra) for (var k in extra) r[k] = extra[k];
  return r;
}

/* ---------- แฮช ---------- */

function sha256Hex_(str) {
  return bytesToHex_(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, str, Utilities.Charset.UTF_8));
}

/** PBKDF2-HMAC-SHA256 (1 บล็อก = 32 ไบต์) -> hex */
function pbkdf2Hex_(password, saltStr, iterations) {
  var key = Utilities.newBlob(password).getBytes();
  var salt = Utilities.newBlob(saltStr).getBytes().concat([0, 0, 0, 1]);
  var u = Utilities.computeHmacSha256Signature(salt, key);
  var t = u.slice();
  for (var i = 1; i < iterations; i++) {
    u = Utilities.computeHmacSha256Signature(u, key);
    for (var k = 0; k < t.length; k++) t[k] ^= u[k];
  }
  return bytesToHex_(t);
}

function getPepper_() {
  var v = PropertiesService.getScriptProperties().getProperty('PEPPER');
  if (!v) throw new Error('ยังไม่ได้ตั้งค่าระบบ: รันเมนู Score Portal > ตั้งค่าเริ่มต้น');
  return v;
}

function hashPassword_(password, salt, iterations) {
  return pbkdf2Hex_(String(password), salt + '|' + getPepper_(), iterations);
}

function randomHex_(bytesLen) {
  var s = '';
  while (s.length < bytesLen * 2) s += Utilities.getUuid().replace(/-/g, '');
  return s.slice(0, bytesLen * 2);
}

/* ---------- จำกัดจำนวนครั้ง ---------- */

function throttle_(bucket, max, windowSec) {
  var cache = CacheService.getScriptCache();
  var now = Date.now(), n = 0, start = now;
  var raw = cache.get(bucket);
  if (raw) {
    var p = raw.split('|');
    n = parseInt(p[0], 10) || 0;
    start = parseInt(p[1], 10) || now;
    if (now - start > windowSec * 1000) { n = 0; start = now; }
  }
  if (n >= max) return false;
  cache.put(bucket, (n + 1) + '|' + start, windowSec);
  return true;
}

/* ---------- เซสชัน ---------- */

function createSession_(idKey, hours) {
  var token = randomHex_(32);
  var ttl = Math.min(21600, Math.floor(hours * 3600)); // CacheService สูงสุด 6 ชม.
  CacheService.getScriptCache().put('sess:' + sha256Hex_(token), idKey + '|' + Date.now(), ttl);
  return { token: token, expiresAt: Date.now() + ttl * 1000 };
}

/** คืนรหัสนักศึกษา (ตัวเลขล้วน) ของเซสชัน หรือ null */
function getSession_(token) {
  if (typeof token !== 'string' || token.length !== 64 || !/^[0-9a-f]+$/.test(token)) return null;
  var cache = CacheService.getScriptCache();
  var raw = cache.get('sess:' + sha256Hex_(token));
  if (!raw) return null;
  var p = raw.split('|');
  var revoked = parseInt(cache.get('revoked:' + p[0]), 10);
  if (revoked && parseInt(p[1], 10) <= revoked) return null;
  return p[0];
}

function destroySession_(token) {
  if (typeof token !== 'string' || token.length !== 64) return;
  CacheService.getScriptCache().remove('sess:' + sha256Hex_(token));
}

/** เพิกถอนทุกเซสชันของนักศึกษา (ใช้ตอนรีเซ็ตรหัสผ่าน) */
function revokeSessions_(idKey) {
  CacheService.getScriptCache().put('revoked:' + idKey, String(Date.now()), 21600);
}

/* ---------- ชีต Users ---------- */

function findRowByStudent_(sheet, idKey, ncols) {
  var last = sheet.getLastRow();
  if (last < 2) return null;
  var vals = sheet.getRange(2, 1, last - 1, ncols).getValues();
  for (var i = 0; i < vals.length; i++) {
    if (normalizeId_(vals[i][0]) === idKey) return { row: i + 2, data: vals[i] };
  }
  return null;
}

function userFromRow_(r) {
  return {
    row: r.row, id: r.data[0], name: r.data[1], salt: String(r.data[2]), hash: String(r.data[3]),
    iter: parseInt(r.data[4], 10) || CONFIG.KDF_ITERATIONS, failed: parseInt(r.data[7], 10) || 0,
    lockedUntil: r.data[8] ? new Date(r.data[8]).getTime() : 0
  };
}

/* ---------- ลงทะเบียน ---------- */

function verifyByCode_(idKey, codeRaw) {
  var sh = getTab_(CONFIG.TAB_CODES);
  var r = findRowByStudent_(sh, idKey, CODE_COLS_.length);
  var input = String(codeRaw == null ? '' : codeRaw).replace(/\s|-/g, '').toUpperCase();
  if (!r || !input) return { ok: false, error: 'รหัสยืนยันไม่ถูกต้อง' };
  if (r.data[4]) return { ok: false, error: 'รหัสยืนยันนี้ถูกใช้ไปแล้ว หากเป็นของท่านโปรดติดต่อผู้สอน' };
  var stored = String(r.data[2]).replace(/\s|-/g, '').toUpperCase();
  if (!safeEqual_(stored, input)) return { ok: false, error: 'รหัสยืนยันไม่ถูกต้อง' };
  return { ok: true, row: r.row };
}

function register_(p) {
  p = p || {};
  var settings = getSettings_();
  var idKey = normalizeId_(p.studentId);
  if (idKey.length < 8) return fail_('รหัสนักศึกษาไม่ถูกต้อง');
  if (!throttle_('reg:' + idKey, CONFIG.MAX_REGISTER_ATTEMPTS, CONFIG.REGISTER_WINDOW_SECONDS)) {
    return fail_('ลองหลายครั้งเกินไป กรุณารอสักครู่ (ประมาณ 15 นาที) แล้วลองใหม่');
  }

  var D = loadClassData_(settings);
  var idx = findStudent_(D, idKey);
  if (idx < 0) return fail_('ไม่พบรหัสนักศึกษานี้ในรายชื่อ กรุณาตรวจสอบรหัสอีกครั้ง');
  var stu = D.students[idx];

  var codeRow = null;
  if (settings.register_verify === 'code') {
    var v = verifyByCode_(idKey, p.code);
    if (!v.ok) { audit_(idKey, 'register_fail', 'code'); return fail_(v.error); }
    codeRow = v.row;
  } else if (normalizeName_(p.name) !== normalizeName_(stu.name)) {
    audit_(idKey, 'register_fail', 'name');
    return fail_('ชื่อ-สกุลไม่ตรงกับรายชื่อ (พิมพ์ชื่อและนามสกุลให้ตรงกับทะเบียน ไม่จำเป็นต้องใส่คำนำหน้า)');
  }

  var pwErr = validatePassword_(p.password, idKey, settings.min_password_length);
  if (pwErr) return fail_(pwErr);

  var salt = randomHex_(16);
  var hash = hashPassword_(p.password, salt, CONFIG.KDF_ITERATIONS);

  var lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    var users = getTab_(CONFIG.TAB_USERS);
    if (findRowByStudent_(users, idKey, USER_COLS_.length)) {
      return fail_('รหัสนักศึกษานี้ลงทะเบียนแล้ว ให้เข้าสู่ระบบ — ถ้าลืมรหัสผ่านโปรดติดต่อผู้สอนเพื่อรีเซ็ต');
    }
    var now = new Date().toISOString();
    users.appendRow([stu.id, stu.name, salt, hash, CONFIG.KDF_ITERATIONS, now, now, 0, '']);
    if (codeRow) getTab_(CONFIG.TAB_CODES).getRange(codeRow, 5).setValue(now);
  } finally {
    lock.releaseLock();
  }
  audit_(idKey, 'register_ok', settings.register_verify);
  var s = createSession_(idKey, settings.session_hours);
  return { ok: true, token: s.token, expiresAt: s.expiresAt, name: stu.name };
}

/* ---------- เข้าสู่ระบบ ---------- */

function login_(p) {
  p = p || {};
  var settings = getSettings_();
  var idKey = normalizeId_(p.studentId);
  var password = String(p.password == null ? '' : p.password);
  if (idKey.length < 8 || !password || password.length > 128) return fail_(GENERIC_LOGIN_ERROR_);

  var users = getTab_(CONFIG.TAB_USERS);
  var found = findRowByStudent_(users, idKey, USER_COLS_.length);
  if (!found) { audit_(idKey, 'login_fail', 'no_user'); return fail_(GENERIC_LOGIN_ERROR_); }
  var u = userFromRow_(found);

  var now = Date.now();
  if (u.lockedUntil > now) {
    var mins = Math.ceil((u.lockedUntil - now) / 60000);
    return fail_('กรอกรหัสผ่านผิดหลายครั้ง บัญชีถูกล็อกชั่วคราว กรุณารออีกประมาณ ' + mins + ' นาที');
  }

  var ok = safeEqual_(hashPassword_(password, u.salt, u.iter), u.hash);

  var lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    var cur = findRowByStudent_(users, idKey, USER_COLS_.length);
    if (!cur) return fail_(GENERIC_LOGIN_ERROR_);
    var row = cur.data.slice(0, USER_COLS_.length);
    if (ok) {
      row[6] = new Date().toISOString();
      row[7] = 0;
      row[8] = '';
    } else {
      var failed = (parseInt(row[7], 10) || 0) + 1;
      if (failed >= CONFIG.MAX_FAILED_LOGINS) {
        row[7] = 0;
        row[8] = new Date(now + CONFIG.LOCK_MINUTES * 60000).toISOString();
      } else {
        row[7] = failed;
      }
    }
    users.getRange(cur.row, 1, 1, USER_COLS_.length).setValues([row]);
  } finally {
    lock.releaseLock();
  }

  if (!ok) { audit_(idKey, 'login_fail', 'bad_password'); return fail_(GENERIC_LOGIN_ERROR_); }
  audit_(idKey, 'login_ok', '');
  var s = createSession_(idKey, settings.session_hours);
  return { ok: true, token: s.token, expiresAt: s.expiresAt, name: u.name };
}

/* ===== Code.gs ===== */
/**
 * จุดเข้าของเว็บแอป + API ที่หน้าเว็บเรียกผ่าน google.script.run
 *
 * ข้อควรระวัง: ฟังก์ชันระดับบนสุดที่ "ไม่ลงท้ายด้วย _" ใครก็เรียกผ่านหน้าเว็บได้
 * ดังนั้นฟังก์ชัน api_* ทุกตัวต้องตรวจเซสชันเอง และตัวช่วยอื่นต้องลงท้ายด้วย _
 */

function doGet(e) {
  var boot = { title: '020325201 ADV.STRUCTURAL', subtitle: '', notice: '', published: false, registerVerify: 'name', ready: true };
  try {
    var s = getSettings_();
    boot = {
      title: s.course_title, subtitle: s.course_subtitle, notice: s.notice,
      published: s.published, registerVerify: s.register_verify, ready: true
    };
  } catch (e) {
    console.error('doGet settings: ' + e);
    boot.ready = false;
  }
  // หน้าผู้ดูแล: เปิดได้เฉพาะเมื่อลิงก์มี ?admin=<คีย์ลับ> ที่ถูกต้อง คีย์ผิดจะได้หน้านักศึกษาปกติ (ไม่บอกใบ้)
  // ตัวหน้าผู้ดูแลยังต้องกรอกรหัสผ่านผู้ดูแลอีกชั้น (ดู AdminApi.gs)
  var adminKey = e && e.parameter && e.parameter.admin;
  if (adminKey && checkAdminKey_(adminKey)) { boot.admin = true; boot.adminKey = String(adminKey); }
  var t = HtmlService.createTemplateFromFile('Index');
  t.boot = jsonForScript_(boot);
  return t.evaluate()
    .setTitle('ประกาศคะแนน · ' + boot.title)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

/** ใส่ JSON ลงใน <script> อย่างปลอดภัย */
function jsonForScript_(obj) {
  return JSON.stringify(obj)
    .replace(/</g, '\\u003c').replace(/>/g, '\\u003e').replace(/&/g, '\\u0026')
    .replace(/\u2028/g, '\\u2028').replace(/\u2029/g, '\\u2029');
}

function include(name) {
  return HtmlService.createHtmlOutputFromFile(name).getContent();
}

/** ห่อ API: จับข้อผิดพลาด ไม่ส่งรายละเอียดภายในกลับไปหน้าเว็บ */
function guard_(fn) {
  try {
    return fn();
  } catch (e) {
    console.error('API error: ' + (e && e.stack ? e.stack : e));
    return fail_('ระบบขัดข้องชั่วคราว กรุณาลองใหม่อีกครั้ง หากยังไม่ได้ให้แจ้งผู้สอน', { server: true });
  }
}

function api_register(payload) {
  return guard_(function () { return register_(payload); });
}

function api_login(payload) {
  return guard_(function () { return login_(payload); });
}

function api_logout(token) {
  return guard_(function () { destroySession_(token); return { ok: true }; });
}

function api_dashboard(token) {
  return guard_(function () {
    var idKey = getSession_(token);
    if (!idKey) return fail_('เซสชันหมดอายุ กรุณาเข้าสู่ระบบใหม่', { expired: true });
    var settings = getSettings_();
    var D = loadClassData_(settings);
    var idx = findStudent_(D, idKey);
    if (idx < 0) return fail_('ไม่พบรหัสนักศึกษาของท่านในชีตคะแนน กรุณาติดต่อผู้สอน');
    var me = D.students[idx];
    if (!settings.published) {
      return { ok: true, published: false, student: { id: me.id, name: me.name }, notice: settings.notice };
    }
    return {
      ok: true, published: true, notice: settings.notice,
      course: { title: settings.course_title, subtitle: settings.course_subtitle },
      data: buildDashboard_(D, idKey, settings)
    };
  });
}

/** ส่ง PDF ของนักศึกษาที่ล็อกอินอยู่เท่านั้น (ไม่รับรหัสไฟล์จากหน้าเว็บ) */
function api_pdf(token) {
  return guard_(function () {
    var idKey = getSession_(token);
    if (!idKey) return fail_('เซสชันหมดอายุ กรุณาเข้าสู่ระบบใหม่', { expired: true });
    var settings = getSettings_();
    if (!settings.published || !settings.show_pdf) return fail_('ยังไม่เปิดให้ดูไฟล์ PDF');
    var D = loadClassData_(settings);
    var idx = findStudent_(D, idKey);
    if (idx < 0) return fail_('ไม่พบรหัสนักศึกษาของท่านในชีตคะแนน');
    var res = pdfResponse_(D.students[idx], settings);
    if (res.ok) audit_(idKey, 'pdf_view', '');
    return res;
  });
}

/** อ่านไฟล์ PDF ของนักศึกษาจากโฟลเดอร์ -> {ok, name, base64} (ใช้ร่วมกับหน้าผู้ดูแล) */
function pdfResponse_(me, settings) {
  var fileId = resolvePdfId_(me, listPdfMap_(settings, false));
  if (!fileId) fileId = resolvePdfId_(me, listPdfMap_(settings, true)); // รีเฟรชรายการไฟล์หนึ่งครั้ง
  if (!fileId) return fail_('ยังไม่พบไฟล์ PDF ในโฟลเดอร์ กรุณาติดต่อผู้สอน');
  var file = DriveApp.getFileById(fileId);
  if (file.getSize() > CONFIG.MAX_PDF_BYTES) return fail_('ไฟล์ PDF ใหญ่เกินกว่าจะแสดงบนหน้าเว็บ กรุณาติดต่อผู้สอน');
  return {
    ok: true,
    name: me.pdfName || file.getName(),
    base64: Utilities.base64Encode(file.getBlob().getBytes())
  };
}

/* ===== AdminApi.gs ===== */
/**
 * หน้าผู้ดูแล (Admin) — ดูข้อมูลของนักศึกษาทุกคน
 *
 * การเข้าถึงต้องผ่าน 2 ชั้น:
 *   1) คีย์ลับในลิงก์  <URL>/exec?admin=<ADMIN_KEY>  (สุ่ม 128 บิต เก็บใน Script Properties)
 *   2) รหัสผ่านผู้ดูแลกลางหนึ่งรหัส (เก็บเป็น PBKDF2 ใน Script Properties ไม่เก็บข้อความจริง)
 * ทุก api_admin* ต้องแนบโทเคนผู้ดูแลที่ได้หลังผ่านทั้งสองชั้น เซสชันผู้ดูแลแยกจากเซสชันนักศึกษา
 *
 * เหตุที่ไม่ให้หน้าล็อกอินนักศึกษารับ "รหัสกลาง": รหัสสั้นบนหน้าสาธารณะ ใครก็ลองได้
 * และสำเร็จแล้วเห็นคะแนนกับกระดาษคำตอบของทุกคน — ที่นี่รหัสกลางใช้ได้เฉพาะผู้ที่มีคีย์ลับในลิงก์
 * และมีล็อกอัตโนมัติเมื่อกรอกผิดติดกัน
 */

var ADMIN_SESSION_SECONDS_ = 7200;

function adminProps_() { return PropertiesService.getScriptProperties(); }

function getAdminKey_() { return adminProps_().getProperty('ADMIN_KEY') || ''; }

function checkAdminKey_(key) {
  var k = getAdminKey_();
  return !!k && typeof key === 'string' && key.length === k.length && safeEqual_(key, k);
}

/** ตั้ง/เปลี่ยนรหัสผ่านผู้ดูแล; คืนข้อความผิดพลาดหรือ '' ; เซสชันผู้ดูแลเดิมถูกเพิกถอน */
function setAdminPassword_(pw) {
  pw = String(pw == null ? '' : pw);
  if (pw.length < 4) return 'รหัสผ่านผู้ดูแลต้องยาวอย่างน้อย 4 ตัวอักษร';
  if (pw.length > 128) return 'รหัสผ่านยาวเกินไป';
  var salt = randomHex_(16), p = adminProps_();
  p.setProperty('ADMIN_SALT', salt);
  p.setProperty('ADMIN_ITER', String(CONFIG.KDF_ITERATIONS));
  p.setProperty('ADMIN_HASH', hashPassword_(pw, salt, CONFIG.KDF_ITERATIONS));
  p.setProperty('ADMIN_REVOKED_AT', String(Date.now()));
  return '';
}

function adminLogin_(key, password) {
  if (!checkAdminKey_(key)) return fail_('ลิงก์ผู้ดูแลไม่ถูกต้อง');
  var p = adminProps_(), hash = p.getProperty('ADMIN_HASH');
  if (!hash) return fail_('ยังไม่ได้ตั้งรหัสผ่านผู้ดูแล (เมนู Score Portal › ตั้งรหัสผ่านผู้ดูแล)');
  var cache = CacheService.getScriptCache();
  var lockedUntil = parseInt(cache.get('adminlock'), 10) || 0;
  if (lockedUntil > Date.now()) {
    return fail_('กรอกรหัสผ่านผิดหลายครั้ง ล็อกชั่วคราว กรุณารออีกประมาณ ' + Math.ceil((lockedUntil - Date.now()) / 60000) + ' นาที');
  }
  var iter = parseInt(p.getProperty('ADMIN_ITER'), 10) || CONFIG.KDF_ITERATIONS;
  var pw = String(password == null ? '' : password);
  var ok = pw.length > 0 && pw.length <= 128 && safeEqual_(hashPassword_(pw, p.getProperty('ADMIN_SALT') || '', iter), hash);
  if (!ok) {
    var n = (parseInt(cache.get('adminfail'), 10) || 0) + 1;
    if (n >= CONFIG.MAX_FAILED_LOGINS) {
      cache.put('adminlock', String(Date.now() + CONFIG.LOCK_MINUTES * 60000), CONFIG.LOCK_MINUTES * 60);
      cache.remove('adminfail');
    } else {
      cache.put('adminfail', String(n), 900);
    }
    audit_('ADMIN', 'admin_login_fail', '');
    return fail_('รหัสผ่านไม่ถูกต้อง');
  }
  cache.remove('adminfail');
  var token = randomHex_(32);
  cache.put('asess:' + sha256Hex_(token), String(Date.now()), ADMIN_SESSION_SECONDS_);
  audit_('ADMIN', 'admin_login_ok', '');
  return { ok: true, token: token };
}

function isAdminSession_(token) {
  if (typeof token !== 'string' || token.length !== 64 || !/^[0-9a-f]+$/.test(token)) return false;
  var raw = CacheService.getScriptCache().get('asess:' + sha256Hex_(token));
  if (!raw) return false;
  var revoked = parseInt(adminProps_().getProperty('ADMIN_REVOKED_AT'), 10) || 0;
  return parseInt(raw, 10) > revoked;
}

function adminExpired_() {
  return fail_('เซสชันผู้ดูแลหมดอายุ กรุณาเข้าสู่ระบบใหม่', { expired: true });
}

function toIso_(v) {
  if (!v) return '';
  return v.toISOString ? v.toISOString() : String(v);
}

/** ภาพรวมทุกคน: คะแนน อันดับ สถานะลงทะเบียน และมี PDF หรือไม่ */
function adminOverview_() {
  var settings = getSettings_();
  var D = loadClassData_(settings);
  var mode = TOTAL_LABELS_[settings.total_mode] ? settings.total_mode : 'official';
  var totals = D.students.map(function (s) { return totalFor_(s, mode); });
  var ranks = competitionRanks_(totals);
  var floor0 = mode === 'mcq_floor0';

  var users = {};
  try {
    var sh = getTab_(CONFIG.TAB_USERS);
    if (sh.getLastRow() > 1) {
      sh.getRange(2, 1, sh.getLastRow() - 1, USER_COLS_.length).getValues().forEach(function (r) {
        users[normalizeId_(r[0])] = { registeredAt: toIso_(r[5]), lastLoginAt: toIso_(r[6]) };
      });
    }
  } catch (e) { /* ยังไม่มีแท็บ Users */ }

  var pdfMap = null;
  try { pdfMap = listPdfMap_(settings, false); } catch (e) { /* ยังไม่ตั้งโฟลเดอร์ */ }

  var hist = buildHistogram_(totals, 10);
  var registered = 0;
  var rows = D.students.map(function (s, i) {
    var u = users[s.idKey];
    if (u) registered++;
    var mcq = s.mcq.used == null ? null : (floor0 ? Math.max(0, s.mcq.used) : s.mcq.used);
    return {
      seq: s.seq, id: s.id, idKey: s.idKey, name: s.name, group: s.group,
      mcq: mcq, q1: s.w[0], q2: s.w[1], q3: s.w[2], written: s.wTotal,
      total: totals[i], rank: ranks[i],
      registered: !!u, lastLoginAt: u ? u.lastLoginAt : '',
      pdf: pdfMap ? !!resolvePdfId_(s, pdfMap) : null
    };
  });
  return {
    ok: true,
    published: !!settings.published,
    course: { title: settings.course_title, subtitle: settings.course_subtitle },
    totalMode: mode, totalNote: TOTAL_LABELS_[mode].note,
    max: D.max, stats: statBlock_(totals),
    distribution: { width: hist.width, bins: hist.bins, you: -1 },
    registered: registered,
    rows: rows,
    warnings: D.warnings,
    builtAt: D.builtAt
  };
}

/** ข้อมูลเต็มของนักศึกษา 1 คน เหมือนที่เจ้าตัวเห็น แต่ผู้ดูแลเห็นแม้ยังไม่เปิดประกาศผล และเห็นความเห็นรายข้อ */
function adminStudent_(idKeyRaw) {
  var idKey = normalizeId_(idKeyRaw);
  var settings = getSettings_();
  var D = loadClassData_(settings);
  var view = {};
  Object.keys(settings).forEach(function (k) { view[k] = settings[k]; });
  view.show_leaderboard = true; view.show_feedback = true; view.show_pdf = true;
  var d = buildDashboard_(D, idKey, view);
  if (!d) return fail_('ไม่พบรหัสนักศึกษานี้ในชีตคะแนน');
  var registered = false;
  try { registered = !!findRowByStudent_(getTab_(CONFIG.TAB_USERS), idKey, USER_COLS_.length); } catch (e) { /* ignore */ }
  audit_('ADMIN', 'admin_view', idKey);
  return {
    ok: true, published: !!settings.published, registered: registered,
    course: { title: settings.course_title, subtitle: settings.course_subtitle },
    data: d
  };
}

function adminPdf_(idKeyRaw) {
  var idKey = normalizeId_(idKeyRaw);
  var settings = getSettings_();
  var D = loadClassData_(settings);
  var idx = findStudent_(D, idKey);
  if (idx < 0) return fail_('ไม่พบรหัสนักศึกษานี้ในชีตคะแนน');
  var res = pdfResponse_(D.students[idx], settings);
  if (res.ok) audit_('ADMIN', 'admin_pdf', idKey);
  return res;
}

/* ---------- API สำหรับหน้าผู้ดูแล (ทุกตัวตรวจโทเคนผู้ดูแลเอง) ---------- */

function api_adminLogin(key, password) {
  return guard_(function () { return adminLogin_(key, password); });
}

function api_adminLogout(token) {
  return guard_(function () {
    if (typeof token === 'string' && token.length === 64) CacheService.getScriptCache().remove('asess:' + sha256Hex_(token));
    return { ok: true };
  });
}

function api_adminOverview(token) {
  return guard_(function () { return isAdminSession_(token) ? adminOverview_() : adminExpired_(); });
}

function api_adminStudent(token, idKey) {
  return guard_(function () { return isAdminSession_(token) ? adminStudent_(idKey) : adminExpired_(); });
}

function api_adminPdf(token, idKey) {
  return guard_(function () { return isAdminSession_(token) ? adminPdf_(idKey) : adminExpired_(); });
}

/* ===== Admin.gs ===== */
/**
 * เมนูผู้สอนในชีตฐานข้อมูล: เมนู "Score Portal"
 *
 * ทุกฟังก์ชัน admin* ตรวจสิทธิ์ด้วย assertAdmin_() เพราะฟังก์ชันที่ไม่ลงท้าย _ ถูกเรียกจากหน้าเว็บได้
 * ผู้เข้าชมเว็บ (execute as deployer) จะมี ActiveUser ≠ EffectiveUser จึงถูกปฏิเสธ
 */

function onOpen() {
  try {
    SpreadsheetApp.getUi().createMenu('Score Portal')
      .addItem('1) ตั้งค่าเริ่มต้น (ครั้งแรก)', 'adminSetup')
      .addItem('2) วางลิงก์ไฟล์คะแนนและโฟลเดอร์ PDF', 'adminConfigure')
      .addItem('3) ตั้งรหัสผ่านผู้ดูแล (หน้าดูข้อมูลทุกคน)', 'adminSetPassword')
      .addItem('4) ตรวจสอบข้อมูลคะแนนและ PDF', 'adminCheckData')
      .addSeparator()
      .addItem('เปิดประกาศผล', 'adminPublishOn')
      .addItem('ปิดประกาศผล (ล็อก)', 'adminPublishOff')
      .addSeparator()
      .addItem('แสดงลิงก์ผู้ดูแล', 'adminShowLink')
      .addItem('สร้างลิงก์ผู้ดูแลใหม่ (ถ้าลิงก์รั่ว)', 'adminRotateKey')
      .addSeparator()
      .addItem('สร้างรหัสยืนยันรายคน (โหมด code)', 'adminGenerateCodes')
      .addItem('รีเซ็ตรหัสผ่านนักศึกษา', 'adminResetPassword')
      .addItem('ล้างแคช (หลังแก้ชีตคะแนน)', 'adminClearCache')
      .addToUi();
  } catch (e) { /* ไม่ได้เปิดจากชีต */ }
}

function assertAdmin_() {
  var eff = '', act = '';
  try { eff = Session.getEffectiveUser().getEmail(); } catch (e) { /* ignore */ }
  try { act = Session.getActiveUser().getEmail(); } catch (e) { /* ignore */ }
  if (!eff || !act || eff.toLowerCase() !== act.toLowerCase()) {
    throw new Error('ต้องเป็นผู้ดูแลระบบ');
  }
}

function alert_(msg) {
  try { SpreadsheetApp.getUi().alert(msg); } catch (e) { console.log(msg); }
}

function ensureTab_(ss, name, headers) {
  var sh = ss.getSheetByName(name);
  if (!sh) sh = ss.insertSheet(name);
  if (headers && sh.getLastRow() === 0) {
    sh.getRange(1, 1, 1, headers.length).setValues([headers]).setFontWeight('bold');
    sh.setFrozenRows(1);
  }
  return sh;
}

function adminSetup() {
  assertAdmin_();
  var ss = SpreadsheetApp.getActiveSpreadsheet() || getDb_();
  var props = PropertiesService.getScriptProperties();
  props.setProperty('DB_ID', ss.getId());
  if (!props.getProperty('PEPPER')) props.setProperty('PEPPER', randomHex_(32));
  if (!props.getProperty('ADMIN_KEY')) props.setProperty('ADMIN_KEY', randomHex_(16)); // คีย์ลับในลิงก์ผู้ดูแล

  var settings = ensureTab_(ss, CONFIG.TAB_SETTINGS, ['key', 'value', 'คำอธิบาย']);
  var existing = {};
  settings.getDataRange().getValues().forEach(function (r) { existing[cell_(r[0])] = true; });
  SETTINGS_DEFAULTS.forEach(function (d) {
    if (!existing[d[0]]) settings.appendRow([d[0], d[1], d[2]]);
  });
  settings.setColumnWidth(1, 190); settings.setColumnWidth(2, 260); settings.setColumnWidth(3, 620);

  var users = ensureTab_(ss, CONFIG.TAB_USERS, USER_COLS_);
  users.getRange('A:A').setNumberFormat('@'); // กันรหัสนักศึกษาถูกแปลงเป็นตัวเลข
  var codes = ensureTab_(ss, CONFIG.TAB_CODES, CODE_COLS_);
  codes.getRange('A:A').setNumberFormat('@');
  ensureTab_(ss, CONFIG.TAB_AUDIT, ['time', 'studentId', 'event', 'detail']);

  clearAllCaches_();
  alert_('ตั้งค่าเริ่มต้นเรียบร้อย\n\nขั้นต่อไป:\n1) แปลงไฟล์ .xlsx เป็น Google Sheets แล้วใส่ ID ที่ Settings > scores_spreadsheet_id\n2) เมนู Score Portal > ตรวจสอบข้อมูลคะแนนและ PDF\n3) เมื่อผู้สอนตรวจทานคะแนนแล้ว จึงเมนู เปิดประกาศผล\n\nแท็บ Users / Codes / Audit มีข้อมูลนักศึกษา โปรดอย่าแชร์ชีตนี้ให้ผู้อื่น');
}

function setSetting_(key, value) {
  var sh = getTab_(CONFIG.TAB_SETTINGS);
  var rows = sh.getDataRange().getValues();
  for (var r = 0; r < rows.length; r++) {
    if (cell_(rows[r][0]) === key) { sh.getRange(r + 1, 2).setValue(value); clearAllCaches_(); return; }
  }
  sh.appendRow([key, value, '']);
  clearAllCaches_();
}

function adminPublishOn() {
  assertAdmin_();
  setSetting_('published', true);
  alert_('เปิดประกาศผลแล้ว — นักศึกษาที่เข้าสู่ระบบจะเห็นคะแนน');
}

function adminPublishOff() {
  assertAdmin_();
  setSetting_('published', false);
  alert_('ปิดประกาศผลแล้ว — นักศึกษาจะเห็นเพียงข้อความรอประกาศ');
}

function adminClearCache() {
  assertAdmin_();
  clearAllCaches_();
  alert_('ล้างแคชแล้ว ข้อมูลล่าสุดจากชีตคะแนนจะถูกโหลดในการเข้าชมครั้งถัดไป');
}

/** รายงานตรวจข้อมูล: คืนบรรทัดข้อความ (ทดสอบได้) */
function buildCheckReport_(settings) {
  var lines = [];
  var D = readClassData_(settings);
  lines.push('นักศึกษาในชีตคะแนน: ' + D.students.length + ' คน');
  lines.push('คะแนนเต็ม: ปรนัย ' + D.max.mcq + ' / อัตนัยข้อละ ' + D.max.w.join(', ') + ' / รวม ' + D.max.total);

  var missingTotals = D.students.filter(function (s) { return s.totals.official == null; });
  if (missingTotals.length) lines.push('⚠ ไม่มีคะแนนรวม: ' + missingTotals.map(function (s) { return s.id; }).join(', '));
  if (settings.total_mode !== 'official') {
    var noAlt = D.students.filter(function (s) { return s.totals[settings.total_mode] == null; });
    if (noAlt.length) lines.push('⚠ total_mode=' + settings.total_mode + ' แต่ ' + noAlt.length + ' คนไม่มีคอลัมน์นี้ (จะใช้คะแนนรวมตามข้อสอบแทน)');
  }

  // ตรวจความสอดคล้องปรนัยรายข้อ กับ ถูก/ผิด/ไม่ตอบ ในแท็บสรุป
  if (D.mcq) {
    var mism = 0;
    D.students.forEach(function (s) {
      if (!s.answers) return;
      var c = 0, w = 0, b = 0;
      s.answers.forEach(function (a, k) {
        var key = D.mcq.key[D.mcq.items[k]];
        if (a == null) b++; else if (a === key) c++; else w++;
      });
      if (s.mcq.correct != null && (c !== s.mcq.correct || w !== s.mcq.wrong || b !== s.mcq.blank)) {
        mism++;
        lines.push('⚠ ปรนัยรายข้อไม่ตรงกับแท็บสรุป: ' + s.id + ' (รายข้อ ถูก/ผิด/ว่าง = ' + c + '/' + w + '/' + b +
          ', สรุป = ' + s.mcq.correct + '/' + s.mcq.wrong + '/' + s.mcq.blank + ')');
      }
    });
    if (!mism) lines.push('✓ ปรนัยรายข้อสอดคล้องกับแท็บสรุปทุกคน');
    if (Object.keys(D.mcq.key).length !== D.mcq.items.length) lines.push('⚠ เฉลยปรนัยไม่ครบทุกข้อ');
  }
  if (D.written) {
    var wm = 0;
    D.students.forEach(function (s) {
      if (!s.wd) return;
      s.wd.forEach(function (q, qi) {
        if (q.total != null && s.w[qi] != null && q.total !== s.w[qi]) {
          wm++;
          lines.push('⚠ อัตนัยข้อ ' + D.written.questions[qi].no + ' ไม่ตรงกับแท็บสรุป: ' + s.id + ' (' + q.total + ' ≠ ' + s.w[qi] + ')');
        }
      });
    });
    if (!wm) lines.push('✓ อัตนัยรายหัวข้อสอดคล้องกับแท็บสรุปทุกคน');
  }

  // PDF
  var map = listPdfMap_(settings, true);
  var noPdf = D.students.filter(function (s) { return !resolvePdfId_(s, map); });
  lines.push('ไฟล์ PDF ในโฟลเดอร์: ' + Object.keys(map).length + ' ไฟล์');
  if (noPdf.length) lines.push('⚠ ไม่พบ PDF ของ: ' + noPdf.map(function (s) { return s.id + ' ' + s.name; }).join(' ; '));
  else lines.push('✓ จับคู่ PDF ได้ครบทุกคน');

  D.warnings.forEach(function (w) { lines.push('⚠ ' + w); });
  lines.push('สถานะ: ' + (settings.published ? 'เปิดประกาศผลแล้ว' : 'ยังล็อกอยู่ (published = FALSE)'));
  lines.push('ความเห็นรายข้อ: ' + (settings.show_feedback ? 'เปิดให้นักศึกษาเห็น — โปรดตรวจข้อความก่อน' : 'ปิด (ปลอดภัย)'));
  return lines;
}

function adminCheckData() {
  assertAdmin_();
  clearAllCaches_();
  var lines;
  try {
    lines = buildCheckReport_(getSettings_());
  } catch (e) {
    lines = ['✗ อ่านข้อมูลไม่สำเร็จ: ' + (e && e.message ? e.message : e)];
  }
  alert_(lines.slice(0, 40).join('\n') + (lines.length > 40 ? '\n… (อีก ' + (lines.length - 40) + ' บรรทัด ดูใน Logs)' : ''));
  console.log(lines.join('\n'));
}

/** ดึง ID ไฟล์/โฟลเดอร์จากลิงก์ Google Drive/Docs หรือรับ ID ล้วนๆ; คืน '' ถ้าไม่เข้ารูปแบบ */
function extractDriveId_(text) {
  var t = String(text == null ? '' : text).trim();
  if (!t) return '';
  var m = /\/(?:d|folders)\/([A-Za-z0-9_-]+)/.exec(t) || /[?&]id=([A-Za-z0-9_-]+)/.exec(t);
  if (m) return m[1];
  return /^[A-Za-z0-9_-]{20,}$/.test(t) ? t : '';
}

/** วางลิงก์ไฟล์คะแนน (Google Sheets) และโฟลเดอร์ PDF แล้วตรวจข้อมูลให้ทันที */
function adminConfigure() {
  assertAdmin_();
  var ui = SpreadsheetApp.getUi();
  function ask(title, text) {
    var r = ui.prompt(title, text, ui.ButtonSet.OK_CANCEL);
    return r.getSelectedButton() === ui.Button.OK ? r.getResponseText() : null;
  }
  var sheetLink = ask('1/2 ไฟล์สรุปคะแนน', 'วางลิงก์ของไฟล์สรุปคะแนนที่แปลงเป็น Google Sheets แล้ว (เปิดไฟล์แล้วคัดลอกลิงก์จากแถบที่อยู่เบราว์เซอร์)\nเว้นว่างไว้ = ไม่เปลี่ยน');
  if (sheetLink === null) return;
  var folderLink = ask('2/2 โฟลเดอร์ PDF', 'วางลิงก์โฟลเดอร์ที่เก็บ PDF ที่ตรวจแล้ว\nเว้นว่างไว้ = ไม่เปลี่ยน');
  if (folderLink === null) return;
  var msgs = [];
  if (sheetLink.trim()) {
    var sid = extractDriveId_(sheetLink);
    if (!sid) return alert_('อ่านลิงก์ไฟล์คะแนนไม่ออก — ลองคัดลอกลิงก์ทั้งหมดจากแถบที่อยู่เบราว์เซอร์อีกครั้ง');
    setSetting_('scores_spreadsheet_id', sid);
    msgs.push('ตั้งไฟล์คะแนนแล้ว');
  }
  if (folderLink.trim()) {
    var fid = extractDriveId_(folderLink);
    if (!fid) return alert_('อ่านลิงก์โฟลเดอร์ไม่ออก — ลองคัดลอกลิงก์ทั้งหมดจากแถบที่อยู่เบราว์เซอร์อีกครั้ง');
    setSetting_('pdf_folder_id', fid);
    msgs.push('ตั้งโฟลเดอร์ PDF แล้ว');
  }
  clearAllCaches_();
  var lines;
  try {
    lines = buildCheckReport_(getSettings_());
  } catch (e) {
    lines = ['✗ อ่านข้อมูลไม่สำเร็จ: ' + (e && e.message ? e.message : e),
      'ตรวจว่าบัญชีนี้เปิดไฟล์/โฟลเดอร์นั้นได้ และไฟล์เป็น Google Sheets (ไม่ใช่ .xlsx)'];
  }
  alert_((msgs.length ? msgs.join(' · ') + '\n\n' : '') + lines.slice(0, 40).join('\n'));
}

var CODE_ALPHABET_ = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';

function makeActivationCode_() {
  var hex = randomHex_(8), out = '';
  for (var i = 0; i < 8; i++) {
    out += CODE_ALPHABET_.charAt(parseInt(hex.substr(i * 2, 2), 16) % CODE_ALPHABET_.length);
  }
  return out.slice(0, 4) + '-' + out.slice(4);
}

/** สร้างรหัสยืนยันให้นักศึกษาที่ยังไม่มีรหัส (ไม่ทับรหัสเดิม) */
function adminGenerateCodes() {
  assertAdmin_();
  var D = loadClassData_(getSettings_(), true);
  var sh = getTab_(CONFIG.TAB_CODES);
  var have = {};
  if (sh.getLastRow() > 1) {
    sh.getRange(2, 1, sh.getLastRow() - 1, 1).getValues().forEach(function (r) { have[normalizeId_(r[0])] = true; });
  }
  var added = 0, now = new Date().toISOString();
  D.students.forEach(function (s) {
    if (have[s.idKey]) return;
    sh.appendRow([s.id, s.name, makeActivationCode_(), now, '']);
    added++;
  });
  alert_('สร้างรหัสยืนยันใหม่ ' + added + ' รหัส (แท็บ Codes)\nแจกรหัสให้นักศึกษาแต่ละคนผ่านช่องทางส่วนตัว และตั้ง Settings > register_verify = code');
}

/** ลิงก์หน้าผู้ดูแล (ถ้า Deploy แล้วจะได้ URL เต็ม ไม่งั้นแสดงเฉพาะส่วนท้าย) */
function adminLink_() {
  var key = getAdminKey_();
  if (!key) throw new Error('ยังไม่ได้ตั้งค่า: เมนู ตั้งค่าเริ่มต้น');
  var base = '';
  try { base = ScriptApp.getService().getUrl() || ''; } catch (e) { /* ยังไม่ได้ Deploy */ }
  return base ? base + '?admin=' + key : '(URL เว็บแอป)/exec?admin=' + key;
}

function adminSetPassword() {
  assertAdmin_();
  var ui = SpreadsheetApp.getUi();
  var resp = ui.prompt('ตั้งรหัสผ่านผู้ดูแล',
    'รหัสผ่านกลางสำหรับหน้าผู้ดูแล (อย่างน้อย 4 ตัวอักษร)\nใช้ได้เฉพาะผู้ที่มีลิงก์ผู้ดูแล และล็อก 15 นาทีเมื่อกรอกผิด 5 ครั้งติด',
    ui.ButtonSet.OK_CANCEL);
  if (resp.getSelectedButton() !== ui.Button.OK) return;
  var pw = resp.getResponseText();
  var err = setAdminPassword_(pw);
  if (err) return alert_(err);
  var weak = pw.length < 8 || /^\d+$/.test(pw);
  alert_('ตั้งรหัสผ่านผู้ดูแลแล้ว (เซสชันผู้ดูแลเดิมถูกเพิกถอน)\n\nลิงก์ผู้ดูแล:\n' + adminLink_() +
    (weak ? '\n\n⚠ รหัสนี้สั้น/เดาง่าย ความปลอดภัยพึ่งลิงก์ลับเป็นหลัก — อย่าส่งลิงก์ผู้ดูแลให้ใคร และถ้าลิงก์รั่วให้สร้างลิงก์ใหม่' : ''));
}

function adminShowLink() {
  assertAdmin_();
  alert_('ลิงก์ผู้ดูแล (ห้ามแชร์ให้นักศึกษา):\n' + adminLink_() +
    (adminProps_().getProperty('ADMIN_HASH') ? '' : '\n\nยังไม่ได้ตั้งรหัสผ่านผู้ดูแล — เมนู ตั้งรหัสผ่านผู้ดูแล'));
}

function adminRotateKey() {
  assertAdmin_();
  adminProps_().setProperty('ADMIN_KEY', randomHex_(16));
  adminProps_().setProperty('ADMIN_REVOKED_AT', String(Date.now()));
  alert_('สร้างลิงก์ผู้ดูแลใหม่แล้ว (ลิงก์เดิมและเซสชันผู้ดูแลเดิมใช้ไม่ได้)\n\n' + adminLink_());
}

function resetPasswordFor_(idKey) {
  var lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    var users = getTab_(CONFIG.TAB_USERS);
    var r = findRowByStudent_(users, idKey, USER_COLS_.length);
    if (!r) return false;
    users.deleteRow(r.row);
    var codes = getTab_(CONFIG.TAB_CODES);
    var c = findRowByStudent_(codes, idKey, CODE_COLS_.length);
    if (c) codes.getRange(c.row, 5).setValue('');
  } finally {
    lock.releaseLock();
  }
  revokeSessions_(idKey);
  audit_(idKey, 'admin_reset', '');
  return true;
}

function adminResetPassword() {
  assertAdmin_();
  var ui = SpreadsheetApp.getUi();
  var resp = ui.prompt('รีเซ็ตรหัสผ่าน', 'กรอกรหัสนักศึกษา (นักศึกษาจะต้องลงทะเบียนใหม่):', ui.ButtonSet.OK_CANCEL);
  if (resp.getSelectedButton() !== ui.Button.OK) return;
  var idKey = normalizeId_(resp.getResponseText());
  alert_(resetPasswordFor_(idKey) ? 'รีเซ็ตแล้ว: ' + idKey : 'ไม่พบผู้ใช้ที่ลงทะเบียนด้วยรหัส ' + idKey);
}
