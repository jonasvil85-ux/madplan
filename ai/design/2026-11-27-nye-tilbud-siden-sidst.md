# Design: "Nye tilbud siden sidst" på forsiden

## Set på siden
Forsiden (`index.html`) er en trinvis flade: toppen (`header.top`), trinnene 1–6, derunder `#uge-besked` (en eksisterende, skjult besked-boks, i dag kun brugt til "Din ugeplan er fra …"), så `#indhold`. Skærmbilledet `mob_1_forside.png` (390 px, Browser-QA GRØN, 0 fejl) viser, at kortet "Hvor handler du?" og kortet "Sammenlign butikker" allerede fylder hele første skærm. **"Brug forslaget" og "ugens retter" ligger under skærmens fold allerede i dag** – acceptkriterie 5 er altså ikke opfyldt på main, og en ny linje gør det ikke bedre.
`retter.json` har `genereret` (ISO-tid) og pr. butik en liste `retter` (60 stk.) med `navn`, `pris`, `hvorfor` … **Der findes intet `id` på retterne**, kun `navn` pr. butik.

## Problemet set fra brugeren
Tilbud skifter hver uge, men en, der kommer igen, får samme forside som en nybegynder og ved ikke, om der er noget nyt at hente. Man skal selv tjekke alt igen.

## To meget forskellige løsninger
**A. Lukkebar linje øverst (kravets forslag):** én rolig linje med tal ("12 nye retter hos dine butikker"). Billig, men et tal uden handling er kun pynt – brugeren spørger "så hvad?".
**B. Linje med handling (valgt):** samme lille linje, men med en knap "Brug de nye", der laver ugens forslag ud fra de nye retter, eller som blot rykker brugeren til trin 2 med de nye retter markeret. Mere kode og kobler til forslagsmotoren (klasse H).
**Valg: A med et lille hak af B – en sekundær tekstknap "Se ugens forslag", der blot fører til madplanen (`#sim-plads`), som i forvejen findes.** Begrundelse: kravet er klasse A og hypotesen er uafprøvet; vi skal først måle, om nogen bruger linjen. Ingen ændring af ugeforslagets beregning (Ikke-mål). Knappen kobler linjen til det, brugeren alligevel vil: se ugens madplan.

## Hvornår vises linjen
Gemmes i `localStorage` under nøglen `mj-set` (ingen cookies, intet i Supabase, intet bruger-id):
`{ g: "<genereret fra sidste lukning>", n: { netto: ["Kyllingebrystfilet", …], rema: [...] , … } }` – navnene pr. butik, som brugeren sidst har "set". (Ca. 9 × 60 korte navne ≈ 15 KB; kun navne, intet andet.)

Regel, når `retter.json` er hentet og siden vises:
1. **Ingen gemt `mj-set`** (første besøg): gem nu-værdien som baseline. **Vis intet.**
2. **Ingen valgte butikker** (`state.butikker` tom): vis intet. "Dine butikker" findes ikke endnu.
3. Ellers: `nye` = antal retter hos de **valgte butikker**, hvis `navn` ikke stod i baseline for samme butik (en ny butik, der ikke fandtes i baseline, tæller ikke med, ellers ser en nyvalgt butik alt som "nyt").
4. `nye = 0`: opdatér baseline stille til nu; vis intet.
5. `nye ≥ 1` og `genereret` er nyere end `g`: **vis linjen.** Baseline ændres IKKE, før brugeren lukker linjen – så forsvinder den ikke, bare fordi man genindlæser siden samme dag.
6. Lukker brugeren linjen: skriv ny baseline (nu-værdien). Linjen kommer først igen, når der næste gang er nye retter.
7. Blokeret/fuld `localStorage` (try/catch om alt): siden opfører sig præcis som i dag, ingen linje, ingen fejl.
Tallet er altid regnet af `retter.json`; intet opfundet. Under 3 nye retter vises linjen ikke (1–2 nye er støj, ikke en nyhed) – se indvending.

