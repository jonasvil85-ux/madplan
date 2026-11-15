# Udviklerrapport 2026-11-15 – indkøbslistens rækker (bygget af Claude i chatten på Jonas' bestilling)

**Hvad:** Rækkerne under "På tilbud i …" på indkøbslisten viser nu produktets navn, én kort linje (mængde og den første ret, fx "500 g · Til Frikadeller af gris og kalv med kartoffelmos og 2 retter mere") og et lille "Detaljer"-link, der folder den fulde tekst ud (avisens egen tekst, stykpris, samlet behov og alle retter). Før stod alt som en lang grå blok under hver vare.

**Hvorfor:** ROADMAP 5 (højeste prioritet, 12,0). Rækken skal kunne skimmes i butikken. Tidligere stod fx "Avisen: MADVÆRKET Julemedister eller hakket grise- og kalvekød · 500 g · Til: 500 g hakket grise- og kalvekød (Frikadeller af gris og kalv med kartoffelmos)" under hver vare.

**Klasse:** A (kun visning af tekst; listens linjer, varenavne, mængder, priser og summer er uændrede, se tabel).

**Filer:** `index.html` (`listeLinjer`, `renderListe`, CSS), denne rapport.

**Accept:** (1) rækkens detalje er kort: gennemsnit 37 → 25 tegn, længste 226 → 120 tegn, rækker over 100 tegn 8 → 2 (målt på `.liste-vare .detalje`, mobil 390 px). (2) Intet går tabt: den fulde tekst er uændret i "Detaljer". (3) Et tryk på "Detaljer" folder ud uden at krydse varen af eller på (testet: afkrydsningen er uændret, `details.open` er sand); et tryk på varens navn krydser stadig af. (4) Listens indhold er uændret.

**Før/efter-tal for alle 9 butikker (sidens `listeLinjer()` og `prisSum()`; ugeforslagets retter, 2 voksne + 2 børn):** identiske før og efter i alle 9 butikker:

| Butik | På tilbud (linjer) | Øvrige | Basisvarer | Sum for listen (kr) | Ugepris |
|---|---|---|---|---|---|
| 365discount | 12 | 11 | 12 | 707 | 514 |
| Netto | 11 | 9 | 19 | 780 | 464 |
| MENY | 7 | 14 | 15 | 865 | 658 |
| Bilka | 7 | 16 | 13 | 767 | 565 |
| REMA 1000 | 10 | 14 | 14 | 792 | 583 |
| Kvickly | 8 | 16 | 10 | 656 | 522 |
| Lidl | 13 | 11 | 16 | 637 | 421 |
| SPAR | 8 | 18 | 14 | 825 | 608 |
| Min Købmand | 7 | 14 | 13 | 785 | 595 |


**Test:** `kontrol.py` lokalt: `RESULTAT: BESTÅET`. Regressionstesten kunne ikke køres lokalt (ingen node); den dækker listens linjer og skal køres af kontrolløren. Set i headless Edge på 390 px: rækkerne, "Detaljer" udfoldet og krydsning af.

**Dækker IKKE:** indkøbsseddel-trinnet (uændret), "Øvrige"- og "Basis"-rækkerne (de har allerede korte tekster, men viser stadig alle retter), skærmlæser (details/summary er native), rigtig telefon; siden bliver ca. 134 px længere (8.277 → 8.411 px) på grund af "Detaljer"-linkene.

**Kontrolløren bør kigge på:** at diffen kun rører `listeLinjer`/`renderListe` og CSS, at `regression.py` er uændret, et skærmbillede af listen fra Browser-QA.

**Næste skridt:** (1) Gruppér listen efter butiksafdeling (frugt og grønt, kød, mejeri) i stedet for kun tilbud/øvrige/basis. (2) Vis den foreslåede mængde i hele pakker ("1 pakke à 500 g"). (3) Retter-listen: søgning og "vis flere" (ROADMAP 6).
