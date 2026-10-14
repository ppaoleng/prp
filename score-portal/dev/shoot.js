'use strict';
/**
 * ตรวจหน้าเว็บด้วย Chromium (Playwright): ล็อกอิน -> แดชบอร์ด -> PDF -> เก็บภาพหน้าจอ + ตรวจ console error
 *   PDFJS_DIR=<โฟลเดอร์ pdfjs-dist/build> node dev/shoot.js <outDir>
 * cdnjs ถูกบล็อกในบางสภาพแวดล้อม จึงตอบด้วยไฟล์ pdf.js เวอร์ชันเดียวกันจากเครื่อง
 */
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const out = path.resolve(process.argv[2] || path.join(__dirname, 'out'));
const PDFJS_DIR = process.env.PDFJS_DIR;
const meta = () => JSON.parse(fs.readFileSync(path.join(out, 'meta.json'), 'utf8'));

async function makeSamplePdf(browser) {
  const page = await browser.newPage();
  const sheet = (n) => `<section style="page-break-after:always;height:1040px;padding:44px;font-family:'Noto Sans Thai',sans-serif;position:relative">
    <h2 style="margin:0 0 6px">ข้อสอบปลายภาค (ตัวอย่างสมมติ) — หน้า ${n}</h2>
    <p style="color:#555;margin:0 0 24px">เอกสารตัวอย่างสำหรับทดสอบตัวแสดง PDF ไม่ใช่ข้อมูลจริง</p>
    ${[1, 2, 3, 4, 5].map((i) => `<div style="margin:18px 0"><b>ข้อ ${i}.</b> จงคำนวณหาแรงปฏิกิริยาที่จุดรองรับ A, B, C ของคานต่อเนื่อง
      <div style="margin:10px 0 0 24px;font:italic 20px 'Comic Sans MS',cursive;color:#1b3fa8">Ay = ${20 * i + n} kN ,&nbsp; By = ${15 * i} kN ,&nbsp; Mc = ${100 + i * n} kN·m</div></div>`).join('')}
    <div style="position:absolute;right:50px;top:40px;border:3px solid #c0261f;color:#c0261f;border-radius:50%;width:78px;height:78px;display:grid;place-items:center;font:700 26px sans-serif;transform:rotate(-12deg)">${14 - n}/20</div>
  </section>`;
  await page.setContent(`<body style="margin:0">${sheet(1)}${sheet(2)}${sheet(3)}</body>`);
  await page.pdf({ path: path.join(out, 'sample.pdf'), format: 'A4', printBackground: true });
  await page.close();
}

