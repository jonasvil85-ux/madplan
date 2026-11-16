// Test af "Sammenlign butikker" (BACKLOG accept 1, 2, 8, 9, 10, 11). Køres af kontrol.py (node, uden browser, uden net). Samme DOM-attrap, frosne ur og datakopi som regression.js.
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
  // Alle tal regnes igen her med sidens egne prisfunktioner (simK/simPlan, simStandard, ugePris, planMult) og sammenlignes med kortets funktioner.
  const ud = kør(`(() => {
    const fejl = [], info = [], rapport = {};
    const BUT = Object.keys(data.butikker);
    const r2 = x => Math.round(x * 100) / 100;
    const planPris = p => ugePris(p.map(x => x.r.id), planMult(p), p.S);
    for (const [v, bo] of [[2, 2], [2, 0], [1, 0]]) {
      const H = v + '+' + bo;
      state.voksne = v; state.boern = bo; state.personer = v + bo; state.budget = 0; nulstilSim();
      // (1)+(8)+(11): hver butik = det, siden viser, når butikken vælges alene; 7 aftensmåltider til husstanden, ingen mindre portioner
      const pris = {};
      for (const b of BUT) {
        state.butikker = [b]; state.koebButikker = []; state.maxButikker = 0;
        const k = simK(), plan = simPlan(k), t = sammButikTal(b);
        const egen = planPris(plan);  // uafhængig genberegning af den pris, siden viser ved enkeltvalg
        const tag = H + ' ' + b;
        if (k !== b + '|1') fejl.push(tag + ': enkeltvalget bruger nøglen ' + k + ', kortet ' + b + '|1');
        if (Math.abs(t.ialt - egen.ialt) > 0.001 || Math.abs(t.ialt - simPrisPlan(k).ialt) > 0.001) fejl.push(tag + ': kortets pris ' + r2(t.ialt) + ' er ikke sidens pris ' + r2(egen.ialt));
        if (Math.abs(t.spar - egen.spar) > 0.001) fejl.push(tag + ': "Sparer" ' + r2(t.spar) + ' er ikke normalpris minus pris for de samme varer (' + r2(egen.spar) + ')');
        if (!(t.spar >= 0) || !(t.ialt > 0) || !Number.isFinite(t.tilbud)) fejl.push(tag + ': ugyldige tal ' + JSON.stringify([t.ialt, t.spar, t.tilbud]));
        if (plan.length !== 7) fejl.push(tag + ': ' + plan.length + ' aftensmåltider, ikke 7');
        if (plan.some(x => !(x.mult >= 1))) fejl.push(tag + ': en ret har mindre end én portion til husstanden');
        if (state.personer !== v + bo) fejl.push(tag + ': regnet for ' + state.personer + ' personer');
        pris[b] = t;
      }
      // (2): sorteret billigst først, og "Billigst" på den billigste (samme orden og regel som kortet)
      Object.assign(SAMM, { pris, fejl: {}, faerdig: true, kombi: null });
      const orden = sammOrden(), gyldige = orden.filter(b => !udloebet(data.butikker[b]));
      for (let i = 1; i < gyldige.length; i++) if (Math.round(pris[gyldige[i]].ialt) < Math.round(pris[gyldige[i - 1]].ialt)) fejl.push(H + ': listen er ikke billigst først (' + gyldige[i - 1] + ' før ' + gyldige[i] + ')');
      const billigst = orden.map((b, i) => sammRaekke(b, i)).filter(h => h.includes('samm-billigst')).length;
      const minP = Math.min(...gyldige.map(b => Math.round(pris[b].ialt))), antalMin = gyldige.filter(b => Math.round(pris[b].ialt) === minP).length;
      if (billigst !== antalMin || billigst < 1) fejl.push(H + ': ' + billigst + ' rækker har "Billigst", forventet ' + antalMin);
      // (9)+(11): to butikker. For HVERT par regnes prisen igen som én samlet liste over begge butikker,
      // og besparelsen mod (a) samme retter og mængder i den billigste enkeltbutik og (b) dens egen uge.
      const { enkeltButik, top } = sammKombiKandidater();
      if (enkeltButik !== gyldige[0]) fejl.push(H + ': kombinationen sammenlignes med ' + enkeltButik + ', men billigste butik er ' + gyldige[0]);
      const enkeltPlan = simPlan(enkeltButik + '|1'), enkelt = planPris(enkeltPlan).ialt;
      const par = []; for (let i = 0; i < gyldige.length; i++) for (let j = i + 1; j < gyldige.length; j++) par.push([gyldige[i], gyldige[j]]);
      let bedstTop = null, bedstAlle = null;
      for (const p of par) {
        const tag = H + ' ' + p.join('+'), t = sammKombiTal(p, enkeltButik), k = p.slice().sort().join('+') + '|2', plan = simStandard(k);
        if (!plan || plan.length !== 7 || plan.butikker.length < 2) { if (t) fejl.push(tag + ': kombinationen kan vises, selv om ugen ikke bruger begge butikker'); continue; }
        if (!t) { fejl.push(tag + ': kunne ikke regnes'); continue; }
        if (plan.some(x => !(x.mult >= 1))) fejl.push(tag + ': en ret har mindre end én portion');
        const ids = plan.map(x => x.r.id), mult = planMult(plan);
        const samlet = ugePris(ids, mult, plan.S).ialt, iEnkelt = ugePris(ids, mult, [enkeltButik]).ialt;
        if (Math.abs(t.pris - samlet) > 0.001 || Math.abs(t.pris - simPris(k).ialt) > 0.001) fejl.push(tag + ': prisen ' + r2(t.pris) + ' er ikke én samlet liste over begge butikker (' + r2(samlet) + ')');
        if (Math.abs(t.sammeIEnkelt - iEnkelt) > 0.001) fejl.push(tag + ': "samme retter i ' + enkeltButik + '" ' + r2(t.sammeIEnkelt) + ' mod genberegnet ' + r2(iEnkelt));
        if (Math.abs(t.enkelt - enkelt) > 0.001) fejl.push(tag + ': enkeltbutikkens uge ' + r2(t.enkelt) + ' mod ' + r2(enkelt));
        const spar = Math.min(Math.round(iEnkelt), Math.round(enkelt)) - Math.round(samlet);
        if (t.spar !== spar) fejl.push(tag + ': besparelsen ' + t.spar + ' er ikke det mindste af (a) og (b): ' + spar);
        const indTop = top.includes(p[0]) && top.includes(p[1]);
        const bedre = (x, y) => x.spar >= ANBEFAL_SPAR && (!y || x.vist.pris < y.vist.pris || (x.vist.pris === y.vist.pris && x.spar > y.spar));
        if (indTop && bedre(t, bedstTop)) bedstTop = t;
        if (bedre(t, bedstAlle)) bedstAlle = t;
      }
      const vist = bedstTop && bedstTop.spar >= ANBEFAL_SPAR ? bedstTop : null;
      if (vist && !(vist.spar > STRAF_PR_EKSTRA_BUTIK)) fejl.push(H + ': kombinationen overvinder ikke tidsstraffen for en ekstra butik');
      if (vist) {  // teksten, brugeren ser
        SAMM.kombi = vist; const html = sammKombiHtml();
        for (const tal of [vist.spar, vist.vist.pris, vist.vist.sammeIEnkelt, vist.vist.enkelt]) if (!html.includes(kr(tal))) fejl.push(H + ': kombi-teksten mangler ' + kr(tal));
        if (!/Transport/.test(html) || !/ikke regnet med/.test(html)) fejl.push(H + ': kombi-teksten siger ikke, at transport ikke er regnet med');
        if (vist.vist.pris + vist.spar > Math.min(vist.vist.sammeIEnkelt, vist.vist.enkelt)) fejl.push(H + ': tallene i teksten går ikke op');
      }
      if (bedstAlle && (!vist || bedstAlle.vist.pris < vist.vist.pris)) info.push(H + ': parret ' + bedstAlle.butikker.join('+') + ' uden for de ' + SAMM_KOMBI_TOP + ' billigste ville give ' + bedstAlle.vist.pris + ' kr mod vist ' + (vist ? vist.vist.pris + ' kr' : 'ingen'));
      const status = sammStatus();
      if (!status.includes('7 aftensmåltider') || !status.includes(husstandTekst(v, bo))) fejl.push(H + ': kortet siger ikke "7 aftensmåltider til ' + husstandTekst(v, bo) + '"');
      rapport[H] = { pris: Object.fromEntries(BUT.map(b => [b, Math.round(pris[b].ialt)])), kombi: vist ? [vist.butikker.join('+'), vist.vist.pris, vist.vist.sammeIEnkelt, vist.vist.enkelt, vist.spar] : null };
    }
    state.voksne = 2; state.boern = 2; state.personer = 4; state.butikker = []; nulstilSim();
    Object.assign(SAMM, { pris: {}, fejl: {}, faerdig: false, kombi: null });
    return { fejl, info, rapport };
  })()`, 'sammenlign');
  for (const l of ud.info) console.log('INFO: ' + l);
  if (ud.fejl.length) { console.log('FEJL:\n' + ud.fejl.slice(0, 30).join('\n')); process.exit(1); }
  const fp = require('crypto').createHash('sha256').update(JSON.stringify(ud.rapport)).digest('hex').slice(0, 12);
  for (const [h, r] of Object.entries(ud.rapport)) console.log(h + ': ' + Object.entries(r.pris).map(([b, p]) => b + ' ' + p).join(', ') + ' | to butikker: ' + (r.kombi ? r.kombi.join(' / ') : 'ingen'));
  console.log('SAMMENLIGN: BESTÅET (3 husstande × 9 butikker og alle par; fingeraftryk ' + fp + ')');
})().catch(e => { console.error('FEJL: ' + (e && e.stack || e)); process.exit(2); });
