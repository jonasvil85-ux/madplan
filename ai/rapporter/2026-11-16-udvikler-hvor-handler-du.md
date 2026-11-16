# Udviklerrapport 2026-11-16 – "Hvor handler du?": ét kort, flere butikker med et tryk, én regel for to butikker

**Erstatter** grenene `ai/2026-11-16-et-kort` og `ai/2026-11-16-to-butikker`. De skal ikke slås sammen; denne gren indeholder begge og Jonas' revision. Én H-ændring, én tilbagerulning.

**Hvad brugeren ser:**
- Ét kort, "Hvor handler du?". Listen over de 9 butikker, billigst først, er afkrydsning. Et tryk sætter eller fjerner fluebenet, gerne på flere butikker.
- Med flere butikker valgt vises "Hvor mange butikker vil du handle i?" under listen (1 butik / 2 butikker, "Anbefalet").
- Logo-gitteret, "Hvor mange butikker" ved én butik og knappen "Vælg selv flere butikker" er væk.
- Har man én butik valgt, og et par er mindst 30 kr billigere, står der fx "Spar 54 kr ved også at handle i Netto – Lidl + Netto: 367 kr for ugen mod 421 kr i Lidl alene. Transport og ekstra tid er ikke regnet med i prisen. [Tilføj Netto]". Forslaget forsvinder, når parret er valgt.
- En valgt butik skjules aldrig, når listen er foldet sammen ("Vis alle 9 butikker").
- Uden priser (fejl) vises listen stadig, så man kan vælge.

**Hvorfor:** Jonas 2026-11-16:
- Om de to kort: "det fremstår ikke særlig smart, at jeg har 'hvor handler du' og sammenlign butikker".
- Om flere butikker: "Kunderne skal have mulighed for at vælge mere end en butik bare ved at trykke på en butik mere. Det er vigtigt du laver det her pænt, simpelt og logisk."
- Om to butikker: "Vælger man flere butikker skal det jo gerne blive billigere".

Krav: BACKLOG "Ét kort" (revideret) og "Én regel for to butikker". Design: `ai/design/2026-11-16-hvor-handler-du-samlet.md`.

**Sådan virker et tryk:** rækken bruger `skiftButik` – præcis den funktion, logoerne brugte (spørger, før valgte retter fjernes; antal butikker følger igen anbefalingen; gemmes). Derefter `opdaterButikRoligt` som før. Ingen pris-, plan- eller listefunktion er ændret.

**To butikker (én regel):** kortet anbefaler et par, når parrets fælles billigste uge (én samlet liste over begge butikker, egne tilbud) er mindst 30 kr (`ANBEFAL_SPAR`) billigere end den billigste enkeltbutiks uge. Sammenligningen sker på præcise tal, som boksens `anbefaletAntal`. Vælger man parret, anbefaler boksen 2 butikker til samme pris (testet).

**Klasse:** H.

**Filer:** `index.html`, `scripts/tests/sammenlign.js`, `scripts/tests/sammenlign_side.js`, denne rapport (og rapporterne for et-kort og to-butikker, som denne gren bygger videre på).

**Test (alle automatiske):**
- `sammenlign.js` (node): alle 9 butikker × 2+2/2+0/1+0 og alle 36 par regnes igen. Den tjekker reglen på præcise tal, besparelse = forskellen på de viste tal, og at boksen anbefaler 2 butikker til samme pris for hvert anbefalet par.
- `sammenlign_side.js` (Chromium, 390 px, touch, kørt af `sammenlign_browser.py`):
  - priser i DOM mod enkeltvalget, sortering, "Billigst";
  - kombiknappen: siger "Tilføj Netto", vælger parret, boksen viser "2 butikker 367 kr Netto og Lidl Anbefalet", madplanen koster 367 kr, og forslaget forsvinder;
  - ét kort: ingen logo-gitter, ingen særskilt knap, intet "Hvor mange butikker" ved én butik;
  - et tryk på en butik mere giver flueben på begge, "Hvor mange butikker" med 2 butikker og 7 dage; et tryk igen giver én butik og samme pris som rækken;
  - en valgt butik forbliver synlig, når listen foldes sammen;
  - rundvisningen og fejlvisningen;
  - madplanens placering og tidsmåling.
- Mutationsprøve: rækken sat tilbage til "vælg kun denne" og "Vis alle" skjulte valgte butikker. Testen fangede 6 brud ("tryk på netto gav [\"netto\"] (forventet begge)" m.fl.).
- Headless Edge, to kørsler: `FEJL: []`; længste opgave 73–137 ms; madplanen ved 884 px med forslaget (ca. 220 px), dvs. ca. 660 px uden.
- `budget.js` uændret (ac9c5f5cbdb3), `kontrol.py` BESTÅET, før/efter 27 af 27 identiske.

**Ikke ændret (bevidst):** boksens regel og antal-felterne; den gamle CSS for logo-gitteret ligger tilbage uden brug (ufarlig; fjernes i en oprydning, så stylesheetet ikke risikerer en halv regel).

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

## Tilføjet efter Jonas' afprøvning ("Lidl er valgt – vælger jeg SPAR også, står der stadig bare Lidl – det er ikke intuitivt")
- **En valgt butik, som madplanen ikke bruger, siger det selv i sin række:** stiplet kant, gråt flueben og teksten "Ikke med i madplanen – Ugen er billigere uden SPAR". Den sidste del står kun, når ingen kombination er billigere.
- **Under listen står én klar sætning** i stedet for en ensom "1 butik"-knap: "Madplanen bruger kun Lidl: 421 kr. SPAR gør ikke ugen billigere denne uge, så der er ingen varer derfra i madplanen." Den ekstra note nederst vises så ikke, så det ikke står to gange.
- **Kan flere butikker betale sig,** vises valget "1 butik / 2 butikker – Anbefalet" som før. Sætningen og boksen bruger samme regel for, hvilke felter der vises (`antalSynlige`), så de aldrig er uenige.

**Test:** browsertesten finder selv en butik, der ikke gør ugen billigere sammen med den billigste (i denne uge Lidl + SPAR), og tjekker rækken, sætningen, at der ikke er en ensom knap, og at forklaringen ikke står to gange. Den fejler, hvis den ikke kan finde et sådant tilfælde.
- Mutationsprøve: rækkens markering fjernet. Testen fangede det ("rækken for spar siger ikke, at den ikke er med i madplanen").

**Tidsmåling:** mine egne headless Edge-processer hobede sig op igen (68 stk.), og tiderne steg til ca. 250 ms, også i en kopi uden ændringen. Efter oprydning efter hver kørsel er tiderne 69–154 ms.
