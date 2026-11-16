# Udviklerrapport 2026-11-16 – ét kort for butiksvalg ("Hvor handler du?" + "Sammenlign butikker")

**Hvad:** forsiden har nu ét kort, "Hvor handler du?":
- Den rangerede liste (hver butiks billigste uge ud fra dens egne tilbud) ER butiksvalget; et tryk på en række vælger butikken.
- Overskriften "Sammenlign butikker" og det separate kort er væk.
- Logo-gitteret og "Hvor mange butikker" ligger bag "Vælg selv flere butikker ›" (knap med aria-expanded). Den er åben af sig selv, når der er valgt mere end én butik, så et eksisterende flerbutiksvalg aldrig skjules.
- "Vis alle 9" og "Vælg selv flere butikker" står som to tekstlinks på én linje under listen; to-butiks-forslaget står mellem listen og linkene.
- Rundvisningens trin 2 peger på listen, trin 3 på "Vælg selv flere butikker".

**Hvorfor:** Jonas: "det fremstår ikke særlig smart, at jeg har 'hvor handler du' og sammenlign butikker". Godkendt af Jonas 2026-11-16: "læg det sammen i et kort og udregn prisen på baggrund af det du mener er korrekt". Krav og designfil: BACKLOG "Ét kort" og `ai/design/2026-11-16-hvor-handler-du-samlet.md`.

**Prisgrundlag (uændret):** hver butiks egen billigste uge ud fra dens egne tilbud. Fravalgt: "samme madplan i alle butikker", fordi det er urimeligt over for butikker, hvor retterne ikke er på tilbud (Jonas' pointe). Teksten siger nu: "Billigste uge i hver butik ud fra dens egne tilbud · 7 aftensmåltider til 2 voksne + 2 børn."

**Klasse:** H (ændrer det eksisterende butiksvalg på forsiden). Ingen pris-, plan- eller listefunktion er ændret.

**Filer:** `index.html` (butikPanel, sammenlignHtml, ny klik-lytter for "Vælg selv flere butikker", rundvisningens trin 2–3, CSS), `scripts/tests/sammenlign_side.js` (nye tjek), denne rapport.

**Accept:**
- (1) ét kort, ingen "Sammenlign butikker"-overskrift, logo-gitter og "Hvor mange butikker" skjult ved én butik: ✓ (browsertest).
- (2) alle tal uændrede: `sammenlign.js` samme fingeraftryk som på main (bc1c23328b49), browsertestens prisdel består.
- (3) tryk på række / kombiknap: ✓ (uændret, browsertest).
- (4) "Vælg selv flere butikker": åbner valget, afkrydsning af en anden butik giver 2 butikker, "2 butikker" i "Hvor mange butikker" og 7 dage; åbent af sig selv med 2 butikker; "Skjul" skjuler: ✓ (browsertest).
- (5) madplanen på 390 px: main 1056 px → grenen 683 px (overskriften), dvs. 373 px højere: ✓ (browsertest, grænse 756 px).
- (6) alle 6 rundvisningstrin peger på synlige områder: ✓ (browsertest).
- (7) regression og budget uændrede: `budget.js` samme fingeraftryk (ac9c5f5cbdb3); `kontrol.py` BESTÅET; intet vandret scroll; tryk-flader ≥ 44 px (browsertest).
- (8) tekst: ✓.
- (9) automatisk test: (1), (4), (5) og (6) i `scripts/tests/sammenlign_side.js`, kørt af `sammenlign_browser.py`.
- (10) før/efter: tabel nedenfor.

**Mutationsprøve:** i en kopi blev logo-valget gjort altid synligt, og rundvisningens trin 3 blev sat tilbage til `#antal-plads`. Browsertesten fangede alle fire brud (logo-gitter synligt, "Hvor mange butikker" synligt, madplanen 1002 px nede, rundvisningen).

**Kørt lokalt:** testkoden er kørt i headless Edge (390 px, touch) to gange, `FEJL: []` begge gange. Node og Playwright findes ikke her.

**Set, men IKKE ændret (kræver Jonas' ja):** i "Vælg selv flere butikker" viser den eksisterende boks "Hvor mange butikker" fx "2 butikker 367 kr (Netto og Lidl) – Anbefalet" efter den gamle regel (≥ 30 kr billigere end 1 butik). Kortets to-butiks-forslag bruger den ærlige regel (samme retter og mængder) og anbefaler ikke den kombination (kun 24 kr skyldes butiksvalget). De to regler bør være ens, men det ændrer madplanen for brugere med flere butikker, så det er en egen opgave.

**Før/efter-tal (sidens egne funktioner, main mod grenen, 27 af 27 identiske):**

| Husstand | Butik | Ugepris før | Ugepris efter | Retter | Indkøbslinjer tilbud / øvrige / basis | Ens (samme ret-id'er) |
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

**Ikke dækket:** butikslogoer (blokeret lokalt), mørkt tema og rigtig telefon.

---

## Forsøg 2 (2026-11-16, efter kontrollantens afvisning)

**Fund rettet (rød-hold 4):** når priserne ikke kan regnes (`SAMM.fejlAlle`), sagde teksten "Du kan stadig vælge butik ovenfor", men valget står nu nedenfor. Nu:
- Teksten er "Priserne kunne ikke regnes lige nu. Vælg din butik nedenfor."
- Logo-valget åbnes af sig selv i den situation (`sammenlignTegn`), fordi listen så mangler, og logo-valget er den eneste vej til en butik. Teksten peger altså på noget, der findes og er synligt.

**Ny test:** `sammenlign_side.js` sætter `SAMM.fejlAlle` og kræver, at teksten ikke siger "ovenfor", og at logo-valget er synligt.
- Mutationsprøve: den gamle tekst og uden automatisk åbning, og testen fangede begge.
- Grenen i headless Edge (390 px), to kørsler: `FEJL: []`; længste opgave 51–122 ms.

**Om tidsmålingerne tidligere i dag:** mine egne headless Edge-processer fra testkørslerne blev ikke lukket ordentligt (kun forældreprocessen), så maskinen var belastet. Det forklarer en del af de 219–277 ms, jeg rapporterede under sammenlign-butikker. Efter oprydning: 51–122 ms. Mine testscripts lukker nu hele processtræet.

**Fingeraftryk:** kontrollantens `sammenlign.js` (node, frossen datakopi) giver 5c7736814650. Mit bc1c23328b49 er fra samme testkode kørt i Edge på de aktuelle data, så de to tal kan ikke sammenlignes. Det afgørende er, at main og grenen giver samme tal i samme miljø, og det er de hos os begge.

**H-plads:** dagens tre er brugt, så grenen kan tidligst slås sammen 2026-11-17.
