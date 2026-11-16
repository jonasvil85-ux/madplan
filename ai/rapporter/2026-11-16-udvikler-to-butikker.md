# Udviklerrapport 2026-11-16 – én regel for to butikker

**Hvad:** kortets to-butiks-forslag bruger nu samme regel som boksen "Hvor mange butikker" (`anbefaletAntal`). To butikker anbefales, når deres fælles billigste uge er mindst `ANBEFAL_SPAR` (30 kr) billigere end den billigste enkeltbutiks uge, regnet på præcise tal.
- Parrets uge er én samlet indkøbsliste over begge butikker, ud fra egne tilbud.
- Begge uger er 7 aftensmåltider til husstanden med samme portioner.
- Blandt flere par vises den billigste uge.
- Teksten: "Handl i to butikker og spar 54 kr – Lidl + Netto: 367 kr for ugens 7 aftensmåltider mod 421 kr i Lidl alene. Begge priser er den billigste uge ud fra butikkernes egne tilbud. Transport og ekstra tid er ikke regnet med i prisen." Besparelsen er forskellen på de viste tal.

**Hvorfor:** Jonas 2026-11-16: "Vælger man flere butikker skal det jo gerne blive billigere ja", og tidligere: det er ikke fair at prissætte retter i en butik, hvor de ikke er på tilbud. Før anbefalede kortet ikke Netto + Lidl, mens boksen gjorde. Krav: BACKLOG "Én regel for to butikker".

**Afhænger af:** `ai/2026-11-16-et-kort` (bygget oven på den). Slås "Ét kort" sammen først, er denne grens egen ændring kun reglen og dens test og kan rulles tilbage for sig.

**Klasse:** H (ændrer, hvad kortet anbefaler). Ingen pris-, plan- eller listefunktion er ændret; boksens regel er uændret.

**Filer:** `index.html` (`sammKombiTal`, `sammKombiHtml`, udvælgelsen i `sammenlignKombi`), `scripts/tests/sammenlign.js`, `scripts/tests/sammenlign_side.js`, denne rapport.

**Hvad viser kortet nu (denne uges data):**
| Husstand | Forslag | Pris | Billigste enkeltbutik | Spar |
|---|---|---|---|---|
| 2 voksne + 2 børn | Lidl + Netto | 367 kr | Lidl 421 kr | 54 kr |
| 2 voksne | intet (ingen par ≥ 30 kr billigere end Lidl 254 kr) | | | |
| 1 voksen | MENY + REMA | 168 kr | REMA 216 kr | 48 kr |

**Accept:**
- (1) reglen på præcise tal som `anbefaletAntal`: ✓ (node: alle 36 par × 3 husstande).
- (2) vælger man kortets par, anbefaler boksen 2 butikker til præcis kortets pris, og madplanen koster det samme. Node tjekker det for alle anbefalede par; browsertesten trykker på kombiknappen, fx "2 butikker 367 kr Netto og Lidl Anbefalet" og "2 butikker 168 kr REMA 1000 og MENY Anbefalet". ✓
- (3) teksten: begge tal, besparelsen = forskellen, transportsætningen: ✓.
- (4) test opdateret. Mutationsprøve: (a) kortets grænse hævet med 10 kr gav 3 fejl ("anbefalet=false, men forskellen er 31.6 kr"); (b) boksens grænse hævet gav fejl ("kortet anbefaler parret, men 'Hvor mange butikker' anbefaler 1 butik"). ✓
- (5) regression og `budget.js` uændrede (budget-fingeraftryk ac9c5f5cbdb3); før/efter nedenfor: 27 af 27 identiske.

**Layout:** forslaget gør kortet ca. 220 px højere, når det vises (2+2 i denne uge). Browsertestens krav om madplanens placering (Ét kort, accept 5) trækker forslagets højde fra, fordi main's måling (1056 px) ikke havde et forslag. Begge tal udskrives (madplanTop390 = 905, toButiksForslagPx = 222).

