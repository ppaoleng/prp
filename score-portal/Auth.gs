/**
 * ลงทะเบียน / เข้าสู่ระบบ / เซสชัน
 *
 * - รหัสผ่านเก็บเป็น PBKDF2-HMAC-SHA256 + salt รายคน + pepper (เก็บใน Script Properties ไม่อยู่ในชีต)
 * - ล็อกบัญชีชั่วคราวเมื่อกรอกผิดติดกัน; จำกัดจำนวนครั้งลงทะเบียนต่อรหัสนักศึกษา
 * - เซสชันเก็บฝั่งเซิร์ฟเวอร์ (CacheService) เพิกถอนได้ ไม่ใช้คุกกี้
 */

var USER_COLS_ = ['studentId', 'name', 'salt', 'hash', 'iter', 'registeredAt', 'lastLoginAt', 'failed', 'lockedUntil'];
var CODE_COLS_ = ['studentId', 'name', 'code', 'issuedAt', 'usedAt'];
var GENERIC_LOGIN_ERROR_ = 'รหัสนักศึกษาหรือรหัสผ่านไม่ถูกต้อง (ถ้ายังไม่เคยลงทะเบียน ให้ไปที่แท็บ "ลงทะเบียน" ก่อน)';

function fail_(msg, extra) {
  var r = { ok: false, error: msg };
  if (extra) for (var k in extra) r[k] = extra[k];
  return r;
}

/* ---------- แฮช ---------- */

function sha256Hex_(str) {
  return bytesToHex_(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, str, Utilities.Charset.UTF_8));
}

/** PBKDF2-HMAC-SHA256 (1 บล็อก = 32 ไบต์) -> hex */
function pbkdf2Hex_(password, saltStr, iterations) {
  var key = Utilities.newBlob(password).getBytes();
  var salt = Utilities.newBlob(saltStr).getBytes().concat([0, 0, 0, 1]);
  var u = Utilities.computeHmacSha256Signature(salt, key);
  var t = u.slice();
  for (var i = 1; i < iterations; i++) {
    u = Utilities.computeHmacSha256Signature(u, key);
    for (var k = 0; k < t.length; k++) t[k] ^= u[k];
  }
  return bytesToHex_(t);
}

function getPepper_() {
  var v = PropertiesService.getScriptProperties().getProperty('PEPPER');
  if (!v) throw new Error('ยังไม่ได้ตั้งค่าระบบ: รันเมนู Score Portal > ตั้งค่าเริ่มต้น');
  return v;
}

function hashPassword_(password, salt, iterations) {
  return pbkdf2Hex_(String(password), salt + '|' + getPepper_(), iterations);
}

function randomHex_(bytesLen) {
  var s = '';
  while (s.length < bytesLen * 2) s += Utilities.getUuid().replace(/-/g, '');
  return s.slice(0, bytesLen * 2);
}

/* ---------- จำกัดจำนวนครั้ง ---------- */

function throttle_(bucket, max, windowSec) {
  var cache = CacheService.getScriptCache();
  var now = Date.now(), n = 0, start = now;
  var raw = cache.get(bucket);
  if (raw) {
    var p = raw.split('|');
    n = parseInt(p[0], 10) || 0;
    start = parseInt(p[1], 10) || now;
    if (now - start > windowSec * 1000) { n = 0; start = now; }
  }
  if (n >= max) return false;
  cache.put(bucket, (n + 1) + '|' + start, windowSec);
  return true;
}

/* ---------- เซสชัน ---------- */

function createSession_(idKey, hours) {
  var token = randomHex_(32);
  var ttl = Math.min(21600, Math.floor(hours * 3600)); // CacheService สูงสุด 6 ชม.
  CacheService.getScriptCache().put('sess:' + sha256Hex_(token), idKey + '|' + Date.now(), ttl);
  return { token: token, expiresAt: Date.now() + ttl * 1000 };
}

