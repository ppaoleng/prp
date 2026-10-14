'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const F = require('./fixtures');
const { createEnv, createReadyEnv } = require('./harness');

// ผลจากภายใน vm มี prototype คนละ realm -> แปลงเป็น plain ก่อนเทียบ
const plain = (x) => JSON.parse(JSON.stringify(x));
const S = F.STUDENTS;
const idOf = (i) => S[i].id;
const nameOf = (i) => S[i].name;
const PW = 'Passw0rd!x';

/* ---------- ฟังก์ชันล้วน ---------- */

test('normalizeId_: รับขีด ช่องว่าง เลขไทย', () => {
  const { ctx } = createEnv();
  assert.equal(ctx.normalizeId_('69-020328-4601-3'), '6902032846013');
  assert.equal(ctx.normalizeId_(' ๖๙ ๐๒๐๓๒๘ ๔๖๐๑ ๓ '), '6902032846013');
  assert.equal(ctx.normalizeId_(null), '');
});

test('normalizeName_: ตัดคำนำหน้า/ช่องว่าง ให้ชื่อเทียบกันได้', () => {
  const { ctx } = createEnv();
  const n = (s) => ctx.normalizeName_(s);
  assert.equal(n('นางสาวแสงดาว ธิตา'), n('แสงดาว ธิตา'));
  assert.equal(n('นางสาวแสงดาว ธิตา'), n('น.ส. แสงดาว  ธิตา'));
  assert.equal(n('นายกติกา ไชยศิริ'), n('กติกา ไชยศิริ'));
  assert.notEqual(n('นายกติกา ไชยศิริ'), n('นายกติกา ไชยศรี'));
  assert.equal(n('นางสาวสมมติ หก'), 'สมมติหก');
  assert.equal(n('  Mr. John  Doe '), 'johndoe');
});

test('validatePassword_', () => {
  const { ctx } = createEnv();
  const v = (pw) => ctx.validatePassword_(pw, '6902032846013', 8);
  assert.match(v('abc123'), /อย่างน้อย 8/);
  assert.match(v('abcdefgh'), /ตัวอักษรและตัวเลข/);
  assert.match(v('12345678'), /ตัวอักษรและตัวเลข/);
  assert.match(v('aaaaaaaa'), /ตัวอักษรและตัวเลข|ง่ายเกินไป/);
  assert.match(v('69-020328-4601-3'), /ตัวอักษรและตัวเลข|ห้ามใช้รหัสนักศึกษา/);
  assert.match(v('abc6902032846013'), /ห้ามใช้รหัสนักศึกษา/);
  assert.equal(v('Passw0rd!x'), '');
  assert.equal(v('รหัสลับ12345'), '');
});

test('competitionRanks_ / percentAbove_ / histogram', () => {
  const { ctx } = createEnv();
  assert.deepEqual(plain(ctx.competitionRanks_([54, 40, 40, 10, null, -5])), [1, 2, 2, 4, null, 5]);
  assert.equal(ctx.percentAbove_(54, [54, 40, 40, 10, -5]), 100);
  assert.equal(ctx.percentAbove_(-5, [54, 40, 40, 10, -5]), 0);
  assert.equal(ctx.percentAbove_(40, [54, 40, 40, 10, -5]), 50); // คนอื่น 4 คน: ต่ำกว่า 2
  assert.equal(ctx.percentAbove_(5, [5]), null);
  const h = plain(ctx.buildHistogram_([-5, 0, 9, 10, 54, 54], 10));
  assert.equal(h.bins[0].from, -10);
  assert.equal(h.bins[h.bins.length - 1].to, 59);
  assert.equal(h.bins.reduce((a, b) => a + b.count, 0), 6);
  assert.equal(ctx.binIndexFor_(h, 54), h.bins.length - 1);
  assert.equal(ctx.binIndexFor_(h, 10), 2);
});

