# Daglig opdatering af Madplan (kører automatisk kl. 06 som Claude-rutine i skyen)

Siden madplan-blue.vercel.app viser ugens tilbudsaviser fra 8 butikker og ca. 50 hjemmelavede retter pr. butik, bygget
ud fra butikkens egne tilbud. Vercel deployer automatisk, når `main` på GitHub opdateres.

## Trin 0 – Skal der gøres noget?
```
python -I scripts/tjek_nyt.py
```
Sidste linje er `NYE: <butikker>` eller `NYE: ingen`. Ved `ingen` → STOP uden at ændre eller committe noget.
Hvis scriptet ikke kan nå Tjek (exit-kode 2 eller fejlbeskeder for alle butikker), så stop og skriv det i din slutrapport.

## Trin 1 – Hent de nye aviser (kun de nye butikker)
```
python -I scripts/tilbud.py <butik> [<butik> …] > tilbud.txt
```
Det opdaterer `scripts/tilbud_snapshot.json` for de nævnte butikker og skriver tilbudslisten (id | navn | pris | mængde | beskrivelse).
ID'erne (N1, M1 …) gælder KUN for dette øjebliksbillede. Kør derfor aldrig `tilbud.py` igen for samme butik i samme kørsel
(rækkefølgen er ustabil, og retterne ville pege på forkerte varer). Gør du det alligevel: `git checkout HEAD -- scripts/tilbud_snapshot.json` og start forfra.
Butikker: netto, meny, bilka, rema, kvickly, superbrugsen, lidl, 365. Kvickly og SuperBrugsen har samme avis (se trin 3).