## Placering
Mobil (390 px) og desktop: ny `<div id="nyt-siden-sidst" class="nyt-linje" hidden>` lige over `#uge-besked` (under trin-navigationen), samme bredde som kortene. Er `#uge-besked` også synlig, vises kun den ene (uge-beskeden vinder: den er en handling, der kræver stillingtagen); linjen venter til næste besøg.

## Udseende (sidens tokens)
- Baggrund `--surface-2`, 1 px kant `--border`, `border-radius: var(--radius)`, indre afstand 10 × 14 px, `margin-bottom: 12px`. Ingen gul/rød (rolig side, én accent). Ingen animation.
- Tekst 14 px / 1.4 `--text-2`; tallet fedt i `--text-1`.
- Højde: én linje på desktop; på 390 px højst to linjer tekst + knapperne på egen række = højst ca. 88 px. Må ikke give vandret scroll.
- Knapper (tekstknapper med kant `--border`): "Se ugens forslag" og lukkeknappen (× 20 px ikon i en 44 × 44 px tryk-flade). Begge min. 44 × 44 px.

## Tekster (ord for ord)
- Mange: "**12 nye retter** hos dine butikker siden sidst."
- Netop 1: ikke vist (se grænse). Hos 1 butik: "**5 nye retter** hos REMA 1000 siden sidst." (butiksnavn kun, når der er nøjagtig én valgt butik).
- Knap: "Se ugens forslag" · Luk: `aria-label="Luk"`.
- Ingen "tilbud" i tallet: det er *retter bygget af tilbud*, ikke tilbud – ordene "nye retter" er ærlige.

## Tilstande
Første besøg: intet. Intet nyt: intet. Nyt: linjen. Lukket: væk til næste nyhed. `localStorage` blokeret: intet. Indlæser: intet (vises først, når data er hentet; ingen springende layout – linjen sættes ind før `#indhold` males, ellers på toppen af siden kun hvis brugeren står i top, som i bannerdesignet). Få/mange retter: tal over 99 vises som "99+".

## Tilgængelighed
`role="status"`, ikke `alert`. Kontrast `--text-2` på `--surface-2` ≥ 4,5:1 i begge temaer. Synlig fokusring (2 px `--valgt`, offset 2 px), tabrækkefølge: tekst → "Se ugens forslag" → luk. Enter/mellemrum udløser knapperne.

## Hvordan hvert acceptkriterium opfyldes
1. *Første besøg: ingen linje* – regel 1.
2. *Andet besøg efter nye retter: linjen vises og kan lukkes* – regel 5–6; browsertest: sæt `mj-set` med én butik uden 5 af retterne, indlæs, se linjen, luk, genindlæs → væk.
3. *Tallet fra `retter.json` (`genereret` + retter)* – sammenligning på `navn` pr. butik (der findes ingen id'er).
4. *Virker uændret, hvis `localStorage` er blokeret* – try/catch; test med blokeret lager.
5. *390 × 844: butiksvalg, ugens retter og "Brug forslaget" synlige uden scroll* – **kan ikke opfyldes af dette krav** (er brudt på main allerede); se indvending. Linjen selv må højst være ca. 88 px.
6. *kontrol.py BESTÅET.*

## Indvending til Ejeren
- **Accept (5) måler det forkerte:** på main er "Brug forslaget" og ugens retter ikke synlige uden scroll på 390 × 844 (skærmbillede `mob_1_forside.png`: butiksvalg + "Sammenlign butikker" fylder alt). Kriteriet kan ikke være bestået før eller efter dette krav. Formulér i stedet: "(5) linjen er højst 90 px høj på 390 px og flytter ikke `#sim-plads` mere end dens egen højde; ingen vandret scroll." Selve "alt på første skærm"-problemet er et separat krav (jf. "Hvor handler du?").
- **"Retternes id" findes ikke:** brug `navn` pr. butik (accept 3).
- **Tilføj accept:** (7) mindst 3 nye retter, før linjen vises; (8) linjen forsvinder ikke ved genindlæsning, før den er lukket; (9) vises ikke, når ingen butik er valgt.
- **Hypotesen kan først måles med hændelsesmålingen** ("Anonym hændelsesmåling" ligger lavere i backloggen). Overvej at rykke den op, ellers bygger vi en funktion, vi aldrig kan evaluere.
