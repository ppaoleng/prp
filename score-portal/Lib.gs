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
