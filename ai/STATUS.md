# Status for AI-holdet

**HELBRED.md findes ikke endnu** (Vagtpost-handlingen er ny og har ikke skrevet den); den udgivne side er ikke tjekket 2026-11-15 kl. 09.

Sidst kontrolleret: 2026-11-15 kl. 09 (kontrollant)
Main-status: BESTÅET (0 fejl, 9 advarsler) og REGRESSION: BESTÅET efter sammenlægning af ai/2026-11-15-regressionstest.

## Afvist – UX-udvikleren retter
(ingen)

## Rullet tilbage
(ingen)

## Seneste sammenlægninger
- 2026-11-15: ai/2026-11-15-regressionstest (A, kun test): regression.py/.js + facit + frossen datakopi; kaldes af kontrol.py. Klasse H kan nu valideres efter den skærpede proces.
- 2026-11-15: ai/2026-11-15-kontrol-jsonld (A, kun test): kontrol.py springer JSON-LD-blokke over i JS-tjekket.

## Kendte begrænsninger
- Skyen har ingen browser: udseende er vurderet ud fra koden og designfilen.
- Regressionstesten dækker ikke DOM/udseende, simByt, andre husstande end 2+2/2+0 eller live-data (se udviklerrapporten 2026-11-15).
- Brugerfeedback (Supabase) kan holdet ikke læse.
- Skyrutinerne kan ikke hente den udgivne side (netværkspolitikken afviser den). Vagtposten er derfor flyttet til GitHub-handlingen "Vagtpost", som skriver `ai/HELBRED.md`; rutinerne læser den fil.
- Skyrutinerne kan ikke slette grene på GitHub; Vagtposten rydder sammenlagte `ai/*`-grene.
