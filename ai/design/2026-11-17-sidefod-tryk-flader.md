# Design: Mobil – "Om Måltidsjagten" og sidefod som tryk-flader

## Problemet set fra brugeren
Nederst på siden står fire små, næsten usynlige ord: "Om Måltidsjagten" (95 × 14 px), "Rundvisning", "Installér som app" og "Privatlivspolitik". De er 11,5 px store, står med 60–70 % opacitet (`.fod { opacity: .6 }`, senere `.7`) og ligger tæt. På telefon er de svære at ramme og svære at læse. "Om Måltidsjagten" åbner et `<details>` med den ærlige uafhængighedserklæring, som er vigtig for tilliden (`index.html` ca. linje 324–358 og 902).

## To meget forskellige løsninger
**A. Fire store knapper i et 2 × 2-gitter:** hver med kant og 44 px højde. Tydeligt, men en sjældent brugt sidefod bliver en tung blok, der konkurrerer med indholdet.
**B. Rolig lodret liste (valgt):** hver handling er en fuld-bredde række uden kant, 48 px høj, adskilt af en tynd linje, med et lille ikon til højre. Samme rolige udtryk som i dag, men hele rækken er tryk-flade, og disclaimeren folder ud på stedet.

**Valg: B.** En liste ligner indstillingsskærme, som folk kender fra telefonen, og er nem at ramme med tommelfingeren uden at gøre sidefoden dominerende.

## Detaljer
### Mobil (≤ 600 px, 390–400 px bredde)
Rækkefølge oppefra:
1. **Om Måltidsjagten** (`summary`) – folder teksten ud. Til højre `+` (lukket) / `–` (åben), 18 px, `--text-3`.
2. **Rundvisning** (knap).
3. **Installér som app** (knap, kun når `#installer` ikke er `hidden`).
4. **Privatlivspolitik** (link, ikon `›`).

Mål:
- Hver række: `min-height: 48px`, `display: flex; align-items: center; justify-content: space-between; width: 100%`. Ingen række under 44 px.
- Rækkerne er adskilt af `1px solid var(--border)` uden mellemrum, så trykzonerne ikke overlapper.
- Luft over sidefoden som i dag (`margin-top: 40px`); under: `max(24px, env(safe-area-inset-bottom))`.
- Tekst 15 px (op fra 11,5), `line-height: 1.4`, `color: var(--text-2)`. **Opacity fjernes.** Kontrast mod baggrunden mindst 4,5:1 (tokens opfylder det i begge temaer); `--text-3` kun til ikonet.
- Åben tilstand: teksten under rækken, `padding: 4px 0 16px`, 14 px, `max-width: 70ch`, `line-height: 1.5`.
- På mobil skifter `.fod` fra `display:flex; flex-wrap:wrap` til `display:block`.

### Desktop (> 600 px)
Samme rækkefølge på én linje, 13 px, uden opacity, med `padding: 12px 0` omkring hvert ord, så musen ikke skal ramme 14 px høje ord.

### Farver
Kun eksisterende tokens: `--text-2`, `--text-3`, `--border`. Ingen accent (sidefoden skal ikke trække øjnene).

### Tekster (uændrede, ord for ord)
- "Om Måltidsjagten"
- "Måltidsjagten er et uafhængigt projekt og er ikke tilknyttet Netto, MENY, Bilka, REMA 1000, Kvickly, SuperBrugsen, Lidl, 365discount, SPAR eller Min Købmand. Tilbud er fra butikkernes offentlige tilbudsaviser. Priser er vejledende og kan afvige i den enkelte butik. Priser på varer uden tilbud er estimerede normalpriser."
- "Rundvisning", "Installér som app", "Privatlivspolitik"

### Tilstande
- Lukket/åben: `+` ↔ `–`; `details` giver `aria-expanded` gratis.
- "Installér som app" findes kun, når browseren kan installere (som i dag).
- Hover (kun `(hover: hover)`): understregning som nu. Tryk: baggrund `var(--valgt-tint)` i 120 ms. Fokus: `:focus-visible` 2 px kant i `--valgt`, `outline-offset: -2px`. Ingen højde-animation.
- Tom/fejl/indlæser: ikke relevant (statisk indhold).

### Tilgængelighed
Tab-rækkefølge som ovenfor; Enter/Space folder "Om" ud; synligt fokus; ikoner `aria-hidden`; tekst 15 px, kontrast ≥ 4,5:1.

## Sådan opfyldes acceptkriterierne
1. **Ingen sidefodslinks under 40 px** – alle rækker ≥ 48 px; sidefodens elementer må ikke længere optræde på Browser-QA's liste.
2. **390 px uden vandret scroll** – rækkerne er `width: 100%`, teksten ombrydes, ingen faste bredder.
3. **Færre små tryk-flader end 23** – sidefoden fjerner sine egne elementer fra listen (se indvending om at skærpe kriteriet).

## Indvending til Ejeren
- Accept (3) ("færre end 23") er for svagt: kravet kan opfyldes ved at fjerne ét element. Formulér det: **"ingen sidefodselement er under 44 px på 390 px"**, og kræv en automatisk Chromium-test af `.fod`-elementernes højde.
- Kravet siger "mindst 44 px", accept (1) siger "under 40 px". Brug 44 px begge steder, ellers kan 40–43 px slippe igennem (samme indvending som i designfilen om tryk-flader).
- Opacity på `.fod` fjernes af kontrastgrunde. Det er en lille visuel ændring uden for ordlyden; skriv den ind i kravet, så kontrollanten ikke ser det som uden for opgaven.
