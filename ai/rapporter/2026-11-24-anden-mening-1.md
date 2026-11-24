# Anden mening 2026-11-24 (kørsel 1)

Udløst af ændringen i `ai/BACKLOG.md` (commit 3383867): to nye krav (Rema/ris og test af byggeren). Der var ingen ændringer i `ai/design/`. Roller: Product Owner (emne 1 og 2). Ingen `[SIKKERHED]`-krav var nye. Kald: 3 af 3 (1 kreativ, 2 kritiske). Modellen: gpt-oss-120b. Modellen er rådgiver; intet er ændret i backlog eller design.

## Emne 1: [DATA] [H] Rema: "ris" må ikke give riskiks på indkøbslisten

**Spørgsmål:** hvordan forhindrer man generelt forkerte ingrediens-til-tilbud-koblinger af typen ris → riskiks?

**Idéer (kreativ runde):**
1. Kategorikontrol (kategori for ingrediens og tilbud skal passe, ellers afvises koblingen): **valgt i enkel form**: en lille liste over forbudte par i byggeren i stedet for en hel ontologi (for tungt at vedligeholde for 9 butikker).
2. ML-scorer på historiske par: afvist (for lidt træningsdata, uigennemsigtig, kan selv lave fejl; kravet er en forkert vare = værre end ingen).
3. Crowdsourcet "match-mission" for brugere: afvist (siden har ingen brugerkonti i byggeriet; ville give børnesygdomme i tilliden og strider mod "rolig side").
4. Billed-/OCR-genkendelse af tilbudsbillede: afvist (skør, dyr og langsom; tekstmatch er nok).
5. Vend om: først brugerens plan, så kun eksakte produkt-ID'er som tilbud: afvist (produktet er bygget omvendt, tilbud styrer ugen; men tanken "hellere ingen tilbudslinje end en forkert" er allerede kravets kerne).

**Modellens kritik (kritisk runde, omskrevet):**
- Listen kan give falsk tryghed og falske afvisninger: "ris" i "grisekød", "basmatiris", "risengrød". Brug kun hele ord.
- Andre typiske par bør kortlægges: mel/melis, smør/smørbar, ost/ostechips, kokos/kokosmel, mælk/mælkechokolade.
- Vedligeholdelse af listen er uklar (hvem, hvornår).
- Log afviste koblinger; overvej at falde tilbage til "ingen tilbud" frem for at stoppe hele bygget.
- Scan hele varekataloget for tvetydige matches som advarsel.

**Min vurdering:**
- Hele ord/ordslutning: **enig**, men præciser. "basmatiris" og "jasminris" er risvarer og skal accepteres, så regel på ingrediensen alene ("indeholder 'ris'") er ikke nok. Retningen er den modsatte: kig på **tilbuddets titel** for et kiks-/snack-ord (kiks, chips, skiver, majskiks) og afvis, når ingrediensen ikke selv indeholder det ord. "grisekød" er ikke et problem, hvis testen er "ingrediensnavn indeholder ris som ord eller som endelse (-ris), og tilbudstitlen indeholder kiks". Husk reglen i `ai/regler.md`: ikke `\b` med æøå, brug `(?<![a-zæøå])…(?![a-zæøå])`.
- Kortlægning af flere par (mel/melis, smør/smørbar osv.): **delvist enig**. Ikke som ny stor liste i dette krav (scope), men som engangsscan af de nuværende koblinger i alle 9 butikker med resultatet i rapporten. Ny liste kun for par, der faktisk findes i data. Ellers opfindes problemer, som ikke er der.
- Falde tilbage til "ingen tilbud" i stedet for at stoppe: **uenig**. En afvist forkert kobling er netop den slags fejl, der skal gøre bygget rødt (samme princip som 20 %-reglen), så den bliver rettet i kilden; en stille fallback skjuler fejlen. Men fejlmeddelelsen skal navne ret, ingrediens og tilbud.
- Log/vedligeholdelsesproces: **delvist**. Listen står som en navngivet konstant øverst i byggeren med en kommentar om, at nye par tilføjes, når en ny fejltype findes (Ejeren/Kontrollanten ved fund). Ingen ekstra proces.
- Idé 1 var ikke ny for holdet; vigtigste nye ting: at kontrollere fra tilbudssiden, og et engangsscan af alle butikker.

