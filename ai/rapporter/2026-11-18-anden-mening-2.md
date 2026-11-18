# Anden mening 2026-11-18 (kørsel 2)

Nyt i seneste commit: `ai/BACKLOG.md` har fået 10 nye `[SIKKERHED]`-krav fra uge 47 (H1, H2, M1-M5, L1, L4, L2/L3); ingen designfiler er ændret. Jeg tog 2 emner (M2 og M1; H1 og M3 er mere ligetil, H2/L2/L3 er grundlov). Kald til modellen: 3 af 3 (emne 1: kreativ + kritisk, emne 2: kritisk). Modellen er rådgiver; vurderingen er min.

## Emne 1: Feedback-tabellen får grænser på serveren (M2)

**Spørgsmål:** Hvordan beskytter man en anonym feedback-tabel uden at genere ærlige brugere og uden at ændre klienten?

### Idéer (kreativ runde)
1. *Trigger med check, whitelist og hastighedsgrænse* (sikker): **Valgt**, er i forvejen M2. Men "pr. IP via `inet_client_addr()`" **afvist**: bag API-laget er IP ikke pålidelig. "Falsk succesbesked ved afvisning" **afvist**: ikke ærligt og skjuler fejl.
2. *Staging-tabel + materialiseret visning + natligt rengøringsjob* (karantæne): **Afvist.** Dobbelt så mange dele at holde i live; admin-siden skal alligevel tåle dårlige rækker. Kun delen "admin springer dårlige rækker over" er med.
3. *Lokkemad-tabel til spam* (skør): **Afvist.** Angribere kan ikke skelnes fra ærlige, og kompleksiteten står ikke mål med en lille tabel.
4. *Proof-of-work i feedbackens felter* (vender problemet): **Afvist.** Kræver ændring af `feedback.js` (grundlov, ikke-mål), og en hemmelighed i triggeren er ikke hemmelig for en angriber, der kender klienten.
5. *Gateway-API med fast nøgle i siden* (radikalt enklere): **Afvist.** En nøgle i siden er lige så offentlig som den, vi har; ingen sikkerhedsgevinst, og klienten ville skulle pege et andet sted hen.

### Modellens kritik (kort, runde 2 på det opdaterede krav)
Hastighedsgrænsen kan have race-condition ved samtidige indsættelser; "gyldigt format" for kontaktadresse er vagt; den globale grænse kan bruges som våben (alle ærlige låses ude); ingen log/alarm ved afvisning; JSON bør have whitelist af nøgler; forslag om CAPTCHA, per-klient-grænse, sanitering.

### Min vurdering
- **Enig** i våbenrisikoen: en global grænse på 30/min lader en angriber låse feedback for alle. Det er ikke en nedetid for kerneprodukt (madplanen virker uden feedback), så en global grænse er stadig det rigtige valg, når IP ikke kan bruges, men det skal stå i kravet som *kendt og accepteret afvejning*, og grænsen må ikke give en falsk succes.
- **Enig** i race-condition: tællingen i triggeren bør tage en advisory lock (`pg_advisory_xact_lock`) eller acceptere, at grænsen er "omtrent". Konkret punkt, vi manglede.
- **Delvist enig** i "ingen log": en afvist indsættelse efterlader intet spor. Billig løsning: en lille tæller-tabel eller `raise warning` i triggeren; ingen alarm-system.
- **Delvist enig** i whitelist af nøgler i JSON: nyttig, men klienten ændres ikke, så listen skal tages fra, hvad den sender i dag; ellers afviser vi ærlige beskeder. Skal testes med samme felter som i dag (står allerede i Accept 3).
- **Uenig** i CAPTCHA/proof-of-work (kræver klientændring og modarbejder en rolig side) og i "sanitering ved gemning": korrekt løsning er escaping ved visning i admin (L1/esc), ikke at ændre data. Idempotente migreringer er allerede et krav.
- Ukendt, ikke tjekket: om platformens API-lag tillader en trigger at afvise med en læsbar fejltekst til klienten; skal afprøves af den, der bygger det.

