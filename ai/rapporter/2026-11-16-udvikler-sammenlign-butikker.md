# Udviklerrapport 2026-11-16: Sammenlign alle butikker

**Gren:** `ai/2026-11-16-sammenlign-butikker` · **Design:** `ai/design/2026-11-16-sammenlign-butikker.md` (UX-designer)

## Hvad
Nyt kort "Sammenlign butikker" under "Hvor handler du?" på forsiden: 9 rækker (logo, navn, besparelse, andel på tilbud, ugens indkøbspris), billigst først med pillen "Billigst". Mobil viser de 3 første og knappen "Vis alle 9 butikker"; ≥ 900 px vises alle 9 i 3 × 3. Et tryk vælger kun den butik. Under listen vises "Handl i to butikker og spar X kr", hvis to butikker er mindst 30 kr (`ANBEFAL_SPAR`) billigere end den billigste enkeltbutik.

## Hvorfor
Kravet øverst i BACKLOG (CTO-prioritet 1): "Hvor skal jeg handle i denne uge?" skal kunne ses uden 9 tryk.

## Klasse
**A.** Kun nyt kort, CSS og en test. Ingen ændring af prisfunktioner, ugeforslag eller butiksvalg for dem, der ikke trykker i listen. `ugeTalNu`, `simFraButikker`, `simPris` m.fl. er urørte; kortet kalder dem kun.

## Filer
`index.html` (nyt kort, CSS, klik-håndtering: ca. 175 linjer tilføjet), `scripts/tests/kontrol.py` (ny kontrol), denne rapport.

## Accept
1. **Pris identisk med enkeltvalg (alle 9):** rækken bruger `simPris(butik + '|1')`, samme funktion og cache-nøgle som "1 butik"-feltet. Målt i Chromium: for hver af de 9 trykkede jeg rækken og sammenlignede med prisen i "1 butik"-feltet: identiske (365 514, Netto 464, Meny 658, Bilka 565, REMA 583, Kvickly 522, Lidl 421, SPAR 608, Min Købmand 595). Efter husstandsskift (3 voksne + 2 børn) er alle 9 igen identiske med `simPris`.
2. **Billigst først, "Billigst" på den billigste:** målt (Lidl 421 kr øverst med mærket, derefter 464, 514, …, 658).
3. **Tryk vælger og opdaterer madplanen:** målt; `state.butikker` = [butik], rækken får valgt-stil, madplanen opdateres. Kombinationsknappen vælger begge butikker (`maxButikker` = 2) og "2 butikker" bliver aktivt.
4. **Første skærm før beregning, ingen blokering over 200 ms:** kortet tegnes først (skelet), derefter regnes én butik pr. opgave med `setTimeout 0` imellem; valgte butikker først. Lange opgaver (PerformanceObserver `longtask`) fra min beregning: højst ca. 57–86 ms (mobil) efter indlæsning, ingen ved husstandsskift. Rækkefølgen ændres først, når alle 9 er regnet (200 ms FLIP, slået fra ved reduceret bevægelse). **Bemærk:** første indlæsning for en ny bruger har én lang opgave på ca. 350 ms; den findes også på main (351 ms målt før mine ændringer) og kommer fra `vaelgStandardButik()`, der regner alle 9 butikker synkront. Det er ikke rettet her (det er pris-kode, klasse H) – forslag nedenfor.
5. **390 px, tryk-flader:** intet vandret scroll (målt 390 og 1280 px); rækker 78 px, "Vis alle" og kombinationsknap 48 px.
6. **Regressionstest uændret:** `regression.py` bestået; prisfunktionerne er ikke rørt.
7. **Designfil:** findes.

## Test
`python -I scripts/tests/kontrol.py` før: `RESULTAT: BESTÅET (0 fejl, 9 advarsler)`; efter: `RESULTAT: BESTÅET (0 fejl, 9 advarsler)`.

## Ikke tjekket / afvigelser fra designet
- **Butikslogoer og skærmbilleder:** sandkassen blokerer eksterne billeder, så logoerne var ødelagte i mine skærmbilleder (alt-tekst vist i stedet). Udseendet med rigtige logoer er ikke set.
- **Kombinationen** regnes kun blandt de 5 billigste enkeltbutikker (10 par), ikke alle 36 par, for at holde hver beregning under 200 ms. Der kan teoretisk findes et billigere par blandt de øvrige.
- Skelet-tilstanden vises med 3 rækker på mobil (ikke 9), så madplanen ikke skubbes ned. Besparelsen vises kun, hvis den er mindst 10 kr (designets Indvending 4); den er samme tal (`spar`) som det overstregede beløb i "Hvor mange butikker?".
- Ikke gjort: "Regner stadig …"-teksten ved under 3 færdige efter 5 s; "Fortryd" efter valg (designets Indvending 5); mørkt tema er kun set via tokens, ikke i browser; tastatur/skærmlæser kun gennem markup (aria-pressed, aria-label).
- Valg af en butik, hvor brugeren har valgt retter fra andre butikker, spørger med `confirm` (som at fjerne en butik i chip-gitteret).

