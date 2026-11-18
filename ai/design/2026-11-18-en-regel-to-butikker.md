# Design: Én regel for to butikker (forslaget "Spar X kr ved også at handle i …")

Status på siden i dag: "Ét kort" er rullet tilbage, så main viser stadig logo-gitter, boksen "Hvor mange butikker vil du handle i?" og kortet "Sammenlign butikker" (skærmbillede `mob_1_forside.png`, 390 px). Reglen herunder er ren logik; designet handler om, hvordan forslaget **siges** til brugeren. Det bygges oven på "Ét kort" og samme designfil `2026-11-16-hvor-handler-du-samlet.md` (placering under listen, mål, tokens).

## Problemet set fra brugeren
To steder på forsiden svarer forskelligt på "kan det betale sig at handle i to butikker?": kortet tier stille, mens boksen siger ja. Brugeren ser enten et tilbud om at spare 54 kr eller ingenting, alt efter hvor der kigges, og kan ikke vide, hvilket svar der er sandt.

## To løsningsforslag
**A. Bred sammenligning:** en tabel "1 butik / 2 butikker / 3 butikker" med pris og besparelse for hver. Fuldstændig, men giver tal, brugeren ikke bad om, og gør kortet tungt (stik imod Jonas' ønske om "pænt, simpelt og logisk" og "hele forsiden på én skærm").
**B. Ét ja/nej-forslag (valgt):** kun når reglen siger ja (≥ ANBEFAL_SPAR kr billigere), vises én rolig linje under butikslisten med parrets pris, enkeltbutikkens pris og besparelsen og én knap. Siger reglen nej, vises intet (ingen "det kan ikke betale sig"-støj; boksen "Hvor mange butikker" viser stadig 1 butik).

**Valg: B.** Kravet er netop, at begge steder giver samme svar; derfor kun ét sted og kun ét svar. Fuld ugepris-oversigt findes allerede i rækkerne (hver butiks billigste uge).

## Detaljer (390–400 px; desktop samme rækkefølge, max-bredde som kortet)
Placering: lige under butiksrækkerne, over "Hvor mange butikker". Vises kun med præcis én valgt butik og et billigere par (som i designfilen "Hvor handler du samlet").

```
┌──────────────────────────────────────────┐
│ Spar 54 kr ved også at handle i Netto    │  ← 15 px, fed (600), --text
│ Lidl + Netto: 367 kr · kun Lidl: 421 kr  │  ← 14 px, --text-2
│ Transport og ekstra tid er ikke regnet   │  ← 13 px, --text-3 (kontrast ≥ 4,5:1)
│ med.                                     │
│ [ Tilføj Netto ]                         │  ← knap, min-højde 44 px, fuld bredde på mobil
└──────────────────────────────────────────┘
```
- Boks: `border-radius` og `padding` som øvrige kort (16 px), baggrund `--valgt-tint`, 1 px `--border`; afstand 12 px over og under. Knap: sekundær (kant i `--valgt`, ingen udfyldning) – der er kun ét primært kald pr. skærm ("Brug forslaget").
- **Tekster ord for ord:** "Spar {X} kr ved også at handle i {Butik}" · "{Butik1} + {Butik2}: {P} kr · kun {Butik1}: {E} kr" · "Transport og ekstra tid er ikke regnet med." · knap "Tilføj {Butik}". Står to nye butikker som par (1+2-situationen), skrives "ved at handle i {B1} og {B2}" og knappen "Vælg begge".
- Besparelsen skal være præcis forskellen på de to viste tal (afrundede kr, vist ens begge steder – regn på præcise tal, men vis så den viste forskel passer; er forskellen af afrunding 53,6 → vis tallene og X ud fra de viste, afrundede tal).
- Priser: parrets pris er "indkøbspris for ugen" (7 aftensmåltider, egne tilbud), ikke forbrugspris. Ordet "uge" står i boksen "Hvor mange butikker" ("7 aftensmåltider"), så forbrugspris/indkøbspris ikke blandes.

### Tilstande
- **Nej (under 30 kr):** intet forslag, ingen plads reserveret (ingen hop i layoutet).
- **Indlæser:** reglen kræver to uger regnet; vis ikke boksen før begge er færdige (ingen blinkende halve tal). Boksen fader ind (150 ms opacity); ingen anden animation. Respektér `prefers-reduced-motion`.
- **Fejl/ingen priser:** boksen vises ikke; butiklisten virker stadig (accept (11) i "Ét kort").
- **Parret valgt:** forslaget forsvinder; boksen "Hvor mange butikker" viser "2 butikker" med samme pris som forslaget lovede (accept (2)).
- **Få/mange:** altid kun det ene bedste par (billigste uge blandt dem, der opfylder reglen).

### Tilgængelighed
Boksen er `role="region"` med `aria-label="Forslag: handl i to butikker"`; knappen er en rigtig `<button>`, synligt fokus (2 px `--valgt`), tastatur Enter/Space. Efter tryk flyttes fokus til den nye afkrydsede række, og `aria-live="polite"` melder "Netto tilføjet. 2 butikker, 367 kr."

## Sådan opfyldes acceptkriterierne
1 (kortet viser kombinationen ved ≥ 30 kr, billigste uge): boksen vises kun ved ja, det ene bedste par. 2 (boks og kort er enige): samme funktion og samme tal vises i begge. 3 (tekst): se tekstlinjerne ovenfor – begge priser, besparelse = viste forskel, transport-forbeholdet står der. 4–5 er tests/logik og påvirkes ikke af designet.

## Indvending til Ejeren
- **Afrunding:** accept (1) siger "regnet på præcise tal", accept (3) siger "besparelsen = forskellen på de viste tal". De kan modsige hinanden (fx 53,6 kr bliver "54", mens 421 − 367 = 54, men kan også blive 53). Forslag: *"Tærsklen (≥ ANBEFAL_SPAR) afgøres på præcise tal; de viste tal er hele kroner og besparelsen er forskellen på de viste hele kroner, så brugeren altid kan regne efter."* Giv en automatisk test på 20 tilfældige butikspar.
- **Kravet er en [UX] [H]-opgave uden synlig nyhed**: den bør ikke bygges, før "Ét kort" er genindsendt (runner rettet) – ellers bygges den oven på en rullet-tilbage gren. Sæt rækkefølgen i kravet.
