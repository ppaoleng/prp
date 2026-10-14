'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const F = require('./fixtures');
const { createReadyEnv } = require('./harness');

const plain = (x) => JSON.parse(JSON.stringify(x));
const S = F.STUDENTS;
const ADMIN_PW = '1111'; // รหัสที่ผู้ใช้ขอ (ตั้งผ่านเมนู ไม่ฝังในโค้ด)

function adminEnv(opts) {
  const env = createReadyEnv(F, opts);
  env.state.promptText = ADMIN_PW;
  // เมนู "ตั้งรหัสผ่านผู้ดูแล" — จำลอง prompt ที่ผู้ใช้พิมพ์ 1111
  env.ctx.adminSetPassword();
  env.key = env.state.props.ADMIN_KEY;
  env.login = (pw = ADMIN_PW, key = env.key) => plain(env.ctx.api_adminLogin(key, pw));
  return env;
}

test('ตั้งค่าเริ่มต้นสร้างคีย์ลับ 128 บิต และรหัสผ่านผู้ดูแลไม่ถูกเก็บเป็นข้อความ', () => {
  const env = adminEnv();
  assert.match(env.key, /^[0-9a-f]{32}$/);
  const dump = JSON.stringify(env.state.props);
  assert.ok(!dump.includes(ADMIN_PW + '"'), 'ต้องไม่เก็บรหัสผ่านผู้ดูแลเป็นข้อความ');
  assert.equal(env.state.props.ADMIN_HASH.length, 64);
  assert.ok(!JSON.stringify(env.db.getSheets().map((s) => s.rows)).includes(env.key), 'คีย์ลับต้องไม่อยู่ในชีต');
  assert.ok(env.state.uiLog.some((m) => m.includes('?admin=' + env.key)), 'เมนูต้องแสดงลิงก์ผู้ดูแล');
  assert.ok(env.state.uiLog.some((m) => m.includes('สั้น/เดาง่าย')), 'ต้องเตือนเมื่อรหัสสั้น');
});

test('ตั้งรหัสผ่านผู้ดูแลสั้นกว่า 4 ตัวไม่ได้', () => {
  const env = adminEnv();
  assert.match(env.ctx.setAdminPassword_('123'), /อย่างน้อย 4/);
  assert.equal(env.ctx.setAdminPassword_('1111'), '');
});

test('doGet: คีย์ถูกจึงได้หน้าผู้ดูแล, คีย์ผิด/ไม่มี ได้หน้านักศึกษาปกติ ไม่มีคำใบ้', () => {
  const env = adminEnv();
  const boot = (e) => JSON.parse(env.ctx.doGet(e).boot);
  assert.equal(boot({ parameter: { admin: env.key } }).admin, true);
  assert.equal(boot({ parameter: { admin: env.key } }).adminKey, env.key);
  for (const e of [undefined, {}, { parameter: {} }, { parameter: { admin: 'x'.repeat(32) } }, { parameter: { admin: '' } }, { parameter: { admin: env.key.slice(0, 31) } }]) {
    const b = boot(e);
    assert.equal(b.admin, undefined);
    assert.equal(b.adminKey, undefined);
  }
});

test('api_adminLogin: ต้องมีคีย์ถูก + รหัสผ่านถูก; ผิดอย่างใดอย่างหนึ่งไม่ได้โทเคน', () => {
  const env = adminEnv();
  assert.equal(env.login('1111', 'wrongkey').ok, false);
  assert.equal(env.login('1111', null).ok, false);
  assert.equal(plain(env.ctx.api_adminLogin(undefined, '1111')).ok, false, 'ไม่ส่งคีย์เลยต้องเข้าไม่ได้');
  assert.equal(plain(env.ctx.api_adminLogin()).ok, false);
  assert.equal(plain(env.ctx.api_adminLogin({ toString: () => env.key }, '1111')).ok, false, 'คีย์ต้องเป็นสตริงจริง ไม่รับ object');
  assert.equal(env.login('1111', '').ok, false);
  assert.equal(env.login('9999').ok, false);
  assert.equal(env.login('').ok, false);
  const ok = env.login('1111');
  assert.equal(ok.ok, true);
  assert.match(ok.token, /^[0-9a-f]{64}$/);
});

