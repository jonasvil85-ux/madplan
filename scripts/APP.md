# Måltidsjagten som app (Google Play og App Store)

Status: siden er en **PWA** (kan installeres fra browseren og virker uden net). Filer: `manifest.webmanifest`, `sw.js`, `ikoner/`.
Vejen til butikkerne bygger videre på den. Alt nedenfor kræver konti og betaling i dit navn, så det gør du selv.

## Det der allerede virker (gratis, ingen butik)
- **Android (Chrome):** menu → "Installér app" – eller knappen "Installér som app" nederst på siden.
- **iPhone (Safari):** Del → "Føj til hjemmeskærm" (knappen nederst på siden viser vejledningen).
- Indkøbssedlen og madplanen kan åbnes uden net, når man har besøgt siden én gang.
- Appikonet har genvejen "Min indkøbsseddel".

## Google Play (anbefalet først – billigt og hurtigt)
Metode: Trusted Web Activity (TWA) – selve appen er din side i en Android-ramme. Google tillader det, hvis siden er en rigtig PWA.
1. **Konto:** Google Play Console, engangsgebyr ca. 25 USD. Identitetstjek tager typisk nogle dage. Nye private konti skal normalt køre en *lukket test* med et antal testere i ca. 14 dage, før appen må udgives – tjek de aktuelle krav i Play Console.
2. **Byg pakken:** gå til https://www.pwabuilder.com, skriv sidens adresse, vælg "Package for stores" → Android. Du får en `.aab`-fil og en signeringsnøgle. **Gem nøglen sikkert** – uden den kan appen ikke opdateres.
3. **Bevis at siden er din:** læg SHA-256-fingeraftrykket fra nøglen i `/.well-known/assetlinks.json` på siden (jeg kan gøre det, når du har fingeraftrykket).
4. **Butiksside:** titel, kort og lang beskrivelse, ikon 512×512 (`ikoner/butik-1024.png` kan skaleres), mindst 2 skærmbilleder af telefonen, link til privatlivspolitikken, "Datasikkerhed"-skema og aldersmærkning.
5. Upload `.aab`, send til gennemgang.

## App Store (iPhone) – sværere
- **Konto:** Apple Developer Program, 99 USD pr. år. Kræver en **Mac med Xcode** (eller en cloud-Mac / byggetjeneste som Codemagic) – det kan ikke bygges på Windows.
- **Vigtigt:** Apple afviser ofte apps, der kun er en hjemmeside i en ramme (retningslinje 4.2 "Minimum Functionality"). Appen skal have noget, som en hjemmeside ikke har. Forslag, der giver reel værdi: **pushbesked** hver mandag med ugens madplan, **del-ark**/deling af indkøbssedlen, **widget** med dagens ret.
- Metode: Capacitor (en app-ramme om siden, med adgang til telefonens funktioner), testes i TestFlight, derefter indsendelse.
- Butiksside: som ovenfor, plus ikon 1024×1024 uden gennemsigtighed (`ikoner/butik-1024.png`), skærmbilleder i flere størrelser og privatlivsoplysninger ("App Privacy").

## Tjekliste før indsendelse
- [ ] Stabilt domæne uden "å" (adressen i appen kan ikke nemt ændres bagefter).
- [ ] Privatlivspolitikken nævner appen og de data, der gemmes (e-mail, valg af butikker).
- [ ] Ret at brugeren kan slette sin konto (kræves af både Google og Apple, hvis man kan oprette en konto).
- [ ] Avisdata: tjek, at brugen af tilbudsdata og butiksnavne/logoer er tilladt kommercielt.
- [ ] Skærmbilleder og tekst klar.

## Omkostninger (omtrentlige)
| Post | Pris |
|---|---|
| Google Play-konto | ca. 25 USD, én gang |
| Apple Developer Program | 99 USD pr. år |
| Mac / cloud-Mac til iPhone-bygning | ca. 0–50 USD pr. måned, hvis du ikke har en Mac |
| Selve appen (PWA/TWA) | 0 kr. |
