/**
 * จุดเข้าของเว็บแอป + API ที่หน้าเว็บเรียกผ่าน google.script.run
 *
 * ข้อควรระวัง: ฟังก์ชันระดับบนสุดที่ "ไม่ลงท้ายด้วย _" ใครก็เรียกผ่านหน้าเว็บได้
 * ดังนั้นฟังก์ชัน api_* ทุกตัวต้องตรวจเซสชันเอง และตัวช่วยอื่นต้องลงท้ายด้วย _
 */

function doGet() {
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
    var me = D.students[idx];

    var fileId = resolvePdfId_(me, listPdfMap_(settings, false));
    if (!fileId) fileId = resolvePdfId_(me, listPdfMap_(settings, true)); // รีเฟรชรายการไฟล์หนึ่งครั้ง
    if (!fileId) return fail_('ยังไม่พบไฟล์ PDF ของท่านในโฟลเดอร์ กรุณาติดต่อผู้สอน');

    var file = DriveApp.getFileById(fileId);
    if (file.getSize() > CONFIG.MAX_PDF_BYTES) return fail_('ไฟล์ PDF ใหญ่เกินกว่าจะแสดงบนหน้าเว็บ กรุณาติดต่อผู้สอน');
    audit_(idKey, 'pdf_view', '');
    return {
      ok: true,
      name: me.pdfName || file.getName(),
      base64: Utilities.base64Encode(file.getBlob().getBytes())
    };
  });
}
