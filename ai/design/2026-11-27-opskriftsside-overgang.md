# Design: Opskriftsside – tydelig overgang til ugens tilbud

## Set på siden
Opskriftssiderne bygges af `scripts/byg_sider.py` (statisk HTML, eget CSS med `--knap` #C9561E, `.knap` 48 px høj, `.kort`, `.lille`). Nederst, efter "Næring", står i dag:
- overskriften "Hvad koster den i denne uge?"
- et afsnit: "Måltidsjagten finder ugens tilbud i Netto, MENY, … og viser, hvad retten koster i den butik, du handler i."
- knappen **"Se ugens tilbud og lav din madplan"** → `/`.
Det er allerede en tydelig knap med en forklaring. Problemet er snarere, at **overskriften lover et svar ("hvad koster den?"), som siden ikke giver** – siden viser ingen pris – og at knappen ikke siger, hvad brugeren får. Den samme knaptekst står på oversigtssiden `/opskrifter/`.

## Problemet set fra brugeren
Man kommer fra Google for at lave en ret. Nederst bliver man spurgt "hvad koster den?", men får en generel sætning og en knap, der fører til en forside om "tilbud", ikke til netop denne ret. Det er uklart, hvad klikket giver, så man lader være.

## To meget forskellige løsninger
**A. Kun ny knaptekst (kravets forslag):** "Se hvilke butikker der har tilbud til denne ret i denne uge". Én linje i byggescriptet. Risiko: **lover noget, siden ikke kan holde** – forsiden viser ugens forslag, ikke et opslag på den enkelte ret; er der ingen tilbud til retten den uge, er svaret "ingen" (Anden mening-agenten nævnte samme risiko).
**B. Ærlig løfte-linje + knap (valgt):** overskriften og afsnittet omskrives til det, forsiden faktisk gør, og knappen får en kort, ærlig tekst. Ingen priser, ingen påstand om netop denne rets tilbud.
**Valg: B.** Samme omfang for byggescriptet (tekst i én skabelon, ens på alle sider), men ingen brudt forventning.

## Detaljeret beskrivelse (kun tekst – layout uændret)
Rækkefølge uændret (efter "Næring", før "Flere opskrifter i samme stil"); samme `.knap`-stil (min-højde 48 px ≥ 44 px, fuld synlig fokusring fra browserens standard eller `outline: 2px solid var(--knap); outline-offset: 2px`), samme afstande på mobil (400 px) og desktop. Ingen ny farve, ingen billede, ingen animation.

**Tekster (ord for ord):**
- Overskrift (`h2`): "Lav den af ugens tilbud"
- Afsnit: "Tilbuddene skifter hver uge. Vælg din butik, så laver Måltidsjagten en madplan og en indkøbsliste, hvor ugens tilbud er brugt – og viser, hvad ugen koster." (To korte sætninger. Nævner hverken priser eller tilbud for netop denne ret.)
- Knap: "Se ugens tilbud og din madplan"
- Under knappen, `.lille` (14 px, `--t3`): "Gratis. Du behøver ikke at oprette en bruger."  *(Kun hvis det er sandt: siden virker uden login – Ejeren bekræfter; ellers udelades linjen.)*

Oversigtssiden `/opskrifter/` beholder sin nuværende knaptekst (kravet nævner kun opskriftssiderne; ændring dér er ikke-mål). Opskriftsnavne i ellers uændret markup; titel, beskrivelse, JSON-LD og brødkrumme røres ikke.

## Tilstande
Statisk side: ingen tom-/indlæsnings-/fejltilstand. Mange/få ingredienser: uden betydning. Uden JavaScript: virker (almindeligt link). Mørkt tema: siden bruger lyst tema, uændret.

## Tilgængelighed
Knappen er et rigtigt `<a>` med beskrivende tekst (ingen "klik her"). Kontrast hvid på #C9561E er allerede i brug. Overskriftsrækkefølgen (h1 → h2) uændret.

## Hvordan hvert acceptkriterium opfyldes
1. *Alle 193 sider har den nye tekst* – én skabelon i `byg_sider.py` (linjen med `Hvad koster den i denne uge?`), kør `python -I scripts/byg_sider.py`; kontrolen tjekker, at ingen side har den gamle tekst.
2. *Ingen priser eller tilbud på siderne* – teksten har ingen tal og lover ingen tilbud til netop retten.
3. *Titler, beskrivelser og markup uændrede* – kun to tekststrenge og knappens tekst ændres.
4. *kontrol.py BESTÅET* – hvis kontrollen tjekker den gamle knaptekst, opdateres den.

## Indvending til Ejeren
- **Kravets eksempeltekst bør ikke bruges ordret:** "Se hvilke butikker der har tilbud til denne ret i denne uge" lover et opslag pr. ret, som forsiden ikke giver (og som kan have svaret "ingen"). Ærlig formulering: se ovenfor. Forslag til accept (1): "alle sider har den nye tekst, og teksten påstår ikke, at netop denne ret har tilbud".
- **Overskriften "Hvad koster den i denne uge?" bør også væk** – den er det egentlige brudte løfte, ikke knappen.
- **Tilføj accept:** (5) nederste blok er højst 6 linjer tekst på 390 px, og knappen er mindst 44 px høj.
- Hypotesen kan først vurderes med den anonyme hændelsesmåling, som ligger langt nede; overvej at rykke den op.
