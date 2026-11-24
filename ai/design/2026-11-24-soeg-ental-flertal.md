# Design: Søg i "Vælg selv" – ental/flertal og småfejl

Krav: `[UX] [A] Søg i "Vælg selv": ental/flertal og småfejl` (Ejer 2026-11-23). Bygger oven på `2026-11-22-soeg-vaelg-selv.md` (felt, tekster, tilstande uændrede). Her designes kun, hvordan søgningen *opfører sig* for brugeren, og de to ting kontrollanten fandt afvist (forsøg 1, `ai/rapporter/2026-11-23-kontrol.md`).

## Set på siden
`soegRetter()` i `index.html` (ca. linje 2339) søger først på den skrevne form (fra 4 tegn også inde i sammensatte ord, under 4 tegn kun ordstart). Findes ingen træffere, prøver den en kort liste over uregelmæssige flertal og at fjerne -ne/-er/-e/-r. Resultatet er ujævnt: i Nettos retter giver "kartoffel" 2 retter, "kartofler" 21; "gulerod" 0, "gulerødder" 6; "løgene" 0, "løg" 16. Brugeren tror, der kun er 2 kartoffelretter. Søgefeltet, resultatlinjen og tom-tilstanden virker fint. Der er stadig tre "Din uge"-forekomster i koden (ét i den sammenfoldede visning ved søgning, ét ellers); brugeren må kun se én overskrift ad gangen.

## Problemet set fra brugeren
"Jeg skrev 'kartoffel' og fik to retter – så skrev jeg 'kartofler' og fik enogtyve. Hvorfor? Er søgningen i stykker?" Ental og flertal skal give det samme; og jeg må heller ikke få mærkelige træffere ("hvide bønner" må ikke vise chili con carne).

## To meget forskellige løsninger
**A. Fælles stamme på begge sider, men kun som tillæg til den eksisterende søgning (valgt).** Alt, som søgningen finder i dag, findes stadig (aldrig færre træffere end nu). Oven i det tæller et ord som træffer, hvis søgeordets stamme er lig stammen af et *helt* ord i retten. Små, eksplicitte regler; ingen ordliste over ingredienser.
**B. Fuzzy/"ligner"-søgning** (ordafstand, f.eks. 1 tegns forskel): fanger også tastefejl ("kyllng"), men giver uforudsigelige træffere ("ost"/"rost"), er svær at teste og forklare, og kravet udelukker stavefejlstolerance.

**Valg: A.** Forudsigeligt, testbart, og den rammer præcis det, brugerne skriver (ental ↔ flertal). Tidligere forsøg faldt, fordi stammen *erstattede* den rå søgning; her er den kun et supplement, og stammen sammenlignes kun på hele ord.

## Regel (det, udvikleren bygger)
Normaliser som i dag (små bogstaver, accenter væk, opdel i ord på alt andet end a–z, æ, ø, å, 0–9). For hvert søgeord `s` og hvert ord `w` i retten (navn + ingredienser):

1. **Som i dag (uændret, kører først):** `s.length >= 4` → `w` indeholder `s`; ellers `w` begynder med `s`. Træffer det, er ordet fundet. Det sikrer "rejer" → "kutterrejer" og "olie" → "olivenolie".
2. **Tillæg – samme stamme:** ordet er også fundet, hvis `stamme(s) == stamme(w)` (hele ord, ikke "indeholder").
3. `stamme(x)`:
   - først en lille fast tabel over uregelmæssige flertal, der giver ental: kartofler→kartoffel, gulerødder→gulerod, tomater→tomat, æbler→æble, bønner→bønne, løg/løgene→løg. Tabellen må udvides, når nye ord dukker op, men skal være kort;
   - ellers fjern *én* endelse fra listen `erne, ene, er, en` hvis der er mindst **3** tegn tilbage, eller `e, r` hvis der er mindst **5** tegn tilbage;
   - ellers ordet uændret.
   Mindstelængderne er med vilje: "hvide" (→ "hvid", kun 4) og "sorte" (→ "sort") stammes ikke og kan derfor ikke ramme "hvidløg"/"sort peber"; "rejer" findes via trin 1.
4. Ordstart for ord under 4 tegn gælder stadig ("ris" finder ikke "tomatris", "ost" ikke "rost"). Stamme-sammenligningen er hele-ord, så den kan aldrig finde midt i ord.
5. Alle søgeord skal passe (som i dag). Stammerne anvendes på **begge** sider på samme måde, så reglen er symmetrisk: "kartoffel" ↔ "kartofler", "tomat" ↔ "tomater", "løg" ↔ "løgene", "gulerod" ↔ "gulerødder".

