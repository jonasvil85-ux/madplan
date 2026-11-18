# Sikkerhed – uge 47 (2026-11-18)

Sikkerhedsagentens første gennemgang. Ingen tidligere sikkerhedsrapport, og ingen tidligere anden mening om `[SIKKERHED]`-krav.
Gennemgået: hele arbejdstræet og hele git-historikken (363 commits efter `git fetch --unshallow`), `scripts/*.sql`, `auth.js`, `feedback.js`, `admin.html`, `index.html`, `sw.js`, `privatlivspolitik.html` og alle 8 workflows i `.github/workflows/`.

**Ikke tjekket** (ærligt):
- Den udgivne side: proxyen i skyen afviste forbindelsen til madplan-blue.vercel.app, så de faktiske HTTP-hoveder er ikke målt. At der mangler hoveder, er udledt af, at der ikke er nogen `vercel.json`.
- Supabase-projektet selv: om SQL-filerne faktisk er kørt, om "Confirm email", "Secure email change", lækket-adgangskode-beskyttelse og CAPTCHA er slået til, og om der findes andre tabeller eller politikker end dem i repoet.
- GitHub-indstillinger: grenbeskyttelse på `main`, hvem der har skriveadgang, og om Actions må godkende sig selv. Repoet er **offentligt** (bekræftet via GitHubs søge-API).

## Resumé
| Alvor | Antal |
|---|---|
| Kritisk | 0 |
| Høj | 2 |
| Middel | 5 |
| Lav | 5 |

Ingen hemmeligheder fundet i filer eller historik. Den eneste JWT i historikken er Supabase **anon**-nøglen (`auth.js:6`, rolle `anon`), som gerne må være offentlig. Ingen service-nøgle, GitHub-, Anthropic-, Cloudflare-, AWS- eller private nøgler. `scripts/agent_feedback.sql` indeholder kun pladsholderen, ikke selve hemmeligheden. Row level security er slået til på alle tre tabeller i repoet (`feedback`, `brugerdata`, `agent_noegle`), og `brugerdata` er korrekt låst til ejeren.

---

## Høj