test('PBKDF2 ที่เขียนเอง ตรงกับ crypto.pbkdf2Sync ของ Node (1000 รอบ)', () => {
  const { ctx } = createEnv();
  const mine = ctx.pbkdf2Hex_('รหัสผ่าน-ทดสอบ 123', 'saltABC|pepper', 1000);
  const ref = crypto.pbkdf2Sync(Buffer.from('รหัสผ่าน-ทดสอบ 123'), Buffer.from('saltABC|pepper'), 1000, 32, 'sha256').toString('hex');
  assert.equal(mine, ref);
});

/* ---------- ตัวอ่านชีต ---------- */

test('parseSummary_: อ่านนักศึกษา ข้ามแถวสถิติ และไม่อ่านคอลัมน์บันทึกภายใน', () => {
  const { ctx } = createEnv();
  const r = plain(ctx.parseSummary_(F.summaryTab()));
  assert.equal(r.students.length, 6);
  assert.deepEqual(r.max, { mcq: 40, w: [20, 20, 20], total: 100, written: 60 });
  const s1 = r.students[0];
  assert.equal(s1.idKey, '6999999900011');
  assert.equal(s1.pdfName, S[0].pdf);
  assert.equal(s1.totals.official, F.derive(S[0]).official);
  assert.ok(!JSON.stringify(r).includes('บันทึกลับ'), 'บันทึกภายในต้องไม่หลุดเข้าโครงสร้างข้อมูล');
});

test('parseSummary_: หัวตารางหาย -> ข้อผิดพลาดบอกชื่อคอลัมน์ที่ขาด', () => {
  const { ctx } = createEnv();
  const bad = F.summaryTab().map((row) => row.map((c) => (c === 'อัตนัยข้อ 2 (20)' ? 'x' : c)));
  assert.throws(() => ctx.parseSummary_(bad), /อัตนัยข้อ 2/);
  assert.throws(() => ctx.parseSummary_([['a', 'b']]), /รหัสนักศึกษา/);
});

test('parseMcq_: เฉลยและคำตอบรายข้อ', () => {
  const { ctx } = createEnv();
  const m = plain(ctx.parseMcq_(F.mcqTab()));
  assert.equal(m.items.length, 15);
  assert.equal(m.key[1], 'ค');
  assert.equal(m.key[15], 'ก');
  assert.deepEqual(m.rows[6].answers.slice(0, 4), ['ค', 'ข', 'ค', null]); // นักศึกษาลำดับ 6: 3 ข้อแรกถูก ที่เหลือว่าง
  assert.equal(m.rows[6].answers[10], null);
});

test('parseMcq_: เฉลยที่ไม่ตรงคอลัมน์ ใช้การไล่ตัวเลือกตามลำดับ', () => {
  const { ctx } = createEnv();
  const tab = F.mcqTab();
  tab[3] = ['เฉลย', 'เฉลยที่ใช้ตรวจ', '', ...F.KEY.slice(0, 15)]; // เลื่อนไปหนึ่งคอลัมน์
  const m = plain(ctx.parseMcq_(tab));
  assert.equal(m.key[1], 'ค');
  assert.equal(m.key[15], 'ก');
});

test('parseWritten_: โครงสร้างหัวข้อและคะแนนเต็ม', () => {
  const { ctx } = createEnv();
  const w = plain(ctx.parseWritten_(F.writtenTab()));
  assert.equal(w.questions.length, 3);
  assert.deepEqual(w.questions.map((q) => q.max), [20, 20, 20]);
  assert.deepEqual(w.questions[0].items.map((i) => i.max), [4, 3, 4, 3, 3, 3]);
  assert.equal(w.questions[1].items.length, 4);
  assert.equal(w.questions[1].items[2].label, 'Cy และ Mc');
  assert.equal(w.rows[1].q[1].total, 20);
});

