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

async function startAuth(fortsaet) {
  if (!AUTH.url || !AUTH.anonKey || !window.supabase) return fortsaet();  // login er ikke sat op endnu
  sb = window.supabase.createClient(AUTH.url, AUTH.anonKey);

  sb.auth.onAuthStateChange((event, session) => {
    bruger = session?.user || null;
    if (event === 'PASSWORD_RECOVERY') visLogin('nyt');  // brugeren kom fra "nulstil adgangskode"-mailen
  });

  const { data } = await sb.auth.getSession();
  bruger = data.session?.user || null;
  if (location.hash.includes('type=recovery')) return visLogin('nyt');
  if (bruger) { visBruger(); fortsaet(); }
  else visLogin('ind');
}

function visBruger() {
  document.body.classList.remove('kraever-login');
  const el = document.getElementById('bruger');
  if (el && bruger) el.innerHTML = `<span>${esc(bruger.email)}</span> <button class="chip" id="logud">Log ud</button>`;
}

function visLogin(fane = 'ind', besked = '') {
  document.body.classList.add('kraever-login');
  const titel = { ind: 'Log ind', opret: 'Opret bruger', glemt: 'Glemt adgangskode', nyt: 'Vælg ny adgangskode' }[fane];
  const felter = {
    ind: `<input id="l-mail" type="email" placeholder="E-mail" autocomplete="email" required>
          <input id="l-pw" type="password" placeholder="Adgangskode" autocomplete="current-password" required>`,
    opret: `<input id="l-mail" type="email" placeholder="E-mail" autocomplete="email" required>
            <input id="l-pw" type="password" placeholder="Adgangskode (mindst 6 tegn)" autocomplete="new-password" minlength="6" required>
            <input id="l-pw2" type="password" placeholder="Gentag adgangskode" autocomplete="new-password" minlength="6" required>`,
    glemt: `<input id="l-mail" type="email" placeholder="E-mail" autocomplete="email" required>`,
    nyt: `<input id="l-pw" type="password" placeholder="Ny adgangskode (mindst 6 tegn)" autocomplete="new-password" minlength="6" required>`,
  }[fane];
  const knap = { ind: 'Log ind', opret: 'Opret bruger', glemt: 'Send link', nyt: 'Gem adgangskode' }[fane];

  document.getElementById('indhold').innerHTML = `
    <div class="login-boks">
      <h2>${titel}</h2>
      <p class="detalje">Måltidsjagten – hjemmelavet mad ud fra ugens tilbud. Log ind for at komme i gang.</p>
      ${fane !== 'nyt' ? `<div class="login-faner">
        <button class="chip ${fane === 'ind' ? 'aktiv' : ''}" data-login-fane="ind">Log ind</button>
        <button class="chip ${fane === 'opret' ? 'aktiv' : ''}" data-login-fane="opret">Opret bruger</button>
      </div>` : ''}
      <form id="login-form" data-fane="${fane}">
        ${felter}
        <button class="knap" type="submit">${knap}</button>
      </form>
      <p id="login-besked" class="${besked.startsWith('✓') ? 'ok' : 'fejl'}">${esc(besked)}</p>
      ${fane === 'opret' ? '<p class="detalje">Når du opretter en bruger, gemmer vi din e-mail. Læs <a href="/privatlivspolitik.html" target="_blank" rel="noopener">privatlivspolitikken</a>.</p>' : ''}
      ${fane === 'ind' ? '<button class="link" data-login-fane="glemt">Glemt adgangskode?</button>' : ''}
      ${fane === 'glemt' ? '<button class="link" data-login-fane="ind">← Tilbage til log ind</button>' : ''}
    </div>`;
  document.getElementById('bund').classList.add('skjult');
  document.querySelector('#login-form input')?.focus();
}

document.addEventListener('click', async e => {
  const fane = e.target.closest('[data-login-fane]')?.dataset.loginFane;
  if (fane) return visLogin(fane);
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
