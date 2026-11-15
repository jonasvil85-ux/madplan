# Udviklerrapport 2026-11-15 – fravalg og budget (bygget af Claude i chatten på Jonas' bestilling)

**Hvad:** (1) **Fravalg:** i "Dine valg"-boksen kan brugeren vælge "Vi spiser ikke …": svinekød, okse og kalv, kylling og and, fisk og skaldyr, kød og fisk (kødfri), løg, svampe, mælkeprodukter, æg. Forslag, "Vælg selv" og "Byt" viser kun retter uden det valgte. (2) **Budget:** et valgfrit felt "Budget for ugens aftensmad". Ugeforslaget søger en uge under budgettet, og en besked siger ærligt, om det lykkedes. Begge gemmes på enheden og på brugeren.

**Hvorfor:** ROADMAP 3 og 4. Uden fravalg kan mange familier ikke bruge forslaget; uden budget tænker siden i kroner pr. ret i stedet for kroner pr. uge.

**Klasse:** H (ændrer ugeforslagets beregning, `simFraButikker`, `pool`, `simSig`).

**Filer:** `index.html` (fravalgsdefinitioner og filter i `pool`, budgetstraf og sammenligning i ugeforslaget, boks, beskeder, CSS, gem/hent), `scripts/tests/fravalg_budget.js` (ny test), `scripts/tests/kontrol.py` (kører testen), `ai/design/2026-11-15-fravalg-budget.md`, denne rapport.

**Accept:**
1. Fravalg respekteres overalt: uge, "Vælg selv" (171 → 125 retter ved svin-fravalg på Lidl), byt. Uafhængig tjek med en separat liste af svinekødsord: 0 brud i alle 9 butikker.
2. Budget gør aldrig ugen dyrere end uden budget (testet for 7 budgetter × 9 butikker) og ændrer ikke ugen, når budgettet ≥ ugens pris (testet).
3. Ærlig besked: grøn når budgettet holdes, gul med billigste pris når det ikke kan.
4. For restriktive fravalg (færre end 12 retter) bruges ikke, og forslaget går ikke i stykker (testet med alle 9 fravalg).
5. Valg huskes efter genindlæsning (set i browser).
6. Uden fravalg og budget er alt uændret: ugepriserne er identiske med før (tabel nedenfor).

**Før/efter-tal (sidens egen JavaScript i headless Edge; 2 voksne + 2 børn; én butik ad gangen):**

| Butik | Uge før (ingen valg) | Uge efter (ingen valg) | Uden svinekød | Med budget 500 | Retter i "Vælg selv" |
|---|---|---|---|---|---|
| 365discount | 514 | 514 | 586 | 496 | |
| Netto | 464 | 464 | 568 | 464 | |
| MENY | 658 | 658 | 770 | 658 (kan ikke holdes) | |
| Bilka | 565 | 565 | 534 | 539 (kan ikke holdes) | |
| REMA 1000 | 583 | 583 | 644 | 566 | |
| Kvickly | 522 | 522 | 616 | 501 | |
| Lidl | 421 | 421 | 585 | 421 | 171 → 125 (svin) |
| SPAR | 608 | 608 | 756 | 580 | |
| Min Købmand | 595 | 595 | 939 | 595 (kan ikke holdes) | |

"Uge før" er målt på `main` med `pris` fra ugeforslaget; "uge efter" på grenen. Alle ni er identiske. Bilka uden svinekød (534) er billigere end med (565): ugeforslagets søgning er heuristisk og ikke garanteret optimal; det er ikke indført af denne ændring.

**Test:** (a) `scripts/tests/fravalg_budget.js` (ny; node, frossen datakopi): *kunne ikke køres lokalt (ingen node)*; samme testkode er kørt i headless Edge mod sidens funktioner: `FEJL: []` for alle 9 butikker. Den fandt undervejs en rigtig fejl i mit første udkast (et budget lig ugens pris ændrede ugen) som er rettet. (b) UI klikket igennem på 390 og 1100 px: boksen, fravalg, budget, besked, gem og genindlæsning; ingen JavaScript-fejl. (c) `kontrol.py` lokalt: `RESULTAT: BESTÅET`. (d) `regression.py` skal køres af kontrolløren; den dækker standardvalget, som er uændret (tabel).

**Dækker IKKE:** allergisikkerhed (fravalg er ordsøgning i ingredienser og kategori, ikke en garanti; siden siger det); ingredienser stavet usædvanligt kan slippe igennem; "Kød og fisk" tæller en vegetarret med fisk i en ingrediens som ikke kødfri; kun for én husstandsstørrelse testet (2+2) i budget-testen; flere butikker samtidig er ikke dækket af den nye test (kun én butik ad gangen); brugere uden fravalg/budget er ikke ændret.

**Fund undervejs:** de fleste butikker har for få vegetarretter til en kødfri uge (kun Lidl har 12 eller flere): fravalget "Kød og fisk" bruges derfor ikke og siden siger det. Det er en datamangel, ikke en fejl i funktionen.

**Kontrolløren bør kigge på:** `index.html`-diffen (især `pool`, `simSig` og slutningen af `simFraButikker`), at `regression.py` er uændret, at `fravalg_budget.js` består i skyen, og at `retter.json`/`opskrifter.json` er uændrede.

**Næste skridt:** (1) Vegetarretter pr. butik (DATA): mindst 12 kødfri retter i hver butik. (2) Giv budgettet en pænere forklaring af, hvilken butik der er billigst. (3) Tæl fravalg på mobilknappen (kun et badge i dag). (4) Test af flere butikker på én gang.
