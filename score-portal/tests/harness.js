'use strict';
/**
 * โหลดไฟล์ .gs ทั้งหมดเข้า vm เดียว (เหมือน Apps Script ที่รวมทุกไฟล์เป็น global เดียว)
 * พร้อมตัวจำลองบริการของ Google ที่ใช้จริง: Utilities, CacheService, PropertiesService, LockService,
 * SpreadsheetApp, DriveApp, Session — เก็บทุกอย่างในหน่วยความจำ
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const crypto = require('crypto');

const ROOT = path.join(__dirname, '..');
const FILES = ['Config.gs', 'Lib.gs', 'Data.gs', 'Store.gs', 'Auth.gs', 'Code.gs', 'Admin.gs'];

const toBuf = (x) => (typeof x === 'string' ? Buffer.from(x, 'utf8') : Buffer.from(x.map((b) => b & 255)));
const toSigned = (buf) => Array.from(buf).map((b) => (b > 127 ? b - 256 : b));

class MockSheet {
  constructor(name, rows) {
    this.name = name;
    this.rows = (rows || []).map((r) => r.slice());
    this.formats = [];
  }
  getName() { return this.name; }
  getLastRow() { return this.rows.length; }
  getDataRange() {
    const self = this;
    return {
      getValues() {
        const w = Math.max(0, ...self.rows.map((r) => r.length));
        return self.rows.map((r) => { const c = r.slice(); while (c.length < w) c.push(''); return c; });
      }
    };
  }
  appendRow(r) { this.rows.push(r.slice()); }
  deleteRow(i) { this.rows.splice(i - 1, 1); }
  setFrozenRows() {}
  setColumnWidth() {}
  getRange(a, b, nr, nc) {
    const self = this;
    if (typeof a === 'string') {
      return { setNumberFormat(f) { self.formats.push([a, f]); return this; }, setFontWeight() { return this; } };
    }
    const r0 = a, c0 = b, R = nr || 1, C = nc || 1;
    return {
      getValues() {
        const out = [];
        for (let i = 0; i < R; i++) {
          const row = [];
          for (let j = 0; j < C; j++) { const v = (self.rows[r0 - 1 + i] || [])[c0 - 1 + j]; row.push(v === undefined ? '' : v); }
          out.push(row);
        }
        return out;
      },
      setValues(vals) {
        for (let i = 0; i < vals.length; i++) {
          while (self.rows.length < r0 + i) self.rows.push([]);
          for (let j = 0; j < vals[i].length; j++) self.rows[r0 - 1 + i][c0 - 1 + j] = vals[i][j];
        }
        return this;
      },
      setValue(v) { return this.setValues([[v]]); },
      setNumberFormat() { return this; },
      setFontWeight() { return this; }
    };
  }
}

class MockSpreadsheet {
  constructor(id, tabs) {
    this.id = id;
    this.sheets = Object.keys(tabs || {}).map((n) => new MockSheet(n, tabs[n]));
  }
  getId() { return this.id; }
  getSheets() { return this.sheets; }
  getSheetByName(n) { return this.sheets.find((s) => s.name === n) || null; }
  insertSheet(n) { const s = new MockSheet(n, []); this.sheets.push(s); return s; }
}

function createEnv(opts = {}) {
  const state = {
    spreadsheets: {},
    cache: new Map(),
    props: {},
    drive: { folders: {}, files: {} },
    session: { effective: 'owner@example.com', active: 'owner@example.com' },
    uiLog: [],
    now: null
  };
  const db = new MockSpreadsheet('DB1', {});
  state.spreadsheets.DB1 = db;

  const cacheApi = {
    get(k) { const e = state.cache.get(k); if (!e) return null; if (e.exp && e.exp < Date.now()) { state.cache.delete(k); return null; } return e.v; },
    put(k, v, ttl) { state.cache.set(k, { v: String(v), exp: ttl ? Date.now() + ttl * 1000 : 0 }); },
    putAll(m, ttl) { Object.keys(m).forEach((k) => cacheApi.put(k, m[k], ttl)); },
    getAll(keys) { const o = {}; keys.forEach((k) => { const v = cacheApi.get(k); if (v != null) o[k] = v; }); return o; },
    remove(k) { state.cache.delete(k); }
  };

  const sandbox = {
    console,
    Date,
    JSON,
    Math,
    Utilities: {
      DigestAlgorithm: { SHA_256: 'SHA_256' },
      Charset: { UTF_8: 'UTF_8' },
      computeDigest(alg, str) { return toSigned(crypto.createHash('sha256').update(toBuf(str)).digest()); },
      computeHmacSha256Signature(value, key) { return toSigned(crypto.createHmac('sha256', toBuf(key)).update(toBuf(value)).digest()); },
      newBlob(s) { return { getBytes: () => toSigned(Buffer.from(String(s), 'utf8')) }; },
      getUuid() { return crypto.randomUUID(); },
      base64Encode(bytes) { return toBuf(bytes).toString('base64'); }
    },
    CacheService: { getScriptCache: () => cacheApi },
    PropertiesService: {
      getScriptProperties: () => ({
        getProperty: (k) => (k in state.props ? state.props[k] : null),
        setProperty: (k, v) => { state.props[k] = String(v); }
      })
    },
    LockService: { getScriptLock: () => ({ waitLock() {}, releaseLock() {} }) },
    SpreadsheetApp: {
      getActiveSpreadsheet: () => db,
      openById(id) { if (!state.spreadsheets[id]) throw new Error('no spreadsheet ' + id); return state.spreadsheets[id]; },
      getUi: () => ({
        alert(m) { state.uiLog.push(m); },
        prompt() { return { getSelectedButton: () => 'OK', getResponseText: () => state.promptText || '' }; },
        ButtonSet: { OK_CANCEL: 1 }, Button: { OK: 'OK' },
        createMenu: () => { const m = { addItem: () => m, addSeparator: () => m, addToUi: () => m }; return m; }
      })
    },
    DriveApp: {
      getFolderById(id) {
        const files = state.drive.folders[id];
        if (!files) throw new Error('no folder ' + id);
        let i = 0;
        return { getFiles: () => ({ hasNext: () => i < files.length, next: () => state.drive.files[files[i++]] }) };
      },
      getFileById(id) { if (!state.drive.files[id]) throw new Error('no file ' + id); return state.drive.files[id]; }
    },
    Session: {
      getEffectiveUser: () => ({ getEmail: () => state.session.effective }),
      getActiveUser: () => ({ getEmail: () => state.session.active })
    },
    HtmlService: {}
  };
  const ctx = vm.createContext(sandbox);
  FILES.forEach((f) => vm.runInContext(fs.readFileSync(path.join(ROOT, f), 'utf8'), ctx, { filename: f }));

  const env = {
    ctx, state, db,
    addScores(id, tabs) { state.spreadsheets[id] = new MockSpreadsheet(id, tabs); return state.spreadsheets[id]; },
    addPdf(folderId, fileId, name, bytes) {
      state.drive.files[fileId] = {
        getId: () => fileId, getName: () => name, getMimeType: () => 'application/pdf',
        getSize: () => bytes.length, getBlob: () => ({ getBytes: () => toSigned(Buffer.from(bytes)) })
      };
      (state.drive.folders[folderId] = state.drive.folders[folderId] || []).push(fileId);
    },
    setting(key, value) {
      const sh = db.getSheetByName('Settings');
      const row = sh.rows.find((r) => r[0] === key);
      if (row) row[1] = value; else sh.rows.push([key, value, '']);
      ctx.clearAllCaches_();
    },
    asVisitor() { state.session.active = ''; },
    asOwner() { state.session.active = state.session.effective; },
    call(fn, ...args) { return vm.runInContext(fn, ctx)(...args); }
  };
  return env;
}

/** สภาพแวดล้อมพร้อมใช้: ตั้งค่าแล้ว มีชีตคะแนนสมมติและ PDF ครบ */
function createReadyEnv(fixtures, { published = true, pdf = true } = {}) {
  const env = createEnv();
  env.ctx.adminSetup();
  env.addScores('SCORES1', {
    'สรุปคะแนน': fixtures.summaryTab(),
    'ปรนัยรายข้อ': fixtures.mcqTab(),
    'อัตนัยรายข้อ': fixtures.writtenTab(),
    'ข้อควรพิจารณา': fixtures.feedbackTab()
  });
  env.setting('scores_spreadsheet_id', 'SCORES1');
  env.setting('pdf_folder_id', 'FOLDER1');
  env.setting('published', published);
  if (pdf) {
    fixtures.STUDENTS.forEach((s) => env.addPdf('FOLDER1', 'F' + s.seq, s.pdf, Buffer.from('%PDF-1.4 fake ' + s.seq)));
  }
  return env;
}

module.exports = { createEnv, createReadyEnv, MockSheet, MockSpreadsheet };
