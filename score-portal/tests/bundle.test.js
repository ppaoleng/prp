'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const F = require('./fixtures');
const { createReadyEnv } = require('./harness');
const { build } = require('../dev/bundle');

const ROOT = path.join(__dirname, '..');
const plain = (x) => JSON.parse(JSON.stringify(x));

test('dist ตรงกับไฟล์ต้นทางเสมอ (ถ้าไม่ตรงให้รัน npm run bundle แล้ว commit)', () => {
  const b = build();
  assert.equal(fs.readFileSync(path.join(ROOT, 'dist/Code.gs'), 'utf8'), b.code, 'dist/Code.gs ล้าสมัย');
  assert.equal(fs.readFileSync(path.join(ROOT, 'dist/Index.html'), 'utf8'), b.html, 'dist/Index.html ล้าสมัย');
  assert.equal(fs.readFileSync(path.join(ROOT, 'dist/appsscript.json'), 'utf8'), b.manifest, 'dist/appsscript.json ล้าสมัย');
});

test('Index.html รวมแล้วไม่เหลือ include และมี scriptlet เดียวคือ boot', () => {
  const { html } = build();
  assert.ok(!html.includes('include('), 'ต้องไม่มี include() เหลือ');
  assert.equal((html.match(/<\?/g) || []).length, 1, 'ต้องมี <? แค่ตัวเดียว (boot)');
  assert.equal((html.match(/\?>/g) || []).length, 1);
  assert.equal((html.match(/<\?!= boot \?>/g) || []).length, 1);
  assert.ok(html.includes('<style>') && html.includes('window.__BOOT__'));
  // สคริปต์ฝั่งหน้าเว็บต้อง syntax ถูกต้อง
  const js = html.slice(html.indexOf('<script>\n(function'), html.lastIndexOf('</script>')).replace(/^<script>/, '');
  assert.doesNotThrow(() => new Function(js));
});

test('Code.gs รวมแล้วมีฟังก์ชันสาธารณะเท่าเดิม และไม่มีฟังก์ชันซ้ำชื่อ', () => {
  const { code } = build();
  const names = [...code.matchAll(/^function +([A-Za-z0-9_]+)/gm)].map((m) => m[1]);
  assert.equal(new Set(names).size, names.length, 'มีชื่อฟังก์ชันซ้ำ: ' + names.filter((n, i) => names.indexOf(n) !== i));
  const pub = names.filter((n) => !n.endsWith('_')).sort();
  assert.deepEqual(pub, ['adminCheckData', 'adminClearCache', 'adminConfigure', 'adminGenerateCodes', 'adminPublishOff', 'adminPublishOn',
    'adminResetPassword', 'adminRotateKey', 'adminSetPassword', 'adminSetup', 'adminShowLink', 'api_adminLogin', 'api_adminLogout',
    'api_adminOverview', 'api_adminPdf', 'api_adminStudent', 'api_dashboard', 'api_login', 'api_logout', 'api_pdf', 'api_register',
    'doGet', 'include', 'onOpen'].sort());
});

test('ไฟล์รวม dist/Code.gs เพียงไฟล์เดียวใช้งานได้ครบ: ลงทะเบียน -> ดูคะแนน -> PDF -> ผู้ดูแล', () => {
  const env = createReadyEnv(F, { files: ['dist/Code.gs'] });
  const S = F.STUDENTS;
  const reg = plain(env.ctx.api_register({ studentId: S[0].id, name: S[0].name, password: 'Passw0rd!x' }));
  assert.equal(reg.ok, true, reg.error);
  const dash = plain(env.ctx.api_dashboard(reg.token));
  assert.equal(dash.data.total.score, F.derive(S[0]).official);
  assert.equal(Buffer.from(plain(env.ctx.api_pdf(reg.token)).base64, 'base64').toString(), '%PDF-1.4 fake 1');
  env.state.promptText = '1111';
  env.ctx.adminSetPassword();
  const adm = plain(env.ctx.api_adminLogin(env.state.props.ADMIN_KEY, '1111'));
  assert.equal(plain(env.ctx.api_adminOverview(adm.token)).rows.length, 6);
});
