# Faste regler for alle agenter

Læs dem, før du rører noget. De kommer fra Jonas (ejeren) eller fra fejl, vi har haft.

## Produktet
- Måltidsjagten laver ugens madplan og indkøbsseddel ud fra supermarkedernes tilbud (9 butikker, Tjek-data). Målgruppe: en dansk familie, 2 voksne + 2 børn. Sproget på siden er dansk.
- Mål: lave priser, mange tilbud i brug, ærlig mærkning, børnevenlig mad, rolig og pæn side. En fejl i en pris eller mængde er værre end en manglende funktion.
- **Kun rigtig aftensmad.** Ingen desserter, søde pandekager, grød, morgenmad eller frokost (rugbrødsmadder). Mættende hovedmåltid til 4.
- Retterne skal være spændende og se forskellige ud: flere køkkener, friske farver, forskellig servering. Ingen ugeplan med fire brune kartoffelretter.
- Indkøbslisten skal vise den vare, retten bruger – aldrig tilbuddets hele gruppetekst ("A, B eller C"). Se `tilbudVariant()` i `index.html`.
- Priser vises ærligt: forbrugspris og indkøbspris er to forskellige tal. Opfind aldrig priser, produkter eller tilbud.

## Arbejdsmåde
- Aldrig direkte på `main` med kode eller data (kontrolløren er den eneste, der må slå dem sammen). Ejer, Kontrollant og Sekretær må skrive deres egne filer i `ai/` direkte på main. Gren: `ai/ÅÅÅÅ-MM-DD-emne`.
- Én lille opgave ad gangen: højst ca. 15 filer. Er opgaven større, så del den i trin i `BACKLOG.md` og tag det første.
- Læs `ai/STATUS.md` og de to seneste rapporter, før du vælger. Gentag ikke noget, der allerede er afvist.
- Kør `python -I scripts/tests/kontrol.py` før og efter. Den skal slutte med `BESTÅET`. Bliver den rød af en ældre fejl, så ret den ikke i samme gren – skriv den i rapporten.
- Bygge-rækkefølge for data er ALTID `byg_retter.py` → `byg_opskrifter.py` (ellers forsvinder `vt`/`ty`, og indkøbslisten viser hele tilbudsgrupper). Læs `scripts/RUTINE.md` før du rører data. Ændrer du biblioteksopskrifter (`scripts/bibliotek_*.py`) eller deres billeder, så kør bagefter `python -I scripts/byg_sider.py` (bygger opskriftssiderne og sitemap til Google, findes når grenen `ai/2026-11-15-opskriftssider` er slået sammen); kontrollen fejler, hvis en opskrift mangler sin side.
- Skriv en ny kontrol i `scripts/tests/kontrol.py`, hver gang du finder eller retter en fejl, der kunne være fanget automatisk.
- Brug `python -I` til Python. Skriv UTF-8 (æøå) og bevar eksisterende linjeskift og indrykning. Brug ikke `\b` i regex med æøå (brug `(?<![a-zæøå])…(?![a-zæøå])`).
- Rør ikke filer uden for opgaven. Ret aldrig i grundloven (se nedenfor) – foreslå det i rapporten.
- Hæv `VERSION` i `sw.js`, når billeder eller gemte filer skiftes (det er klasse H – se ovenfor).

## Klasse A og H (høj risiko)
**A (lav risiko):** tekst, layout/CSS, nye eller ændrede retter/opskrifter, billeder, dokumentation, tests, SEO-metadata.
**H (høj risiko):** priser, mængder, pakker, indkøbsliste, ugeforslagets beregning (`simuler`, `ugePris`, variation), `pris.js`, `kategorier.js`-logik, `sw.js`/cache, `scripts/byg_*.py`, `tilbud.py`, sletning af mere end 5 retter.
Er du i tvivl, er det H. H må slås sammen af kontrolløren, men kun efter den skærpede validering i `ai/agenter/kontrollant.md` (regressionstest, før/efter-tal for alle butikker, rød-hold, tilbagerulning). Der er ingen menneskelig godkendelse bag H; derfor er kontrollen strengere, ikke mildere.

## Grundloven (kan ingen agent ændre)
`ai/regler.md`, `ai/agenter/*`, `.github/`, `auth.js`, `feedback.js`, `privatlivspolitik.html`, nøgler og adgangskoder, og rutinernes egne instrukser. Kontrolløren afviser enhver ændring heri. Mener en agent, at grundloven bør ændres, skriver Ejeren et forslag i sin rapport; Sekretæren sender det til Jonas, som er den eneste, der kan ændre den.

## Ærlighed
- Rapportér det, du IKKE har kunnet tjekke (fx "ikke set i browser"). Skriv aldrig "færdigt", uden at kontrollen er kørt, og citér dens sidste linje.
- Er resultatet usikkert, så sig det. En afvist ændring er bedre end en skjult fejl.
- Gå ikke uden om blokeringer (bot-beskyttelse, adgangskontrol). Tjek-kald bruger den ærlige User-Agent i `scripts/tilbud.py`.
- Ingen persondata, nøgler eller adgangskoder i filer, rapporter eller commits.
