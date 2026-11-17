# Måltidsjagtens AI-hold

Siden udvikles hver dag af et hold Claude-rutiner i skyen. De styrer sig selv og kontrollerer hinanden. Holdet finder selv på forbedringerne og styrer køreplanen. Jonas er primær bruger og brugerprøver: han får en daglig rapport og prøver nye funktioner som almindelig bruger, men skal hverken finde på idéer eller godkende noget teknisk (se `regler.md`, afsnittet Roller).

## Holdet: 9 agenter og 4 automatiske værktøjer

| # | Agent (Claude-rutine) | Hvornår (UTC) | Opgave | Instruks |
|---|---|---|---|---|
| 1 | **Ejer** (CTO og produkt) | dagligt 06:00 | Ejer visionen og køreplanen. Skriver krav med acceptkriterier, efterkontrollerer det udgivne | `agenter/ejer.md` |
| 2 | **UX-designer** | dagligt 06:15 | Omsætter de øverste UX-krav til designfiler og udfordrer kravene | `agenter/ux-designer.md` |
| 3 | **Frontend-udvikler** | dagligt 06:30 | Bygger det brugeren ser, efter designfilen, på en gren | `agenter/ux-udvikler.md` |
| 4 | **Backend- og dataudvikler** | dagligt 06:30 | Bygger beregning, filtre, data og tests, på en gren | `agenter/backend-udvikler.md` |
| 5 | **Kontrollant** (QA) | dagligt 09:00 | Uafhængig validering. Slår sammen, afviser eller ruller tilbage | `agenter/kontrollant.md` |
| 6 | **Sekretær** | dagligt 10:30 | Én dagsrapport til Jonas som e-mail og telefonbesked | `agenter/sekretaer.md` |
| 7 | **Sikkerhedsagent** | onsdag 07:00 | Gennemgår hemmeligheder, Supabase-regler, frontend og privatliv | `agenter/sikkerhed.md` |
| 8 | **SEO- og vækstagent** | torsdag 07:00 | SEO, fastholdelse og måling | `agenter/seo-vaekst.md` |
| 9 | **Tilbudsrutinen** (data) | dagligt 05:08 | Henter aviser, skriver retter, bygger data | `scripts/RUTINE.md` |

| Automatisk værktøj (GitHub, ikke en agent) | Hvornår | Opgave |
|---|---|---|
| Billedhandling | dagligt 05:35 | Laver billeder til nye retter |
| Vagtpost | efter hver ændring + hver 3. time | Sammenligner den udgivne side med main, skriver `HELBRED.md`, rydder grene |
| Browser-QA | efter hver ændring + hver 6. time | Åbner siden i Chromium, måler, tager skærmbilleder, skriver `BROWSER.md` |
| Dagsrapport | når `DAGENS.md` ændres | Sender sekretærens rapport som e-mail |

Fælles regler: `regler.md`. Køreplan: `ROADMAP.md`. Overblik: `STATUS.md`. Seneste dagsrapport: `DAGENS.md`. Målinger fra browseren: `BROWSER.md`.

## Flowet
1. **Ejer** skriver krav i `BACKLOG.md`, mærket `[UX]`, `[BACKEND]`, `[DATA]`, `[TEST]`, `[SIKKERHED]` eller `[SEO]`, og holder `ROADMAP.md` levende.
2. **UX-designer** laver designfilen til de øverste `[UX]`-krav (`design/`), efter at have set siden og skærmbillederne fra Browser-QA. Udfordrer kravet, hvis det er dårligt for brugeren.
3. **Frontend-udvikler** bygger `[UX]`-kravet efter designfilen; **Backend- og dataudvikleren** bygger `[BACKEND]`/`[DATA]`/`[TEST]`. Begge på egne grene `ai/DATO-emne`, med kontrollerne og en rapport med bevis for hvert acceptkriterium. Ingen rører `main`.
4. **Kontrollant** kører kontrollerne selv, tjekker acceptkriterierne og klassificerer:
   - **Klasse A** (tekst, design, retter, billeder, tests): slås sammen, når alt er grønt.
   - **Klasse H** (priser, mængder, indkøbsliste, madplanens beregning, cache, byggescripts): slås kun sammen efter skærpet validering: regressionstest, før/efter-tal for alle 9 butikker, mindst tre egne forsøg på at få den til at fejle, og tilbagerulning kan prøves.
   - **Afvist:** fejlrapport, udvikleren retter (højst tre forsøg, kun indholdsfejl tæller, hvert forsøg skal ændre løsningen), så parkeres opgaven og Ejeren får den. Op til tre uafhængige H-ændringer om dagen med regression efter hver (regler godkendt af Jonas 2026-11-16).
5. **Vagtposten** og **Browser-QA** (GitHub) måler den udgivne side. Kontrollantens første trin næste dag læser dem og kan rulle en sammenlægning tilbage med `git revert`.
6. **Ejer** efterkontrollerer: opfyldte det udgivne kravet? Nej giver et nyt krav øverst.
7. **Sikkerhed** og **SEO/vækst** skriver ugentligt krav i backloggen.
8. **Sekretær** skriver dagsrapporten; en GitHub-handling sender den som e-mail.

## Grundloven
Disse filer kan ingen agent ændre: `regler.md`, `agenter/*`, `.github/`, `auth.js`, `feedback.js`, `privatlivspolitik.html`, nøgler og rutinernes instrukser. Ejeren og sikkerhedsagenten kan foreslå ændringer; kun Jonas kan gennemføre dem. Det er den eneste menneskelige port.

## Stop alt
Pausér rutinerne på https://claude.ai/code/routines (og slå handlingerne fra under fanen Actions på GitHub).

## Hvad holdet ikke kan (endnu)
- **Se siden live:** agenterne har ingen browser. De læser `BROWSER.md` og skærmbillederne fra Browser-QA (en rigtig browser i GitHub), men kan ikke selv klikke rundt.
- **Brugerfeedback og trafik:** ligger i Supabase og Vercel Insights, som holdet ikke har adgang til. Klistr relevant data ind i `BACKLOG.md` under "Fra brugerne".
- **Konkurrentresearch:** skyen kan ikke komme på nettet. Det gør Claude i chatten på forespørgsel.
