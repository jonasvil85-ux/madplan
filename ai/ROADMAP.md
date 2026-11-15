# Produktrevision og køreplan (15. november 2026)

Mandat: AI-holdet udvikler hele Måltidsjagten – ikke kun data og billeder. Mål: Danmarks bedste platform for madplan og tilbud. Ejeren revurderer denne fil hver søndag.

## Hvordan revisionen er lavet
- Siden åbnet som en bruger i headless Edge på 360, 390, 768 og 1280 px, hele flowet klikket igennem (forside → "Brug forslaget" → indkøbsliste → tilføj varer → indkøbsseddel → Retter) med skærmbilleder og målinger af hvert trin.
- Koden læst: `index.html` (206 KB, ca. 2.800 linjer, al logik og al CSS), `pris.js`, `kategorier.js`, `varer.js`, `sw.js`, byggescripts og data.
- Browser-QA (GitHub, Chromium) målte det samme uafhængigt og fandt 32 små tryk-flader på mobil, hvilket bekræfter min måling.

## Hvad der virker
Hurtig (indlæsning under 1 s), ingen JavaScript-fejl, intet vandret scroll, komplet flow i fem trin, onboarding, PWA, delbar liste, 9 butikker, ugeforslag med variation, login og feedback. Billeder på alle retter. Faste kontroller, regressionstest, vagtpost og Browser-QA.

## Hvad revisionen fandt (kort)
- **Forsiden** har ikke budget og ikke fravalg; man kan ikke sige "højst 600 kr" eller "ikke svinekød".
- **Mobil:** Byt/Fjern-knapperne var 27 × 21 px; liste-ikonet 22 px; mange chips 34 px; butikker 38 px (anbefaling: 44 px).
- **Indkøbslisten** er 8.300 px lang på mobil; hver række har en lang grå tekst ("Avisen: MADVÆRKET Julemedister eller hakket grise- og kalvekød · 500 g · Til: …") i stedet for det, man skal købe.
- **Retter ("Vælg selv")** er 63.000 px lang på mobil: 171 retter uden søgning; kun kategorier.
- **Google:** én URL; ingen opskrift kan findes via søgning.
- **Kødfri uge** kan ikke laves: kun Lidl har 12 eller flere vegetarretter i sin egen butik.
- **Ingen favoritter eller gemte madplaner**, ingen påmindelse, ingen måling af hvad brugerne gør.
- **Teknisk:** monolit i én fil; 458 KB opskriftsfil hentes ved hvert besøg; sikkerheden er ikke gennemgået systematisk.

## De 20 vigtigste forbedringer
Score 1–5 for **kundeværdi (K)**, **forretningsværdi (F)** og **teknisk vigtighed (T)**. Indsats: S (små, under en dag), M (en til tre dage), L (en uge eller mere). **Prioritet = (2·K + 2·F + T) ÷ (1 + 0,5 · indsats)**, hvor S = 1, M = 2, L = 3. Rangeret efter prioritet; lige tal ordnes efter kundeværdi.

