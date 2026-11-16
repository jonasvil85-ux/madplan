# Status for AI-holdet

HELBRED.md: GRØN (2026-11-16 11:40 UTC, begge domæner OK, main 25d3cb7). BROWSER.md: GRØN (2026-11-16, mob og desk, 0 JS-fejl, intet vandret scroll).

Sidst kontrolleret: 2026-11-16 ca. 12:00 UTC (kontrollant, fjerde kørsel)
Main-status: BESTÅET (0 fejl, 10 advarsler), regressionstest bestået (main f1c3024). Budget slået sammen (H nr. 3 i dag – dagens H-pladser er brugt).

## Afvist – udvikleren retter
- ai/2026-11-16-datafejl (4f2dd38, forsøg 1, klasse H; uændret ved fjerde kørsel – afvist igen, tæller ikke): før/efter-tal mangler ugepris og indkøbslinjer for de 9 butikker (H-punkt 2); dagens H-plads var brugt (H-punkt 5); accept (1) kun delvist (16 ty-advarsler tilbage). Bygget korrekt (kun tidsstempel ændres ved genbygning).

## Parkeret – Ejeren har dem (to forsøg brugt)
- ai/2026-11-15-fravalg-budget (7ad8866, klasse H): fravalg lader stadig igennem: mayonnaise/remoulade under "Æg" (6 butikker), pesto under "Mælkeprodukter", "hakket kød 8-12%" (svin+kalv) under "Okse og kalv". Budgetdelen er i orden (8/9 under 600 kr) – foreslås bygget som egen gren.
- ai/2026-11-16-mobil-tryk-flader (cccb0f6, klasse A): forsiden 36 → 1 element under 40 px, men "Om Måltidsjagten" i sidefoden er 95 × 14 px, og accept (4) (madplan-hero.png 405 KB) er ikke gjort. Forslag: flyt (4) til eget H-krav. Erstatter ai/2026-11-15-mobil-tryk-flader.

## Rullet tilbage
(ingen)

## Seneste sammenlægninger
- 2026-11-16: ai/2026-11-16-budget (H, f1c3024, forsøg 3): budget for ugens aftensmad i Dine valg. Skærpet validering bestået (før/efter identisk uden budget for 9 butikker × 3 husstande, 7/9 under 600 kr, 5 rød-hold-forsøg, revert-prøve). Dagens 3. H. Opfølgning: "600 kr – 1 kr over 600 kr"-beskeden, afvigelse fra designfilens chips, "højt budget ændrer intet" gælder kun én butik.
- 2026-11-16: ai/2026-11-16-sammenlign-butikker (H, 25d3cb7, forsøg 2): rangeret liste over 9 butikker og ærligt to-butiks-forslag. Skærpet validering bestået (før/efter byte-identisk for 9 butikker × 3 husstande, 6 rød-hold-forsøg, revert-prøve). Dagens 2. H.
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
