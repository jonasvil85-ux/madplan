// Test af budget i ugeforslaget. Køres af kontrol.py (node, uden browser, uden net). Samme DOM-attrap, frosne ur og datakopi som regression.js.
// Indlæser sidens EGEN JavaScript (ikoner.js, varer.js, pris.js, kategorier.js og scriptet i index.html) i en vm
// med en minimal DOM-attrap og fastfrosset ur, og regner på en gemt kopi af data (fixtur/*.json.gz).
// Brug: node regression.js <rodmappe> [fixturmappe]  -> skriver resultatet som JSON på stdout.
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm'), zlib = require('zlib');
const rod = path.resolve(process.argv[2] || '.');
const fix = path.resolve(process.argv[3] || path.join(rod, 'scripts/tests/fixtur'));
const laes = n => JSON.parse(zlib.gunzipSync(fs.readFileSync(path.join(fix, n + '.json.gz'))).toString('utf8'));
const D = { retter: laes('retter'), opskrifter: laes('opskrifter'), tilbudsliste: laes('tilbudsliste'), naering: laes('naering') };

// ---- DOM-attrap: alt kan kaldes og læses, intet gør noget ----
const attrap = () => {
  const f = function () {};
  const p = new Proxy(f, {
    get: (t, k) => k === Symbol.toPrimitive ? () => '' : k === 'then' ? undefined : k === 'length' ? 0 : k === Symbol.iterator ? function* () {} : k === 'dataset' ? {} : k === 'style' ? {} : k === 'classList' ? { add() {}, remove() {}, toggle() {}, contains: () => false } : p,
    set: () => true, apply: () => p, construct: () => p,
  });
  return p;
};
// Fastfrosset ur: søndag 2026-11-15 12:00 lokal tid (data har ingen betydning for prisregler, men ugedage og udløbsdatoer skal være ens)
const NU = new Date(2026, 10, 15, 12, 0, 0).getTime();
const RealDate = Date;
class FrossenDato extends RealDate { constructor(...a) { if (a.length === 0) super(NU); else super(...a); } static now() { return NU; } }
const lager = {};
const win = {};
const sb = {
  window: win, document: attrap(), navigator: { userAgent: 'node', platform: 'node', maxTouchPoints: 0, serviceWorker: undefined },
  location: { search: '', hash: '', protocol: 'http:', hostname: 'test', pathname: '/' },
  localStorage: { getItem: k => lager[k] ?? null, setItem: (k, v) => { lager[k] = String(v); }, removeItem: k => { delete lager[k]; } },
  sessionStorage: { getItem: () => null, setItem() {} },
  matchMedia: () => ({ matches: false, addEventListener() {} }), addEventListener() {}, setTimeout: () => 0, clearTimeout() {}, requestAnimationFrame: () => 0,
  scrollTo() {}, scrollY: 0, confirm: () => true, console, Date: FrossenDato, Math, JSON, structuredClone,
  URLSearchParams, fetch: async u => { const n = String(u).replace(/^\/|\.json.*$/g, ''); if (!D[n]) return { ok: false, status: 404 }; return { ok: true, status: 200, json: async () => structuredClone(D[n]) }; },
};
Object.assign(win, sb); sb.window = win; sb.self = win; sb.globalThis = win;
const ctx = vm.createContext(sb);
const kør = (kode, fil) => vm.runInContext(kode, ctx, { filename: fil });

for (const f of ['ikoner.js', 'varer.js', 'pris.js', 'kategorier.js']) kør(fs.readFileSync(path.join(rod, f), 'utf8'), f);
const html = fs.readFileSync(path.join(rod, 'index.html'), 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
if (scripts.length !== 1) throw new Error('forventede ét indlejret script i index.html, fandt ' + scripts.length);
// De to sidste linjer starter siden (henter data, login); testen indlæser data selv
const kode = scripts[0].replace(/^forhent\(\);\s*$/m, '').replace(/^startAuth\(start\);.*$/m, '');
if (kode === scripts[0]) throw new Error('kunne ikke finde start-linjerne (forhent/startAuth) i index.html');
kør(kode, 'index.html');

(async () => {
  await kør('(async () => { await start(); })()', 'start');
  // Egenskaber for budget i ugeforslaget (frossen datakopi, frosset ur), for tre husstande og alle 9 butikker:
  // 1) uden budget er alt som før (samme uge to gange)  2) et budget gør aldrig ugen dyrere end uden  3) et budget >= ugens pris ændrer ikke ugen
  // 4) altid 7 retter  5) ugyldige gemte værdier får intet til at gå i stykker
  const ud = kør(`(() => {
    const fejl = [], rapport = {};
    const plan = (b, v, bo) => { state.voksne = v; state.boern = bo; state.personer = v + bo; nulstilSim(); const pl = simFraButikker([b]); const pris = ugePris(pl.map(x => x.r.id), planMult(pl), [b]); return { ids: pl.map(x => x.r.id), ialt: Math.round(pris.ialt), eksakt: pris.ialt, dage: pl.length }; };
    for (const [v, bo] of [[2, 2], [2, 0], [1, 0]]) {
      for (const b of Object.keys(data.butikker)) {
        state.budget = 0;
        const basis = plan(b, v, bo), igen = plan(b, v, bo);
        const h = v + '+' + bo + ' ' + b;
        if (JSON.stringify(basis.ids) !== JSON.stringify(igen.ids) || basis.eksakt !== igen.eksakt) fejl.push(h + ': samme valg giver ikke samme uge');
        if (basis.dage !== 7) fejl.push(h + ': ugen har ' + basis.dage + ' retter');
        for (const bud of [1, Math.round(basis.eksakt * 0.8), Math.round(basis.eksakt * 0.95), Math.floor(basis.eksakt), Math.ceil(basis.eksakt), Math.ceil(basis.eksakt) + 1, 100000]) {
          state.budget = bud; const q = plan(b, v, bo);
          if (q.dage !== 7) fejl.push(h + ': budget ' + bud + ' gav ' + q.dage + ' retter');
          if (q.eksakt > basis.eksakt + 0.001) fejl.push(h + ': budget ' + bud + ' gjorde ugen dyrere (' + q.ialt + ' mod ' + basis.ialt + ')');
          if (bud >= basis.eksakt && JSON.stringify(q.ids) !== JSON.stringify(basis.ids)) fejl.push(h + ': budget ' + bud + ' over ugens pris ændrede ugen');
        }
        state.budget = 0;
        rapport[h] = basis.ialt;
      }
    }
    // ugyldige gemte værdier
    for (const bad of [{ budget: 'abc' }, { budget: -5 }, { budget: 1e9 }, { budget: null }]) {
      try { anvendHusstand({ voksne: 2, boern: 2, ...bad }); if (!(state.budget >= 0 && state.budget <= 20000) && state.budget !== 0) fejl.push('ugyldig budgetværdi gav ' + state.budget); } catch (e) { fejl.push('ugyldig værdi ' + JSON.stringify(bad) + ' kastede: ' + e.message); }
    }
    state.budget = 0; state.voksne = 2; state.boern = 2; state.personer = 4;
    return { fejl, rapport };
  })()`, 'budget');
  if (ud.fejl.length) { console.log('FEJL:\n' + ud.fejl.slice(0, 30).join('\n')); process.exit(1); }
  console.log('BUDGET: BESTÅET (' + Object.keys(ud.rapport).length + ' kombinationer af husstand og butik)');
})().catch(e => { console.error('FEJL: ' + (e && e.stack || e)); process.exit(2); });
