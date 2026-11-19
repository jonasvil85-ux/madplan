# Anden mening 2026-11-19 (kørsel 2)

Nyt siden sidst (`HEAD~1..HEAD`): to nye designfiler i `ai/design/`. Begge tages med (2 emner, 3 kald: 2 på emne 1, 1 på emne 2). Kald brugt: 3 af 3.

## Emne 1: Banner "Du ser en gemt kopi" (`2026-11-19-gemt-kopi-banner.md`)

**Spørgsmål:** Hvordan får brugeren bedst at vide, at tilbud og priser kan være en gammel gemt kopi, uden at gøre siden urolig?

**Idéer (kreativ runde)**
1. Tynd grå statuslinje i bunden af toppen med "data fra X minutter siden": **afvist** som selvstændig løsning (en relativ tid kræver et pålideligt tidsstempel; vi har kun en dato, og linjen er i praksis det banner, vi allerede har).
2. Faner "Frisk / Gammel": **afvist**, giver brugeren et valg, de ikke skal træffe, og dobbelt UI i en rolig side.
3. Tidsmaskine-slider med AR-pristag: **afvist**, skørt og ikke børnevenligt/roligt; ingen værdi i butikken.
4. "Prisstjerner" efter friskhed: **afvist**, alle priser i en kopi er lige gamle; stjerner antyder en præcision, vi ikke har, og strider mod ærlige tal.
5. Kun et lille "Senest synk: dato"-stempel på indkøbslisten, der kan trykkes for at hente igen: **valgt (delvist)**. Vi har allerede en linje på indkøbslisten; idéen gør den mere brugbar: datoen vises dér, hvor den gør nytte, og et tryk på den henter igen (så man ikke behøver finde banneret øverst).

**Modellens kritik (kritisk runde, omskrevet)**
- Hvor gammel må en kopi være, før den ikke længere tæller som gyldig? (uklar grænse)
- Ingen manuel opdatering/mulighed for at slå kopien fra.
- Banneret vises kun, når siden står i top; rulles man ned, kan man gå glip af advarslen.
- `role=status` + `polite` er for svagt til skærmlæsere; brug `alert`/dialog.
- Ingen vejledning ud over "Prøv igen".
- Hvis service workeren fejler, ingen advarsel; brug netværkstjek/timeout.

**Min vurdering**
- Alder/grænse: **delvist enig.** Designet viser dato, når den er kendt, men har ingen tærskel. Forslag: er `data.genereret` ældre end 7 dage (tilbud gælder typisk en uge), så skift teksten til "Tilbuddene kan være udløbet." Dette er et konkret hul, jeg ikke selv havde med.
- Manuel opdatering: **uenig.** "Prøv igen" findes allerede; en "slå kopien fra"-kontakt er unødig kompleksitet.
- Banner skjult under rulning: **delvist enig.** Designet undgår hop bevidst; risikoen dækkes af gentagelsen på indkøbslisten (der hvor prisen betyder noget). Tilføj, at linjen på indkøbslisten **altid** vises, også når man står midt på siden, fordi den er i flowet.
- `alert` i stedet for `status`: **uenig.** Det er ikke en fejl; `alert` afbryder skærmlæseren og er i strid med "rolig side". Behold `status`/`polite`.
- Ingen vejledning: **delvist enig.** Tekstlinjen "Ingen forbindelse lige nu. Det du har gemt virker stadig." findes allerede; generelt råd uden nyt indhold.
- Service worker uden support: **uenig.** Uden service worker findes ingen kopi, så der er intet at advare om (står i designets tilstande).

**Foreslået ændring af designet**
1. På indkøbslisten: erstat linjen med en tryk-bar dato: "Priserne er fra en gemt kopi fra 17. november. Tryk for at hente igen." (min. 44 px trykflade, samme "Henter …"/"Opdateret."-tilstande som banneret; ingen dato, hvis den ikke kendes eller er ugyldig).
2. Tilføj en alderstærskel: er `data.genereret` mere end 7 dage gammel, bruges teksten "Tilbuddene kan være udløbet." i stedet for "kan være ældre end i dag."
3. Tilføj accept: (7) indkøbslistens linje er synlig uden at rulle op og kan udløse "Prøv igen" med ét tryk.
4. Indvendingerne til Ejeren i designfilen står ved magt (accept 2 omformuleres, accept 5 og 6 tilføjes).

