'use strict';
/**
 * รวมไฟล์ทั้งหมดให้เหลือ 3 ไฟล์ที่คัดลอกวางลง Apps Script ได้ง่าย:
 *   dist/Code.gs          = Config + Lib + Data + Store + Auth + Code + AdminApi + Admin
 *   dist/Index.html       = Index.html ที่ฝัง Styles.html และ Script.html ไว้แล้ว
 *   dist/appsscript.json  = manifest
 * ใช้: node dev/bundle.js   (เทสต์ tests/bundle.test.js ตรวจว่า dist ตรงกับไฟล์ต้นทางเสมอ)
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const GS = ['Config', 'Lib', 'Data', 'Store', 'Auth', 'Code', 'AdminApi', 'Admin'];

function build() {
  const read = (f) => fs.readFileSync(path.join(ROOT, f), 'utf8');
  const code = '/**\n * Score Portal — ไฟล์รวม สร้างอัตโนมัติด้วย dev/bundle.js\n * ห้ามแก้ไฟล์นี้โดยตรง: แก้ที่ไฟล์ต้นทางแล้วรัน node dev/bundle.js ใหม่\n */\n\n' +
    GS.map((n) => '/* ===== ' + n + '.gs ===== */\n' + read(n + '.gs').replace(/\s+$/, '') + '\n').join('\n');
  const html = read('Index.html')
    .replace("<?!= include('Styles'); ?>", () => read('Styles.html').replace(/\s+$/, ''))
    .replace("<?!= include('Script'); ?>", () => read('Script.html').replace(/\s+$/, ''));
  return { code, html, manifest: read('appsscript.json') };
}

if (require.main === module) {
  const out = path.join(ROOT, 'dist');
  fs.mkdirSync(out, { recursive: true });
  const b = build();
  fs.writeFileSync(path.join(out, 'Code.gs'), b.code);
  fs.writeFileSync(path.join(out, 'Index.html'), b.html);
  fs.writeFileSync(path.join(out, 'appsscript.json'), b.manifest);
  console.log('dist/Code.gs', b.code.length, 'chars | dist/Index.html', b.html.length, 'chars');
}

module.exports = { build, GS };
