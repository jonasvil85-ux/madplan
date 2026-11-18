# Dagsrapport 2026-11-18
**Siden i dag:** Sund. Udgivet side grøn, kontrol bestået (0 fejl, 10 advarsler); browserudseendet er kun målt af Browser-QA, ikke set af mig.
## Ændret på siden (slået sammen)
- Sidefod som tryk-flader på mobil (3104489, klasse A, forsøg 2): rolig liste med 48 px rækker, +/– ved teksten på desktop. Kontrollanten godkendte; kontrol.py og Chromium-test bestået (i GitHub Actions). Eneste ændring af index.html i døgnet.
- Browsertesten kan køre i skyen (3b28eb5, klasse A, kun test): fejl i siden giver nu FEJLET, ikke bare "IKKE KØRT". Ingen ændring for brugeren.
## Afvist eller rullet tilbage
- Intet nyt i dag. Stadig rullet tilbage fra 17/11: "Hvor handler du?" (090801b); venter på genindsendelse med rettet runner.
- Stadig afvist/parkeret uden nyt forsøg: ai/2026-11-16-datafejl (H), ai/2026-11-15-fravalg-budget, ai/2026-11-16-mobil-tryk-flader.
## Data
- retter.json er genereret 2026-11-15T08:39 (ingen ny dataændring i git siden 16/11). 479 retter: netto 64, bilka 58, kvickly 60, meny 53, spar 53, rema 50, lidl 50, 365 46, minkoebmand 45. Retter uden billede: 0. Ubrugte billeder: 188.
- Feedback fra brugerne: 0 nye beskeder i dag (FEEDBACK.md: seneste 17/11 var 2 testbeskeder, 0 brugbare). Ingen HASTER.
## Sundhed
- Kontrol: RESULTAT: BESTÅET (0 fejl, 10 advarsler). Udgivet side: nået, matcher main ja (Vagtpost 07:07 UTC, begge domæner OK; Browser-QA GRØN, 0 JS-fejl, intet vandret scroll, 30 små tryk-flader på mobil). Advarsler af betydning: 5 dyre andretter (495–758 kr for hele retten), Kvickly svinemørbrad mangler på ingrediensliste, 25 Netto-ingredienser uden ty, 188 ubrugte billeder. Ikke tjekket: sidefodens Chromium-test (Playwright mangler i skyen, kun kørt i Actions), farvekontrast, tastatur, login.
## I morgen
- Øverst i backloggen: "Ret kendte datafejl" (DATA, H, backend-udvikleren); "Hvor handler du?" skal genindsendes (frontend).
## Til prøve hos Jonas
- Sidefoden på mobil: links nederst (fx "Om Måltidsjagten") er nu en liste med store tryk-flader. Er det nemmere at ramme? Ser det rigtigt ud? Noget forvirrende?
## Til Jonas
- Grundlovs-punkter fra Sikkerhedsagentens uge 47 (kun du kan gennemføre): H2 (kontrollant-workflowet adskiller grenens kode fra hemmeligheder), L2/L3 (faste versioner i workflows), politiktekst i M4 og M5. Se ai/rapporter/2026-uge-47-sikkerhed.md.
