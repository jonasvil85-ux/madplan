# Dagsrapport 2026-11-20
**Siden i dag:** Sund (grøn). Kun nye tilbudsdata er udgivet; to ændringer blev afvist af kontrollanten.
## Ændret på siden (slået sammen)
- Nye tilbudsaviser uge 48 (meny, bilka, kvickly, spar, minkoebmand) og billeder til nye retter (9eac79c, dcaa466): automatisk data fra tilbudsrutinen, ikke en funktionsændring. Kontrol bestået (se Sundhed). Ingen UX- eller kodeændringer slået sammen i dag.
## Afvist eller rullet tilbage
- ai/2026-11-19-gode-tilbud-grupper (forsøg 2): "Vis færre" virker ikke, når en vare i gruppen er afkrydset. Ét forsøg tilbage.
- ai/2026-11-20-datafejl (forsøg 2): ny kødtype rammer også rent okse-/grisekød, så indkøbslisten kan vise hele avisens gruppetekst. Ét forsøg tilbage.
- Ingen tilbagerulning i dag. Øvrige ai/-grene er uændrede/parkerede.
## Data
- 572 retter: netto 64, meny 73, bilka 83, rema 50, kvickly 88, lidl 50, 365 50, spar 73, minkoebmand 41 (minimum er 40).
- Retter uden billede: 11 (alle 365; Frikadeller hos minkoebmand nævnes af kontrollanten som billedløs, men tælles ikke i mit tjek). 222 billeder bruges ikke (kan ryddes).
- Datakvalitet dårligere efter uge 48 (Ejeren): netto har 25 ingredienser uden type, 5 retter koster over 450 kr (andelår/and, 494–773 kr).
- Feedback fra brugerne: ingen nye beskeder; seneste (17/11) var 2 testbeskeder, ikke brugbare. Intet HASTER.
## Sundhed
- Kontrol: BESTÅET (0 fejl, 10 advarsler) inkl. regression, budget og sammenlign butikker. Udgivet side: nået, matcher main ja (Vagtpost GRØN 07:06 UTC, sw.js v6, 572 retter). Browser-QA GRØN: 0 JS-fejl, intet vandret scroll, 30 små tryk-flader (<40 px) på mobil. Advarsler af betydning: de 5 dyre retter, 25 netto uden type, 11 retter uden billede hos 365.
- Ikke tjekket af mig: udseende i en rigtig browser (jeg har ingen), sidefodens Chromium-test (Playwright mangler her), farvekontrast og tastaturbrug.
## I morgen
- Øverst: "Ret kendte datafejl" (DATA, H) – sidste forsøg; derefter "Ét kort: Hvor handler du?" (genindsendelse). Tages af Backend-udvikleren hhv. Frontend-udvikleren, efter Ejerens prioritering.
## Til prøve hos Jonas
- Intet.
## Til Jonas
- Intet nyt. Sikkerhedspunkter H2, L2/L3, M4/M5 afventer stadig Jonas (grundlov), jf. Ejerens rapport.
