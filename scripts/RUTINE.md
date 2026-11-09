# Daglig opdatering af Madplan (kører automatisk kl. 06 som Claude-rutine i skyen)

Siden madplan-blue.vercel.app viser ugens tilbudsaviser fra 9 butikker (10 kæder) og ca. 50 hjemmelavede retter pr. butik, bygget
ud fra butikkens egne tilbud. Vercel deployer automatisk, når `main` på GitHub opdateres.

## Trin 0 – Skal der gøres noget?
```
python -I scripts/tjek_nyt.py
```
Sidste linje er `NYE: <butikker>` eller `NYE: ingen`. Ved `ingen` → STOP uden at ændre eller committe noget.
Hvis scriptet ikke kan nå Tjek (exit-kode 2 eller fejlbeskeder for alle butikker), så stop og skriv det i din slutrapport.

## Hvilke aviser tages med
Ugeavisen (har et ugenummer i navnet) og alle andre aviser hos butikken, der indeholder MAD, fx Lidls "Fast lav pris i Lidl" (se `find_aviser` i `scripts/tilbud.py`).
Aviser, der aldrig er mad, tages ikke med: nonfood, vin, magasiner, kataloger, legetøj, gaver, elektronik og menuer, Premium-aviser, der kun gentager hovedavisen, og produktkataloger uden tilbud (Salling Princip). Andre aviser skal have mindst 35 % mad i tilbuddene.
Samme vare til samme pris i flere aviser tælles kun én gang. Faste aviser (gyldige længe) er markeret `fast` og tæller ikke med i periode og udløb; kun ugeavisen gør det.
Ændrer en butiks udvalg af aviser sig uden at ugeavisen er ny, flytter alle tilbuds-id'er sig: kør `python -I scripts/remap_ider.py <butik>` efter `tilbud.py`, så retterne flyttes til de nye id'er i stedet for at blive skrevet forfra.

