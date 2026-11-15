# Måltidsjagtens AI-hold

Siden udvikles hver dag af et lille hold Claude-rutiner i skyen. De arbejder på hver sin rolle og kontrollerer hinanden. Jonas er direktør og beslutter alt, der kan skade.

| Rolle | Hvornår (UTC) | Opgave | Instruks |
|---|---|---|---|
| Tilbudsrutinen (findes) | dagligt 05:08 | Henter nye aviser, skriver retter, bygger data | `scripts/RUTINE.md` |
| **Udvikler** | dagligt 06:30 | Tager ÉN opgave fra `BACKLOG.md`, bygger den på en egen gren, tester, skriver rapport | `agenter/udvikler.md` |
| **Kontrollant** | dagligt 09:00 | Uafhængig kontrol af udviklerens gren. Slår sammen med main, afviser eller sender til Jonas | `agenter/kontrollant.md` |
| **Produktchef** | mandag 06:00 | Gennemgår siden og rapporterne, rydder op i og prioriterer `BACKLOG.md` | `agenter/produktchef.md` |

Fælles regler for alle: `regler.md`. Overblik over hvad der sker: `STATUS.md`.

## Flowet
1. Udvikleren arbejder aldrig direkte på `main`. Alt sker på en gren `ai/DATO-emne`.
2. Udvikleren kører `python -I scripts/tests/kontrol.py` og skriver en rapport i `rapporter/`.
3. Kontrolløren kører kontrollerne selv, læser ændringen med friske øjne og klassificerer den:
   - **Klasse A (sikker):** tekst, layout/CSS, nye eller ændrede retter og opskrifter, billeder, dokumentation, tests. Kontrolløren slår sammen med `main` (Vercel udgiver automatisk), hvis alt er bestået.
   - **Klasse B (kræver Jonas):** alt der rører priser, mængder, indkøbslisten, madplanens beregning, service worker, login/dataindsamling, byggescripts, rutinernes instrukser eller sletter mange retter. Grenen bliver stående og står som VENTER i `STATUS.md`. Jonas siger "godkend ai/…" i chatten, så slår Claude den sammen.
   - **Afvist:** fejl rapporteres i `rapporter/`; udvikleren retter dagen efter (højst to forsøg, så parkeres opgaven).
4. Skyen har `node`, så kontrollen syntaks-tjekker al JavaScript. Mangler node en dag (kontrollen skriver det), er enhver ændring i `.js`/`index.html` automatisk klasse B. Syntaks-tjek er ikke det samme som, at siden virker – derfor er ændringer i beregninger altid B.
5. Alt kan rulles tilbage: `main` er en git-historik, og hver ændring er ét sammenlægnings-commit.

## Jonas' styring
- Se `STATUS.md` på GitHub (eller bed Claude i chatten om status).
- Skriv ønsker øverst i `BACKLOG.md` (eller sig dem i chatten), så tages de først.
- Stop alt: pausér rutinerne på https://claude.ai/code/routines.

## Hvad holdet ikke kan (endnu)
- **Billeder:** laves af GitHub-handlingen `.github/workflows/billeder.yml` hver dag kl. 05:35 UTC (kræver hemmeligheden `CLOUDFLARE_API_TOKEN` i GitHub). Uden den, eller indtil den har kørt, viser nye retter et gaffelikon; Jonas kan også køre `python -I scripts/billeder.py` lokalt.
- **Browsertest:** skyen har ikke en browser. Visuelle ændringer vurderes ud fra koden; Jonas ser dem på siden efter udgivelsen.
- **Brugerfeedback:** ligger i Supabase, som holdet ikke har adgang til. Klistr relevant feedback ind i `BACKLOG.md`.
