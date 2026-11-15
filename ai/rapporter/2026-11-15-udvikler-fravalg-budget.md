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


**Indkøbslistens linjer og summer (før = main, efter = grenen; ugeforslagets valgte retter, 2 voksne + 2 børn, én butik; målt med sidens `listeLinjer()` og `prisSum()` i headless Edge):**

| Butik | På tilbud (linjer) | Øvrige | Basisvarer | Sum for listen (kr) | Ugepris | Før = efter |
|---|---|---|---|---|---|---|
| 365discount | 12 | 11 | 12 | 707 | 514 | ja |
| Netto | 11 | 9 | 19 | 780 | 464 | ja |
| MENY | 7 | 14 | 15 | 865 | 658 | ja |
| Bilka | 7 | 16 | 13 | 767 | 565 | ja |
| REMA 1000 | 10 | 14 | 14 | 792 | 583 | ja |
| Kvickly | 8 | 16 | 10 | 656 | 522 | ja |
| Lidl | 13 | 11 | 16 | 637 | 421 | ja |
| SPAR | 8 | 18 | 14 | 825 | 608 | ja |
| Min Købmand | 7 | 14 | 13 | 785 | 595 | ja |

Alle tal er identiske før og efter i alle 9 butikker.

---

## Forsøg 2 (efter kontrollantens afvisning)

Kontrolløren fandt tre rigtige huller og en for svag test. Alt er rettet:

| Fund | Rettelse |
|---|---|
| (a) "Kød og fisk" lod lammegryde (`lammekød`) slippe igennem | Ordlisten for kød har nu alle lammeord fra `bibliotek_typer.py` (lammekød, -kølle, -culotte, -kotelet, -fars, -skank, -lår, -steg, -bov, -gryde), samt krondyr, hjort, vildt, vildsvin, vildand, salami og spegepølse. "Lammefjordskartofler" er stadig ikke kød. |
| (b) "Mælkeprodukter" lod ost slippe igennem i 8 af 9 butikker | Alle ostetyper er med: mozzarella, feta, parmesan, grana/padano, cheddar, gouda, havarti, emmentaler, danbo, brie, camembert, halloumi/grillost, philadelphia, ricotta, gorgonzola/blåskimmel, paneer (plus mælk, fløde, smør, yoghurt, skyr, creme fraiche, kefir, ymer, mascarpone). |
| (c) "Løg" lod porre slippe igennem | `porre` er med under "Løg". |
| Test for svag (kun svin, regex som delmængde af implementeringens) | `fravalg_budget.js` tester nu alle ni fravalg mod en uafhængig ordliste (bygget ud fra typerne i `bibliotek_typer.py`) over HELE puljen i hver af de 9 butikker, ikke kun ugens retter. |

**Resultat:** testkoden kørt i headless Edge mod sidens funktioner: `FEJL: []`; 73 fravalg-kombinationer afprøvet over hele puljen (9 butikker × 9 fravalg, minus 8 hvor fravalget efterlader under 12 retter og derfor bevidst ikke bruges; det er de vegetariske, som kun Lidl kan: 13 retter). Lammegryden er ude af Lidls kødfri pulje. Uge og budget er uændrede (ugepriser uden valg: 514/464/658/565/583/522/421/608/595; budgettest uændret grøn). Det kan ikke ses i denne rapport, at node-udgaven er kørt i skyen: det gør kontrolløren.

**Størrelse af puljen efter fravalg** (retter at vælge imellem, én butik): alle 58–171; uden svin 24–125; uden okse 51–141; uden fjerkræ 47–115; uden fisk 47–142; uden løg og porre 25–47; uden svampe 56–164; uden mælkeprodukter 14–50; uden æg 39–142. Kødfri: kun Lidl (13); de andre 3–8.

**Ærlig begrænsning:** den uafhængige ordliste er skrevet af den samme (mig) som implementeringen, selv om den er bygget fra typefilen; en ukendt stavemåde kan stadig slippe igennem. Fravalg er ikke en allergigaranti, og siden siger det.

**Næste skridt:** (1) Mindst 12 kødfri retter pr. butik (DATA). (2) Test for 2+0 og 1+0 i budget (kontrollanten kørte dem, men de er ikke i den faste test). (3) UI-test i Browser-QA.
