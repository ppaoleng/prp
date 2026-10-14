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