## Trin 1 – Hent de nye aviser (kun de nye butikker)
```
python -I scripts/tilbud.py <butik> [<butik> …] > tilbud.txt
```
Det opdaterer `scripts/tilbud_snapshot.json` for de nævnte butikker og skriver tilbudslisten (id | navn | pris | mængde | beskrivelse).
ID'erne (N1, M1 …) gælder KUN for dette øjebliksbillede. Kør derfor aldrig `tilbud.py` igen for samme butik i samme kørsel
(rækkefølgen er ustabil, og retterne ville pege på forkerte varer). Gør du det alligevel: `git checkout HEAD -- scripts/tilbud_snapshot.json` og start forfra.
Butikker: netto, meny, bilka, rema, kvickly, lidl, 365, spar, minkoebmand. Kvickly og SuperBrugsen er EN samlet butik ("kvickly" = Kvickly / SuperBrugsen): `tilbud.py` beholder kun tilbud, der gælder begge kæder, så `kopier_retter.py` og `retter/superbrugsen.json` er ikke længere i brug (SPAR har en tynd madavis – kvalitet før antal; `udvid_retter.py spar --min-tilbud 0.4`). Kvickly og SuperBrugsen har samme avis (se trin 3).

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
python -I scripts/byg_retter.py                                # validerer og skriver retter.json
python -I scripts/byg_opskrifter.py                            # opdaterer opskrifter.json (opskriftsbiblioteket koblet på ALLE butikkers tilbud – siden vælger selv billigste tilbud pr. ingrediens blandt brugerens butikker)
python -I scripts/byg_tilbudsliste.py                          # opdaterer tilbudsliste.json ("Gode tilbud i dine butikker" nederst på indkøbslisten: sodavand, smør, mælk, vaskemiddel, shampoo … – ikke aftensmad)
python -I scripts/naering/byg_naering.py                       # næringsindhold pr. ret -> naering.json (kategorien Fitness på siden). Kører også automatisk sidst i byg_opskrifter.py
```
`naering.json` (id -> kcal, protein, fedt, kulhydrat pr. portion) bygges ud fra retter.json og opskrifter.json og stemples med retter.json's tidsstempel: siden bruger kun tallene, hvis stemplet passer, ellers vises kategorien Fitness ikke (så gamle tal aldrig sidder på nye retter). Skriv aldrig tal i hånden; nye ingredienser uden opslag står i udskriften fra `scripts/naering/byg_naering.py` og tilføjes i `scripts/naering/tabel.py` (næringsværdier pr. 100 g i `foedevarer.json`, fra USDA FoodData Central – skal på sigt skiftes til DTU's Frida).
`byg_tilbudsliste.py` bygger også de fire grupper nederst på indkøbslisten: Weekenden (slik, sodavand, chips, is/kager), Madpakken (brød, pålæg, ost, frugt), Morgenmad og Frokost – op til 10 pr. gruppe, hver vare kun i én gruppe, uden alkohol (reglerne står i GRUPPER i scripts/byg_tilbudsliste.py).
`byg_opskrifter.py` og `byg_tilbudsliste.py` læser øjebliksbilledet (scripts/tilbud_snapshot.json) og skal altid køres, når aviser er hentet, så forsidens liste ikke bliver forældet. Den sammenligner tilbud med tilbud og kræver ingen tekst fra dig. `"top"` i butikkens json vises ikke længere på siden (feltet må gerne blive stående).
**Håndskrevne retter først (brugerens ønske):** Kør `python -I scripts/genbrug_retter.py <butik> --op-til 45` (evt. `--min-andel 0.5`), som genbruger de håndskrevne opskrifter (scripts/retter_skabeloner.json) med butikkens egne tilbud
som "som"-referencer, FØR du kører udvid_retter.py. Skriv desuden gerne nye håndskrevne retter af de bedste tilbud (fx kød, and, laks, smør, frisk rødkål, appelsiner).
Brug IKKE skiveost i madlavningen – brug en blok ost (cheddar, Danbo, Castello, skæreost) eller revet ost.

**Flest mulige tilbud i brug:** `udvid_retter.py` kan bruge ALLE varer i et tilbud med flere ("Grønlandske rejer, kold- eller varmrøget laks" er både rejer og laks; siden viser den vare, retten bruger), og vælger retter, der bringer tilbud i brug, som ingen valgt ret bruger endnu (`NYE_TILBUD_BONUS`).
En opskrift kan optræde med op til 4 forskellige tilbud som nøgle-ingrediens (højst 1,8 gange så dyrt som det billigste), så en vare med mange tilbud (fx 10 andetilbud) ikke altid bruger det billigste; kun én udgave pr. opskrift vælges (`MAX_VARIANTER`, `VARIANT_PRIS`).
Kør den med `--til 70` for at få op til 70 retter pr. butik: `python -I scripts/udvid_retter.py <butik> … --til 70`. Mangler biblioteket opskrifter til en vare, der ofte er på tilbud, så tilføj en type i `bibliotek_typer.py` og retter i `bibliotek_5.py` (kør derefter `byg_bibliotek4.py`, som skriver billedbeskrivelserne). Tjek altid udskriften: en ny type må ikke ramme ikke-mad (fx det engelske ord "and" i en vinetiket).

**MÅL: HVER BUTIK SKAL HAVE MINDST 50 RETTER hver uge** (tallet står i udskriften: `X eksisterende + Y nye = N`). Opskriftsbiblioteket har 175 opskrifter (bibliotek_1..6). bibliotek_6 er proteinrige retter til kategorien Fitness (kylling, kalkun, torsk, laks, rejer, tun, skyr, hytteost, æg, magert oksekød); nye opskrifter: skriv dem i bibliotek_N.py, tilføj i bibliotek.py og byg_bibliotek4.py, kør byg_bibliotek4.py → byg_opskrifter.py → billeder.py → byg_opskrifter.py. Mængder i 'stk' = hele stykker (rugbrød skrives som 1 'pakke', ikke 8 'stk').

**Kombination:** vælger brugeren flere butikker, vælger siden for hver ingrediens det billigste tilbud blandt dem (lavMixRet). Kategorien Kombination (kategorier.js, kombiInfo) viser retter, der bruger tilbud fra mindst to butikker og enten kun kan laves sådan eller er mindst 5 kr billigere end i den billigste enkeltbutik.
Når en butik ikke når 50 med standardindstillingerne, så prøv i denne rækkefølge (stop, når der er 50):
1. `python -I scripts/udvid_retter.py <butik> --min-tilbud 0.3` (flere retter med færre tilbudsvarer)
2. `... --max-noegle 6` eller 8 (lad ét tilbud, fx kyllingebryst, indgå i flere retter) og `--max-dansk 30` (flere danske retter)
3. Mangler der stadig retter (typisk SPAR og 365discount med tynde aviser): skriv de manglende retter i hånden i `scripts/retter/<butik>.json` ud fra butikkens tilbud (varierede køkkener, hovedingrediens på tilbud) og kør `udvid_retter.py` igen – de håndskrevne retter bevares.
Husk at skrive en engelsk billedbeskrivelse til hver ny ret (`billedprompts.json`), før `billeder.py` køres.

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
