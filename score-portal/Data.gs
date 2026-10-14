/**
 * อ่านและแปลงข้อมูลจากชีตสรุปคะแนน (แท็บ สรุปคะแนน / ปรนัยรายข้อ / อัตนัยรายข้อ / ข้อควรพิจารณา)
 * ฟังก์ชัน parse*_ รับอาร์เรย์ 2 มิติ (getValues) จึงทดสอบนอก Google ได้
 * การหาคอลัมน์ใช้ "ข้อความหัวตาราง" ไม่ใช้ตำแหน่ง ผู้สอนเพิ่ม/ย้ายคอลัมน์ได้
 *
 * หมายเหตุความเป็นส่วนตัว: คอลัมน์ "ข้อควรพิจารณา" ในแท็บสรุปคะแนน (บันทึกภายในถึงผู้สอน)
 * ไม่ถูกอ่านเข้าระบบเลย
 */

var INTERNAL_COMMENT_RE_ = /ผู้สอน|ลำดับที่\s*\d+|คัดลอก|ผู้ช่วยตรวจ/;

function findHeaderRow_(values, pred, maxScan) {
  var n = Math.min(values.length, maxScan || 40);
  for (var r = 0; r < n; r++) {
    if (pred((values[r] || []).map(cell_))) return r;
  }
  return -1;
}

function colWhere_(head, pred) {
  for (var i = 0; i < head.length; i++) if (pred(head[i], i)) return i;
  return -1;
}

function colStarts_(head, prefix) {
  return colWhere_(head, function (c) { return c.indexOf(prefix) === 0; });
}

/** ดึงคะแนนเต็มจากหัวคอลัมน์ เช่น "อัตนัยข้อ 1 (20)" "ปรนัยที่ใช้ (สูงสุด 40)" */
function maxFromHeader_(text, fallback) {
  var m = /\((?:สูงสุด\s*)?(\d+(?:\.\d+)?)\)/.exec(String(text || ''));
  return m ? parseFloat(m[1]) : fallback;
}

function isSeq_(v) {
  var n = toNum_(v);
  return n != null && n > 0 && Math.floor(n) === n;
}

/* ---------- แท็บ สรุปคะแนน ---------- */

