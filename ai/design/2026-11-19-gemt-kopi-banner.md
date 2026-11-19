# Design: Banner "Du ser en gemt kopi"

## Set på siden
`sw.js` (`netFoerst`) venter højst 5 sekunder på nettet og leverer derefter den gemte kopi (`gavKopi = true`). Hentes friske data bagefter og er de ændret, sender arbejderen `data-nyt`, og `index.html` genindlæser siden én gang (højst hver 60. sekund). Er data uændrede, sker der intet, og siden siger aldrig, at den har været en kopi. Er man helt uden net, ser man kopien uden nogen forklaring. Skærmbillederne fra Browser-QA (GRØN, 0 fejl) viser en side uden noget banner, og toppen (`header.top`, logo + bruger + husstand) er allerede fyldt på 390 px.

## Problemet set fra brugeren
I butikken med dårlig dækning ser man tilbud og priser, uden at vide at de kan være en uge gamle. Brugeren kan komme til at tro, at et tilbud stadig gælder, og stå ved hylden med en forkert pris.

## To meget forskellige løsninger
**A. Fast bjælke øverst i skærmen (sticky):** altid synlig, mens man ruller. Utvetydig, men æder højde på en telefon, flytter hele siden ned, og "hele forsiden på én skærm" (krav 12 i "Hvor handler du?") bliver sværere.
**B. Rolig linje i sidens flow lige under toppen (valgt):** ét kort afsnit på ca. 44 px, som skubber indholdet ned, så længe den vises, men ikke følger med ved rulning. På indkøbssedlen (trin 3/5) gentages den som en lille grå linje over listen, fordi det er dér, en forkert pris gør skade.

**Valg: B.** Siden skal være rolig; bannerets opgave er at forklare, ikke at advare. Gentagelsen på selve indkøbslisten er den eneste placering, hvor tiden er afgørende.

## Hvornår vises den (signal)
Arbejderen sender to beskeder (`postMessage` til siden, samme kanal som `data-nyt`):
- `{type:'gemt-kopi'}` når `gavKopi` sættes til true (5 sekunders grænsen eller netfejl), for navigation OG for `retter.json`/`tilbudsliste.json`.
- `{type:'data-frisk'}` når en fetch lykkes og kopien er opdateret (uanset om data er ændret).
Siden husker `gemtKopi = true` i hukommelsen (ikke i `localStorage`, så banneret ikke hænger fast til næste besøg). Banneret vises kun, når `gemtKopi` er sand, og skjules ved `data-frisk` eller når en ny hentning lykkes. Ændrede data genindlæser stadig siden som i dag (så forsvinder banneret af sig selv). **Første besøg og onlinebrug viser aldrig banneret.**

## Placering (mobil 390 px og desktop)
1. Direkte under `header.top`, over første kort. Samme bredde som kortene, `margin-bottom: 12px`.
2. Desktop: samme placering, maks. bredde som indholdet (ikke fuld skærmbredde).
3. Indkøbsliste (trin 3 og indkøbsseddel): en linje over listen med samme tekst, kun uden knap: "Priserne er fra en gemt kopi."

## Udseende
- Baggrund `--surface-2`, 1 px kant `--border`, `--radius`, indre afstand 10 × 14 px. Ingen rød eller gul (rolig side, én accent): ikon er en lille 16 px "ur"-glyf i `--text-3`.
- Tekst 14 px / 1.4, `--text-2`; fed første sætning i `--text-1`.
- Knap "Prøv igen": sekundær stil (kant `--border`, ingen udfyldning), min-højde 44 px, min-bredde 44 px, tekst `--text-1`. På 390 px ligger knappen under teksten, fuld bredde; fra 600 px til højre på samme linje.
- Ingen animation. Banneret må ikke flytte siden, mens man læser: vises ved indlæsning (før første maling, hvis signalet er kendt) og senere kun ved at fylde pladsen over indholdet *når siden står i top*; er brugeren rullet ned, ventes til næste rulning til toppen (undgår hop).

