# Backlog (øverst = først)

Ejeren vedligeholder listen. Format (se `agenter/ejer.md`): `- [ ] [UX|DATA|TEST] [A|H] Titel`, med Krav, Hvorfor, Accept og Ikke-mål. UX-udvikleren tager det øverste punkt, som kan gøres på én dag.

## Fra brugerne
(klistr feedback ind her)

## Åbne krav
- [ ] [TEST] [A] Regressionstest af pris, indkøbsliste og ugeforslag i node
  Krav: `scripts/tests/regression.py` (der kalder node) indlæser sidens egen JavaScript (`pris.js`, `kategorier.js`, funktionerne i `index.html`) uden browser og beregner for hver af de 9 butikker ugeforslagets pris, indkøbslistens linjer og et udvalg af retters forbrugs- og indkøbspris. Resultatet sammenlignes med en gemt facitliste (`scripts/tests/facit.json`).
  Hvorfor: uden den kan ingen ændring af priser, mængder eller ugeforslag valideres automatisk, så alle H-ændringer er blokeret.
  Accept: (1) kører i skyen uden internet på under 2 minutter, (2) fanger en bevidst ændring af en prisregel og en ændring af en pakkestørrelse (bevis i rapporten), (3) facitlisten kan opdateres med én kommando, når en ændring er tilsigtet, (4) kaldes af `kontrol.py`, (5) rapporten beskriver, hvad den IKKE dækker.
  Ikke-mål: ændre noget i selve prisberegningen.
- [ ] [DATA] [A] Farverige, spændende aftensretter med blikfang
  Krav: de mest brugte brune retter (pølseret, spanske kødboller, frikadeller, carbonara, hakkebøf) får et friskt tilbehør (råkost, salat, grønt) i opskrift og ingrediensliste; 365discount får mindst 4 vegetarretter; Min Købmand får 2–3 børnevenlige retter i et nyt køkken.
  Hvorfor: ugeforslaget må ikke være fire brune kartoffelretter; farver og variation er forsidens blikfang.
  Accept: (1) alle ændrede retter består `kontrol.py`, (2) hver ændret ret har mindst tre friske farver i ingredienserne, (3) forsidens ugeforslag for 365discount og Min Købmand har mindst tre forskellige køkkener, (4) nye retter har en engelsk billedbeskrivelse i `billedprompts.json`, (5) svinekød udgør højst 35 % af retterne hos Min Købmand og Spar (i dag 24 af 45 og 24 af 53), og suppe-retter (fx pastinaksuppe) har så mættende tilbehør, at de er et hovedmåltid til 4.
  Ikke-mål: ugeforslagets algoritme.
- [ ] [DATA] [A] Ret kendte datafejl
  Krav: Kvickly "Svinemørbrad med svampesauce og kartoffelmos" får svinemørbrad som ingrediens; `ty`-oplysning for ingredienser med tilbud, der mangler den (kontrollen tæller dem; mango, majs, salsa, parmigiano, rygeost m.fl.) via `bibliotek_typer.py`, uden at ramme ikke-mad; dyre andretter (over 450 kr for hele retten) vurderes og fjernes eller laves billigere.
  Hvorfor: tillid til indkøbslisten og et ugeforslag uden urealistisk dyre retter.
  Accept: (1) kontrollens advarsler om disse punkter er væk, (2) ingen ret på forsiden koster over 450 kr, (3) indkøbslisten viser kun den vare, retten bruger, for de rettede ingredienser.
  Ikke-mål: ændre `tilbudVariant()`.
- [ ] [UX] [A] Gode tilbud-grupperne nederst på indkøbslisten
  Krav: gruppetekster er korte og viser det, man kan købe (højst ca. 40 tegn pr. vare), og listen er hurtig at skimme på mobil.
  Hvorfor: de lange gruppetekster ("A, B eller C") forvirrer i butikken.
  Accept: (1) ingen vare i grupperne har tekst over 45 tegn, (2) 400 px bredde uden vandret scroll, (3) designfil med valgt løsning.
  Ikke-mål: ændre hvilke tilbud der vælges.
- [ ] [UX] [H] Banner "Du ser en gemt kopi"
  Krav: når siden er vist fra service workerens cache og ikke fra nettet, forklarer et lille, roligt banner det, med en knap der prøver igen.
  Hvorfor: på netværk, hvor siden er blokeret, ser brugeren forældede data uden at vide det.
  Accept: (1) vises kun ved cache-visning, (2) forsvinder, når frisk data er hentet, (3) rører ikke cache-strategien for billeder, (4) regressionstest består.
  Ikke-mål: ændre hvad der caches.
- [ ] [UX] [A] SEO-gennemgang (kun kortlægning og små rettelser)
  Krav: kortlæg titel, beskrivelse, `og:`-tags, sitemap og robots.txt, og hvad Google kan se (retterne er ikke egne sider). Ret småting; foreslå resten som nye krav.
  Hvorfor: organisk trafik uden betalt annoncering.
  Accept: (1) rapport med fund, (2) små rettelser lagt ind, (3) ingen nye tusinde sider.
  Ikke-mål: bygge opskriftssider.
- [ ] [UX] [A] Tilgængelighed og hastighed på mobil
  Krav: kontrast, tryk-flader, `alt`-tekster og billedstørrelse (kontrollen advarer om billeder over 160 KB).
  Hvorfor: siden bruges mest på telefon i butikken.
  Accept: (1) ingen billeder over 160 KB, (2) alle billeder har `alt`, (3) tryk-flader mindst 44 px på forsiden og indkøbslisten.
  Ikke-mål: nyt design.
- [ ] [DATA] [H] Næring pr. voksen i Fitness
  Krav: kategorien Fitness regner næring pr. voksen i stedet for pr. gennemsnitsportion (børn spiser mindre).
  Hvorfor: tallene skal passe til, hvad en voksen faktisk spiser.
  Accept: (1) forklaret i teksten på siden, (2) regressionstest og før/efter-tal, (3) `naering.json` bygges med den nye regel.
  Ikke-mål: ændre andre kategorier.

- [ ] [TEST] [A] Hold genererede filer ude af commits
  Krav: `scripts/_tjek_fund.json` (skrives af `tjek_opskrifter.py`) kommer i `.gitignore`.
  Hvorfor: den kom med i en commit ved et uheld 2026-11-15.
  Accept: (1) filen er ignoreret, (2) `git status` er ren efter en kørsel af `kontrol.py`.
  Ikke-mål: røre andre filer.

## Afvist / parkeret
(ingen)
