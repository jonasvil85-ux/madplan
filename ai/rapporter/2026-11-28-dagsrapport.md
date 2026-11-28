# Dagsrapport 2026-11-28
**Siden i dag:** Problem: main er RØD (kontrol.py FEJLET, 4 fejl) for andet døgn. Fire retter koster over 450 kr, og den udgivne side er grøn og identisk med main, så de vises stadig for brugerne.
## Ændret på siden (slået sammen)
- Nye tilbudsaviser: netto uge 49 (4380164, tilbudsrutinen, 05:14 UTC). Ingen kontrollant-sammenlægninger de sidste 24 timer. Intet andet udgivet.
## Afvist eller rullet tilbage
- ai/2026-11-28-dyre-retter (H, forsøg 2): afvist. Spar er rettet, men bilka viser stadig 4 biblioteksretter over 450 kr i "Vælg selv" (mix-133/134/135/172, 490–521 kr), fordi de er koblet til oksemørbrad B162. Kontrollen i går kaldte bilka "i orden" ved en fejl.
- ai/2026-11-28-ux (A, forsøg 2 på "Nye tilbud siden sidst"): afvist. "Se ugens forslag" fra trin 2–5 går til det låste trin 6 (tom side/login-væg).
- Ingen tilbagerulning (fejlen kommer fra data, ikke en sammenlægning). Se ai/rapporter/2026-11-28-kontrol.md.
## Data
- Antal retter pr. butik (retter.json på main): netto 50, meny 93, bilka 82, rema 56, kvickly 94, lidl 49, 365 50, spar 92, minkoebmand 77 (i alt 643).
- Retter uden billede: netto 31, 365 3 (billeder laves kun lokalt). 371 ubrugte billeder.
- Feedback fra brugerne: ingen nye beskeder siden 2026-11-25 (ai/FEEDBACK.md); ingen HASTER-punkter.
## Sundhed
- Kontrol (min egen kørsel på main): FEJLET (4 fejl, 6 advarsler). Udgivet side: nået (Vagtpost GRØN 07:57 UTC, begge domæner), matcher main ja (retter.json identisk). Browser-QA GRØN (0 JS-fejl, intet vandret scroll; 30 små tryk-flader på mobil).
- Advarsler af betydning: rema og lidl har 18 tilbudsingredienser uden typeoplysning (indkøbslisten kan vise hele tilbudsgruppen). Sidefodens Chromium-test er IKKE kørt (Playwright mangler i skyen).
- Ikke tjekket af mig: udseende i browser, selve den udgivne side.
## I morgen
- Øverste punkt i backloggen: HASTER [DATA][H] fjern/ret de fire dyre retter, inkl. bilkas biblioteksretter. Ejeren skal omformulere kravet (rettelsen ligger i biblioteksopskrifterne); derefter backend-udvikleren.
## Til prøve hos Jonas
- Intet.
## Til Jonas
- Uændret afventende forslag til grundloven fra Ejeren: tilbudsrutinen skal køre `byg_retter.py` og `kontrol.py` før commit (RUTINE.md). Main er rød af samme årsag som 2026-11-20.
