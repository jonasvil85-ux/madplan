# Design: Gemte madplaner og favoritter (ROADMAP 5)

## Problemet set fra brugeren
Hver uge starter forfra: en plan, man var glad for, forsvinder, når tilbuddene skifter, og retter familien elsker, kommer kun tilbage ved tilfældighed. Siden gemmer i dag kun den aktuelle plan (`localStorage`-nøglen `GEM`). Der er ingen måde at sige "den her ret er vores".

## To meget forskellige løsninger
**A. Gem hele ugen som en navngivet plan:** "Gem denne uge", en liste "Dine planer" og stjerner på retter. Mange skærme, og en gemt plans pris ville være forældet i næste uge (i strid med ærlige priser).
**B. Hjerte på retten og "Dine favoritter" som genvej (valgt):** den vigtigste handling er at markere en ret. En gemt uge er blot retterne, uden priser; priser regnes altid frisk. Næsten ingen ny skærm.

**Valg: B**, med en genvej, der markerer hele ugens retter. Det opfylder kravets formål (grund til at komme igen) uden gemte, forældede priser.

## Detaljer
### Hjertet på retkortet (mobil 400 px og desktop)
- Hjerte, 22 px, øverst til højre på retbilledet (dagkort og retoversigt), tryk-flade **44 × 44 px** (usynlig `::after`), 8 px fra kanten; overlapper ikke "Byt"/"Fjern" under billedet.
- Tomt: kontur 1,5 px i hvid på en halvgennemsigtig mørk cirkel (`rgba(0,0,0,.35)`), så det kan ses på billeder. Valgt: udfyldt `--valgt`.
- `aria-label`: "Gem [retnavn] som favorit" / "Fjern [retnavn] fra favoritter"; `aria-pressed`.
- Animation: valgt hjerte 1 → 1,15 → 1 på 160 ms; slået fra ved `prefers-reduced-motion`.
- Første gang: kort besked (3 s, `role="status"`, over installér-bandet): "Gemt. Dine favoritter bliver oftere foreslået."

### "Dine favoritter"
- Placering: under ugens retter, over "Vælg selv". Overskrift "Dine favoritter (3)". Vises kun med mindst én favorit.
- Mobil: vandret række (egen scroll-beholder, ikke siden), kort 140 px brede med billede, retnavn (højst to linjer) og "Tilføj" (≥ 44 px), der lægger retten på en tom dag. Desktop: gitter, tre pr. række.
- Ret uden tilbud i den valgte butik denne uge: nedtonet (55 %), teksten "Ikke på tilbud i [butik] denne uge", stadig tilføjelig; prisen er en estimeret normalpris, mærket som resten af siden.

### Oftere foreslået
Favoritter vægtes op i ugeforslaget, højst to af syv dage, så ugen forbliver varieret. Linje under forslaget, når en favorit er med: "Med i ugen: dine favoritter [navn] og [navn]". Det rører ugeforslagets beregning (klasse H, se indvending).

### Genvej
Sekundær knap (44 px) under ugens retter: "Gem ugens retter som favoritter". Bekræfter: "7 retter gemt som favoritter" (færre hvis nogle allerede var favoritter). Ingen priser gemmes.

### Uden og med konto
- Uden konto: lokalt (`localStorage`, ny nøgle). Under favoritterne, én gang: "Gemt på denne enhed. Log ind for at have dem på alle dine enheder." med den eksisterende "Log ind"-knap (44 px). `auth.js` røres ikke.
- Med konto: samme visning uden hint; synkronisering kun hvis den kan ske uden ændring af `auth.js` (ellers trin 2).

### Tilstande
- **Tom:** sektionen vises ikke. Første gang et lille tip ved første hjerte: "Tryk på hjertet for at gemme en ret" (forsvinder ved første tryk).
- **Indlæser:** tre grå skelet-kort.
- **Fejl** (kan ikke gemme, fx privat tilstand): "Kunne ikke gemme. Prøv igen, eller log ind." – hjertet vender tilbage til tomt.
- **Få (1–2):** kun dem, ingen tomme pladser.
- **Mange (> 12):** de 12 nyeste og "Se alle (N)" (44 px), som åbner en bund-skuffe, hvor man også fjerner favoritter.
- **Fjern:** udfyldt hjerte trykkes → "Fjernet. Fortryd" i 4 s.

### Farver og tilgængelighed
Tokens: `--valgt` (hjerte, "Tilføj"), `--surface`/`--surface-2`, `--text-1/2/3`, `--border`. Ingen nye farver. Hjertet er en `button` med `aria-pressed`; fokus `:focus-visible` 2 px `--valgt`; betydningen bæres også af form (fyldt/kontur), ikke kun farve; tekstkontrast ≥ 4,5:1; "Fortryd" kan nås med tastatur.

## Sådan opfyldes acceptkriterierne
1. **Gem/åbn madplan:** genvejen gemmer ugens retter; "Dine favoritter" åbner dem og lægger dem i en frisk plan (se indvending).
2. **Favoritstjerne på retkort:** et hjerte (stjerner læses som karakterer) på dagkort og retoversigt.
3. **Uden konto lokalt:** ja, med hint om at logge ind.
4. **Rører ikke auth.js:** ja.

## Indvending til Ejeren
- **"Gem madplan" strider mod ærlige priser:** en gemt plan har forældede priser. Omformulér accept (1): "retterne i en uge kan gemmes og lægges i en ny uge; priser regnes altid frisk".
- **"Favoritstjerne" → "hjerte"** i accept (2), eller tillad begge.
- **"Forslået oftere" ændrer ugeforslagets beregning (klasse H), men kravet er [A].** Del i (a) [UX][A] gem og vis favoritter og (b) [UX][H] vægt favoritter (højst 2 af 7 dage, regression og før/efter-tal for 9 butikker). Ellers afviser kontrollanten (a).
- **Kontosynkronisering** kræver sandsynligvis nyt felt i Supabase (sikkerhedsvurdering). Tag lokal lagring først, konto som trin 2.
