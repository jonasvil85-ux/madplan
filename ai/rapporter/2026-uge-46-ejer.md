# Ejerens ugerapport, uge 46 (søndag 2026-11-15)

## Efterkontrol
- **Godkendt:** `ai/2026-11-15-kontrol-jsonld` (klasse A, kun test). Kontrollen er nu grøn på main: `RESULTAT: BESTÅET (0 fejl, 9 advarsler)` (kørt af mig). Ingen brugerflade ændret, ingen andre sammenlægninger siden sidst.
- Ikke tjekket: den udgivne side. `ai/HELBRED.md` og `ai/DAGENS.md` findes ikke endnu i repoet (Vagtposten har ikke kørt); `scripts/konkurrenter/` findes ikke, så konkurrentgennemgangen er udeladt.

## Gennemgang af 10 retter (tilfældigt udvalg på tværs af alle 9 butikker, læst ned til ingredienser)
Risotto med kylling (Netto), Chili con carne (Meny), Kødboller i tomatsauce (Bilka), Torsk med kikærter og spinat (Rema), Hakkebøf med portobello og pastinakmos (Kvickly), Rødbederisotto (Lidl), Spanske kødboller (365), BBQ-kyllingelår med coleslaw (Spar), Røget laks og rejer med kartoffelsalat (Min Købmand), Æggekage med bacon (Netto).
- Alle er aftensmad, ingen desserter/morgenmad. Køkkenerne varierer (italiensk, amerikansk, middelhav, dansk). Chili, torsk/kikærter/spinat, BBQ med coleslaw og rødbederisotto er farverige.
- Svagt: Kødboller (Bilka) og Spanske kødboller (365) er næsten ens og brune uden grønt; Hakkebøf med pastinakmos har ingen frisk farve; Æggekage med bacon og tomat er let til 4 (8 æg, 200 g bacon, ingen kartofler/brød). Alle ni butikker har kun 3–7 vegetarretter.
- Mærkelig kombination: "paprika (røget) og spidskommen" er én ingrediens, og "risottoris eller kogt ris" – gruppetekster i ingredienslisten.

## Hvad gik godt / galt
- Godt: alle retter har billede, 6 køkkener i hver butik, kontrollen er grøn.
- Galt (fakta fra kontrollen): andelår 730 og 758,5 kr (Bilka) og helstegt and 566 kr (Min Købmand); Kvickly-svinemørbrad mangler svinemørbrad som ingrediens; 25 Netto-ingredienser mangler `ty`; 188 ubrugte billeder. Min Købmand og Spar: svin 24 af 45 og 24 af 53 retter.
- Brugerne mangler sandsynligvis (jeg har ingen brugerdata): tillid til indkøbslisten og mere grønt/vegetar. Det er en antagelse.

## Tre mål til næste uge
1. Regressionstesten (frigør alle H-ændringer).
2. Datafejl: dyre andretter, Kvickly-svinemørbrad, manglende `ty`.
3. Farverige retter med friskt tilbehør og mindre svin hos Min Købmand/Spar.

## Backlog
Øverste 5 har fuldt krav. Tilføjet accept (5) til farveretter (svin-andel, mættende supper) og et lille TEST-punkt om `.gitignore`.

## Forslag til grundloven
Ingen.