function parseSummary_(values) {
  var h = findHeaderRow_(values, function (row) { return row.indexOf('รหัสนักศึกษา') !== -1; });
  if (h < 0) throw new Error('แท็บ "' + CONFIG.TAB_SUMMARY + '": ไม่พบหัวคอลัมน์ "รหัสนักศึกษา"');
  var head = values[h].map(cell_);
  var col = {
    seq: head.indexOf('ลำดับ'),
    id: head.indexOf('รหัสนักศึกษา'),
    name: head.indexOf('ชื่อ-สกุล'),
    group: colStarts_(head, 'กลุ่ม'),
    mcqCorrect: head.indexOf('ปรนัยถูก'),
    mcqWrong: head.indexOf('ปรนัยผิด'),
    mcqBlank: head.indexOf('ไม่ตอบ'),
    mcqFormula: colStarts_(head, 'ปรนัยตามสูตร'),
    mcqUsed: colStarts_(head, 'ปรนัยที่ใช้'),
    w1: colStarts_(head, 'อัตนัยข้อ 1'),
    w2: colStarts_(head, 'อัตนัยข้อ 2'),
    w3: colStarts_(head, 'อัตนัยข้อ 3'),
    wTotal: colStarts_(head, 'อัตนัยรวม'),
    tOfficial: colStarts_(head, 'คะแนนรวม'),
    tFloor0: colStarts_(head, 'รวม ถ้าปรนัย'),
    tNoPartial: colStarts_(head, 'รวม ถ้าข้อ 2'),
    pdf: colStarts_(head, 'ไฟล์ PDF')
  };
  var labels = { id: 'รหัสนักศึกษา', name: 'ชื่อ-สกุล', mcqUsed: 'ปรนัยที่ใช้', w1: 'อัตนัยข้อ 1', w2: 'อัตนัยข้อ 2', w3: 'อัตนัยข้อ 3', tOfficial: 'คะแนนรวม' };
  var missing = [];
  Object.keys(labels).forEach(function (k) { if (col[k] < 0) missing.push(labels[k]); });
  if (missing.length) {
    throw new Error('แท็บ "' + CONFIG.TAB_SUMMARY + '": ไม่พบหัวคอลัมน์ ' + missing.join(', '));
  }

  var max = {
    mcq: maxFromHeader_(head[col.mcqUsed], CONFIG.MCQ_CAP_DEFAULT),
    w: [
      maxFromHeader_(head[col.w1], CONFIG.WRITTEN_MAX_DEFAULT),
      maxFromHeader_(head[col.w2], CONFIG.WRITTEN_MAX_DEFAULT),
      maxFromHeader_(head[col.w3], CONFIG.WRITTEN_MAX_DEFAULT)
    ],
    total: maxFromHeader_(head[col.tOfficial], CONFIG.TOTAL_MAX_DEFAULT)
  };
  max.written = col.wTotal >= 0 ? maxFromHeader_(head[col.wTotal], sum_(max.w)) : sum_(max.w);

  function num(row, c) { return c >= 0 ? toNum_(row[c]) : null; }
  var students = [];
  for (var r = h + 1; r < values.length; r++) {
    var row = values[r] || [];
    var idKey = normalizeId_(row[col.id]);
    if (idKey.length < 8) continue; // แถวสถิติท้ายตาราง (เฉลี่ย/สูงสุด/ต่ำสุด) ไม่มีรหัสนักศึกษา
    var w = [num(row, col.w1), num(row, col.w2), num(row, col.w3)];
    var wTotal = num(row, col.wTotal);
    if (wTotal == null && w.every(function (x) { return x != null; })) wTotal = sum_(w);
    var used = num(row, col.mcqUsed);
    var official = num(row, col.tOfficial);
    if (official == null && used != null && wTotal != null) official = used + wTotal;
    var floor0 = num(row, col.tFloor0);
    if (floor0 == null && used != null && wTotal != null) floor0 = Math.max(0, used) + wTotal;
    students.push({
      seq: col.seq >= 0 && isSeq_(row[col.seq]) ? toNum_(row[col.seq]) : students.length + 1,
      id: cell_(row[col.id]),
      idKey: idKey,
      name: cell_(row[col.name]),
      group: col.group >= 0 ? cell_(row[col.group]) : '',
      pdfName: col.pdf >= 0 ? cell_(row[col.pdf]) : '',
      mcq: {
        correct: num(row, col.mcqCorrect), wrong: num(row, col.mcqWrong), blank: num(row, col.mcqBlank),
        formula: num(row, col.mcqFormula), used: used
      },
      w: w,
      wTotal: wTotal,
      totals: { official: official, mcq_floor0: floor0, no_partial_q2: num(row, col.tNoPartial) }
    });
  }
  return { students: students, max: max };
}

/* ---------- แท็บ ปรนัยรายข้อ ---------- */

var MCQ_CHOICES_ = 'กขคงจ';

function cleanChoice_(v) {
  var c = cell_(v).charAt(0);
  return c && MCQ_CHOICES_.indexOf(c) !== -1 ? c : null;
}

