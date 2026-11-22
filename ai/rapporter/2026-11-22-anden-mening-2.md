# Anden mening 2026-11-22 (kørsel 2)

Udløst af commit c2cb378: to nye designfiler i `ai/design/` (`2026-11-22-soeg-vaelg-selv.md`, `2026-11-22-gode-tilbud-smaating.md`). Ingen ændring i `ai/BACKLOG.md` og ingen `[SIKKERHED]`-krav. Rollen er UX Designer. Kravet "Søg i Vælg selv" blev idévalideret i kørsel 1 (kreativ + kritisk); her er det *designet* der prøves, kun kritisk runde.

Kald brugt: 2 af 3 (ingen kreativ runde: kørsel 1 gav allerede idéerne, og designvalgene er truffet).

## Emne 1: Design af søgning i "Vælg selv"
**Spørgsmål i én linje:** Findes der huller i matchreglerne, tilstandene og sammenfoldningen af "Din uge"?

### Idéer
Ingen (kun kritisk runde; idéerne fra kørsel 1 gælder).

### Modellens kritik (omskrevet) og min vurdering
1. **Bøjninger/flertal** ("kyllingefileter", "kyllingefileten" matcher ikke) – **delvist enig.** Modellens eksempler er svage (det, man taster, er næsten altid begyndelsen af ordet, og ordbegyndelse fanger "kyllingefilet"). Men der er et ægte hul, som modellen ikke så: man taster ofte flertal ("gulerødder", "kartofler", "æbler"), og retterne har ental. Se forslag A.
2. **æ/ø/å ikke håndteret** – **uenig.** Designet siger, at æ, ø, å skrives som de er, og de er netop *ikke* sidestillet med a/o. At "a" skulle fange "åben" ville give falske træffere. (Brugere uden dansk tastatur, der skriver "ae/oe/aa", er et lille, men tænkeligt hul; ikke taget med nu: ingen belæg for det hos familien, og det ville gøre matchning mindre forudsigelig.)
3. **"ris" kan ramme "Paris" hvis ordsplitningen fejler** – **uenig som designfejl** (det er en implementeringsrisiko, og designet har allerede testcasen "ris"/ordbegyndelse). Tages som testpunkt, ikke som ændring.
4. **Ingen besked ved 0 træffere** – **uenig.** Misforstået: designet har en tom-tilstand med `Vis alle retter` og resultatlinjen.
5. **Skjulte valgte retter tælles med i "7 retter valgt"** – **uenig.** Det er præcis, hvad designet vil: madplanen og listen må aldrig miste valgte retter, og en note forklarer det. Modellen læste det som et problem uden at se noten.
6. **Foldning af "Din uge" ændrer scrollposition og kan skjule noten** – **delvist enig.** Noten om skjulte valgte retter må ikke ligge inde i den sammenfoldede "Din uge"; den skal stå under resultatlinjen, så den altid er synlig. (Den flytning af første træffer, modellen kalder et problem, er hele formålet.)

### Foreslået ændring af designet
- **A. Flertalsfald-tilbage:** *"Finder et søgeord ingen retter, og ender det på `er`, `e`, `r` eller `ne`, prøves det igen uden endelsen (min. 4 tegn tilbage); Vokalskifte og uregelmæssige flertal håndteres kun via en lille fast liste (gulerødder→gulerod, kartofler→kartoffel), ikke generelt."* Hold den lille og testbar; den må ikke ændre noget, når der allerede er træffere. Bemærk samtidig, at designets testcase "gulerod" ikke finder "gulerødder" (ø ≠ o): ingrediensnavne skal søges på det, der står i data; test begge former.
- **B.** Noten om valgte, skjulte retter placeres under resultatlinjen, uden for den sammenfoldede "Din uge".
- **C.** Tilføj testcases: "ris" mod "Paris"/"citrus", "kyllinger"/"gulerødder" (flertal), "gulerod".

## Emne 2: Design af "Gode tilbud"-småting
**Spørgsmål i én linje:** Findes der huller i "Vis 1 mere"/"Vis N flere" og i rækkefølgen foldet/udfoldet?

### Idéer
Ingen (kun kritisk runde).

### Modellens kritik (omskrevet) og min vurdering
Modellen misforstod designet: den behandlede afvist alternativ B ("Valgt"-undergruppen) som valgt.
1. **Afkrydsede rækker flytter til "Valgt"** – **uenig.** Findes ikke i det valgte design (A); rækkerne bliver stående.
2. **Knaptekst ikke opdateret for skærmlæsere** – **delvist enig.** Teksten genskabes ved hver visning, så etiketten er rigtig; men en skærmlæser får ikke at vide, at tallet er ændret, når man afkrydser i foldet gruppe. Lav prioritet; ikke taget med (ville give støj på en rolig side).
3. **Scrollposition hopper ved rækkeskift** – **uenig** for designet (ingen række flytter sig, når man afkrydser).
4. **Mangler `aria-expanded`/`aria-controls`** – **uenig.** De findes allerede (står i designets første afsnit).

Intet af modellens svar fandt noget nyt i designet. Et hul, jeg selv ser ved gennemlæsning: **fjerner man fluebenet på en række uden for de første 4 i en foldet gruppe, forsvinder rækken under fingeren** (den hører ikke længere til de viste).
- **Foreslået ændring:** *"En række, der er afkrydset i denne visning, bliver stående i visningen, til gruppen foldes eller siden skifter trin, også efter at fluebenet er fjernet (så man kan fortryde)."* Tilføj som accept (6) og som test: afkryds række 7, fjern flueben, rækken står stadig.

## Samlet
Uenighed: 2, 3, 4 og 5 i emne 1 og 1, 3, 4 i emne 2 skyldes, at modellen enten misforstod designet eller opfandt problemer, der allerede er løst. Konkret udbytte: flertalsfald-tilbage, notens placering og "fortryd uden at rækken forsvinder".

Nyttigt: delvist