test('parseFeedback_: ตัดบันทึกภายใน/ข้อความถึงผู้สอน/อ้างอิงเพื่อนคนอื่น', () => {
  const { ctx } = createEnv();
  const fb = plain(ctx.parseFeedback_(F.feedbackTab()));
  assert.deepEqual(fb[1].map((x) => x.scope), ['อัตนัย 1']);
  assert.deepEqual(fb[2].map((x) => x.scope), ['ปรนัยข้อ 5']);
  assert.deepEqual(fb[4].map((x) => x.scope), ['อัตนัย 3']);
  const all = JSON.stringify(fb);
  ['บันทึกภายใน', 'ผู้สอน', 'ลำดับที่'].forEach((w) => assert.ok(!all.includes(w), w));
});

/* ---------- Dashboard ---------- */

function dashboardFor(env, i, settingsPatch = {}) {
  const settings = Object.assign(plain(env.ctx.getSettings_()), settingsPatch);
  const D = env.ctx.loadClassData_(settings, true);
  return plain(env.ctx.buildDashboard_(D, env.ctx.normalizeId_(idOf(i)), settings));
}

test('buildDashboard_: คะแนน อันดับ (รวมเสมอกัน) สถิติห้อง', () => {
  const env = createReadyEnv(F);
  const totals = S.map((s) => F.derive(s).official);
  const d0 = dashboardFor(env, 0);
  assert.equal(d0.total.score, totals[0]);
  assert.equal(d0.total.rank, 1);
  assert.equal(d0.total.of, 6);
  assert.equal(d0.total.best, Math.max(...totals));
  assert.equal(d0.total.low, Math.min(...totals));
  const mean = totals.reduce((a, b) => a + b, 0) / totals.length;
  assert.equal(d0.total.mean, Math.round(mean * 100) / 100);
  assert.equal(d0.total.percentAbove, 100);

  // นักศึกษาลำดับ 3 กับ 5 คะแนนปรนัย/อัตนัยทำให้คะแนนรวมใกล้กัน — ตรวจว่าอันดับตรงกับการเรียงจริง
  const sorted = [...totals].sort((a, b) => b - a);
  S.forEach((_, i) => {
    const d = dashboardFor(env, i);
    assert.equal(d.total.rank, sorted.indexOf(totals[i]) + 1, 'rank ของลำดับ ' + (i + 1));
    assert.equal(d.total.ties, totals.filter((t, k) => k !== i && t === totals[i]).length);
  });
});

test('buildDashboard_: ปรนัยรายข้อ ถูก/ผิด/ว่าง และ % ที่ตอบถูกทั้งห้อง', () => {
  const env = createReadyEnv(F);
  const d = dashboardFor(env, 2); // ลำดับ 3: ccccccccccc ww c -
  assert.equal(d.mcq.items.length, 15);
  assert.equal(d.mcq.items[0].result, 'correct');
  assert.equal(d.mcq.items[0].points, 3);
  assert.equal(d.mcq.items[11].result, 'wrong');
  assert.equal(d.mcq.items[11].points, -2);
  assert.equal(d.mcq.items[14].result, 'blank');
  assert.equal(d.mcq.items[14].points, -1);
  assert.equal(d.mcq.items[14].answer, null);
  const counts = d.mcq.items.reduce((a, i) => { a[i.result]++; return a; }, { correct: 0, wrong: 0, blank: 0 });
  assert.equal(counts.correct, d.mcq.correct);
  assert.equal(counts.wrong, d.mcq.wrong);
  assert.equal(counts.blank, d.mcq.blank);
  // ข้อ 1: ทุกคนตอบถูกหมด (ทุก spec ขึ้นต้น c)
  assert.equal(d.mcq.items[0].classCorrectPct, 100);
});

test('buildDashboard_: อัตนัยรายหัวข้อ เทียบค่าเฉลี่ยห้อง', () => {
  const env = createReadyEnv(F);
  const d = dashboardFor(env, 1);
  assert.equal(d.writtenDetail.length, 3);
  assert.equal(d.writtenDetail[1].items.length, 4);
  assert.equal(d.writtenDetail[1].score, 12);
  const avgQ2 = S.map((s) => s.w[1].reduce((a, b) => a + b, 0)).reduce((a, b) => a + b, 0) / 6;
  assert.equal(d.writtenDetail[1].classMean, Math.round(avgQ2 * 100) / 100);
  assert.equal(d.written.max, 60);
});

