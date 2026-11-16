# Design: Sammenlign alle butikker på forsiden (CTO-prioritet 1)

## Hvad jeg har set
Kilde: `index.html` (`butikPanel()`, `antalValgHtml()`, `simFraButikker()`) og skærmbilledet `mob_1_forside.png` (Browser-QA 2026-11-16, 390 px, lyst tema). Kortet "Hvor handler du?" er en tæt gruppe af 9 små logo-chips (4+4+1 på mobil) med et flueben på den valgte, og under den kortet "Hvor mange butikker vil du handle i?" med én pris (fx ~~817 kr~~ **421 kr**, Lidl). Det virker: logoerne er genkendelige, og én pris er let at forstå. Det forvirrer: logoerne står uden tal, så man kan ikke se, om Lidl er billigere end Netto – det kræver 9 tryk og at huske tallene. Den niende chip (Min Købmand) hænger alene på en tredje række. Hint-teksten om "flere butikker" er det eneste, der antyder, at kombinationer findes.

## Problemet set fra brugeren
"Hvor skal jeg handle i denne uge, og hvad sparer jeg?" Svaret ligger skjult bag 9 tryk. Brugeren i entréen med telefonen vil have en liste: billigst øverst, ét tryk, færdig.

## To meget forskellige løsninger
**A. Rangeret liste (rækker):** erstatter chip-gitteret med 9 rækker, billigst først. Hver række: logo, navn, ugepris, besparelse. Let at skimme og sammenligne lodret; hele rækken er én stor tryk-flade. Koster højde (9 × 56 px ≈ 500 px), så madplanen skubbes ned.
**B. Søjlediagram med logoer:** 9 vandrette søjler med længde efter pris. Visuelt slående, men prisforskelle mellem butikker er ofte kun 5–15 %, så søjlerne ligner hinanden og lover mere forskel, end der er; svært at læse tal på 390 px; unødigt "diagram" til 9 tal.

## Valg: A, med de 3 billigste synlige og resten foldet ud
Begrundelse: tal i en liste er ærligere og hurtigere at læse end søjler. Højden løses ved at vise **de 3 billigste** og en knap "Vis alle 9 butikker" (44 px). Accept (1) kræver alle 9 – de er der, blot foldet; på desktop (≥ 900 px) vises alle 9 uden fold. Chip-gitteret bevares som kompakt butikvalg (se nedenfor), så ingen nuværende vej ændres for dem, der ikke bruger listen.

## Placering og rækkefølge
**Mobil (390–400 px)**, trin 1 "Butik":
1. Kort "Hvor handler du?" – **uændret øverst**: chip-gitteret (valg af butikker) og "Hvor mange butikker …"-kortet, uændret.
2. **Nyt kort direkte under:** `Sammenlign butikker` (h2, 20 px/700 som øvrige kort-overskrifter) + undertekst (13 px, `--text-3`): "Ugens madplan til din husstand, regnet butik for butik."
3. Liste: 3 rækker (billigst først) + knap `Vis alle 9 butikker` / `Vis færre`.
4. Under listen (kun hvis sandt): kombinationslinjen (se nedenfor).
5. Madplan-kortet som i dag.

**Desktop (≥ 900 px):** kortet ligger under butikvalget i fuld bredde (max 1100 px, som siden). Rækkerne i et 3 × 3-gitter *sorteret billigst først læst række for række* – hvert felt er en række som på mobil. Alle 9 vises, ingen fold.

## Rækken (hver butik)
Mobil, højde 64 px (min. 56 px), `padding: 8px 12px`, `border: 1px solid var(--border)`, `border-radius: 12px`, afstand mellem rækker 8 px, hele rækken er en `<button>` (≥ 44 px høj, 100 % bred):
```
[#1] [logo 54×32]  Lidl                      421 kr
                   Spar 396 kr · 62 % på tilbud
```
- Venstre: rang-tal "1", "2" … (14 px, `--text-3`, 20 px bred) og logoet i `.butikhoved.lille`-størrelsen (54 × 32 px, som i dag).
- Midten: butiksnavn (16 px/600, `--text-1`). Under: besparelsen og andelen (13 px, `--text-3`): "Sparer 396 kr · 62 % på tilbud". Hvor "sparer" er normalpris minus indkøbspris – samme to tal som siden i dag viser som ~~817 kr~~ **421 kr**.
- Højre: **ugens indkøbspris** (18 px/700, `--text-1`, tabulære tal: `font-variant-numeric: tabular-nums`, højrestillet). Mærkaten "Ugens indkøb" er med i `aria-label`, ikke i synlig tekst, for ro. Forbrugspris vises ikke her (to tal i en liste forvirrer); den står stadig i madplanen. Rækken må ikke blande de to tal.
- **"Billigst"-mærke:** på rang 1: lille pille foran prisen, `background: var(--sek-lys)`, tekst `--sek-dk`, 12px/600, "Billigst". Kun én rækkes mærke; ved lighed (samme hele krone) får begge det.
- **Valgt butik:** (de butikker, brugeren har krydset af i chip-gitteret) `border: 2px solid var(--valgt)`, `background: var(--valgt-tint)`, og et ✓ efter navnet. Orange bruges kun til valg, som resten af siden.
- Fokus: 2 px `--valgt`-outline, 2 px forskudt. Hover (desktop): `border-color: var(--text-3)`.

