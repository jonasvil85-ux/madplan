# Anden mening 2026-11-18 (kørsel 1)

Nyt i seneste commit: to designfiler i `ai/design/` (`2026-11-18-en-regel-to-butikker.md`, `2026-11-18-gode-tilbud-grupper.md`). Backloggen er ikke ændret. Emner: 2. Kald til modellen: 3 af 3 (emne 1: kreativ + kritisk, emne 2: kritisk). Modellen er rådgiver; vurderingen er min.

## Emne 1: Én regel for to butikker (ja/nej-forslag under butikslisten)

**Spørgsmål:** Hvordan siges og vises "spar X kr ved også at handle i Y" roligt og ærligt, så boks og kort ikke modsiger hinanden?

### Idéer (kreativ runde)
1. *Blid bannerlinje* (sikker): stort set vores nuværende design. **Valgt** (bekræfter designet).
2. *Spar-meter med pop-up* (spilificering): **Afvist.** Animation og spil stride mod "rolig side"; pop-up afbryder en travl forælder.
3. *Scratch-card* (skør): **Afvist.** Gør en pris til et lotteri; mod "ærlige tal".
4. *Bytte-fane "Vil du overveje en anden butik?"* (vender problemet): **Delvist.** Spørgsmålsformen er pænere end en sælgende påstand, men vi beholder det konkrete tal i overskriften, så ærligheden og besparelsen står først.
5. *Én linje, altid "Bedste pris i dag"* (radikalt enkel): **Delvist.** Idéen om færre linjer er god; "altid vis" er afvist, fordi det giver støj ved nej og lover en pris, brugeren ikke har bedt om. Tog: de to prislinjer og forbeholdet kan slås sammen til én sætning.

### Modellens kritik (kort)
Uklart hvordan "valgt butik" fastlægges; "begge uger regnet" er uklar; lagerstatus mangler; transport/tid er nævnt men ikke regnet; kun Netto som partner; tillidsbrist ved afrunding; boks der først dukker op sent kan forvirre.

### Min vurdering
- Meget af kritikken er misforståelser: partneren er allerede "det bedste par" (ikke altid Netto), "valgt butik" er brugerens egne afkrydsninger, og afrundingsreglen står allerede i designet (besparelse = forskel på viste kroner). **Uenig** i disse.
- **Uenig** i lagerstatus: vi har ikke lagerdata og må aldrig opfinde dem; tilbud er ugetilbud.
- **Delvist enig** i "boks der dukker op sent": designet siger fade-in og ingen reserveret plads, men en boks, der popper ind efter tal er regnet, kan flytte knapper under den, mens brugeren trykker. Det er et konkret, reelt punkt, modellen ikke formulerede præcist.
- **Enig** i, at transportforbeholdet ikke kan regnes; det er derfor, det står som tekst. Ingen ændring.

### Foreslået ændring af designet
- Tekst, færre linjer (valgt idé 5): *"Spar 54 kr ved også at handle i Netto"* (fed) og under den *"367 kr i Lidl + Netto mod 421 kr kun i Lidl. Transport og ekstra tid er ikke regnet med."* (én afsnit i `--text-2`, 14 px; forbeholdet i samme sætning i stedet for tredje linje). Knappen uændret.
- Tilføj under Tilstande: *"Boksen indsættes under butikslisten og skubber kun indhold, der ligger nedenunder; ingen knap eller række, brugeren er ved at trykke på, må flytte sig. Hvis den kommer, mens brugeren ruller, ændres scrollpositionen ikke (`overflow-anchor`)."*
- Afrundingsforslaget i designfilens "Indvending til Ejeren" står fast (test på 20 tilfældige par).

## Emne 2: "Gode tilbud"-grupperne nederst på indkøbslisten

**Spørgsmål:** Er designet (kortere titler ved hele ord, første alternativ som titel + "eller 2 andre slags", 4 rækker pr. gruppe + "Vis 6 flere") ærligt og brugbart i butikken? Kun kritisk runde (ikke flere kald til rådighed til kreativ).

### Modellens kritik (kort)
Afkortning kan skjule hvilken variant; "første alternativ" er vagt; enhedspris/total mangler; filtre/sortering efter pris, allergi, børnevenlighed; lagerstatus; fold-ud kræver klik og kan skjule relevante varer; fuld tekst i tooltip; erstat "eller 2 andre slags" med en liste eller ikon.

### Min vurdering
- **Delvist enig:** "eller 2 andre slags" fortæller ikke hvilke, og brugeren kan komme til at købe den forkerte vare. Designet siger allerede "billigste alternativ først" (så "første" er defineret; modellen overså det), men man bør kunne se de andre uden at forlade rækken. Tooltip/hover virker ikke på mobil, så det **afvises**; i stedet kan "eller 2 andre slags" være en tryk-flade, der folder alternativerne ud i rækken som kort liste (kun avisens egne ord).
- **Delvist enig** i fold-risikoen: i butikken er man træt af at trykke. Da gruppen allerede er lukket kun når intet er afkrydset, og "Vis 6 flere" er 44 px, er risikoen begrænset; men antallet "· 10" i overskriften skal stå synligt, så man ved, at der er mere.
- **Uenig:** pris står allerede i hver række (`prisCelle`) uanset fold, og tilbud har ikke altid sammenlignelig enhedspris; filtre/sortering/allergi/lagerstatus er nye funktioner uden grundlag i vores data og går imod "rolig side". Generelle råd uden konkret indhold er ikke taget med.
- Sammenligningen med afvist kompakt liste (A) ændrer sig ikke.

### Foreslået ændring af designet
- Tilføj: *"'eller 2 andre slags' er en knap (min. 44 px høj), der viser de andre alternativer som en kort liste under rækken med avisens egne navne; `aria-expanded`. Ingen tooltip (virker ikke på mobil)."*
- Tilføj: *"Overskriften viser altid det samlede antal ('· 10'), også når gruppen er lukket."* (står allerede for antallet; gør det til accept-punkt.)
- Accept-formuleringen fra designets egen "Indvending til Ejeren" (1–5) står fast.

## Bemærkninger
- `anden-mening-svar.txt` (tom, ikke sporet) ligger i roden; ikke rørt, fordi kun rapporten må ændres. `spoergsmaal.txt` er slettet.
- Ingen personoplysninger, nøgler eller kode er sendt; kun egne beskrivelser af designene.

Nyttigt: delvist (idéen om at slå forbeholdet sammen med prislinjen, at en sent indsat boks kan flytte knapper, og at "eller 2 andre slags" ikke viser hvilke; resten var generelt eller misforstået).
