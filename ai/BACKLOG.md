# Backlog (øverst = først)

Format: `- [ ] [A|B] Titel – hvorfor/detaljer`. Udvikleren tager det øverste punkt, som kan gøres på én dag. Klasse A/B: se `regler.md`.

## Fra Jonas
- [ ] [A] Spændende, farverige retter og billeder med blikfang, især dem der foreslås på forsiden. Ingen ensformig brun mad. (Bibliotek_8 er forbilledet.)
- [ ] [A] Kun rigtig aftensmad – ingen frokost-, morgenmads- eller dessertagtige retter.

## Åbne punkter
- [ ] [A] Giv de mest brugte brune retter et friskt tilbehør (råkost, salat, grønt) i opskrift og ingrediensliste, så de bliver pænere og mere komplette. Start med retter, som ugeforslaget vælger oftest (pølseret, spanske kødboller, frikadeller, carbonara, hakkebøf).
- [ ] [A] 365discount har kun 3 vegetarretter (mål: mindst 4), Min Købmand har få børnevenlige retter og en ensformig uge (to kødbolleretter, tre italienske). Skriv 2–3 passende retter pr. butik i `scripts/retter/<butik>.json`.
- [ ] [A] Kvickly: "Svinemørbrad med svampesauce og kartoffelmos" mangler svinemørbrad som ingrediens (kontrollen advarer). Ret retten.
- [ ] [A] Dyre andretter (andelår/hel and, 130–190 kr pr. person): vurdér, om de skal bort eller laves billigere, så forsiden ikke viser dem. Kontrollen advarer om retter over 450 kr.
- [ ] [A] Indkøbslistens typeoplysning (`ty`) mangler på mange ingredienser med tilbud (kontrollen tæller dem). Ret `bibliotek_typer.py`, så de manglende typer (mango, majs, salsa, parmigiano, rygeost …) får en type, uden at ramme ikke-mad.
- [ ] [A] "Gode tilbud"-grupperne nederst på indkøbslisten har lange gruppetekster – forkort dem til det, der kan købes.
- [ ] [B] Banner "Du ser en gemt kopi", når siden er hentet fra service worker-cachen (forklarer forældede data på netværk, hvor siden er blokeret). Rører `sw.js` og `index.html`.
- [ ] [A] SEO-gennemgang: titel, beskrivelse, `og:`-tags, sitemap og robots.txt. Kortlæg først, hvad Google kan se (retterne ligger ikke som egne sider). Skriv en rapport og forslag; byg ikke tusind sider.
- [ ] [A] Tilgængelighed og mobil: kontrast, tryk-flader, billeders `alt`-tekst, og billedstørrelse (kontrollen advarer om billeder over 160 KB).
- [ ] [B] Næring pr. voksen i stedet for pr. gennemsnitsportion i kategorien Fitness (børnene spiser mindre end de voksne).

## Afvist / parkeret
(ingen)
