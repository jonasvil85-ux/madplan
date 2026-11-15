# Måltidsjagtens AI-hold

Siden udvikles hver dag af et hold Claude-rutiner i skyen. De styrer sig selv og kontrollerer hinanden. Jonas får en daglig rapport og behøver ikke godkende noget.

| Rolle | Hvornår (UTC) | Opgave | Instruks |
|---|---|---|---|
| Tilbudsrutinen | dagligt 05:08 | Henter nye aviser, skriver retter, bygger data | `scripts/RUTINE.md` |
| Billedhandlingen (GitHub) | dagligt 05:35 | Laver billeder til nye retter | `.github/workflows/billeder.yml` |
| **Ejer** | dagligt 06:00 | Ejer visionen. Skriver krav med acceptkriterier. Efterkontrollerer det udgivne. Gennemgår grundigt om søndagen | `agenter/ejer.md` |
| **UX-udvikler** | dagligt 06:30 | Kreativ designer og udvikler. Tager det øverste krav, designer, bygger på en gren, tester | `agenter/ux-udvikler.md` |
| **Kontrollant** | dagligt 09:00 | Vagtpost over det udgivne (kan rulle tilbage). Validerer grene og slår sammen eller afviser | `agenter/kontrollant.md` |
| **Sekretær** | dagligt 10:30 | Samler dagens fakta til én rapport (`DAGENS.md`) og sender den til Jonas som e-mail | `agenter/sekretaer.md` |

Fælles regler: `regler.md`. Overblik: `STATUS.md`. Seneste dagsrapport: `DAGENS.md`.

## Flowet
1. **Ejer** skriver krav i `BACKLOG.md` (hvad, hvorfor, acceptkriterier, ikke-mål).
2. **UX-udvikler** vælger løsningen, skriver en kort designfil i `design/`, bygger på en gren `ai/DATO-emne`, kører kontrollerne og skriver en rapport med bevis for hvert acceptkriterium. Rører aldrig `main`.
3. **Kontrollant** kører kontrollerne selv, tjekker acceptkriterierne og klassificerer ændringen:
   - **Klasse A** (tekst, design, retter, billeder, tests): slås sammen, når alt er grønt.
   - **Klasse H** (priser, mængder, indkøbsliste, madplanens beregning, cache, byggescripts): slås kun sammen efter skærpet validering: regressionstest, før/efter-tal for alle 9 butikker, mindst tre egne forsøg på at få den til at fejle (rød-hold), og tilbagerulning kan prøves. Mangler et punkt, afvises den.
   - **Afvist:** fejlrapport, UX-udvikleren retter (højst to forsøg), så parkeres opgaven og Ejeren får den.
4. **Vagtposten** (kontrollantens første trin næste dag) tjekker den udgivne side og kan rulle en sammenlægning tilbage med `git revert`.
5. **Ejer** efterkontrollerer: opfyldte det udgivne kravet? Nej giver et nyt krav øverst.
6. **Sekretær** skriver dagsrapporten; en GitHub-handling sender den som e-mail.

## Grundloven
Disse filer kan ingen agent ændre: `regler.md`, `agenter/*`, `.github/`, `auth.js`, `feedback.js`, `privatlivspolitik.html`, nøgler og rutinernes instrukser. Ejeren kan foreslå ændringer; kun Jonas kan gennemføre dem. Det er den eneste menneskelige port.

## Stop alt
Pausér rutinerne på https://claude.ai/code/routines (og slå handlingerne fra under fanen Actions på GitHub).

## Hvad holdet ikke kan (endnu)
- **Browsertest:** skyen har ikke en browser. Udseende vurderes ud fra koden og designfilen; Ejeren ser resultatet på den udgivne side.
- **Brugerfeedback:** ligger i Supabase, som holdet ikke har adgang til. Klistr relevant feedback ind i `BACKLOG.md` under "Fra brugerne".
- **Regressionstest af priser og indkøbsliste i JavaScript:** findes ikke endnu. Den er det første krav i backloggen, og indtil den består, kan ingen klasse H-ændring slås sammen.