async function newPage(browser, viewport, scheme) {
  const ctx = await browser.newContext({ viewport, colorScheme: scheme || 'dark', deviceScaleFactor: viewport.width < 600 ? 2 : 1 });
  if (PDFJS_DIR) {
    await ctx.route('https://cdnjs.cloudflare.com/ajax/libs/pdf.js/**', (route) => {
      const f = path.join(PDFJS_DIR, path.basename(new URL(route.request().url()).pathname));
      if (fs.existsSync(f)) route.fulfill({ status: 200, contentType: 'text/javascript', headers: { 'access-control-allow-origin': '*' }, body: fs.readFileSync(f) });
      else route.abort();
    });
  }
  const page = await ctx.newPage();
  const errors = [];
  page.on('console', (m) => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
  return { page, errors, ctx };
}

(async () => {
  const browser = await chromium.launch();
  await makeSamplePdf(browser);
  require('child_process').execFileSync('node', [path.join(__dirname, 'build-preview.js'), out, process.argv[3] || 'published'], { stdio: 'inherit' });
  const url = 'file://' + path.join(out, 'index.html');
  const { id, password } = meta();
  const report = [];

  if ((process.argv[3] || 'published') === 'locked') {
    const { page, errors, ctx } = await newPage(browser, { width: 1280, height: 800 }, 'dark');
    await page.goto(url);
    await page.fill('#f_id', id); await page.fill('#f_pw', password); await page.click('#submitBtn');
    await page.waitForSelector('.locked');
    await page.waitForTimeout(700);
    await page.screenshot({ path: path.join(out, 'locked.png') });
    const body = await page.evaluate(() => document.body.innerText);
    report.push({ name: 'locked', errors, info: { hasScore: /คะแนนรวม|อันดับ/.test(body), text: body.slice(0, 300) } });
    await browser.close();
    console.log(JSON.stringify(report, null, 2));
    return;
  }

  {
    const { page, errors, ctx } = await newPage(browser, { width: 1280, height: 800 }, 'dark');
    await page.goto(url);
    await page.waitForSelector('#authForm');
    await page.click('[data-tab="register"]');
    await page.fill('#f_pw', 'abc12345');
    await page.waitForTimeout(500);
    await page.screenshot({ path: path.join(out, 'register.png') });
    report.push({ name: 'register', errors, info: { strength: await page.getAttribute('#strength', 'data-s') } });
    await ctx.close();
  }

  for (const cfg of [
    { name: 'desktop-dark', vp: { width: 1280, height: 900 }, theme: 'dark' },
    { name: 'desktop-light', vp: { width: 1280, height: 900 }, theme: 'light' },
    { name: 'mobile-dark', vp: { width: 390, height: 844 }, theme: 'dark' },
    { name: 'mobile-light', vp: { width: 390, height: 844 }, theme: 'light' }
  ]) {
    const { page, errors, ctx } = await newPage(browser, cfg.vp, cfg.theme);
    await page.addInitScript((t) => { try { localStorage.setItem('sp_theme', t); } catch (e) { /* ignore */ } }, cfg.theme);
    await page.goto(url);
    await page.waitForSelector('#authForm');
    await page.waitForTimeout(900);
    await page.screenshot({ path: path.join(out, cfg.name + '-1-login.png') });

    // ล็อกอินจริงผ่านฟอร์ม
    await page.fill('#f_id', id);
    await page.fill('#f_pw', password);
    await page.click('#submitBtn');
    await page.waitForSelector('.hero', { timeout: 8000 });
    await page.waitForSelector('#hist svg', { timeout: 8000 });
    await page.waitForTimeout(1600);
    await page.evaluate(() => document.getElementById('pdfCard') && document.getElementById('pdfCard').scrollIntoView());
    await page.waitForSelector('.pg canvas', { timeout: 15000 }).catch(() => errors.push('pdf: ไม่มี canvas ภายใน 15 วินาที'));
    await page.waitForTimeout(800);
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(out, cfg.name + '-2-dashboard.png'), fullPage: true });
    if (cfg.vp.width < 600) {
      const H = await page.evaluate(() => document.documentElement.scrollHeight);
      await page.screenshot({ path: path.join(out, cfg.name + '-3-top.png'), fullPage: true, clip: { x: 0, y: 0, width: 390, height: 1500 } });
      await page.screenshot({ path: path.join(out, cfg.name + '-4-mid.png'), fullPage: true, clip: { x: 0, y: 1500, width: 390, height: 1700 } });
      await page.screenshot({ path: path.join(out, cfg.name + '-5-bottom.png'), fullPage: true, clip: { x: 0, y: 3200, width: 390, height: Math.min(1700, H - 3200) } });
    }

    const info = await page.evaluate(() => ({
      overflowX: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
      scrollW: document.documentElement.scrollWidth, clientW: document.documentElement.clientWidth,
      chips: document.querySelectorAll('.q').length,
      canvases: document.querySelectorAll('.pg canvas').length,
      heroScore: (document.querySelector('.hero-figure') || {}).textContent,
      rank: (document.querySelector('.rank-fig b') || {}).textContent
    }));
    report.push({ name: cfg.name, errors, info });
    await ctx.close();
  }

  // ทดสอบ interaction บน desktop-dark
  {
    const { page, errors, ctx } = await newPage(browser, { width: 1280, height: 900 }, 'dark');
    await page.goto(url);
    await page.fill('#f_id', id); await page.fill('#f_pw', password); await page.click('#submitBtn');
    await page.waitForSelector('#hist svg');
    await page.waitForTimeout(1500);
    const bar = page.locator('#hist g.b').nth(3);
    await bar.hover();
    await page.waitForTimeout(250);
    const tipTxt = await page.locator('#tip').innerText();
    await page.locator('#hist').scrollIntoViewIfNeeded();
    await page.screenshot({ path: path.join(out, 'interact-hist-tip.png') });
    await page.locator('.q').nth(11).hover();
    await page.waitForTimeout(250);
    const tip2 = await page.locator('#tip').innerText();
    await page.locator('#mcqChips').scrollIntoViewIfNeeded();
    await page.screenshot({ path: path.join(out, 'interact-mcq-tip.png') });
    await page.click('#histTbl');
    const tblRows = await page.locator('#histTable tbody tr').count();
    await page.click('#mcqTbl');
    const mcqRows = await page.locator('#mcqTable tbody tr').count();
    await page.waitForSelector('.pg canvas', { timeout: 15000 });
    const w0 = await page.locator('.pg').first().evaluate((e) => e.clientWidth);
    await page.click('#zIn');
    await page.waitForTimeout(600);
    const w1 = await page.locator('.pg').first().evaluate((e) => e.clientWidth);
    const zoomTxt = await page.locator('#zVal').innerText();
    // ออกจากระบบ
    await page.click('#logoutBtn');
    await page.waitForSelector('#authForm');
    const afterLogout = await page.locator('#msg').innerText();
    // รหัสผิด
    await page.fill('#f_id', id); await page.fill('#f_pw', 'wrong-pass-9'); await page.click('#submitBtn');
    await page.waitForSelector('#msg .alert-err');
    const wrongMsg = await page.locator('#msg').innerText();
    await page.screenshot({ path: path.join(out, 'interact-wrong-login.png') });
    report.push({ name: 'interact', errors, info: { tipTxt, tip2, tblRows, mcqRows, w0, w1, zoomTxt, afterLogout, wrongMsg } });
    await ctx.close();
  }

  await browser.close();
  console.log(JSON.stringify(report, null, 2));
})().catch((e) => { console.error(e); process.exit(1); });
