# Udviklerrapport 2026-11-16 – budget (adskilt fra fravalg, på Jonas' beslutning)

**Hvad:** Et valgfrit felt "Budget for ugens aftensmad" i "Dine valg"-boksen. Ugeforslaget søger en uge under budgettet; en besked under "Madplan" siger ærligt, om det lykkedes ("Inden for dit budget: 421 kr af 450 kr" eller "Billigste uge vi kan finde her koster X – Y kr over dit budget"). Budgettet gemmes på enheden og på brugeren. **Ingen afhængighed af fravalg:** ingen fravalgskode er med.

**Hvorfor:** familier tænker i kroner pr. uge. Krav "Budget: Højst X kr for ugen" i BACKLOG; designfil `ai/design/2026-11-16-budget.md` (UX-designeren).

**Klasse:** H (ugeforslagets beregning: `simFraButikker`, `simSig`).

**Filer:** `index.html`, `scripts/tests/budget.js` (ny), `scripts/tests/kontrol.py` (kører den), denne rapport.

**Sådan virker beregningen:** hver krone over budgettet tæller 6 gange så tungt i søgningen. Derefter regnes også ugen uden budget: holder den budgettet, bruges den uændret; ellers vælges den bedste af de to. Derfor kan et budget aldrig gøre ugen dyrere, og et budget over ugens pris ændrer intet.

**Accept:** (1) felt i husstandsboksen: ja; (2) ugeforslaget holder 600 kr i 8 af 9 butikker for 2+2 (kontrollanten målte det samme i går; kun MENY 658 kan ikke); (3) uopnåeligt budget giver en klar besked med billigste pris: ja; (4) regressionstesten uændret for brugere uden budget: lister og ugepriser identiske (tabel); (5) før/efter-tal: tabel.

**Før/efter-tal for alle 9 butikker uden budget (2 voksne + 2 børn; sidens egne funktioner `simFraButikker`, `ugePris`, `listeLinjer`, `prisSum`; main mod grenen):**

| Butik | Ugepris før | Ugepris efter | Indkøbslinjer tilbud / øvrige / basis | Listens sum (kr) | Ens |
|---|---|---|---|---|---|
| 365discount | 514 | 514 | 12 / 11 / 12 | 707 | ja |
| Netto | 464 | 464 | 11 / 9 / 19 | 780 | ja |
| MENY | 658 | 658 | 7 / 14 / 15 | 865 | ja |
| Bilka | 565 | 565 | 7 / 16 / 13 | 767 | ja |
| REMA 1000 | 583 | 583 | 10 / 14 / 14 | 792 | ja |
| Kvickly | 522 | 522 | 8 / 16 / 10 | 656 | ja |
| Lidl | 421 | 421 | 13 / 11 / 16 | 637 | ja |
| SPAR | 608 | 608 | 8 / 18 / 14 | 825 | ja |
| Min Købmand | 595 | 595 | 7 / 14 / 13 | 785 | ja |

**Test:** `scripts/tests/budget.js` (node, frossen datakopi) tester 3 husstande (2+2, 2+0, 1+0) × 9 butikker × 7 budgetter: aldrig dyrere, altid 7 retter, budget ≥ ugens pris ændrer ikke ugen, samme valg giver samme uge, ugyldige gemte værdier (tekst, negativ, 1e9, null) giver intet nedbrud. Kunne ikke køres lokalt (ingen node); samme testkode er kørt i headless Edge mod sidens funktioner: `FEJL: []` (27 kombinationer). Testen fandt undervejs en afrundingsfejl i testen selv (et budget lig den afrundede pris var 0,4 kr under den præcise); rettet til at bruge præcise priser. UI klikket igennem på 390 og 1100 px: felt, besked, gem og genindlæsning; ingen JavaScript-fejl. `kontrol.py` lokalt: `RESULTAT: BESTÅET`.

**Dækker IKKE:** flere butikker samtidig i den faste test (logikken er den samme, men ikke testet); søgningen finder ikke garanteret den billigst mulige uge (heuristik), kun aldrig en dyrere end uden budget.

**Kontrolløren bør kigge på:** slutningen af `simFraButikker` (sammenligning med ugen uden budget og rekursionsvagten `simUdenBudget`), `simSig`, og at grenen ikke indeholder noget fravalg.
