// Browsertest af "Hvor handler du?" og sammenligningen (BACKLOG "Sammenlign butikker", "Ét kort" og "Én regel for to butikker"), kørt INDE på siden i Chromium.
// Bruges af scripts/tests/sammenlign_browser.py (Playwright). Udtrykket evalueres som et løfte og giver JSON: { fejl: [...], maal: {...} }.
// Kortet køres rigtigt (asynkront, med DOM); tallene i DOM sammenlignes med sidens egne prisfunktioner.
(async () => {
  const fejl = [], maal = {};
  const vent = ms => new Promise(r => setTimeout(r, ms));
  const lange = []; let po = null;
  try { po = new PerformanceObserver(l => l.getEntries().forEach(e => lange.push({ start: e.startTime, ms: Math.round(e.duration) }))); po.observe({ type: 'longtask' }); } catch (e) { fejl.push('PerformanceObserver longtask findes ikke'); }
  const ventPaaKort = async () => { for (let i = 0; i < 240; i++) { if (SAMM.sig === simSig() && SAMM.faerdig && !SAMM.koerer) return true; /* færdig for netop denne husstand, ikke den forrige */ await vent(250); } return false; };
  const tekst = el => (el ? el.textContent : '').replace(/\s+/g, ' ').trim();
  const kombiTjek = [];
  // Kortets beregning for én husstand, målt: skiftet af husstand sker i testens egen opgave (som et klik) og måles ikke; alt bagefter måles.
  const maalHusstand = async (v, bo) => {
    saetHusstand(v, bo); opdaterHusstand(); const t0 = performance.now(); await vent(0);
    if (state.trin !== 'butik' || !document.getElementById('samm-kort')) return { fejl: 'kortet "Sammenlign butikker" vises ikke på forsiden' };
    if (!(await ventPaaKort())) return { fejl: 'kortet blev ikke færdigt inden for 60 s' };
    await vent(300);
    const efter = lange.filter(e => e.start >= t0).map(e => e.ms);
    return { ms: efter.length ? Math.max(...efter) : 0 };
  };
  for (const [v, bo] of [[2, 2], [2, 0], [1, 0]]) {
    const H = v + '+' + bo;
    let m = await maalHusstand(v, bo);
    if (m.fejl) { fejl.push(H + ': ' + m.fejl); continue; }
    maal[H] = { laengsteOpgaveMs: m.ms };
    // Én beregning af en enkelt uge (simFraButikker) kan ikke deles op uden at ændre motoren, og en GC-pause midt i den kan
    // give en enkelt lang opgave – det ses også på main uden kortet. Derfor måles én gang til; begge tal vises, og testen fejler, hvis begge er over 200 ms.
    if (m.ms > 200) {
      const [v2, b2] = v === 1 ? [2, 0] : [1, 0]; await maalHusstand(v2, b2);
      const m2 = await maalHusstand(v, bo);
      maal[H].andenMaalingMs = m2.ms;
      if (m2.fejl || m2.ms > 200) fejl.push(H + ': hovedtråden blokeret ' + m.ms + ' og ' + (m2.ms ?? '?') + ' ms i to målinger (krav: højst 200)');
    }
    // (1)+(2): rækkernes priser i DOM = sidens pris for butikken alene, billigst først
    const raekker = [...document.querySelectorAll('#samm-kort .samm-raekke')];
    if (raekker.length !== Object.keys(data.butikker).length) fejl.push(H + ': ' + raekker.length + ' rækker, forventet ' + Object.keys(data.butikker).length);
    const vistePriser = [];
    for (const r of raekker) {
      const k = r.dataset.sammvalg, forvent = kr(Math.round(sammButikTal(k).ialt)), vist = tekst(r.querySelector('.samm-pris span:last-child'));
      if (!udloebet(data.butikker[k])) { if (vist !== forvent) fejl.push(H + ' ' + k + ': rækken viser "' + vist + '", sidens pris er "' + forvent + '"'); vistePriser.push(Math.round(sammButikTal(k).ialt)); }
    }
    for (let i = 1; i < vistePriser.length; i++) if (vistePriser[i] < vistePriser[i - 1]) fejl.push(H + ': rækkerne er ikke billigst først');
    if (!document.querySelector('#samm-kort .samm-billigst')) fejl.push(H + ': ingen række er markeret "Billigst"');
    if (!tekst(document.getElementById('samm-status')).includes('7 aftensmåltider til ' + husstandTekst(v, bo))) fejl.push(H + ': kortet siger ikke "7 aftensmåltider til ' + husstandTekst(v, bo) + '"');
    // Én regel: kombinationen i DOM = den billigste uge blandt parrene (de 5 billigste), som er mindst ANBEFAL_SPAR billigere end den billigste enkeltbutik
    const { enkeltButik, top } = sammKombiKandidater(); let forvent = null;
    for (let i = 0; i < top.length; i++) for (let j = i + 1; j < top.length; j++) {
      const t = sammKombiTal([top[i], top[j]], enkeltButik);
      if (t && t.anbefalet && (!forvent || t.pris < forvent.pris)) forvent = t;
    }
    const kombiTekst = tekst(document.getElementById('samm-kombi-plads'));
    maal[H].kombi = forvent ? forvent.butikker.join('+') + ' ' + forvent.vist.pris + ' kr, spar ' + forvent.spar : 'ingen';
    if (!forvent && kombiTekst) fejl.push(H + ': kortet viser en kombination, som ikke sparer nok: ' + kombiTekst.slice(0, 120));
    if (forvent) {
      for (const tal of [forvent.spar, forvent.vist.pris, forvent.vist.enkelt]) if (!kombiTekst.includes(kr(tal))) fejl.push(H + ': kombinationsteksten mangler ' + kr(tal) + ' ("' + kombiTekst.slice(0, 160) + '")');
      if (!/Transport og ekstra tid er ikke regnet med/.test(kombiTekst)) fejl.push(H + ': kombinationsteksten siger ikke, at transport ikke er regnet med');
      kombiTjek.push([v, bo, forvent]);  // trykket på kombiknappen tjekkes efter tidsmålingerne (det vælger 2 butikker og ville påvirke næste måling)
    }
    // (5): 390 px uden vandret scroll, tryk-flader i kortet mindst 44 px
    if (document.documentElement.scrollWidth > innerWidth + 1) fejl.push(H + ': vandret scroll (' + document.documentElement.scrollWidth + ' > ' + innerWidth + ')');
    for (const b of document.querySelectorAll('#samm-kort button')) {
      const r = b.getBoundingClientRect();
      if (r.width && r.height && (r.height < 44 || r.width < 44)) fejl.push(H + ': tryk-flade ' + Math.round(r.width) + '×' + Math.round(r.height) + ' px: "' + tekst(b).slice(0, 40) + '"');
    }
  }
  // ===== Hjælpere til resten af testen =====
  const synlig = el => !!el && !el.closest('[hidden]') && el.getBoundingClientRect().height > 0;
  const enButik = k => { state.butikker = [k]; state.maxButikker = 0; state.koebButikker = []; renderButikker(); };
  const raekke = k => document.querySelector('.samm-raekke[data-sammvalg="' + CSS.escape(k) + '"]');
  // Én regel: tryk på kombiknappen → "Hvor mange butikker" anbefaler 2 butikker til samme pris, og madplanen koster det samme
  for (const [v, bo, forvent] of kombiTjek) {
    const H = v + '+' + bo;
    saetHusstand(v, bo); opdaterHusstand(); await vent(0); await ventPaaKort();
    enButik(forvent.enkeltButik); await vent(300); await ventPaaKort(); await vent(300);  // start fra den billigste enkeltbutik alene
    const knap = document.querySelector('[data-sammkombi]');
    if (!knap || knap.dataset.sammkombi !== forvent.butikker.join('+')) { fejl.push(H + ': kombiknappen mangler eller gælder ' + (knap && knap.dataset.sammkombi)); continue; }
    if (forvent.butikker.includes(forvent.enkeltButik) && !/^Tilføj /.test(tekst(knap))) fejl.push(H + ': knappen burde tilbyde at tilføje den anden butik, men siger "' + tekst(knap) + '"');
    knap.click(); await vent(2500);
    if (state.butikker.slice().sort().join('+') !== forvent.butikker.join('+')) fejl.push(H + ': kombiknappen valgte ' + JSON.stringify(state.butikker));
    const anbKnap = [...document.querySelectorAll('#antal-plads .antal-knap')].find(b => b.querySelector('.anbef'));
    if (!anbKnap || !/2 butikker/.test(tekst(anbKnap)) || !tekst(anbKnap).includes(kr(forvent.vist.pris))) fejl.push(H + ': efter kombiknappen anbefaler "Hvor mange butikker" ikke 2 butikker til ' + kr(forvent.vist.pris) + ' ("' + tekst(anbKnap) + '")');
    const pk2 = simK();
    if (!pk2 || Math.round(simPrisPlan(pk2).ialt) !== forvent.vist.pris) fejl.push(H + ': efter kombiknappen koster madplanen ' + (pk2 ? Math.round(simPrisPlan(pk2).ialt) : '?') + ' kr, kortet sagde ' + kr(forvent.vist.pris));
    if (document.querySelector('#samm-kombi-plads .samm-kombi')) fejl.push(H + ': forslaget vises stadig, selv om parret er valgt');
    maal[H].kombiKnap = anbKnap ? tekst(anbKnap) : '(ingen anbefaling)';
  }
  // ===== Ét kort, flere butikker med et tryk (BACKLOG "Ét kort": accept 1, 3, 4, 5, 6) =====
  saetHusstand(2, 2); opdaterHusstand(); await vent(50); await ventPaaKort();
  const foerste = sammKombiKandidater().ok[0] || Object.keys(data.butikker)[0];
  enButik(foerste); await vent(800);
  // (1) kun ét kort om butiksvalg; intet logo-gitter; "Hvor mange butikker" først, når der er valgt flere
  const h2 = [...document.querySelectorAll('h2')].map(h => tekst(h));
  if (h2.filter(t => t === 'Hvor handler du?').length !== 1) fejl.push('Ét kort: "Hvor handler du?" står ' + h2.filter(t => t === 'Hvor handler du?').length + ' gange');
  if (h2.some(t => /Sammenlign butikker/.test(t))) fejl.push('Ét kort: der er stadig en separat overskrift "Sammenlign butikker"');
  if (!document.querySelector('.butikpanel #samm-kort')) fejl.push('Ét kort: listen ligger ikke i kortet "Hvor handler du?"');
  if (document.querySelector('.butik-chip')) fejl.push('Ét kort: logo-gitteret findes stadig (butikkerne skal vælges i listen)');
  if (document.querySelector('[data-flere-butikker]')) fejl.push('Ét kort: der er stadig en særskilt knap for at vælge flere butikker');
  if (synlig(document.getElementById('antal-plads'))) fejl.push('Ét kort: "Hvor mange butikker" vises, selv om der kun er valgt én butik');
  // (5) madplanen starter mindst 300 px højere på 390 px end på main (main 2026-11-16: overskriften "Madplan" ved 1056 px, én butik valgt)
  if (innerWidth <= 400) {
    // Et to-butiks-forslag afhænger af ugens tilbud og gør kortet højere; det fandtes ikke i main's måling (1056 px). Dets højde trækkes fra, og begge tal vises.
    const top = Math.round(document.getElementById('sim-plads').getBoundingClientRect().top + scrollY);
    const kombiEl = document.querySelector('#samm-kombi-plads .samm-kombi'), kombiH = kombiEl ? Math.round(kombiEl.getBoundingClientRect().height + 12) : 0;
    maal.madplanTop390 = top; maal.toButiksForslagPx = kombiH;
    if (top - kombiH > 756) fejl.push('Ét kort: madplanen starter ' + (top - kombiH) + ' px nede uden to-butiks-forslaget (krav: højst 756 px, dvs. 300 px højere end main)');
  }
  // (6) rundvisningen: trin 2 = listen; et trin må kun pege på noget skjult, hvis det er "Hvor mange butikker" (springes over ved én butik)
  if (INTRO_TRIN[1].sel !== '#samm-plads') fejl.push('Rundvisning: trin 2 peger på ' + INTRO_TRIN[1].sel);
  for (const [i, t] of INTRO_TRIN.entries()) if (!synlig(document.querySelector(t.sel)) && t.sel !== '#antal-plads') fejl.push('Rundvisning: trin ' + (i + 1) + ' (' + t.sel + ') findes ikke eller er skjult');
  // (3)+(4) et tryk på en butik mere = flueben på begge; "Hvor mange butikker" dukker op; et tryk igen fjerner den
  const anden = sammOrden().find(k => k !== foerste && !udloebet(data.butikker[k]));
  raekke(anden).click(); await vent(2500);
  if (state.butikker.length !== 2 || !state.butikker.includes(foerste) || !state.butikker.includes(anden)) fejl.push('Flere butikker: tryk på ' + anden + ' gav ' + JSON.stringify(state.butikker) + ' (forventet begge)');
  if (raekke(anden).getAttribute('aria-pressed') !== 'true' || raekke(foerste).getAttribute('aria-pressed') !== 'true') fejl.push('Flere butikker: begge rækker skal have flueben');
  if (!synlig(document.getElementById('antal-plads')) || !/2 butikker/.test(tekst(document.getElementById('antal-plads')))) fejl.push('Flere butikker: "Hvor mange butikker" viser ikke 2 butikker efter et tryk på en butik mere');
  if (document.querySelectorAll('.kalender .dag-kort').length !== 7) fejl.push('Flere butikker: madplanen har ikke 7 dage');
  raekke(anden).click(); await vent(2500);
  if (state.butikker.length !== 1 || state.butikker[0] !== foerste) fejl.push('Flere butikker: et tryk igen fjernede ikke ' + anden + ' (' + JSON.stringify(state.butikker) + ')');
  if (synlig(document.getElementById('antal-plads'))) fejl.push('Flere butikker: "Hvor mange butikker" vises stadig med én butik');
  const pk = simK(); if (!pk || Math.round(simPrisPlan(pk).ialt) !== Math.round(sammButikTal(foerste).ialt)) fejl.push('Én butik igen: madplanen koster ' + (pk ? Math.round(simPrisPlan(pk).ialt) : '?') + ' kr, rækken ' + Math.round(sammButikTal(foerste).ialt) + ' kr');
  // en valgt butik skjules aldrig af "Vis alle" (telefon viser 3 rækker)
  const sidste = sammOrden().filter(k => !udloebet(data.butikker[k])).slice(-1)[0];
  SAMM.alle = true; sammenlignTegn(); await vent(100); raekke(sidste).click(); await vent(2500);
  SAMM.alle = false; sammenlignTegn(); await vent(100);
  if (innerWidth <= 400 && !synlig(raekke(sidste))) fejl.push('Vis alle: den valgte butik ' + sidste + ' er skjult, når listen er foldet sammen');
  raekke(sidste).click(); await vent(2000);
  // Jonas 2026-11-16 ("vælger jeg SPAR også, står der stadig bare Lidl"): en valgt butik, som madplanen ikke bruger, skal sige det selv,
  // og under listen står én klar sætning i stedet for en ensom "1 butik"-knap. Testen finder selv en butik, der ikke gør ugen billigere.
  enButik(foerste); await vent(300);
  let fundet = null;
  for (const k of sammOrden().filter(x => x !== foerste && !udloebet(data.butikker[x])).reverse()) {
    raekke(k).click(); for (let n = 0; n < 40 && manglerSim(); n++) await vent(250); await vent(600);
    if (kunEnMulighed()) { fundet = k; break; }
    // flere butikker kan betale sig her: så skal valget 1/2 butikker vises, og forklaringen ikke
    if (!document.querySelector('#antal-plads .antal-knap')) fejl.push('Flere butikker (' + foerste + '+' + k + '): valget 1/2 butikker vises ikke');
    raekke(k).click(); for (let n = 0; n < 40 && manglerSim(); n++) await vent(250); await vent(300);
  }
  if (!fundet) fejl.push('Ubrugt butik: fandt ingen butik, der ikke gør ugen billigere sammen med ' + foerste + ' (kan ikke afprøves med disse data)');
  else {
    const ap = document.getElementById('antal-plads'), np = document.getElementById('note-plads'), brugt = simStandard(simK()).butikker;
    if (!raekke(fundet).classList.contains('ubrugt') || !/Ikke med i madplanen/.test(tekst(raekke(fundet)))) fejl.push('Ubrugt butik: rækken for ' + fundet + ' siger ikke, at den ikke er med i madplanen ("' + tekst(raekke(fundet)) + '")');
    if (!tekst(ap).includes('Madplanen bruger kun ' + butikTekst(brugt)) || !tekst(ap).includes(kr(Math.round(simPrisPlan(simK()).ialt)))) fejl.push('Ubrugt butik: under listen står ikke "Madplanen bruger kun ' + butikTekst(brugt) + '" med prisen ("' + tekst(ap).slice(0, 120) + '")');
    if (ap.querySelector('.antal-knap')) fejl.push('Ubrugt butik: der står en ensom "1 butik"-knap');
    if (tekst(np)) fejl.push('Ubrugt butik: forklaringen står to gange ("' + tekst(np) + '")');
    maal.ubrugtButik = foerste + '+' + fundet + ': ' + tekst(ap).slice(0, 70);
    raekke(fundet).click(); await vent(1500);
    if (raekke(fundet).classList.contains('ubrugt')) fejl.push('Ubrugt butik: markeringen bliver hængende, efter butikken er fravalgt');
  }
  // Fejlvisning: uden priser kan man stadig vælge butikker i listen
  enButik(foerste); await vent(300);
  SAMM.fejlAlle = true; sammenlignTegn(); await vent(100);
  const ft = tekst(document.getElementById('samm-status'));
  if (/ovenfor|nedenfor/.test(ft)) fejl.push('Fejlvisning: teksten peger på et sted ("' + ft + '")');
  if (document.querySelectorAll('#samm-kort .samm-raekke').length !== Object.keys(data.butikker).length) fejl.push('Fejlvisning: listen med butikker vises ikke, så man ikke kan vælge ("' + ft + '")');
  SAMM.fejlAlle = false; SAMM.sig = null;
  enButik(foerste); await vent(300);
  if (po) po.disconnect();
  return JSON.stringify({ fejl, maal });
})()
