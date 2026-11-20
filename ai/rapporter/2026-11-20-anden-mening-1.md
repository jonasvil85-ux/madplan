# Anden mening 2026-11-20 (kørsel 1)

Ændring i `HEAD~1..HEAD`: kun `ai/BACKLOG.md` (Ejer 2026-11-20). Én ny ting: opdateringslinjen under det øverste krav **[DATA] [H] Ret kendte datafejl** (25 ty-advarsler i stedet for 16, 5 nye retter over 450 kr). Ingen designfiler ændret. Emner: 1. Modellen blev kaldt 2 gange (kreativ + kritisk).

## Emne 1: [DATA] [H] Ret kendte datafejl (opdateret med uge 48-tal)

**Spørgsmål:** Hvordan gør vi typerettelser og dyre retter robuste, så problemet ikke vokser hver ny avis, uden at opfinde priser?

### Idéer (kreativ runde)
1. Automatisk API-integration og valideringspipeline: **afvist**. Skal ikke bygge ny datakilde; vi har Tjek-data, og kravet er klasse H med små trin.
2. Versionsstyret typeliste med automatiske tests: **delvist valgt**. Vi har allerede liste og kontrol; det nye er, at kontrollen skal fejle samme dag, en ny avis giver ingredienser med tilbud uden `ty`.
3. Fællesskabs-tagging med point og rabatkoder: **afvist** (brugerinput i data, rabatkoder, støj, uforeneligt med rolig side og ærlige tal).
4. "Budget-first" forside med skjult premium-menu: **delvist valgt**. Idéen om, at forsiden kun må have retter under grænsen, passer; "premium-menuen" afvises som ny funktion uden for kravet.
5. Måltidslotteri: **afvist** (modsiger ærlig, forudsigelig plan og børnevenlig mad).

### Modellens kritik (kritisk runde, omskrevet)
Modellen kaldte kravet vagt: hvad "avis" og "fejler" betyder, hvordan retprisen beregnes, udsolgte tilbud, besked til brugeren når en ret fjernes, opdateringstidspunkt og rollback. Den foreslog et maskinlæsbart typekatalog med "ikke-mad"-blacklist.

### Min vurdering
- **Enig, konkret:** kravet siger ikke, hvilken pris grænsen på 450 kr gælder (forbrugspris eller indkøbspris; `regler.md` skiller dem). Det kan give uenighed mellem Udvikler og Kontrollant.
- **Delvist:** typekatalog/blacklist. Typelisten findes allerede i `bibliotek_typer.py`, og "uden at ramme ikke-mad" ligger allerede i kravet og i kontrollantens rød-hold ('Jalapeño ost', 'Mayonnaise med mango', blandingsfars). Ny struktur er ikke nødvendig; en tilføjet negativ test pr. rød-hold-eksempel er nok.
- **Uenig:** udsolgte tilbud, brugerbesked ved fjernelse af en ret, notifikationer og opdateringstidspunkt. Det er generelle råd uden for dette krav; retter fjernes fra forsiden før udgivelse, ikke for en bruger i drift. Rollback er allerede kontrollantens H-regel.
- "Test med brugere"-agtige råd er ikke taget med.

### Foreslået ændring af kravet (tekst til Ejeren)
Tilføj i Krav/Accept:
- "(4) Grænsen på 450 kr gælder **forbrugsprisen for hele retten til 4 personer** (kun den mængde retten bruger, ikke hele pakker); indkøbsprisen (hele pakker) må være højere. Kontrollen og før/efter-tallene angiver, hvilken af de to der er målt."
- "(5) Kontrollen fejler (ikke kun advarer), hvis en ingrediens med tilbud mangler `ty`, så nye mangler efter hver avis opdages samme dag. Tilføj en test pr. rød-hold-eksempel (Jalapeño ost, Mayonnaise med mango, blandingsfars), der viser, at de ikke får forkert type."
- "Retter, der ikke kan komme under grænsen med rigtige tal, fjernes fra forsiden; ingen priser opfindes."

Nyttigt: delvist (pris-definitionen var et hul; resten kendte vi eller var generelt).
