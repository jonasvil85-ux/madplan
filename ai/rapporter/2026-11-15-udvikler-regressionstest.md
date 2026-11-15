# Udviklerrapport 2026-11-15 (regressionstest)

**Hvad:** `scripts/tests/regression.py` + `regression.js` kører sidens egen JavaScript (`ikoner.js`, `varer.js`, `pris.js`, `kategorier.js`, scriptet i `index.html`) i node uden browser og net, på en gemt datakopi (`scripts/tests/fixtur/*.json.gz`), og sammenligner med `scripts/tests/facit.json`. Kaldes af `kontrol.py` (trin 8).

**Hvorfor:** øverste krav i backloggen; uden testen kan ingen klasse H-ændring slås sammen.

**Klasse:** A (kun test og dokumentation; ingen produktionskode ændret).

**Filer:** `scripts/tests/regression.py`, `regression.js`, `facit.json`, `fixtur/` (4 filer), `scripts/tests/kontrol.py` (+8 linjer), `ai/design/2026-11-15-regressionstest.md`, denne rapport.

**Valg/antagelse:** kravet siger "gemt facitliste". Da data bygges dagligt, ville facit være rødt hver dag; derfor køres på en frossen datakopi (fixtur). Fixturen opdateres bevidst med `--opdater-fixtur`.

**Accept:**
1. Under 2 min uden net: ca. 2,3 s lokalt (ingen netværkskald; `fetch` er erstattet af fixturen).
2. Fanger bevidste ændringer (hver rullet tilbage med `git checkout` bagefter): `gulerød` 13→14 kr i `pris.js` → `FEJLET – 21 forskelle` (bl.a. Meny-listens sum 864,75→912,75); `PAKKE_TOLERANCE` 0,15→0,05 i `index.html` → `FEJLET – 294 forskelle`; pastapakke 500→400 g i `pris.js` → `FEJLET – 1 forskel` (`skoen[2][1]` 12→24). Med prisregel-ændringen gik `kontrol.py` også rød (1 fejl).
3. `python -I scripts/tests/regression.py --opdater-facit` (eller `--opdater-fixtur` for nyt dataudsnit).
4. `kontrol.py` kalder den; uden node giver den en advarsel.
5. Se nedenfor.
Deterministisk: to kørsler giver byte-identisk output.

**Test:** før: `RESULTAT: BESTÅET (0 fejl, 9 advarsler)`. Efter: `RESULTAT: BESTÅET (0 fejl, 9 advarsler)` (se også `REGRESSION: BESTÅET`).

**Dækker IKKE:** udseende/DOM/render, login/Supabase, service worker, sletning/bytning af dage (`simByt`), `forbrugspris` for flere end tre retter pr. butik, 3-butikskombinationer ud over én, ugeforslag for andre husstande end 2+2 og 2+0, tilstande hvor brugeren selv vælger retter, ikke-afrundede tal (alt rundes til 2 decimaler), og live-data (testen bruger bevidst en gammel kopi, så en fejl i dagens data fanges kun af `kontrol.py`). Ur og ugedage er frosset til 2026-11-15; udløbslogik med andre datoer er ikke testet. DOM-attrappen kan skjule fejl, der kun opstår i en rigtig browser.

**Før/efter-tal:** ikke relevant (ingen H-ændring; ingen sidekode rørt).

**Kontrolløren bør kigge på:** at `fixtur/` er en uændret kopi af main-data (`gunzip -c … | cmp - retter.json`, forventes ens i dag); at facit er stabilt over to kørsler; selv at ændre en prisregel og se den fanges (rød-hold).

**Næste skridt:** Ejeren kan flytte regressionstesten fra "Åbne krav" til færdig og fjerne spærringen af klasse H i `STATUS.md`/`README.md` (disse er ikke rørt af mig). Forslag: udvid senere med byt/fjern dag og flere husstande.
