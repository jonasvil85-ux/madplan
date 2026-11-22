# Design: Søg i "Vælg selv" (trin 2 "Retter")

Set på siden: `renderRetter()` i `index.html` bygger, oppefra: kategorikortene (`katRaekke`: Budget, Fitness, Fast food … som vandret række), rækken "Din uge" (`ugeplanValg`, ca. 300 px høj på telefon), og så retgitteret (`.grid`, ét kort pr. ret med stort billede). På skærmbilledet `mob_3_trin_2.png` (390 px) er der ved første blik kategorier og "Din uge"; selve retkortene begynder først omkring 610 px nede. Der er ingen søgning. (Søgefeltet `#soeg` findes kun i trin "tilføj varer" og røres ikke.)

## Problemet set fra brugeren
"Jeg ved, at jeg vil have noget med kylling – men listen er uendelig lang, og jeg ved ikke, hvilken kategori retten ligger i." Uden søgning giver folk op og trykker "Brug forslaget".

## To meget forskellige løsninger
**A. Søgefelt øverst, der filtrerer gitteret (valgt):** ét felt over kategorierne; mens man skriver, vises kun retter, hvis navn eller ingredienser passer, direkte under feltet.
**B. Søgning som fuldskærmsark:** en "Søg"-knap åbner et ark med felt og resultatliste, som lukkes igen. Giver plads til flere filtre, men flytter brugeren væk fra retkortene, de skal vælge på, og kræver et ekstra tryk, før man kan skrive.

**Valg: A.** Det er det, folk forventer, det er ét tryk til at skrive, og retkortene (billede, pris, "vælg") bruges uændret – vi bygger ingen ny retvisning.

## Detaljer (valgt løsning)

### Rækkefølge
Mobil (390 px), oppefra: **søgefelt** → kategorikort → "Din uge" → retgitter. Felt på toppen, så kravet "synligt uden at scrolle" er opfyldt med margen (feltet ligger ca. 16 px under fanerne).
Desktop (1280 px): samme rækkefølge; feltet er højst 480 px bredt og venstrestillet i sidens kolonne (ikke strakt over hele bredden).

### Mål og udseende
- Felt: højde 48 px (≥ 44), fuld bredde på mobil, radius 10 px (som `.soegefelt input`), baggrund `--surface-2`, kant 1 px `--border`, tekst `--text-1`, skriftstørrelse **16 px** (ellers zoomer iOS ind). Fokus: kant `--accent`, 2 px fokusring `--valgt`.
- Forstørrelsesglas-ikon (`ikon('search')` – findes ikonet ikke, tilføjes samme stil som de øvrige 1,5 px-ikoner) 18 px, `--text-3`, 14 px fra venstre kant.
- **Ryd-knap ×** til højre inde i feltet, kun når der står noget: 44 × 44 px tryk-flade (ikonet 16 px), `aria-label="Ryd søgning"`. Samme knap hedder "Vis alle retter" i tom-tilstanden (se nedenfor).
- Margen under feltet 12 px, over kategorierne.

### Tekster (ord for ord)
- Pladsholder: `Søg efter ret eller ingrediens, fx kylling`
- Skjult label (for skærmlæser): `Søg i retter`
- Resultatlinje under feltet (kun mens der søges, 14 px `--text-3`, `aria-live="polite"`): `12 retter passer til "kylling"` / ved én: `1 ret passer til "kylling"`
- Note når valgte retter er filtreret væk (samme linje, ny linje under): `3 valgte retter passer ikke til søgningen, men er stadig med i din madplan.` (ental: `1 valgt ret passer ikke …, men er stadig med …`)
- Tom-tilstand (0 træffere): overskrift `Ingen retter passer til "kyllin"`, linje `Prøv et kortere ord, eller tjek stavningen.`, knap `Vis alle retter` (44 px, fuld bredde på mobil, sekundær stil som `.knap.sekundaer`).

### Hvad der sker, mens man søger
1. Søgningen gælder **alle retter i de valgte butikker**, uanset den aktive kategori og "Bruger min rest" – ellers ville "0 træffere" kunne skyldes, at brugeren stod i Fitness. Kategorikortene dæmpes ikke og skjules ikke, men intet kort er markeret aktivt, og resultatlinjen siger, at der søges i alle retter. (Tryk på et kategorikort rydder søgningen og viser kategorien – ét mentalt lag, ingen skjulte kombinationer.)
2. **"Din uge" foldes sammen** til én linje (`Din uge · 7 af 7 dage ▾`, 44 px høj, tryk folder ud), så de første træffere ligger ca. 230 px nede på 390 px i stedet for 610 px. Madplanens indhold ændres ikke.
3. Sortering som "Alle retter" i dag (`katSort('alle')`); ingen omsortering efter relevans (forudsigeligt).
4. Retkortene er uændrede (billede, pris, "tilbud", valg). **Valgte retter, der passer til søgningen, står med det vanlige flueben.** Valgte retter, der ikke passer, vises ikke i gitteret, men tæller stadig i "7 retter valgt" nederst, i "Din uge" og på indkøbslisten – og noten ovenfor siger det. (Accept 4.)
5. Søgningen huskes **ikke** ved genindlæsning eller skift af butik/trin: man kommer tilbage til den fulde liste. Den huskes mens man går frem og tilbage mellem trin i samme besøg.
6. Ingen animation. Resultaterne opdateres straks (filtrering på `input`, ingen forsinkelse; datamængden er lille).