test('buildDashboard_: total_mode เปลี่ยนคะแนนและอันดับ', () => {
  const env = createReadyEnv(F);
  const idx = 3; // ลำดับ 4: ปรนัยติดลบ
  const off = dashboardFor(env, idx);
  const fl = dashboardFor(env, idx, { total_mode: 'mcq_floor0' });
  assert.ok(off.total.score < fl.total.score);
  assert.equal(fl.total.score, F.derive(S[idx]).floor0);
  assert.equal(fl.components[0].score, 0);
  assert.match(fl.total.note, /ต่ำสุดเป็น 0/);
});

test('buildDashboard_: กระดานอันดับไม่มีชื่อ/รหัสของเพื่อนคนอื่น', () => {
  const env = createReadyEnv(F);
  const d = dashboardFor(env, 0);
  assert.equal(d.leaderboard.length, 6);
  assert.equal(d.leaderboard.filter((r) => r.you).length, 1);
  const json = JSON.stringify(d);
  for (let i = 1; i < S.length; i++) {
    assert.ok(!json.includes(S[i].name), 'ชื่อเพื่อนหลุด: ' + S[i].name);
    assert.ok(!json.includes(S[i].id), 'รหัสเพื่อนหลุด: ' + S[i].id);
  }
  assert.ok(!json.includes('บันทึกลับ'));
});

test('buildDashboard_: show_leaderboard/show_feedback/show_pdf', () => {
  const env = createReadyEnv(F);
  const off = dashboardFor(env, 1, { show_leaderboard: false, show_feedback: false, show_pdf: false });
  assert.equal(off.leaderboard, null);
  assert.equal(off.distribution, null);
  assert.equal(off.feedback, null);
  assert.equal(off.hasPdf, false);
  const on = dashboardFor(env, 1, { show_feedback: true });
  assert.deepEqual(on.feedback.map((f) => f.scope), ['ปรนัยข้อ 5']); // ความเห็นถึงผู้สอนถูกตัดออก
  assert.equal(on.hasPdf, true);
});

/* ---------- จับคู่ PDF ---------- */

test('resolvePdfId_: ตามชื่อไฟล์ในชีต, สำรองด้วยลำดับ+ชื่อ, ทนการ escape/Unicode', () => {
  const { ctx } = createEnv();
  const map = {};
  const put = (n, id) => { map[ctx.normalizeFileName_(n)] = id; };
  put('ตรวจแล้ว_01_นายทดสอบ หนึ่ง.pdf', 'A');
  put('ตรวจแล้ว_02_นางสาวทดสอบ  สอง.pdf', 'B');
  const stu = (o) => Object.assign({ seq: 1, name: 'นายทดสอบ หนึ่ง', pdfName: '' }, o);
  assert.equal(ctx.resolvePdfId_(stu({ pdfName: 'ตรวจแล้ว\\_01\\_นายทดสอบ หนึ่ง.pdf' }), map), 'A');
  assert.equal(ctx.resolvePdfId_(stu({ pdfName: '' }), map), 'A');
  assert.equal(ctx.resolvePdfId_(stu({ seq: 2, name: 'นางสาวทดสอบ สอง', pdfName: 'ผิดชื่อ.pdf' }), map), 'B');
  assert.equal(ctx.resolvePdfId_(stu({ seq: 3, name: 'ไม่มี', pdfName: '' }), map), null);
});

/* ---------- ลงทะเบียน / เข้าสู่ระบบ / API ---------- */

