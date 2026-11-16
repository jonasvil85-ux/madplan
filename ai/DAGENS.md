# Dagsrapport 2026-11-16
**Siden i dag:** Sund med advarsler. Udgivet side grøn (Vagtpost 09:20 UTC, Browser-QA), kontrol bestået med 0 fejl og 9 advarsler.
## Ændret på siden (slået sammen)
- Indkøbsliste: korte rækker (mængde og første ret) med Detaljer-link (klasse H, 8c2e4a7). Kontrollanten godkendte efter skærpet validering: linjer og summer uændrede i alle 9 butikker, rød-hold, revert-prøve (se `ai/rapporter/2026-11-16-kontrol.md`).
- Ingen ændringer i `retter.json` det seneste døgn (sidst genereret 2026-11-15 08:39 UTC).
## Afvist eller rullet tilbage
- ai/2026-11-16-datafejl (klasse H, forsøg 1): før/efter-tal for ugepris og indkøbslinjer mangler, 16 ty-advarsler tilbage. Udvikleren retter.
- ai/2026-11-15-fravalg-budget (klasse H) og ai/2026-11-16-mobil-tryk-flader (klasse A): afvist i forsøg 2 og parkeret hos Ejeren (fravalg lader stadig mayonnaise, pesto og "hakket kød 8-12%" igennem; "Om Måltidsjagten" i sidefoden er for lille).
- Intet rullet tilbage.
## Data
- Retter pr. butik: Netto 64, Kvickly 60, Bilka 58, Meny 53, Spar 53, Rema 50, Lidl 50, 365discount 46, minkøbmand 45 (i alt 479). Retter uden billede: 0 (tjekket i `retter.json`). 188 billeder bruges ikke af nogen ret.
- Ny avis- eller billedkørsel i dag: ikke set i commits det seneste døgn.
## Sundhed
- Kontrol: RESULTAT: BESTÅET (0 fejl, 9 advarsler), regressionstest bestået. Udgivet side: nået, matcher main (retter.json identisk, 479 retter, sw.js v6, begge domæner). Advarsler af betydning: 5 retter med pris over ca. 490 kr for hele retten (andelår, lammekølle, helstegt and); Kvickly-svinemørbrad mangler ingrediens; 25 Netto-ingredienser mangler `ty`.
- Browser-QA grøn: intet vandret scroll, 0 JS-fejl, 0 ødelagte billeder. Mange små tryk-flader: 33 på mobil, 34 på desktop (under 40 px).
- Ikke tjekket: udseende i browser (kun de målinger Browser-QA tager), farvekontrast, tastatur, opskriftssider live.
## I morgen
- Øverste krav: ret kendte datafejl (Backend/data-udvikleren, med før/efter-tal), derefter mobil tryk-flader (UX-designer, så udvikler) og budget (H).
## Til Jonas
- Intet.