### Hvordan der matches
- Små/store bogstaver er ligegyldige (`toLocaleLowerCase('da')`); æ, ø, å skrives som de er. Accentbogstaver (é, ü) sidestilles med deres grundbogstav.
- Teksten deles i ord. **Alle** søgeordene skal passe (OG): "kylling pasta" finder retter med begge dele, i navn eller i ingredienser, i hvilken som helst rækkefølge.
- Et søgeord passer, hvis det **begynder et ord** i retnavn eller ingrediensnavn ("kylling" → "Kyllingefilet", "Kyllingebryst"). Fra 4 tegn passer det også **inde i et sammensat ord** ("ost" skal ikke gøre det, men "laks" → "Røget laksefilet"; "fisk" → "Torskefisk"), fordi danske ord er sammensatte. Under 4 tegn kun ordbegyndelse (så "ris" ikke fanger "Paris" og "citrus").
- Mellemrum først/sidst ignoreres. Kun mellemrum i feltet = ingen søgning.
- Søgeteksten sættes ind som tekst, aldrig som HTML (`esc`).

### Tilstande
- **Tom (ingen søgning):** siden er identisk med i dag plus feltet øverst.
- **Indlæser/fejl (ingen retter endnu):** feltet vises ikke (der er intet at søge i).
- **Få træffere (1–3):** vises som i dag; resultatlinjen står stadig. **Mange:** hele gitteret, som i dag.
- **Valgte, men ikke matchende:** noten ovenfor.

### Tilgængelighed
`<input type="search" role="searchbox" enterkeyhint="search" autocomplete="off" autocapitalize="none" spellcheck="false">` med synlig fokusring; Enter lukker tastaturet (skjuler det ved at fjerne fokus), ændrer intet andet; Escape rydder; × og "Vis alle retter" kan nås med Tab. Tekstkontrast ≥ 4,5:1 i både mørkt og lyst tema (kun eksisterende tokens). Resultatlinjen oplæses ved ændring. 360–400 px uden vandret scroll.

## Sådan opfyldes acceptkriterierne
1. **Synligt øverst, ≥ 44 px:** feltet er sidens første element under fanerne, 48 px højt; testes: feltets `top + højde` < 844 på 390 × 844, højde ≥ 44.
2. **Ret og ingrediens, æ/ø/å, store/små:** matchreglerne ovenfor. Testcases: "KYLLING", "kylling", "pasta", "bøf", "rødbede", "æble", "gulerod", "ost" (kun ordbegyndelse), "kyl", "kylling pasta".
3. **0 træffere:** tom-tilstanden med `Vis alle retter`.
4. **Valgt ret forsvinder aldrig fra madplanen:** søgningen ændrer kun, hvad gitteret viser, aldrig `state.valgte`/`state.plan`; noten viser antallet. Test: vælg ret, søg efter noget andet, `state.valgte` uændret, "N retter valgt" uændret.
5. **Priser/madplan/indkøbsliste uændrede:** ingen beregning røres; regression og facit skal være identiske (før/efter-tal for 9 butikker).
6. **Chromium-test:** felt synligt og ≥ 44 px, skriv "kylling" → kun matchende kort, ryd → alle kort, nonsens → tom-tilstand, valgt ret overlever søgning, 390 px uden vandret scroll.
7. **Designfil:** denne.

## Indvending til Ejeren
- Accept (2) siger "søgning på ret og på ingrediens", men siger ikke hvordan ord matches. På dansk er det afgørende (sammensatte ord): forslag til tilføjelse: *"(2b) et søgeord matcher begyndelsen af et ord i navn eller ingrediens, og fra 4 tegn også inde i et sammensat ord; flere søgeord skal alle passe; 'ris' må ikke finde 'Paris'."*
- Kravet siger intet om, hvad der sker med den aktive kategori og "Bruger min rest". Jeg har valgt, at søgningen gælder alle retter (ellers kan brugeren stå i en kategori og få en misvisende "0 træffere"). Ejeren bør bekræfte det i kravet.
- Hvorfor-teksten nævner 63.000 px lang liste. Søgning hjælper dem, der ved, hvad de vil have; den gør ikke listen kortere for dem, der blot browser. Det er ikke en indvending mod kravet, men Ejeren bør overveje en opfølgning (fx at folde kategorier eller indlæse flere kort ad gangen) – ikke i denne omgang.
- Accept (5) kan med fordel præciseres: *"filtreringen er ren visning: `state.valgte`, `state.plan` og alle beregninger er bit-for-bit uændrede."*