test('ลงทะเบียน: สำเร็จด้วยรหัส+ชื่อ แล้วเข้าสู่ระบบได้ และรหัสผ่านไม่ถูกเก็บเป็นข้อความ', () => {
  const env = createReadyEnv(F);
  const { ctx } = env;
  const r = plain(ctx.api_register({ studentId: idOf(0).replace(/-/g, ' '), name: 'ทดสอบ หนึ่ง', password: PW }));
  assert.equal(r.ok, true, r.error);
  assert.equal(r.token.length, 64);

  const users = env.db.getSheetByName('Users');
  assert.equal(users.rows.length, 2);
  const stored = JSON.stringify(users.rows[1]);
  assert.ok(!stored.includes(PW));
  assert.equal(users.rows[1][3].length, 64); // hex ของ SHA-256 32 ไบต์

  const again = plain(ctx.api_register({ studentId: idOf(0), name: nameOf(0), password: PW }));
  assert.equal(again.ok, false);
  assert.match(again.error, /ลงทะเบียนแล้ว/);

  const login = plain(ctx.api_login({ studentId: idOf(0), password: PW }));
  assert.equal(login.ok, true);
  assert.notEqual(login.token, r.token);
});

test('ลงทะเบียน: ปฏิเสธรหัสที่ไม่มีในรายชื่อ ชื่อไม่ตรง และรหัสผ่านอ่อน', () => {
  const env = createReadyEnv(F);
  const { ctx } = env;
  assert.match(plain(ctx.api_register({ studentId: '69-111111-9999-9', name: 'x', password: PW })).error, /ไม่พบรหัสนักศึกษา/);
  assert.match(plain(ctx.api_register({ studentId: idOf(1), name: 'คนอื่น นามสกุลอื่น', password: PW })).error, /ชื่อ-สกุลไม่ตรง/);
  assert.match(plain(ctx.api_register({ studentId: idOf(1), name: nameOf(1), password: 'short1' })).error, /อย่างน้อย/);
  assert.equal(env.db.getSheetByName('Users').rows.length, 1); // ยังไม่มีผู้ใช้
});

test('เข้าสู่ระบบ: ผิดซ้ำ -> ล็อกชั่วคราว แม้ใส่รหัสถูกก็เข้าไม่ได้ระหว่างล็อก', () => {
  const env = createReadyEnv(F);
  const { ctx } = env;
  assert.equal(plain(ctx.api_register({ studentId: idOf(0), name: nameOf(0), password: PW })).ok, true);
  for (let i = 0; i < 4; i++) {
    assert.match(plain(ctx.api_login({ studentId: idOf(0), password: 'wrong-pass1' })).error, /ไม่ถูกต้อง/);
  }
  const fifth = plain(ctx.api_login({ studentId: idOf(0), password: 'wrong-pass1' }));
  assert.equal(fifth.ok, false);
  const locked = plain(ctx.api_login({ studentId: idOf(0), password: PW }));
  assert.equal(locked.ok, false);
  assert.match(locked.error, /ล็อก/);
});

test('เข้าสู่ระบบ: ข้อความผิดพลาดเหมือนกันทั้งกรณีไม่มีผู้ใช้และรหัสผิด (ไม่เปิดเผยว่ามีบัญชีหรือไม่)', () => {
  const env = createReadyEnv(F);
  const { ctx } = env;
  ctx.api_register({ studentId: idOf(0), name: nameOf(0), password: PW });
  const a = plain(ctx.api_login({ studentId: idOf(0), password: 'bad-pass-1' })).error;
  const b = plain(ctx.api_login({ studentId: idOf(3), password: 'bad-pass-1' })).error;
  assert.equal(a, b);
});

test('จำกัดจำนวนครั้งลงทะเบียนต่อรหัสนักศึกษา', () => {
  const env = createReadyEnv(F);
  const { ctx } = env;
  let last;
  for (let i = 0; i < 12; i++) last = plain(ctx.api_register({ studentId: idOf(2), name: 'ผิด ชื่อ', password: PW }));
  assert.match(last.error, /หลายครั้งเกินไป/);
});

