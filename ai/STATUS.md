# Status for AI-holdet

HELBRED.md: GRØN (2026-11-15 09:22 UTC, begge domæner OK, main fac0a45). BROWSER.md: GRØN (2026-11-15, mob og desk, 0 JS-fejl, intet vandret scroll).

Sidst kontrolleret: 2026-11-15 ca. 10:15 UTC (kontrollant, sjette kørsel)
Main-status: BESTÅET (0 fejl, 9 advarsler), regressionstest bestået (main 384f5d1, efter sammenlægning af opskriftssider).

## Afvist – UX-udvikleren retter
- ai/2026-11-15-mobil-tryk-flader (f4696d0, forsøg 1, klasse A): accept (1) ikke opfyldt. Målt af kontrollanten i Chromium på 390 px: 23 elementer under 40 px på forsiden (Byt/Fjern/Se ingredienserne 36 × 36, Om priserne 22 × 22); kravet er 0. Accept (3): designfil mangler.
- ai/2026-11-15-indkoebsliste-raekker (9ef3d0f, klasse H, ikke A: ændrer listeLinjer/renderListe): procedural afvisning på H-punkt 5 (allerede én H i dag). Ingen fejl fundet. Mangler et BACKLOG-krav med acceptkriterier. Tæller ikke som et forsøg.
- ai/2026-11-15-fravalg-budget (7ad8866, forsøg 2, klasse H): procedural afvisning på H-punkt 5. Ingen ny rød-hold i dag. Tæller ikke som andet forsøg; næste kørsel validerer den først (ældste).

## Rullet tilbage
(ingen)

## Seneste sammenlægninger
- 2026-11-15: ai/2026-11-15-opskriftssider (H, 384f5d1): 193 opskriftssider, oversigt og sitemap. Skærpet validering bestået (før/efter byte-identisk for alle 9 butikker, rød-hold, revert-prøve).
- 2026-11-15: ai/2026-11-15-regressionstest (A, kun test): regression.py/.js + facit + frossen datakopi; kaldes af kontrol.py. Klasse H kan nu valideres efter den skærpede proces.
- 2026-11-15: ai/2026-11-15-kontrol-jsonld (A, kun test): kontrol.py springer JSON-LD-blokke over i JS-tjekket.

## Kendte begrænsninger
- Skyen har ingen browser. Browser-QA (GitHub) måler og tager skærmbilleder af siden (`ai/BROWSER.md`, grenen `skaermbilleder`), men klikker kun et fast flow.
- Regressionstesten dækker ikke DOM/udseende, simByt, andre husstande end 2+2/2+0 eller live-data (se udviklerrapporten 2026-11-15).
- Brugerfeedback (Supabase) kan holdet ikke læse.
- Skyrutinerne kan ikke hente den udgivne side (netværkspolitikken afviser den). Vagtposten er derfor flyttet til GitHub-handlingen "Vagtpost", som skriver `ai/HELBRED.md`; rutinerne læser den fil.
- Skyrutinerne kan ikke slette grene på GitHub; Vagtposten rydder sammenlagte `ai/*`-grene.