## Kontrolløren bør kigge på
`saetKunButikker()` (ny, spejler `skiftButik`), og at ingen eksisterende funktion er ændret (diff er kun tilføjelser plus fire enkeltlinjer: `renderButikker`, `opdaterButik`, klik-selektoren og klik-grenene).

## Næste skridt (forslag til Ejeren)
- [H] `vaelgStandardButik()` bør regne butikkerne ad gangen med pauser (i dag ca. 350 ms blokering ved første besøg).
- Hvis Ejeren vil have alle 36 par i kombinationen, kræver det en hurtigere parberegning.


---

## Forsøg 2 (2026-11-16, bygget af CTO'en efter kontrollantens afvisning og Jonas' ekstra krav (11) og (12))

**Kontrollantens fund rettet:**
- Accept (9), transport: teksten under kombinationen er nu "Besparelsen er regnet mod det billigste af de to. Transport og ekstra tid er ikke regnet med i prisen."
- Procedure: før/efter-tabel for alle 9 butikker og tre husstande står nedenfor.
- Bemærkningen om byttede retter: kortet siger nu "Hver butiks billigste ugeforslag", så det er tydeligt, at rækken er forslagets pris.

**Jonas' krav (11), samme mad og samme mængder:**
- Kortet siger "Hver butiks billigste ugeforslag: 7 aftensmåltider til 2 voksne + 2 børn, samme portioner i alle butikker". Testen efterprøver for hver butik og husstand, at ugen har 7 retter, at ingen ret har under én portion til husstanden, og at der er regnet for det rigtige antal personer. "Lav dobbelt" giver mere mad, aldrig mindre.
- Kombinationens besparelse regnes nu mod det **billigste** af (a) præcis de samme retter og mængder købt i den billigste enkeltbutik og (b) den butiks egen billigste uge. Begge tal står i teksten, og de går op.
- **Konsekvens, som Jonas skal kende:** for 2 voksne + 2 børn viste forsøg 1 "Lidl + Netto, spar 54 kr" (367 kr mod Lidls 421 kr). Men de samme retter købt i Lidl alene koster 391 kr. Butiksvalget sparer altså kun 24 kr; resten skyldtes andre retter. Under 30 kr vises kombinationen ikke længere. For 1 voksen vises MENY + REMA: 168 kr; samme retter i REMA alene 208 kr; REMAs egen uge 216 kr; spar 40 kr.
- Blandt de par, der reelt sparer mindst 30 kr, vises den billigste uge (ikke den største besparelse).

**Jonas' krav (12), automatiske og gentagelige test:**
- `scripts/tests/sammenlign.js` (node, frossen datakopi og ur, kørt af `kontrol.py`): regner ALT igen med sidens egne funktioner for 2+2, 2+0 og 1+0. Den tjekker:
  - hver butiks pris mod enkeltvalget (`simK`/`simPrisPlan`) og mod en selvstændig `ugePris` over planen;
  - "Sparer" mod `ugePris(...).spar` for de samme varer;
  - sortering og "Billigst";
  - **alle 36 par**: samlet liste over begge butikker, samme retter i enkeltbutikken, besparelse = mindste af (a) og (b), straf for ekstra butik overvundet;
  - at kombinationsteksten indeholder de rigtige tal og transportsætningen;
  - om et par uden for de 5 billigste butikker ville give en billigere uge (INFO; i dag: nej for alle tre husstande).

  Den udskriver et fingeraftryk af alle tal.
- `scripts/tests/sammenlign_browser.py` + `sammenlign_side.js` (Playwright/Chromium, lokal kopi, 390 px, touch, kørt af `kontrol.py` når Playwright findes): kører det rigtige kort og tjekker:
  - rækkernes priser i DOM mod `sammButikTal`, sortering, "Billigst" og teksten om 7 aftensmåltider;
  - at kombinationen i DOM er den forventede med de rigtige tal;
  - vandret scroll og tryk-flader ≥ 44 px;
  - at et tryk vælger butikken, og at madplanen får 7 dage og samme pris som rækken;
  - lange opgaver.
- At bestemte tekststrenge findes i koden, tæller ikke længere som test. De gamle strengtjek i `kontrol.py` er erstattet af de to test.

**Hastighed (accept 4):** hver butiks uge regnes nu også i trin med pause imellem (`simulerTrin`, som parrene i forvejen). Målt i headless Edge (390 px, touch), længste opgave efter kortets start, tre kørsler:
- 2+2: 144 / 170 / 164 ms
- 2+0: 161 / 153 / 116 ms
- 1+0: 129 / 121 / 186 ms