test('api_dashboard: ต้องมีเซสชัน; ปิดประกาศ -> ไม่ส่งคะแนน; เปิด -> ส่งเฉพาะของตัวเอง', () => {
  const env = createReadyEnv(F, { published: false });
  const { ctx } = env;
  assert.equal(plain(ctx.api_dashboard('x'.repeat(64))).expired, true);
  assert.equal(plain(ctx.api_dashboard(undefined)).ok, false);

  const reg = plain(ctx.api_register({ studentId: idOf(1), name: nameOf(1), password: PW }));
  const locked = plain(ctx.api_dashboard(reg.token));
  assert.equal(locked.ok, true);
  assert.equal(locked.published, false);
  assert.equal(locked.data, undefined);
  assert.ok(!JSON.stringify(locked).includes('score'));

  env.setting('published', true);
  const open = plain(ctx.api_dashboard(reg.token));
  assert.equal(open.published, true);
  assert.equal(open.data.student.id, idOf(1));
  assert.equal(open.data.total.score, F.derive(S[1]).official);
  assert.equal(open.course.title, '020325201 ADV.STRUCTURAL');
});

test('api_logout ยกเลิกเซสชัน', () => {
  const env = createReadyEnv(F);
  const { ctx } = env;
  const reg = plain(ctx.api_register({ studentId: idOf(0), name: nameOf(0), password: PW }));
  assert.equal(plain(ctx.api_dashboard(reg.token)).ok, true);
  ctx.api_logout(reg.token);
  assert.equal(plain(ctx.api_dashboard(reg.token)).expired, true);
});

test('api_pdf: ส่งไฟล์ของนักศึกษาที่ล็อกอินเท่านั้น และไม่รับรหัสไฟล์จากหน้าเว็บ', () => {
  const env = createReadyEnv(F);
  const { ctx } = env;
  const r0 = plain(ctx.api_register({ studentId: idOf(0), name: nameOf(0), password: PW }));
  const r1 = plain(ctx.api_register({ studentId: idOf(1), name: nameOf(1), password: PW }));
  const p0 = plain(ctx.api_pdf(r0.token));
  const p1 = plain(ctx.api_pdf(r1.token));
  assert.equal(p0.ok, true);
  assert.equal(Buffer.from(p0.base64, 'base64').toString(), '%PDF-1.4 fake 1');
  assert.equal(Buffer.from(p1.base64, 'base64').toString(), '%PDF-1.4 fake 2');
  assert.equal(p0.name, S[0].pdf);
  assert.equal(plain(ctx.api_pdf('0'.repeat(64))).expired, true);
  // ไม่มีพารามิเตอร์รับ fileId — ส่งเพิ่มมาก็ถูกเพิกเฉย
  assert.equal(Buffer.from(plain(ctx.api_pdf(r0.token, 'F2')).base64, 'base64').toString(), '%PDF-1.4 fake 1');
});

test('api_pdf: ปิดประกาศหรือปิด show_pdf -> ไม่ส่งไฟล์; ไฟล์หาย -> ข้อความชัดเจน', () => {
  const env = createReadyEnv(F, { pdf: false });
  const { ctx } = env;
  const r = plain(ctx.api_register({ studentId: idOf(0), name: nameOf(0), password: PW }));
  env.state.drive.folders.FOLDER1 = [];
  assert.match(plain(ctx.api_pdf(r.token)).error, /ยังไม่พบไฟล์ PDF/);
  env.setting('show_pdf', false);
  assert.match(plain(ctx.api_pdf(r.token)).error, /ยังไม่เปิด/);
  env.setting('show_pdf', true);
  env.setting('published', false);
  assert.match(plain(ctx.api_pdf(r.token)).error, /ยังไม่เปิด/);
});

test('ข้อผิดพลาดภายในไม่รั่วรายละเอียดไปหน้าเว็บ', () => {
  const env = createReadyEnv(F);
  env.setting('scores_spreadsheet_id', 'NOT_EXIST');
  const r = plain(env.ctx.api_register({ studentId: idOf(0), name: nameOf(0), password: PW }));
  assert.equal(r.ok, false);
  assert.match(r.error, /ระบบขัดข้อง/);
  assert.ok(!r.error.includes('NOT_EXIST'));
});