test('api_adminLogin: ไม่ได้ตั้งรหัสผ่านผู้ดูแล -> เข้าไม่ได้ (ไม่มีรหัสเริ่มต้น)', () => {
  const env = createReadyEnv(F); // ยังไม่ได้ตั้งรหัสผ่านผู้ดูแล
  const key = env.state.props.ADMIN_KEY;
  for (const pw of ['', '1111', 'admin', 'undefined', 'null']) {
    const r = plain(env.ctx.api_adminLogin(key, pw));
    assert.equal(r.ok, false);
    assert.match(r.error, /ยังไม่ได้ตั้งรหัสผ่านผู้ดูแล/);
  }
});

test('api_adminLogin: ผิด 5 ครั้งติด -> ล็อก แม้ใส่รหัสถูกก็เข้าไม่ได้', () => {
  const env = adminEnv();
  for (let i = 0; i < 5; i++) assert.equal(env.login('0000').ok, false);
  const locked = env.login('1111');
  assert.equal(locked.ok, false);
  assert.match(locked.error, /ล็อก/);
});

test('โทเคนนักศึกษากับโทเคนผู้ดูแลใช้แทนกันไม่ได้', () => {
  const env = adminEnv();
  const stu = plain(env.ctx.api_register({ studentId: S[0].id, name: S[0].name, password: 'Passw0rd!x' }));
  const adm = env.login('1111');
  for (const call of [
    () => env.ctx.api_adminOverview(stu.token),
    () => env.ctx.api_adminStudent(stu.token, S[1].id),
    () => env.ctx.api_adminPdf(stu.token, S[1].id),
    () => env.ctx.api_adminOverview(undefined),
    () => env.ctx.api_adminOverview('0'.repeat(64)),
    () => env.ctx.api_adminStudent(env.key, S[1].id)
  ]) {
    const r = plain(call());
    assert.equal(r.ok, false);
    assert.equal(r.expired, true);
  }
  assert.equal(plain(env.ctx.api_dashboard(adm.token)).expired, true, 'โทเคนผู้ดูแลต้องใช้เป็นเซสชันนักศึกษาไม่ได้');
  assert.equal(plain(env.ctx.api_pdf(adm.token)).expired, true);
});

test('api_adminOverview: ครบทุกคน คะแนน/อันดับตรงกับหน้าของนักศึกษา และไม่มีข้อมูลลับ', () => {
  const env = adminEnv({ published: false }); // ผู้ดูแลเห็นได้แม้ยังไม่เปิดประกาศผล
  const o = plain(env.ctx.api_adminOverview(env.login('1111').token));
  assert.equal(o.ok, true);
  assert.equal(o.published, false);
  assert.equal(o.rows.length, 6);
  assert.equal(o.registered, 0);
  const totals = S.map((s) => F.derive(s).official);
  o.rows.forEach((r, i) => {
    assert.equal(r.id, S[i].id);
    assert.equal(r.name, S[i].name);
    assert.equal(r.total, totals[i]);
    assert.equal(r.rank, totals.filter((t) => t > totals[i]).length + 1);
    assert.equal(r.pdf, true);
    assert.equal(r.registered, false);
  });
  assert.equal(o.stats.n, 6);
  assert.equal(o.distribution.you, -1);
  const json = JSON.stringify(o);
  for (const secret of ['บันทึกลับ', 'ผู้สอนโปรดพิจารณา', env.state.props.PEPPER, env.state.props.ADMIN_HASH, env.state.props.ADMIN_SALT]) {
    assert.ok(!json.includes(secret), 'หลุด: ' + secret);
  }
});