**Foreslået ændring af kravet (tekst til Ejeren):**
> Tilføj til Krav: "Byggeren har en navngivet konstant `FORBUDTE_PAR` (ingrediensord → ord, der ikke må stå i tilbudstitlen; start: ris → kiks), matchet på hele ord eller ordslutning uden `\b` (æøå-sikkert); den afviser koblingen med exit 1 og en fejl, der nævner ret, ingrediens og tilbud. 'basmatiris' og 'jasminris' skal stadig kunne kobles til en rigtig risvare, 'grisekød' må ikke ramme reglen (tests for begge)."
> Tilføj til Accept: "(5) engangsscan af alle nuværende koblinger i alle 9 butikker for lignende par (mel/melis, smør/smørbar, ost/ostechips, mælk/mælkechokolade, kokos/kokosmel) med fundene skrevet i rapporten; nye par føjes kun til listen, hvis de findes i data."
> Ikke-mål (uændret + tilføjet): ingen stille fallback til 'ingen tilbud' i byggeren; ingen ML eller billedgenkendelse.

## Emne 2: [TEST] [A] Test af selve byggeren (10 % dækning skal stoppe bygget)

**Spørgsmål:** hvad kan gøre en test, der kører `byg_retter.py` på en konstrueret kilde og kræver exit 1, selv falsk tryg?

**Idéer:** ingen kreativ runde (kun kritisk, som reglen foreskriver for øvrige emner).

**Modellens kritik (omskrevet):**
- Tester man kun exit-koden, kan bygget fejle af en anden grund (relative stier, manglende konfig, manglende data i den konstruerede kilde), så testen består uden at dækningstjekket er rørt.
- Tjek også stderr for den forventede dækningsmeddelelse.
- Tilføj en positiv test (dækning ≥ 20 % skriver `retter.json`), så man ved, at den konstruerede kilde i sig selv er gyldig.
- Isolér miljøet (midlertidig mappe, rene miljøvariabler) og ryd op.
- Mock/patch funktioner for at se, om `daekning()` blev kaldt.

**Min vurdering:**
- Stderr-tjek på den specifikke dækningsmeddelelse: **enig**, og det er den vigtigste pointe. Uden den kan testen bestå af en forkert årsag.
- Positiv kontroltest (samme kilde med 30 % dækning → exit 0 og fil skrevet): **enig**. Den beviser, at den konstruerede kilde er gyldig, og at 10 %-testen fejler på dækning og ikke på kilden. Tæt på nul meromkostning: samme kilde, kun én værdi ændret.
- Isolation/oprydning med midlertidig mappe: **enig**, og kravets accept (3) (filerne uændrede) dækker det allerede. Det kræver, at byggeren kan pege på en anden mappe; findes det ikke, er det en ændring i et H-script (`scripts/byg_*.py`) og bryder kravets "ikke-mål" og klasse A. Udvikleren skal i så fald stoppe og skrive det i rapporten frem for at ændre byggeren i det samme krav.
- Mock/patch af funktionskald: **uenig**. Man mister det, der gør testen værdifuld, nemlig at køre den rigtige byggeproces. Rød-hold med `if False:` fanger samme fejl med mindre skrøbelighed.

**Foreslået ændring af kravet (tekst til Ejeren):**
> Tilføj til Krav: "testen kræver både exit 1 og at stderr indeholder dækningsfejlen (ret, ingrediens, procent), og kører den samme konstruerede kilde med 30 % dækning som positiv kontrol (exit 0, retter.json skrevet i den midlertidige mappe)."
> Tilføj til Accept: "(4) 10 %-testen fejler ikke af anden årsag end dækning (kontrolleret via den positive test); (5) kan byggeren ikke pege på en midlertidig mappe uden at ændres, skrives det i rapporten, og kravet deles (ændringen af byggeren som eget [H]-krav)."

## Oversigt
- Emner: 2 (begge Product Owner). Kald brugt: 3 af 3.
- Taget med: tilbudstitel-vinklen og æøå-sikker ordmatch, engangsscan af alle butikker (emne 1); stderr-tjek og positiv kontroltest (emne 2).
- Afvist: ML, crowdsourcing, billedgenkendelse, stille fallback, mocking.
- Modellens svar var delvist generelle (fx "dokumentér vedligeholdelsesproces", "log-modul"); jeg tog ikke de generelle råd med.
- Ikke tjekket: jeg har ikke set i byggeren eller dataene, hvilke ingredienser og tilbud der faktisk findes; forslagene om ordmatch skal verificeres mod `retter.json` af udvikleren.

Nyttigt: delvist (ideerne i runde 1 var gængse; de to konkrete tilføjelser til test af byggeren og vinklen fra tilbudstitlen var værd at få med).
