# Status for AI-holdet

HELBRED.md: GRØN (2026-11-15 09:12 UTC, begge domæner OK, main d52a40a).

Sidst kontrolleret: 2026-11-15 ca. 09:15 UTC (kontrollant, anden kørsel)
Main-status: BESTÅET (0 fejl, 9 advarsler), regressionstest bestået (main 039205b).

## Afvist – UX-udvikleren retter
- ai/2026-11-15-opskriftssider (forsøg 1, 2026-11-15): klasse H (`scripts/byg_*.py`). Alt andet er grønt, men rapporten mangler før/efter-tal for de 9 butikker (H-punkt 2). Se ai/rapporter/2026-11-15-kontrol.md.

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