/* ---------- โหมดรหัสยืนยัน + แอดมิน ---------- */

test('โหมด code: ต้องมีรหัสยืนยันที่ถูกต้อง ใช้ได้ครั้งเดียว', () => {
  const env = createReadyEnv(F);
  const { ctx } = env;
  ctx.adminGenerateCodes();
  const codes = env.db.getSheetByName('Codes');
  assert.equal(codes.rows.length, 7);
  assert.match(codes.rows[1][2], /^[A-Z2-9]{4}-[A-Z2-9]{4}$/);
  env.setting('register_verify', 'code');

  const bad = plain(ctx.api_register({ studentId: idOf(0), code: 'AAAA-AAAA', password: PW }));
  assert.match(bad.error, /รหัสยืนยันไม่ถูกต้อง/);
  const code = codes.rows[1][2];
  const ok = plain(ctx.api_register({ studentId: idOf(0), code: code.toLowerCase().replace('-', ' '), password: PW }));
  assert.equal(ok.ok, true, ok.error);
  assert.ok(codes.rows[1][4], 'ต้องบันทึกเวลาที่ใช้รหัส');

  ctx.resetPasswordFor_(ctx.normalizeId_(idOf(0)));
  assert.equal(codes.rows[1][4], '', 'รีเซ็ตแล้วรหัสยืนยันใช้ได้อีกครั้ง');
});

test('adminGenerateCodes ไม่ทับรหัสเดิม', () => {
  const env = createReadyEnv(F);
  env.ctx.adminGenerateCodes();
  const before = JSON.stringify(env.db.getSheetByName('Codes').rows);
  env.ctx.adminGenerateCodes();
  assert.equal(JSON.stringify(env.db.getSheetByName('Codes').rows), before);
});

test('สิทธิ์แอดมิน: ผู้เข้าชมเว็บ (ActiveUser ≠ EffectiveUser) เรียกฟังก์ชันผู้ดูแลไม่ได้', () => {
  const env = createReadyEnv(F);
  env.asVisitor();
  for (const fn of ['adminSetup', 'adminCheckData', 'adminPublishOn', 'adminPublishOff', 'adminGenerateCodes', 'adminResetPassword', 'adminClearCache']) {
    assert.throws(() => env.ctx[fn](), /ผู้ดูแลระบบ/, fn);
  }
  env.state.session.active = 'someone-else@example.com';
  assert.throws(() => env.ctx.adminPublishOn(), /ผู้ดูแลระบบ/);
  env.asOwner();
  env.ctx.adminPublishOn();
  assert.equal(plain(env.ctx.getSettings_()).published, true);
});

test('รีเซ็ตรหัสผ่านเพิกถอนเซสชันเดิมและให้ลงทะเบียนใหม่ได้', () => {
  const env = createReadyEnv(F);
  const { ctx } = env;
  const r = plain(ctx.api_register({ studentId: idOf(0), name: nameOf(0), password: PW }));
  assert.equal(plain(ctx.api_dashboard(r.token)).ok, true);
  assert.equal(ctx.resetPasswordFor_(ctx.normalizeId_(idOf(0))), true);
  assert.equal(ctx.resetPasswordFor_(ctx.normalizeId_(idOf(0))), false);
  return new Promise((resolve) => setTimeout(resolve, 5)).then(() => {
    assert.equal(plain(ctx.api_dashboard(r.token)).expired, true);
    assert.equal(plain(ctx.api_login({ studentId: idOf(0), password: PW })).ok, false);
    assert.equal(plain(ctx.api_register({ studentId: idOf(0), name: nameOf(0), password: 'NewPassw0rd' })).ok, true);
  });
});

