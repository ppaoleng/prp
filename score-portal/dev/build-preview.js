'use strict';
/**
 * สร้างหน้าพรีวิวสำหรับดูหน้าตาในเบราว์เซอร์โดยไม่ต้องใช้ Google
 *   node dev/build-preview.js <outDir> [state]
 * - ประกอบ Index.html + Styles.html + Script.html เหมือนที่ Apps Script ทำ
 * - แทน google.script.run ด้วยตัวจำลองที่เรียก "โค้ดเซิร์ฟเวอร์จริง" (api_*) ผ่านข้อมูลสมมติ
 *   จึงเห็นรูปแบบข้อมูลที่หน้าเว็บจะได้รับจริง (ข้อมูลทั้งหมดเป็นข้อมูลสมมติ)
 */
const fs = require('fs');
const path = require('path');
const F = require('../tests/fixtures');
const { createReadyEnv } = require('../tests/harness');

const ROOT = path.join(__dirname, '..');
const out = process.argv[2] || path.join(__dirname, 'out');
const mode = process.argv[3] || 'published'; // published | locked
fs.mkdirSync(out, { recursive: true });

// XSS=1: ใส่ HTML/JS ในชื่อ ประกาศ ความเห็น และหัวข้อ เพื่อทดสอบว่าหน้าเว็บ escape ครบ
if (process.env.XSS) {
  const bad = '<img src=x onerror="window.__xss=1">';
  F.STUDENTS[2].name = 'นาย' + bad;
  F.feedbackTab = () => [['x'], ['ลำดับ', 'ชื่อ-สกุล', 'ข้อ', 'ความเห็น'], [3, F.STUDENTS[2].name, 'อัตนัย 1', bad + '<script>window.__xss=2</script>']];
}
const env = createReadyEnv(F, { published: mode === 'published' });
env.setting('show_feedback', true);
env.setting('notice', process.env.XSS ? '</script><img src=x onerror="window.__xss=3">' : 'ผลคะแนนเป็นผลเบื้องต้น หากพบข้อผิดพลาดแจ้งผู้สอนภายใน 7 วัน');
const plain = (x) => JSON.parse(JSON.stringify(x));

// สมัครนักศึกษาสมมติ 1 คนไว้ล่วงหน้า (ลำดับ 3) เพื่อให้ล็อกอินในพรีวิวได้
const PW = 'Preview123';
const me = F.STUDENTS[2];
env.ctx.api_register({ studentId: me.id, name: me.name, password: PW });

// ตัวอย่าง PDF: ถ้ามีไฟล์ sample.pdf ให้ใช้ (สร้างด้วย Playwright) ไม่งั้นใช้ไฟล์ว่าง
const samplePdf = path.join(out, 'sample.pdf');
const pdfB64 = fs.existsSync(samplePdf) ? fs.readFileSync(samplePdf).toString('base64') : '';

const boot = plain(env.ctx.getSettings_());
const bootObj = { title: boot.course_title, subtitle: boot.course_subtitle, notice: boot.notice, published: boot.published, registerVerify: boot.register_verify, ready: true };
const jsonForScript = (o) => env.ctx.jsonForScript_(o);

const handlers = {
  api_login: (p) => plain(env.ctx.api_login(p)),
  api_register: (p) => plain(env.ctx.api_register(p)),
  api_logout: (t) => plain(env.ctx.api_logout(t)),
  api_dashboard: (t) => plain(env.ctx.api_dashboard(t)),
  api_pdf: (t) => {
    const r = plain(env.ctx.api_pdf(t));
    if (pdfB64 && r.ok) r.base64 = pdfB64;
    return r;
  }
};
// ผลลัพธ์ทุกกรณีที่หน้าเว็บอาจเรียก ถูกคำนวณล่วงหน้าแล้วฝังเป็นตาราง (ไม่มีเซิร์ฟเวอร์ตอนรันจริง)
const loginAs = plain(env.ctx.api_login({ studentId: me.id, password: PW }));
const snapshot = {
  token: loginAs.token,
  dashboard: handlers.api_dashboard(loginAs.token),
  pdf: handlers.api_pdf(loginAs.token),
  loginOk: loginAs
};
const fail = (msg) => ({ ok: false, error: msg });

const mock = `
<script>
(function(){
  var S = ${jsonForScript(snapshot)};
  var users = {}; users[${JSON.stringify(me.id)}] = ${JSON.stringify(PW)};
  function digits(s){ return String(s||'').replace(/\\D/g,''); }
  var api = {
    api_login: function(p){
      if (users[Object.keys(users).filter(function(k){return digits(k)===digits(p.studentId)})[0]] === p.password) return S.loginOk;
      return ${JSON.stringify(fail('รหัสนักศึกษาหรือรหัสผ่านไม่ถูกต้อง (ถ้ายังไม่เคยลงทะเบียน ให้ไปที่แท็บ "ลงทะเบียน" ก่อน)'))};
    },
    api_register: function(p){ return p.name ? S.loginOk : ${JSON.stringify(fail('ชื่อ-สกุลไม่ตรงกับรายชื่อ'))}; },
    api_logout: function(){ return {ok:true}; },
    api_dashboard: function(t){ return t === S.token ? S.dashboard : {ok:false, expired:true, error:'x'}; },
    api_pdf: function(t){ return t === S.token ? S.pdf : {ok:false, expired:true, error:'x'}; }
  };
  window.google = { script: { run: (function make(ok, ko){
    return new Proxy({}, { get: function(_, name){
      if (name === 'withSuccessHandler') return function(f){ return make(f, ko); };
      if (name === 'withFailureHandler') return function(f){ return make(ok, f); };
      return function(){ var a = arguments; setTimeout(function(){ try { ok && ok(api[name].apply(null, a)); } catch (e) { ko && ko(e); } }, 250); };
    }});
  })() } };
})();
</script>`;

const read = (f) => fs.readFileSync(path.join(ROOT, f), 'utf8');
let html = read('Index.html')
  .replace("<?!= include('Styles'); ?>", () => read('Styles.html'))
  .replace("<?!= include('Script'); ?>", () => read('Script.html'))
  .replace('<?!= boot ?>', () => jsonForScript(bootObj))
  .replace('<script>window.__BOOT__', () => mock + '\n<script>window.__BOOT__');
fs.writeFileSync(path.join(out, 'index.html'), html);
fs.writeFileSync(path.join(out, 'meta.json'), JSON.stringify({ id: me.id, password: PW, name: me.name }));
console.log('wrote', path.join(out, 'index.html'), '(' + html.length + ' bytes)');
