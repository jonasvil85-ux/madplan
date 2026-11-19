# Design: Motoren i trin (`simFraButikker` delt op)

## Set på siden
Kravet er teknisk (ingen synlig ændring), men brugeren mærker det: en beregning af én uge kan tage 60–280 ms i ét stræk. På telefon betyder det, at et tryk på en butik eller "Byt" kan føles hakkende, hvis siden ikke svarer på trykket med det samme. Browser-QA viser indlæsning under 1 s, så problemet er ikke målt som synligt i dag.

## Problemet set fra brugeren
Et tryk skal give svar med det samme. I dag fryser siden et øjeblik, mens ugen regnes, og brugeren ved ikke, om trykket virkede.

## To meget forskellige løsninger
**A. Del beregningen i trin med pause imellem (Ejerens krav):** siden forbliver responsiv, men det kræver en omskrivning af kernen (klasse H, høj risiko for prisfejl).
**B. Lad beregningen stå, men giv øjeblikkelig respons:** trykket får straks en tydelig tilstand (valgt række, "Regner …" på ugens plads), og først derefter regnes ugen. Ingen ændring af beregningen, kun af rækkefølgen af visning og beregning.

**Valg: B først, A kun hvis B ikke er nok.** Brugerens problem er manglende respons, ikke de 60–280 ms i sig selv. B løser det uden at røre priserne; en fejl i en pris er værre end en træg knap (`regler.md`).

## Detaljer for B (hvis Ejeren tager den)
- Ved tryk på en butik, "Byt" eller husstandsændring: flueben/knaptilstand opdateres synligt inden for 100 ms (`requestAnimationFrame` før den tunge beregning).
- Ugens plads (`#sim-plads`) bevarer sin højde (ingen layoutspring) og viser en rolig tilstand: tekst "Regner ugen …" (14 px, `--text-3`), de gamle kort nedtonet til 60 % uden animation. Ingen spinner.
- Tilgængelighed: `aria-busy="true"` på pladsen under beregning; fjernes bagefter. Tryk-flader uændret (≥ 44 px).
- Tom/fejl: fejler beregningen, vises den eksisterende fejltekst; pladsen låses ikke.
- Beregning efter hinanden: et nyt tryk under beregning kasserer den ældre (kun seneste tryk vises).

## Hvordan acceptkriterierne opfyldes
(1) Regression, budget og sammenlign uændrede: B rører ikke beregningen. (2) "Ingen opgave over 100 ms": B opfylder det IKKE, men sikrer, at trykket vises inden 100 ms. (3) Før/efter-tal for 9 butikker: uændrede.

## Indvending til Ejeren
- Accept (2) måler det forkerte: brugeren mærker *tid til første svar*, ikke længste opgave. Foreslået formulering: "Efter et tryk er ændringen (flueben/knaptilstand/'Regner ugen …') synlig inden for 100 ms målt i Chromium over 5 kørsler for alle 9 butikker; ugens tal er uændrede."
- Kravet er mærket `[UX]`, men er i sin hårde form (opdeling af motoren) et `[BACKEND] [H]`-krav. Opdel i: (a) `[UX] [A]` øjeblikkeligt svar (B ovenfor), (b) `[BACKEND] [H]` opdeling kun hvis (a) ikke er nok.
- Lav prioritet er rimelig: ingen brugerklage, ingen browsermåling viser et problem.
