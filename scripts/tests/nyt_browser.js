// Browsertest af "Nye tilbud siden sidst" (index.html) i Chromium (node-Playwright) mod en LOKAL kopi af repoet.
// Kør:  node scripts/tests/nyt_browser.js [rodmappe]
// Afslutter med 0 (bestået), 1 (fejl) eller 3 (Playwright/Chromium findes ikke her: testen er IKKE kørt).
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
const fejl = [], jsFejl = [];
const t = (ok, tekst) => { if (!ok) fejl.push(tekst); };
(async () => {
  await new Promise(r => srv.listen(0, '127.0.0.1', r));
  const U = `http://127.0.0.1:${srv.address().port}/`;
  const d = JSON.parse(fs.readFileSync(path.join(ROD, 'retter.json'), 'utf8'));
  const n = {}; for (const [k, b] of Object.entries(d.butikker)) n[k] = b.retter.map(r => r.navn).slice(5);  // baseline uden de første 5 retter pr. butik
  const base = JSON.stringify({ g: '2000-01-01T00:00:00+00:00', n });
  let b;
  try {
    for (const o of [{}, ...(process.env.PW_CHROMIUM ? [{ executablePath: process.env.PW_CHROMIUM }] : []), { executablePath: '/opt/pw-browsers/chromium' }]) { try { b = await chromium.launch(o); break; } catch (e) { /* næste */ } }
    if (!b) { console.error('IKKE KØRT: Chromium kunne ikke startes'); process.exitCode = 3; return; }
    const ny = async init => {
      const c = await b.newContext({ viewport: { width: 390, height: 844 }, serviceWorkers: 'block' });
      const p = await c.newPage();
      p.on('pageerror', e => jsFejl.push(String(e).slice(0, 200)));
      await p.route('**/*', r => r.request().url().startsWith(U) ? r.continue() : r.abort());
      if (init) await p.addInitScript(init, base);
      return p;
    };
    const klar = p => p.waitForFunction("typeof data!=='undefined'&&data&&data.butikker&&typeof render==='function'", null, { timeout: 60000 });
    const vaelg = async (p, liste) => { await p.evaluate(l => { const k = l || [Object.keys(data.butikker)[0]]; state.butikker = k; state.butik = k[0] || null; state.butikValgt = true; render(); }, liste); await p.waitForTimeout(300); };
    const skjult = p => p.$eval('#nyt-siden-sidst', e => e.hidden);
    const sat = x => { if (!sessionStorage.getItem('sat')) { localStorage.setItem('mj-set', x); sessionStorage.setItem('sat', '1'); } };
    // (1) første besøg: ingen linje, baseline gemmes
    let p = await ny(); await p.goto(U); await klar(p);
    t(await skjult(p), 'første besøg viser linjen');
    t(await p.evaluate(() => !!localStorage.getItem('mj-set')), 'første besøg gemmer ikke baseline');
    // (2) gammel baseline + valgt butik: linje med tal, ≤ 90 px, ingen vandret scroll
    p = await ny(sat); await p.goto(U); await klar(p); await vaelg(p);
    t(!(await skjult(p)), 'linjen vises ikke ved nye retter');
    const tekst = await p.innerText('#nyt-siden-sidst');
    t(/^5 nye retter hos .+ siden sidst\./m.test(tekst), 'forkert tekst/tal: ' + tekst);
    const m = await p.evaluate(() => ({ h: document.getElementById('nyt-siden-sidst').getBoundingClientRect().height, vs: document.documentElement.scrollWidth > innerWidth, knap: [...document.querySelectorAll('#nyt-siden-sidst button')].map(k => [k.offsetWidth, k.offsetHeight]) }));
    t(m.h <= 90, 'linjen er over 90 px høj: ' + m.h); t(!m.vs, 'vandret scroll'); t(m.knap.every(([w, h]) => w >= 44 && h >= 44), 'knapper under 44 px: ' + JSON.stringify(m.knap));
    // (2b) udskrift: linjen er skjult på indkøbssedlen, men synlig på skærmen
    t(await p.$eval('#nyt-siden-sidst', e => getComputedStyle(e).display) !== 'none', 'linjen er skjult på skærmen');
    await p.emulateMedia({ media: 'print' });
    t(await p.$eval('#nyt-siden-sidst', e => getComputedStyle(e).display) === 'none', 'linjen kommer med på udskriften');
    await p.emulateMedia({ media: 'screen' });
    // (3) mindre end 3 nye: ingen linje
    await p.evaluate(() => { const g = JSON.parse(localStorage.getItem('mj-set')); const k = state.butikker[0]; g.n[k] = data.butikker[k].retter.map(r => r.navn).slice(2); localStorage.setItem('mj-set', JSON.stringify(g)); render(); });
    t(await skjult(p), 'linjen vises ved kun 2 nye retter');
    await p.evaluate(() => { const g = JSON.parse(localStorage.getItem('mj-set')); const k = state.butikker[0]; g.n[k] = data.butikker[k].retter.map(r => r.navn).slice(5); localStorage.setItem('mj-set', JSON.stringify(g)); render(); });
    // (4) ingen valgt butik: ingen linje
    await vaelg(p, []); t(await skjult(p), 'linjen vises uden valgt butik'); await vaelg(p);
    // (5) genindlæsning før luk: linjen består; luk: væk, også efter genindlæsning
    await p.reload(); await klar(p); await vaelg(p); t(!(await skjult(p)), 'linjen forsvandt ved genindlæsning før luk');
    await p.click('[data-nyt-luk]'); t(await skjult(p), 'linjen kan ikke lukkes');
    await p.reload(); await klar(p); await vaelg(p); t(await skjult(p), 'linjen kom igen efter luk');
    // (6) blokeret localStorage: ingen linje, ingen fejl
    const c3 = await b.newContext({ viewport: { width: 390, height: 844 }, serviceWorkers: 'block' }); p = await c3.newPage();
    p.on('pageerror', e => jsFejl.push('blokeret: ' + String(e).slice(0, 200)));
    await p.route('**/*', r => r.request().url().startsWith(U) ? r.continue() : r.abort());
    await p.addInitScript(() => { Object.defineProperty(window, 'localStorage', { get() { throw new Error('blocked'); } }); });
    await p.goto(U); await klar(p); t(await skjult(p), 'linjen vises, selvom localStorage er blokeret');
  } finally { if (b) await b.close(); srv.close(); }
  if (process.exitCode === 3) return;
  if (jsFejl.length) fejl.push('JS-fejl: ' + jsFejl.slice(0, 3).join(' | '));
  if (fejl.length) { console.log(fejl.join('\n')); process.exitCode = 1; } else console.log('nyt siden sidst: bestået');
})().catch(e => { console.error(e); process.exitCode = 1; srv.close(); });
