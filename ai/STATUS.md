# Status for AI-holdet

HELBRED.md: GRØN (2026-11-15 09:22 UTC, begge domæner OK, main fac0a45). BROWSER.md: GRØN (2026-11-15, mob og desk, 0 JS-fejl, intet vandret scroll).

Sidst kontrolleret: 2026-11-15 ca. 09:45 UTC (kontrollant, femte kørsel)
Main-status: BESTÅET (0 fejl, 9 advarsler), regressionstest bestået (main 1508f73).

## Afvist – UX-udvikleren retter
- ai/2026-11-15-fravalg-budget (1035a27, forsøg 1, klasse H): rød-hold fandt brud på fravalgets accept (2). "Kød og fisk" giver Lammegryde (lammekød) hos Lidl, "Mælkeprodukter" slipper mozzarella/feta/Grana Padano igennem i 8 af 9 butikker, og "Løg" slipper porre igennem. Testen tjekker kun svin med en delmængde af kodens egen regex. Budgetdelen er ok (8/9 ved 600 kr, aldrig dyrere). Se ai/rapporter/2026-11-15-kontrol.md, femte kørsel.

## Klar til sammenlægning – afparkeret 2026-11-15 (Ejer/CTO)
- ai/2026-11-15-opskriftssider (9360d24): H-punkt 2 er lukket i forsøg 3 (indkøbslistens linjer passer med kontrollantens egne tal). Afparkeret: næste kontrolkørsel slår den sammen efter ny kørsel af kontrol, regression og revert-prøve.

## Rullet tilbage
(ingen)

## Seneste sammenlægninger
- 2026-11-15: ai/2026-11-15-regressionstest (A, kun test): regression.py/.js + facit + frossen datakopi; kaldes af kontrol.py. Klasse H kan nu valideres efter den skærpede proces.
- 2026-11-15: ai/2026-11-15-kontrol-jsonld (A, kun test): kontrol.py springer JSON-LD-blokke over i JS-tjekket.

## Kendte begrænsninger
- Skyen har ingen browser. Browser-QA (GitHub) måler og tager skærmbilleder af siden (`ai/BROWSER.md`, grenen `skaermbilleder`), men klikker kun et fast flow.
- Regressionstesten dækker ikke DOM/udseende, simByt, andre husstande end 2+2/2+0 eller live-data (se udviklerrapporten 2026-11-15).
- Brugerfeedback (Supabase) kan holdet ikke læse.
- Skyrutinerne kan ikke hente den udgivne side (netværkspolitikken afviser den). Vagtposten er derfor flyttet til GitHub-handlingen "Vagtpost", som skriver `ai/HELBRED.md`; rutinerne læser den fil.
- Skyrutinerne kan ikke slette grene på GitHub; Vagtposten rydder sammenlagte `ai/*`-grene.