### Foreslået ændring af kravet (M2)
Tilføj til **Krav**: *"Hastighedsgrænsen er global (ikke pr. IP, der ikke er pålidelig bag API-laget) og tæller i en transaktion med `pg_advisory_xact_lock`, så samtidige indsættelser ikke slipper forbi. Den afviser med en tydelig fejl (aldrig falsk succes). Maks. ca. 30 pr. minut og ca. 500 pr. døgn. Afvisninger tælles i en lille logtabel, så misbrug kan ses i admin."*
Tilføj til **Hvorfor**: *"Kendt afvejning: en angriber kan fylde grænsen og midlertidigt blokere feedback fra alle; det rammer ikke madplanen, og grænsen er bevidst valgt frem for at risikere en fyldt tabel."*
Tilføj til **Accept**: *"(6) en test af 40 hurtige indsættelser viser, at højst grænsen slipper igennem og resten får en læsbar afvisning."*
Constraints: tilføj *"Check-reglerne lægges på som `NOT VALID` og valideres, når tjekket af gamle rækker er rent."* Fravælg: CAPTCHA, proof-of-work, staging-tabel.

## Emne 2: Sikkerhedshoveder via `vercel.json` (M1)

**Spørgsmål:** Hvad er svagt, glemt eller risikabelt i kravet om CSP (først Report-Only) og de øvrige hoveder på en statisk side med inline-scripts, tredjeparts-billeder, login og service worker? Kun kritisk runde (ingen kald til rådighed til kreativ).

### Modellens kritik (kort)
`unsafe-inline` giver åben XSS-vektor; mangler SRI; manglende cookie-flags (`Secure`, `HttpOnly`, `SameSite`) og HSTS-preload; `script-src`/`img-src`/`font-src`/`connect-src` skal nævne alle tredjeparter; CSRF og login-rate-limiting; CSP-rapport-endpoint og `upgrade-insecure-requests`; Report-Only kan skjule fejl; service worker kan cache kompromitterede svar; enforce fra starten med nonces/hashes; særskilt streng CSP for admin.

### Min vurdering
- **Enig** i, at Report-Only uden rapport-endpoint giver ingen indsamlede fejl: der er ingen, der læser en browserkonsol i produktion. Accept (2) hviler derfor alene på Browser-QA. Konkret forslag: *Report-Only først, og Browser-QA skal åbne forsiden, login, feedback, en opskriftsside, admin og en side med tilbudsbilleder og læse konsollen, før kravet kan skifte til håndhævelse (eget lille trin, ikke samme gren).* Jeg afviser en rapport-adresse (ny tredjepart og nyt persondatalager).
- **Delvist enig** i service worker: `sw.js` og manifestet skal også få hovederne, og `connect-src` skal dække databasen og Vercel Insights, ellers rammer CSP'en offline-cachen. Det mangler i kravets Accept (2).
- **Enig** i `upgrade-insecure-requests` (billig og ufarlig); **afvist**: HSTS `preload` (svær at gøre om; ikke nødvendig).
- **Uenig:** nonces er umulige på en statisk side uden server; hashes for inline-scripts er skøre (bryder ved hver tekstændring) og er allerede et bevidst ikke-mål (`unsafe-inline` senere). "Enforce fra starten" er farligt for login og billeder uden test.
- **Uenig / misforstået:** cookie-flags og CSRF-tokens passer ikke; siden bruger ikke egne cookies, og login-token sendes i en header. SRI er allerede H1; rate-limiting af login ligger hos databasetjenesten. Generelle råd uden konkret indhold er ikke taget med.

### Foreslået ændring af kravet (M1)
- Tilføj til **Krav**: *"`upgrade-insecure-requests` i CSP. Hovederne gælder også `/sw.js` og `/manifest`-filen. `connect-src` indeholder databasen og Vercel Insights; `img-src` Tjek-billederne; `font-src`/`style-src` følger M4 (egne fonte)."*
- Ændr **Accept (2)** til: *"Report-Only-trinnet afleveres først; en senere gren skifter til håndhævelse, når Browser-QA har gennemgået forside, login, log ud, feedback, opskriftsside, admin og offline-genstart med service worker uden CSP-fejl i konsollen."*
- Ikke-mål tilføjes: *"rapport-adresse (report-uri), HSTS-preload, nonces."*

## Afsluttende
Nyttigt: delvist. Race-condition/advisory lock, den bevidste afvejning ved den globale grænse og service worker/connect-src i CSP var nye punkter; resten var enten allerede i kravene eller bygget på misforståelser (cookies, CSRF, nonces på statisk side).
