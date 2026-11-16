# Backlog (øverst = først)

Ejeren vedligeholder listen. Format (se `agenter/ejer.md`): `- [ ] [UX|DATA|TEST] [A|H] Titel`, med Krav, Hvorfor, Accept og Ikke-mål. UX-udvikleren tager det øverste punkt, som kan gøres på én dag.

## Fra brugerne
(klistr feedback ind her)

## Åbne krav
- [ ] [UX] [H] Én regel for to butikker (Jonas 2026-11-16: "Vælger man flere butikker skal det jo gerne blive billigere"; afløser (11)'s del (a) i "Sammenlign butikker". Bygges oven på "Ét kort")
  Krav: kortets to-butiks-forslag og boksen "Hvor mange butikker" bruger samme regel: to butikker anbefales, når deres fælles billigste uge (én samlet indkøbsliste over begge, egne tilbud) er mindst ANBEFAL_SPAR (30 kr) billigere end den billigste enkeltbutiks uge. Begge uger er 7 aftensmåltider til husstanden med samme portioner. Fravalgt: at prissætte parrets retter i én butik (urimeligt over for butikker uden tilbud på retterne, Jonas' pointe).
  Hvorfor: kortet anbefalede ikke Netto + Lidl (367 kr mod Lidls 421 kr), mens boksen gjorde. Brugeren sparer reelt 54 kr ved at handle i begge, uden at få mindre mad.
  Accept: (1) kortet viser kombinationen, når (enkeltbutikkens uge − parrets uge) ≥ ANBEFAL_SPAR, regnet på præcise tal som boksens `anbefaletAntal`; blandt flere vises den billigste uge; (2) vælger man kortets par, anbefaler boksen 2 butikker, og madplanen koster præcis kortets pris (automatisk test for 2+2, 2+0, 1+0); (3) teksten viser parrets pris og enkeltbutikkens pris, besparelsen = forskellen på de viste tal, og at transport og ekstra tid ikke er regnet med; (4) sammenlign.js og browsertesten er opdateret og består; mutationsprøve af reglen; (5) regression og budget uændrede; før/efter-tal.
- [ ] [UX] [H] Ét kort: "Hvor handler du?" og "Sammenlign butikker" lagt sammen (Jonas godkendte 2026-11-16; designfil ai/design/2026-11-16-hvor-handler-du-samlet.md) (gren ai/2026-11-16-et-kort AFVIST forsøg 1 2026-11-16: fejltekst "vælge butik ovenfor" er forkert efter omlægningen; H-plads brugt; resten bestået)
  Krav: forsiden har ét kort om butiksvalg. Den rangerede liste (hver butiks billigste uge ud fra dens egne tilbud) ER butiksvalget; logo-gitteret og "Hvor mange butikker" ligger bag "Vælg selv flere butikker".
  Hvorfor: siden stillede samme spørgsmål to gange med samme logoer og tal, og madplanen blev skubbet ca. 1.050 px ned på telefonen.
  Accept: (1) kun ét kort om butiksvalg på forsiden: ingen separat "Sammenlign butikker"-overskrift, og logo-gitteret er skjult på første skærm, når der er valgt én butik; (2) alle tal og accept (1)–(12) for "Sammenlign butikker" gælder uændret (sammenlign.js og browsertesten består); (3) tryk på en række vælger butikken, kombiknappen som før; (4) "Vælg selv flere butikker" (knap med aria-expanded) viser det eksisterende logo-valg og "Hvor mange butikker", og det er åbent af sig selv, når der er valgt mere end én butik; flerbutiksvalget virker som før (afkrydsning, antal butikker, madplan); (5) madplanen (#sim-plads) starter mindst 300 px højere på 390 px end på main; (6) rundvisningens trin peger kun på synlige områder (trin 2 = listen, trin 3 = "Vælg selv flere butikker"); (7) regressionstest, budget.js uændrede; 390 px uden vandret scroll; tryk-flader ≥ 44 px; (8) teksten siger, at prisen er hver butiks billigste uge ud fra dens egne tilbud, til den valgte husstand; (9) (1), (4), (5) og (6) testes automatisk i Chromium (scripts/tests), ikke ved manuelle forsøg; (10) før/efter-tal for alle 9 butikker.
  Ikke-mål: ændre priser, ugeforslag eller to-butiks-reglen; "samme madplan i alle butikker" (fravalgt: urimelig over for butikker uden tilbud på retterne).
- [x] [UX] [H] Sammenlign alle butikker på forsiden (CTO-prioritet 1) (slået sammen 2026-11-16 af kontrollanten, 25d3cb7, forsøg 2; skærpet validering bestået)
  Krav: under "Hvor handler du?" vises en rangeret liste over alle 9 butikker med ugens pris for brugerens husstand (samme beregning som ugeforslaget, én butik ad gangen), besparelse mod normalpris og andel på tilbud. Den billigste er markeret "Billigst". Et tryk på en butik vælger den (som at krydse den af alene). Under listen vises den bedste kombination af to butikker, hvis den er mindst 30 kr billigere end den billigste enkeltbutik. Tallene regnes i baggrunden butik for butik og vises efterhånden; siden må aldrig fryse.
  Hvorfor: "Hvor skal jeg handle i denne uge?" er kernespørgsmålet for en tilbudsside, og det kræver i dag mange klik. Konkurrenten Goma reklamerer netop med prissammenligning.
  Accept: (1) alle 9 butikker vises med en pris, der er identisk med den pris, siden viser, når butikken vælges alene (testet for alle 9); (2) listen er sorteret billigst først, og "Billigst" står på den billigste; (3) et tryk vælger butikken og opdaterer madplanen; (4) første skærm vises før beregningen er færdig, og hovedtråden blokeres aldrig mere end 200 ms ad gangen (målt i Chromium); (5) 390 px uden vandret scroll, tryk-flader mindst 44 px; (6) regressionstesten uændret; (7) designfil i ai/design/; (8) **samme forudsætninger overalt** (Jonas 2026-11-16): alle priser og besparelser regnes for den valgte husstand (voksne og børn) med samme funktioner som resten af siden (`simFraButikker`/`ugePris`, indkøbspris i hele pakker, normalpris for samme varer); testet for 2+2, 2+0 og 1+0; (9) **kombinationen er reelt billigere**: prisen for to butikker regnes som én samlet indkøbsliste over begge butikker (`ugePris` med begge, så pakker og dobbeltindkøb tælles), den eksisterende tidsstraf for en ekstra butik (`STRAF_PR_EKSTRA_BUTIK`) skal være overvundet, og teksten siger ærligt, at transport ikke er regnet med i kroner; (10) besparelsen "Sparer X kr" er normalpris minus indkøbspris for præcis de samme varer, som siden allerede viser, og overdrives aldrig; (11) **samme mad og samme mængder** (Jonas 2026-11-16, "ingen besparelse, der skyldes, at brugeren reelt får mindre"): hver butiks pris gælder 7 aftensmåltider for den valgte husstand med samme portioner pr. person (`planMult` for husstanden, hele pakker), aldrig færre retter eller mindre portioner; kortet skriver, at prisen er hver butiks billigste uge med 7 aftensmåltider til N personer. For kombinationen gælder: den viste besparelse = det mindste af (a) prisen for **præcis samme retter og mængder** købt i den billigste enkeltbutik minus prisen i de to butikker og (b) den billigste enkeltbutiks egen uge minus prisen i de to butikker. Er det mindste under 30 kr, vises kombinationen ikke; (12) **automatisk og gentagelig test** (Jonas 2026-11-16): `scripts/tests/sammenlign.js` (node, frossen datakopi og frosset ur som regression.js) kører fra `kontrol.py` og efterprøver (1), (2), (8), (9), (10) og (11) for 2+2, 2+0 og 1+0 ved selv at regne priserne igen med sidens egne funktioner. At bestemte tekststrenge findes i koden, tæller ikke som test. (4) og (5) måles automatisk i Chromium (Browser-QA eller et script i scripts/tests), ikke ved manuelle forsøg. Samme kørsel to gange skal give samme tal.
  Ikke-mål: ændre prisberegningen, ugeforslaget eller butiksvalget for brugere, der ikke trykker i listen.
- [x] [TEST] [A] Regressionstest af pris, indkøbsliste og ugeforslag i node
  Krav: `scripts/tests/regression.py` (der kalder node) indlæser sidens egen JavaScript (`pris.js`, `kategorier.js`, funktionerne i `index.html`) uden browser og beregner for hver af de 9 butikker ugeforslagets pris, indkøbslistens linjer og et udvalg af retters forbrugs- og indkøbspris. Resultatet sammenlignes med en gemt facitliste (`scripts/tests/facit.json`).
  Hvorfor: uden den kan ingen ændring af priser, mængder eller ugeforslag valideres automatisk, så alle H-ændringer er blokeret.
  Accept: (1) kører i skyen uden internet på under 2 minutter, (2) fanger en bevidst ændring af en prisregel og en ændring af en pakkestørrelse (bevis i rapporten), (3) facitlisten kan opdateres med én kommando, når en ændring er tilsigtet, (4) kaldes af `kontrol.py`, (5) rapporten beskriver, hvad den IKKE dækker.
  Ikke-mål: ændre noget i selve prisberegningen.
- [x] [UX] [H] Opskriftssider til Google (slået sammen 2026-11-15 af kontrollanten, 384f5d1)
  Krav: hver af de 193 biblioteksopskrifter får en egen side `/opskrift/<navn>/` med billede, ingredienser til 4, trin, tid, næring og Recipe-struktureret data, plus en oversigt `/opskrifter/` og sitemap.
  Hvorfor: siden har kun én URL, så Google ser ingen retter. Organisk trafik er den største vækstmulighed uden annoncer.
  Accept: (1) 193 sider + oversigt, (2) gyldig Recipe-JSON-LD på hver, (3) sitemap med alle, (4) kontrollen tjekker at hver opskrift har en side, (5) sider bygges af `scripts/byg_sider.py`, (6) ingen priser eller datoer på siderne (de bliver gamle).
  Ikke-mål: ændre appen eller prisberegningen.
- [ ] [DATA] [H] Ret kendte datafejl (gren ai/2026-11-16-datafejl AFVIST forsøg 1 2026-11-16: klasse H, før/efter mangler ugepris og indkøbslinjer for 9 butikker, 16 ty-advarsler tilbage; se kontrolrapporten)
  Krav: Kvickly "Svinemørbrad med svampesauce og kartoffelmos" får svinemørbrad som ingrediens; `ty`-oplysning for ingredienser med tilbud, der mangler den (kontrollen tæller dem; mango, majs, salsa, parmigiano, rygeost m.fl.) via `bibliotek_typer.py`, uden at ramme ikke-mad; dyre andretter (over 450 kr for hele retten) vurderes og fjernes eller laves billigere.
  Hvorfor: tillid til indkøbslisten og et ugeforslag uden urealistisk dyre retter.
  Accept: (1) kontrollens advarsler om disse punkter er væk, (2) ingen ret på forsiden koster over 450 kr, (3) indkøbslisten viser kun den vare, retten bruger, for de rettede ingredienser.
  Ikke-mål: ændre `tilbudVariant()`.
- [ ] [UX] [A] Mobil: tryk-flader og luft (ROADMAP 2) (AFVIST forsøg 1 2026-11-15; AFVIST forsøg 2 2026-11-16 og PARKERET hos Ejeren: "Om Måltidsjagten" i sidefoden 95 × 14 px, accept (4) billeder ikke gjort – foreslås flyttet til eget H-krav)
  Krav: alle knapper og links på forsiden, retter og indkøbsliste er mindst 44 × 44 px på telefon (i dag er 25–27 elementer under 32 px).
  Hvorfor: siden bruges mest på telefon i butikken, og små knapper giver forkerte tryk.
  Accept: (1) måling i CDP-audit viser 0 elementer under 40 px på 390 px bredde (undtagen tekstlinks i brødtekst), (2) intet vandret scroll på 360 px, (3) designfil med før/efter.
  Ikke-mål: nyt design.
  Tilføjet af Ejeren 2026-11-16: slår "Tilgængelighed og hastighed" sammen hertil – også (4) ingen billeder over 160 KB, (5) alle billeder har alt, (6) UX-designeren laver designfilen FØR udvikleren bygger (afvist sidst fordi den manglede).
- [x] [UX] [H] Budget: "Højst X kr for ugen" (ROADMAP 3) (SLÅET SAMMEN 2026-11-16 af kontrollanten, f1c3024, forsøg 3; opfølgning: beskeden "600 kr – 1 kr over 600 kr" bør vise øre, designfilens chips er ikke bygget, et budget over ugens pris kan ændre ugen ved flere butikker) (gren ai/2026-11-16-budget AFVIST forsøg 1 2026-11-16: "billigste uge" efter Byt; AFVIST forsøg 2 2026-11-16: budget.js fejler i node – `sb is not defined`, kontrol.py rød; ét forsøg tilbage) (gren ai/2026-11-15-fravalg-budget PARKERET 2026-11-16 sammen med fravalg; budgetdelen er i orden – 8/9 butikker under 600 kr – og bør bygges som egen gren)
  Krav: brugeren kan skrive et ugebudget (fx 600 kr), og ugeforslaget holder sig under det, hvis det kan lade sig gøre; ellers fortæller siden ærligt, hvad den billigste mulighed koster.
  Hvorfor: familier tænker i kroner pr. uge, ikke i kroner pr. ret. Det er den funktion, konkurrenter fremhæver mest.
  Accept: (1) budgetfelt i husstandslinjen på forsiden, (2) ugeforslaget overholder budgettet i mindst 7 af 9 butikker ved 600 kr, (3) uopnåeligt budget giver en klar besked med billigste pris, (4) regressionstest uændret for brugere uden budget, (5) før/efter-tal for alle 9 butikker; (6) **grænsetilfælde** (Jonas 2026-11-16) testes for alle 9 butikker og 2+2, 2+0 og 1+0: budget præcis lig ugeprisen, 1 kr under og 1 kr over, meget lavt budget (1 kr og 50 kr), og ændring af familiestørrelse efter budgettet er tastet (budgettet bevares, ugen regnes igen for den nye husstand og følger stadig reglerne); (7) budgetfunktionen afhænger ikke af fravalg; (8) testene er automatiske og gentagelige: `scripts/tests/budget.js` (node, frossen datakopi) kører fra `kontrol.py`, og to kørsler giver samme resultat.
  Ikke-mål: ændre prisregler.
- [ ] [UX] [H] Motoren i trin: del `simFraButikker` op (Ejer 2026-11-16, fundet under sammenlign-butikker; IKKE påbegyndt, lav prioritet)
  Krav: én beregning af én uge kan i dag tage 60–280 ms i ét stræk (GC-pauser), også på main uden nye funktioner. Del den i trin med pause imellem uden at ændre resultatet.
  Accept: (1) regression.py, budget.js og sammenlign.js uændrede; (2) ingen opgave over 100 ms i sammenlign_browser.py over 5 kørsler; (3) før/efter-tal for alle 9 butikker.
- [ ] [UX] [H] Fravalg og kost: "Vi spiser ikke …" (ROADMAP 4) (AFVIST forsøg 1 2026-11-15; AFVIST forsøg 2 2026-11-16 og PARKERET hos Ejeren: mayonnaise/remoulade under Æg, pesto under Mælkeprodukter, "hakket kød" (svin+kalv) under Okse og kalv; se kontrolrapporten 2026-11-16)
  Krav: brugeren kan fravælge ingredienser og kosttyper (svinekød, fisk, løg, laktose, vegetar), og forslag, "Vælg selv" og indkøbsliste respekterer det.
  Hvorfor: uden fravalg kan mange familier ikke bruge forslaget; det er en forudsætning for gentagne besøg.
  Accept: (1) valget gemmes (lokalt og i konto), (2) ingen foreslået ret indeholder en fravalgt ingrediens (testes i regression), (3) tydelig besked, hvis for få retter er tilbage, (4) før/efter-tal.
  Ikke-mål: allergi-garantier. Siden må ikke love, at noget er allergensikkert.
- [ ] [UX] [A] Gemte madplaner og favoritter (ROADMAP 5)
  Krav: en bruger med konto kan gemme en madplan og markere retter som favoritter, og få dem forslået oftere.
  Hvorfor: giver grund til at komme igen hver uge.
  Accept: (1) gem/åbn madplan, (2) favoritstjerne på retkort, (3) fungerer uden konto lokalt, (4) rører ikke login-koden (auth.js).
  Ikke-mål: ændre login.
- [ ] [DATA] [A] Farverige, spændende aftensretter med blikfang
  Krav: de mest brugte brune retter (pølseret, spanske kødboller, frikadeller, carbonara, hakkebøf) får et friskt tilbehør (råkost, salat, grønt) i opskrift og ingrediensliste; 365discount får mindst 4 vegetarretter; Min Købmand får 2–3 børnevenlige retter i et nyt køkken.
  Hvorfor: ugeforslaget må ikke være fire brune kartoffelretter; farver og variation er forsidens blikfang.
  Accept: (1) alle ændrede retter består `kontrol.py`, (2) hver ændret ret har mindst tre friske farver i ingredienserne, (3) forsidens ugeforslag for 365discount og Min Købmand har mindst tre forskellige køkkener, (4) nye retter har en engelsk billedbeskrivelse i `billedprompts.json`, (5) svinekød udgør højst 35 % af retterne hos Min Købmand og Spar (i dag 24 af 45 og 24 af 53), og suppe-retter (fx pastinaksuppe) har så mættende tilbehør, at de er et hovedmåltid til 4.
  Ikke-mål: ugeforslagets algoritme.
- [ ] [UX] [A] Gode tilbud-grupperne nederst på indkøbslisten
  Krav: gruppetekster er korte og viser det, man kan købe (højst ca. 40 tegn pr. vare), og listen er hurtig at skimme på mobil.
  Hvorfor: de lange gruppetekster ("A, B eller C") forvirrer i butikken.
  Accept: (1) ingen vare i grupperne har tekst over 45 tegn, (2) 400 px bredde uden vandret scroll, (3) designfil med valgt løsning.
  Ikke-mål: ændre hvilke tilbud der vælges.
- [x] [UX] [H] Indkøbsliste: tydelige rækker (slået sammen 2026-11-16 af kontrollanten, 8c2e4a7; alle fire accept målt af kontrollanten)
  Krav: hver vare på indkøbslisten er en tydelig række med varenavn, mængde og pris, og kan afkrydses med ét tryk på telefon i butikken.
  Hvorfor: listen er det, brugeren bruger i butikken; den skal kunne skimmes og afkrydses med én hånd.
  Accept: (1) tryk-flade mindst 44 px pr. række, (2) afkrydsning huskes ved genindlæsning, (3) summer og linjer uændrede: regressionstest og før/efter-tal for alle 9 butikker, (4) 360 px uden vandret scroll.
  Ikke-mål: ændre hvilke varer eller priser listen viser.
- [ ] [SEO] [A] Opskriftssider: forsiden linker til dem og SEO-detaljer (opfølgning på 384f5d1)
  Krav: forsiden har et synligt link til /opskrifter/, hver opskriftsside linker tilbage til forsiden og til oversigten, og robots.txt peger på sitemap.xml.
  Hvorfor: Google finder siderne via links; kun sitemap giver svag indeksering.
  Accept: (1) link fra forsiden, (2) brødkrumme/tilbage-link på alle 193 sider, (3) robots.txt indeholder Sitemap-linjen, (4) kontrollen tjekker (2) og (3), (5) ingen priser på siderne.
  Ikke-mål: ændre appen eller prisberegningen.
- [ ] [UX] [H] Banner "Du ser en gemt kopi"
  Krav: når siden er vist fra service workerens cache og ikke fra nettet, forklarer et lille, roligt banner det, med en knap der prøver igen.
  Hvorfor: på netværk, hvor siden er blokeret, ser brugeren forældede data uden at vide det.
  Accept: (1) vises kun ved cache-visning, (2) forsvinder, når frisk data er hentet, (3) rører ikke cache-strategien for billeder, (4) regressionstest består.
  Ikke-mål: ændre hvad der caches.
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
- [ ] [TEST] [A] Kontrollen opdager forældede og forældreløse opskriftssider (forslag fra kontrollanten)
  Krav: `kontrol.py` sammenligner Recipe-JSON-LD's ingredienser og trin med `opskrifter.json` og fejler på mapper i `opskrift/` uden en opskrift.
  Hvorfor: rød-hold 2026-11-15 viste, at en ændret opskrift uden ny kørsel af `byg_sider.py` og en forældreløs side begge giver BESTÅET.
  Accept: (1) ændret ingrediens uden genbygning giver FEJLET, (2) forældreløs mappe giver FEJLET, (3) slug-funktionen findes ét sted (importeres fra `byg_sider.py`).
  Ikke-mål: ændre siderne.
- [ ] [TEST] [A] Bedre fejltekst når regression.js crasher (forslag fra kontrollanten)
  Krav: `regression.py` viser selve fejlbeskeden (linjen med `FEJL:`) i stedet for stderr's sidste linje (`Node.js v…`).
  Hvorfor: ved en ødelagt fixtur 2026-11-15 sagde fejlen kun "Node.js v22.23.4".
  Accept: (1) en bevidst ødelagt fixtur giver en læsbar fejltekst, (2) kontrol.py er BESTÅET.
  Ikke-mål: ændre facit.

## Afvist / parkeret
