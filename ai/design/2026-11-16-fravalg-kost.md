# Design: Fravalg og kost – "Vi spiser ikke …" (ROADMAP 4)

## Hvad jeg har set
Kilde: `index.html` (husstandsboksen bag personikonet øverst til højre, "4" i en sort cirkel) og skærmbilledet `mob_1_forside.png` (390 px). I dag vælger man kun antal voksne og børn. Madplanen viser 7 dage med store billeder og knapperne "Byt" og "Fjern" på hvert kort. Det virker: boksen er det rigtige sted for husstandsvalg, og "Byt" findes allerede. Det forvirrer: man opdager ikke, at der er flere valg, for ikonet viser kun et tal; og får man et svinekødskort, er eneste vej at bytte retter én for én.
Der findes et tidligere design på den parkerede gren (`ai/2026-11-15-fravalg-budget`, ikke på main). Det er i orden i hovedtrækkene (valg i husstandsboksen, ni knapper); dette design bygger på det, men retter tre ting: (1) ærligheden om, hvad "uden" betyder, (2) hvordan siden fortæller, hvad der er fjernet, (3) at fravalg bygges **adskilt fra budget** (budget har egen designfil `2026-11-16-budget.md`).

## Problemet set fra brugeren
"Vi spiser ikke svin, og ungerne hader svampe." I dag skal brugeren bytte hver enkelt uønsket ret manuelt hver uge, eller opgive forslaget. Mange familier kan slet ikke bruge forslaget uden at kunne sige nej til noget – og det er netop dem, der ellers ville komme igen hver uge.

## To meget forskellige løsninger
**A. Valgknapper i husstandsboksen:** ni slå-til/fra-knapper ("Svinekød", "Fisk og skaldyr", "Løg" …) under voksne/børn. Ét sted, hurtigt, huskes. Risiko: at man glemmer, at de er slået til.
**B. Tilbagemelding på retterne ("Ikke den her"):** et tryk på et kort siger "spis ikke denne slags", og siden udleder fravalget. Mere naturligt i øjeblikket, men giver uforudsigelige regler og kan ikke forklares ærligt ("hvorfor forsvandt alle retter med ost?").

**Valg: A.** Brugeren skal altid kunne se og styre præcis, hvad der er fravalgt. B er skjult og uigennemskuelig, hvilket er det modsatte af sidens løfte om ærlighed. Kort-niveau-"Byt" findes allerede og dækker enkeltretter.

## Placering og rækkefølge
**Husstandsboksen** (åbnes af personikonet, som i dag), mobil 400 px, fra top:
1. Voksne / Børn (uændret).
2. Skillelinje (1 px `--border`, 16 px luft).
3. Overskrift `Vi spiser ikke …` (h3, 16 px/600, `--text-1`). Undertekst (13 px, `--text-3`): "Tryk på det, I vil undgå. Madplanen og 'Vælg selv' viser så kun retter uden."
4. **Knapgitter**, 2 kolonner på mobil (hver 44 px høj, 8 px gap, fuld bredde ÷ 2), 3 kolonner fra 560 px. Ni knapper i denne rækkefølge: `Svinekød` · `Okse og kalv` · `Kylling og and` · `Fisk og skaldyr` · `Kød og fisk (kødfri)` · `Løg` · `Svampe` · `Mælkeprodukter` · `Æg`.
   - Off: `border:1px solid var(--border)`, hvid baggrund, `--text-2`.
   - On: `border:2px solid var(--valgt)`, `background:var(--valgt-tint)`, `--text-1`, **og et ✓ foran teksten** (farve er aldrig eneste signal). `aria-pressed`.
   - "Kød og fisk (kødfri)" slår de fire kødknapper til som gruppe; trykkes en af dem fra igen, slukkes kødfri. Teksten på knappen er "Vegetar" i `aria-label` ("Vegetar: ingen kød eller fisk"); synlig tekst "Kødfri".
5. Nederste note (12 px, `--text-3`): "Vi sorterer efter ingredienserne i opskrifterne. Det er ikke en allergigaranti – tjek altid varedeklarationen."
6. Knap `Nulstil fravalg` (tekstknap, 44 px høj, kun synlig når mindst ét er valgt).

**Husstands-ikonet** øverst: viser stadig antal personer; når fravalg er aktive, tilføjes en lille prik (8 px, `--valgt`) på ikonet, og `aria-label` bliver "Husstand: 4 personer, 2 fravalg".
**Desktop (≥ 900 px):** boksen er bredere (max 440 px); knapgitteret 3 kolonner; knappen i toppen viser "4 · 2 fravalg" som tekst.

## Hvad siden fortæller, når der er fravalg
Direkte under "Madplan"-overskriften (over kortene), en rolig chiplinje (samme afstande som siden i øvrigt):
> `Uden: Svinekød · Svampe  [Ret]`  

hvor "Ret" åbner husstandsboksen. Én linje, 13 px, `--text-2`, chips `--surface-2`. Hensigten: man ser altid hvorfor madplanen er, som den er, og kan rette på 1 tryk. Intet fravalg → linjen findes ikke (siden som i dag).

