# Dagsrapport 2026-11-15
**Siden i dag:** Sund. Udgivet side grøn (Vagtpost og Browser-QA), kontrollen bestået med 9 advarsler, ingen fejl.
## Ændret på siden (slået sammen)
- Opskriftssider (klasse H, 384f5d1): 193 opskriftssider, oversigt og sitemap, så Google kan se retterne. Godkendt af kontrollanten efter skærpet validering (før/efter byte-identisk for alle 9 butikker, rød-hold, revert-prøve).
- Kun test (klasse A): regressionstest af pris, indkøbsliste og ugeforslag; kontrol.py springer JSON-LD over i JS-tjekket.
- Data: nye aviser Rema 1000 og Lidl (uge 47), billeder til 89 nye retter (Netto, REMA, Lidl), service worker v6 (commits sidste døgn).
## Afvist eller rullet tilbage
- ai/2026-11-15-mobil-tryk-flader: 23 elementer under 40 px på forsiden (krav 0), designfil mangler.
- ai/2026-11-15-indkoebsliste-raekker: afvist proceduralt (klasse H, højst én H pr. dag, mangler BACKLOG-krav). Ingen fejl fundet.
- ai/2026-11-15-fravalg-budget: afvist proceduralt (samme H-grænse); tidligere rød-hold: lammekød, ost og porre slipper igennem fravalg.
- Intet rullet tilbage.
## Data
- Retter i retter.json (genereret 08:39 UTC): 479 i alt. Netto 64, Meny 53, Bilka 58, Rema 50, Kvickly 60, Lidl 50, 365discount 46, Spar 53, Min Købmand 45.
- Retter uden billede: 0 (tjekket på feltet `billede`; om filerne findes er ikke tjekket her). 188 billeder bruges ikke af nogen ret.
## Sundhed
- Kontrol: RESULTAT: BESTÅET (0 fejl, 9 advarsler). Udgivet side: nået, begge domæner OK, retter.json identisk med main (HELBRED.md 10:18 UTC, main 384f5d1; senere commits siden er kun AI-filer). Browser-QA: grøn, 0 JS-fejl, intet vandret scroll.
- Advarsler af betydning: 33 tryk-flader under 40 px på mobil (34 på desktop); 6 hele-ret-priser over ca. 500 kr (andelår, lammekølle, helstegt and); Kvickly: svinemørbrad nævnt i navn men ikke i ingredienser; Netto: 25 tilbudsingredienser mangler `ty`.
- Ikke tjekket: udseende i browser ud over BROWSER.md, farvekontrast, tastatur, andre husstande, login, brugerfeedback og trafik.
## I morgen
- Øverste åbne krav: mobil tryk-flader (UX-udvikleren retter efter afvisning; designfil mangler, UX-designeren). Afviste H-grene (fravalg-budget først) valideres af kontrollanten.
## Til Jonas
- Intet.
