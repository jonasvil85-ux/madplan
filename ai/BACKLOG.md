# Backlog (øverst = først)

Ejeren vedligeholder listen. Format (se `agenter/ejer.md`): `- [ ] [UX|DATA|TEST] [A|H] Titel`, med Krav, Hvorfor, Accept og Ikke-mål. UX-udvikleren tager det øverste punkt, som kan gøres på én dag.

## Fra brugerne
(klistr feedback ind her)

## Åbne krav
- [ ] [DATA] [H] Ret kendte datafejl (gren ai/2026-11-16-datafejl AFVIST forsøg 1 2026-11-16: klasse H, før/efter mangler ugepris og indkøbslinjer for 9 butikker, 16 ty-advarsler tilbage; se kontrolrapporten. ai/2026-11-19-datafejl AFVIST 2026-11-19 uden nyt forsøg: kode uændret, accept (1) stadig 16 ty-advarsler)
  Krav: Kvickly "Svinemørbrad med svampesauce og kartoffelmos" får svinemørbrad som ingrediens; `ty`-oplysning for ingredienser med tilbud, der mangler den (kontrollen tæller dem; mango, majs, salsa, parmigiano, rygeost m.fl.) via `bibliotek_typer.py`, uden at ramme ikke-mad; dyre andretter (over 450 kr for hele retten) vurderes og fjernes eller laves billigere.
  Hvorfor: tillid til indkøbslisten og et ugeforslag uden urealistisk dyre retter.
  Opdatering Ejer 2026-11-20: efter aviserne uge 48 er problemet vokset: netto har nu 25 ty-advarsler (var 16), og 5 nye retter er over 450 kr (bilka-andelår 773,5 og 732 kr, minkoebmand 494 og 512,5 kr, spar helstegt and 567 kr). Næste forsøg skal tage højde for nye data, ikke kun de gamle 16 – og udelukke 'Jalapeño ost', 'Mayonnaise med mango' og blandingsfars (kontrollantens rød-hold). Kvickly/meny-svinemørbraden: Ejeren accepterer, at kontrollen tæller 'mørbrad af gris' som svinemørbrad, hvis ingrediensen ellers passer.
  Accept: (1) kontrollens advarsler om disse punkter er væk, (2) ingen ret på forsiden koster over 450 kr, (3) indkøbslisten viser kun den vare, retten bruger, for de rettede ingredienser.
  Ikke-mål: ændre `tilbudVariant()`.
