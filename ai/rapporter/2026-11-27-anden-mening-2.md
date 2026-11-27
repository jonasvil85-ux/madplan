# Anden mening 2026-11-27 (kørsel 2)

Ændringen i `HEAD~1..HEAD`: to nye designfiler i `ai/design/` (UX Designer): "Nye tilbud siden sidst" og "Opskriftsside – tydelig overgang". Ingen ændring i `ai/BACKLOG.md`, ingen `[SIKKERHED]`-krav. To emner, 3 af 3 kald brugt (emne 1: kreativ + kritisk, emne 2: kun kritisk).

## Emne 1: Design "Nye retter siden sidst" på forsiden
**Spørgsmål:** Hvordan kan en tilbagevendende bruger hurtigt se og få glæde af det, der er nyt, og hvad er svagt i den lukbare linje med "Se ugens forslag"?

**Idéer (kreativ runde):**
1. Grøn prik/"Ny"-mærke på nye retter, klik viser kun de nye: **valgt (kun mærket).** Billigt, roligt og passer til tallet i linjen. Filtreringen ("klik viser kun nye") afvist: ny funktion uden målt behov.
2. Flash-banner der glider ind i 3 sek. ved hver indlæsning: **afvist.** Bevægelse og gentagelse bryder "rolig side".
3. Samlekort/stempler med bonusopskrift eller rabat hos partner-butik: **afvist.** Spilmekanik, opfundne rabatter og partnere strider mod ærlige tal og lav kompleksitet.
4. Feed af kun nye retter i stedet for madplanen: **afvist.** Vender forsiden om og rører ugeforslagets flow (klasse H), uden at hypotesen er målt.
5. Fast "Nyt siden sidst?"-knap i topmenuen med filtrering: **afvist.** Påstår at kunne undvære gemte data; det kan den ikke, for "nyt" kræver en baseline.

**Modellens kritik (omskrevet):**
- "Ny" er ikke defineret, hvis en ret forsvinder og vender tilbage; hvad hvis linjen aldrig lukkes?
- Mangler: gemmer kun i localStorage, så ingen historik på tværs af enheder; tilgængelighed; fejl/tomt feed; privatlivsnote.
- Risiko: forældet lokal liste kan forvirre; "Ny" uden at være nyt skader tilliden; ryddet browserdata gør alt "nyt" igen; brugeren kan pille ved localStorage.
- Forslag: server eller anonym cookie til historik, 4-ugers vindue, "Vis igen", fallback ved fejl, privatlivsnote.

**Min vurdering:**
- Definition af "ny" ved forsvundet/tilbagevendende ret: **enig.** Designet siger "ikke i baseline for samme butik", men siger ikke, om en ret, der var væk en uge og kommer igen, tæller. Med baseline = sidst lukkede liste tæller den som ny, hvis den ikke stod der. Det bør stå eksplicit.
- Linjen lukkes aldrig: **delvist enig.** Designet forklarer, at baseline først flyttes ved lukning. Men en bruger, der aldrig lukker, ser tallet vokse for evigt og får aldrig en ny baseline. Forslag 1 nedenfor.
- Server-side lager/cookie: **uenig.** Bryder "ingen cookies, intet bruger-id, ingen server" og berører privatlivspolitikken (grundlov). localStorage-tab på nyt udstyr er en acceptabel pris for en uafprøvet hypotese.
- Manipulation af localStorage: **uenig.** Brugeren kan kun narre sig selv; tallet bruges ikke til noget andet.
- Tilgængelighed, fejltilstand, privatlivsnote: **uenig som nyt.** Designet har allerede `role="status"`, kontrast, fokusring, tabrækkefølge og en try/catch-tilstand. Privatlivsnote: ingen persondata gemmes, kun rettens navne; hører under grundloven. Modellen har ikke læst det hele.
- "Vis igen": **uenig.** Linjen er en nyhedsnotits, ikke indhold; at mangle den er ikke et problem.
- Misvisende "Ny"-mærke: **enig, men det er et nyt risikopunkt i vores egen tilføjelse** (se forslag 2).
- 4-ugers vindue: **delvist.** Det løser den evigt voksende liste, men tilføjer kompleksitet; se forslag 1 i enklere form.

