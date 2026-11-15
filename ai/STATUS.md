# Status for AI-holdet

HELBRED.md: GRØN (2026-11-15 09:22 UTC, begge domæner OK, main fac0a45). BROWSER.md: GRØN (2026-11-15, mob og desk, 0 JS-fejl, intet vandret scroll).

Sidst kontrolleret: 2026-11-15 ca. 09:45 UTC (kontrollant, femte kørsel)
Main-status: BESTÅET (0 fejl, 9 advarsler), regressionstest bestået (main 1508f73).

## Afvist – UX-udvikleren retter
- ai/2026-11-15-fravalg-budget (1035a27, forsøg 1, klasse H): rød-hold fandt brud på fravalgets accept (2). "Kød og fisk" giver Lammegryde (lammekød) hos Lidl, "Mælkeprodukter" slipper mozzarella/feta/Grana Padano igennem i 8 af 9 butikker, og "Løg" slipper porre igennem. Testen tjekker kun svin med en delmængde af koden egen regex. Budgetdelen er ok (8/9 ved 600 kr, aldrig dyrere). Se ai/rapporter/2026-11-15-kontrol.md, femte kørsel.

## Parkeret – tilbage hos Ejeren
- ai/2026-11-15-opskriftssider (552202c): afvist to gange på H-punkt 2. Forsøg 2 tilføjede ugepris og antal retter, men ikke indkøbslistens linjer. Kontrollanten har selv genskabt alle tal (uændrede, hele regression-output identisk), og alle andre H-punkter er grønne (kontrol, konflikt-fri sammenlægning, rød-hold, revert). Ejeren beslutter. Se ai/rapporter/2026-11-15-kontrol.md (fjerde kørsel).
  Opdatering, femte kørsel: forsøg 3 (9360d24) tilføjer indkøbslistens linjer, og tallene passer med kontrollantens egne. Den sidste mangel er dermed lukket. Ejeren kan fjerne parkeringen, så næste kontrolkørsel slår grenen sammen efter en ny validering.

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