function parseMcq_(values) {
  var h = findHeaderRow_(values, function (row) {
    return row.indexOf('ชื่อ-สกุล') !== -1 && row.some(function (c) { return /^ข้อ ?1$/.test(c); });
  });
  if (h < 0) throw new Error('แท็บ "' + CONFIG.TAB_MCQ + '": ไม่พบหัวตาราง (ชื่อ-สกุล, ข้อ 1, ข้อ 2, ...)');
  var head = values[h].map(cell_);
  var cols = [];
  head.forEach(function (c, i) {
    var m = /^ข้อ ?(\d+)$/.exec(c);
    if (m) cols.push({ no: parseInt(m[1], 10), col: i });
  });
  cols.sort(function (a, b) { return a.no - b.no; });
  var colSeq = head.indexOf('ลำดับ'), colName = head.indexOf('ชื่อ-สกุล');

  // แถวเฉลย: แถวใต้หัวตารางที่มีคำว่า "เฉลย"
  var key = {};
  for (var r = h + 1; r < Math.min(values.length, h + 8); r++) {
    var row = values[r] || [];
    var hasLabel = row.some(function (c) { return cell_(c).indexOf('เฉลย') !== -1; });
    if (!hasLabel) continue;
    cols.forEach(function (c) {
      var ch = cleanChoice_(row[c.col]);
      if (ch) key[c.no] = ch;
    });
    if (Object.keys(key).length < cols.length) { // เฉลยไม่ตรงคอลัมน์ -> ไล่ตัวเลือกตามลำดับ
      var letters = [];
      row.forEach(function (c) { if (/^[กขคงจ]$/.test(cell_(c))) letters.push(cell_(c)); });
      if (letters.length === cols.length) {
        key = {};
        cols.forEach(function (c, k) { key[c.no] = letters[k]; });
      }
    }
    break;
  }

  var rows = {};
  for (var q = h + 1; q < values.length; q++) {
    var rw = values[q] || [];
    if (colSeq < 0 || !isSeq_(rw[colSeq]) || !cell_(rw[colName])) continue;
    rows[toNum_(rw[colSeq])] = {
      name: cell_(rw[colName]),
      answers: cols.map(function (c) { return cleanChoice_(rw[c.col]); })
    };
  }
  return { items: cols.map(function (c) { return c.no; }), key: key, rows: rows };
}

/* ---------- แท็บ อัตนัยรายข้อ ---------- */

function parseWritten_(values) {
  var h = findHeaderRow_(values, function (row) {
    return row.indexOf('ชื่อ-สกุล') !== -1 && row.some(function (c) { return /^ข้อ ?\d+ .+/.test(c); });
  });
  if (h < 0) throw new Error('แท็บ "' + CONFIG.TAB_WRITTEN + '": ไม่พบหัวตาราง (ชื่อ-สกุล, ข้อ1 ..., ข้อ 1 รวม)');
  var head = values[h].map(cell_);
  var qs = {};
  head.forEach(function (c, i) {
    var m = /^ข้อ ?(\d+) (.+)$/.exec(c);
    if (!m) return;
    var no = parseInt(m[1], 10);
    var q = qs[no] || (qs[no] = { no: no, items: [], totalCol: -1 });
    if (m[2].trim() === 'รวม') q.totalCol = i;
    else q.items.push({ label: m[2].trim(), col: i });
  });
  var questions = Object.keys(qs).map(function (k) { return qs[k]; }).sort(function (a, b) { return a.no - b.no; });
  var colSeq = head.indexOf('ลำดับ'), colName = head.indexOf('ชื่อ-สกุล');
  var colTotal = colStarts_(head, 'อัตนัยรวม');

  // แถว "คะแนนเต็ม" ใต้หัวตาราง
  var maxRow = null;
  for (var r = h + 1; r < Math.min(values.length, h + 6); r++) {
    var rr = values[r] || [];
    if (rr.some(function (c) { return cell_(c).indexOf('คะแนนเต็ม') !== -1; })) { maxRow = rr; break; }
  }
  questions.forEach(function (q) {
    q.items.forEach(function (it) { it.max = maxRow ? toNum_(maxRow[it.col]) : null; });
    var tm = maxRow && q.totalCol >= 0 ? toNum_(maxRow[q.totalCol]) : null;
    var itemSum = sum_(onlyNums_(q.items.map(function (it) { return it.max; })));
    q.max = tm != null ? tm : (itemSum || CONFIG.WRITTEN_MAX_DEFAULT);
  });

  var rows = {};
  for (var s = h + 1; s < values.length; s++) {
    var rw = values[s] || [];
    if (colSeq < 0 || !isSeq_(rw[colSeq]) || !cell_(rw[colName])) continue;
    rows[toNum_(rw[colSeq])] = {
      name: cell_(rw[colName]),
      q: questions.map(function (q) {
        var items = q.items.map(function (it) { return toNum_(rw[it.col]); });
        var total = q.totalCol >= 0 ? toNum_(rw[q.totalCol]) : null;
        if (total == null && items.length && items.every(function (x) { return x != null; })) total = sum_(items);
        return { items: items, total: total };
      })
    };
  }
  return {
    questions: questions.map(function (q) {
      return { no: q.no, max: q.max, items: q.items.map(function (it) { return { label: it.label, max: it.max }; }) };
    }),
    rows: rows
  };
}

