# Produktrevision og køreplan (15. november 2026)

Mandat: AI-holdet udvikler hele Måltidsjagten – ikke kun data og billeder. Mål: Danmarks bedste platform for madplan og tilbud. Denne fil er Ejerens og UX-udviklerens fælles køreplan; Ejeren opdaterer den hver søndag.

## Hvad der virker (målt 15/11-2026 med headless Edge, 360/390/768/1280 px)
- Hurtig: indlæsning under 1 sekund, ingen JavaScript-fejl i konsollen, intet vandret scroll på siden.
- Komplet flow i fem trin (butik → retter → indkøbsliste → tilføj varer → seddel), onboarding i seks trin, PWA, delbar liste, 9 butikker, ugeforslag med variation og farve, Fitness/Budget/Kokken/Vegetar, login (Supabase), feedback-chat.
- Billeder på alle 479 butiksretter og 193 opskrifter. Faste kontroller, regressionstest og vagtpost.

## Svagheder (med målinger)
1. **Usynlig for Google.** Én URL (`/`) og to adresser i sitemap. Ingen opskrift har sin egen side, så ingen kan finde en ret via søgning.
2. **Små tryk-flader på mobil.** 25–27 knapper og links er under 32 px høje (anbefaling 44 px).
3. **Ingen budget-indgang.** Forslaget optimerer pris, men brugeren kan ikke sige "højst 600 kr".
4. **Ingen fravalg.** Man kan ikke sige "vi spiser ikke svinekød/fisk/løg" – forslagene kan derfor være ubrugelige for mange husstande.
5. **Ingen favoritter eller gemte madplaner** – ingen grund til at komme igen om mandagen.
6. **Ingen "tøm køleskabet"** og ingen prisalarmer (kræver mere backend; senere).
7. **Monolit:** `index.html` er 206 KB og ca. 2.800 linjer med alt indlejret. Regressionstesten gør den sikrere at ændre, men en opdeling bør ske gradvist.
8. **Data:** 25 ingredienser i Netto uden typeoplysning, et par urealistisk dyre retter, to butikker med mere end halvdelen svinekød.
9. **Ingen måling af brugernes adfærd** ud over Vercel Insights; Ejeren ved ikke, hvor brugerne falder fra.

## Rangeret køreplan (værdi for brugeren → indsats)
| # | Tiltag | Klasse | Hvorfor først |
|---|---|---|---|
| 1 | Opskriftssider med Recipe-markup, oversigt og sitemap | A | Største vækstmulighed; ingen risiko for prisberegning |
| 2 | Mobil: tryk-flader og luft | A | Primær enhed; hurtig gevinst |
| 3 | Budget: "højst X kr for ugen" | H | Den funktion familier forstår; differentierer |
| 4 | Fravalg og kost | H | Gør forslaget brugbart for flere |
| 5 | Favoritter og gemte madplaner | A | Retention |
| 6 | Data: farver, svinekød-andel, typer, dyre retter | A | Kvalitet og blikfang |
| 7 | Banner om gemt kopi | H | Ærlighed ved blokeret netværk |
| 8 | Tøm køleskabet; prisalarmer; push | H | Efter 3–5; kræver design og eventuelt backend |
| 9 | Opdel `index.html` i moduler | H | Når regressionstesten dækker nok |

## Hvad holdet ikke kan måle endnu
Udseende i browser (ingen browser i skyen), brugeradfærd (ingen adgang til Supabase/Insights), konkurrenters sider (netværket i skyen er begrænset). Forslag til at lukke hullerne står i Ejerens rapporter.
