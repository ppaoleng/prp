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
      .addItem('2) ตรวจสอบข้อมูลคะแนนและ PDF', 'adminCheckData')
      .addSeparator()
      .addItem('เปิดประกาศผล', 'adminPublishOn')
      .addItem('ปิดประกาศผล (ล็อก)', 'adminPublishOff')
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
