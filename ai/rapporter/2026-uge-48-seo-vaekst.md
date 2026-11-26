# SEO og vækst – uge 48 (2026-11-26)

Ingen trafiktal, søgedata eller brugerdata findes for holdet; alt er læst i repoet, `ai/BROWSER.md` og `ai/HELBRED.md`. Hypoteser er mærket **HYPOTESE**. Ikke tjekket: den udgivne side direkte, Search Console, søgeord og efterspørgsel, skærmbillederne (grenen `skaermbilleder` er ikke hentet).

## Efterkontrol af uge 47
Alle fire [SEO]-krav fra sidste uge er stadig åbne i backloggen, og målingerne er uændrede (målt igen i dag med script over `opskrift/*/index.html`):
- 171 af 193 titler er over 60 tegn (længste 99, median 69); 13 beskrivelser under 70 tegn, 1 over 160.
- Forsiden: `<h1>` er stadig kun logoet; meta-beskrivelse, `og:description` og JSON-LD siger stadig "10 supermarkeder", mens regler og kode taler om 9. Ejeren har ikke afgjort tallet (intet om det i ejerrapporterne for uge 47 og 2026-11-26).
- Måling: kun `/_vercel/insights/script.js` (sidevisninger); ingen hændelser.
- Ejerens rapport 2026-11-26 nævner selv, at fire SEO-punkter ligger hos mig, og at tre af de åbne punkter er grundlov. Jeg tilføjer derfor ikke flere store SEO-krav, men to små om fastholdelse.

## Nye fund med bevis
- Opskriftssiderne har fuldt `Recipe`-markup med `recipeCuisine`, `recipeCategory`, `author`, `totalTime`, `recipeYield`, `NutritionInformation`, `BreadcrumbList` (193 af 193). Mangler: `keywords`, `datePublished`, `prepTime`, `video` (0 af 193). Ingen af dem er påkrævet for Google; jeg foreslår intet, da det kun ville være fyld.
- Billeder er ikke et problem: 709 JPG i `billeder/`, største 81 kB, median 50 kB, ingen over 150 kB. Opskriftssider har 4 interne links til andre opskrifter udover forside og oversigt.
- Browser-QA 2026-11-26: GRØN, under 1 s, 0 JS-fejl, 30 små tryk-flader på mobil (uændret niveau). Vagtpost: GRØN.
- Forsiden er stadig bygget i JavaScript; `<noscript>` er kort. **HYPOTESE:** Google kører JavaScript, så det er en svaghed og ikke en blokering; ikke målt.

## Vækst og fastholdelse (hypoteser)
- **HYPOTESE:** Tilbuddene skifter hver uge, så den bedste grund til at komme igen er "hvad er nyt siden sidst". I dag mødes en tilbagevendende bruger af samme forside som en ny. Et lille "Nye tilbud siden dit sidste besøg" kan bygges kun på `localStorage` (ingen persondata, ingen server).
- **HYPOTESE:** Besøgende, der lander på en opskriftsside fra Google, ser kun én knap ("Se ugens tilbud og lav din madplan"). En knap, der forklarer værdien ("Se hvilke butikker der har tilbud til denne ret i denne uge"), kunne give flere klik videre. Må ikke vise priser på siderne (statiske sider, priser skifter). Effekten kan først vurderes, når hændelsesmålingen findes.
- Gemte madplaner/favoritter (ROADMAP 5) og delbart link (ROADMAP 12) er fortsat de dyreste huller; de er allerede krav og afhænger af login (grundlov, Sikkerhed).

## Analyse
Uændret forslag fra uge 47 (anonyme hændelser `butik_valgt`, `forslag_brugt`, `seddel_aabnet`, `liste_delt`, `opskrift_til_forside`, kun hændelsesnavn). Det er uafklaret, om Vercel-abonnementet tillader egne hændelser, og om privatlivspolitikken (grundlov) skal udvides. Det er den, der blokerer alt vurdering af vækst.

## Tre forslag
1. **[SEO] Opskriftssider: titler ≤ 60 tegn og beskrivelser 70–160** (eksisterende krav, bør tages først: lille, A, målbart).
2. **[UX] Forside: "Nye tilbud siden sidst" for tilbagevendende brugere** (nyt krav, kun `localStorage`).
3. **[UX] Opskriftsside: knap, der forklarer værdien af at gå videre til ugens tilbud** (nyt krav, ingen priser på siderne). Ejeren bør samtidig afgøre butikstallet (9/10), da det blokerer det ældre forsidekrav.
