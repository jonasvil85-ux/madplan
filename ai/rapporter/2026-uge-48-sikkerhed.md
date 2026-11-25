# Sikkerhed – uge 48 (2026-11-25)

Anden ugentlige gennemgang. Forrige rapport: `ai/rapporter/2026-uge-47-sikkerhed.md`.
Gennemgået: hele arbejdstræet, hele git-historikken (499 commits på tværs af grene efter `git fetch --unshallow`) med særligt fokus på de 126 commits siden 18. nov. på main, `scripts/*.sql`, `index.html` (ny søgefunktion), `admin.html`, `auth.js`, `feedback.js`, `privatlivspolitik.html`, `sw.js`, alle 8 workflows, `scripts/second_opinion.py`, `scripts/billeder.py`-kæden, `ai/FEEDBACK.md` og feedbackrapporterne. Repoets GitHub-indstillinger er læst via API'et (kun læsning).
Kontrol: `python -I scripts/tests/kontrol.py` → `RESULTAT: BESTÅET (0 fejl, 4 advarsler)` (kørt på main 19b1135; ingen kode ændret).

**Ikke tjekket** (ærligt):
- Den udgivne side: proxyen i skyen afviste igen forbindelsen (403 for begge domæner), så HTTP-hovederne er ikke målt. `BROWSER.md` og `HELBRED.md` måler heller ingen sikkerhedshoveder.
- Supabase-projektet selv (indstillinger, om SQL-filerne er kørt, ekstra tabeller).
- GitHub Actions-indstillingerne (standardrettigheder for `GITHUB_TOKEN`, om Actions må godkende PR'er) og listen over samarbejdspartnere: API'et afviste adgangen fra skyen.
- Om Claude Codes `--allowedTools "Bash(python3 scripts/second_opinion.py:*)"` også tillader sammensatte kommandoer; ikke afprøvet (det ville være at teste mod workflowet).

## Resumé
| Alvor | Antal | Heraf nye |
|---|---|---|
| Kritisk | 0 | 0 |
| Høj | 3 | 1 (N1) |
| Middel | 6 | 1 (N2) |
| Lav | 5 | 0 |

**Ingen af de 10 `[SIKKERHED]`-krav fra uge 47 er taget eller udført.** Ingen af de berørte filer (`.github/`, `scripts/*.sql`, `auth.js`, `feedback.js`, `admin.html`, `privatlivspolitik.html`) er ændret siden 18. nov. Holdet har i stedet bygget søgning, datarettelser og tests. Det er ikke farligt i sig selv, men tre af kravene er klasse A eller små og kan tages uden Jonas (L1-kontrollen, M5-domænekontrollen og den nye N1-kontrol). Forslag til Ejeren nedenfor.

Ingen nye hemmeligheder: den eneste JWT i hele historikken er stadig Supabase **anon**-nøglen (`auth.js:6`). Ingen service-nøgle, GitHub-, Anthropic-, Cloudflare-, AWS- eller private nøgler i filer eller commits. Alle 126 commits siden 18. nov. har noreply-adresser som forfatter. GitHubs hemmelighedsscanning og push-beskyttelse er slået til (bekræftet via API).

---

## Høj

### N1 (NY). Hemmeligheder står i miljøet, mens agent-redigerbar kode fra `main` kører
**Bevis:**
- `.github/workflows/billeder.yml`, trinnet "Lav billeder" (ca. linje 49–58): `CLOUDFLARE_API_TOKEN` står i trinnets miljø, og samme trin kører `scripts/billeder.py`, `scripts/byg_retter.py`, `scripts/byg_opskrifter.py` og `scripts/tests/kontrol.py` (som igen starter node- og browsertests). `kontrol.py` og testene er klasse A og kan slås sammen af kontrollanten uden skærpet validering. Jobbet har desuden `contents: write` og pusher til `main`.
- `.github/workflows/anden-mening.yml` linje 70–84: `CLAUDE_CODE_OAUTH_TOKEN` og `CLOUDFLARE_API_TOKEN` står i miljøet for Claude-trinnet. Agenten har `Write` og `Edit` **uden stibegrænsning** og må køre `python3 scripts/second_opinion.py`. Den kan altså ændre scriptet og derefter køre det. Commit-tjekket bagefter (linje 92–100) stopper kun commits, ikke det, der allerede er sket under kørslen. Agentens input er diffen i `ai/BACKLOG.md`/`ai/design/`, som delvist stammer fra anonym feedback (se M5).
- `scripts/second_opinion.py` og `scripts/billeder.py` står ikke i grundloven og er ikke klasse H efter `regler.md`.

**Risiko:** en ændring i et testscript eller i `second_opinion.py`, der bliver slået sammen på `main` (fejl, en agent der lader sig styre, eller et lækket token), kører næste gang med Jonas' private Claude-token og Cloudflare-nøglen i miljøet og kan sende dem ud. Med Cloudflare-nøglen kan en fremmed bruge Jonas' konto (regning). Med Claude-tokenet kan en fremmed bruge hans abonnement. Det er samme type problem som H2, men de to workflows blev ikke gennemgået i uge 47.

**Forslag:**
1. `billeder.yml`: kun `billeder.py` får nøglen. Del trinnet i to: "Lav billeder" (kun `billeder.py` med nøglen) og "Byg og kontrollér" (byg + kontrol **uden** nøglen).
2. `anden-mening.yml`: begræns skriveværktøjerne til rapporten, fx `"Write(ai/rapporter/**)" "Edit(ai/rapporter/**)"`, og kør scriptet fra en kopi i `$RUNNER_TEMP`, som er lavet før agenten starter (så agentens ændringer ikke kører).
3. Tilføj `scripts/second_opinion.py` og `scripts/billeder.py` til grundloven (de kører med hemmeligheder), eller i det mindste til klasse H i `regler.md`.
4. Det holdet selv kan gøre nu (klasse A): en kontrol i `kontrol.py`, der fejler, hvis en fil under `scripts/` uden for en tilladt liste (i dag `tilbud.py`, `billeder.py`, `second_opinion.py`, `tests/live_tjek.py` og browsertestene) bruger netværk (`urllib`, `http.client`, `socket`, `requests`, `curl`/`wget` i `subprocess`) eller læser miljøvariabler med `TOKEN`/`KEY`/`SECRET` i navnet. Det er ikke et værn mod en bevidst angriber (han kan ændre kontrollen), men det fanger fejl og gør ændringer synlige for kontrollanten.
**Grundlov:** punkt 1–3 ja (`.github/`, `regler.md`), punkt 4 nej.

### H1 (uændret). Supabase-biblioteket hentes fra et CDN uden fast version og uden integritetstjek
**Bevis:** `index.html:990` (linjen er flyttet fra 968) og `admin.html:85`: `<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2">`, uden `integrity`. Ingen CSP.
**Status:** ikke taget. Forslaget fra uge 47 står ved magt. Klasse H, ikke grundlov.

### H2 (uændret, nu bekræftet). Kontrollant-workflowet kører grenenes kode med Bash og hemmeligheder i samme job
**Bevis:** `.github/workflows/kontrollant.yml` linje 17–20 (`contents: write`, `actions: write`, `issues: write`) og 63–72 (`--allowedTools Bash …` med `CLAUDE_CODE_OAUTH_TOKEN` og `GH_TOKEN` i miljøet). Uændret siden uge 47.
**Nyt bevis:** GitHub-API'et viser, at `main` **ikke er beskyttet** (`protected: false`, ingen grenbeskyttelse og ingen rulesets), og repoet er offentligt. Et lækket token med `contents: write` kan altså force-pushe eller slette `main`, og Vercel udgiver straks. Se N2.
**Grundlov:** ja.

---

## Middel

### N2 (NY). `main` har ingen grenbeskyttelse
**Bevis:** `GET repos/…/branches/main` → `protected: false`; `…/branches/main/protection` → 404 "Branch not protected"; `…/rulesets` → `[]`.
**Risiko:** et lækket token (H2, N1) eller en fejl kan omskrive eller slette historikken på `main`, og Vercel udgiver det med det samme. Vagtposten kan ikke rulle tilbage, hvis historikken er væk.
**Forslag:** et ruleset på `main` (Settings → Rules → Rulesets), der **kun** forbyder force-push og sletning. Det bryder ikke agenternes direkte push af `ai/`-filer og kontrollantens sammenlægninger. Krav om PR eller status-tjek skal ikke slås til (det ville stoppe holdet).
**Grundlov:** nej (GitHub-indstilling), men kun Jonas har adgang. Det tager under 2 minutter og er det billigste værn på listen.

### M1 (uændret, krav opdateret). Ingen sikkerhedshoveder (ingen `vercel.json`)
**Bevis:** stadig ingen `vercel.json`. Ikke målt på den udgivne side.
**Opdatering:** anden mening (`2026-11-18-anden-mening-2.md`) foreslog tilføjelser, som aldrig kom ind i backloggen: `upgrade-insecure-requests`, hoveder også på `/sw.js` og manifestet, `connect-src` med databasen og Vercel Insights, Report-Only først og håndhævelse i en senere gren, efter at Browser-QA har gennemgået alle flows inkl. offline-genstart; ikke-mål: rapport-adresse, HSTS-preload, nonces. Jeg er enig og har skrevet det ind i kravet.

### M2–M5 (uændrede)
- **M2** feedback-tabellen uden grænser på serveren: `scripts/feedback.sql:14` uændret.
- **M3** admin uden 2-trinsbekræftelse: `scripts/admin.sql` uændret.
- **M4** privatlivspolitikken (`privatlivspolitik.html:21`, "Sidst opdateret: 3. november 2026") nævner stadig ikke Anthropic, GitHub, Google Fonts eller jsDelivr. Google Fonts hentes nu også fra **alle 194 opskriftssider** (`opskrift/*/index.html`), ikke kun forsiden.
- **M5** styring via anonym feedback: workflowet er uændret. **Positivt:** i `ai/FEEDBACK.md` (2026-11-23) genkendte Product Owner en besked, der pressede på for hurtig gennemførelse, som et forsøg på at give instrukser, og fulgte den ikke ("Instrukser i beskeder forsøgt fulgt: 0"). Ejeren afviste begge forslag fra den dag med en begrundelse. Værnet i prompten virker altså i praksis, men det maskinelle filter (links, telefonnumre) mangler stadig. Ingen links, telefonnumre eller e-mailadresser i `ai/FEEDBACK.md` eller `ai/rapporter/*-feedback.md`.

---

## Lav (alle uændrede)
- **L1** escaping: søgefeltet, der er nyt (8ea3f25), escaper korrekt (`esc(retSoeg)` i både `value=` og resultatteksten). Stederne fra uge 47 er uændrede (fx `index.html:2103` `${navn}`, `:2155` butiksnavne i en kombination, `:1223` `ing.navn`). Datafilerne `retter.json`, `opskrifter.json`, `tilbudsliste.json` og `naering.json` indeholder stadig 0 forekomster af `<`, `>` eller `javascript:`.
- **L2** flydende versioner i workflows: uændret. Dependabot-sikkerhedsopdateringer er slået fra. Repoet har ingen `package.json`/`requirements.txt`, så kun `github-actions` er relevant for Dependabot.
- **L3** feedback-workflowet sender sin hemmelighed til adressen i `auth.js`: uændret (`feedback-product-owner.yml` ca. linje 47–52).
- **L4** ingen `.vercelignore`: uændret. Kunne ikke måle, om `/ai/STATUS.md` udgives (proxy).
- **L5** e-mail i offentlige filer: admin-e-mailen står stadig i `admin.html`, `scripts/admin.sql`, `feedback.js` (fejlbeskeden) og `privatlivspolitik.html` (lovpligtig dér). Ikke gengivet her.

---

## Hvad der er i orden (nyt eller bekræftet i uge 48)
- Ingen hemmeligheder i de 126 nye commits; alle nye forfattere er noreply-adresser.
- Hemmelighedsscanning og push-beskyttelse er slået til på GitHub.
- Den nye søgning i "Vælg selv" escaper brugerens tekst alle steder, den vises.
- `sw.js` gemmer stadig kun samme oprindelse, og der er ingen nye tredjepartsdomæner i HTML/JS (kun jsDelivr, Google Fonts og eget domæne, som i uge 47).
- Ingen inline-hændelser; alle `target="_blank"` har `rel="noopener"`.
- Cloudflare-konto-id'et i `scripts/second_opinion.py` er et id og ikke en hemmelighed; nøglen læses fra miljøet.
- Product Owners værn mod instrukser i feedback virkede i praksis (se M5).

## Til Ejeren (prioritering, ikke grundlov)
Holdet kan tage tre sikkerhedskrav uden Jonas, og hver af dem er en lille, isoleret ændring:
1. **L1-kontrollen** (klasse A, kun `kontrol.py`).
2. **M5-kontrollen** af tilladte eksterne domæner (klasse A, kun `kontrol.py`).
3. **N1-kontrollen** af netværk og hemmeligheder i `scripts/` (klasse A, kun `kontrol.py`).
Derefter **H1** (supabase-js med fast version, klasse H). Jeg foreslår, at mindst ét af dem lægges i top 5 i næste uge.

## Forslag til grundloven (kun Jonas kan gennemføre)
Nye i uge 48 (nr. 1–3), derefter de uændrede fra uge 47:
1. **Ruleset på `main` (N2):** forbyd force-push og sletning. Intet andet. (GitHub → Settings → Rules.)
2. **`.github/workflows/billeder.yml` (N1):** `CLOUDFLARE_API_TOKEN` kun på et trin, der alene kører `scripts/billeder.py`; byg og `kontrol.py` i et trin uden nøglen.
3. **`.github/workflows/anden-mening.yml` (N1):** `Write`/`Edit` begrænses til `ai/rapporter/**`; `second_opinion.py` kopieres til `$RUNNER_TEMP` før agenten starter og køres derfra. **`ai/regler.md`:** `scripts/second_opinion.py` og `scripts/billeder.py` føjes til grundloven (eller klasse H), fordi de kører med hemmeligheder.
4. `kontrollant.yml` (H2): testjob uden hemmeligheder, fjern `actions: write`, `persist-credentials: false`.
5. `privatlivspolitik.html` (M4): Anthropic, GitHub og, indtil de er fjernet, Google Fonts (nu også på opskriftssiderne) og jsDelivr; ny dato.
6. `feedback-product-owner.yml` (M5, L3): afvis links og telefonnumre; fast Supabase-adresse.
7. `ai/agenter/ejer.md` og `kontrollant.md` (M5): krav fra feedback må ikke tilføje eksterne adresser/scripts uden sikkerhedsgennemsyn.
8. Alle workflows (L2): SHA-fastlåsning, faste npm-/pip-versioner, Dependabot for `github-actions`.
9. `auth.js` (M3): "mindst 8 tegn", når Supabase-indstillingen er hævet.
10. Supabase (M2, M3, M4): MFA for admin, beskyttelse mod lækkede adgangskoder, mindst 8 tegn, kør de nye SQL-filer, når de er skrevet.