/** คืนรหัสนักศึกษา (ตัวเลขล้วน) ของเซสชัน หรือ null */
function getSession_(token) {
  if (typeof token !== 'string' || token.length !== 64 || !/^[0-9a-f]+$/.test(token)) return null;
  var cache = CacheService.getScriptCache();
  var raw = cache.get('sess:' + sha256Hex_(token));
  if (!raw) return null;
  var p = raw.split('|');
  var revoked = parseInt(cache.get('revoked:' + p[0]), 10);
  if (revoked && parseInt(p[1], 10) <= revoked) return null;
  return p[0];
}

function destroySession_(token) {
  if (typeof token !== 'string' || token.length !== 64) return;
  CacheService.getScriptCache().remove('sess:' + sha256Hex_(token));
}

/** เพิกถอนทุกเซสชันของนักศึกษา (ใช้ตอนรีเซ็ตรหัสผ่าน) */
function revokeSessions_(idKey) {
  CacheService.getScriptCache().put('revoked:' + idKey, String(Date.now()), 21600);
}

/* ---------- ชีต Users ---------- */

function findRowByStudent_(sheet, idKey, ncols) {
  var last = sheet.getLastRow();
  if (last < 2) return null;
  var vals = sheet.getRange(2, 1, last - 1, ncols).getValues();
  for (var i = 0; i < vals.length; i++) {
    if (normalizeId_(vals[i][0]) === idKey) return { row: i + 2, data: vals[i] };
  }
  return null;
}

function userFromRow_(r) {
  return {
    row: r.row, id: r.data[0], name: r.data[1], salt: String(r.data[2]), hash: String(r.data[3]),
    iter: parseInt(r.data[4], 10) || CONFIG.KDF_ITERATIONS, failed: parseInt(r.data[7], 10) || 0,
    lockedUntil: r.data[8] ? new Date(r.data[8]).getTime() : 0
  };
}

/* ---------- ลงทะเบียน ---------- */

function verifyByCode_(idKey, codeRaw) {
  var sh = getTab_(CONFIG.TAB_CODES);
  var r = findRowByStudent_(sh, idKey, CODE_COLS_.length);
  var input = String(codeRaw == null ? '' : codeRaw).replace(/\s|-/g, '').toUpperCase();
  if (!r || !input) return { ok: false, error: 'รหัสยืนยันไม่ถูกต้อง' };
  if (r.data[4]) return { ok: false, error: 'รหัสยืนยันนี้ถูกใช้ไปแล้ว หากเป็นของท่านโปรดติดต่อผู้สอน' };
  var stored = String(r.data[2]).replace(/\s|-/g, '').toUpperCase();
  if (!safeEqual_(stored, input)) return { ok: false, error: 'รหัสยืนยันไม่ถูกต้อง' };
  return { ok: true, row: r.row };
}

