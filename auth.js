// Login med e-mail og adgangskode via Supabase (https://supabase.com).
// Udfyld url og anonKey fra Supabase → Project Settings → API. anonKey er offentlig og må gerne stå her.
// Så længe de er tomme, kører siden uden login.
const AUTH = {
  url: 'https://vppbimvewavvduwwcuwp.supabase.co',
  anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZwcGJpbXZld2F2dmR1d3djdXdwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTM2NDY1NDEsImV4cCI6MjEwOTIyMjU0MX0.WN96TpMaan1MC74-dCpFhfzh2wMeSlElpKH4Oo2XkXI',
};

let sb = null;      // Supabase-klient
let bruger = null;  // den indloggede bruger

const FEJLTEKST = [
  [/invalid login credentials/i, 'Forkert e-mail eller adgangskode.'],
  [/user already registered/i, 'Der findes allerede en bruger med den e-mail. Prøv at logge ind.'],
  [/at least 6 characters|password should be/i, 'Adgangskoden skal være mindst 6 tegn.'],
  [/email not confirmed/i, 'Du skal bekræfte din e-mail først – tjek din indbakke (og spam).'],
  [/rate limit|too many/i, 'For mange forsøg. Vent et par minutter og prøv igen.'],
  [/invalid email|unable to validate email/i, 'E-mailadressen ser ikke rigtig ud.'],
];
const dansk = fejl => (FEJLTEKST.find(([m]) => m.test(fejl?.message || '')) || [, fejl?.message || 'Noget gik galt.'])[1];

// Login er valgfrit: man kan bruge siden frit og logger først ind, når man vil gemme sin madplan.
async function startAuth(fortsaet) {
  if (!AUTH.url || !AUTH.anonKey || !window.supabase) return fortsaet();  // login er ikke sat op endnu
  sb = window.supabase.createClient(AUTH.url, AUTH.anonKey);

  sb.auth.onAuthStateChange((event, session) => {
    bruger = session?.user || null;
    if (event === 'PASSWORD_RECOVERY') visLogin('nyt');  // brugeren kom fra "nulstil adgangskode"-mailen
  });

  const { data } = await sb.auth.getSession();
  bruger = data.session?.user || null;
  visBruger();
  fortsaet();
  if (location.hash.includes('type=recovery')) visLogin('nyt');
}

function visBruger() {
  const el = document.getElementById('bruger');
  if (!el) return;
  el.innerHTML = bruger
    ? `<span>${esc(bruger.email)}</span> <button class="chip" id="logud">Log ud</button>`
    : `<button class="chip" data-aabn-login data-fane="ind">Log ind</button> <button class="chip aktiv" data-aabn-login data-fane="opret">Opret gratis bruger</button>`;
}

// ---------- Login-vindue (åbnes når man vil gemme, eller via knapperne i toppen) ----------
let loginEkstra = {};  // { titel, tekst } – fx når man vil gemme sin madplan

function sikrLoginVindue() {
  if (document.getElementById('login-vindue')) return;
  const st = document.createElement('style');
  st.textContent = `
    #login-vindue { position: fixed; inset: 0; z-index: 90; display: none; align-items: flex-start; justify-content: center; overflow-y: auto;
      background: rgba(5,8,16,.78); padding: 24px 16px; }
    #login-vindue.aaben { display: flex; }
    #login-vindue .login-boks { margin: 6vh auto; position: relative; width: 100%; }
    #login-vindue .luk-x { position: absolute; top: 10px; right: 14px; background: none; border: 0; color: var(--text-3, #A0A0A0); font-size: 24px; cursor: pointer; line-height: 1; }
    #login-vindue .login-fordele { margin: 8px 0 4px; padding-left: 18px; font-size: 14px; color: var(--text-2, #D4D4D4); }
    #login-vindue .login-fordele li { margin: 3px 0; }
    #login-vindue .login-fod { margin-top: 12px; font-size: 12px; color: var(--text-3, #A0A0A0); }
    #login-vindue .login-fod a { color: var(--emerald, #10B981); }`;
  document.head.appendChild(st);
  const v = document.createElement('div');
  v.id = 'login-vindue';
  v.addEventListener('click', e => { if (e.target === v) lukLogin(); });
  document.body.appendChild(v);
}

function lukLogin() {
  document.getElementById('login-vindue')?.classList.remove('aaben');
  document.body.style.overflow = '';
}

