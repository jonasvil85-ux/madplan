// Måling: bliver ugeforslaget dyrere, når der kommer en (billig) ret til? Køres af monotoni.py (node, uden browser og net).
// Samme DOM-attrap, frosne ur og datakopi som regression.js. Ændrer INTET i ugeforslagets algoritme – kun måling.
// Brug: node monotoni.js <rodmappe> [fixturmappe] [--ingen-konstrueret]  -> skriver resultatet som JSON på stdout.
'use strict';
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
  sb: null, bruger: null,  // login (auth.js indlæses ikke i testen): som en bruger, der ikke er logget ind; gemHusstand gemmer så kun lokalt
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
  const ud = kør(`(() => {
    const HUSSTANDE = [[2, 0], [2, 2], [6, 4]];
    const ryd = () => { INGHUKOMMELSE = new WeakMap(); MIXHUKOMMELSE.clear(); POOLHUKOMMELSE.clear(); KANDHUKOMMELSE.clear(); };
    const ugeFor = (b, v, bo) => { state.voksne = v; state.boern = bo; state.personer = v + bo; state.budget = 0; nulstilSim(); ryd();
      const pl = simFraButikker([b]); const p = ugePris(pl.map(x => x.r.id), planMult(pl), [b]); return { ids: pl.map(x => x.r.id), pris: p.ialt }; };
    // Konstruerede billige retter: kopier af butikkens billigste og mest børnevenlige retter med faktor f på alle priser
    // (nyt id og navn). Pr. butik og husstand tages det værste udfald; et fald er i orden, en stigning er en advarsel.
    const donorer = b => { const rs = data.butikker[b].retter;
      const bill = rs.slice().sort((x, y) => prisIAlt(x) - prisIAlt(y)).slice(0, 3);
      const smag = rs.slice().sort((x, y) => smagScore(y) - smagScore(x) || prisIAlt(x) - prisIAlt(y)).slice(0, 3);
      return [...new Set([...bill, ...smag])]; };
    const lav = (b, donor, f) => { const ny = { ...structuredClone(donor), id: b + '-9999', navn: 'Konstrueret billig ret (måling)' };
      for (const k of ['pris_tilbud', 'pris_oevrigt', 'pris_i_alt', 'pris_forbrug']) if (typeof ny[k] === 'number') ny[k] = ny[k] * f;
      return ny; };
    const afr = n => Math.round(n * 100) / 100;
    const raekker = [];
    for (const b of Object.keys(data.butikker)) {
      const rs = data.butikker[b].retter, ds = donorer(b);
      for (const [v, bo] of HUSSTANDE) {
        const for_ = ugeFor(b, v, bo);
        let vaerst = null, forsoeg = 0;
        for (const d of ds) for (const f of [0.25, 0.5]) {
          const ny = lav(b, d, f);
          data.butikker[b].retter = [...rs, ny];   // nyt array (opslag på id er cachet pr. array)
          const efter = ugeFor(b, v, bo);
          data.butikker[b].retter = rs;
          forsoeg++;
          const diff = efter.pris - for_.pris;
          if (!vaerst || diff > vaerst.diff) vaerst = { diff, efter: efter.pris, donor: d.id, faktor: f, brugt: efter.ids.includes(ny.id) };
        }
        const igen = ugeFor(b, v, bo);   // gentagelighed: samme uge igen, når retterne er væk
        raekker.push({ butik: b, husstand: v + '+' + bo, for: afr(for_.pris), efter: afr(vaerst.efter), diff: afr(vaerst.diff), donor: vaerst.donor, faktor: vaerst.faktor, brugt: vaerst.brugt, forsoeg,
          gentagelig: JSON.stringify(igen.ids) === JSON.stringify(for_.ids) && igen.pris === for_.pris });
      }
    }
    return { raekker };
  })()`, 'monotoni');
  process.stdout.write(JSON.stringify(ud, null, 1));
})().catch(e => { console.error('FEJL: ' + (e && e.stack || e)); process.exit(2); });
