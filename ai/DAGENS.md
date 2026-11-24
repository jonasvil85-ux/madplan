# Dagsrapport 2026-11-24
**Siden i dag:** Sund med advarsler. Udgivet side grøn (Vagtpost 07:02 UTC, begge domæner, 566 retter, retter.json identisk med main), kontrol bestået med 0 fejl og 4 advarsler.
## Ændret på siden (slået sammen)
- Rema: "ris" kobles ikke længere til riskiks (merge 2604467, klasse H, kontrollanten). 12 rema-retter fik ris som almindelig vare (7,5 kr) i stedet for en forkert riskiks-vare på indkøbslisten; byggeren afviser nu forbudte par. Bestået: kontrol, regressionstest, dækningstest, før/efter for 9 butikker (kun de 12 rema-retter ændrer pris), fire rød-hold-forsøg og tilbagerulningsprøve.
- Ved samme genbygning fjernes udløste Kvickly-tilbud (K31/K32) fra opskrifter.json: Kvickly-uge 2+2 går 576 → 567 kr (ifølge kontrolrapporten).
## Afvist eller rullet tilbage
- ai/2026-11-24-ux (søgning ental/flertal, klasse A, forsøg 2): afvist. Søgningen er i orden, men grenen sletter afsnit 7a i `kontrol.py`, så 20 %-testen ikke længere køres, og det er ikke nævnt i udviklerrapporten.
- Ingen tilbagerulning. Stadig afvist/parkeret fra før: se `ai/STATUS.md`.
## Data
- Retter: Kvickly 88, Bilka 80, Meny 73, Spar 71, Netto 60, Rema 56, Lidl 49, 365discount 49, minkøbmand 40 (i alt 566). Uden billede: 0. 313 billeder bruges ikke af nogen ret. `retter.json` genereret 2026-11-24 06:38 UTC. Nye aviser/retter i dag: ingen nye retter (566 som i går).
- Feedback fra brugerne: ingen ny feedback-rapport i dag (seneste: 23/11, 4 beskeder, 0 brugbare ifølge Ejeren, 2 afvist og 2 støj). Ingen HASTER.
## Sundhed
- Kontrol: RESULTAT: BESTÅET (0 fejl, 4 advarsler), kørt af mig på main 54c2ce4. Udgivet side: nået, matcher main ifølge Vagtposten (på 693d8c0, 07:02 UTC). Browser-QA GRØN (0 JS-fejl, intet vandret scroll, flow ok; 30 tryk-flader under 40 px på mobil).
- Advarsler af betydning: 18 ingredienser uden `ty` hos hhv. Rema og Lidl; 313 ubrugte billeder; sidefodens Chromium-test kunne ikke køres i min session (Playwright mangler).
- Ikke tjekket: udseende i browser (skærmbilleder ikke åbnet), kontrast, tastatur, iOS Safari, indkøbsliste for de 12 rema-retter i browser.
## I morgen
- Øverste åbne krav: søgning i "Vælg selv" med ental/flertal (UX, A, frontend-udvikleren; forsøg 3, uden at miste 20 %-testen). Derefter test af selve byggeren (TEST).
## Til prøve hos Jonas
- Intet (ingen synlig ny funktion udgivet).
## Til Jonas
- Intet nyt. Ejerens sikkerhedspunkter (H2, M4, M5, L2/L3) og forslaget om, at tilbudsrutinen kører `byg_retter.py` og `kontrol.py` før commit, afventer dig (se `ai/rapporter/2026-11-24-ejer.md`).
