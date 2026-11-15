# Udviklerrapport 2026-11-15 – opskriftssider (bygget af Claude i chatten på Jonas' bestilling)

**Hvad:** `scripts/byg_sider.py` bygger en statisk side til hver af de 193 biblioteksopskrifter (`/opskrift/<navn>/`), en oversigt (`/opskrifter/`) og `sitemap.xml` (196 adresser). Hver side har billede, ingredienser til 4, trin, tid, næring, Recipe- og brødkrumme-JSON-LD, intern linkning til fire andre opskrifter og en knap til appen. Forsiden har fået et link "Alle opskrifter" i bunden.

**Hvorfor:** ROADMAP 1: siden havde én URL, så Google kunne ikke vise nogen ret. Det er den største vækstmulighed uden betalt annoncering.

**Klasse:** A i indhold (nye statiske filer, intet i appens beregninger, priser eller data ændret). Formelt matcher navnet `byg_*.py` klasse H, men scriptet læser kun `opskrifter.json` og `naering.json` og skriver kun nye filer; `retter.json`, `opskrifter.json` og al JavaScript er uændret (kun ét link i footeren i `index.html`). Regressionstesten skal være uændret.

**Filer:** `scripts/byg_sider.py`, `opskrift/` (193 mapper), `opskrifter/index.html`, `sitemap.xml`, `index.html` (ét link), `scripts/tests/kontrol.py` (nyt tjek: hver opskrift har en side, står i sitemap og har gyldig Recipe-JSON-LD), denne rapport.

**Accept:**
1. 193 sider + oversigt: bygget.
2. Gyldig Recipe-JSON-LD på hver: alle 193 parser som JSON og har navn, ingredienser og trin (kontrollen tjekker det). Ikke tjekket mod Googles egen rich results-test (kræver internet og værktøj, der ikke er tilgængeligt her).
3. Sitemap med alle: 196 adresser.
4. Kontrollen tjekker det: bevist ved at flytte én side væk; `FEJLET (1 fejl)`, derefter `BESTÅET`.
5. Siderne bygges af `byg_sider.py`: ja.
6. Ingen priser eller datoer på siderne: ja.

**Test:** `RESULTAT: BESTÅET (0 fejl, 11 advarsler)` lokalt (uden node, så JavaScript og regression kørte ikke lokalt; skal køres af kontrolløren). Set i headless Edge: mobil (390 px) og desktop (1100 px) uden vandret scroll; skærmbilleder af en opskriftsside og oversigten kontrolleret.

**Dækker IKKE:** om Google faktisk indekserer siderne (det tager uger); mørk tilstand er kun kontrolleret i CSS, ikke på skærmen; sider for butiksretterne (de skifter hver uge); `scripts/byg_sider.py` er endnu ikke kaldt af tilbudsrutinen eller billedhandlingen (opskrifterne ændres sjældent; byg_sider skal køres, når `bibliotek_*.py` ændres).

**Kontrolløren bør kigge på:** at `python -I scripts/byg_sider.py` giver byte-identiske filer to gange i træk; at `retter.json`/`opskrifter.json` er uændrede; at regressionstesten er uændret; stikprøve af 5 sider.

**Næste skridt:** (1) Lad billedhandlingen og RUTINE.md kalde `byg_sider.py` efter `byg_opskrifter.py` (grundlov; Jonas/chatten gør det). (2) Når siderne er indekseret: mål visninger i Google Search Console (kræver Jonas). (3) Overvej opskriftssider med "typisk pris pr. person" først når et ærligt, stabilt tal findes.
