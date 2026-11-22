# Design: "Gode tilbud" – småting efter udgivelsen

Set på siden: `renderListe()` i `index.html` viser hver "Gode tilbud"-gruppe foldet til de første 4 rækker (`EKSTRA_SYNLIGE`) **plus alle afkrydsede**, og en knap `Vis ${skjulte} flere` / `Vis færre` (`.chip.ekstra-flere`, 44 px, fuld bredde, `aria-expanded`, `aria-controls`). Det virker, men ved præcis én skjult række står der "Vis 1 flere", som er forkert dansk. Afkrydsede rækker uden for de første 4 står lige efter de første 4 i gruppens egen rækkefølge, og når gruppen foldes ud, kommer de øvrige rækker ind *mellem* dem – rækken flytter sig, og det ser tilfældigt ud.

## Problemet set fra brugeren
En lille sproglig fejl ("1 flere") og en række, der hopper, når man folder ud, får en ellers rolig side til at virke ugennemtænkt.

## To meget forskellige løsninger
**A. Ret kun teksten og lad rækkefølgen være (valgt):** "Vis 1 mere" ved præcis én skjult række, "Vis N flere" ellers. Afkrydsede rækker bliver stående, hvor de er i gruppens egen rækkefølge; ingen ekstra overskrift.
**B. Afkrydsede varer samles i en lille undergruppe "Valgt" øverst i gruppen**, resten foldet nedenunder. Klart, hvorfor en række står dér, men fordobler overskrifterne i en liste, der skal være rolig, og flytter rækker, når man krydser af.

**Valg: A.** Rækkefølgen er allerede forklaret af knappen ("Vis 5 flere" under de rækker, man kan se); hopperne forsvinder, når foldede og udfoldede rækker holder samme indbyrdes rækkefølge. B er mere maskineri, end en lille ting kræver.

## Detaljer
### Tekst på knappen (ord for ord)
- Lukket, N skjulte rækker: `Vis N flere` for N ≥ 2, `Vis 1 mere` for N = 1. (Aldrig `Vis 0 …` – ved 0 skjulte vises knappen slet ikke, som i dag.)
- Åben: `Vis færre` (uændret).
- `aria-label` er teksten selv; `aria-expanded` skifter som nu.

### Rækkefølge og "ikke tilfældigt"
- Foldet visning = de første 4 rækker i gruppens rækkefølge, derefter de afkrydsede rækker (stadig i gruppens indbyrdes rækkefølge). Det er uændret.
- **Udfoldet visning bevarer de allerede viste rækkers plads:** de viste rækker står først i samme rækkefølge, og de øvrige skjulte rækker kommer efter dem, i gruppens rækkefølge. Ingen række hopper op eller ned, når man trykker "Vis flere" eller "Vis færre". (En række, der er afkrydset uden for de første 4, kan altså stå som nr. 5 i begge visninger.)
- Ingen ekstra overskrift, ingen mærkat. Selve fluebenet og den fremhævede baggrund (`.vare.valgt`) forklarer, hvorfor rækken er med.
- Efter tryk bevares scrollpositionen: knappen står stille under sin gruppe (ingen `scrollTo`); fokus bliver på knappen.

### Mål, farver, animation, tilgængelighed
Uændret: knappen min. 44 px høj, fuld bredde, sekundær stil, tekst `--text-2`, fokusring 2 px `--valgt`; ingen animation; 390–400 px uden vandret scroll. Kontrast ≥ 4,5:1.

### Tilstande
- Gruppe med ≤ 4 rækker: ingen knap. Alle rækker afkrydsede eller alle synlige: ingen knap.
- Tom gruppe / ikke indlæst: vises ikke (som i dag).
- Én skjult række: `Vis 1 mere`. Mange: `Vis N flere`.

## Sådan opfyldes acceptkriterierne
1. **"Vis 1 mere" / "Vis N flere":** teksten vælges ud fra antallet af skjulte rækker; testes for N = 1, 2 og 6.
2. **tilbudsgrupper.js dækker det:** tilføj tests for knaptekst (1, 2, 6 skjulte) og for, at rækkefølgen af viste rækker er den samme foldet og udfoldet; udtræk teksten og rækkefølgen til en lille ren funktion, så den kan testes i node.
3. **Regression og facit uændrede:** kun tekst og rækkefølge i visningen; `prisSum`, `listeLinjer` og afkrydsning røres ikke.

## Indvending til Ejeren
- Accept mangler det, brugeren faktisk ser: at rækker ikke hopper ved fold ud/ind. Forslag: *"(4) rækkerne, der er synlige i den foldede gruppe, står i samme rækkefølge og samme indbyrdes placering i den udfoldede gruppe."*
- Kravet siger "tjek i browseren": holdet kan ikke selv klikke, så det skal være en Chromium-test i `scripts/tests` (afkryds række 7, fold ud, læs rækkefølgen). Forslag: skriv det som accept (5).
- Ikke en indvending, men en bemærkning: [A] er korrekt, så længe tekst og rækkefølge er de eneste ændringer.
