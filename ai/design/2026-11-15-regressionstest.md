# Design: regressionstest af pris, indkøbsliste og ugeforslag (TEST, ingen UI)

**Problem:** uden en automatisk test kan ingen H-ændring valideres. Brugeren mærker det som fejl i priser/lister, når en ændring slipper igennem.

**Forslag 1 – test mod de levende datafiler.** Simpelt, men facit ændres hver dag, når tilbudsrutinen bygger nye data, så testen er rød uden at koden er ændret. Forkastet.
**Forslag 2 (valgt) – test mod en frossen datakopi.** Sidens egen JavaScript køres i node (`vm`, minimal DOM-attrap, fastfrosset ur 2026-11-15) på en gemt kopi af de fire datafiler (`scripts/tests/fixtur/*.json.gz`). Resultatet sammenlignes med `facit.json`. Testen fanger dermed kun ændringer i KODEN.

**Hvad den regner (for hver af de 9 butikker):** ugeforslag og pris for 2+2 og 2+0, indkøbslistens linjer (tilbud, øvrige, basis, ekstra-tilbud) og summer for familiens forslag, `ugePris`, forbrugs-/indkøbspris for tre retter, plus to kombinationer af butikker, 25 biblioteksretters pris, `antalPakker` og `skoenPris` direkte.

**Kommandoer:** `python -I scripts/tests/regression.py` (sammenlign) · `--opdater-facit` (tilsigtet ændring) · `--opdater-fixtur` (nyt dataudsnit + nyt facit). Kaldes af `kontrol.py`.

**Fejlvisning:** forskelle som `sti: facit=… nu=…` (første 25) og en besked om, hvordan facit opdateres.

**Acceptkriterier:** (1) kører offline på ca. 2,5 s. (2) bevis for fanget prisregel og pakkestørrelse: se rapporten. (3) én kommando opdaterer facit. (4) `kontrol.py` trin 8. (5) dækningshuller står i rapporten.