/* ---------- แท็บ ข้อควรพิจารณา (ความเห็นรายข้อ) ---------- */

function parseFeedback_(values) {
  var h = findHeaderRow_(values, function (row) {
    return row.indexOf('ชื่อ-สกุล') !== -1 && row.indexOf('ความเห็น') !== -1;
  });
  if (h < 0) throw new Error('แท็บ "' + CONFIG.TAB_FEEDBACK + '": ไม่พบหัวตาราง (ชื่อ-สกุล, ข้อ, ความเห็น)');
  var head = values[h].map(cell_);
  var cSeq = head.indexOf('ลำดับ'), cScope = head.indexOf('ข้อ'), cText = head.indexOf('ความเห็น');
  var bySeq = {};
  for (var r = h + 1; r < values.length; r++) {
    var row = values[r] || [];
    if (cSeq < 0 || !isSeq_(row[cSeq])) continue;
    var scope = cell_(row[cScope]);
    var text = cleanText_(row[cText]);
    // เฉพาะความเห็นรายข้อ; ข้ามบันทึกภายใน ("ข้อควรพิจารณา") และข้อความที่พูดถึงผู้สอน/นักศึกษาคนอื่น
    var isItem = scope.indexOf('อัตนัย') === 0 || scope.indexOf('ปรนัยข้อ') === 0;
    if (!isItem || !text || INTERNAL_COMMENT_RE_.test(text)) continue;
    var seq = toNum_(row[cSeq]);
    (bySeq[seq] = bySeq[seq] || []).push({ scope: scope, text: text });
  }
  return bySeq;
}

/* ---------- รวมทุกแท็บเป็นข้อมูลห้อง ---------- */

function buildClassData_(summary, mcq, written, feedback) {
  var warnings = [];
  var seen = {};

  function lookup(rows, s, label) {
    if (!rows) return null;
    var r = rows[s.seq];
    if (r && normalizeName_(r.name) === normalizeName_(s.name)) return r;
    var hit = null;
    Object.keys(rows).forEach(function (k) {
      if (!hit && normalizeName_(rows[k].name) === normalizeName_(s.name)) hit = rows[k];
    });
    if (!hit) warnings.push('ไม่พบ "' + s.name + '" ในแท็บ' + label);
    else if (r) warnings.push('ลำดับของ "' + s.name + '" ในแท็บ' + label + ' ไม่ตรงกับแท็บสรุปคะแนน (จับคู่ด้วยชื่อ)');
    return hit;
  }

  var students = [];
  summary.students.forEach(function (s) {
    if (seen[s.idKey]) { warnings.push('รหัสนักศึกษาซ้ำ: ' + s.id + ' (ใช้แถวแรก)'); return; }
    seen[s.idKey] = true;
    var m = lookup(mcq && mcq.rows, s, CONFIG.TAB_MCQ);
    var w = lookup(written && written.rows, s, CONFIG.TAB_WRITTEN);
    var fb = (feedback && feedback[s.seq]) || [];
    students.push({
      seq: s.seq, id: s.id, idKey: s.idKey, name: s.name, group: s.group, pdfName: s.pdfName,
      mcq: s.mcq, w: s.w, wTotal: s.wTotal, totals: s.totals,
      answers: m ? m.answers : null,
      wd: w ? w.q : null,
      feedback: fb
    });
  });
  return {
    builtAt: new Date().toISOString(),
    students: students,
    max: summary.max,
    mcq: mcq ? { items: mcq.items, key: mcq.key } : null,
    written: written ? { questions: written.questions } : null,
    warnings: warnings
  };
}

