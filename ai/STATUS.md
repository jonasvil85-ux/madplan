# Status for AI-holdet

Sidst kontrolleret: 2026-11-15 (kontrollant)
Main-status: BESTÅET (0 fejl, 9 advarsler) efter sammenlægning af ai/2026-11-15-kontrol-jsonld. Før var den rød af en falsk JSON-LD-fejl i kontrol.py. Udgivet side ikke tjekket (proxy blokerer madplan-blue.vercel.app).

## Afvist – UX-udvikleren retter
(ingen)

## Rullet tilbage
(ingen)

## Seneste sammenlægninger
- 2026-11-15: ai/2026-11-15-kontrol-jsonld (A, kun test): kontrol.py springer JSON-LD-blokke over i JS-tjekket.

## Kendte begrænsninger
- Skyen har ingen browser: udseende er vurderet ud fra koden og designfilen.
- Regressionstest af pris, indkøbsliste og ugeforslag findes ikke endnu: ingen klasse H-ændring kan slås sammen, før den er bygget.
- Brugerfeedback (Supabase) kan holdet ikke læse.
- Kontrollantens skyrutine kan ikke hente den udgivne side (madplan-blue.vercel.app afvises af netværkspolitikken). Vagtpostens sammenligning af side og main kan derfor ikke laves, før domænet tillades.
