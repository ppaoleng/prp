'use strict';
/**
 * ตรวจหน้าผู้ดูแลด้วย Chromium: ล็อกอิน -> ตาราง -> ค้นหา/เรียง -> เปิดดูนักศึกษา -> PDF -> CSV -> ออกจากระบบ
 *   node dev/build-preview.js <outDir> admin   (ต้องมี <outDir>/sample.pdf ถ้าอยากเห็น PDF)
 *   PDFJS_DIR=<pdfjs-dist/build> node dev/shoot-admin.js <outDir>
 */
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const out = path.resolve(process.argv[2] || path.join(__dirname, 'out'));
const PDFJS_DIR = process.env.PDFJS_DIR;
const url = 'file://' + path.join(out, 'index.html');

async function open(browser, viewport, scheme) {
  const ctx = await browser.newContext({ viewport, colorScheme: scheme, acceptDownloads: true, deviceScaleFactor: viewport.width < 600 ? 2 : 1 });
  if (PDFJS_DIR) {
    await ctx.route('https://cdnjs.cloudflare.com/ajax/libs/pdf.js/**', (route) => {
      const f = path.join(PDFJS_DIR, path.basename(new URL(route.request().url()).pathname));
      fs.existsSync(f) ? route.fulfill({ status: 200, contentType: 'text/javascript', headers: { 'access-control-allow-origin': '*' }, body: fs.readFileSync(f) }) : route.abort();
    });
  }
  const page = await ctx.newPage();
  const errors = [];
  page.on('console', (m) => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
  await page.addInitScript((t) => { try { localStorage.setItem('sp_theme', t); } catch (e) { /* ignore */ } }, scheme);
  return { page, ctx, errors };
}

(async () => {
  const browser = await chromium.launch();
  const report = {};

  // ---------- เดสก์ท็อปธีมมืด: ทั้งโฟลว์ ----------
  {
    const { page, ctx, errors } = await open(browser, { width: 1280, height: 900 }, 'dark');
    await page.goto(url);
    await page.waitForSelector('#admForm');
    report.authTitle = await page.locator('main h2').innerText();
    await page.screenshot({ path: path.join(out, 'admin-1-login.png') });

    await page.fill('#f_apw', '9999');
    await page.click('#submitBtn');
    await page.waitForSelector('#msg .alert-err');
    report.wrongPw = await page.locator('#msg').innerText();

    await page.fill('#f_apw', '1111');
    await page.click('#submitBtn');
    await page.waitForSelector('#admBody tr[data-id]');
    await page.waitForSelector('#hist svg');
    await page.waitForTimeout(1500);
    report.rows = await page.locator('#admBody tr[data-id]').count();
    report.registeredFig = await page.locator('.bigfig').innerText();
    await page.screenshot({ path: path.join(out, 'admin-2-overview.png'), fullPage: true });

    // ค้นหา
    await page.fill('#admQ', 'ตัวอย่าง');
    report.searchName = await page.locator('#admBody tr[data-id]').count();
    await page.fill('#admQ', '999999-0005');
    report.searchId = await page.locator('#admBody tr[data-id]').count();
    await page.fill('#admQ', 'ไม่มีคนนี้');
    report.searchNone = await page.locator('#admBody td.empty').count();
    await page.fill('#admQ', '');

    // เรียงตามคะแนนรวม (คลิก 2 ครั้ง = มาก -> น้อย)
    await page.click('th[data-sort="total"]');
    await page.click('th[data-sort="total"]');
    report.sortedTotals = await page.locator('#admBody tr td:nth-child(9)').allInnerTexts();

    // CSV
    const [dl] = await Promise.all([page.waitForEvent('download'), page.click('#admCsv')]);
    const csv = fs.readFileSync(await dl.path(), 'utf8');
    report.csv = { name: dl.suggestedFilename(), bom: csv.charCodeAt(0) === 0xfeff, lines: csv.split('\r\n').length, head: csv.split('\r\n')[0], first: csv.split('\r\n')[1] };

    // เปิดดูนักศึกษา (ลำดับ 4 ซึ่งปรนัยติดลบ) ด้วยการพิมพ์รหัสแล้วกด Enter
    await page.fill('#admQ', '999999-0004');
    await page.press('#admQ', 'Enter');
    await page.waitForSelector('.adminbar');
    await page.waitForSelector('#hist svg');
    await page.evaluate(() => document.getElementById('pdfCard').scrollIntoView()); // PDF โหลดแบบ lazy เมื่อเลื่อนใกล้การ์ด
    await page.waitForSelector('.pg canvas', { timeout: 15000 }).catch(() => errors.push('pdf: ไม่มี canvas'));
    await page.waitForTimeout(1500);
    report.adminBar = await page.locator('.adminbar').innerText();
    report.studentName = await page.locator('.score-meta .name').innerText();
    report.legend = await page.locator('.legend').first().innerText();
    report.pdfCanvases = await page.locator('.pg canvas').count();
    report.hasYouWording = await page.evaluate(() => /คุณ/.test(document.querySelector('main').innerText));
    await page.screenshot({ path: path.join(out, 'admin-3-student.png'), fullPage: true });

    // กลับรายชื่อ — ค่าค้นหา/เรียงต้องคงอยู่
    await page.click('#backBtn');
    await page.waitForSelector('#admBody tr[data-id]');
    report.afterBackQuery = await page.inputValue('#admQ');
    report.afterBackRows = await page.locator('#admBody tr[data-id]').count();

    // ออกจากระบบ
    await page.click('#logoutBtn');
    await page.waitForSelector('#admForm');
    report.afterLogout = await page.locator('#msg').innerText();
    report.errorsDesktop = errors;
    await ctx.close();
  }

  // ---------- มือถือ/ธีมสว่าง ----------
  for (const cfg of [{ n: 'mobile-light', vp: { width: 390, height: 844 }, th: 'light' }, { n: 'desktop-light', vp: { width: 1280, height: 900 }, th: 'light' }]) {
    const { page, ctx, errors } = await open(browser, cfg.vp, cfg.th);
    await page.goto(url);
    await page.fill('#f_apw', '1111'); await page.click('#submitBtn');
    await page.waitForSelector('#admBody tr[data-id]'); await page.waitForSelector('#hist svg');
    await page.waitForTimeout(1500);
    await page.screenshot({ path: path.join(out, 'admin-' + cfg.n + '-overview.png'), fullPage: cfg.vp.width > 600 });
    const info = await page.evaluate(() => ({ overflowX: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1, scrollW: document.documentElement.scrollWidth, clientW: document.documentElement.clientWidth }));
    report[cfg.n] = { info, errors };
    await ctx.close();
  }

  await browser.close();
  console.log(JSON.stringify(report, null, 2));
})().catch((e) => { console.error(e); process.exit(1); });