function register_(p) {
  p = p || {};
  var settings = getSettings_();
  var idKey = normalizeId_(p.studentId);
  if (idKey.length < 8) return fail_('รหัสนักศึกษาไม่ถูกต้อง');
  if (!throttle_('reg:' + idKey, CONFIG.MAX_REGISTER_ATTEMPTS, CONFIG.REGISTER_WINDOW_SECONDS)) {
    return fail_('ลองหลายครั้งเกินไป กรุณารอสักครู่ (ประมาณ 15 นาที) แล้วลองใหม่');
  }

  var D = loadClassData_(settings);
  var idx = findStudent_(D, idKey);
  if (idx < 0) return fail_('ไม่พบรหัสนักศึกษานี้ในรายชื่อ กรุณาตรวจสอบรหัสอีกครั้ง');
  var stu = D.students[idx];

  var codeRow = null;
  if (settings.register_verify === 'code') {
    var v = verifyByCode_(idKey, p.code);
    if (!v.ok) { audit_(idKey, 'register_fail', 'code'); return fail_(v.error); }
    codeRow = v.row;
  } else if (normalizeName_(p.name) !== normalizeName_(stu.name)) {
    audit_(idKey, 'register_fail', 'name');
    return fail_('ชื่อ-สกุลไม่ตรงกับรายชื่อ (พิมพ์ชื่อและนามสกุลให้ตรงกับทะเบียน ไม่จำเป็นต้องใส่คำนำหน้า)');
  }

  var pwErr = validatePassword_(p.password, idKey, settings.min_password_length);
  if (pwErr) return fail_(pwErr);

  var salt = randomHex_(16);
  var hash = hashPassword_(p.password, salt, CONFIG.KDF_ITERATIONS);

  var lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    var users = getTab_(CONFIG.TAB_USERS);
    if (findRowByStudent_(users, idKey, USER_COLS_.length)) {
      return fail_('รหัสนักศึกษานี้ลงทะเบียนแล้ว ให้เข้าสู่ระบบ — ถ้าลืมรหัสผ่านโปรดติดต่อผู้สอนเพื่อรีเซ็ต');
    }
    var now = new Date().toISOString();
    users.appendRow([stu.id, stu.name, salt, hash, CONFIG.KDF_ITERATIONS, now, now, 0, '']);
    if (codeRow) getTab_(CONFIG.TAB_CODES).getRange(codeRow, 5).setValue(now);
  } finally {
    lock.releaseLock();
  }
  audit_(idKey, 'register_ok', settings.register_verify);
  var s = createSession_(idKey, settings.session_hours);
  return { ok: true, token: s.token, expiresAt: s.expiresAt, name: stu.name };
}

/* ---------- เข้าสู่ระบบ ---------- */

function login_(p) {
  p = p || {};
  var settings = getSettings_();
  var idKey = normalizeId_(p.studentId);
  var password = String(p.password == null ? '' : p.password);
  if (idKey.length < 8 || !password || password.length > 128) return fail_(GENERIC_LOGIN_ERROR_);

  var users = getTab_(CONFIG.TAB_USERS);
  var found = findRowByStudent_(users, idKey, USER_COLS_.length);
  if (!found) { audit_(idKey, 'login_fail', 'no_user'); return fail_(GENERIC_LOGIN_ERROR_); }
  var u = userFromRow_(found);

  var now = Date.now();
  if (u.lockedUntil > now) {
    var mins = Math.ceil((u.lockedUntil - now) / 60000);
    return fail_('กรอกรหัสผ่านผิดหลายครั้ง บัญชีถูกล็อกชั่วคราว กรุณารออีกประมาณ ' + mins + ' นาที');
  }

  var ok = safeEqual_(hashPassword_(password, u.salt, u.iter), u.hash);

  var lock = LockService.getScriptLock();
  lock.waitLock(15000);
  try {
    var cur = findRowByStudent_(users, idKey, USER_COLS_.length);
    if (!cur) return fail_(GENERIC_LOGIN_ERROR_);
    var row = cur.data.slice(0, USER_COLS_.length);
    if (ok) {
      row[6] = new Date().toISOString();
      row[7] = 0;
      row[8] = '';
    } else {
      var failed = (parseInt(row[7], 10) || 0) + 1;
      if (failed >= CONFIG.MAX_FAILED_LOGINS) {
        row[7] = 0;
        row[8] = new Date(now + CONFIG.LOCK_MINUTES * 60000).toISOString();
      } else {
        row[7] = failed;
      }
    }
    users.getRange(cur.row, 1, 1, USER_COLS_.length).setValues([row]);
  } finally {
    lock.releaseLock();
  }

  if (!ok) { audit_(idKey, 'login_fail', 'bad_password'); return fail_(GENERIC_LOGIN_ERROR_); }
  audit_(idKey, 'login_ok', '');
  var s = createSession_(idKey, settings.session_hours);
  return { ok: true, token: s.token, expiresAt: s.expiresAt, name: u.name };
}