## Tekster (ord for ord)
- Titel (fed): "Du ser en gemt kopi."
- Tekst: "Tilbud og priser kan være ældre end i dag." Er datoen kendt (`data.genereret`): "Tilbud og priser er fra 17. november." (formateret som resten af siden; vises KUN, hvis datoen er kendt og gyldig – opfind aldrig en dato).
- Knap: "Prøv igen"
- Mens der prøves: knappen viser "Henter …", er deaktiveret (`aria-disabled`), højde uændret.
- Lykkes det: banneret forsvinder, siden genindlæses kun hvis data er ændret; en kort linje i `aria-live` siger "Opdateret." i 3 sekunder på banneret plads (ingen layoutspring: pladsen holdes 3 sekunder, derefter lukkes den med 150 ms højdeovergang, kun hvis `prefers-reduced-motion` ikke er sat).
- Lykkes det ikke: banneret bliver, knappen er igen aktiv og teksten får linjen: "Ingen forbindelse lige nu. Det du har gemt virker stadig."

## Tilstande
- **Online, friske data:** intet banner.
- **Gemt kopi leveret (langsomt net):** banner; forsvinder af sig selv, når friske data kommer.
- **Helt offline:** banner med "Prøv igen"; ingen fejlmeddelelse ud over ovenstående.
- **Første besøg uden net:** ingen kopi findes; siden viser sin eksisterende fejlside (uændret, ikke dette krav).
- **Uden service worker (ældre browsere):** intet banner; intet at forklare.
- **Indlæser:** banneret vises ikke, før arbejderen har meldt `gemt-kopi`.
- **Få/mange retter:** uden betydning for banneret.

## Tilgængelighed
`role="status"` + `aria-live="polite"` (ikke `alert`: det er ikke en fejl). Kontrast mellem `--text-2` og `--surface-2` ≥ 4,5:1 i både mørkt og lyst tema (måles i Browser-QA). Knappen har synlig fokusring (2 px `--valgt`, offset 2 px) og kan nås med tab lige efter toppens links; Enter/mellemrum udløser den. Ikonet er `aria-hidden`.

## Hvordan hvert acceptkriterium opfyldes
1. *Vises kun ved cache-visning:* kun `gemt-kopi`-beskeden fra arbejderen (sat, når kopien faktisk leveres) viser banneret; ingen sammenligning med `navigator.onLine`, som ikke kan stoles på.
2. *Forsvinder, når frisk data er hentet:* `data-frisk` (og genindlæsning ved ændrede data) skjuler det; testes ved at stoppe netsvaret i Chromium, se banneret, så åbne nettet og trykke "Prøv igen".
3. *Rører ikke cache-strategien for billeder:* kun `netFoerst` for HTML/JSON får `postMessage`-linjer; `gemFoerst` (billeder) og alle cache-navne er uændrede. `VERSION` i `sw.js` hæves, fordi arbejderen ændres (klasse H).
4. *Regressionstest består:* ingen beregning ændres; browsertesten får to tjek (banner vist ved simuleret langsomt/ingen net, ikke vist ved friskt svar).

## Indvending til Ejeren
- **Accept (2) er ufuldstændig:** i dag genindlæser siden sig selv, når data er ændret; banneret er kun synligt i de tilfælde, hvor data er UÆNDREDE eller nettet ikke svarer. Formulér: "(2) banneret forsvinder, når frisk data er hentet – uanset om data er ændret – og efter 'Prøv igen' uden at siden hopper".
- **Tilføj accept:** (5) banneret må ikke give vandret scroll og ikke skubbe "Brug forslaget" ud af første skærm på 390 × 844 px, når det vises (dvs. højst 2 linjer + knap; ellers skjules knappen bag "Prøv igen" i samme række); (6) første besøg og normal onlinebrug viser aldrig banneret (testet).
- **Klasse:** `[H]` er rigtigt, fordi `sw.js`/cache berøres; men selve UI'et er A. Hold ændringen i arbejderen til de to `postMessage`-linjer.
- **Anbefaling:** vis datoen på banneret kun, hvis `data.genereret` er pålidelig; ellers ingen dato frem for en forkert.
