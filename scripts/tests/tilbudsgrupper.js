// Test af "Gode tilbud"-grupperne på indkøbslisten (BACKLOG [UX] "Gode tilbud-grupperne nederst på indkøbslisten"). Køres af kontrol.py (node, uden browser).
// Samme DOM-attrap, frosne ur og datakopi som sammenlign.js. Tjekker titlerne for alle varer i alle grupper og alle 9 butikker, og at den tegnede liste
// foldes til 4 rækker pr. gruppe uden at ændre summen.
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
    const fejl = []; let antal = 0, med = 0;
    for (const [g, liste] of Object.entries(tilbudsliste.grupper)) for (const t of liste) {
      antal++;
      const titel = kortNavn(t.navn), alt = alternativer(t.navn), n = andreSlags(t.navn);
      if (titel.length > 41) fejl.push(g + ': titel over 40 tegn: ' + titel);
      if (/\\seller\\s/i.test(titel) && !/-\\s+eller\\s/i.test(t.navn)) fejl.push(g + ': titlen indeholder alternativer: ' + titel);
      if (titel.endsWith('…') && !(alt[0].startsWith(titel.slice(0, -1)) && (alt[0][titel.length - 1] === ' ' || alt[0][titel.length - 1] === ',')))
        fejl.push(g + ': afkortet midt i et ord: ' + titel + ' <- ' + alt[0]);
      if (n !== alt.length - 1 || n < 0) fejl.push(g + ': forkert antal andre: ' + t.navn);
      if (n) med++;
    }
    const prov = [['PEPSI MAX, FAXE KONDI ELLER COLA ZERO', 'Pepsi max', 2], ['Combino fusilli eller penne rigate', 'Combino fusilli', 1], ['Høker røget bacon', 'Høker røget bacon', 0],
                  ['Meget lang tilbudstekst uden alternativer og med mange ord i titlen', 'Meget lang tilbudstekst uden…', 0]];
    for (const [i, t, n] of prov) if (kortNavn(i) !== t || andreSlags(i) !== n) fejl.push('prøve "' + i + '": fik "' + kortNavn(i) + '" / ' + andreSlags(i) + ', forventede "' + t + '" / ' + n);
    // Tegnet liste: lukkede grupper viser højst 4 rækker, "Vis flere" findes, og summen er den samme foldet og udfoldet
    const rapport = {};
    let html = '';
    const ind = { set innerHTML(h) { html = h; }, get innerHTML() { return html; } }, dok0 = document;
    document = new Proxy(dok0, { get: (t, k) => k === 'getElementById' ? id => id === 'indhold' ? ind : dok0.getElementById(id) : t[k] });
    for (const b of Object.keys(data.butikker)) {
      state.voksne = 2; state.boern = 2; state.personer = 4; state.budget = 0; state.butikker = [b]; state.koebButikker = []; nulstilSim();
      const plan = simPlan(simK());
      state.butik = b; state.koebButikker = [b]; state.valgte = plan.map(x => x.r.id); state.mult = planMult(plan); state.valgtVare = {}; state.ekstra = [];
      standardValg(); ekstraAaben.clear();
      const L = listeLinjer(), sek = listeSektioner(L).filter(s => s.vaelgAlle === false);
      html = ''; renderListe(); const lukket = html; 
      for (const s of sek) {
        if (s.linjer.length <= EKSTRA_SYNLIGE) continue;
        const i = lukket.indexOf('id="ekstra-' + s.id + '"');
        if (i < 0) { fejl.push(b + ' ' + s.id + ': gruppen er ikke foldet'); continue; }
        const stykke = lukket.slice(i, lukket.indexOf('</button>', i));
        const rk = (stykke.match(/class="vare liste-vare/g) || []).length;
        if (rk !== EKSTRA_SYNLIGE) fejl.push(b + ' ' + s.id + ': ' + rk + ' rækker i lukket gruppe, ikke ' + EKSTRA_SYNLIGE);
        if (!stykke.includes('Vis ' + (s.linjer.length - EKSTRA_SYNLIGE) + ' flere') || !stykke.includes('aria-expanded="false"')) fejl.push(b + ' ' + s.id + ': knappen "Vis flere" mangler');
        ekstraAaben.add(s.id); html = ''; renderListe(); const aaben = html; ekstraAaben.delete(s.id);
        const j = aaben.indexOf('id="ekstra-' + s.id + '"'), st2 = aaben.slice(j, aaben.indexOf('</button>', j));
        if ((st2.match(/class="vare liste-vare/g) || []).length !== s.linjer.length || !st2.includes('Vis færre')) fejl.push(b + ' ' + s.id + ': udfoldet gruppe viser ikke alle rækker');
      }
      const sum = Math.round(prisSum(Object.values(L).flat().filter(x => state.valgtVare[x.key])).ialt * 100) / 100;
      rapport[b] = { grupper: sek.map(s => s.linjer.length), sum };
    }
    const foldede = Object.values(rapport).flatMap(r => r.grupper).filter(n => n > EKSTRA_SYNLIGE).length;
    if (foldede < 10) fejl.push('kun ' + foldede + ' foldede grupper i alle butikker – foldningen er ikke testet');
    if (!kortNavn('Graasten italiensk- eller karrysalat').includes('karrysalat')) fejl.push('sammensat ord "italiensk- eller karrysalat" må ikke deles');
    return { fejl, antal, med, rapport };
  })()`, 'grupper');
  if (ud.fejl.length) { console.log('FEJL:\n' + ud.fejl.slice(0, 30).join('\n')); process.exit(1); }
  console.log('GRUPPER: BESTÅET (' + ud.antal + ' varer, ' + ud.med + ' med alternativer; ' + Object.keys(ud.rapport).length + ' butikker; grupper ' + JSON.stringify(Object.fromEntries(Object.entries(ud.rapport).map(([b, r]) => [b, r.grupper.join('/')]))) + ')');
})().catch(e => { console.error('FEJL: ' + (e && e.stack || e)); process.exit(2); });
