# SEO og vækst – uge 47 (2026-11-19)

Første SEO-rapport. Ingen trafiktal, søgedata eller brugerdata findes for holdet (Vercel Insights og Supabase kan ikke læses herfra); alt nedenfor er læst i repoet eller i `ai/BROWSER.md` / `ai/HELBRED.md`. Hypoteser er mærket **HYPOTESE**. Ikke tjekket: den udgivne side direkte, Google Search Console, rigtige søgeord og deres efterspørgsel, skærmbillederne på grenen `skaermbilleder` (ikke hentet i denne kørsel).

## Fund med bevis
**Det, der allerede er i orden**
- 193 opskriftssider + `/opskrifter/` + forside + privatlivspolitik = 196 URL'er i `sitemap.xml`; `robots.txt` har `Sitemap:`-linjen og spærrer kun `/admin.html`.
- Alle 193 sider har unik titel og unik beskrivelse, canonical, `og:`-tags, `Recipe`- og `BreadcrumbList`-markup, synlig brødkrumme, ét billede med `fetchpriority="high"` og bredde/højde, `loading="lazy"` på de øvrige, 191–343 ord (median 237) og link til forsiden og oversigten. Forsiden har link til `/opskrifter/` i sidefoden.
- Browser-QA (2026-11-19): grøn, indlæsning under 1 s, 0 billeder uden alt, 0 JavaScript-fejl.
- **Det ældre [SEO]-krav "Opskriftssider: forsiden linker til dem" er i praksis opfyldt** (forside-link, brødkrumme, `Sitemap:` i robots.txt findes). Ejeren bør efterkontrollere accept (4) (kontrollen tjekker det) og afkrydse det.

**Svagheder**
1. **Titler for lange:** 171 af 193 opskriftstitler er over 60 tegn (længste 99). Målt med et script over `opskrift/*/index.html`. Mønstret er "Navn – opskrift til 4 | Måltidsjagten"; Google afkorter typisk omkring 60 tegn (jeg lover ingen placering). 13 beskrivelser er under 70 tegn (korteste 59), én er 161.
2. **Forsiden er tom for crawlere uden JavaScript:** brødteksten bygges i JS (`#sim-plads` fyldes af `simuleringHtml()`, `index.html:2283`); `<noscript>` har to sætninger. `<h1>` er kun logoet (`aria-label="Måltidsjagten"`), så forsiden har ingen synlig overskrift med søgeord. Google kører JavaScript, så **HYPOTESE:** det er en svaghed, ikke en blokering; det er ikke målt.
3. **Inkonsistent butikstal:** `<meta name="description">`, `og:description`, JSON-LD og opskriftssiderne skriver "10 supermarkeder" / nævner 10 kæder; `regler.md` og README taler om 9 butikker. Ejeren afgør, hvad der er rigtigt (ærlig mærkning).
4. **Opskriftssiderne har ingen klar vej til at komme igen:** kun knappen "Se ugens tilbud og lav din madplan" nederst. Ingen kobling til, hvad retten koster *denne uge* (må ikke opfindes; priser på siderne er et ikke-mål i det ældre krav).
5. **Næringsdata i markup kan være forkert:** 5 sider angiver over 1000 kcal pr. portion (højst 1436 kcal, "Helstegt and med æbler og svesker"; 1354 kcal for "Æbleflæsk med rugbrød"). Det er skrevet som "gennemsnit af 4". **HYPOTESE:** tallene er for høje eller misvisende; nøjagtigheden kunne ikke tjekkes her. Forkerte tal i `Recipe`-markup er værre end ingen.
6. **Sitemap uden `lastmod`:** alle URL'er har kun `changefreq` (Google bruger den ikke); en rigtig `lastmod` fra data ville hjælpe genindeksering. Kræver ændring i `scripts/byg_sider.py` (H).
7. **Måling:** kun Vercel Insights' sidevisninger (`index.html:28`); privatlivspolitikken lover "anonym besøgsstatistik … ingen cookies". Ingen hændelser: man kan ikke se, om nogen når til indkøbssedlen.

## Vækst og fastholdelse (hypoteser)
- **HYPOTESE:** Ugens tilbud skifter, så naturlig grund til at komme igen er "hvad er billigt i denne uge". I dag findes kun "gem lokalt" (`localStorage`, `index.html:1044`) og et delbart link til listen; favoritter og gemte madplaner er et åbent krav (ROADMAP 5), delbart link til madplan er ROADMAP 12. Det er de to dyreste huller i fastholdelsen.
- **HYPOTESE:** Folk, der lander på en opskrift fra Google, ser ikke madplanen. En tydelig overgang "Brug denne ret i din uge" kunne konvertere søgetrafik til brugere. Kan kun vurderes efter måling (forslag 2).
- Første 30 sekunder: Browser-QA's flow kører, men "30–31 små tryk-flader" (`BROWSER.md`) peger på friktion på telefon; der er ingen måling af frafald. Skærmbillederne er ikke set i denne kørsel.

## Analyse – forslag til privatlivsvenlig måling
Tæl kun anonyme hændelser uden bruger-id, uden IP, uden indhold: `butik_valgt`, `forslag_brugt`, `seddel_aabnet`, `liste_delt`, `opskrift_til_forside` (klik fra opskriftsside). Siden bruger allerede Vercel Web Analytics; **uafklaret** om kontoen/abonnementet tillader egne hændelser (`track`) – det kan holdet ikke se. Skal i så fald ske uden at røre `auth.js`/`feedback.js`, og privatlivspolitikken (grundlov, kun Jonas) dækker allerede "anonym besøgsstatistik"; Ejeren bør vurdere, om hændelser kræver en tilføjelse og i så fald foreslå den til Jonas.

## Tre forslag
1. **[SEO] Kortere titler og beskrivelser på opskriftssiderne** (A, lille, målbart; krav i backlog).
2. **[SEO] Anonym hændelsesmåling** af de fem hændelser (A/H-vurdering hos Ejeren; krav i backlog).
3. **[SEO] Forsiden: synlig overskrift og kort statisk tekst til crawlere**, og ens butikstal overalt (krav i backlog). Ingen nye landingssider endnu: søgeord som "billig aftensmad" eller "madplan til 4" kan ikke dokumenteres uden søgedata; først når målingen (2) eller Search Console viser efterspørgsel, bør én side med reelt unikt indhold overvejes.

## Efterkontrol af tidligere forslag
Ingen tidligere SEO-rapport. Næste uge: Ejeren har afgjort butikstallet? Er titlerne kortet?