test('api_adminOverview: สถานะลงทะเบียนและ PDF ที่หาย', () => {
  const env = adminEnv();
  env.ctx.api_register({ studentId: S[1].id, name: S[1].name, password: 'Passw0rd!x' });
  env.state.drive.folders.FOLDER1 = env.state.drive.folders.FOLDER1.filter((id) => id !== 'F4');
  env.ctx.clearAllCaches_();
  const o = plain(env.ctx.api_adminOverview(env.login('1111').token));
  assert.equal(o.registered, 1);
  assert.deepEqual(o.rows.map((r) => r.registered), [false, true, false, false, false, false]);
  assert.equal(o.rows[1].lastLoginAt.length > 10, true);
  assert.equal(o.rows[3].pdf, false);
  assert.equal(o.rows[0].pdf, true);
});

test('api_adminStudent: ข้อมูลเต็มของคนที่เลือก แม้ยังไม่เปิดประกาศและปิด feedback/leaderboard', () => {
  const env = adminEnv({ published: false });
  env.setting('show_feedback', false);
  env.setting('show_leaderboard', false);
  const tok = env.login('1111').token;
  const r = plain(env.ctx.api_adminStudent(tok, S[1].id.replace(/-/g, ' ')));
  assert.equal(r.ok, true);
  assert.equal(r.published, false);
  assert.equal(r.registered, false);
  assert.equal(r.data.student.id, S[1].id);
  assert.equal(r.data.total.score, F.derive(S[1]).official);
  assert.ok(r.data.leaderboard.length === 6);
  assert.deepEqual(r.data.feedback.map((f) => f.scope), ['ปรนัยข้อ 5']);
  assert.ok(!JSON.stringify(r).includes('บันทึกลับ'));
  assert.equal(plain(env.ctx.api_adminStudent(tok, '69-000000-0000-0')).ok, false);
  assert.equal(plain(env.ctx.api_adminStudent(tok, '')).ok, false);
  // การตั้งค่าจริงต้องไม่ถูกแก้โดยการดูของผู้ดูแล
  assert.equal(plain(env.ctx.getSettings_()).show_feedback, false);
});

test('api_adminPdf: ส่งไฟล์ของนักศึกษาที่เลือก แม้ยังไม่เปิดประกาศ', () => {
  const env = adminEnv({ published: false });
  const tok = env.login('1111').token;
  const r = plain(env.ctx.api_adminPdf(tok, S[4].id));
  assert.equal(r.ok, true);
  assert.equal(Buffer.from(r.base64, 'base64').toString(), '%PDF-1.4 fake 5');
  assert.equal(plain(env.ctx.api_adminPdf(tok, 'nope')).ok, false);
});

test('เปลี่ยนรหัสผ่านผู้ดูแล / สร้างลิงก์ใหม่ เพิกถอนเซสชันเดิมทันที', () => {
  const env = adminEnv();
  let tok = env.login('1111').token;
  assert.equal(plain(env.ctx.api_adminOverview(tok)).ok, true);
  return new Promise((r) => setTimeout(r, 5)).then(() => {
    env.ctx.setAdminPassword_('NewAdminPw9');
    assert.equal(plain(env.ctx.api_adminOverview(tok)).expired, true);
    assert.equal(env.login('1111').ok, false);
    tok = env.login('NewAdminPw9').token;
    assert.equal(plain(env.ctx.api_adminOverview(tok)).ok, true);
    return new Promise((r) => setTimeout(r, 5));
  }).then(() => {
    const oldKey = env.key;
    env.ctx.adminRotateKey();
    assert.equal(plain(env.ctx.api_adminOverview(tok)).expired, true);
    assert.equal(env.login('NewAdminPw9', oldKey).ok, false, 'คีย์เดิมต้องใช้ไม่ได้');
    assert.equal(env.login('NewAdminPw9', env.state.props.ADMIN_KEY).ok, true);
  });
});

