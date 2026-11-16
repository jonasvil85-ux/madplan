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