function visLogin(fane = 'ind', besked = '', ekstra) {
  if (ekstra) loginEkstra = ekstra;
  sikrLoginVindue();
  const titel = loginEkstra.titel || { ind: 'Log ind', opret: 'Opret gratis bruger', glemt: 'Glemt adgangskode', nyt: 'Vælg ny adgangskode' }[fane];
  const felter = {
    ind: `<input id="l-mail" type="email" placeholder="E-mail" autocomplete="email" required>
          <input id="l-pw" type="password" placeholder="Adgangskode" autocomplete="current-password" required>`,
    opret: `<input id="l-mail" type="email" placeholder="E-mail" autocomplete="email" required>
            <input id="l-pw" type="password" placeholder="Adgangskode (mindst 6 tegn)" autocomplete="new-password" minlength="6" required>
            <input id="l-pw2" type="password" placeholder="Gentag adgangskode" autocomplete="new-password" minlength="6" required>`,
    glemt: `<input id="l-mail" type="email" placeholder="E-mail" autocomplete="email" required>`,
    nyt: `<input id="l-pw" type="password" placeholder="Ny adgangskode (mindst 6 tegn)" autocomplete="new-password" minlength="6" required>`,
  }[fane];
  const knap = { ind: 'Log ind', opret: 'Opret gratis bruger', glemt: 'Send link', nyt: 'Gem adgangskode' }[fane];
  const intro = loginEkstra.tekst || (fane === 'ind' ? 'Log ind for at se din gemte madplan.' : '');

  const v = document.getElementById('login-vindue');
  v.innerHTML = `
    <div class="login-boks">
      <button class="luk-x" data-luk-login aria-label="Luk">×</button>
      <h2>${esc(titel)}</h2>
      ${intro ? `<p class="detalje">${esc(intro)}</p>` : ''}
      ${fane === 'opret' ? `<ul class="login-fordele"><li>Find dine valgte retter og din indkøbsliste igen hele ugen</li>
        <li>Se din ugeplan på både telefon og computer</li><li>Det er gratis, og du kan slette dine valg når som helst</li></ul>` : ''}
      ${fane !== 'nyt' ? `<div class="login-faner">
        <button class="chip ${fane === 'opret' ? 'aktiv' : ''}" data-login-fane="opret">Opret gratis bruger</button>
        <button class="chip ${fane === 'ind' ? 'aktiv' : ''}" data-login-fane="ind">Log ind</button>
      </div>` : ''}
      <form id="login-form" data-fane="${fane}">
        ${felter}
        <button class="knap" type="submit">${knap}</button>
      </form>
      <p id="login-besked" class="${besked.startsWith('✓') ? 'ok' : 'fejl'}">${esc(besked)}</p>
      ${fane === 'ind' ? '<button class="link" data-login-fane="glemt">Glemt adgangskode?</button>' : ''}
      ${fane === 'glemt' ? '<button class="link" data-login-fane="ind">← Tilbage til log ind</button>' : ''}
      ${fane !== 'nyt' ? '<button class="link" data-luk-login>Fortsæt uden at gemme</button>' : ''}
      <p class="login-fod">Når du opretter en bruger, gemmer vi din e-mail og dine valg. Læs <a href="/privatlivspolitik.html" target="_blank" rel="noopener">privatlivspolitikken</a>.</p>
    </div>`;
  v.classList.add('aaben');
  document.body.style.overflow = 'hidden';
  v.querySelector('#login-form input')?.focus();
}

document.addEventListener('keydown', e => { if (e.key === 'Escape') lukLogin(); });

document.addEventListener('click', async e => {
  const fane = e.target.closest('[data-login-fane]')?.dataset.loginFane;
  if (fane) return visLogin(fane);
  const aabn = e.target.closest('[data-aabn-login]');
  if (aabn) { loginEkstra = {}; return visLogin(aabn.dataset.fane || 'ind'); }
  if (e.target.closest('[data-luk-login]')) return lukLogin();
  if (e.target.id === 'logud') { await sb.auth.signOut(); location.reload(); }
});

document.addEventListener('submit', async e => {
  if (e.target.id !== 'login-form') return;
  e.preventDefault();
  const fane = e.target.dataset.fane;
  const mail = document.getElementById('l-mail')?.value.trim();
  const pw = document.getElementById('l-pw')?.value;
  const besked = t => { const el = document.getElementById('login-besked'); el.className = t.startsWith('✓') ? 'ok' : 'fejl'; el.textContent = t; };
  const knap = e.target.querySelector('button[type=submit]');
  knap.disabled = true;
  try {
    if (fane === 'ind') {
      const { error } = await sb.auth.signInWithPassword({ email: mail, password: pw });
      if (error) throw error;
      location.reload();
    } else if (fane === 'opret') {
      if (pw !== document.getElementById('l-pw2').value) throw new Error('De to adgangskoder er ikke ens.');
      const { data, error } = await sb.auth.signUp({ email: mail, password: pw, options: { emailRedirectTo: location.origin } });
      if (error) throw error;
      if (data.session) return location.reload();
      visLogin('ind', '✓ Næsten færdig! Vi har sendt en mail til ' + mail + ' – klik på linket for at bekræfte din bruger.');
    } else if (fane === 'glemt') {
      const { error } = await sb.auth.resetPasswordForEmail(mail, { redirectTo: location.origin });
      if (error) throw error;
      besked('✓ Hvis der findes en bruger med den e-mail, har vi sendt et link til at nulstille adgangskoden.');
    } else if (fane === 'nyt') {
      const { error } = await sb.auth.updateUser({ password: pw });
      if (error) throw error;
      history.replaceState(null, '', location.pathname);
      location.reload();
    }
  } catch (fejl) {
    besked(dansk(fejl));
  } finally {
    knap.disabled = false;
  }
});
