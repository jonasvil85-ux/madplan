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
    // Grænsetilfælde (Jonas 2026-11-16), alle 9 butikker × 3 husstande:
    // budget præcis lig ugeprisen, 1 kr under, 1 kr over, meget lavt (1 og 50 kr). Beskeden under madplanen skal passe til tallet.
    const note = (q) => budgetNote({ ialt: q.eksakt });
    const graense = {};
    for (const [v, bo] of [[2, 2], [2, 0], [1, 0]]) {
      for (const b of Object.keys(data.butikker)) {
        state.budget = 0;
        const basis = plan(b, v, bo), h = v + '+' + bo + ' ' + b;
        const tilfaelde = { 'præcis ugeprisen': basis.eksakt, '1 kr under': basis.eksakt - 1, '1 kr over': basis.eksakt + 1, 'meget lavt 1 kr': 1, 'meget lavt 50 kr': 50 };
        for (const [navn, bud] of Object.entries(tilfaelde)) {
          state.budget = bud; const q = plan(b, v, bo), n = note(q);
          const tag = h + ', budget ' + navn + ' (' + bud.toFixed(2) + ' kr)';
          if (q.dage !== 7) fejl.push(tag + ': ' + q.dage + ' retter');
          if (q.eksakt > basis.eksakt + 0.001) fejl.push(tag + ': ugen blev dyrere (' + q.eksakt.toFixed(2) + ' mod ' + basis.eksakt.toFixed(2) + ')');
          if (bud >= basis.eksakt && (JSON.stringify(q.ids) !== JSON.stringify(basis.ids) || q.eksakt !== basis.eksakt)) fejl.push(tag + ': budget på eller over ugens pris ændrede ugen');
          const inden = q.eksakt <= bud;
          if (inden && !n.includes('bud-note ok')) fejl.push(tag + ': ugen holder budgettet, men beskeden siger andet');
          if (!inden && !n.includes('bud-note over')) fejl.push(tag + ': ugen er over budgettet (' + q.eksakt.toFixed(2) + '), men beskeden siger "inden for"');
          if (!inden) { const over = Math.max(1, Math.round(q.eksakt - bud)); if (!n.includes(kr(over) + ' over')) fejl.push(tag + ': beskeden angiver ikke overskridelsen ' + kr(over)); }
          graense[tag] = Math.round(q.eksakt * 100);
        }
      }
    }
    // Ændring af familiestørrelse efter budgettet er tastet (samme vej som knapperne: saetHusstand):
    // budgettet bevares, ugen regnes igen for den nye husstand (ingen gammel mellemregning) og følger stadig reglerne.
    for (const b of Object.keys(data.butikker)) {
      for (const [[v1, b1], [v2, b2]] of [[[2, 2], [1, 0]], [[1, 0], [2, 2]], [[2, 0], [2, 3]]]) {
        state.budget = 0; const basis2 = plan(b, v2, b2);
        state.budget = 0; const basis1 = plan(b, v1, b1);
        const bud = Math.round(basis1.eksakt * 0.9);
        state.budget = bud; state.voksne = v1; state.boern = b1; state.personer = v1 + b1; nulstilSim();
        state.koebButikker = [b]; simFraButikker([b]);  // forslaget for den første husstand ligger i mellemlageret
        saetHusstand(v2, b2);
        const tag = b + ': budget ' + bud + ' tastet ved ' + v1 + '+' + b1 + ', skiftet til ' + v2 + '+' + b2;
        if (state.budget !== bud) fejl.push(tag + ': budgettet blev ' + state.budget);
        if (state.voksne !== v2 || state.boern !== b2) fejl.push(tag + ': husstanden blev ikke skiftet');
        const pl = simFraButikker([b]), efter = { ids: pl.map(x => x.r.id), eksakt: ugePris(pl.map(x => x.r.id), planMult(pl), [b]).ialt };
        const frisk = plan(b, v2, b2);  // samme budget, regnet helt forfra
        if (JSON.stringify(efter.ids) !== JSON.stringify(frisk.ids) || Math.abs(efter.eksakt - frisk.eksakt) > 0.001) fejl.push(tag + ': ugen efter skiftet er ikke den samme som regnet forfra for den nye husstand');
        if (pl.length !== 7) fejl.push(tag + ': ' + pl.length + ' retter');
        if (efter.eksakt > basis2.eksakt + 0.001) fejl.push(tag + ': ugen blev dyrere end uden budget for den nye husstand');
        if (bud >= basis2.eksakt && JSON.stringify(efter.ids) !== JSON.stringify(basis2.ids)) fejl.push(tag + ': budget over den nye husstands ugepris ændrede ugen');
        const gemt = JSON.parse(localStorage.getItem(HUSSTAND_GEM) || '{}');
        if (gemt.budget !== bud || husstand(state).budget !== bud) fejl.push(tag + ': det gemte budget er ' + gemt.budget);
        graense[tag] = Math.round(efter.eksakt * 100);
      }
    }
    state.koebButikker = [];
    // Kontrollantens fund 2026-11-16: efter "Byt" må beskeden ikke kalde brugerens ændrede plan "billigste uge".
    // Alle 9 butikker, 2+2, budget 300 kr og et højt budget: byt mandag–onsdag, og beskeden skal tale om "Din madplan" med planens egen pris.
    for (const b of Object.keys(data.butikker)) {
      for (const bud of [300, 100000]) {
        state.voksne = 2; state.boern = 2; state.personer = 4; state.budget = bud; nulstilSim();
        const k = b + '|1', tag = b + ', budget ' + bud + ' efter Byt';
        simPlan(k); for (const i of [0, 1, 2]) simByt(k, i);
        if (!simAendret(k)) { fejl.push(tag + ': Byt ændrede ikke planen (testen kan ikke afgøre noget)'); continue; }
        const pp = simPrisPlan(k), n = budgetNote(pp, k, simAktive(k).length);
        if (n.includes('Billigste uge')) fejl.push(tag + ': beskeden kalder den ændrede plan "billigste uge"');
        if (!n.includes('Din madplan')) fejl.push(tag + ': beskeden nævner ikke, at det er brugerens egen madplan');
        if (!n.includes(kr(Math.round(pp.ialt)))) fejl.push(tag + ': beskeden viser ikke planens pris ' + kr(Math.round(pp.ialt)));
        if (pp.ialt <= bud ? !n.includes('bud-note ok') : !n.includes('bud-note over')) fejl.push(tag + ': beskeden passer ikke til planens pris ' + pp.ialt.toFixed(2));
        if (pp.ialt > bud && !n.includes('Vores forslag for ugen koster ' + kr(Math.round(simPris(k).ialt)))) fejl.push(tag + ': forslagets pris mangler i beskeden');
        graense[tag] = Math.round(pp.ialt * 100);
      }
    }
    state.budget = 0; nulstilSim();
    // Når budgettet ændres i feltet, beholdes de beregnede uger (nulstilBudget). Resultatet skal være præcis det samme som regnet helt forfra,
    // også efter flere skift frem og tilbage, for 1, 2 og 3 butikker.
    for (const butikker of [...Object.keys(data.butikker).map(b => [b]), ['netto', 'lidl'], ['rema', 'bilka', 'spar']]) {
      for (const [v, bo] of [[2, 2], [1, 0]]) {
        state.voksne = v; state.boern = bo; state.personer = v + bo; state.budget = 0; nulstilSim();
        const k = butikker.join('+') + '|' + butikker.length, tag = v + '+' + bo + ' ' + k;
        const fri = bud => { state.budget = bud; nulstilSim(); const p = simPlan(k); return JSON.stringify([p.map(x => x.r.id), Math.round(simPris(k).ialt * 100)]); };
        const facit = {}; for (const bud of [0, 300, 450, 100000]) facit[bud] = fri(bud);
        state.budget = 0; nulstilSim(); simPlan(k);  // varm: ugen uden budget ligger i mellemlageret
        for (const bud of [300, 0, 450, 300, 100000, 0]) {
          state.budget = bud; nulstilBudget(); const p = simPlan(k);
          const ud = JSON.stringify([p.map(x => x.r.id), Math.round(simPris(k).ialt * 100)]);
          if (ud !== facit[bud]) fejl.push(tag + ': budget ' + bud + ' via feltet gav en anden uge end regnet forfra');
        }
      }
    }
    state.budget = 0; state.voksne = 2; state.boern = 2; state.personer = 4; nulstilSim();
    rapport.graense = graense;
    // ugyldige gemte værdier
    for (const bad of [{ budget: 'abc' }, { budget: -5 }, { budget: 1e9 }, { budget: null }]) {
      try { anvendHusstand({ voksne: 2, boern: 2, ...bad }); if (!(state.budget >= 0 && state.budget <= 20000) && state.budget !== 0) fejl.push('ugyldig budgetværdi gav ' + state.budget); } catch (e) { fejl.push('ugyldig værdi ' + JSON.stringify(bad) + ' kastede: ' + e.message); }
    }
    state.budget = 0; state.voksne = 2; state.boern = 2; state.personer = 4;
    return { fejl, rapport };
  })()`, 'budget');
  if (ud.fejl.length) { console.log('FEJL:\n' + ud.fejl.slice(0, 30).join('\n')); process.exit(1); }
  // Fingeraftryk af alle tal: to kørsler på samme data skal give samme fingeraftryk (gentagelighed).
  const fp = require('crypto').createHash('sha256').update(JSON.stringify(ud.rapport)).digest('hex').slice(0, 12);
  console.log('BUDGET: BESTÅET (' + (Object.keys(ud.rapport).length - 1) + ' kombinationer af husstand og butik, ' + Object.keys(ud.rapport.graense).length + ' grænsetilfælde; fingeraftryk ' + fp + ')');
})().catch(e => { console.error('FEJL: ' + (e && e.stack || e)); process.exit(2); });
