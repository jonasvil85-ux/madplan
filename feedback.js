// Feedback-chat nederst til højre: guider brugeren til at melde fejl og forslag, og gemmer dem i Supabase-tabellen "feedback".
// Det er en enkel, scriptet chat (ingen AI) – opret tabellen med SQL'en i scripts/feedback.sql.
(() => {
  const MAX_PR_TIME = 5;
  const TYPER = ['Mærkelig opskrift', 'Forkert vare på listen', 'Forkert pris eller tilbud', 'Forslag til forbedring', 'Andet'];
  const SPOERGSMAAL = {
    'Mærkelig opskrift': 'Hvilken ret er det, og hvad virker mærkeligt? (fx en ingrediens der ikke passer, forkert mængde eller noget der ikke er hjemmelavet)',
    'Forkert vare på listen': 'Hvilken vare er forkert, og hvad skulle det have været? (fx kylling i stedet for and, eller et tilbud der ikke passer til retten)',
    'Forkert pris eller tilbud': 'Hvilken butik og vare drejer det sig om, og hvad er forkert?',
    'Forslag til forbedring': 'Fortæl os gerne, hvad der ville gøre Måltidsjagten bedre for dig.',
    'Andet': 'Hvad vil du gerne fortælle os?',
  };

  const css = `
  #fb-knap { position: fixed; right: 18px; bottom: 18px; z-index: 60; width: 54px; height: 54px; border-radius: 50%; border: 0; cursor: pointer;
    background: #C9561E; color: #fff; font-size: 24px; box-shadow: 0 6px 20px rgba(0,0,0,.45); }
  #fb-knap:hover { filter: brightness(1.1); }
  body.har-bund #fb-knap { bottom: 86px; }
  @media (max-width: 700px) {
    #fb-knap { width: 46px; height: 46px; right: 12px; bottom: calc(10px + env(safe-area-inset-bottom, 0px)); }
    #fb-knap svg { width: 22px; height: 22px; }
    body.har-bund #fb-knap { bottom: 78px; }
    #fb-panel { right: 10px; bottom: 64px; }
  }
  #fb-panel { position: fixed; right: 18px; bottom: 84px; z-index: 61; width: min(360px, calc(100vw - 24px)); max-height: min(520px, calc(100vh - 110px));
    display: none; flex-direction: column; background: #1F1813; border: 1px solid #3A2D22; border-radius: 16px; box-shadow: 0 12px 40px rgba(0,0,0,.55); overflow: hidden; }
  #fb-panel.aaben { display: flex; }
  #fb-top { padding: 12px 14px; background: #2B211A; border-bottom: 1px solid #3A2D22; display: flex; align-items: center; justify-content: space-between; color: #fff; font-weight: 600; font-size: 14px; }
  #fb-top button { background: none; border: 0; color: #A0A0A0; font-size: 20px; cursor: pointer; line-height: 1; }
  #fb-log { flex: 1; overflow-y: auto; padding: 12px; display: flex; flex-direction: column; gap: 8px; font-size: 14px; }
  .fb-b { max-width: 88%; padding: 8px 12px; border-radius: 14px; line-height: 1.4; white-space: pre-wrap; word-wrap: break-word; }
  .fb-bot { background: #2B211A; color: #E5E7EB; align-self: flex-start; border-bottom-left-radius: 4px; }
  .fb-dig { background: #C9561E; color: #fff; align-self: flex-end; border-bottom-right-radius: 4px; }
  .fb-valg { display: flex; flex-wrap: wrap; gap: 6px; }
  .fb-valg button { background: #2B211A; border: 1px solid #43342A; color: #D4D4D4; padding: 6px 10px; border-radius: 999px; font-size: 13px; cursor: pointer; }
  .fb-valg button:hover { border-color: #E8743B; color: #fff; }
  #fb-form { display: none; gap: 8px; padding: 10px; border-top: 1px solid #3A2D22; background: #18120E; }
  #fb-form.aaben { display: flex; }
  #fb-felt { flex: 1; resize: none; background: #2B211A; color: #fff; border: 1px solid #43342A; border-radius: 10px; padding: 8px 10px; font: inherit; font-size: 16px; max-height: 110px; }
  #fb-send { background: #C9561E; border: 0; color: #fff; font-weight: 600; border-radius: 10px; padding: 0 14px; cursor: pointer; }
  #fb-send:disabled { opacity: .5; }
  #fb-fod { padding: 0 12px 10px; font-size: 11px; color: #A99A89; background: #18120E; }
  #fb-fod a { color: #E8743B; }
  .fb-hp { position: absolute; left: -9999px; width: 1px; height: 1px; opacity: 0; }
  `;
  document.head.appendChild(Object.assign(document.createElement('style'), { textContent: css }));

  const html = `
    <button id="fb-knap" type="button" aria-label="Giv feedback" title="Giv feedback"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22z"/></svg></button>
    <div id="fb-panel" role="dialog" aria-label="Feedback">
      <div id="fb-top"><span>Hjælp os med at blive bedre</span><button type="button" id="fb-luk" aria-label="Luk">×</button></div>
      <div id="fb-log"></div>
      <form id="fb-form" autocomplete="off">
        <input class="fb-hp" id="fb-hp" tabindex="-1" aria-hidden="true" placeholder="Lad stå tom">
        <textarea id="fb-felt" rows="2" maxlength="1500" placeholder="Skriv her…"></textarea>
        <button id="fb-send" type="submit">Send</button>
      </form>
      <div id="fb-fod">Skriv ikke personlige oplysninger. <a href="/privatlivspolitik.html" target="_blank" rel="noopener">Læs om hvordan vi bruger din feedback</a>.</div>
    </div>`;
  const rod = document.createElement('div');
  rod.innerHTML = html;
  document.body.appendChild(rod);

  const $ = id => document.getElementById(id);
  let trin = 'start';      // start -> besked -> mail -> faerdig
  let valg = null, besked = '';

  const boble = (tekst, hvem) => {
    const d = document.createElement('div');
    d.className = 'fb-b ' + (hvem === 'dig' ? 'fb-dig' : 'fb-bot');
    d.textContent = tekst;
    $('fb-log').appendChild(d);
    $('fb-log').scrollTop = $('fb-log').scrollHeight;
  };
  const valgknapper = (liste, ved) => {
    const d = document.createElement('div');
    d.className = 'fb-valg';
    liste.forEach(t => {
      const b = document.createElement('button');
      b.type = 'button'; b.textContent = t;
      b.onclick = () => { d.remove(); ved(t); };
      d.appendChild(b);
    });
    $('fb-log').appendChild(d);
    $('fb-log').scrollTop = $('fb-log').scrollHeight;
  };
  const visFelt = (vis, placeholder = 'Skriv her…', type = 'text') => {
    $('fb-form').classList.toggle('aaben', vis);
    $('fb-felt').placeholder = placeholder;
    $('fb-felt').dataset.type = type;
    if (vis) $('fb-felt').focus();
  };

  function start() {
    $('fb-log').innerHTML = '';
    trin = 'start'; valg = null; besked = '';
    visFelt(false);
    boble('Hej! Har du set en mærkelig opskrift, en forkert vare på listen eller noget andet, der kan blive bedre? Fortæl os det – vi læser alt og forsøger at gøre siden bedre.');
    boble('Hvad drejer det sig om?');
    valgknapper(TYPER, t => {
      valg = t;
      boble(t, 'dig');
      boble(SPOERGSMAAL[t]);
      trin = 'besked';
      visFelt(true, 'Skriv her…');
    });
  }

  function kontekst() {
    try {
      const s = typeof state !== 'undefined' ? state : {};
      const b = typeof B === 'function' && s.butik ? B() : null;
      const navne = (s.valgte || []).map(id => (b?.retter || []).find(r => r.id === id)?.navn).filter(Boolean).slice(0, 10);
      return { butik: s.butik || null, trin: s.trin || null, valgte_retter: navne, genereret: (typeof data !== 'undefined' && data?.genereret) || null,
               skaerm: innerWidth + 'x' + innerHeight };
    } catch { return {}; }
  }

  function tilladt() {
    const nu = Date.now();
    const log = JSON.parse(localStorage.getItem('madplan-fb') || '[]').filter(t => nu - t < 3600e3);
    return log.length < MAX_PR_TIME;
  }
  function husk() {
    const nu = Date.now();
    const log = JSON.parse(localStorage.getItem('madplan-fb') || '[]').filter(t => nu - t < 3600e3);
    log.push(nu);
    localStorage.setItem('madplan-fb', JSON.stringify(log));
  }

  async function send(email) {
    $('fb-send').disabled = true;
    visFelt(false);
    if ($('fb-hp').value) { boble('Tak for dit input!'); trin = 'faerdig'; return; }  // bot-fælde
    if (!tilladt()) { boble('Du har sendt mange beskeder på kort tid – prøv igen om lidt. Tak for din tålmodighed!'); trin = 'faerdig'; return; }
    try {
      if (!AUTH?.url || !AUTH?.anonKey) throw new Error('ingen forbindelse sat op');
      const svar = await fetch(AUTH.url + '/rest/v1/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', apikey: AUTH.anonKey, Authorization: 'Bearer ' + AUTH.anonKey, Prefer: 'return=minimal' },
        body: JSON.stringify({ type: valg, besked, email: email || null, kontekst: kontekst(), side: location.pathname }),
      });
      if (!svar.ok) throw new Error('HTTP ' + svar.status);
      husk();
      boble('Tak for dit input! Vi vil forsøge at implementere det. Jo mere konkret du var (hvilken ret, butik og vare), jo nemmere er det for os at rette.');
      boble('Har du mere på hjerte?');
      valgknapper(['Send en ny besked', 'Luk'], t => t === 'Luk' ? luk() : start());
    } catch (e) {
      boble('Hov, din besked kunne ikke sendes lige nu. Du kan i stedet skrive til jonasvilladsen@live.dk – og tak, fordi du ville hjælpe!');
    }
    trin = 'faerdig';
    $('fb-send').disabled = false;
  }

  $('fb-form').addEventListener('submit', e => {
    e.preventDefault();
    const tekst = $('fb-felt').value.trim();
    if (trin === 'besked') {
      if (tekst.length < 3) return;
      besked = tekst.slice(0, 1500);
      boble(besked, 'dig');
      $('fb-felt').value = '';
      trin = 'mail';
      boble('Tak! Vil du have svar? Skriv din e-mail herunder, eller tryk "Nej tak" – det er helt valgfrit.');
      visFelt(true, 'din@mail.dk', 'email');
      valgknapper(['Nej tak, send bare'], () => { boble('Nej tak, send bare', 'dig'); send(null); });
    } else if (trin === 'mail') {
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(tekst)) { boble('Den e-mail ser ikke helt rigtig ud – prøv igen, eller vælg "Nej tak".'); return; }
      boble(tekst, 'dig');
      $('fb-felt').value = '';
      send(tekst.slice(0, 200));
    }
  });
  $('fb-felt').addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); $('fb-form').requestSubmit(); }
  });

  function aabn() { $('fb-panel').classList.add('aaben'); if (!$('fb-log').children.length) start(); }
  function luk() { $('fb-panel').classList.remove('aaben'); }
  $('fb-knap').onclick = () => $('fb-panel').classList.contains('aaben') ? luk() : aabn();
  $('fb-luk').onclick = luk;

  // Hold knappen fri af den faste bundlinje (indkøbsliste m.m.), når den vises
  const bund = document.getElementById('bund');
  if (bund) new MutationObserver(() => document.body.classList.toggle('har-bund', !bund.classList.contains('skjult'))).observe(bund, { attributes: true, attributeFilter: ['class'] });
})();