| # | Forbedring | K | F | T | Indsats | Prio | Status |
|---|---|---|---|---|---|---|---|
| 1 | Indkøbsliste: skimmable rækker (vare stort, detaljer foldet ind) | 5 | 3 | 2 | S | 12,0 | **Bygget** (`ai/2026-11-15-indkoebsliste-raekker`) |
| 2 | Mobil: tryk-flader på 44 px (Byt/Fjern, ikoner, chips, faner) | 4 | 3 | 2 | S | 10,7 | **Bygget** (`ai/2026-11-15-mobil-tryk-flader`) |
| 3 | Fravalg: "Vi spiser ikke …" (svin, okse, fjerkræ, fisk, kødfri, løg, svampe, mejeri, æg) | 5 | 4 | 3 | M | 10,5 | **Bygget** (`ai/2026-11-15-fravalg-budget`) |
| 4 | Budget: "højst X kr for ugen" med ærlig besked | 5 | 4 | 3 | M | 10,5 | **Bygget** (samme gren) |
| 5 | Gemte madplaner og favoritter (retention) | 4 | 5 | 3 | M | 10,5 | Krav i backlog |
| 6 | Sikkerhedsgennemgang (Supabase-regler, hoveder, hemmeligheder) | 2 | 3 | 5 | S | 10,0 | Sikkerhedsagenten, onsdag |
| 7 | Opskriftssider til Google (193 sider, Recipe-markup, sitemap) | 3 | 5 | 3 | M | 9,5 | **Bygget** (`ai/2026-11-15-opskriftssider`) |
| 8 | Banner "Du ser en gemt kopi" | 3 | 2 | 4 | S | 9,3 | Krav (H) |
| 9 | Kortere onboarding (seks trin → tre) | 3 | 3 | 2 | S | 9,3 | Krav |
| 10 | Søgning og filtre i "Vælg selv" (ret og ingrediens, "vis flere") | 5 | 3 | 2 | M | 9,0 | Næste |
| 11 | Sammenlign alle butikker (ugens pris pr, butik på ét sted) | 5 | 5 | 2 | L | 8,8 | Krav |
| 12 | Delbart link til madplan (valg i URL) | 3 | 4 | 3 | M | 8,5 | Krav |
| 13 | Tøm køleskabet (ingredienser jeg har) | 5 | 4 | 3 | L | 8,4 | Krav, efter 6 |
| 14 | Prisalarmer og ugentlig påmindelse | 4 | 5 | 3 | L | 8,4 | Kræver backend og beslutning |
| 15 | Kødfri uge muligt: mindst 12 vegetarretter pr, butik | 4 | 3 | 2 | M | 8,0 | Krav (DATA) |
| 16 | Måling (privatlivsvenlig tælling af fald i flowet) | 1 | 5 | 4 | M | 8,0 | SEO/vækst-agenten |
| 17 | Tilgængelighed: kontrast, tastatur, skærmlæser | 3 | 3 | 3 | M | 7,5 | Krav |
| 18 | Ydeevne: hent opskrifter (458 KB) først ved "Vælg selv" | 3 | 2 | 4 | M | 7,0 | Krav |
| 19 | Næring pr, voksen i Fitness | 2 | 2 | 2 | S | 6,7 | Krav (H) |
| 20 | Opdel `index,html` i moduler (monolit, 206 KB) | 1 | 2 | 5 | L | 4,4 | Efter regressionstest dækker mere |

Note: tallene er beregnet med formlen ovenfor. Jeg byggede nr. 1–5 i denne omgang: de fem med højest prioritet, bortset fra tre med samme score 10,5 (fravalg, budget og favoritter); favoritter venter, fordi de kræver ændringer i login og lagring, som er en del af grundloven og skal gennemgås af sikkerhedsagenten først.

## Implementeringsplan
1. **Nu (bygget, afventer kontrollantens sammenlægning):** mobil tryk-flader, fravalg, budget, opskriftssider og indkøbslistens rækker.
2. **Denne uge (agenterne tager dem fra backloggen):** søgning i Vælg selv, kødfri retter, gemt-kopi-banner, onboarding. Sikkerhedsagenten kører onsdag (7), SEO/vækst torsdag (15).
3. **Næste uge:** 8 favoritter og gemte planer, 9 sammenlign butikker, 12 delbart link.
4. **Senere:** 11 tøm køleskabet, 13 prisalarmer (kræver, at Jonas vælger kanal, fx e-mail), 16–17 tilgængelighed og ydeevne, 19, 20.

## Hvad holdet ikke kan måle endnu
Rigtige brugeres adfærd (ingen adgang til Supabase eller Vercel Insights), konkurrenters sider (kun Claude i chatten kan søge på nettet), udseende på rigtige telefoner (kun Chromium).
