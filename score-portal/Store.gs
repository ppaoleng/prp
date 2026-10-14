/**
 * ชั้นเก็บข้อมูล: แคช, ตั้งค่า, ชีตฐานข้อมูล (Users/Codes/Audit), โหลดข้อมูลห้อง และรายการไฟล์ PDF
 */

/* ---------- แคช (แบ่งก้อนเพราะ CacheService จำกัด ~100KB ต่อค่า) ---------- */

var CACHE_CHUNK_ = 30000;

function cachePutJson_(key, obj, ttl) {
  try {
    var s = JSON.stringify(obj);
    var n = Math.max(1, Math.ceil(s.length / CACHE_CHUNK_));
    var map = {};
    for (var i = 0; i < n; i++) map[key + ':' + i] = s.substr(i * CACHE_CHUNK_, CACHE_CHUNK_);
    map[key + ':n'] = String(n);
    CacheService.getScriptCache().putAll(map, ttl);
  } catch (e) { /* แคชพลาดไม่เป็นไร ระบบอ่านจากชีตตรงๆ ได้ */ }
}

function cacheGetJson_(key) {
  try {
    var cache = CacheService.getScriptCache();
    var n = parseInt(cache.get(key + ':n'), 10);
    if (!n) return null;
    var keys = [];
    for (var i = 0; i < n; i++) keys.push(key + ':' + i);
    var got = cache.getAll(keys), s = '';
    for (var j = 0; j < n; j++) {
      if (got[keys[j]] == null) return null;
      s += got[keys[j]];
    }
    return JSON.parse(s);
  } catch (e) { return null; }
}

function cacheRemoveJson_(key) {
  try { CacheService.getScriptCache().remove(key + ':n'); } catch (e) { /* ignore */ }
}

function clearAllCaches_() {
  ['classdata', 'settings', 'pdfmap'].forEach(cacheRemoveJson_);
}

/* ---------- ชีตฐานข้อมูล ---------- */

function getDb_() {
  var id = PropertiesService.getScriptProperties().getProperty('DB_ID');
  if (id) return SpreadsheetApp.openById(id);
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  if (!ss) throw new Error('ยังไม่ได้ตั้งค่าชีตฐานข้อมูล: เปิดชีตที่ผูกกับสคริปต์แล้วเมนู Score Portal > ตั้งค่าเริ่มต้น');
  return ss;
}

function getTab_(name) {
  var sh = getDb_().getSheetByName(name);
  if (!sh) throw new Error('ไม่พบแท็บ "' + name + '" — รันเมนู Score Portal > ตั้งค่าเริ่มต้น');
  return sh;
}

/* ---------- ตั้งค่า (แท็บ Settings) ---------- */

function getSettings_() {
  var cached = cacheGetJson_('settings');
  if (cached) return cached;
  var out = {}, defaults = {};
  SETTINGS_DEFAULTS.forEach(function (d) { defaults[d[0]] = d[1]; out[d[0]] = d[1]; });
  var sh = getDb_().getSheetByName(CONFIG.TAB_SETTINGS);
  if (sh) {
    var rows = sh.getDataRange().getValues();
    for (var r = 0; r < rows.length; r++) {
      var key = cell_(rows[r][0]);
      if (!Object.prototype.hasOwnProperty.call(defaults, key)) continue;
      var raw = rows[r][1], d = defaults[key];
      if (typeof d === 'boolean') out[key] = asBool_(raw, d);
      else if (typeof d === 'number') { var n = toNum_(raw); out[key] = n == null ? d : n; }
      else out[key] = cell_(raw);
    }
  }
  if (!{ official: 1, mcq_floor0: 1, no_partial_q2: 1 }[out.total_mode]) out.total_mode = 'official';
  if (!{ name: 1, code: 1 }[out.register_verify]) out.register_verify = 'name';
  out.session_hours = Math.min(6, Math.max(0.25, out.session_hours));
  out.min_password_length = Math.max(6, Math.floor(out.min_password_length));
  cachePutJson_('settings', out, CONFIG.CACHE_SETTINGS_SECONDS);
  return out;
}

/* ---------- Audit log (ไม่บันทึกรหัสผ่าน) ---------- */

function audit_(studentKey, event, detail) {
  try {
    getTab_(CONFIG.TAB_AUDIT).appendRow([new Date().toISOString(), studentKey || '', event, detail || '']);
  } catch (e) { /* ล็อกพลาดต้องไม่ทำให้ระบบล่ม */ }
}

/* ---------- โหลดข้อมูลห้องจากชีตคะแนน ---------- */

function getScoresSpreadsheet_(settings) {
  if (!settings.scores_spreadsheet_id) {
    throw new Error('ยังไม่ได้ตั้งค่า scores_spreadsheet_id ในแท็บ Settings');
  }
  return SpreadsheetApp.openById(settings.scores_spreadsheet_id);
}

function findSheet_(ss, name) {
  var exact = ss.getSheetByName(name);
  if (exact) return exact;
  var all = ss.getSheets();
  for (var i = 0; i < all.length; i++) if (all[i].getName().indexOf(name) !== -1) return all[i];
  return null;
}

function readTab_(ss, name, required) {
  var sh = findSheet_(ss, name);
  if (!sh) {
    if (required) throw new Error('ไม่พบแท็บ "' + name + '" ในชีตคะแนน');
    return null;
  }
  return sh.getDataRange().getValues();
}

/** อ่านชีตคะแนนทั้งหมด (ไม่ใช้แคช) -> ข้อมูลห้อง */
function readClassData_(settings) {
  var ss = getScoresSpreadsheet_(settings);
  var extra = [];
  var summary = parseSummary_(readTab_(ss, CONFIG.TAB_SUMMARY, true));

  function optional(tab, fn) {
    var v = readTab_(ss, tab, false);
    if (!v) { extra.push('ไม่พบแท็บ "' + tab + '" (ข้ามส่วนนี้)'); return null; }
    try { return fn(v); } catch (e) { extra.push(String(e.message || e)); return null; }
  }
  var mcq = optional(CONFIG.TAB_MCQ, parseMcq_);
  var written = optional(CONFIG.TAB_WRITTEN, parseWritten_);
  var feedback = optional(CONFIG.TAB_FEEDBACK, parseFeedback_);
  var D = buildClassData_(summary, mcq, written, feedback);
  D.warnings = extra.concat(D.warnings);
  return D;
}

function loadClassData_(settings, forceFresh) {
  if (!forceFresh) {
    var cached = cacheGetJson_('classdata');
    if (cached) return cached;
  }
  var D = readClassData_(settings);
  cachePutJson_('classdata', D, CONFIG.CACHE_DATA_SECONDS);
  return D;
}

/* ---------- รายการไฟล์ PDF ในโฟลเดอร์ ---------- */

function listPdfMap_(settings, forceFresh) {
  if (!forceFresh) {
    var cached = cacheGetJson_('pdfmap');
    if (cached) return cached;
  }
  if (!settings.pdf_folder_id) throw new Error('ยังไม่ได้ตั้งค่า pdf_folder_id ในแท็บ Settings');
  var map = {};
  var files = DriveApp.getFolderById(settings.pdf_folder_id).getFiles();
  while (files.hasNext()) {
    var f = files.next();
    if (f.getMimeType() === 'application/pdf') map[normalizeFileName_(f.getName())] = f.getId();
  }
  cachePutJson_('pdfmap', map, CONFIG.CACHE_PDFMAP_SECONDS);
  return map;
}
