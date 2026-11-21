// Test af "Gode tilbud"-grupperne på indkøbslisten (BACKLOG [UX] "Gode tilbud-grupperne nederst på indkøbslisten"). Køres af kontrol.py (node, uden browser).
// Samme DOM-attrap, frosne ur og datakopi som sammenlign.js. Tjekker, at titlerne er avisens egen tekst (aldrig kun første alternativ), for alle varer i alle grupper og alle 9 butikker, og at den tegnede liste
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
      const titel = kortNavn(t.navn), fuld = versalNavn(t.navn);
      if (titel.length > 42) fejl.push(g + ': titel over 42 tegn: ' + titel);
      // Titlen er avisens egen tekst, aldrig et enkelt alternativ: afkortes den, er den et præfiks af hele teksten ved en ordgrænse
      if (titel.endsWith('…')) {
        const r = titel.slice(0, -1);
        if (!fuld.startsWith(r) || !/[\\s,;:–-]/.test(fuld.charAt(r.length) || ' ')) fejl.push(g + ': afkortet midt i et ord: ' + titel + ' <- ' + fuld);
      } else if (titel !== fuld) fejl.push(g + ': titlen er ændret uden afkortning: ' + titel + ' <- ' + fuld);
      if (/\\seller\\s/i.test(t.navn)) med++;
    }
    const prov = [['PEPSI MAX, FAXE KONDI ELLER COLA ZERO', 'Pepsi max, faxe kondi eller cola zero'], ['Starbucks eller Illy kaffekapsler', 'Starbucks eller Illy kaffekapsler'],
                  ['Daim, Oreo, Toblerone eller Philadelphia cheesecake', 'Daim, Oreo, Toblerone eller Philadelphia…'], ['Høker røget bacon', 'Høker røget bacon'],
                  ['Dan Cake juleromkugler, havregrynskugler, kryddermazarin og mere', 'Dan Cake juleromkugler, havregrynskugler…']];
    for (const [i, t] of prov) if (kortNavn(i) !== t) fejl.push('prøve "' + i + '": fik "' + kortNavn(i) + '", forventede "' + t + '"');
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
        // Afkryds en vare uden for de første rækker: foldet gruppe viser den stadig, og "Vis færre" lukker gruppen (virker også med afkrydset vare)
        if (s.linjer.length < EKSTRA_SYNLIGE + 2) continue;  // med 5 rækker og en valgt er intet skjult, så der er ingen knap
        const sidste = s.linjer[s.linjer.length - 1];
        state.valgtVare[sidste.key] = true;
        html = ''; renderListe(); const m1 = html;
        ekstraAaben.add(s.id); html = ''; renderListe(); const m2 = html; ekstraAaben.delete(s.id);
        const udsnit = (h) => { const q = h.indexOf('id="ekstra-' + s.id + '"'); return h.slice(q, h.indexOf('</button>', h.indexOf('ekstra-flere', q))); };
        const rk1 = (udsnit(m1).match(/class="vare liste-vare/g) || []).length, rk2 = (udsnit(m2).match(/class="vare liste-vare/g) || []).length;
        if (rk1 !== EKSTRA_SYNLIGE + 1) fejl.push(b + ' ' + s.id + ': foldet gruppe med afkrydset vare viser ' + rk1 + ' rækker, forventede ' + (EKSTRA_SYNLIGE + 1));
        if (rk2 !== s.linjer.length) fejl.push(b + ' ' + s.id + ': udfoldet gruppe med afkrydset vare viser ikke alle rækker');
        if (!udsnit(m1).includes('aria-expanded="false"') || !udsnit(m2).includes('Vis færre')) fejl.push(b + ' ' + s.id + ': "Vis færre" mangler/virker ikke med afkrydset vare');
        delete state.valgtVare[sidste.key];
      }
      const sum = Math.round(prisSum(Object.values(L).flat().filter(x => state.valgtVare[x.key])).ialt * 100) / 100;
      rapport[b] = { grupper: sek.map(s => s.linjer.length), sum };
    }
    const foldede = Object.values(rapport).flatMap(r => r.grupper).filter(n => n > EKSTRA_SYNLIGE).length;
    if (foldede < 10) fejl.push('kun ' + foldede + ' foldede grupper i alle butikker – foldningen er ikke testet');
    return { fejl, antal, med, rapport };
  })()`, 'grupper');
  if (ud.fejl.length) { console.log('FEJL:\n' + ud.fejl.slice(0, 30).join('\n')); process.exit(1); }
  console.log('GRUPPER: BESTÅET (' + ud.antal + ' varer, ' + ud.med + ' med alternativer; ' + Object.keys(ud.rapport).length + ' butikker; grupper ' + JSON.stringify(Object.fromEntries(Object.entries(ud.rapport).map(([b, r]) => [b, r.grupper.join('/')]))) + ')');
})().catch(e => { console.error('FEJL: ' + (e && e.stack || e)); process.exit(2); });