## Trin 2 – Skriv retter til hver ny butik
Udskift ALLE ikke-auto retter i `scripts/retter/<butik>.json` (de gamle peger på sidste uges id'er og er ugyldige) og opdatér `"avis"`
til det nye katalog-id (står i `tilbud.txt` overskriften) og `"top"` til de 3 bedste tilbud (`{"id": "N7", "hvorfor": "…"}`).
Skriv ca. 30 retter med `"auto"` UDEN (de håndskrevne) – det er dem der giver de bedste, mest tilbudsdrevne retter.
Brug den gamle fil (`git show HEAD:scripts/retter/<butik>.json`) som skabelon til format, tone og niveau, og genbrug opskrifter ved at
pege på de nye id'er. Format: se docstring øverst i `scripts/byg_retter.py`. Hver ret SKAL have `koekken`
(dansk | italiensk | amerikansk | asiatisk | middelhav | vegetar; vegetar-kategorien = vegetar) og `kategori`/`niveau`
(student | familie | weekend). Mængder er til 4 personer. Studentermad højst ca. 35 kr/person.

Regler for retterne (kommer fra brugeren – følg dem):
- Fokus på tilbud, pris og LÆKKER mad. Hovedingrediensen (kød/fisk/grønt) skal være på tilbud i butikkens avis; brug mange tilbudsvarer pr. ret.
- HJEMMELAVET. Ingen ultra-forarbejdede færdigretter (færdige kødboller i karry, lasagne, nuggets, dinner kits, kopsupper, færdige flødekartofler/gratin,
  mortensaftens-menuer osv.). Simple halvfabrikata er OK: rødkål/rødbeder på glas, pesto, pastasauce, pizzadej, bouillon, ketchup/remoulade, konserves,
  frosne grøntsager. Frysepizza/paneret fisk/pommes højst 2 retter pr. butik. `byg_retter.py` håndhæver det.
- Ingen laktosefri/Lactofree, ingen smørbar/margarine/Kærgården/Naturli' – brug rigtigt smør, almindelig mælk, yoghurt naturel (aldrig sød Yoggi i salte retter).
- Retter må gerne gå igen mellem butikker. Tilbudsvarer må ikke være noget andet end det ingrediensen siger (ingen granatæble som æble, ingen marineret kotelet som almindelig kotelet,
  ingen ikke-mad som vin, kosmetik, legetøj).
- Kun varer fra denne butiks egen avis i tilbuds-id'erne.
- Min. 4 retter i hvert køkken pr. butik hvis avisen overhovedet giver mulighed for det (4-5 er målet).

## Trin 3 – Udvid til 50 og byg
```
python -I scripts/udvid_retter.py <butik> [<butik> …]          # fylder op til 50 fra scripts/bibliotek_*.py; tilføj --min-tilbud 0.4 for butikker med tynd avis
python -I scripts/kopier_retter.py kvickly superbrugsen        # KUN når Kvickly er ny – kopierer til SuperBrugsen (samme avis). Gør det efter at kvickly.json er færdig.
python -I scripts/byg_retter.py                                # validerer og skriver retter.json
python -I scripts/byg_opskrifter.py                            # opdaterer opskrifter.json (opskriftsbiblioteket koblet på ALLE butikkers tilbud – siden vælger selv billigste tilbud pr. ingrediens blandt brugerens butikker)
python -I scripts/byg_tilbudsliste.py                          # opdaterer tilbudsliste.json ("Gode tilbud i dine butikker" nederst på indkøbslisten: sodavand, smør, mælk, vaskemiddel, shampoo … – ikke aftensmad)
```
`byg_opskrifter.py` og `byg_tilbudsliste.py` læser øjebliksbilledet (scripts/tilbud_snapshot.json) og skal altid køres, når aviser er hentet, så forsidens liste ikke bliver forældet. Den sammenligner tilbud med tilbud og kræver ingen tekst fra dig. `"top"` i butikkens json vises ikke længere på siden (feltet må gerne blive stående).
`udvid_retter.py` udskriver for hver ny auto-ret hvilket tilbud hver ingrediens er koblet til. GENNEMGÅ listen: hvert tilbud skal give mening i retten.
Findes en fejlkobling (fx andebryst som kyllingebryst), så ret regexen i `scripts/bibliotek_typer.py` (brug `(?<![a-zæøå])…(?![a-zæøå])` – `\b` virker ikke med æøå)
eller `IKKE_MAD` i `udvid_retter.py`, og kør igen. Tynde aviser (Kvickly/SuperBrugsen/Lidl) når måske ikke 50 – kvalitet er vigtigere end antal.

**Billeder (valgfrit trin, kun hvis miljøvariablen `CLOUDFLARE_API_TOKEN` findes):** Billedmodellen forstår ikke danske retnavne, så hver ret skal have en kort ENGELSK beskrivelse af, hvordan den færdige ret ser ud på tallerkenen
(fx "Danish stewed white cabbage in a creamy white sauce, served with fried brown medister sausage slices and boiled potatoes"). Skriv beskrivelsen til hver NY ret i `scripts/billedprompts.json` (nøgle = rettens præcise navn) – scriptet advarer om retter uden. Kør derefter `python -I scripts/billeder.py` FØR `byg_retter.py`. `--forfra` laver alle billeder om. Den laver et illustrationsbillede til hver ny ret
(Cloudflare Workers AI, Flux Schnell, gratis daglig grænse), gemmer det i `billeder/` (ca. 60 KB pr. stk.) og springer retter over, der allerede har et. Når den daglige gratis grænse er nået, stopper den
uden fejl – resten tages næste dag. Findes nøglen ikke (eller kan `api.cloudflare.com` ikke nås), så spring trinnet over; retter uden billede viser et køkkenikon. `byg_retter.py` sætter selv feltet `billede`. `billeder.py` laver også billeder til biblioteksopskrifterne i `opskrifter.json` (de kan vælges i madplanen) – kør det FØR `byg_opskrifter.py`, som sætter `billede`, når filen findes. Alle 74 opskrifter har billede; en ret uden billede vises med et køkkenikon.
Husk at committe de nye filer i `billeder/`.

`byg_retter.py` skal slutte uden linjen `FEJL:`. Ved FEJL skrives `retter.json` ikke. Ret retterne og kør igen. Gennemse ADVARSLER og REST-TIP,
og ret de enkle (studentermad over loftet → niveau `familie`). Antal retter og køkkenfordeling står i udskriften pr. butik.

## Trin 4 – Udgiv
Kun hvis byggeren gik rent igennem (ingen FEJL) og `retter.json` er skrevet:
```
git add -A
git commit -m "Nye tilbudsaviser: <butikker> (uge <nr>)"
git push origin main
```
Rør aldrig andet end madplan-repoet. Slet midlertidige filer (tilbud.txt m.m.) før commit. Hvis noget går galt, så lad `main` være uændret og beskriv fejlen.

## Slutrapport (kort, på dansk)
Hvilke butikker havde ny avis, hvor mange retter pr. butik, køkkenfordeling, evt. advarsler, om der blev pushet — eller hvorfor ikke.
