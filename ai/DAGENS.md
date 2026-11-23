# Dagsrapport 2026-11-23
**Siden i dag:** Sund med advarsler. Udgivet side grøn (Vagtpost 07:13 UTC, begge domæner, 566 retter), kontrol bestået med 0 fejl og 4 advarsler.
## Ændret på siden (slået sammen)
- Én ændring: 20 %-regel mod fejlkoblinger i `byg_retter.py` (merge 2aa01e8, klasse H, kontrollanten). Tre fejlkoblede retter er fjernet (bilka, 365, rema), så en ret ikke prissættes ud fra en alt for lille vare. Brugeren mister tre retter. Bestået: kontrol, regressionstest, dækningstest, før/efter-tal for 9 butikker (priser og indkøbslister uændrede), 6 egne fejlforsøg og tilbagerulning kan prøves.
- Billeder til nye retter (automatisk, 22/11 kl. 13:37 UTC).
## Afvist eller rullet tilbage
- ai/2026-11-23-ux (søgning i "Vælg selv", klasse A, forsøg 1): afvist. "rejer" finder ikke længere "Røget laks og kutterrejer", og "hvide bønner" rammer retter med hvidløg.
- Ingen tilbagerulning. Stadig afvist/parkeret fra før: sidefod-tryk-flader, browsertest-sky, fravalg-budget, mobil-tryk-flader (se `ai/STATUS.md`).
## Data
- Retter: Kvickly 88, Bilka 80, Meny 73, Spar 71, Netto 60, Rema 56, Lidl 49, 365discount 49, minkøbmand 40 (i alt 566). Uden billede: 0. 313 billeder bruges ikke af nogen ret.
- `retter.json` genereret 2026-11-23 06:36 UTC.
- Fund fra kontrollanten: 6 rema-retter kobler "ris" til en riskiks-vare (kan vælges i "Vælg selv"). Ejeren har det til et DATA-krav.
- Feedback fra brugerne: ingen ny feedback-rapport i dag (seneste i `ai/FEEDBACK.md`: 17/11, 2 testbeskeder). Ingen HASTER.
## Sundhed
- Kontrol: RESULTAT: BESTÅET (0 fejl, 4 advarsler) på main e4413dc (kørt af mig). Udgivet side: nået, matcher main ifølge Vagtposten (på cda1365, før kontrollantens sidste rapport-commit). Browser-QA GRØN (0 JS-fejl, intet vandret scroll, flow ok).
- Advarsler af betydning: 18 ingredienser uden `ty` hos hhv. Rema og Lidl; 313 ubrugte billeder; sidefodens Chromium-test kunne ikke køres i min session (Playwright mangler).
- Ikke tjekket: udseende i browser (skærmbilleder ikke åbnet), kontrast, tastatur, iOS Safari.
## I morgen
- Øverste krav: søgning i "Vælg selv" med ental/flertal (UX, A, frontend-udvikleren; forsøg 2 efter afvisning). Derefter måling af ugeforslagets pris ved flere retter (TEST) og genindsendelse af "Ét kort".
## Til prøve hos Jonas
- Søgefeltet i "Vælg selv" (udgivet tidligere): skriv en ret eller ingrediens, fx "kylling" eller "kartofler". Er det intuitivt at finde og rydde? Finder det det, du forventer, også i ental/flertal (ental/flertal er kendt svagt: "kartoffel" 11 mod "kartofler" 72 retter)? Noget forvirrende?
## Til Jonas
- Intet (Ejerens liste over sikkerhedspunkter, der afventer dig, ligger i `ai/rapporter/2026-11-23-ejer.md`).
