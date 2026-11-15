// Test af fravalg ("Vi spiser ikke …") og budget i ugeforslaget. Køres af kontrol.py (node, uden browser, uden net).
// Bruger samme DOM-attrap, frosne ur og datakopi som regression.js.
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
  // Testen kører sidens egen ugeforslag-kode med fravalg og budget (frossen datakopi, frosset ur) og tjekker egenskaber, ikke tal:
  // 1) fravalg "svin" giver aldrig en ret med svinekød, og ugen har stadig 7 retter  2) et budget gør aldrig ugen dyrere end uden budget
  // 3) uden budget og fravalg er alt som før  4) for restriktive fravalg bruges ikke (siden siger det) og forslaget går ikke i stykker  5) samme valg giver samme uge
  const ud = kør(`(() => {
    const fejl = [], rapport = {};
    const plan = (b, v = 2, bo = 2) => { state.voksne = v; state.boern = bo; state.personer = v + bo; nulstilSim(); const pl = simFraButikker([b]); const pris = ugePris(pl.map(x => x.r.id), planMult(pl), [b]); return { ids: pl.map(x => x.r.id), ialt: Math.round(pris.ialt), dage: pl.length }; };
    const SVIN = /svin|gris|flæsk|bacon|medister|skinke|chorizo|pølse|spareribs|kamkotelet|nakkefilet|salsiccia/;
    const indeholder = (id, re) => { const r = ret(id); return re.test(r.navn.toLowerCase()) || r.ingredienser.some(i => re.test(i.navn.toLowerCase())); };
    // Alle ni fravalg mod en UAFHÆNGIG ordliste (bygget ud fra typerne i bibliotek_typer.py), over hele puljen i hver butik, ikke kun ugens retter
    const KOEDORD = 'svin|gris|flæsk|bacon|medister|skinke|chorizo|salsiccia|spegepølse|salami|pølse|spareribs|ribbensteg|nakkefilet|nakkesteg|nakkekam|kamsteg|kamkotelet|svinemedaljon|pulled pork|hamburgerryg|okse|bøf|entrecote|ribeye|roastbeef|culotte|flanksteak|tyksteg|tyndsteg|kalv|osso buco|gullasch|kylling|kalkun|andebryst|andelår|vildand|canette|fasan|høne|fjerkræ|laks|torsk|rejer|sild|fisk|rødspætte|makrel|skaldyr|ansjos|alaska|hellefisk|krondyr|hjort|vildt|vildsvin|lammekød|lammekølle|lammeculotte|lammekotelet|lammefars|lammeskank|lammelår|lammesteg|lammebov';
    const INDEP = {
      svin: new RegExp('svin|gris|flæsk|bacon|medister|skinke|chorizo|salsiccia|spegepølse|salami|pølse|spareribs|ribbensteg|nakkefilet|nakkesteg|nakkekam|kamsteg|kamkotelet|svinemedaljon|pulled pork|hamburgerryg'),
      okse: new RegExp('okse|bøf|entrecote|ribeye|roastbeef|culotte|flanksteak|tyksteg|tyndsteg|kalv|osso buco|gullasch'),
      fjerkrae: new RegExp('kylling|kalkun|andebryst|andelår|vildand|canette|fasan|høne|fjerkræ'),
      fisk: new RegExp('laks|torsk|rejer|sild|fisk|rødspætte|makrel|skaldyr|ansjos|alaska|hellefisk|rogn'),
      vegetar: new RegExp(KOEDORD + '|(?<![a-zæøå])lam(?![a-zæøå])|(?<![a-zæøå])tun(?!ge)'),
      loeg: new RegExp('løg|skalotte|porre'),
      svampe: new RegExp('champignon|svamp|portobello|østershat|shiitake'),
      mejeri: new RegExp('(?<!kokos)(?<!havre)mælk|fløde|ost(?![a-zæøå])|mozzarella|feta|parmesan|parmigiano|reggiano|pecorino|grana|cheddar|gouda|havarti|emmentaler|danbo|brie|camembert|halloumi|ricotta|gorgonzola|mascarpone|smør|yoghurt|skyr|creme fraiche|kefir|ymer|paneer'),
      aeg: new RegExp('(?<![a-zæøå])æg(?![a-zæøå])|æggekage|omelet|spejlæg|æggeblomme|frittata'),
    };
    let tjekket = 0; const sprunget = [];
    for (const b of Object.keys(data.butikker)) for (const f of FRAVALG) {
      state.fravalg = [f.id]; const lst = pool([b]);
      if (fravalgFejl) { sprunget.push(b + ':' + f.id); continue; }  // for få retter: fravalget bruges ikke (det er meningen)
      tjekket++;
      for (const r of lst) {
        const ord = [r.navn, ...r.ingredienser.map(i => i.navn)].map(x => x.toLowerCase());
        const ramt = ord.find(x => INDEP[f.id].test(x) && !(f.id === 'vegetar' && r.kategori === 'vegetar' && !ord.slice(1).some(y => INDEP.vegetar.test(y))));
        if (ramt && fejl.length < 40) fejl.push(b + ': fravalg ' + f.id + ' lader "' + r.navn + '" slippe igennem (' + ramt + ')');
      }
    }
    state.fravalg = [];
    if (tjekket < 20) fejl.push('for få fravalg kunne afprøves over puljen (' + tjekket + ')');
    rapport.puljetjek = { tjekket, sprunget: sprunget.length };
    for (const b of Object.keys(data.butikker)) {
      state.fravalg = []; state.budget = 0;
      const basis = plan(b), igen = plan(b);
      if (JSON.stringify(basis) !== JSON.stringify(igen)) fejl.push(b + ': samme valg giver ikke samme uge');
      if (basis.dage !== 7) fejl.push(b + ': basisugen har ' + basis.dage + ' retter');
      state.fravalg = ['svin'];
      const svin = plan(b);
      if (svin.dage !== 7) fejl.push(b + ': uge uden svinekød har ' + svin.dage + ' retter');
      const brud = svin.ids.filter(id => indeholder(id, SVIN));
      if (brud.length) fejl.push(b + ': fravalg svin gav retter med svinekød: ' + brud.map(id => ret(id).navn).join('; '));
      state.fravalg = [];
      for (const bud of [1, 400, 500, 600, basis.ialt, basis.ialt + 1, 100000]) {
        state.budget = bud; const q = plan(b);
        if (q.dage !== 7) fejl.push(b + ': uge med budget ' + bud + ' har ' + q.dage + ' retter');
        if (q.ialt > basis.ialt) fejl.push(b + ': budget ' + bud + ' gjorde ugen dyrere (' + q.ialt + ' mod ' + basis.ialt + ')');
        if (bud >= basis.ialt && JSON.stringify(q) !== JSON.stringify(basis)) fejl.push(b + ': et budget over prisen ændrede ugen (' + bud + ')');
      }
      state.budget = 0;
      state.fravalg = FRAVALG.map(f => f.id);
      let alt; try { alt = plan(b); } catch (e) { fejl.push(b + ': alle fravalg fik forslaget til at fejle: ' + e.message); }
      if (alt && alt.dage !== 7) fejl.push(b + ': alle fravalg gav ' + alt.dage + ' retter');
      pool([b]); if (!fravalgFejl) fejl.push(b + ': alle fravalg burde give besked om for få retter');
      state.fravalg = [];
      rapport[b] = { basis: basis.ialt, svin: svin.ialt, bud500: (state.budget = 500, plan(b).ialt) };
      state.budget = 0;
    }
    state.fravalg = []; state.budget = 0;
    return { fejl, rapport };
  })()`, 'fravalg_budget');
  if (ud.fejl.length) { console.log('FEJL:\n' + ud.fejl.slice(0, 30).join('\n')); process.exit(1); }
  console.log('FRAVALG_BUDGET: BESTÅET (' + (Object.keys(ud.rapport).length - 1) + ' butikker, ' + ud.rapport.puljetjek.tjekket + ' fravalg-kombinationer over hele puljen)');
})().catch(e => { console.error('FEJL: ' + (e && e.stack || e)); process.exit(2); });