Forventede tal (prøvet på Nettos 60 retter): kartoffel = kartofler = 21; gulerod = gulerødder = 6; tomat = tomater = 20; løg = løgene = 16; rejer = reje = 4 (uændret); "hvide" 0 og "ris" 10 (uændret); olie 33 (uændret).

**Sammensatte ord (beslutning, som den anden AI bad om):** et søgeord på mindst 4 tegn finder også ordet som begyndelse eller midte af et sammensat ord ("kartoffel" → "kartoffelmos"; "laks" → "røgetlaksefilet"), som i dag. Under 4 tegn kun ordstart. Det skal stå i rapporten.

## Hvad brugeren ser
Ingen ny knap, tekst eller farve. Det eneste synlige: ental og flertal giver samme antal i resultatlinjen (`21 retter passer til "kartoffel" – søgt i alle retter`). Resultatlinjen viser det, brugeren skrev (ikke stammen), så de ikke undrer sig. Ingen "vis også"-forslag, ingen rettelse af stavning.

### "Din uge"-overskrift (kun én)
Mens der søges, vises kun den sammenfoldede linje `Din uge · 7 af 7 dage ▾` (44 px, som i designet af 2026-11-22). Den fulde `Din uge`-overskrift inde i det foldede indhold skjules, mens det er lukket, og vises *uden* en ekstra overskrift over sig, når det er foldet ud (linjen er overskriften). Uden søgning: den fulde overskrift som i dag. I Chromium må der på intet tidspunkt være to synlige "Din uge"-overskrifter (390, 360 og 1280 px; lyst og mørkt tema).

### Tilstande
- Tom søgning: hele listen (uændret). Ét tegn: filtrerer ved ordstart.
- 0 træffere: tom-tilstanden fra 2022-11-22-designet (`Ingen retter passer til "…"`, `Prøv et kortere ord, eller tjek stavningen.`, knappen `Vis alle retter`).
- Ingen indlæsningstilstand (data er lokale). Ingen animation.
- Tilgængelighed: uændret (label "Søg i retter", `aria-live="polite"` på resultatlinjen, ryd-knap 44 × 44 px, fokusring `--valgt`).

## Acceptkriterier – hvordan hvert opfyldes
1. Ental = flertal og "ingen falske træffere": trin 2–3 ovenfor; test mindst kartoffel/kartofler, gulerod/gulerødder, løg/løgene, tomat/tomater med forventet *lige* antal, og negative tilfælde: "hvide bønner" må ikke ramme retter uden hvide bønner, "sorte" ikke "sort peber", "ris" ikke "tomatris".
2. "ris"/"ost" ikke midt i ord: trin 1 og 4 uændret.
3. Én "Din uge"-overskrift: se afsnittet ovenfor; måles i Chromium på tre bredder.
4. Søgetesten kører med Python-Playwright (som de øvrige Chromium-tests) og består i `kontrol.py`.
5. Uændret beregning: kun den rene visningsfunktion `soegRetter` ændres; `state.valgte`, `plan`, priser og listen røres ikke.
6. (Foreslået tillæg) "Aldrig færre træffere end i dag": test over alle ord i retterne for alle 9 butikker, at ethvert søgeord, der gav træffere før, giver mindst de samme nu.

## Indvending til Ejeren
- **Accept (1) er selvmodsigende uden et præcist mål:** "samme antal for mindst to andre par" *og* "ingen falske træffere" kan ikke begge afprøves, før man siger, hvad "falsk" er. Forslag: "Et ord, der gav træffere før, giver mindst de samme nu (ingen tabte retter), og de nye træffere er kun retter, hvor søgeordet og et helt ord i retten har samme stamme." Så er det målbart (se punkt 6).
- **Accept (1) nævner "løg"/"løgene" som negativt eksempel,** men "løgene" er netop et flertal, der skal finde "løg". Det negative eksempel skal være "ris"/"tomatris", ikke løg.
- **Stavefejl** er stadig udenfor; det er rigtigt. Brugerne får tom-tilstandens hjælpetekst.
- Småpunktet "finger/fingre" rammer ingen ret i dag: lad være at bygge det, før en ret med fingre findes.
