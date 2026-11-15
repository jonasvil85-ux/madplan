# Status for AI-holdet

HELBRED.md: GRØN (2026-11-15 09:22 UTC, begge domæner OK, main fac0a45). BROWSER.md: GRØN (2026-11-15, mob og desk, 0 JS-fejl, intet vandret scroll).

Sidst kontrolleret: 2026-11-15 ca. 09:30 UTC (kontrollant, fjerde kørsel)
Main-status: BESTÅET (0 fejl, 9 advarsler), regressionstest bestået (main bc8033e).

## Afvist – UX-udvikleren retter
(ingen)

## Parkeret – tilbage hos Ejeren
- ai/2026-11-15-opskriftssider (552202c): afvist to gange på H-punkt 2. Forsøg 2 tilføjede ugepris og antal retter, men ikke indkøbslistens linjer. Kontrollanten har selv genskabt alle tal (uændrede, hele regression-output identisk), og alle andre H-punkter er grønne (kontrol, konflikt-fri sammenlægning, rød-hold, revert). Ejeren beslutter. Se ai/rapporter/2026-11-15-kontrol.md (fjerde kørsel).

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
