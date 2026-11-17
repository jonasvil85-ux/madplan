// Reserve for sammenlign_browser.py: kører samme browsertest med node-Playwright (når Python ikke har Playwright).
// Kør:  node scripts/tests/sammenlign_browser_node.js <rodmappe>
// Skriver ét JSON-objekt {ud, jsFejl} til stdout. Afslutter med 3, hvis Playwright/Chromium ikke findes.
const http = require('http'), fs = require('fs'), path = require('path');
const ROD = path.resolve(process.argv[2] || path.join(__dirname, '..', '..'));
let chromium;
try { ({ chromium } = require('playwright')); } catch (e) { console.error('IKKE KØRT: Playwright findes ikke i node'); process.exit(3); }
const TYPER = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json', '.css': 'text/css', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml' };
const srv = http.createServer((q, s) => {
  let p = decodeURIComponent(q.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html';
  const f = path.join(ROD, p);
  if (!f.startsWith(ROD) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { s.writeHead(404); return s.end(); }
  s.writeHead(200, { 'Content-Type': TYPER[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(s);
});
(async () => {
  await new Promise(r => srv.listen(0, '127.0.0.1', r));
  const url = `http://127.0.0.1:${srv.address().port}/`;
  const test = fs.readFileSync(path.join(ROD, 'scripts', 'tests', 'sammenlign_side.js'), 'utf8');
  const jsFejl = []; let b;
  try {
    const kandidater = [{}, ...(process.env.PW_CHROMIUM ? [{ executablePath: process.env.PW_CHROMIUM }] : []), { executablePath: '/opt/pw-browsers/chromium' }];
    let fejl0;
    for (const o of kandidater) { try { b = await chromium.launch(o); break; } catch (e) { fejl0 = fejl0 || e; } }
    if (!b) { console.error('IKKE KØRT: Chromium kunne ikke startes: ' + String(fejl0.message).split('\n')[0]); process.exitCode = 3; return; }
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
    const side = await ctx.newPage();
    side.on('pageerror', e => jsFejl.push(String(e).slice(0, 200)));
    await side.route('**/*', r => r.request().url().startsWith(url) ? r.continue() : r.abort());
    await side.goto(url);
    await side.waitForFunction("typeof data !== 'undefined' && data && data.butikker && typeof SAMM !== 'undefined'", null, { timeout: 60000 });
    await side.evaluate("() => { localStorage.clear(); document.querySelector('[data-intro-luk]')?.click(); }");
    const ud = await side.evaluate(test);
    process.stdout.write(JSON.stringify({ ud, jsFejl }));
  } finally { if (b) await b.close(); srv.close(); }
})().catch(e => { console.error('IKKE KØRT: ' + e.message.split('\n')[0]); process.exit(3); });
