# Anden mening 2026-11-22 (kørsel 1)

Udløst af ændring i `ai/BACKLOG.md` (commit e98dcc2). Nyt i diffen: kravet "Søg i Vælg selv", små rettelser til "Gode tilbud", en samlet TEST-opgave, en opdatering/opfølgning til dataopgaven (ty-advarsler, retter over 450 kr, afvisning af koblinger under 20 %) og et arkiv. Ingen `[SIKKERHED]`-ændringer og ingen designfiler. Rollen er Product Owner.

Valgte emner (2 af højst 3):
1. **Søg i "Vælg selv"** (UX/A): kreativ runde + kritisk runde.
2. Dataopgavens opfølgning om `byg_retter.py`-afvisning og udgivelsestjek: **ikke sendt til modellen**. Det er en intern byggeregel uden brugerside, og modellen kan ikke vide noget om vores data. Det ville være et spildt kald.
Resten (småtekster "Vis 1 mere", samling af tre testpunkter, arkivering) er for små til at validere.

Kald brugt: 2 af 3.

## Emne 1: Søg i "Vælg selv"
**Spørgsmål i én linje:** Hvordan hjælper vi brugeren med at finde en ret i en meget lang liste (søgefelt med ret og ingrediens, ét tryk rydder, valgte retter bevares)?

### Idéer (kreativ runde)
1. **Instant-filter med fastlåst søgefelt og valgte retter, der "klæber" øverst** – *delvist valgt:* sticky felt tages med. At valgte retter klæber øverst i listen afvises (kravet siger allerede, at madplanen aldrig mister dem; en ekstra række forstyrrer en rolig side).
2. **Tags/hurtigvalg (Kylling, Pasta …) i en vandret bjælke** – *valgt i lille form:* 5–6 hurtigvalg, så man ikke skal taste på telefonen. Kalorie- og tids-tags afvises (vi har ikke pålidelige data, og "ærlige tal" vejer tungere).
3. **Stemme/chat-assistent "Mad-Mika"** – afvist: kræver ekstern tjeneste og ny persondatahåndtering, og siden skal være rolig.
4. **Vend problemet: indtast budget/hovedingrediens, få færdig plan** – afvist som nyt krav: det er i forvejen ugeforslaget plus budgetfunktionen; "Vælg selv" er til dem, der vil vælge selv.
5. **AR-kort/spil** – afvist: skørt, tungt, mod målet om lav pris og rolig side.
Ingen radikalt enklere løsning kom, der var bedre end søgefeltet. (Den enklere vej, kategori-ankre øverst, findes allerede som kategorier og er ikke nok ifølge kravet.)

### Modellens kritik (kritisk runde, omskrevet)
- Usikker placering/synlighed af søgefelt og "ryd"-knap.
- Tastaturet kan dække et sticky felt og de første træffere.
- Uklart om hurtigvalg kan kombineres, eller om de nulstiller søgefeltet.
- Delstrengs-match ("ris" i "tris") giver forkerte træffere.
- Manglende debounce kan få siden til at hakke.
- Foreslog server-side søgning/virtuel scroll "med 63.000 retter".

### Min vurdering
- **Enig:** delstrengs-match (vigtigst og konkret; "ris" mod "tris", "ål" mod "pålæg"). Ryd-knap inde i feltet. Hurtigvalgenes adfærd skal skrives ned.
- **Delvist enig:** tastaturet. Vi kan ikke løse det med en regel i teksten; kravet bør i stedet sige, at feltet ikke må dække træfferne, og at det testes (Chromium kan emulere en lille visningshøjde). Debounce: ja, men kort (ca. 150 ms), og kun hvis målingen viser behov.
- **Uenig:** server-side søgning/virtuel scroll. Modellen har misforstået tallet: 63.000 er *pixel* i højden, ikke antal retter. Siden er statisk med data i browseren; en server ville koste, bryde "lav pris" og kræve privatlivsændring (grundlov). Højden på feltet og "390 px" er bredde, ikke højde; kritikken om "usædvanligt højt" er en misforståelse.
- Generelle råd uden indhold (dokumentér, tydelig knap) er taget med kun, hvor de blev gjort konkrete ovenfor.

### Foreslået ændring af kravet (konkret tekst til "Søg i Vælg selv")
Tilføj til **Krav:** "Under feltet står 5–6 hurtigvalg (fx Kylling, Pasta, Fisk, Suppe, Vegetar) som tryk uden at taste. Et hurtigvalg skriver sit ord i søgefeltet (så ét filter, ét tryk rydder); et nyt hurtigvalg erstatter det forrige. Søgefeltet bliver siddende øverst under scroll."
Erstat Accept (2) med: "(2) søgning på ret og ingrediens uden at skelne store/små bogstaver og med æ/ø/å; match sker på ordets *begyndelse* (fx giver 'ris' ikke 'tris' og 'ål' ikke 'pålæg'), og testen har mindst fire sådanne par."
Tilføj Accept: "(7) med tastatur oppe (visningshøjde ca. 400 px) dækker det siddende felt ikke de første træffere; (8) hvert hurtigvalg giver mindst 3 retter i hver af de 9 butikkers retsæt (ellers fjernes det)." Der er ingen server-side søgning (Ikke-mål).

## Samlet
Modellen havde ét konkret nyt punkt, jeg ikke havde skrevet ned: delstrengs-match i ingrediens-søgning. Hurtigvalg kom fra den kreative runde. Resten var generelt eller bygget på en misforståelse.

Nyttigt: delvist