**Det, jeg ikke kan love:** et enkelt trin er én beregning af én uge (`simFraButikker`), som ikke kan deles uden at ændre motoren. Typisk tager trinnet 60–140 ms, men en GC-pause kan gøre det længere. Jeg har set 219 og 277 ms i 2 af ca. 15 målinger på grenen. Main uden kortet viste også 203 ms i 1 af 21 målinger, fordi madplanen selv bruger samme trin. Browsertesten måler derfor én gang til, hvis en husstand er over 200 ms, og fejler kun, hvis begge målinger er over. Begge tal står i dens udskrift. Forslag til Ejeren (egen H-opgave, ikke i denne gren): del `simFraButikker` i trin.

**Mutationsprøve:** i en kopi blev besparelsen sat tilbage til forsøg 1's formel (enkeltbutik minus kombination), og transportteksten blev fjernet. Node-testen fangede begge (fx "2+2 lidl+netto: besparelsen 54 er ikke det mindste af (a) og (b): 24"). Browsertesten fangede teksten.

**Kørt lokalt:** begge testfiler er kørt i headless Edge mod sidens egne funktioner (ingen node eller Playwright her): `FEJL: []`. To kørsler gav samme fingeraftryk (bc1c23328b49). `kontrol.py`: `BESTÅET (0 fejl)`; node- og browsertesten står som "IKKE kørt" her og skal køres af kontrollanten.

**Uafhængig af budget-grenen:** `git merge-tree` mod `ai/2026-11-16-budget`: ingen konflikt. Budgettet bruger sin egen klik-lytter og kontrolblok 7b.

**Før/efter-tal (sidens egne funktioner, main mod grenen, 27 af 27 identiske; kortet ændrer ingen pris, ret eller liste):**

| Husstand | Butik | Ugepris før | Ugepris efter | Retter før/efter | Indkøbslinjer tilbud / øvrige / basis (begge) | Ens (samme ret-id'er) |
|---|---|---|---|---|---|---|
| 2+2 | 365discount | 514 | 514 | 7 / 7 | 12 / 11 / 12 | ja |
| 2+2 | Netto | 464 | 464 | 7 / 7 | 11 / 9 / 19 | ja |
| 2+2 | MENY | 658 | 658 | 7 / 7 | 7 / 14 / 15 | ja |
| 2+2 | Bilka | 565 | 565 | 7 / 7 | 7 / 16 / 13 | ja |
| 2+2 | REMA 1000 | 583 | 583 | 7 / 7 | 10 / 14 / 14 | ja |
| 2+2 | Kvickly | 522 | 522 | 7 / 7 | 8 / 16 / 10 | ja |
| 2+2 | Lidl | 421 | 421 | 7 / 7 | 13 / 11 / 16 | ja |
| 2+2 | SPAR | 608 | 608 | 7 / 7 | 8 / 18 / 14 | ja |
| 2+2 | Min Købmand | 595 | 595 | 7 / 7 | 7 / 14 / 13 | ja |
| 2+0 | 365discount | 316 | 316 | 7 / 7 | 8 / 8 / 13 | ja |
| 2+0 | Netto | 269 | 269 | 7 / 7 | 12 / 5 / 18 | ja |
| 2+0 | MENY | 375 | 375 | 7 / 7 | 5 / 12 / 11 | ja |
| 2+0 | Bilka | 376 | 376 | 7 / 7 | 7 / 15 / 11 | ja |
| 2+0 | REMA 1000 | 311 | 311 | 7 / 7 | 10 / 5 / 14 | ja |
| 2+0 | Kvickly | 369 | 369 | 7 / 7 | 8 / 11 / 10 | ja |
| 2+0 | Lidl | 254 | 254 | 7 / 7 | 10 / 10 / 11 | ja |
| 2+0 | SPAR | 400 | 400 | 7 / 7 | 8 / 12 / 16 | ja |
| 2+0 | Min Købmand | 530 | 530 | 7 / 7 | 7 / 16 / 13 | ja |
| 1+0 | 365discount | 236 | 236 | 7 / 7 | 10 / 7 / 12 | ja |
| 1+0 | Netto | 267 | 267 | 7 / 7 | 10 / 9 / 15 | ja |
| 1+0 | MENY | 270 | 270 | 7 / 7 | 6 / 11 / 10 | ja |
| 1+0 | Bilka | 326 | 326 | 7 / 7 | 7 / 14 / 12 | ja |
| 1+0 | REMA 1000 | 216 | 216 | 7 / 7 | 10 / 5 / 14 | ja |
| 1+0 | Kvickly | 306 | 306 | 7 / 7 | 8 / 12 / 7 | ja |
| 1+0 | Lidl | 220 | 220 | 7 / 7 | 10 / 8 / 11 | ja |
| 1+0 | SPAR | 278 | 278 | 7 / 7 | 6 / 13 / 10 | ja |
| 1+0 | Min Købmand | 338 | 338 | 7 / 7 | 5 / 11 / 14 | ja |

**Ikke dækket:** butikslogoer (blokeret lokalt), mørkt tema og rigtig telefon. `confirm()` ved fravalg af valgte retter er uændret (samme mønster som det eksisterende butiksskift). Designfilen har stadig den gamle transporttekst.
