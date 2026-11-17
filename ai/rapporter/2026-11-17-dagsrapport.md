# Dagsrapport 2026-11-17
**Siden i dag:** Sund med advarsler. Udgivet side grøn (Vagtpost 10:29 UTC, begge domæner), kontrol bestået med 0 fejl og 10 advarsler.
## Ændret på siden (slået sammen)
- Intet nyt er slået sammen i dag. Eneste ændringer på main det seneste døgn er rapporter, designfiler, agentinstrukser og arkitektursiderne (ingen `index.html` eller `retter.json`).
## Afvist eller rullet tilbage
- Rullet tilbage 06:48 UTC (kontrollanten): "Hvor handler du?" (090801b) og flueben-CSS'en (4211735). Årsag: `kontrol.py` fejlede på main i Chromium (TypeError i `sammenlign_browser.py`). Siden er tilbage på butiksvalget fra før 16/11. Ejeren havde selv målt funktionen som fejlfri, så den indsendes igen som gren, når testen er rettet.
- ai/2026-11-17-sidefod-tryk-flader (forsøg 1): afvist, opacity 0.9 tilbage og desktop-ikon løsrevet.
- ai/2026-11-17-browsertest-sky (forsøg 1): afvist, enhver sidefejl giver kun advarsel, så en ødelagt forside kunne give BESTÅET.
- ai/2026-11-16-datafejl (forsøg 1, H): afvist, før/efter-tal mangler. Parkeret hos Ejeren: fravalg-budget og mobil-tryk-flader.
## Data
- Retter: Netto 64, Kvickly 60, Bilka 58, Meny 53, Spar 53, Rema 50, Lidl 50, 365discount 46, minkøbmand 45 (i alt 479). Uden billede: 0. 188 billeder bruges ikke.
- Ingen ny avis- eller billedkørsel: `retter.json` er sidst genereret 2026-11-15 08:39 UTC (ses af tidsstemplet).
- Feedback fra brugerne: 2 nye beskeder, 0 brugbare (begge tests af feedback-kanalen). Ingen HASTER. Kæden chat til Supabase til Product Owner virker.
## Sundhed
- Kontrol: RESULTAT: BESTÅET (0 fejl, 10 advarsler), regressionstest og budget bestået. Udgivet side: nået, matcher main (sw.js v6, 479 retter). Browser-QA GRØN (BROWSER.md): intet vandret scroll, 0 JS-fejl, 33 små tryk-flader på mobil og 34 på desktop.
- Advarsler af betydning: 6 retter med pris over ca. 495 kr for hele retten (andelår, lammekølle, helstegt and); Kvickly-svinemørbrad mangler ingrediens; 25 Netto-ingredienser mangler `ty`; browsertesten af sammenlign butikker kunne ikke køres i min session (Playwright mangler).
- Ikke tjekket: udseende i browser, kontrast, tastatur, iOS Safari. Ejerens browsertest af "Hvor handler du?" er ikke gentaget af kontrollanten.
## I morgen
- Øverste krav: ret kendte datafejl (Backend/data-udvikleren, H, med før/efter-tal for 9 butikker), derefter sidefod som tryk-flader og browsertesten i skyen.
## Til prøve hos Jonas
- Intet. Butiksvalget "Hvor handler du?" er rullet tilbage og kan ikke prøves.
## Til Jonas
- Intet.
