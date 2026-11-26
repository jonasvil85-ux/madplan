# Dagsrapport 2026-11-26
**Siden i dag:** Sund. Vagtpost og Browser-QA er GRØNNE, og kontrol.py består (0 fejl, 5 advarsler).
## Ændret på siden (slået sammen)
- Søgning i "Vælg selv": ental og flertal giver nu samme træffere (kartoffel/kartofler, gulerod/gulerødder m.fl.), og der vises kun én "Din uge"-overskrift (c63c07c, klasse A, forsøg 3). Kontrollanten slog den sammen efter kontrol.py, regression, søgetest i Chromium og eget rød-hold; priser og indkøbsliste er uændrede (før/efter for 9 butikker identisk).
- Nye tilbudsaviser: 365 (uge 48), netto og lidl (fcf50e7, tilbudsrutinen).
## Afvist eller rullet tilbage
- ai/2026-11-26-monotoni ("Mål om ugeforslaget bliver dyrere", klasse A): afvist, forsøg 1 af 3. Målingen er upålidelig: de konstruerede retter genbruger samme id, så resultatet afhænger af rækkefølgen, og den "billige" ret er ikke billigere i ugeprisen. Det påståede fund (netto +26,75 kr) er derfor en målefejl, ikke en fejl på siden. Ingen tilbagerulning.
## Data
- Retter pr. butik: netto 60, meny 73, bilka 80, rema 56, kvickly 88, lidl 49, 365 50, spar 71, minkoebmand 40. Retter uden billede: 29, alle 365 (nye fra uge 48; kræver lokal billeder.py). 341 billeder bruges ikke (advarsel).
- Feedback fra brugerne: ingen nye beskeder siden 2026-11-25 (ai/FEEDBACK.md; den ene besked fra 25/11 om porre vurderet uklar). Ingen HASTER-punkter.
## Sundhed
- Kontrol: RESULTAT: BESTÅET (0 fejl, 5 advarsler), kørt af mig i dag. Udgivet side: nået, retter.json matcher main (HELBRED GRØN 06:57 UTC på a6c4d99; senere commits på main er rapporter, ikke tjekket af mig om de rører siden).
- Browser-QA GRØN (0 JS-fejl, intet vandret scroll). Tryk-flader under 40 px: 30 (mobil) og 31 (desktop), ikke rettet endnu.
- Advarsler: rema og lidl har 18 tilbudsingredienser uden typeoplysning (ty); 29 retter uden billede; sidefodens Chromium-test kunne ikke køres her (ingen Playwright).
## I morgen
- Øverst: rette målingen i ai/2026-11-26-monotoni (unikt id, reelt billigere ret). Tager Backend-udvikleren (forsøg 2).
## Til prøve hos Jonas
- Søgning i "Vælg selv": skriv fx "kartofler" og så "kartoffel" – giver begge ord de retter, du forventer? Er der kun én "Din uge"-overskrift? Virker det bedre end før? Er noget forvirrende? (Det er nu udgivet; porre-spørgsmålet fra en bruger kan også prøves: søg "porre".)
## Til Jonas
- Intet nyt. Uændret afventende: sikkerhedspunkterne og forslaget om, at tilbudsrutinen kører byg_retter.py og kontrol.py før commit (se tidligere rapporter).
- Ikke tjekket af mig: udseende i browser, skærmbilleder, mørkt tema, om søgningen virker på den live side.
