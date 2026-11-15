# Udviklerrapport 2026-11-15 – mobil: tryk-flader (bygget af Claude i chatten på Jonas' bestilling)

**Hvad:** CSS-blok til mobil (`pointer: coarse` eller bredde højst 700 px): Byt/Fjern-knapperne (var 27 × 21 px) og liste-ikonet på retbilleder (var 22–28 px) er nu 36 × 36 px med et usynligt trykområde på 44 × 44 px; butikvalg, chips ("Tilføj varer"), "Ikke hjemme", trinfanerne, husstandsknappen, papirkurven og fodlinks er mindst 44 px høje; afkrydsningsfelterne er 24 px i rækker på mindst 48 px (hele rækken er allerede en label).

**Hvorfor:** ROADMAP 2. Siden bruges mest på telefon i butikken, og små knapper giver forkerte tryk. Byt/Fjern var de vigtigste knapper på forsiden og kun 21 px høje.

**Klasse:** A (kun CSS i `index.html`; ingen JavaScript, data eller beregning ændret).

**Filer:** `index.html` (en CSS-blok før `</style>`), denne rapport.

**Accept:** (1) mindst 44 px trykområde på forside, retter, indkøbsliste, tilføj varer og seddel: målt og verificeret nedenfor, (2) intet vandret scroll på 390 px: målt `over: false` på alle fem trin, (3) udseendet bevares.

**Før/efter (headless Edge, 390 × 844, siden på `main` mod grenen; antal interaktive elementer, hvis synlige størrelse er under 44 px):**

| Trin | Før | Efter | Hvad der er tilbage efter |
|---|---|---|---|
| Forside | 36 | 22 | 14 Byt/Fjern + 7 liste-ikoner (36 px synlige, 44 px trykområde) + 1 info-ikon (22 px, 44 px trykområde) |
| Indkøbsliste | 86 | 80 | 80 afkrydsningsfelter (24 px) i rækker på 48 px, hvor hele rækken er trykflade |
| Tilføj varer | 309 | 0 | |
| Indkøbsseddel | 29 | 24 | 24 afkrydsningsfelter som ovenfor |
| Retter | 191 | 178 | 171 liste-ikoner + 7 Byt/Fjern (som forside) |

**Trykområdet er hit-testet:** med `elementFromPoint` rammer en berøring 4 px uden for Byt/Fjern- og liste-knappernes synlige kant knappen til venstre og over (trykområdet strækker sig 4 px ud i alle retninger, hit-testet på de to sider punktet ligger inden for), og info-ikonet rammes på alle fire sider.

**Pris for ændringen:** siderne bliver længere, fordi alt er større: Tilføj varer 6.983 → 8.417 px (+21 %), indkøbsliste 8.277 → 8.550 px (+3 %), forside 1.213 → 1.313 px. Overskriftens knapper er nu 44 px, så husstandsknappen ligger i en ny linje på 390 px bredde.

**Test:** `kontrol.py` lokalt `RESULTAT: BESTÅET`; regressionstest uændret (ingen JavaScript rørt; skal køres af kontrolløren). Skærmbilleder af forside og tilføj varer set.

**Dækker IKKE:** desktop (blokken gælder ikke der); skærmlæsere og tastatur; iOS Safari og rigtige telefoner (kun Chromium-emulering); kontrast.

**Kontrolløren bør kigge på:** at diffen kun er CSS i én blok; at `retter.json`, `opskrifter.json` og al JavaScript er uændret; et par skærmbilleder fra Browser-QA efter udgivelsen (hvis den kører; tryk-flader under 40 px skal falde).

**Næste skridt:** (1) Rækkerne i indkøbslisten er lange og rodede ("Avisen: …" i grå tekst); gør dem skimmable (ROADMAP 5). (2) Måling på rigtig telefon.
