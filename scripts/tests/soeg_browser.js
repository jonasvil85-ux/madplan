// Browsertest af "Søg i Vælg selv" (trin Retter) i Chromium (node-Playwright) mod en LOKAL kopi af repoet.
// Kør:  node scripts/tests/soeg_browser.js [rodmappe]
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
  const url = `http://127.0.0.1:${srv.address().port}/`;
  let b;
  try {
    for (const o of [{}, ...(process.env.PW_CHROMIUM ? [{ executablePath: process.env.PW_CHROMIUM }] : []), { executablePath: '/opt/pw-browsers/chromium' }]) { try { b = await chromium.launch(o); break; } catch (e) { /* næste */ } }
    if (!b) { console.error('IKKE KØRT: Chromium kunne ikke startes'); process.exitCode = 3; return; }
    for (const bredde of [390, 360]) {
      const ctx = await b.newContext({ viewport: { width: bredde, height: 844 }, hasTouch: true, isMobile: true });
      const side = await ctx.newPage();
      side.on('pageerror', e => jsFejl.push(String(e).slice(0, 200)));
      await side.route('**/*', r => r.request().url().startsWith(url) ? r.continue() : r.abort());
      await side.goto(url);
      await side.waitForFunction("typeof data !== 'undefined' && data && data.butikker && typeof renderRetter === 'function'", null, { timeout: 60000 });
      await side.evaluate(() => { localStorage.clear(); document.querySelector('[data-intro-luk]')?.click(); });
      await side.evaluate(() => { const k = Object.keys(data.butikker)[0]; state.butikker = [k]; state.butik = k; state.butikValgt = true; state.trin = 'retter'; render(); });
      await side.waitForSelector('#ret-soeg', { timeout: 10000 });
      const m = `${bredde} px: `;
      const felt = await side.evaluate(() => { const r = document.getElementById('ret-soeg').getBoundingClientRect(); return { top: r.top, bund: r.bottom, h: r.height, fs: parseFloat(getComputedStyle(document.getElementById('ret-soeg')).fontSize) }; });
      t(felt.bund < 844 && felt.h >= 44, m + 'søgefeltet er ikke synligt øverst/mindst 44 px: ' + JSON.stringify(felt));
      t(felt.fs >= 16, m + 'skriftstørrelse under 16 px');
      const alle = await side.evaluate(() => document.querySelectorAll('#ret-indhold .grid .ret').length);
      t(alle > 20, m + 'for få retkort uden søgning: ' + alle);
      // match direkte mod sidens egen funktion: forventede par
      const par = await side.evaluate(() => {
        const R = pool(aktivS()), n = s => { const x = soegRetter(R, s); return x ? x.size : -1; };
        const ord = s => R.filter(r => soegOrd([r.navn, ...r.ingredienser.map(i => i.navn)].join(' ')).some(o => o.startsWith(s)));
        return { kylling: n('kylling'), KYLLING: n('KYLLING'), pasta: n('pasta'), kp: n('kylling pasta'), kyl: n('kyl'), nonsens: n('xqzvbn'), tom: n('   '), ris: n('ris'), paris: R.filter(r => soegOrd(r.navn + ' ' + r.ingredienser.map(i => i.navn).join(' ')).includes('paris')).length,
          risForkert: R.filter(r => { const o = soegOrd([r.navn, ...r.ingredienser.map(i => i.navn)].join(' ')); return !o.some(w => w.startsWith('ris')); }).filter(r => soegRetter([r], 'ris').size).length,
          kyllinger: n('kyllinger'), gulerodder: n('gulerødder'), gulerod: n('gulerod'), ost: n('ost'),
          osteForkert: R.filter(r => { const o = soegOrd([r.navn, ...r.ingredienser.map(i => i.navn)].join(' ')); return !o.some(w => w.startsWith('ost')); }).filter(r => soegRetter([r], 'ost').size).length };
      });
      t(par.kylling > 0 && par.kylling === par.KYLLING, m + 'kylling/KYLLING: ' + par.kylling + '/' + par.KYLLING);
      t(par.pasta > 0 && par.kp <= Math.min(par.kylling, par.pasta), m + '"kylling pasta" skal være højst så mange som hvert ord');
      t(par.kyl >= par.kylling, m + '"kyl" finder færre end "kylling"');
      t(par.nonsens === 0, m + 'nonsens finder noget');
      t(par.tom === -1, m + 'kun mellemrum skal ikke være en søgning');
      t(par.risForkert === 0, m + '"ris" matcher midt i et ord');
      t(par.osteForkert === 0, m + '"ost" (under 4 tegn) matcher midt i et ord');
      t(par.kyllinger >= par.kylling, m + 'flertal "kyllinger" finder færre end "kylling"');
      t(par.gulerodder >= par.gulerod, m + 'flertal "gulerødder" finder færre end "gulerod"');
      // ental/flertal giver samme retter, og falske midt-i-ord-træffere udebliver (samme krav som soeg_browser.py)
      const enFl = await side.evaluate(() => {
        const R = pool(aktivS()), mængde = s => { const x = soegRetter(R, s); return x ? x.size : -1; };
        const falsk = [{ id: 'a', navn: 'Tomatris', ingredienser: [{ navn: 'tomatris' }] }, { id: 'b', navn: 'Risotto', ingredienser: [{ navn: 'ris' }] }, { id: 'c', navn: 'Ostesovs', ingredienser: [{ navn: 'smeltet cheddar' }] }, { id: 'd', navn: 'Suppe', ingredienser: [{ navn: 'løgene' }, { navn: 'kartofler' }] }];
        const ids = s => [...soegRetter(falsk, s)].join('');
        return { par: [['kartoffel', 'kartofler'], ['gulerod', 'gulerødder'], ['tomat', 'tomater'], ['pølse', 'pølser'], ['løg', 'løgene']].map(([a, b]) => [a, b, mængde(a), mængde(b)]),
          ris: ids('ris'), ost: ids('ost'), logene: ids('løg'), kartofler: ids('kartoffel'), kartoffel: ids('kartofler') };
      });
      enFl.par.forEach(([a, b, x, y]) => t(x > 0 && x === y, m + `"${a}" (${x}) og "${b}" (${y}) skal give samme antal retter`));
      t(enFl.ris === 'b', m + '"ris" skal kun finde ordet ris, ikke tomatris: ' + enFl.ris);
      t(enFl.ost === 'c', m + '"ost" skal kun finde ordstart: ' + enFl.ost);
      t(enFl.logene === 'd' && enFl.kartofler === 'd' && enFl.kartoffel === 'd', m + 'ental/flertal på prøveretter: ' + JSON.stringify(enFl));
      // skriv i feltet
      const valgtId = await side.evaluate(() => document.querySelector('#ret-indhold .grid .ret')?.dataset.ret);
      await side.click(`#ret-indhold .grid .ret[data-ret="${valgtId}"] h3`);  // vælg en ret
      const valgtFoer = await side.evaluate(() => JSON.stringify([state.valgte, state.dagPlads]));
      await side.fill('#ret-soeg', 'KYLLING');
      const efter = await side.evaluate(() => ({ kort: [...document.querySelectorAll('#ret-indhold .grid .ret')].map(e => e.querySelector('h3').textContent), status: document.getElementById('ret-soeg-status').textContent, x: !document.getElementById('ret-soeg-x').hidden, vandret: document.documentElement.scrollWidth > innerWidth, fokus: document.activeElement.id, foldet: !!document.getElementById('uge-fold'), aktivKat: document.querySelectorAll('.kat.aktiv').length }));
      t(efter.kort.length === par.kylling && efter.kort.length > 0, m + 'antal kort efter søgning: ' + efter.kort.length + ' mod ' + par.kylling);
      t(/retter? passer til "KYLLING"/.test(efter.status), m + 'resultatlinje: ' + efter.status);
      const dinUge = await side.evaluate(() => [...document.querySelectorAll('#ret-indhold *')].filter(e => e.children.length === 0 && /^Din uge\b/.test(e.textContent.trim()) && e.getBoundingClientRect().height > 0).length);
      t(dinUge === 1, m + 'der skal være én synlig "Din uge"-overskrift under søgning (foldet), ikke ' + dinUge);
      t(efter.x && efter.fokus === 'ret-soeg' && efter.foldet && !efter.vandret && efter.aktivKat === 0, m + 'tilstand under søgning: ' + JSON.stringify({ x: efter.x, fokus: efter.fokus, foldet: efter.foldet, vandret: efter.vandret, aktivKat: efter.aktivKat }));
      const kortTop = await side.evaluate(() => document.querySelector('#ret-indhold .grid .ret')?.getBoundingClientRect().top);
      t(kortTop < 500, m + 'første træffer ligger for langt nede: ' + kortTop);
      // valgt ret, der ikke passer, bevares
      await side.fill('#ret-soeg', 'xqzvbn');
      const tom = await side.evaluate(() => ({ kort: document.querySelectorAll('#ret-indhold .grid .ret').length, tom: document.querySelector('.soeg-tom')?.textContent || '', note: document.getElementById('ret-soeg-status').textContent, valgt: JSON.stringify([state.valgte, state.dagPlads]), bund: document.querySelector('.bund, #bund')?.textContent || '' }));
      t(tom.kort === 0 && /Ingen retter passer til "xqzvbn"/.test(tom.tom) && /Vis alle retter/.test(tom.tom), m + 'tom-tilstand mangler: ' + tom.tom.slice(0, 80));
      t(/1 valgt ret passer ikke til søgningen, men er stadig med i din madplan/.test(tom.note), m + 'note om valgt ret mangler: ' + tom.note);
      t(tom.valgt === valgtFoer, m + 'søgningen ændrede state.valgte/dagPlads');
      const knapH = await side.evaluate(() => document.querySelector('[data-retsoeg-ryd].knap').getBoundingClientRect().height);
      t(knapH >= 44, m + '"Vis alle retter" under 44 px');
      await side.click('.soeg-tom [data-retsoeg-ryd]');
      const ryd = await side.evaluate(() => ({ kort: document.querySelectorAll('#ret-indhold .grid .ret').length, v: document.getElementById('ret-soeg').value, valgt: state.valgte.length, foldet: !!document.getElementById('uge-fold') }));
      t(ryd.kort === alle && ryd.v === '' && ryd.valgt === 1 && !ryd.foldet, m + 'rydning: ' + JSON.stringify(ryd) + ' (alle=' + alle + ')');
      // ×-knap og Escape
      await side.fill('#ret-soeg', 'pasta');
      const xh = await side.evaluate(() => document.getElementById('ret-soeg-x').getBoundingClientRect().height);
      t(xh >= 44, m + '× under 44 px');
      await side.click('#ret-soeg-x');
      t((await side.evaluate(() => document.querySelectorAll('#ret-indhold .grid .ret').length)) === alle, m + '× rydder ikke');
      await side.fill('#ret-soeg', 'pasta'); await side.press('#ret-soeg', 'Escape');
      t((await side.evaluate(() => document.getElementById('ret-soeg').value)) === '', m + 'Escape rydder ikke');
      // kategori rydder søgningen
      await side.fill('#ret-soeg', 'pasta');
      await side.click('.kat[data-koekken]');
      t((await side.evaluate(() => document.getElementById('ret-soeg').value)) === '', m + 'tryk på kategori rydder ikke søgningen');
      await ctx.close();
    }
  } finally { if (b) await b.close(); srv.close(); }
})().then(() => {
  jsFejl.forEach(e => fejl.push('JavaScript-fejl: ' + e));
  fejl.slice(0, 30).forEach(f => console.log('FEJL:', f));
  console.log('SØGNING I BROWSER:', fejl.length ? `FEJLET (${fejl.length} fejl)` : 'BESTÅET');
  if (process.exitCode !== 3) process.exitCode = fejl.length ? 1 : 0;
}).catch(e => { console.error('FEJL: ' + String(e && e.message || e).split('\n')[0]); process.exit(1); });