## Interaktion
- Tryk på en række = **vælg kun den butik** (som at krydse den af alene: de øvrige afkrydsninger fjernes). Madplanen opdateres, og siden scroller ikke (brug den eksisterende `opdaterButik(anker)` med rækken som anker, så rækken bliver stående). En lille tekst-bekræftelse vises ikke; rækken får "valgt"-stilen, chip-gitteret får sit flueben.
- Er butikken allerede den eneste valgte, sker der ingenting.
- Brugere, der aldrig rører listen, får uændret adfærd (butiksvalg, standard = billigste, som i dag).

## Kombination af to butikker
Vises kun hvis den bedste to-butiks-kombination er **mindst 30 kr billigere** end den billigste enkeltbutik (accept i Kravet). Ellers vises ingenting (ikke "ingen besparelse") – roen er vigtigere end fuldstændigheden.
Boks under listen (`background: var(--surface-2)`, 12 px radius, 12 px padding):
> **Handl i to butikker og spar 46 kr**
> Lidl + Netto: 375 kr mod 421 kr i Lidl alene.
> `[Vælg Lidl + Netto]`  (knap 44 px, fyldt `--valgt-fill`, hvid tekst)

Tryk vælger begge butikker i chip-gitteret. Teksten påstår aldrig mere end det beregnede; "spar" er kun forskellen mellem de to indkøbspriser. Ærlig note (12 px, `--text-3`): "To butikker betyder ekstra tid; vi regner kun kroner."

## Tilstande
- **Første skærm før beregning:** Kortet vises straks med alle 9 rækker i **skeleton**: logo + navn er kendt med det samme (kommer fra `data.butikker`), pris er en grå bjælke 56 × 18 px (`--surface-2`, ingen animation i `prefers-reduced-motion`, ellers blid puls 1,2 s). Rækkefølgen er først alfabetisk/standard.
- **Efterhånden:** hver butik får sin pris, når den er regnet. **Rækkerne flytter sig ikke, mens der regnes** (ellers hopper listen under fingeren). Først når alle 9 er færdige, sorteres de billigst først med en 200 ms blød overgang (`transform`), og "Billigst" vises. Undtagelse: er under 3 butikker regnet efter 5 s, vises de færdige uden sortering og teksten "Regner stadig …".
- Mens det regnes: statuslinje i kortets undertekst: "Regner butik 4 af 9 …" (`aria-live="polite"`, opdateres højst hvert sekund). Når færdig: undertekstens normale tekst.
- **Bruger trykker på en række, der endnu ikke har pris:** rækken er tryk-bar og vælger butikken (valget afhænger ikke af tallet); prisen kommer, når den er klar.
- **Fejl** (en butiks beregning kaster): rækken viser "–" i stedet for prisen og under navnet "Kunne ikke regnes". Resten er upåvirket; rækken udelades fra rangeringen. Alle fejl: kortet viser "Sammenligningen kunne ikke regnes lige nu. Du kan stadig vælge butik ovenfor." + knap "Prøv igen" (44 px).
- **Butik uden aktuelt tilbud/udløbet avis:** rækken vises dæmpet (`opacity .7`) med "Avisen er udløbet" i stedet for besparelse, og kan ikke få "Billigst". Den er stadig tryk-bar som i dag.
- **Få dage/husstand ændret:** ændres antal voksne/børn eller fravalgte dage, regnes alle rækker om; skelet-tilstanden vises igen, og gamle tal ligger ikke tilbage som "friske".
- **Ingen butikker med data:** kortet skjules helt.