## Emne 2: Motoren i trin (`2026-11-19-motoren-i-trin.md`)

**Spørgsmål:** Er "øjeblikkelig respons først, opdeling af motoren kun hvis nødvendigt" det rigtige valg, og hvad er svagt i den?

**Idéer:** ikke kaldt kreativt (højst 3 kald; kun kritisk runde på emne 2).

**Modellens kritik (omskrevet)**
- `requestAnimationFrame` garanterer ikke, at UI'et er malet før den tunge beregning, især på svage telefoner.
- Kassering af en ældre beregning er ikke specificeret (AbortController); den gamle kan overskrive den nye.
- En afbrudt beregning kan give en blandet pris-liste.
- "Regner ugen …" med nedtonede kort kan misforstås som færdigt resultat.
- Måling kun i Chromium dækker ikke Safari/iOS, Android-WebView og ældre enheder.
- Alternativ: web worker (off-main-thread) i stedet for opdeling.

**Min vurdering**
- rAF: **enig, med præcisering.** En enkelt `rAF` kører *før* malingen; beregningen skal startes efter malingen (fx `rAF` → `setTimeout(0)` eller dobbelt `rAF`). Designet siger "rAF før den tunge beregning", hvilket er flertydigt og kan give en tilstand, der ikke bliver malet. Det er et reelt fund.
- Abort/kassering: **delvist enig.** Beregningen er synkron (ét stræk), så en igangværende beregning kan ikke afbrydes; `AbortController` er irrelevant. Risikoen er i stedet, at to tryk sætter to beregninger i kø, og den ældste skriver sit resultat sidst. Løsning: et løbenummer (`seneste = ++taeller`), og kun resultatet med det seneste nummer vises. Ingen blandede lister, fordi resultatet sættes samlet.
- Forvirring ved nedtonede kort: **delvist enig.** Teksten "Regner ugen …" står på ugens plads, og `aria-busy` sættes, men vi bør også deaktivere "Byt"/"Brug forslaget" på de nedtonede kort under beregning (undgå handling på gamle data).
- Måling kun i Chromium: **delvist enig.** Chromium er det, Browser-QA kan; skriv i rapporten, at Safari/iOS ikke er målt, i stedet for at udvide kravet med en måling, vi ikke kan køre. Tilføj en 4x CPU-nedbremsning i Chromium som stedfortræder for en svag telefon.
- Web worker: **uenig for nu.** Kræver at tilbudsdata og motor flyttes ind i en worker (stor omskrivning, klasse H, risiko for prisfejl) og er større end selve opdelingen. Kan bero til, hvis B ikke er nok.

**Foreslået ændring af designet**
1. Præcisér: "ændringen males først (`rAF` og derefter `setTimeout(0)`), og først derefter starter beregningen."
2. Et løbenummer kasserer ældre resultater; kun det seneste tryks resultat vises.
3. Under beregning er trykflader på de nedtonede kort deaktiveret (`aria-disabled`, uændret størrelse).
4. Accept: "synlig inden for 100 ms målt i Chromium over 5 kørsler for alle 9 butikker, også med 4x CPU-nedbremsning; ikke målt i Safari/iOS (anføres i rapporten)."
5. Klassen `[UX] [A]` for (a) og `[BACKEND] [H]` for (b) står ved magt.

## Samlet

Kald: 3 af 3. Intet er ændret i backlog eller design (kun denne rapport).

Nyttigt: delvist. Nyt for mig: alderstærskel på 7 dage for tilbud, at en enkelt `rAF` ikke garanterer maling før beregningen, og at to hurtige tryk kan lade en gammel beregning skrive sidst. De øvrige punkter var generelle eller allerede dækket i designet.