**Tidsmåling, ærligt:** på min pc ligger længste opgave lige nu omkring 100–240 ms på både denne gren og "Ét kort", på skift i samme time. Tidligere i dag, efter oprydning, var det 51–122 ms, og kontrollanten målte 0–62 ms i skyen. Forskellen er maskinens belastning, ikke ændringen. Det enkelte trin er én ugeberegning (`simFraButikker`), se BACKLOG "Motoren i trin". Kombiknap-tjekket ligger efter tidsmålingerne, så de to butikker, det vælger, ikke påvirker målingen.

**Før/efter-tal (sidens egne funktioner, main mod grenen, 27 af 27 identiske):**

| Husstand | Butik | Ugepris før | Ugepris efter | Retter | Indkøbslinjer tilbud / øvrige / basis | Ens (samme ret-id'er) |
|---|---|---|---|---|---|---|
| 2+2 | 365discount | 514 | 514 | 7 / 7 | 12 / 11 / 12 | ja |
| 2+2 | Netto | 464 | 464 | 7 / 7 | 11 / 9 / 19 | ja |
| 2+2 | MENY | 658 | 658 | 7 / 7 | 7 / 14 / 15 | ja |
| 2+2 | Bilka | 565 | 565 | 7 / 7 | 7 / 16 / 13 | ja |
| 2+2 | REMA 1000 | 583 | 583 | 7 / 7 | 10 / 14 / 14 | ja |
| 2+2 | Kvickly | 522 | 522 | 7 / 7 | 8 / 16 / 10 | ja |
| 2+2 | Lidl | 421 | 421 | 7 / 7 | 13 / 11 / 16 | ja |
| 2+2 | SPAR | 608 | 608 | 7 / 7 | 8 / 18 / 14 | ja |
| 2+2 | Min Købmand | 595 | 595 | 7 / 7 | 7 / 14 / 13 | ja |
| 2+0 | 365discount | 316 | 316 | 7 / 7 | 8 / 8 / 13 | ja |
| 2+0 | Netto | 269 | 269 | 7 / 7 | 12 / 5 / 18 | ja |
| 2+0 | MENY | 375 | 375 | 7 / 7 | 5 / 12 / 11 | ja |
| 2+0 | Bilka | 376 | 376 | 7 / 7 | 7 / 15 / 11 | ja |
| 2+0 | REMA 1000 | 311 | 311 | 7 / 7 | 10 / 5 / 14 | ja |
| 2+0 | Kvickly | 369 | 369 | 7 / 7 | 8 / 11 / 10 | ja |
| 2+0 | Lidl | 254 | 254 | 7 / 7 | 10 / 10 / 11 | ja |
| 2+0 | SPAR | 400 | 400 | 7 / 7 | 8 / 12 / 16 | ja |
| 2+0 | Min Købmand | 530 | 530 | 7 / 7 | 7 / 16 / 13 | ja |
| 1+0 | 365discount | 236 | 236 | 7 / 7 | 10 / 7 / 12 | ja |
| 1+0 | Netto | 267 | 267 | 7 / 7 | 10 / 9 / 15 | ja |
| 1+0 | MENY | 270 | 270 | 7 / 7 | 6 / 11 / 10 | ja |
| 1+0 | Bilka | 326 | 326 | 7 / 7 | 7 / 14 / 12 | ja |
| 1+0 | REMA 1000 | 216 | 216 | 7 / 7 | 10 / 5 / 14 | ja |
| 1+0 | Kvickly | 306 | 306 | 7 / 7 | 8 / 12 / 7 | ja |
| 1+0 | Lidl | 220 | 220 | 7 / 7 | 10 / 8 / 11 | ja |
| 1+0 | SPAR | 278 | 278 | 7 / 7 | 6 / 13 / 10 | ja |
| 1+0 | Min Købmand | 338 | 338 | 7 / 7 | 5 / 11 / 14 | ja |

**Ikke dækket:** butikslogoer (blokeret lokalt), mørkt tema og rigtig telefon.
