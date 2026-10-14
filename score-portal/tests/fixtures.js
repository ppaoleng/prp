'use strict';
/**
 * ข้อมูลสมมติ (ชื่อ/รหัส/คะแนนไม่ใช่ข้อมูลจริง) ที่จำลอง "โครงสร้าง" ของไฟล์
 * สรุปคะแนน_ข้อสอบปลายภาค ป.โท (ร่าง).xlsx: แถวหัวเรื่อง, หัวตาราง, แถวเฉลย/คะแนนเต็ม, แถวสถิติท้ายตาราง
 */

const KEY = ['ค', 'ข', 'ค', 'ง', 'ก', 'ข', 'ง', 'ก', 'ค', 'ง', 'ข', 'ค', 'ก', 'ข', 'ก'];
const WRONG = { 'ก': 'ข', 'ข': 'ค', 'ค': 'ง', 'ง': 'ก' };

/** ตอบตาม spec: 'c' ถูก, 'w' ผิด, '-' ไม่ตอบ */
function answersFrom(spec) {
  return spec.split('').map((ch, i) => (ch === 'c' ? KEY[i] : ch === 'w' ? WRONG[KEY[i]] : '-'));
}

const Q_ITEMS = [
  ['แบบจำลอง/[k]', 'FEF', 'ประกอบสมการ+ทรุดตัว', 'แก้ {d_f}', 'แรงปฏิกิริยา', 'แผนภาพ V,M'],
  ['Ay', 'By', 'Cy และ Mc', 'แผนภาพ V,M'],
  ['แบบจำลอง/[k]', 'FEF', 'ประกอบสมการ+ทรุดตัว', 'แก้ {d_f}', 'แรงปฏิกิริยา', 'แผนภาพ V,M']
];
const Q_MAX = [[4, 3, 4, 3, 3, 3], [5, 5, 5, 5], [4, 3, 4, 3, 3, 3]];

const STUDENTS = [
  { seq: 1, id: '69-999999-0001-1', name: 'นายทดสอบ หนึ่ง', ans: 'ccccccccccccccc', w: [[4, 3, 4, 3, 3, 3], [5, 5, 5, 5], [0, 0, 0, 0, 0, 0]], pdf: 'ตรวจแล้ว_01_นายทดสอบ หนึ่ง.pdf' },
  { seq: 2, id: '69-999999-0002-9', name: 'นางสาวทดสอบ สอง', ans: 'ccccccccccwwwww', w: [[2, 1, 0, 0, 0, 0], [3, 3, 3, 3], [0, 0, 0, 0, 0, 0]], pdf: 'ตรวจแล้ว_02_นางสาวทดสอบ สอง.pdf' },
  { seq: 3, id: '69-999999-0003-7', name: 'นายตัวอย่าง สาม', ans: 'cccccccccccwwc-', w: [[1, 1, 0, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0, 0, 0]], pdf: 'ตรวจแล้ว_03_นายตัวอย่าง สาม.pdf' },
  { seq: 4, id: '69-999999-0004-5', name: 'นางสาวตัวอย่าง สี่', ans: 'cccccwwwwwwwwww', w: [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0, 0, 0]], pdf: 'ตรวจแล้ว_04_นางสาวตัวอย่าง สี่.pdf' },
  { seq: 5, id: '69-999999-0005-2', name: 'นายสมมติ ห้า', ans: 'ccccccccccc-wwc', w: [[1, 1, 0, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0, 0, 0]], pdf: 'ตรวจแล้ว_05_นายสมมติ ห้า.pdf' },
  { seq: 6, id: '69-999999-0006-0', name: 'นางสาวสมมติ หก', ans: 'ccc------------', w: [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0, 0, 0]], pdf: 'ตรวจแล้ว_06_นางสาวสมมติ หก.pdf' }
];

const sum = (a) => a.reduce((x, y) => x + y, 0);

function derive(s) {
  const answers = answersFrom(s.ans);
  const correct = answers.filter((a, i) => a === KEY[i]).length;
  const blank = answers.filter((a) => a === '-').length;
  const wrong = 15 - correct - blank;
  const formula = correct * 3 - wrong * 2 - blank;
  const used = Math.min(40, formula);
  const wq = s.w.map(sum);
  const wTotal = sum(wq);
  return { answers, correct, wrong, blank, formula, used, wq, wTotal, official: used + wTotal, floor0: Math.max(0, used) + wTotal };
}

