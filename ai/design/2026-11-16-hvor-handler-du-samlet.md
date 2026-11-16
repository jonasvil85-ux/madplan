# Design: "Hvor handler du?" og "Sammenlign butikker" lagt sammen i ét kort (2026-11-16)

Godkendt af Jonas 2026-11-16: "læg det sammen i et kort og udregn prisen på baggrund af det du mener er korrekt".

## Problem
Forsiden stiller samme spørgsmål to gange: først 9 logoer at krydse af ("Hvor handler du?" + "Hvor mange butikker"), derefter de samme 9 butikker igen som prisliste ("Sammenlign butikker"). Samme tal står to steder ("1 butik 464 kr" = rækken "Netto 464 kr"), en gammel tekst ("Kryds flere butikker af …") modsiger det nye kort, og madplanen starter ca. 1.050 px nede på telefonen.

## Prisgrundlag (afgjort)
Hver række er **butikkens egen billigste uge ud fra dens egne tilbud**: 7 aftensmåltider, samme husstand, samme portioner. Det er den eneste fair sammenligning: at prissætte én madplan i alle butikker straffer de butikker, hvor retterne ikke er på tilbud (Jonas' pointe). To-butiks-forslaget beholder den forsigtige regel: besparelsen er det mindste af (a) samme retter og mængder i den billigste enkeltbutik og (b) dens egen uge.

## Nyt kort (erstatter begge)
```
Hvor handler du?
Billigste uge i hver butik ud fra dens egne tilbud:
7 aftensmåltider til 2 voksne + 2 børn, samme portioner overalt.
┌──────────────────────────────────────┐
│ 1  Lidl ✓          Billigst   421 kr │  valgt butik: grøn ramme (tryk = vælg)
│ 2  Netto                      464 kr │
│ 3  365discount                514 kr │
└──────────────────────────────────────┘
[ Vis alle 9 butikker ]                     (kun telefon; computer viser 3×3)
[ Handl i to: MENY + REMA … spar 40 kr ]   (kun når besparelsen er ægte, som i dag)
Vælg selv flere butikker ›                 (åbner det eksisterende logo-valg + "Hvor mange butikker")
```
- Overskriften "Sammenlign butikker" og det separate kort forsvinder.
- Logo-gitteret og "Hvor mange butikker"-boksen ligger bag "Vælg selv flere butikker" (knap, aria-expanded). Den er **åben af sig selv**, når brugeren har valgt mere end én butik, så et eksisterende flerbutiksvalg aldrig skjules.
- Under beregningen: rækkerne vises straks med navn og logo (valgte butikker først), prisen som grå bjælke – som i dag. Der kan trykkes med det samme.
- Rundvisningen: trin 2 peger på listen ("Hvor handler du?" – tryk på en butik for at vælge den), trin 3 på "Vælg selv flere butikker". Skjulte områder springes allerede over.

## Mål
- Madplanen starter mindst 300 px højere på 390 px (i dag ca. 1.050 px).
- Ingen dobbelte logoer eller tal på første skærm.
- Alle tal og test fra "Sammenlign butikker" uændrede.


## Revision samme dag (Jonas: "vælge mere end en butik bare ved at trykke på en butik mere … pænt, simpelt og logisk")
"Vælg selv flere butikker" og logo-gitteret er fjernet. Listen er afkrydsning:
```
Hvor handler du?
Tryk på de butikker, du handler i – gerne flere. Prisen er hver butiks billigste uge
ud fra egne tilbud, 7 aftensmåltider til 2 voksne + 2 børn.
┌──────────────────────────────────────┐
│ [✓] Lidl          Billigst   421 kr  │
│ [✓] Netto                    464 kr  │  ← et tryk mere = to butikker
│ [ ] 365discount              514 kr  │
└──────────────────────────────────────┘
Vis alle 9 butikker ▾
────────────────────────────────────────
Hvor mange butikker vil du handle i?      ← kun når der er valgt flere
[ 1 butik  421 kr  Lidl ]
[ 2 butikker 367 kr Netto og Lidl  Anbefalet ]
```
Med én butik valgt og et billigere par: "Spar 54 kr ved også at handle i Netto – Lidl + Netto: 367 kr for ugen mod 421 kr i Lidl alene. Transport og ekstra tid er ikke regnet med i prisen. [Tilføj Netto]". Forslaget forsvinder, når parret er valgt. En valgt butik skjules aldrig af "Vis alle".
