// Browsertest af "Sammenlign butikker" (BACKLOG accept 1, 2, 3, 4, 5, 9, 11), kørt INDE på siden i Chromium.
// Bruges af scripts/tests/sammenlign_browser.py (Playwright). Udtrykket evalueres som et løfte og giver JSON: { fejl: [...], maal: {...} }.
// Kortet køres rigtigt (asynkront, med DOM); tallene i DOM sammenlignes med sidens egne prisfunktioner.
(async () => {
  const fejl = [], maal = {};
  const vent = ms => new Promise(r => setTimeout(r, ms));
  const lange = []; let po = null;
  try { po = new PerformanceObserver(l => l.getEntries().forEach(e => lange.push({ start: e.startTime, ms: Math.round(e.duration) }))); po.observe({ type: 'longtask' }); } catch (e) { fejl.push('PerformanceObserver longtask findes ikke'); }
  const ventPaaKort = async () => { for (let i = 0; i < 240; i++) { if (SAMM.sig === simSig() && SAMM.faerdig && !SAMM.koerer) return true; /* færdig for netop denne husstand, ikke den forrige */ await vent(250); } return false; };
  const tekst = el => (el ? el.textContent : '').replace(/\s+/g, ' ').trim();
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
    // (9)+(11): kombinationen i DOM = den billigste uge blandt parrene (de 5 billigste), der sparer mindst ANBEFAL_SPAR mod både samme retter og enkeltbutikkens uge
    const { enkeltButik, top } = sammKombiKandidater(); let forvent = null;
    for (let i = 0; i < top.length; i++) for (let j = i + 1; j < top.length; j++) {
      const t = sammKombiTal([top[i], top[j]], enkeltButik);
      if (t && t.spar >= ANBEFAL_SPAR && (!forvent || t.vist.pris < forvent.vist.pris || (t.vist.pris === forvent.vist.pris && t.spar > forvent.spar))) forvent = t;
    }
    const kombiTekst = tekst(document.getElementById('samm-kombi-plads'));
    maal[H].kombi = forvent ? forvent.butikker.join('+') + ' ' + forvent.vist.pris + ' kr, spar ' + forvent.spar : 'ingen';
    if (!forvent && kombiTekst) fejl.push(H + ': kortet viser en kombination, som ikke sparer nok: ' + kombiTekst.slice(0, 120));
    if (forvent) {
      for (const tal of [forvent.spar, forvent.vist.pris, forvent.vist.sammeIEnkelt, forvent.vist.enkelt]) if (!kombiTekst.includes(kr(tal))) fejl.push(H + ': kombinationsteksten mangler ' + kr(tal) + ' ("' + kombiTekst.slice(0, 160) + '")');
      if (!/Transport og ekstra tid er ikke regnet med/.test(kombiTekst)) fejl.push(H + ': kombinationsteksten siger ikke, at transport ikke er regnet med');
    }
    // (5): 390 px uden vandret scroll, tryk-flader i kortet mindst 44 px
    if (document.documentElement.scrollWidth > innerWidth + 1) fejl.push(H + ': vandret scroll (' + document.documentElement.scrollWidth + ' > ' + innerWidth + ')');
    for (const b of document.querySelectorAll('#samm-kort button')) {
      const r = b.getBoundingClientRect();
      if (r.width && r.height && (r.height < 44 || r.width < 44)) fejl.push(H + ': tryk-flade ' + Math.round(r.width) + '×' + Math.round(r.height) + ' px: "' + tekst(b).slice(0, 40) + '"');
    }
  }
  // (3): et tryk på en række vælger butikken og opdaterer madplanen (2+2; den næstbilligste, så valget faktisk skifter)
  saetHusstand(2, 2); opdaterHusstand(); await vent(50); await ventPaaKort();
  const r2 = [...document.querySelectorAll('#samm-kort .samm-raekke')][1];
  if (r2) {
    const k = r2.dataset.sammvalg; r2.click(); await vent(1500);
    if (state.butikker.length !== 1 || state.butikker[0] !== k) fejl.push('tryk på ' + k + ' valgte ' + JSON.stringify(state.butikker));
    if (document.querySelectorAll('.kalender .dag-kort').length !== 7) fejl.push('efter tryk på ' + k + ' viser madplanen ' + document.querySelectorAll('.kalender .dag-kort').length + ' dage');
    const pk = simK(); if (pk && Math.round(simPrisPlan(pk).ialt) !== Math.round(sammButikTal(k).ialt)) fejl.push('efter tryk på ' + k + ' viser madplanen ' + Math.round(simPrisPlan(pk).ialt) + ' kr, rækken ' + Math.round(sammButikTal(k).ialt) + ' kr');
  } else fejl.push('ingen række at trykke på');
  if (po) po.disconnect();
  return JSON.stringify({ fejl, maal });
})()
