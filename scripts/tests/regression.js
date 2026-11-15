// Regressionstest af pris, indkøbsliste og ugeforslag. Køres af regression.py (node, uden browser, uden net).
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
  const ud = kør(`(() => {
    const afr = (n, d = 2) => n == null ? null : Math.round(n * 10 ** d) / 10 ** d;
    const afrO = o => o == null ? null : typeof o === 'number' ? afr(o) : Object.fromEntries(Object.entries(o).map(([a, c]) => [a, typeof c === 'number' ? afr(c) : Array.isArray(c) ? c.slice() : c]));
    const res = { genereret: data.genereret, butikker: {} };
    const stil = (butikker, v = 2, b = 2) => { state = { ...structuredClone(TOM), voksne: v, boern: b, personer: v + b, butikker, butik: butikker[0], butikValgt: true }; nulstilSim(); };
    for (const bk of Object.keys(data.butikker)) {
      const o = {};
      stil([bk]);
      // 1) ugeforslaget (én butik) for familie og for to voksne
      for (const [v, b] of [[2, 2], [2, 0]]) {
        stil([bk], v, b);
        const k = simK(), plan = simPlan(k), akt = simAktive(k);
        o['uge_' + v + '_' + b] = { retter: akt.map(x => x.r.id), pris: afrO(simPris(k)) };
      }
      // 2) indkøbsliste for familiens forslag
      stil([bk]);
      { const k = simK(), akt = simAktive(k);
        state.valgte = akt.map(x => x.r.id); state.koebButikker = simPlan(k).S.slice(); state.mult = planMult(akt);
        const L = listeLinjer();
        const lin = g => L[g].map(x => ({ navn: x.navn, butik: x.butik, pris: afr(x.pris), skoen: afr(x.skoen), gruppe: x.gruppe }));
        o.liste = { tilbud: lin('tilbud'), oevrige: lin('oevrige'), basis: lin('basis').map(x => x.navn), sum: Object.fromEntries(Object.entries(prisSum([...L.tilbud, ...L.oevrige, ...L.basis])).map(([a, c]) => [a, afr(c)])),
          ekstra: Object.fromEntries(Object.keys(EKSTRA_TITLER).map(g => [g, L[g].map(x => x.navn + '|' + afr(x.pris))])) };
        o.ugePris = afr(ugePris(state.valgte, state.mult));
      }
      // 3) udvalg af retter: forbrugs- og indkøbspris (første, midterste og sidste ret i butikkens egen liste)
      { const rs = data.butikker[bk].retter; const valg = [rs[0], rs[Math.floor(rs.length / 2)], rs[rs.length - 1]];
        o.retter = valg.map(r => ({ id: r.id, navn: r.navn, forbrug: afr(r.pris_forbrug), indkoeb: afr(prisIAlt(r)), tilbud: afr(r.pris_tilbud), oevrigt: afr(r.pris_oevrigt) })); }
      res.butikker[bk] = o;
    }
    // 4) kombinationer af butikker
    res.kombi = {};
    for (const S of [['netto', 'lidl'], ['rema', 'bilka', 'spar']]) {
      stil(S); const k = simK(); const akt = simAktive(k);
      res.kombi[S.join('+')] = { retter: akt.map(x => x.r.id), pris: afrO(simPris(k)) };
    }
    // 5) opskrifter bygget over alle butikker: pris pr. ret
    stil(Object.keys(data.butikker));
    res.mix = mixFor(Object.keys(data.butikker)).liste.filter(r => r.ok).slice(0, 25).map(r => ({ id: r.id, navn: r.navn, indkoeb: afr(prisIAlt(r)), tilbud: afr(r.pris_tilbud), oevrigt: afr(r.pris_oevrigt) }));
    // 6) pakkeregler (antalPakker) og skønspriser (skoenPris) direkte
    // pakkeregler: antal pakker for et tilbud med en given pakkestørrelse (hele pakker, 15 % tolerance, intervaller bruger midten)
    res.pakker = [[{ maengde: '500', enhed: 'g' }, { g: 480 }], [{ maengde: '500', enhed: 'g' }, { g: 1100 }], [{ maengde: '1', enhed: 'kg' }, { g: 1500 }], [{ maengde: '100-400', enhed: 'g' }, { g: 600 }],
      [{ maengde: '6', enhed: 'stk' }, { stk: 7 }], [{ maengde: '250', enhed: 'ml' }, { ml: 700 }], [{ maengde: '400', enhed: 'g' }, { dåse: 2 }]].map(([t, b]) => antalPakker({ ...t }, b));
    res.skoen = ['kartofler', 'hakket oksekød', 'pasta', 'piskefløde', 'løg', 'hvidløg', 'laks', 'æg', 'ris', 'mælk', 'tomatpuré']
      .map(n => [n, afr(skoenPris(n, 500, 'g')), afr(skoenPris(n, 2, 'stk')), afr(skoenPris(n, 250, 'ml'))]);
    return res;
  })()`, 'regn');
  process.stdout.write(JSON.stringify(ud, null, 1));
})().catch(e => { console.error('FEJL: ' + (e && e.stack || e)); process.exit(2); });
