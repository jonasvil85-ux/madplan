# Design: Mobil – tryk-flader og luft (ROADMAP 2)

## Problemet set fra brugeren
I butikken bruger man siden med én hånd og tommelfingeren. Skærmbillederne (390 px) og `BROWSER.md` viser 33 tryk-flader under 40 px: "Byt/Fjern" på dagskortene, butiksfelterne (36–38 px), faner, "Fravælg alle", liste-ikonet, "Alle opskrifter" m.fl. Det giver forkerte tryk. Billederne er desuden tunge: `madplan-hero.png` er 405 KB (kravets punkt 4: ingen over 160 KB).

## To meget forskellige løsninger
**A. Gør alt større:** hæv hver enkelt knap til 44 px med større padding. Enkelt, men forsiden bliver længere, og dagkortene fyldes af store knapper oven på billederne.
**B. Usynlig tryk-zone (valgt):** knappen *ser* ud som i dag (rolig side), men får en tryk-flade på mindst 44 × 44 px via `min-height`/`min-width` og et usynligt `::after`-område. Kun hvor elementerne står tæt (butiksfelter, chips), vokser selve feltet. Siden holder sit rolige udtryk, og trykkene rammer rigtigt.

**Valg: B**, fordi forsiden allerede er lang, og billederne er sidens blikfang. Den visuelle støj må ikke vokse.

## Detaljer (mobil 400 px, `max-width: 600px`)
Fælles regel: alle `button`, `a.knap`, `.chip`, `.byt-knap`, `.ing-knap`, faner og ikon-knapper: `min-height: 44px; min-width: 44px`. Mellem to nabo-flader mindst 8 px luft (`gap: 8px`).

| Element | I dag | Nyt |
|---|---|---|
| Butiksfelter `.butik-chip` | 36–38 px høje, gap 6 | **44 px** høje, gap 8. Fire pr. række (som nu); 9 butikker = 3 rækker |
| `.byt-knap` (Byt / Fjern) på dagskort | ca. 27 × 21 | Udseende uændret (lille pille med ikon + ord), men usynlig tryk-zone `::after { inset: -12px -6px }` → mindst 44 px høj; knapperne i et kort har 8 px mellem tryk-zonerne (flyt dem til `gap: 8px`, eller stabl dem lodret hvis de ellers overlapper) |
| Liste-ikonet (ingredienser) på dagkort | 22 px | 44 × 44 tryk-zone, ikonet bliver 22 px |
| Faner "1. Butik … 5. Seddel" | ca. 40 px | 44 px høje |
| Chips (kategorier, køkkener, kost) | 34 px | 44 px høje (`padding: 11px 14px`), 8 px gap; sidescroll i rækken må gerne bevares |
| "Fravælg alle", "Alle opskrifter", Log ind / Opret bruger | 30–36 px | 44 px høje |
| Husstandsknappen (👥 4) | ca. 32 px | 44 px høj |
| Afkrydsning på indkøbslisten | 22 px boks | boksen 24 px, hele rækken er tryk-flade ≥ 44 px (se kravet "Indkøbsliste: tydelige rækker") |

Farver: uændrede tokens (`--valgt`, `--valgt-tint`, `--border`, `--surface-2`). Ingen nye farver.
Desktop (>600 px): uændret; reglen gælder kun under 600 px og for `(pointer: coarse)`, så musebrugere ikke får en klodset side.

## Billeder (kravets punkt 4 og 5)
- Ingen billeder over 160 KB: `madplan-hero.png` (405 KB) og `og-image.jpg` (155 KB, ok) tjekkes; hero konverteres til `.jpg`/`.webp` ved ca. 1200 px bredde, kvalitet ≈ 78, under 160 KB. Sidens udseende må ikke ændre sig synligt.
- Alle `<img>` har `alt` (i dag 0 uden alt ifølge Browser-QA – behold det; nye billeder får dansk alt-tekst, dekorative `alt=""`).
- `sw.js`-`VERSION` hæves, når billeder skiftes (klasse H – se `regler.md`).

## Tilstande
- **Hover** (kun `(hover: hover)`): som i dag. **Fokus:** `:focus-visible` med 2 px kant i `--valgt`, `outline-offset: 2px`, aldrig `outline: none` uden erstatning. **Tryk:** `transform: scale(.97)` i 80 ms (hjælper brugeren at mærke trykket). **Deaktiveret:** 45 % opacitet, `cursor: not-allowed`.
- Ingen nye tekster. Eksisterende danske tekster beholdes uændret.

## Tilgængelighed
Kontrast mindst 4,5:1 for tekst på knapper (tokens er allerede valgt for det). Ikon-knapper har `aria-label` på dansk ("Byt mandags ret", "Fjern mandags ret", "Vis ingredienser"). Tastatur: Tab-rækkefølge uændret.

## Sådan opfyldes acceptkriterierne
1. **0 elementer under 40 px på 390 px** – alle flader ≥ 44 px (udviklingen verificeres med Browser-QA's måling; tekstlinks i brødtekst undtaget).
2. **Intet vandret scroll på 360 px** – butiksfelter bruger `minmax(0,1fr)`; chip-rækker, der er bredere, scroller i deres egen beholder, ikke på siden. Tjek 360 px.
3. **Designfil med før/efter** – tabellen ovenfor er "før/efter"; udvikleren vedlægger Browser-QA's tal før og efter.
4. **Billeder ≤ 160 KB**, 5. **alt på alle billeder** – se afsnittet Billeder.
6. **Designfilen findes før udvikling** – denne fil.

## Indvending til Ejeren
- Punkt 4 (billedstørrelse) og tryk-flader er to uafhængige opgaver. Den ene er klasse A (CSS), den anden berører cachen (H pga. `sw.js`). Del dem i to grene, så en cache-fejl ikke blokerer tryk-fladerne, der var afvist én gang allerede. **Forslag:** behold punkt 1–3 og 5 i dette krav, og flyt 4 til et eget [UX][H]-krav.
- Punkt 1 siger "under 40 px", men målet er 44 px. Skriv "under 44 px (undtagen tekstlinks i brødtekst)", ellers kan 40–43 px slippe igennem.