test('api_adminLogout ยกเลิกเซสชัน', () => {
  const env = adminEnv();
  const tok = env.login('1111').token;
  env.ctx.api_adminLogout(tok);
  assert.equal(plain(env.ctx.api_adminOverview(tok)).expired, true);
});

test('เมนูผู้ดูแลใหม่ต้องตรวจสิทธิ์ ผู้เข้าชมเว็บเรียกไม่ได้', () => {
  const env = adminEnv();
  env.asVisitor();
  for (const fn of ['adminSetPassword', 'adminShowLink', 'adminRotateKey', 'adminConfigure']) {
    assert.throws(() => env.ctx[fn](), /ผู้ดูแลระบบ/, fn);
  }
  assert.equal(env.state.props.ADMIN_KEY, env.key, 'คีย์ต้องไม่ถูกเปลี่ยนโดยผู้เข้าชม');
});

test('ผู้ดูแลเข้าได้โดยไม่กระทบการลงทะเบียน/ล็อกอินของนักศึกษา และรหัส 1111 ใช้เป็นรหัสนักศึกษาไม่ได้', () => {
  const env = adminEnv();
  // รหัสกลางห้ามทำงานบนหน้าล็อกอินของนักศึกษา แม้จะรู้รหัสนักศึกษา
  const r = plain(env.ctx.api_login({ studentId: S[0].id, password: '1111' }));
  assert.equal(r.ok, false);
  env.ctx.api_register({ studentId: S[0].id, name: S[0].name, password: 'Passw0rd!x' });
  assert.equal(plain(env.ctx.api_login({ studentId: S[0].id, password: '1111' })).ok, false);
  assert.equal(plain(env.ctx.api_login({ studentId: S[0].id, password: 'Passw0rd!x' })).ok, true);
  // และรหัสผ่านของนักศึกษาใช้เข้าหน้าผู้ดูแลไม่ได้
  assert.equal(env.login('Passw0rd!x').ok, false);
});

