# Design: opskriftssider

**Problem:** søgende familier finder ikke Måltidsjagten, fordi ingen ret har en adresse.
**Forslag 1:** én side pr. ret med pris pr. person fra ugens tilbud. Forkastet: priserne er forældede om få dage og ville være direkte vildledende for Google og brugere.
**Forslag 2 (valgt):** tidløse opskriftssider uden pris, med stærk indhold og en tydelig vej ind i appen, hvor ugens pris står.
**Layout:** samme rolige udtryk som appen (varm hvid baggrund, orange knap, Inter). Mobil: billede i fuld bredde, små pille-chips for tid/personer/køkken, ingredienser i et hvidt kort, nummereret fremgangsmåde, næring, én stor knap, og fire relaterede retter som billedkort. Brødkrumme øverst. Mørk tilstand følger systemet.
**Tilstande:** ret uden billede (billedet udelades); ret uden næring (sektionen udelades).
**Tilgængelighed:** knapper mindst 48 px, brødkrumme med `aria-label`, billeder med alt-tekst, kontrast som appen.
