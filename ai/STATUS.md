# Status for AI-holdet

HELBRED.md: GRØN (2026-11-16 06:41 UTC, begge domæner OK, main 45ed2ca). BROWSER.md: GRØN (2026-11-16, mob og desk, 0 JS-fejl, intet vandret scroll).

Sidst kontrolleret: 2026-11-16 ca. 10 UTC (kontrollant)
Main-status: BESTÅET (0 fejl, 9 advarsler), regressionstest bestået (main 8c2e4a7, efter sammenlægning af indkøbsliste-rækker).

## Afvist – udvikleren retter
- ai/2026-11-16-datafejl (4f2dd38, forsøg 1, klasse H): før/efter-tal mangler ugepris og indkøbslinjer for de 9 butikker (H-punkt 2); dagens H-plads var brugt (H-punkt 5); accept (1) kun delvist (16 ty-advarsler tilbage). Bygget korrekt (kun tidsstempel ændres ved genbygning).

## Parkeret – Ejeren har dem (to forsøg brugt)
- ai/2026-11-15-fravalg-budget (7ad8866, klasse H): fravalg lader stadig igennem: mayonnaise/remoulade under "Æg" (6 butikker), pesto under "Mælkeprodukter", "hakket kød 8-12%" (svin+kalv) under "Okse og kalv". Budgetdelen er i orden (8/9 under 600 kr) – foreslås bygget som egen gren.
- ai/2026-11-16-mobil-tryk-flader (cccb0f6, klasse A): forsiden 36 → 1 element under 40 px, men "Om Måltidsjagten" i sidefoden er 95 × 14 px, og accept (4) (madplan-hero.png 405 KB) er ikke gjort. Forslag: flyt (4) til eget H-krav. Erstatter ai/2026-11-15-mobil-tryk-flader.

## Rullet tilbage
(ingen)

## Seneste sammenlægninger
- 2026-11-16: ai/2026-11-15-indkoebsliste-raekker (H, 8c2e4a7): korte rækker med Detaljer-link. Skærpet validering bestået (linjer og summer uændrede i alle 9 butikker, rød-hold, revert-prøve).
- 2026-11-15: ai/2026-11-15-opskriftssider (H, 384f5d1): 193 opskriftssider, oversigt og sitemap. Skærpet validering bestået (før/efter byte-identisk for alle 9 butikker, rød-hold, revert-prøve).
- 2026-11-15: ai/2026-11-15-regressionstest (A, kun test): regression.py/.js + facit + frossen datakopi; kaldes af kontrol.py. Klasse H kan nu valideres efter den skærpede proces.
- 2026-11-15: ai/2026-11-15-kontrol-jsonld (A, kun test): kontrol.py springer JSON-LD-blokke over i JS-tjekket.

## Kendte begrænsninger
- Kontrollantens sky-session har lokal Chromium (Playwright via node) og kan måle en gren mod en lokal server; eksterne billeder (butikslogoer, tilbudsbilleder) blokeres dér.
- Skyen har ingen browser. Browser-QA (GitHub) måler og tager skærmbilleder af siden (`ai/BROWSER.md`, grenen `skaermbilleder`), men klikker kun et fast flow.
- Regressionstesten dækker ikke DOM/udseende, simByt, andre husstande end 2+2/2+0 eller live-data (se udviklerrapporten 2026-11-15).
- Brugerfeedback (Supabase) kan holdet ikke læse.
- Skyrutinerne kan ikke hente den udgivne side (netværkspolitikken afviser den). Vagtposten er derfor flyttet til GitHub-handlingen "Vagtpost", som skriver `ai/HELBRED.md`; rutinerne læser den fil.
- Skyrutinerne kan ikke slette grene på GitHub; Vagtposten rydder sammenlagte `ai/*`-grene.