### H1. Supabase-biblioteket hentes fra et CDN uden fast version og uden integritetstjek
**Bevis:** `index.html:968` og `admin.html:85`: `<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2">`. Kun hovedversionen er fastlåst (`@2`), og der er ingen `integrity=`. Der er heller ingen CSP, der kunne begrænse skaden (se M1).
**Risiko:** en kompromitteret eller fejlbehæftet udgivelse af pakken (eller af CDN'et) kører straks med fulde rettigheder på forsiden (brugernes login-sessioner og gemte data) og på admin-siden, som kan læse alle feedback-beskeder med e-mailadresser og brugerstatistik. Siden skifter desuden version uden test hver gang der udkommer en ny 2.x.
**Forslag:** læg en bestemt version af `supabase.js` (UMD-buildet) i repoet (fx `vendor/supabase-js-2.x.y.min.js`) og hent den derfra, eller fastlås den præcise version og tilføj `integrity="sha384-…"` og `crossorigin="anonymous"`. At hente den selv fjerner også en tredjepart fra privatlivspolitikken (se M4). Hæv `VERSION` i `sw.js`.
**Grundlov:** nej (`index.html`/`admin.html`). Klasse H (cache/sw.js og login-flowet).

### H2. Kontrollant-workflowet kører grenenes kode med Bash og hemmeligheder i samme job
**Bevis:** `.github/workflows/kontrollant.yml` linje 8–20 (udløses af `push` til `ai/**`; `permissions: contents: write, actions: write, issues: write`) og linje 63–72 (Claude Code kører med `--allowedTools Bash …`, mens `CLAUDE_CODE_OAUTH_TOKEN` og `GH_TOKEN` står i miljøet). Kontrollanten kører grenens egne tests (`kontrol.py`, node- og browsertests) i det miljø.
**Risiko:** kode på en udviklergren, eller en kontrollant-agent, der lader sig styre af tekst i grenen, kan læse miljøet og sende Jonas' private Claude-token eller GitHub-token ud, og med `actions: write` starte eller ændre andre workflows. Der er en lang, automatisk kæde fra fremmede til grenene: anonym feedback → Product Owner-AI → `ai/FEEDBACK.md` → Ejer → backlog → udvikler-agent → gren → kontrollant. Kun dem med skriveadgang kan pushe til `ai/**` (fork-push udløser ikke workflowet), og det trækker alvoren ned fra kritisk.
**Forslag:**
1. Del jobbet i to: et testjob uden hemmeligheder og med `permissions: contents: read`, der kører grenens kode og gemmer resultatet som artefakt; derefter et kontrollant-job, der læser resultatet.
2. Fjern `actions: write`, medmindre det er nødvendigt (skriv i workflowet hvorfor).
3. Sæt hemmelighederne kun på det trin, der bruger dem (det gøres allerede for nogle trin), og tilføj `persist-credentials: false` til `actions/checkout`, hvor der ikke skal pushes.
4. Slå grenbeskyttelse til på `main` (forbyd force-push og sletning), så selv et lækket token ikke kan omskrive historikken.
**Grundlov:** ja (`.github/`) – se "Forslag til grundloven".

---

## Middel

### M1. Ingen sikkerhedshoveder (ingen `vercel.json`)
**Bevis:** der er ingen `vercel.json` i roden, og ingen `<meta http-equiv="Content-Security-Policy">` i `index.html` eller `admin.html`. (Ikke målt på den udgivne side, se ovenfor.)
**Risiko:** login-vinduet og admin-siden kan indlejres i en fremmed side (clickjacking); intet loft over, hvilke scripts der må køre, hvis der sniger sig HTML ind (L1, H1); fuld henvisning (referrer) sendes til tredjeparter.
**Forslag:** en `vercel.json` med hoveder for alle stier:
- `Content-Security-Policy`: `default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net (fjernes efter H1); connect-src 'self' https://<projekt>.supabase.co https://<tilbudsbilleder>; img-src 'self' data: https:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self'`. Start evt. som `Content-Security-Policy-Report-Only` i en uge, og stram `'unsafe-inline'` senere.
- `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy: camera=(), microphone=(), geolocation=()`, `Strict-Transport-Security: max-age=63072000; includeSubDomains`.
- For `/admin.html`: `X-Robots-Tag: noindex` og `Cache-Control: no-store`.
Browser-QA skal bekræfte, at siden, login, feedback, billeder og Vercel Insights stadig virker.
**Grundlov:** nej. Klasse H (rører alle sider og cache-adfærd).

### M2. Feedback-tabellen er åben for skrivning uden loft over størrelse og hastighed
**Bevis:** `scripts/feedback.sql:14` – politikken `for insert to anon, authenticated with check (true)`. `kontekst jsonb` har ingen størrelsesgrænse, `type` er kun begrænset til 40 tegn (ikke de 5 kendte typer), og `email` har ikke noget formattjek. Grænsen på 5 beskeder i timen findes kun i browseren (`feedback.js:116–127`, `localStorage`), og den kan man komme uden om ved at kalde REST-adressen direkte med den offentlige anon-nøgle.
**Risiko:** hvem som helst kan fylde tabellen med store eller mange rækker (databasepladsen kan løbe fuld, og der kommer støj i admin og hos Product Owner-agenten). Følgefejl: `admin.html:147` kalder `k.valgte_retter.join(...)` uden at tjekke typen, så én række, hvor `valgte_retter` ikke er en liste, får hele beskedlisten i admin til at gå ned.
**Forslag:** nye check-regler: `pg_column_size(kontekst) <= 4000`, `jsonb_typeof(kontekst) = 'object'`, `type in (…de 5 typer…)`, et simpelt formattjek af e-mail. En hastighedsgrænse på serveren (fx en `before insert`-trigger, der afviser mere end N rækker i minuttet i alt, eller Supabase CAPTCHA/Turnstile via en Edge Function). I `admin.html`: `Array.isArray(k.valgte_retter)` før `.join`.
**Grundlov:** `feedback.js` er grundlov (kun hvis klienten skal ændres); SQL og `admin.html` er ikke.

### M3. Admin-adgangen kræver kun e-mail og adgangskode (mindst 6 tegn), ingen 2-trinsbekræftelse
**Bevis:** `scripts/admin.sql:11–23` giver adgang ud fra `auth.jwt() ->> 'email'`. `auth.js:83` (og Supabases standard) tillader adgangskoder på 6 tegn. Admin-e-mailen står offentligt i `admin.html:88`, `scripts/admin.sql` og privatlivspolitikken (det sidste er lovpligtigt), så kontoen er et kendt mål.
**Risiko:** gætter eller lækker man adgangskoden til den konto, kan man læse alle feedback-e-mails og brugerstatistik. At adgangen afgøres af e-mailen, hviler på, at "Confirm email" og "Secure email change" er slået til i Supabase (ikke tjekket).
**Forslag:** slå TOTP-2-trinsbekræftelse (MFA) til i Supabase for admin-kontoen og kræv `(auth.jwt() ->> 'aal') = 'aal2'` i begge admin-politikker og i `admin_statistik()`. Sammenlign med kontoens faste `auth.uid()` i stedet for e-mailen. Hæv mindstelængden til 8 tegn (Supabase → Auth → Passwords) og slå "Leaked password protection" til. Bekræft og noter, at "Confirm email" og "Secure email change" er slået til.
**Grundlov:** mindstelængden i `auth.js`-teksterne er grundlov; SQL og Supabase-indstillinger er ikke (men skal køres af Jonas i Supabase).

### M4. Privatlivspolitikken passer ikke længere med virkeligheden
**Bevis:** `privatlivspolitik.html` (opdateret 3. nov.) nævner kun Supabase og Vercel som modtagere. Men:
- feedback-tekster læses dagligt af en AI fra Anthropic (`.github/workflows/feedback-product-owner.yml`), og opsummeringer lægges i det **offentlige** repo (`ai/FEEDBACK.md`, `ai/rapporter/*-feedback.md`). Forslaget `ai/forslag-privatlivspolitik-feedback.md` er ikke gennemført.
- Google Fonts hentes fra `fonts.googleapis.com`/`fonts.gstatic.com` (`index.html:29–31`), så besøgendes IP-adresse sendes til Google uden at det er nævnt (en tysk domstol har kendt dette ulovligt uden samtykke, LG München 2022).
- jsDelivr (H1) får også besøgendes IP-adresse.
- "Feedback gemmes … højst 12 måneder", men der findes ingen automatisk sletning (`scripts/*.sql` har intet job til det).
**Forslag:** hent Inter-fonten og supabase-js fra egen server, så to tredjeparter forsvinder. Gennemfør forslaget om Anthropic, og nævn GitHub (offentlige, anonymiserede opsummeringer). Tilføj et `pg_cron`-job (eller et ugentligt job), der sletter feedback ældre end 12 måneder. Opdater datoen.
**Grundlov:** ja (`privatlivspolitik.html`) – se "Forslag til grundloven". Selvhosting af fonte og sletning er ikke grundlov.

### M5. Anonym tekst kan styre AI-kæden (prompt injection)
**Bevis:** `.github/workflows/feedback-product-owner.yml` linje 69–103: anonym feedback gives til Claude med skriveværktøjer. Der er gode værn: kun to filer må ændres, et filter for e-mailadresser, og prompten kalder beskederne utillidte. Men links, telefonnumre og instruktionslignende tekst filtreres ikke maskinelt, og `ai/FEEDBACK.md` læses bagefter af Ejeren, som skriver krav, der bliver til kode.
**Risiko:** en fremmed kan få indført et "krav" (fx et eksternt script, en ny adresse eller svækkede regler), som går videre gennem kæden. Grundloven og kontrollanten bremser meget, men ikke alt (fx en ny tredjepartsadresse i `index.html` er klasse A/H, ikke grundlov).
**Forslag:** udvid commit-tjekket i workflowet til også at afvise `http(s)://`, `www.` og telefonnumre (8 cifre) i de to filer. Skriv i `agenter/ejer.md`, at krav, der stammer fra feedback, aldrig må tilføje eksterne adresser, scripts eller ændre login, uden at sikkerhedsagenten har set dem. Kontrollanten afviser nye eksterne domæner i HTML/JS uden et `[SIKKERHED]`-krav.
**Grundlov:** ja (`.github/`, `agenter/*`).

---

## Lav

### L1. HTML bygges med data uden escaping enkelte steder
**Bevis:** `index.html` bruger `esc()` mange steder (65 gange), men fx `index.html:1201` (`ing.navn`), `:2077` (`navn`), `:2365` (`r.navn`) og butiksnavne (`data.butikker[k].navn`) sættes ind i `innerHTML` uden `esc()`. Kilden er holdets egne datafiler, men tilbudstekster stammer fra Tjek (tredjepart). I dag indeholder `retter.json`, `opskrifter.json` og `tilbudsliste.json` ingen `<`, `>` eller `javascript:` (tjekket).
**Forslag:** brug `esc()` på alle datafelter i skabelonerne, og tilføj en kontrol i `scripts/tests/kontrol.py`, der fejler, hvis en datafil indeholder `<`, `>` eller `javascript:`.
**Grundlov:** nej. Klasse A for kontrollen; skabelonerne rører indkøbslisten (H).

### L2. Workflows bruger flydende versioner
**Bevis:** alle `uses:` er fastlåst til en tag (`actions/checkout@v4` osv.), ikke til en commit-SHA. `npm install -g @anthropic-ai/claude-code` og `pip install playwright` har ingen version (`kontrollant.yml`, `anden-mening.yml`, `feedback-product-owner.yml`).
**Forslag:** fastlås handlingerne til commit-SHA (med tagget som kommentar) og fastlås npm- og pip-versionerne, og slå Dependabot til for `github-actions`.
**Grundlov:** ja (`.github/`).

### L3. Feedback-workflowet sender sin hemmelighed til den adresse, der står i `auth.js`
**Bevis:** `feedback-product-owner.yml` linje ~47–52 læser `url` med regex fra `auth.js` på `main` og sender `SUPABASE_FEEDBACK_TOKEN` dertil.
**Risiko:** ændres URL'en i `auth.js` (grundlov, men main skrives af agenter), går hemmeligheden til en fremmed server ved næste kørsel.
**Forslag:** læg Supabase-URL'en som GitHub-variabel/hemmelighed, eller tjek at værten ender på `.supabase.co` og matcher en fast projekt-ref, før der sendes.
**Grundlov:** ja (`.github/`).

### L4. Hele repoet udgives på siden
**Bevis:** ingen `.vercelignore`; Vercel udgiver derfor også `ai/`, `scripts/` (SQL, testdata, 954 KB `tilbud_snapshot.json`) osv. Repoet er offentligt i forvejen, så der lækker intet nyt, men det giver unødige offentlige adresser og større udgivelser.
**Forslag:** en `.vercelignore` med `ai/`, `scripts/`, `*.md`, `.github/`. Vagtposten og Browser-QA skal bekræfte, at siden og opskriftssiderne stadig virker.
**Grundlov:** nej. Klasse H (udgivelsen).

### L5. Personlige e-mailadresser i den offentlige historik
**Bevis:** commit-forfatterfeltet i de fleste menneskelige commits er en arbejds-e-mail (ikke gengivet her). Admin-e-mailen står i `admin.html:88` og `scripts/admin.sql`.
**Forslag:** brug GitHubs noreply-adresse (`git config user.email …@users.noreply.github.com`) i fremtidige commits, og slå "Block command line pushes that expose my email" til på GitHub. Historikken omskrives ikke (det ville ødelægge alle grene). Erstat e-mailen i `admin.html` med en tjek af `auth.uid()` (M3).
**Grundlov:** nej (Jonas' egne indstillinger).

---

## Hvad der er i orden
- `brugerdata`: RLS med `auth.uid() = user_id` for alle operationer; rækken slettes sammen med brugeren.
- `feedback`: anon kan kun indsætte og ikke læse; kun admin kan læse og opdatere `behandlet`.
- `agent_noegle`: RLS slået til og alt fjernet fra anon/authenticated; kun en sha256 af hemmeligheden gemmes. Funktionerne returnerer bevidst ikke e-mail. En hemmelighed på mindst 32 tilfældige tegn kan ikke gættes, selv om funktionerne kan kaldes af anon.
- `admin_statistik()` er `security definer` med `set search_path` og tjekker kaldet.
- Login-, feedback- og admin-koden bruger `textContent`/`esc()` til brugerdata; alle `target="_blank"` har `rel="noopener"`; ingen inline-hændelser (`onclick=` m.m.) i `index.html`.
- `sw.js` gemmer kun samme-oprindelse; Supabase-kald røres ikke (`sw.js:68`).
- "Log ud" rydder de lokale valg (`auth.js:146–148`).
- Feedback-workflowet sender ikke e-mailadresser til AI'en og stopper commits med e-mailadresser.

## Forslag til grundloven (kun Jonas kan gennemføre)
1. **`.github/workflows/kontrollant.yml` (H2):** del i testjob uden hemmeligheder og kontrollant-job; fjern `actions: write`; `persist-credentials: false` hvor der ikke pushes. Slå desuden grenbeskyttelse til på `main` under Settings → Branches (forbyd force-push og sletning).
2. **`privatlivspolitik.html` (M4):** tilføj Anthropic (AI læser feedback uden e-mail; kan behandles i USA), GitHub (offentlige, anonymiserede opsummeringer) og – indtil H1/M4 er gjort – Google Fonts og jsDelivr. Opdater datoen. Teksten i `ai/forslag-privatlivspolitik-feedback.md` kan bruges.
3. **`.github/workflows/feedback-product-owner.yml` (M5, L3):** afvis også links og telefonnumre i commit-tjekket; tag Supabase-URL'en fra en variabel eller tjek værten.
4. **`ai/agenter/ejer.md` og `kontrollant.md` (M5):** krav fra feedback må ikke tilføje eksterne adresser/scripts eller røre login uden sikkerhedsagentens gennemsyn; kontrollanten afviser nye eksterne domæner uden `[SIKKERHED]`-krav.
5. **Alle workflows (L2):** fastlås handlinger til SHA og npm/pip-versioner.
6. **`auth.js` (M3):** teksterne "mindst 6 tegn" → "mindst 8 tegn", når Supabase-indstillingen er hævet.
7. **I Supabase (ingen fil, men kun Jonas har adgang):** MFA på admin-kontoen, "Leaked password protection", mindst 8 tegn, bekræft "Confirm email" og "Secure email change", og kør de nye SQL-regler fra M2/M3, når de er skrevet.
