# Anden mening 2026-11-27 (kørsel 1)

Ændringen i `HEAD~1..HEAD`: ét nyt krav i `ai/BACKLOG.md` (Ejer, 2026-11-27, [DATA] [H] HASTER: fire retter over 450 kr). Ingen ændringer i `ai/design/` og ingen `[SIKKERHED]`-krav. Altså ét emne (Product Owner). Kun kritisk runde; kreativ runde sprunget over, fordi kravet er en hastende rettelse med fast løsningsrum, hvor nye idéer ikke tilfører noget. 1 af 3 kald brugt.

## Emne 1: Haster – fire retter over 450 kr (bilka og spar)
**Spørgsmål:** Hvad er svagt, glemt eller risikabelt i kravet om at fjerne/rette de fire dyre retter og finde fejlkoblinger frem for blot at slette?

**Idéer (kreativ runde):** ingen (ikke kørt, se ovenfor).

**Modellens kritik (omskrevet):**
- Grænsen på 450 kr er uklar (pr. portion, samlet, inkl. moms?).
- "Fejlkobling" er ikke defineret; hvem beslutter "billigere"?
- Mangler fallback: vis prisen ærligt i stedet for at slette; audit-log; CI der kører kontrollen før commit; besked til brugeren.
- Risiko: forkerte indkøbssedler ved hastige koblingsrettelser; populære retter forsvinder uden forklaring; inkonsistente menuer.
- Forslag: præ-commit-validering, automatisk alternativ-generator, ændringslog i admin, konfigurerbar grænse pr. butik.

**Min vurdering:**
- Uklar grænse: **uenig.** Kravet siger "aftensret til 4", og 450 kr er en eksisterende kontrolgrænse i `kontrol.py`; ikke-målet udelukker netop at ændre den.
- Fejlkobling ikke defineret: **delvist enig.** Kravet nævner "mængde mod pakke", men giver ikke en konkret fremgangsmåde. Se forslag 1.
- Vis prisen ærligt i stedet for at slette: **uenig.** Produktets mål er en realistisk aftensmad til en almindelig familie; en ret til 500 kr er ikke en ærlig-pris-sag, men et udvalgskriterie. Sletning er legitim, når koblingen er korrekt.
- Præ-commit-validering: **enig i substansen, ikke nyt.** Kravet nævner selv gentagelsesproblemet, og forslaget ligger allerede hos Jonas. Tilbudsrutinens instrukser er grundlov, så det kan ikke ændres her.
- Alternativ-generator, admin-log, konfigurerbar grænse pr. butik: **uenig.** Overdimensioneret til en hastesag, bryder ikke-målet (byggerlogik/grænse urørt) og er det generelle råd uden konkret indhold, som reglerne advarer mod.
- Tab af tillid ved hastig rettelse: **enig, men dækket** af accept (3) og (1).

**Foreslået ændring af kravet (konkret tekst til Ejeren):**
1. Tilføj under Krav: "For hver af de fire retter skrives i rapporten, om prisen er (a) fejlkobling (angiv ingrediens, mængde og pakke), eller (b) korrekt, men dyr. Kun (b) løses ved sletning eller ved at bytte dyr ingrediens (fx okse/and) til billigere variant; (a) rettes i koblingen."
2. Tilføj til Accept: "(6) Hver rettet kobling har en automatisk kontrol i `kontrol.py` (fx loft for mængde pr. pakke), hvis fejlen kunne være fanget automatisk (jf. regler.md)."
3. Tilføj til Accept: "(7) Slettede retter nævnes med navn i rapporten, så de kan genindføres, hvis aviserne ændrer sig."

**Ikke taget med:** alternativ-generator, admin-log, ændring af grænsen, brugerbesked om budget.

Nyttigt: delvist (modellen var overvejende generel; kun punktet om at kræve en eksplicit skelnen mellem fejlkobling og korrekt-men-dyr, samt en automatisk kontrol pr. rettet kobling, var brugbart).
