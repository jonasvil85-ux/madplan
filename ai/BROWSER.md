# Browser-QA af den udgivne side

Sidst kørt: 2026-11-22 · https://madplan-blue.vercel.app/

**Resultat: GRØN**

Skrevet af GitHub-handlingen "Browser-QA" (`scripts/tests/browser_tjek.py`) med Chromium. Skærmbillederne ligger på grenen `skaermbilleder` (hent dem med `git fetch origin skaermbilleder` og `git show origin/skaermbilleder:mob_1_forside.png > /tmp/x.png`, og åbn filen med Read). Rutinerne i skyen har ingen browser, så de læser denne fil og billederne.

### mob (390 px)
- Indlæsning (load-hændelsen): 1–3 s · største indhold vist: 1–3 s
- Vandret scroll: nej · JavaScript-fejl: 0 · ødelagte billeder: 0 · billeder uden alt: 0
- Små tryk-flader (under 40 px): 30 – fx 365discount✓; Bilka✓; Byt Fredags ret; Byt Lørdags ret; Byt Mandags ret; Byt Onsdags ret; Byt Søndags ret; Byt Tirsdags ret
- Flow: brug forslaget: ok, trin 2: ok, trin 3: ok, trin 4: ok, trin 5: ok
- Trin set: butik, retter, liste, tilfoej, seddel

### desk (1280 px)
- Indlæsning (load-hændelsen): under 1 s · største indhold vist: under 1 s
- Vandret scroll: nej · JavaScript-fejl: 0 · ødelagte billeder: 0 · billeder uden alt: 0
- Små tryk-flader (under 40 px): 31 – fx 1 butik821 kr402 kr REMA 100; 365discount✓; Bilka✓; Byt Fredags ret; Byt Lørdags ret; Byt Mandags ret; Byt Onsdags ret; Byt Søndags ret
- Flow: brug forslaget: ok, trin 2: ok, trin 3: ok, trin 4: ok, trin 5: ok
- Trin set: butik, retter, liste, tilfoej, seddel

Målt: vandret scroll, JavaScript-fejl, ødelagte billeder, tryk-flader under 40 px, indlæsningstid (i grove intervaller) og et flow gennem trinene. Ikke målt: farvekontrast, tastaturbrug, andre husstande end standard, login.