test('ทุกฟังก์ชันที่หน้าเว็บเรียกได้มีเท่าที่ตั้งใจ (ไม่มีฟังก์ชัน admin หลุดโดยไม่ตรวจสิทธิ์)', () => {
  const fs = require('node:fs'), path = require('node:path');
  const names = [];
  for (const f of fs.readdirSync(path.join(__dirname, '..')).filter((x) => x.endsWith('.gs'))) {
    for (const m of fs.readFileSync(path.join(__dirname, '..', f), 'utf8').matchAll(/^function +([A-Za-z0-9_]+)/gm)) {
      if (!m[1].endsWith('_')) names.push(m[1]);
    }
  }
  const allowed = new Set(['doGet', 'include', 'onOpen',
    'api_register', 'api_login', 'api_logout', 'api_dashboard', 'api_pdf',
    'api_adminLogin', 'api_adminLogout', 'api_adminOverview', 'api_adminStudent', 'api_adminPdf',
    'adminSetup', 'adminCheckData', 'adminPublishOn', 'adminPublishOff', 'adminClearCache',
    'adminSetPassword', 'adminShowLink', 'adminRotateKey', 'adminGenerateCodes', 'adminResetPassword', 'adminConfigure']);
  for (const n of names) assert.ok(allowed.has(n), 'ฟังก์ชันสาธารณะที่ไม่ได้อนุญาต: ' + n);
  // ทุก admin* (เมนู) ต้องเรียก assertAdmin_ ก่อน
  for (const f of fs.readdirSync(path.join(__dirname, '..')).filter((x) => x.endsWith('.gs'))) {
    const src = fs.readFileSync(path.join(__dirname, '..', f), 'utf8');
    for (const m of src.matchAll(/^function (admin[A-Z][A-Za-z]*)\(\) \{\n  (\w+)/gm)) {
      assert.equal(m[2], 'assertAdmin_', m[1] + ' ต้องตรวจสิทธิ์เป็นบรรทัดแรก');
    }
  }
});

test('extractDriveId_: รับลิงก์ Sheets/โฟลเดอร์/ID ล้วน และปฏิเสธข้อความอื่น', () => {
  const { ctx } = createReadyEnv(F);
  const id = '1udBVVdhtxV0v-kOgW0l9fMa4QupPqQt1';
  const x = (t) => ctx.extractDriveId_(t);
  assert.equal(x('https://docs.google.com/spreadsheets/d/' + id + '/edit?usp=sharing'), id);
  assert.equal(x('https://docs.google.com/spreadsheets/d/' + id + '/edit#gid=0'), id);
  assert.equal(x('https://drive.google.com/drive/folders/' + id + '?usp=sharing'), id);
  assert.equal(x('https://drive.google.com/drive/u/0/folders/' + id), id);
  assert.equal(x('https://drive.google.com/open?id=' + id), id);
  assert.equal(x('  ' + id + '  '), id);
  assert.equal(x(''), '');
  assert.equal(x('สวัสดี'), '');
  assert.equal(x('abc'), '');
  assert.equal(x(null), '');
});

test('adminConfigure: วางลิงก์ -> ตั้งค่า -> ตรวจข้อมูลทันที; เว้นว่าง/ยกเลิกไม่เปลี่ยนค่า', () => {
  const env = createReadyEnv(F);
  env.setting('scores_spreadsheet_id', '');
  env.setting('pdf_folder_id', '');
  // ยกเลิกระหว่างทาง = ไม่เปลี่ยนอะไร
  env.state.promptQueue = ['CANCEL'];
  env.ctx.adminConfigure();
  assert.equal(plain(env.ctx.getSettings_()).scores_spreadsheet_id, '');
  // วางลิงก์จริง
  env.state.uiLog.length = 0;
  env.state.promptQueue = ['https://docs.google.com/spreadsheets/d/SCORES1/edit?usp=sharing', 'https://drive.google.com/drive/folders/FOLDER1?usp=sharing'];
  env.ctx.adminConfigure();
  const st = plain(env.ctx.getSettings_());
  assert.equal(st.scores_spreadsheet_id, 'SCORES1');
  assert.equal(st.pdf_folder_id, 'FOLDER1');
  const report = env.state.uiLog.join('\n');
  assert.match(report, /ตั้งไฟล์คะแนนแล้ว/);
  assert.match(report, /นักศึกษาในชีตคะแนน: 6 คน/);
  assert.match(report, /จับคู่ PDF ได้ครบ/);
  // เว้นว่างทั้งสองช่อง = คงค่าเดิม
  env.state.promptQueue = ['', ''];
  env.ctx.adminConfigure();
  assert.equal(plain(env.ctx.getSettings_()).scores_spreadsheet_id, 'SCORES1');
  // ลิงก์ที่อ่านไม่ออก -> แจ้งและไม่เปลี่ยน
  env.state.uiLog.length = 0;
  env.state.promptQueue = ['ไม่ใช่ลิงก์', ''];
  env.ctx.adminConfigure();
  assert.match(env.state.uiLog.join('\n'), /อ่านลิงก์ไฟล์คะแนนไม่ออก/);
  assert.equal(plain(env.ctx.getSettings_()).scores_spreadsheet_id, 'SCORES1');
});

test('adminConfigure: ไฟล์เปิดไม่ได้ -> รายงานข้อผิดพลาดที่อ่านเข้าใจ ไม่ล่ม', () => {
  const env = createReadyEnv(F);
  env.state.promptQueue = ['https://docs.google.com/spreadsheets/d/NOPE/edit', ''];
  env.ctx.adminConfigure();
  assert.match(env.state.uiLog.join('\n'), /อ่านข้อมูลไม่สำเร็จ/);
});
