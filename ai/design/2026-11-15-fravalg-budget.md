# Design: fravalg og budget

**Problem:** forslaget kan ikke bruges af familier, der ikke spiser svinekød eller fisk, og ingen kan sige "højst 600 kr om ugen".
**Forslag 1:** en ny side/trin "Dine præferencer" før butikvalget. Forkastet: endnu et trin forsinker det vigtigste (se ugens madplan), og de fleste ændrer ikke valgene.
**Forslag 2 (valgt):** valgene bor i den eksisterende "Dine valg"-boks (personikonet), hvor man allerede vælger voksne og børn. Boksen er det naturlige sted ("senere fx økologi og allergier", står der i koden).
**Indhold:** under voksne og børn: "Vi spiser ikke …" som ni vælgerknapper (Svinekød, Okse og kalv, Kylling og and, Fisk og skaldyr, Kød og fisk [= kødfri], Løg, Svampe, Mælkeprodukter, Æg) og "Budget for ugens aftensmad (valgfrit)" som et talfelt med "kr" og "Fjern". Nederst en lille note: fravalg er ikke en allergigaranti.
**Mobil:** boksen fylder bredden; knapper er 44 px høje; talfeltet er 110 px bredt og åbner taltastaturet.
**Tilstande:** (1) ingen valg: alt som før. (2) fravalg: forslag, "Vælg selv" og "Byt" viser kun retter uden det valgte; knappen i toppen viser "N fravalg" på desktop. (3) budget holdt: grøn besked "Inden for dit budget: X af Y". (4) budget ikke muligt: gul besked "Billigste uge vi kan finde her koster X – Z over dit budget. Prøv en anden butik eller et højere budget." (5) for få retter tilbage (færre end 12): fravalget bruges ikke, og en gul besked siger hvorfor.
**Valg gemmes** på enheden og på brugeren (som husstanden).
**Tilgængelighed:** knapperne er `aria-pressed`, talfeltet har navn, farve er aldrig det eneste signal.