## Beregning uden at fryse siden (acceptkriterium 4 – til Frontend)
Design-krav, ikke kode: beregningen opdeles pr. butik, hver butik i egen opgave, mellem opgaverne gives tråden tilbage til browseren (`setTimeout 0` / `requestIdleCallback`); er en butiks beregning selv længere end 200 ms, må udvikleren dele den i flere trin. Første skærm (kortet i skelet) vises før den første butik regnes. Mål i Chromium som kravet siger. **Ugeforslaget for den valgte butik regnes først**, så brugerens eget tal aldrig venter bag de andre.

## Konsistens (acceptkriterium 1)
Tallet i rækken skal være **bit-identisk** med det, siden viser, når butikken vælges alene. Det kan kun garanteres, hvis rækken bruger samme funktion (`simFraButikker([k])` → `ugePris`) og samme husstand/fravalg/budget – ikke en forenklet kopi. Test for alle 9 (frontend).

## Mål og farver
- Rækker ≥ 56 px (mål 64 px) × fuld bredde → tryk-flade ≥ 44 px. "Vis alle"-knap og kombinationsknap 44 px.
- 390 px: ingen vandret scroll. Navn får `min-width: 0; overflow: hidden; text-overflow: ellipsis`; prisen har `flex: none`. Undertekst må ombryde til 2 linjer (rækken vokser).
- Farver kun fra sidens tokens: `--surface`, `--border`, `--text-1/2/3`, `--valgt`/`--valgt-fill`/`--valgt-tint`, `--sek-lys`/`--sek-dk` (billigst). Ingen rød/grøn "dyr/billig"-farvekodning – kun tekst og mærke.

## Tilgængelighed
- Listen er `<ul role="list">` med `<li><button>`. Hver knap har `aria-pressed` (valgt) og `aria-label`: "Lidl, nummer 1, billigst, ugens indkøb 421 kroner, sparer 396 kroner. Vælg butik".
- Rækkefølgen i DOM = visuel rækkefølge (også efter sortering).
- Kontrast: `--text-3` på hvid er #7A6F64 på #FFF ≈ 4,9:1 – OK til 13 px. "Billigst"-pille: `--sek-dk` #2F5753 på `--sek-lys` #A9C5C0 ≈ 4,6:1 – OK.
- Tastatur: Tab gennem rækker, Enter/Space vælger; fokus bliver på rækken efter valg (siden re-render må ikke tage fokus).
- `prefers-reduced-motion`: ingen puls og ingen sorteringsanimation.

## Hvordan hvert acceptkriterium opfyldes
1. **Alle 9 med pris identisk med enkeltvalg:** samme funktion og input som enkeltvalget; test for alle 9 (frontend).
2. **Billigst først, "Billigst" på den billigste:** sortering efter indkøbspris når alle er regnet; mærke på rang 1 (også ved lighed).
3. **Tryk vælger og opdaterer madplanen:** rækken = butikvalg alene; `opdaterButik(anker)`.
4. **Første skærm før beregning, ≤ 200 ms blokering:** skelet straks; én butik pr. opgave; mål i Chromium.
5. **390 px, 44 px:** se Mål; rækkehøjde 56–64 px.
6. **Regressionstest uændret:** ingen ændring af prisfunktioner; listen læser kun resultater.
7. **Designfil:** denne.

## Indvending til Ejeren
1. **Accept (1) er nøjagtigt nok, men "identisk" bør præciseres til "samme indkøbspris i hele kroner".** Siden viser hele kroner; en test på decimaler vil fejle uden grund.
2. **Kravet siger "Tallene regnes … butik for butik og vises efterhånden". Det er i modstrid med en rolig side**, hvis rækker hopper rundt, mens der regnes. Jeg foreslår tilføjet i accept (4): "rækkefølgen ændres først, når alle 9 er regnet (ellers står rækkerne stille)".
3. **Accept bør også dække "ingen forbrugspris i listen"** – listen viser indkøbsprisen alene, så forbrugspris og indkøbspris ikke blandes (jf. regler.md).
4. **Besparelsen "mod normalpris" afhænger af, at normalpris findes for alle varer.** Findes den ikke, skal rækken vise "sparer" kun, når tallet er sandt – ellers kun andelen på tilbud. Ejeren/backend bør bekræfte, at tallet er det samme som det ~~overstregede~~ i dag (fx 817 kr).
5. **"Vælg butik" nulstiller en flervalg.** Hvis brugeren har krydset to butikker af og så trykker på en række, mister vedkommende det valg stille. Forslag (accept): efter trykket vises ét tryk "Fortryd" i 5 s, eller kravet præciseres som beskrevet her (jeg har valgt "vælg kun den" for enkelhed).