- [ ] [UX] [H] Én regel for to butikker (UDGIVET 2026-11-16 i 090801b; RULLET TILBAGE af kontrollanten 2026-11-17 sammen med "Ét kort" – se dér) (Jonas 2026-11-16: "Vælger man flere butikker skal det jo gerne blive billigere"; afløser (11)'s del (a) i "Sammenlign butikker". Bygges oven på "Ét kort")
  Krav: kortets to-butiks-forslag og boksen "Hvor mange butikker" bruger samme regel: to butikker anbefales, når deres fælles billigste uge (én samlet indkøbsliste over begge, egne tilbud) er mindst ANBEFAL_SPAR (30 kr) billigere end den billigste enkeltbutiks uge. Begge uger er 7 aftensmåltider til husstanden med samme portioner. Fravalgt: at prissætte parrets retter i én butik (urimeligt over for butikker uden tilbud på retterne, Jonas' pointe).
  Hvorfor: kortet anbefalede ikke Netto + Lidl (367 kr mod Lidls 421 kr), mens boksen gjorde. Brugeren sparer reelt 54 kr ved at handle i begge, uden at få mindre mad.
  Accept: (1) kortet viser kombinationen, når (enkeltbutikkens uge − parrets uge) ≥ ANBEFAL_SPAR, regnet på præcise tal som boksens `anbefaletAntal`; blandt flere vises den billigste uge; (2) vælger man kortets par, anbefaler boksen 2 butikker, og madplanen koster præcis kortets pris (automatisk test for 2+2, 2+0, 1+0); (3) teksten viser parrets pris og enkeltbutikkens pris, besparelsen = forskellen på de viste tal, og at transport og ekstra tid ikke er regnet med; (4) sammenlign.js og browsertesten er opdateret og består; mutationsprøve af reglen; (5) regression og budget uændrede; før/efter-tal.
- [ ] [UX] [H] Ét kort: "Hvor handler du?" (UDGIVET 2026-11-16 i 090801b på Jonas' ordre; RULLET TILBAGE af kontrollanten 2026-11-17 (4aab106), forsøg 1: kontrol.py FEJLET på main i Chromium – sammenlign_browser.py går ned (TypeError), fordi sammenlign_side.js nu lægger tal/tekst i `maal` (enSkaerm, madplanTop390 …); selve sidens tjek gav fejl = []. Ret runneren (fx som i ai/2026-11-17-browsertest-sky), kør kontrol.py med Playwright, og indsend igen som gren; flueben-CSS'en (4661112) med) – listen er butiksvalget, flere butikker med et tryk (Jonas godkendte 2026-11-16; revideret samme dag efter Jonas: "Kunderne skal have mulighed for at vælge mere end en butik bare ved at trykke på en butik mere … pænt, simpelt og logisk"; designfil ai/design/2026-11-16-hvor-handler-du-samlet.md). Omfatter også "Én regel for to butikker" (samme gren).
  Krav: forsiden har ét kort om butiksvalg. Listen over de 9 butikker (hver butiks billigste uge ud fra egne tilbud) er afkrydsning: et tryk sætter/fjerner fluebenet, gerne flere butikker. Logo-gitteret og "Vælg selv flere butikker" findes ikke. "Hvor mange butikker" vises under listen, når der er valgt mere end én butik.
  Hvorfor: siden stillede samme spørgsmål to gange med samme logoer og tal; at skulle finde en særskilt knap for at vælge en butik mere er hverken simpelt eller logisk.
  Accept: (1) kun ét kort om butiksvalg: ingen "Sammenlign butikker"-overskrift, intet logo-gitter, ingen særskilt knap for flere butikker; (2) alle tal og accept (1)–(12) for "Sammenlign butikker" gælder (sammenlign.js og browsertesten består), dog med to-butiks-reglen fra "Én regel for to butikker"; (3) et tryk på en række sætter/fjerner fluebenet med samme funktion som det gamle butiksvalg (skiftButik: bekræftelse, hvis valgte retter fjernes); (4) et tryk på en butik mere giver flueben på begge, "Hvor mange butikker" vises med 1/2 butikker, madplanen har 7 dage; et tryk igen fjerner butikken og "Hvor mange butikker"; en valgt butik skjules aldrig af "Vis alle"; (5) madplanen (#sim-plads) starter mindst 300 px højere på 390 px end på main, målt uden et eventuelt to-butiks-forslag; (6) rundvisningens trin peger på synlige områder (trin 2 = listen; "Hvor mange butikker" springes over ved én butik); (7) regression og budget.js uændrede; 390 px uden vandret scroll; tryk-flader ≥ 44 px; (8) teksten siger, at man kan trykke på flere butikker, og at prisen er hver butiks billigste uge ud fra egne tilbud, til den valgte husstand; (9) (1), (3), (4), (5) og (6) testes automatisk i Chromium (scripts/tests); (10) før/efter-tal for alle 9 butikker; (11) uden priser (fejl) vises listen stadig, så man kan vælge butikker. (12) **hele forsiden på én skærm på telefon** (Jonas 2026-11-16: "på telefonen kan se hele forsiden på én side uden at scroll"): på 390 × 844 px er butiksvalget, ugens retter og "Brug forslaget" synlige uden at scrolle – med én butik, med to butikker og med en valgt butik, der ikke bruges; testet automatisk. (13) en valgt butik, som madplanen ikke bruger, siger det selv ("Ikke med") og står forrest i rækken på telefonen; under listen står én sætning med begrundelsen.
  **Undtagelse (Jonas 2026-11-16, "ja og lig den online"):** denne gren må slås sammen i dag, selv om dagens tre H-pladser er brugt. Al øvrig validering gælder fuldt; kun loftet over antal H pr. dag er hævet for netop denne gren.
  Ikke-mål: ændre priser, ugeforslag eller boksens regel; "samme madplan i alle butikker" (fravalgt).
- [x] [TEST] [A] Browsertesten kan køres i skyen (Ejer 2026-11-17) (SLÅET SAMMEN 2026-11-18, 91d8dc5..3b28eb5, forsøg 2; gren ai/2026-11-17-browsertest-sky AFVIST forsøg 1 2026-11-17: node-reserven melder sidefejl som "IKKE KØRT" (exit 3 → kun advarsel); se kontrolrapporten)
  Krav: `sammenlign_browser.py` og `kontrol.py` kører Chromium-testen, hvor Chromium findes, i stedet for at springe den over med en advarsel.
  Hvorfor: `python -I` ser ikke Playwright; Ejeren måtte køre `sammenlign_side.js` via node for at efterprøve "Hvor handler du?". Ellers er "hele forsiden på én skærm" aldrig automatisk bevist.
  Accept: (1) kontrol.py siger ikke "IKKE kørt" i et miljø med /opt/pw-browsers (node-Playwright som reserve, `executablePath` til den installerede Chromium); (2) ved manglende Chromium er advarslen uændret; (3) kontrol.py BESTÅET.
  Ikke-mål: ændre testens målinger.
- [x] [UX] [A] Mobil: 'Om Måltidsjagten' og sidefod som tryk-flader (afløser delen af mobil-tryk-flader, der blev parkeret) (SLÅET SAMMEN 2026-11-18 af kontrollanten, 3104489, forsøg 2; accept (3) vurderet efter hensigt – Ejeren 2026-11-19: accept er omformuleret til 'intet sidefodselement under 44 px på 390 px' – opfølgningskrav kommer, når 'Hvor handler du?' er genindsendt; opfølgning: 'Om' 39 px på desktop, ubetingede hover-regler, sidefod_browser.py uden node-reserve) (gren ai/2026-11-17-sidefod-tryk-flader AFVIST forsøg 1 2026-11-17: opacity 0.9 tilbage ved åben/fokus, desktop-ikon løsrevet; accept (3) bør omformuleres – basis 23 forsvandt med tilbagerulningen, main er nu 33)
  Krav: alle links i sidefoden er mindst 44 px høje på 390 px.
  Hvorfor: 'Om Måltidsjagten' er 95 × 14 px og det sidste, som holdt tryk-flader afvist.
  Accept: (1) ingen sidefodslinks under 40 px højde; (2) 390 px uden vandret scroll; (3) browser_tjek viser færre små tryk-flader end 23.
  Ikke-mål: billeder (eget krav).

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
- [ ] [UX] [A] Gode tilbud-grupperne nederst på indkøbslisten (kontrollant 2026-11-20: AFVIST igen, forsøg 2 – "Vis færre" virker ikke med en afkrydset vare, se ai/rapporter/2026-11-20-kontrol.md; ét forsøg tilbage. 2026-11-19: forsøg 1 AFVIST; klassificeret H, fordi den rører listeLinjer og facit; titler som "Daim" og "Kartofler" på sedlen – se kontrolrapporten)
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
- [ ] [SEO] [A] Opskriftssider: titler under 60 tegn og beskrivelser 70–160 tegn (SEO/vækst 2026-11-19, uge 47)
  Krav: byg-scriptet (`scripts/byg_sider.py`) skriver titler på formen "Navn | Måltidsjagten" (eller kortere), højst 60 tegn, og beskrivelser på 70–160 tegn. Bevar unikke titler og beskrivelser.
  Hvorfor: 171 af 193 titler er over 60 tegn (længste 99), og 13 beskrivelser er under 70, så søgeresultater afkortes. Effekten på placering er en hypotese; ingen placering lovet.
  Accept: (1) alle 193 titler ≤ 60 tegn, alle beskrivelser 70–160 tegn, (2) ingen dubletter af titel eller beskrivelse, (3) kontrollen tjekker (1) og (2), (4) `kontrol.py` BESTÅET, (5) ingen priser og ingen opfundet tekst på siderne.
  Ikke-mål: ændre opskrifter, billeder eller forsiden.
- [ ] [SEO] [A] Forside: synlig overskrift, ens butikstal og tekst uden JavaScript (SEO/vækst 2026-11-19)
  Krav: (a) Ejeren afgør butikstallet (9 eller 10) og meta-beskrivelse, `og:description`, JSON-LD og opskriftssidernes tekst bruger samme tal og samme liste; (b) forsiden får en synlig `<h1>` med søgeord (fx "Ugens madplan ud fra tilbud") uden at forskubbe "hele forsiden på én skærm" (UX-designeren vurderer), og logoet bliver ikke-overskrift; (c) `<noscript>` forklarer kort, hvad siden gør, og linker til `/opskrifter/`.
  Hvorfor: forsidens indhold bygges i JavaScript; uden overskrift og ens tal er siden svagere for søgemaskiner og mindre ærlig. Betydningen er en hypotese, ikke målt.
  Accept: (1) kun ét tal for antal butikker i `index.html` og i opskriftssiderne, (2) `<h1>` indeholder synlig tekst, (3) 390 × 844 px: butiksvalg, ugens retter og "Brug forslaget" er stadig synlige uden scroll (browsertesten), (4) `kontrol.py` BESTÅET, (5) ingen ændring af priser eller beregning.
  Ikke-mål: nye landingssider; ændre `simuleringHtml()`.
- [ ] [SEO] [A] Anonym hændelsesmåling uden persondata (SEO/vækst 2026-11-19; ROADMAP 16)
  Krav: Ejeren afklarer, om Vercel Web Analytics' egne hændelser kan bruges (holdet kan ikke se abonnementet); hvis ja, tælles `butik_valgt`, `forslag_brugt`, `seddel_aabnet`, `liste_delt` og `opskrift_til_forside` uden bruger-id, indkøbsindhold eller tekstfelter. Rør ikke `auth.js`/`feedback.js`.
  Hvorfor: ingen kan i dag se, hvor i flowet brugerne falder fra; fastholdelse og søgetrafik kan ikke vurderes uden måling.
  Accept: (1) hændelser sender kun navnet på hændelsen (ingen parametre med persondata eller indkøbsvarer), (2) siden virker uændret, hvis scriptet er blokeret, (3) browsertesten viser 0 JavaScript-fejl, (4) privatlivspolitikken dækker det; mener Ejeren, at den skal ændres, skrives forslaget til Jonas (grundlov), og kravet venter, (5) `kontrol.py` BESTÅET.
  Ikke-mål: cookies, bruger-id, tredjepartsværktøjer, egen tabel i Supabase.
- [ ] [SEO] [A] Tjek næringsdata i opskrifterne (SEO/vækst 2026-11-19; hypotese)
  Krav: 5 opskriftssider angiver over 1000 kcal pr. portion (fx 1354 kcal for æbleflæsk). Udvikleren genberegner dem og retter beregningen eller teksten, så tallet er rimeligt og tydeligt mærket.
  Hvorfor: forkerte tal i `Recipe`-markup og på siden skader tilliden; det er uafklaret, om tallene er forkerte.
  Accept: (1) de 5 sider forklaret eller rettet med bevis (ingrediensliste, regnestykke), (2) kontrollen advarer ved over 1000 kcal pr. portion uden forklaring, (3) `kontrol.py` BESTÅET.
  Ikke-mål: ændre priser.
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

### Sikkerhed (sikkerhedsagenten, uge 47 – rapport: ai/rapporter/2026-uge-47-sikkerhed.md; ingen kritiske fund)
- [ ] [SIKKERHED] [H] Høj: Supabase-biblioteket fra egen server med fast version (H1)
  Krav: `index.html` og `admin.html` henter ikke længere `supabase-js@2` fra jsDelivr uden fast version; en bestemt version ligger i repoet (fx `vendor/`) eller hentes med præcis version + `integrity` + `crossorigin`.
  Hvorfor: en kompromitteret eller ny 2.x-udgivelse kører i dag uden test med fuld adgang til login-sessioner og til admin-siden med feedback-e-mails.
  Accept: (1) `grep -n 'supabase-js@2"' *.html` giver intet; (2) scriptet har enten egen sti eller præcis version med `integrity="sha384-…"`; (3) en kontrol i `kontrol.py` fejler, hvis et `<script src="http…">` mangler `integrity` (undtagen `/_vercel/insights`); (4) login, log ud, gem/hent brugerdata og feedback virker i Browser-QA; (5) `VERSION` i `sw.js` er hævet; (6) kontrol.py BESTÅET.
  Ikke-mål: ændre `auth.js` eller login-flowet.
- [ ] [SIKKERHED] [H] Høj: Kontrollant-workflowet adskiller grenens kode fra hemmelighederne (H2 – GRUNDLOV, kun Jonas)
  Krav: grenens tests kører i et job uden `CLAUDE_CODE_OAUTH_TOKEN` og med `permissions: contents: read`; `actions: write` fjernes eller begrundes; `persist-credentials: false` hvor der ikke pushes; grenbeskyttelse på `main` (ingen force-push/sletning).
  Hvorfor: i dag kan kode på en `ai/**`-gren læse Jonas' private Claude-token og et GitHub-token med skriveadgang.
  Accept: (1) intet job, der kører grenens kode, har en hemmelighed i miljøet (læses i workflowet); (2) kontrollanten kører stadig alle tests og kan slå sammen; (3) `main` afviser force-push.
  Ikke-mål: ændre kontrollantens instruks. Forslaget står i rapporten under "Forslag til grundloven"; Ejeren/Sekretæren sender det til Jonas.
- [ ] [SIKKERHED] [H] Middel: Sikkerhedshoveder via `vercel.json` (M1)
  Krav: en `vercel.json` med `Content-Security-Policy` (først evt. `-Report-Only`), `X-Frame-Options: DENY`/`frame-ancestors 'none'`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy`, `Strict-Transport-Security`; `/admin.html` får også `X-Robots-Tag: noindex` og `Cache-Control: no-store`.
  Hvorfor: login og admin kan i dag indlejres i fremmede sider, og intet begrænser, hvilke scripts der må køre.
  Accept: (1) Browser-QA (eller curl i GitHub) viser alle hoveder på `/`, `/admin.html` og en opskriftsside; (2) ingen CSP-fejl i konsollen ved forside, login, feedback, opskriftsside og Vercel Insights; (3) billeder fra Tjek vises; (4) kontrol.py BESTÅET.
  Ikke-mål: fjerne `'unsafe-inline'` (eget, senere krav).
- [ ] [SIKKERHED] [H] Middel: Feedback-tabellen får grænser på serveren (M2)
  Krav: ny SQL-fil (fx `scripts/feedback_graenser.sql`, som Jonas kører) med check-regler: `pg_column_size(kontekst) <= 4000`, `jsonb_typeof(kontekst) = 'object'`, `type` i de 5 kendte typer, formattjek af e-mail; en hastighedsgrænse på serveren (trigger, der afviser mere end fx 30 rækker pr. minut i alt). `admin.html` tåler rækker med forkert form (`Array.isArray` før `.join`).
  Hvorfor: grænsen på 5 beskeder i timen findes kun i browseren; hvem som helst kan fylde tabellen via REST med den offentlige nøgle, og én misdannet række får admin-listen til at gå ned.
  Accept: (1) SQL'en kan køres flere gange; (2) eksisterende gyldige rækker overholder reglerne (forespørgsel i SQL-filen tjekker det, før reglerne lægges på); (3) `feedback.js` sender stadig gyldige beskeder (testet med samme felter som i dag); (4) admin viser en række med `valgte_retter: "x"` uden at gå ned; (5) kontrol.py BESTÅET.
  Tilføjet 2026-11-19 efter anden mening: grænsen er global (ikke pr. IP), tæller med `pg_advisory_xact_lock`, afviser med tydelig fejl (aldrig falsk succes), afvisninger tælles i en lille logtabel; kendt afvejning: en angriber kan fylde grænsen og blokere feedback (rammer ikke madplanen); check-regler lægges på `NOT VALID` og valideres, når gamle rækker er rene; ekstra accept (6): 40 hurtige indsættelser slipper højst grænsen igennem, resten får læsbar afvisning.
  Ikke-mål: ændre `feedback.js` (grundlov).
- [ ] [SIKKERHED] [H] Middel: Admin kræver 2-trinsbekræftelse og fast bruger-id (M3)
  Krav: admin-politikkerne og `admin_statistik()` kræver `aal2` og sammenligner med admin-kontoens `auth.uid()` i stedet for e-mailen (ny SQL-fil, som Jonas kører); `admin.html` tilbyder TOTP-tilmelding og -kode ved login; Jonas slår MFA, "Leaked password protection" og mindst 8 tegn til i Supabase.
  Hvorfor: i dag beskytter kun en adgangskode (mindst 6 tegn) alle feedback-e-mails, og admin-e-mailen er offentlig.
  Accept: (1) uden MFA giver admin-siden "ikke tilladt" fra databasen; (2) med MFA vises statistik og beskeder; (3) e-mailadressen står ikke længere i `admin.html` eller den nye SQL-fil; (4) kontrol.py BESTÅET.
  Ikke-mål: MFA for almindelige brugere; ændre `auth.js` (teksten "mindst 6 tegn" er et forslag til grundloven).
- [ ] [SIKKERHED] [H] Middel: Færre tredjeparter og sletning efter 12 måneder (M4; politikteksten er GRUNDLOV)
  Krav: Inter-fonten hentes fra egen server (ikke fonts.googleapis.com/gstatic.com); et ugentligt job (`pg_cron` i ny SQL-fil) sletter feedback ældre end 12 måneder. Politikteksten om Anthropic, GitHub og evt. Google/jsDelivr opdateres af Jonas.
  Hvorfor: privatlivspolitikken nævner kun Supabase og Vercel, men besøgendes IP går til Google og jsDelivr, AI'en læser feedback, og løftet om "højst 12 måneder" håndhæves ikke.
  Accept: (1) `grep -rn 'fonts.googleapis\|fonts.gstatic' --include=*.html .` giver intet; (2) fonten ser ens ud (Browser-QA før/efter-skærmbilleder); (3) SQL'en planlægger sletningen og kan køres flere gange; (4) `VERSION` i `sw.js` er hævet, hvis fonte caches; (5) kontrol.py BESTÅET.
  Ikke-mål: ændre `privatlivspolitik.html` (grundlov – forslaget står i rapporten).
- [ ] [SIKKERHED] [H] Middel: Værn mod styring via anonym feedback (M5 – workflow og instrukser er GRUNDLOV)
  Krav: commit-tjekket i feedback-workflowet afviser også links og telefonnumre; Ejerens og kontrollantens instrukser siger, at krav fra feedback ikke må tilføje eksterne adresser/scripts eller røre login uden sikkerhedsagentens gennemsyn. Det, holdet selv kan gøre nu: en kontrol i `kontrol.py`, der fejler, hvis HTML/JS indeholder et eksternt domæne, som ikke står på en tilladt liste i testen.
  Hvorfor: anonym tekst går automatisk gennem fire AI-led, før den kan blive til kode.
  Accept: (1) kontrollen fejler på et nyt `<script src="https://ukendt.example">` og består på main; (2) listen over tilladte domæner står ét sted; (3) kontrol.py BESTÅET.
  Ikke-mål: blokere feedback.
- [ ] [SIKKERHED] [A] Lav: Escaping af alle datafelter og kontrol af datafilerne (L1)
  Krav: `kontrol.py` fejler, hvis `retter.json`, `opskrifter.json` eller `tilbudsliste.json` indeholder `<`, `>` eller `javascript:`. (Skabelonerne i `index.html` får `esc()` på `ing.navn`, `r.navn`, butiksnavne m.fl. som eget H-krav, fordi de rører indkøbslisten.)
  Hvorfor: tilbudstekster kommer fra en tredjepart og sættes enkelte steder ind i `innerHTML` uden escaping.
  Accept: (1) en datafil med `<b>` giver FEJLET; (2) main giver BESTÅET.
  Ikke-mål: ændre datafilerne.
- [ ] [SIKKERHED] [H] Lav: `.vercelignore` så kun selve siden udgives (L4)
  Krav: en `.vercelignore` med `ai/`, `scripts/`, `.github/` og `*.md`.
  Hvorfor: i dag udgives hele repoet, også SQL-filer, testdata og agentrapporter.
  Accept: (1) Vagtposten og Browser-QA er grønne efter udgivelsen (forside, opskriftssider, billeder, manifest, sw.js); (2) `/ai/STATUS.md` og `/scripts/admin.sql` giver 404 på den udgivne side; (3) kontrol.py BESTÅET.
  Ikke-mål: ændre repoets synlighed.
- [ ] [SIKKERHED] [H] Lav: Fastlåste versioner og fast Supabase-adresse i workflows (L2, L3 – GRUNDLOV, kun Jonas)
  Krav: `uses:` fastlåses til commit-SHA, `@anthropic-ai/claude-code` og `playwright` til præcise versioner; feedback-workflowet sender kun hemmeligheden til en fast `…supabase.co`-adresse (variabel eller tjek), ikke til hvad der står i `auth.js`. Jonas bruger GitHubs noreply-adresse i commits (L5).
  Accept: (1) ingen `@v4`/`@v5`/`@v7` uden SHA i `.github/workflows/`; (2) en ændret URL i `auth.js` får workflowet til at stoppe uden at sende hemmeligheden.

## Afvist / parkeret