/* ---------- สร้างข้อมูลหน้า Dashboard ของนักศึกษา 1 คน ---------- */

var TOTAL_LABELS_ = {
  official: { label: 'คะแนนรวม', note: '' },
  mcq_floor0: { label: 'คะแนนรวม', note: 'คำนวณโดยให้คะแนนปรนัยต่ำสุดเป็น 0' },
  no_partial_q2: { label: 'คะแนนรวม', note: 'คำนวณโดยข้อ 2 ไม่ให้คะแนนบางส่วน' }
};

function totalFor_(s, mode) {
  var t = s.totals[mode];
  return t == null ? s.totals.official : t;
}

function findStudent_(D, idKey) {
  for (var i = 0; i < D.students.length; i++) if (D.students[i].idKey === idKey) return i;
  return -1;
}

function statBlock_(values) {
  var v = onlyNums_(values);
  return {
    n: v.length,
    mean: round_(mean_(v), 2),
    median: round_(median_(v), 2),
    sd: round_(sd_(v), 2),
    max: v.length ? Math.max.apply(null, v) : null,
    min: v.length ? Math.min.apply(null, v) : null
  };
}

function buildDashboard_(D, idKey, settings) {
  var idx = findStudent_(D, idKey);
  if (idx < 0) return null;
  var me = D.students[idx];
  var mode = TOTAL_LABELS_[settings.total_mode] ? settings.total_mode : 'official';

  var totals = D.students.map(function (s) { return totalFor_(s, mode); });
  var ranks = competitionRanks_(totals);
  var myTotal = totals[idx];
  var tstat = statBlock_(totals);
  var ties = 0;
  totals.forEach(function (t, i) { if (i !== idx && t != null && t === myTotal) ties++; });

  var hist = buildHistogram_(totals, 10);
  var floor0 = mode === 'mcq_floor0';
  function mcqUsed(s) { return s.mcq.used == null ? null : (floor0 ? Math.max(0, s.mcq.used) : s.mcq.used); }

  function comp(key, label, max, getter) {
    var vals = D.students.map(getter);
    var st = statBlock_(vals);
    return { key: key, label: label, score: getter(me), max: max, mean: st.mean, best: st.max, low: st.min };
  }
  var components = [
    comp('mcq', 'ปรนัย', D.max.mcq, mcqUsed),
    comp('q1', 'อัตนัยข้อ 1', D.max.w[0], function (s) { return s.w[0]; }),
    comp('q2', 'อัตนัยข้อ 2', D.max.w[1], function (s) { return s.w[1]; }),
    comp('q3', 'อัตนัยข้อ 3', D.max.w[2], function (s) { return s.w[2]; })
  ];
  var writtenComp = comp('written', 'อัตนัยรวม', D.max.written, function (s) { return s.wTotal; });

  // ปรนัยรายข้อ
  var mcqBlock = null;
  if (D.mcq && me.answers) {
    var items = D.mcq.items.map(function (no, k) {
      var ans = me.answers[k], key = D.mcq.key[no] || null;
      var result = ans == null ? 'blank' : (ans === key ? 'correct' : 'wrong');
      var answered = 0, right = 0;
      D.students.forEach(function (s) {
        if (!s.answers) return;
        answered++;
        if (key && s.answers[k] === key) right++;
      });
      return {
        no: no, key: key, answer: ans, result: result,
        points: CONFIG.MCQ_POINTS[result],
        classCorrectPct: answered ? Math.round((right / answered) * 100) : null
      };
    });
    mcqBlock = {
      items: items,
      correct: me.mcq.correct, wrong: me.mcq.wrong, blank: me.mcq.blank,
      formula: me.mcq.formula, used: mcqUsed(me), cap: D.max.mcq,
      points: CONFIG.MCQ_POINTS
    };
  }

  // อัตนัยรายหัวข้อ
  var writtenBlock = null;
  if (D.written && me.wd) {
    writtenBlock = D.written.questions.map(function (q, qi) {
      var mine = me.wd[qi];
      var qTotals = D.students.map(function (s) { return s.wd ? s.wd[qi].total : null; });
      return {
        no: q.no, label: 'อัตนัยข้อ ' + q.no, max: q.max,
        score: mine.total, classMean: round_(mean_(onlyNums_(qTotals)), 2),
        items: q.items.map(function (it, k) {
          var col = D.students.map(function (s) { return s.wd ? s.wd[qi].items[k] : null; });
          return { label: it.label, max: it.max, score: mine.items[k], classMean: round_(mean_(onlyNums_(col)), 2) };
        })
      };
    });
  }

  var leaderboard = null;
  if (settings.show_leaderboard) {
    leaderboard = [];
    totals.forEach(function (t, i) {
      if (t != null) leaderboard.push({ rank: ranks[i], score: t, you: i === idx });
    });
    leaderboard.sort(function (a, b) { return a.rank - b.rank || (a.you ? -1 : 0); });
    leaderboard = leaderboard.slice(0, 100);
  }

  return {
    student: { id: me.id, name: me.name, seq: me.seq, group: me.group },
    total: {
      label: TOTAL_LABELS_[mode].label, note: TOTAL_LABELS_[mode].note, mode: mode,
      score: myTotal, max: D.max.total,
      rank: ranks[idx], of: tstat.n, ties: ties,
      percentAbove: myTotal == null ? null : percentAbove_(myTotal, totals),
      mean: tstat.mean, median: tstat.median, sd: tstat.sd, best: tstat.max, low: tstat.min
    },
    components: components,
    written: writtenComp,
    distribution: settings.show_leaderboard ? { width: hist.width, bins: hist.bins, you: binIndexFor_(hist, myTotal) } : null,
    leaderboard: leaderboard,
    mcq: mcqBlock,
    writtenDetail: writtenBlock,
    feedback: settings.show_feedback ? me.feedback : null,
    hasPdf: !!settings.show_pdf && !!me.pdfName,
    builtAt: D.builtAt
  };
}

/* ---------- จับคู่ไฟล์ PDF กับนักศึกษา ---------- */

/** map: { ชื่อไฟล์แบบ normalize -> fileId } ; คืน fileId หรือ null */
function resolvePdfId_(student, map) {
  if (student.pdfName) {
    var hit = map[normalizeFileName_(student.pdfName)];
    if (hit) return hit;
  }
  // สำรอง: ตรวจแล้ว_<ลำดับ 2 หลัก>_<ชื่อ>.pdf
  var pad = (student.seq < 10 ? '0' : '') + student.seq;
  var prefix = normalizeFileName_('ตรวจแล้ว_' + pad + '_');
  var nameKey = normalizeName_(student.name);
  var found = null, count = 0;
  Object.keys(map).forEach(function (k) {
    if (k.indexOf(prefix) === 0 && normalizeName_(k.slice(prefix.length).replace(/\.pdf$/, '')) === nameKey) {
      found = map[k]; count++;
    }
  });
  return count === 1 ? found : null;
}