function summaryTab() {
  const rows = [
    ['สรุปคะแนน สรุปคะแนนข้อสอบปลายภาค 000000000 ทดสอบ (ฉบับร่างให้ผู้สอนตรวจทาน)'],
    ['ปรนัย 15 ข้อ (+3/-2/-1 สูงสุด 40) + อัตนัย 3 ข้อ ข้อละ 20 = 100 คะแนน'],
    ['ลำดับ', 'รหัสนักศึกษา', 'ชื่อ-สกุล', 'กลุ่ม (ไฟล์ Excel)', 'ปรนัยถูก', 'ปรนัยผิด', 'ไม่ตอบ', 'ปรนัยตามสูตร',
      'ปรนัยที่ใช้ (สูงสุด 40)', 'อัตนัยข้อ 1 (20)', 'อัตนัยข้อ 2 (20)', 'อัตนัยข้อ 3 (20)', 'อัตนัยรวม (60)',
      'คะแนนรวม (100) ตามที่ข้อสอบกำหนด', 'รวม ถ้าปรนัยขั้นต่ำ 0', 'รวม ถ้าข้อ 2 ไม่ให้คะแนนบางส่วน',
      'ไฟล์ PDF ที่ตรวจแล้ว', 'ข้อควรพิจารณา']
  ];
  STUDENTS.forEach((s) => {
    const d = derive(s);
    rows.push([s.seq, s.id, s.name, 'GRP-A', d.correct, d.wrong, d.blank, d.formula, d.used, d.wq[0], d.wq[1], d.wq[2],
      d.wTotal, d.official, d.floor0, d.official - 1, s.pdf,
      s.seq === 4 ? 'ผลเหมือนของลำดับที่ 3 ผู้สอนโปรดพิจารณา (บันทึกลับ)' : '']);
  });
  rows.push(['', '', 'คะแนนเฉลี่ย', '', '', '', '', '', 8.21, 3.05, 2.26, 1.16, 6.47, 14.68, 16.47, 12.42, '', '']);
  rows.push(['', '', 'สูงสุด', '', '', '', '', '', 40, 13, 9, 15, 24, 54, 54, 53, '', '']);
  rows.push(['', '', 'จำนวนผู้เข้าสอบ', '', '', '', '', '', '', '', '', '', '', STUDENTS.length, '', '', '', '']);
  return rows;
}

function mcqTab() {
  const rows = [
    ['ปรนัยรายข้อ ตอนที่ 1 ปรนัย 15 ข้อ: คำตอบของนักศึกษา เทียบเฉลย'],
    ['"-" = ไม่ตอบ'],
    ['ลำดับ', 'ชื่อ-สกุล', ...KEY.map((_, i) => 'ข้อ ' + (i + 1)), 'ถูก', 'ผิด', 'ไม่ตอบ', 'คะแนนตามสูตร (+3/-2/-1)'],
    ['เฉลย', 'เฉลยที่ใช้ตรวจ', ...KEY]
  ];
  STUDENTS.forEach((s) => {
    const d = derive(s);
    rows.push([s.seq, s.name, ...d.answers, d.correct, d.wrong, d.blank, d.formula]);
  });
  return rows;
}

function writtenTab() {
  const head = ['ลำดับ', 'ชื่อ-สกุล'];
  const max = ['เต็ม', 'คะแนนเต็ม'];
  Q_ITEMS.forEach((items, q) => {
    items.forEach((label, k) => { head.push('ข้อ' + (q + 1) + ' ' + label); max.push(Q_MAX[q][k]); });
    head.push('ข้อ ' + (q + 1) + ' รวม'); max.push(sum(Q_MAX[q]));
  });
  head.push('อัตนัยรวม'); max.push(60);
  const rows = [['อัตนัยรายข้อ ตอนที่ 2 อัตนัย: คะแนนรายหัวข้อ (ร่าง)'], head, max];
  STUDENTS.forEach((s) => {
    const r = [s.seq, s.name];
    s.w.forEach((items) => { r.push(...items, sum(items)); });
    r.push(sum(s.w.map(sum)));
    rows.push(r);
  });
  return rows;
}

function feedbackTab() {
  return [
    ['ข้อควรพิจารณา ข้อควรพิจารณาและความเห็นรายข้อ (ผู้ช่วยตรวจ ฉบับร่าง)'],
    ['ลำดับ', 'ชื่อ-สกุล', 'ข้อ', 'ความเห็น'],
    [1, STUDENTS[0].name, 'อัตนัย 1', 'แก้สมการถูกต้องทุกขั้นตอน'],
    [1, STUDENTS[0].name, 'ข้อควรพิจารณา', 'บันทึกภายในถึงผู้สอน ห้ามแสดง'],
    [2, STUDENTS[1].name, 'อัตนัย 2', 'ตารางคำตอบไม่ตรงเฉลย ผู้สอนโปรดพิจารณา'],
    [2, STUDENTS[1].name, 'ปรนัยข้อ 5', 'ขีดเส้นใต้จางๆ ที่ ก ตีความว่าเลือก ก'],
    [4, STUDENTS[3].name, 'อัตนัย 1', 'ผลเหมือนของลำดับที่ 3'],
    [4, STUDENTS[3].name, 'อัตนัย 3', 'ไม่ได้ทำ (พบเฉพาะโจทย์)']
  ];
}

module.exports = { KEY, STUDENTS, derive, summaryTab, mcqTab, writtenTab, feedbackTab, Q_ITEMS, Q_MAX };