**Foreslået ændring af designet (konkret tekst):**
1. Tilføj under "Hvornår vises linjen": "Baseline slettes og sættes til nu-værdien, når `g` er mere end 28 dage gammel, uanset om linjen er lukket (så et tal ikke vokser for evigt og et genbesøg efter lang tid ikke starter med et stort, tilfældigt tal). En ret, der var væk og kommer igen, regnes som ny, hvis den ikke stod i baseline."
2. "Ny"-mærket på retter tages **ikke med i dette krav.** Det er klasse A, men det kræver ændring i retlisten og er et selvstændigt krav. Skal det med: mærket vises kun, mens linjen er synlig, og har tekst, ikke kun en farve (fx ordet "Ny"), så det ikke afhænger af farve.
3. Brug ikke "Ny" om retter, hvis navn blot er ændret af os (omskrevet titel); notér i designet, at navneændringer i data vil give falske "nye" og er en kendt svaghed.

**Ikke taget med:** server/cookie, "Vis igen", animeret banner, samlekort, feed, filterknap, privatlivsnote.

## Emne 2: Design "Opskriftsside – tydelig overgang til ugens tilbud"
**Spørgsmål:** Er den ærlige tekst (ny overskrift, afsnit, knap, "Gratis"-linje) og afvisningen af kravets knaptekst tilstrækkelige, og hvad er svagt? (Kun kritisk runde, da designet allerede har to løsninger og et valg.)

**Modellens kritik (omskrevet):**
- Overskriften "Hvad koster den i denne uge?" er misvisende (enig med designet).
- Ikke tydeligt, om priser er estimerede eller faktiske, og hvad "ugens tilbud" dækker.
- Mangler: datakilde og opdateringsfrekvens, "ingen tilbud"-tilstand, butiksvælger før knappen.
- Risiko: forkerte forventninger, hvis kun nogle butikker er med; "Gratis"-linjen skader, hvis den ikke er sand.
- Forslag: overskrift "Se din pris med ugens tilbud" med straks-estimat, dropdown med butik, note om datakilde, eksplicit "ingen tilbud"-besked.

**Min vurdering:**
- Overskriften er misvisende: **enig,** står allerede som indvending i designet.
- Forslaget "Se din pris med ugens tilbud" med estimat: **uenig.** Det genindfører præcis det brudte løfte (en pris, siden ikke viser), og kræver at siden regner en pris; klasse H, uden for en statisk side.
- Butiksvælger på opskriftssiden: **uenig.** Statisk side uden JavaScript; butiksvalget findes på forsiden. Det er en ny funktion, ikke en tekstrettelse.
- "Ingen tilbud"-tilstand: **uenig.** Siden lover ikke tilbud til netop retten, så der er ingen tom tilstand.
- Datakilde og opdateringsfrekvens: **delvist.** "Tilbuddene skifter hver uge" dækker frekvensen; datakilden (Tjek) er en detalje, brugeren her ikke har brug for. Dog nævner afsnittet i dag ikke, at 9 butikker er med; originalteksten gjorde (listen af butikker). Se forslag 1.
- "Gratis"-linjen: **enig i risikoen,** og designet gør den allerede betinget af, at Ejeren bekræfter. Hold fast i det.
- Placering på mobil: **delvist enig.** Acceptpunkt 5 (højst 6 linjer, knap ≥ 44 px) dækker det.

**Foreslået ændring af designet (konkret tekst):**
1. Afsnittet kan nævne omfanget ærligt, så ingen tror, alle supermarkeder er med: "Tilbuddene skifter hver uge. Vælg din butik blandt 9 danske supermarkeder, så laver Måltidsjagten …" (tallet tages fra `retter.json` eller en fast tekst, der opdateres med butikslisten; kontrol: teksten må ikke stå forkert, hvis antallet ændres).
2. Behold "Gratis"-linjen kun efter Ejerens bekræftelse; ellers udelad (som designet allerede siger).
3. Ingen ændring af overskrift, knaptekst og afvisning af kravets forslag. Tilføj ikke butiksvælger, pris eller "ingen tilbud"-tilstand.

**Ikke taget med:** estimeret pris på siden, dropdown, "ingen tilbud"-besked, note om datakilde.

Nyttigt: delvist (idéen om at begrænse baseline-alderen og kravet om et definitionsmæssigt svar på "tilbagevendende ret" var brugbare; resten var generelle råd, der enten stred mod produktets rammer eller allerede stod i designet).
