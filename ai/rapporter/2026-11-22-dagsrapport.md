# Dagsrapport 2026-11-22
**Siden i dag:** Sund med advarsler. Udgivet side grøn (Vagtpost 07:03 UTC, begge domæner, 569 retter), kontrol bestået med 0 fejl og 7 advarsler.
## Ændret på siden (slået sammen)
- Datafejl (9bd1683, klasse H, kontrollanten): 6 fejlkoblede dyre retter (andelår/hel and) fjernet, ny Frikadeller-ret hos Min Købmand, kontrollen fejler nu over 450 kr. Hjælper brugeren med en realistisk ugeplan. Bestået: kontrol.py, før/efter-tal for 9 butikker, tilbagerulning kan prøves.
- Søg i Vælg selv (8ea3f25, klasse A, kontrollanten): søgefelt, der finder ret og ingrediens. Bestået: kontrol.py inkl. søgetest i Chromium, regression og budget uændrede.
- Data: nye tilbudsaviser (rema, lidl uge 48 og tidligere netto, meny, bilka, kvickly, spar, minkøbmand) og billeder.
## Afvist eller rullet tilbage
- Intet i dag. Ingen tilbagerulning. Ældre grene (se STATUS.md) venter stadig uændret, bl.a. 2026-11-17-sidefod-tryk-flader og -browsertest-sky.
## Data
- Retter: Kvickly 88, Bilka 81, Meny 73, Spar 71, Netto 60, Rema 57, 365discount 50, Lidl 49, Min Købmand 40 (i alt 569). Uden billede: Lidl 36, Rema 32, Min Købmand 1 (billedhandlingen mangler at køre). 313 billeder bruges ikke.
- Feedback fra brugerne: ingen nye beskeder siden 2026-11-17 (FEEDBACK.md); ingen HASTER.
## Sundhed
- Kontrol: RESULTAT: BESTÅET (0 fejl, 7 advarsler). Udgivet side: nået, matcher main (Vagtpost 07:03 UTC; main er siden kun ændret i rapporter). Browser-QA GRØN: 0 JS-fejl, intet vandret scroll, flow ok; 30 små tryk-flader på mobil, 31 på desktop.
- Advarsler af betydning: 36+32+1 retter uden billede; 18 ingredienser uden `ty` hos hver af Rema og Lidl; sidefodens Chromium-test kunne ikke køres i min session (Playwright mangler).
- Ikke tjekket: udseende i browser, kontrast, tastatur, iOS Safari.
## I morgen
- Øverste krav i BACKLOG: "Ét kort: Hvor handler du?" og "Én regel for to butikker" genindsendes med rettet Chromium-runner (Frontend-udvikleren); opfølgning om datafejl (20 %-reglen) hos Backend. Rækkefølgen er Ejerens, ikke tjekket af mig.
## Til prøve hos Jonas
- Søg i Vælg selv: skriv en ret eller en vare (fx "kylling") i søgefeltet i "Vælg selv". Finder den det, du forventer? Er det tydeligt, hvor feltet er? Noget forvirrende?
- Gode tilbud nederst på indkøbslisten (udgivet 21/11, fra Ejerens rapport): er grupperne lettere at kigge i og er "se resten" tydeligt?
## Til Jonas
- Intet. (Sikkerhedspunkter H2, M4, M5, L2/L3 afventer stadig dig, jf. Ejerens rapport.)