## Tilstande
- **Ingen fravalg:** alt som i dag, ingen linje, ingen prik.
- **Fravalg aktive:** forslag, "Vælg selv" og "Byt" viser kun retter uden det fravalgte. Den indkøbsliste, der følger, har ikke fravalgte varer. Skeletlinje (samme højde som chiplinjen) mens forslaget regnes om, så siden ikke hopper; `aria-live="polite"`: "Opdaterer madplanen …".
- **For få retter tilbage** (færre end 12 i butikken – nok til et forslag med variation): fravalget gælder stadig i "Vælg selv", men forslaget bruger det ikke fuldt ud. Ærlig besked i amber-stil (`--amber` kant, ikke blokerende): "Der er kun 5 retter uden svinekød og fisk hos Min Købmand. Prøv en anden butik eller fjern et fravalg." + knapperne `Vælg anden butik` og `Fjern fravalg` (44 px). Forslaget vises stadig, og **siden siger tydeligt, hvilke fravalg der ikke kunne overholdes** ("Svampe er stadig med på 1 dag") – aldrig stille brud.
- **Ingen retter overhovedet:** tom-tilstand i madplanen: "Ingen retter passer til alle fravalg i den her butik." + `Fjern fravalg` (44 px).
- **Gemt valg:** gemmes på enheden og, hvis logget ind, i kontoen sammen med husstanden (ingen ny login-kode; `auth.js` røres ikke). Tom/ugyldig gemt værdi ignoreres uden fejl.
- **Fejl i gemning:** valget virker stadig i denne session; ingen fejlbesked (ingen grund til at forstyrre).
- Animation: ingen, undtagen at kortene skifter med et 150 ms fade (slås fra under `prefers-reduced-motion`).

## Ærlighed om grænserne (design-krav)
- Teksten siger "Vi spiser ikke", aldrig "uden allergen" eller "sikker for".
- **Skjulte ingredienser** (mayonnaise, remoulade, aioli = æg; pesto, parmigiano, feta, mozzarella = mælkeprodukter; "hakket kød" = svin + kalv) skal tælle med i fravalget. Retten, der alligevel tvivles på, skal hellere udelades end medtages. Fravalget må ikke overdrive: "Mælkeprodukter" betyder mælk, fløde, ost, smør, yoghurt og kendte oste.
- Retter får ikke et "garanteret uden"-mærke på kortet.

## Mål, farver, tilgængelighed
- Alle knapper 44 px høje; boksen kan scrolle internt på 360 px højde; ingen vandret scroll på 360 px. Knaptekst ombryder ikke midt i et ord; "Kød og fisk (kødfri)" tillader 2 linjer (knappen vokser).
- Farver kun fra tokens: `--valgt`, `--valgt-tint`, `--border`, `--text-1/2/3`, `--amber` til "for få retter".
- Tastatur: Tab gennem knapperne, Space/Enter skifter; fokus 2 px `--valgt`-outline, forskudt 2 px; fokus flyttes ikke ved skift.
- Skærmlæser: gruppen er `role="group"` med `aria-labelledby` på h3; ændring annonceres via live-regionen.

## Hvordan hvert acceptkriterium opfyldes
1. **Gemmes lokalt og i konto:** se Tilstande ("Gemt valg").
2. **Ingen foreslået ret indeholder en fravalgt ingrediens (testet i regression):** knapperne bruger en ordliste pr. kategori; testen skal bruge en **uafhængig** liste og køre over hele puljen i alle 9 butikker (jf. kontrollantens fund 2026-11-16). Se Indvending 1.
3. **Tydelig besked, hvis for få retter er tilbage:** se "For få retter tilbage" og "Ingen retter".
4. **Før/efter-tal:** ingen fravalg = uændret ugepris for alle 9 butikker (regressionstest); udvikleren skal vise det.

## Indvending til Ejeren
1. **Accept (2) er ikke bevisbart i den nuværende form.** "Ingen foreslået ret indeholder en fravalgt ingrediens" kan kun testes mod en ordliste, og al ordliste-baseret sortering slipper nye ord igennem (to afvisninger: mayonnaise, pesto, "hakket kød"). Jeg foreslår at omformulere til: "(2) for hver af de ni fravalg og alle 9 butikker indeholder ingen ret i puljen et ord fra en uafhængig, bredere kontrolliste; kontrollisten udvides, hver gang en fejl findes". Og at **datafilerne** (ikke kun en regex i `index.html`) bærer hver rets kategorier (`ty`/typer i `bibliotek_typer.py`), så sorteringen ikke afhænger af tekstmatchning på ingrediensnavne.
2. **Kravet blander "ingredienser" og "kosttyper".** "Fravalg af løg" og "vegetar" er to forskellige løfter. Jeg har valgt én samlet gruppe af ni knapper, men "Kødfri" er en genvej, ikke en kost-garanti. Bekræft, at det er meningen.
3. **"Allergi" må ikke antydes.** Ikke-mål siger det; designet gentager det i teksten. Ejeren bør også holde ordet "allergi" ude af SEO/butikstekster for fravalget.
4. **Budget hører ikke med her.** Den afviste gren byggede begge dele; designfilen for budget er adskilt (`2026-11-16-budget.md`), og accept her har ingen budgetpunkter. Bekræft i backlog, at de to krav bygges som to grene.
5. **Prioritet:** kravet er afvist to gange og parkeret. Jeg anbefaler, at det først bygges efter "Sammenlign alle butikker" (nr. 1 i backlog), da begge rører ugeforslagets beregning og sammenligningslisten skal regne med de samme fravalg (listen bruger de samme funktioner, så fravalget slår automatisk igennem, men skelet-tilstanden skal gentages ved ændret fravalg).
