# Ændring af arbejdsreglerne (GODKENDT af Jonas 2026-11-16, indført i ai/agenter/kontrollant.md)

Jonas' betingelser: (1) op til tre H om dagen, kun uafhængige, hver kan rulles tilbage separat og testes individuelt, regression efter hver; (2) procedurefejl tæller ikke som forsøg, men manglen skal rettes før godkendelse; (3) tre forsøg, men hvert nyt forsøg skal være en reel forbedring baseret på kontrollantens feedback.

## Hvad der er sket de første to dage
- 9 grene bygget. 3 slået sammen (regressionstest, opskriftssider, indkøbsliste-rækker).
- 5 afvisninger var **procedurale** og ikke fejl: "højst én H pr. dag" eller "før/efter-tal mangler en kolonne". To gode grene (fravalg-budget, mobil) blev **parkeret**, fordi de brugte deres to forsøg, delvist på procedure.
- Rød-hold fandt **rigtige** fejl hver gang (lammekød, ost, porre, parmigiano, mayonnaise, pesto). Den del virker og skal bevares.

## Forslag
| # | I dag | Forslag | Konsekvens |
|---|---|---|---|
| 1 | Højst én H-sammenlægning om dagen | Højst **tre** H om dagen, hvis de rører forskellige områder, og regressionstesten køres igen på main efter hver sammenlægning, før den næste | Hurtigere levering. Risiko: flere ændringer samme dag gør det sværere at finde årsagen til en fejl; afbødes af tilbagerulning pr. sammenlægning og vagtposten |
| 2 | En procedural afvisning (H-plads optaget) tæller ikke, men en manglende tabelkolonne tæller som forsøg | Kun **indholdsfejl** (rød-hold, fejlende test, brudt acceptkriterium) tæller som forsøg; mangler i rapporten sendes tilbage uden at tælle | Færre parkerede gode grene. Risiko: ingen |
| 3 | To forsøg, så parkeres opgaven | **Tre** forsøg | Lidt længere tid på en dårlig gren. Risiko: lav |
| 4 | Før/efter-tal skrives i hånden i rapporten | Et script (`scripts/tests/foer_efter.py`) laver tabellen for alle 9 butikker automatisk, og kontrollanten kører det selv | Fjerner den mest almindelige procedurale afvisning |

Forslag 4 er et testværktøj (klasse A) og kan bygges uden ændring af grundloven. Forslag 1–3 ændrer `ai/agenter/kontrollant.md` og kræver Jonas' ja.
