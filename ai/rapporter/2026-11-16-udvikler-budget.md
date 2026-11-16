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

---

## Forsøg 2 (2026-11-16, efter kontrollantens afvisning og Jonas' ekstra krav)

**Kontrollantens fund rettet:** efter "Byt" kaldte beskeden brugerens ændrede plan "billigste uge". Nu: er planen ændret (`simAendret(k)`), siger beskeden "Din madplan koster X kr – Y kr over dit budget på B kr. Vores forslag for ugen koster Z kr." (eller "Din madplan er inden for dit budget"). Har brugeren fjernet dage, står antallet ("Din madplan (5 dage)"). "Billigste uge" står kun om forslaget selv (`simPris(k)`).

**Præcis sammenligning:** beskeden sammenligner nu den præcise pris med budgettet, ikke den afrundede. Kontrollantens eksempel SPAR 600,x kr mod 600 kr hedder nu "over dit budget", ikke "600 kr af 600 kr". Overskridelsen er den viste pris minus budgettet, så tallene går op for brugeren (406 kr − 300 kr = "106 kr over"), og aldrig "0 kr over" (mindst 1 kr, når den præcise pris er over).

**Hastighed (kontrollanten bad om måling):** budgettet regnede ugen uden budget igen ved hver ændring. Nu bevares de beregnede uger, når kun budgettet ændres (`nulstilBudget()` nulstiller kun brugerens egne byt; mellemlagrene er i forvejen gemt pr. husstand og budget). Målt i headless Edge (PerformanceObserver longtask, rigtige data), længste opgave efter budgetændring:

| Butikker | Før (forsøg 1) | Nu |
|---|---|---|
| Lidl, budget 300 | 195 ms | under 50 ms |
| MENY, budget 600 | 150 ms | 0–75 ms |
| Netto+Lidl, budget 350 | 240 ms | 0–50 ms |
| REMA+Bilka+SPAR, budget 450 | 223 ms | 57–106 ms |

**Uafhængig af sammenlign-butikker:** "Fjern"-knappen har nu sin egen klik-lytter, så den fælles klik-vælger i index.html er uændret i forhold til main, og kontrolblokken ligger som "7b." et andet sted end sammenligningens "9."; `git merge-tree` mod sammenlign-butikker: ingen konflikt. De to grene rører ikke længere de samme linjer.

**Jonas' grænsetilfælde (accept 6), alle i `scripts/tests/budget.js`, kørt automatisk af `kontrol.py`:**
- 9 butikker × 3 husstande (2+2, 2+0, 1+0) × budget præcis lig ugeprisen, 1 kr under, 1 kr over, 1 kr og 50 kr: 7 retter, aldrig dyrere, uændret uge når budget ≥ pris, og beskeden passer til tallet (inden for/over, og den rigtige overskridelse).
- Ændring af familiestørrelse efter budgettet (9 butikker × 3 skift: 2+2→1+0, 1+0→2+2, 2+0→2+3, via `saetHusstand` som knapperne): budgettet bevares og gemmes, og ugen er præcis den samme som regnet forfra for den nye husstand.
- Byt-scenariet: 9 butikker × budget 300 og 100000, byt mandag–onsdag.
- Mellemlageret: 11 butiksvalg (9 enkelte, Netto+Lidl, REMA+Bilka+SPAR) × 2 husstande. Budgettet skiftes frem og tilbage via feltets vej og skal give samme uge og pris som regnet helt forfra.

**Gentagelighed (accept 8):** testen udskriver et fingeraftryk af alle tal. To kørsler på samme data gav samme fingeraftryk.

**Testen kan fejle (mutationsprøve):** jeg lavede tre bevidste fejl i en kopi, og testen fangede alle: fjernet "aldrig dyrere"-vagten, afrundet sammenligning i beskeden (57 fejl), og den gamle Byt-besked. Testkoden er kørt i headless Edge mod sidens egne funktioner: `FEJL: []`, 27 kombinationer + 180 grænsetilfælde. Lokalt er der ingen node, så node-kørslen af selve filen gøres af kontrollanten.