test('adminSetup: สร้างแท็บ ตั้งค่าเริ่มต้นปลอดภัย (ปิดประกาศ/ปิดความเห็น) และไม่ทับค่าที่ผู้สอนแก้', () => {
  const env = createEnv();
  env.ctx.adminSetup();
  const names = env.db.getSheets().map((s) => s.getName());
  ['Settings', 'Users', 'Codes', 'Audit'].forEach((n) => assert.ok(names.includes(n), n));
  const st = plain(env.ctx.getSettings_());
  assert.equal(st.published, false);
  assert.equal(st.show_feedback, false);
  assert.equal(st.register_verify, 'name');
  assert.equal(st.pdf_folder_id, '', 'ไม่ฝัง ID โฟลเดอร์จริงเป็นค่าตั้งต้น');
  const pepper = env.state.props.PEPPER;
  assert.equal(pepper.length, 64);
  env.setting('course_title', 'ชื่อที่ผู้สอนแก้');
  env.ctx.adminSetup();
  assert.equal(env.state.props.PEPPER, pepper, 'pepper ต้องไม่เปลี่ยน ไม่งั้นรหัสผ่านเดิมใช้ไม่ได้');
  assert.equal(plain(env.ctx.getSettings_()).course_title, 'ชื่อที่ผู้สอนแก้');
});

test('buildCheckReport_: รายงานความสอดคล้องและแจ้งสิ่งที่ผิดปกติ', () => {
  const env = createReadyEnv(F);
  let lines = plain(env.ctx.buildCheckReport_(plain(env.ctx.getSettings_())));
  const text = () => lines.join('\n');
  assert.match(text(), /นักศึกษาในชีตคะแนน: 6 คน/);
  assert.match(text(), /ปรนัยรายข้อสอดคล้อง/);
  assert.match(text(), /อัตนัยรายหัวข้อสอดคล้อง/);
  assert.match(text(), /จับคู่ PDF ได้ครบ/);

  // ทำให้ผิดปกติ: แก้คำตอบปรนัย, ลบ PDF หนึ่งไฟล์
  const mcq = env.state.spreadsheets.SCORES1.getSheetByName('ปรนัยรายข้อ');
  mcq.rows[4][2] = mcq.rows[4][2] === 'ก' ? 'ข' : 'ก';
  env.state.drive.folders.FOLDER1 = env.state.drive.folders.FOLDER1.filter((id) => id !== 'F3');
  env.ctx.clearAllCaches_();
  lines = plain(env.ctx.buildCheckReport_(plain(env.ctx.getSettings_())));
  assert.match(text(), /ปรนัยรายข้อไม่ตรงกับแท็บสรุป: 69-999999-0001-1/);
  assert.match(text(), /ไม่พบ PDF ของ: 69-999999-0003-7/);
});

test('แท็บคะแนนที่ไม่ใช่แท็บหลักหาย -> ข้ามส่วนนั้นและแจ้งเตือน ไม่ล่มทั้งระบบ', () => {
  const env = createReadyEnv(F);
  env.state.spreadsheets.SCORES1.sheets = env.state.spreadsheets.SCORES1.sheets.filter((s) => s.name === 'สรุปคะแนน');
  env.ctx.clearAllCaches_();
  const settings = plain(env.ctx.getSettings_());
  const D = plain(env.ctx.readClassData_(settings));
  assert.equal(D.students.length, 6);
  assert.equal(D.mcq, null);
  assert.ok(D.warnings.some((w) => w.includes('ปรนัยรายข้อ')));
  const d = plain(env.ctx.buildDashboard_(D, env.ctx.normalizeId_(idOf(0)), settings));
  assert.equal(d.mcq, null);
  assert.equal(d.writtenDetail, null);
  assert.ok(d.total.score != null);
});

test('doGet ฝังข้อมูลเริ่มต้นเป็น JSON ปลอดภัยใน <script>', () => {
  const env = createReadyEnv(F);
  env.setting('notice', '</script><script>alert(1)</script>');
  const out = env.ctx.jsonForScript_({ notice: '</script><b>&' });
  assert.ok(!out.includes('<'));
  assert.ok(!out.includes('>'));
  assert.deepEqual(JSON.parse(out), { notice: '</script><b>&' });
});
