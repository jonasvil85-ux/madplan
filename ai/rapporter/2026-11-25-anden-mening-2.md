# Anden mening 2026-11-25 (kørsel 2)

Udløst af: `ai/BACKLOG.md` (commit "Sikkerhed: uge 48"). Ingen ændringer i `ai/design/`. Rolle: Security Auditor. Nyt i diffen: kravene N1 og N2 (begge `[SIKKERHED]`) og en tilføjelse til M1, som allerede stammer fra `2026-11-18-anden-mening-2.md` og derfor ikke valideres igen. Emner: 2 (N1, N2). Kald brugt: 3 af 3 (N1 kreativ, N1 kritisk, N2 kritisk).

Note: scriptets filter afviste mit første spørgsmål, fordi det indeholdt ordet "SECRET" (som navnemønster). Jeg omskrev spørgsmålet med "adgangsoplysninger" i stedet. Der stod ingen rigtige nøgler i teksten.

## Emne 1: N1 – adgangsoplysninger ude af miljøet, mens agent-redigerbar kode kører
**Spørgsmål:** Hvordan holder man adgangsoplysninger væk fra kode, som AI-agenter kan ændre, og hvad er svagt i det foreslåede krav?

### Idéer (runde 1, kreativ)
1. **Eget job kun til trinnet med nøglen, byg/test uden:** VALGT (det er i store træk N1(a); bekræfter retningen).
2. **Pladsholdere + OIDC-token fra GitHub, som udskiftes via et hvælv:** AFVIST nu. Kræver et hvælv (Vault), som ejeren ikke har; for tung til et enmandsprojekt. Kan overvejes senere, hvis Cloudflare understøtter OIDC direkte.
3. **Homomorfisk kryptering:** AFVIST. Ikke praktisk og løser ikke problemet.
4. **Flyt agenten ud af CI til en ekstern tjeneste:** AFVIST. Flytter bare problemet og tilføjer en ny tjeneste.
5. **Pre-commit-hook, der blokerer nøgle-mønstre:** AFVIST. Den forhindrer, at nøgler *kommer ind* i koden, ikke at en ændret fil *sender* nøglen ud, som er det rigtige problem. Desuden kan en agent bare ikke køre krogen.

### Modellens kritik (runde 2, kritisk, omskrevet)
- `GITHUB_TOKEN` har som standard skriveret; et job uden egne hemmeligheder kan stadig skrive til repoet og ændre andre workflows.
- Artefakter, cache og logs kan lække oplysninger, hvis noget skrives dertil.
- Den tilladte liste i kontrol (b) skal selv beskyttes (hvor ligger den, hvem kan ændre den).
- Kontrol (b) ser kun direkte `import`; dynamisk import (`__import__`, `importlib`, `eval`), `subprocess`/`os.system` til `curl` og egne hjælpemoduler omgår den.
- Modellen påstod også, at efterfølgende trin arver miljøvariabler fra det trin, der har nøglen.

### Min vurdering
- **Enig** i `GITHUB_TOKEN`: kravet bør sige `permissions: contents: read` på jobbet uden nøgle (og kun de nødvendige rettigheder på de andre). Det er et konkret hul, som N1 ikke dækker i dag.
- **Enig** i, at listen og kontrollen skal ligge et sted, agenter ikke frit kan redigere. Tilføjelsen af `scripts/tests/kontrol.py` selv i klasse H eller grundloven er værd at overveje; ellers kan en agent ændre kontrollen og listen i samme gren. Den ændring afgøres af Jonas/Kontrollanten.
- **Enig** i, at dynamisk import og `subprocess`/`os.system` skal med i kontrollen. Kontrollen bliver aldrig tæt (det er en statisk søgning), og det bør stå ærligt i kravet: den fanger fejl og dovne ændringer, ikke et målrettet angreb. Den egentlige beskyttelse er (a), altså at nøglen slet ikke findes i det job.
- **Delvist enig** om artefakter/cache/logs: der er ingen artefakter i dag (skal tjekkes af udvikleren i workflowfilerne, ikke gættet her). GitHub maskerer hemmeligheder i logs. Et krav: "intet job uploader artefakter eller cache fra jobbet med nøglen" er billigt at tilføje som accept.
- **Uenig** i påstanden om, at senere trin arver nøglen: er den sat som `env` på ét trin, er den ikke synlig i andre trin. Det forudsætter, at den er sat på trinniveau, ikke på job- eller workflowniveau. Det er netop, hvad accept (1) tester.
- **Uenig** i forslaget "forbud mod `os.getenv` uden whitelist": for bredt. Scripts læser mange ufarlige variabler; navnemønsteret i N1(b) er bedre.

### Foreslået ændring af kravet N1
Tilføj til (a): "Jobbet uden adgangsoplysninger har `permissions: contents: read`; ingen jobs uploader artefakter eller cache fra jobbet med `CLOUDFLARE_API_TOKEN`." Tilføj til (b): "Kontrollen fanger også `__import__`, `importlib`, `subprocess`, `os.system` og `eval`/`exec` uden for den tilladte liste. Kravet nævner udtrykkeligt, at kontrollen er et net mod fejl, ikke en grænse mod et målrettet angreb; grænsen er (a)." Tilføj til accept: "(6) `kontrol.py` og den tilladte liste kan ikke ændres uden at Kontrollanten ser det (sti i klasse H)."

## Emne 2: N2 – ruleset på `main` mod force-push og sletning
**Spørgsmål:** Er rulesettet nok, og hvad er billigt at tilføje uden at stoppe agenternes direkte push?

### Idéer
Ingen kreativ runde (kald sparet til kritisk runde på emne 2).

### Modellens kritik (runde 3, kritisk, omskrevet)
- Rulesettet stopper ikke et lækket token i at pushe en *ny* ondsindet commit ovenpå (falske priser, malware), og siden udgives straks.
- Admin/ejer kan slå reglerne fra eller omgå dem (bypass-liste).
- Forslag: krav om signerede commits, lineær historik, statustjek, begrænset push til to bot-konti, mindre token-rettigheder.

### Min vurdering
- **Enig** i det vigtigste: N2 beskytter *historikken*, ikke *indholdet*. Det står ikke tydeligt i kravet. Den reelle beskyttelse mod et lækket token er H2/N1 (token uden hemmeligheder i miljøet, mindst mulige rettigheder).
- **Enig** i bypass-listen: kravet bør sige, at listen er tom, og at Jonas tjekker det i accept (`bypass_actors` er tom).
- **Uenig** i signerede commits: agenternes push sker som GitHub Actions med et almindeligt token; commits via `git push` er ikke signeret, så det ville stoppe hele den daglige arbejdsgang, som kravet netop skal bevare.
- **Uenig** i lineær historik og statustjek: kontrollantens sammenlægninger laver sammenlægningscommits, og statustjek er udtrykkeligt udelukket i kravet (ville stoppe direkte push af `ai/`-filer). Modellen bad om det, kravet bad om det modsatte.
- **Uenig** i "begræns push til to bot-konti" og "fjern `repo:admin`": enmandsrepo uden bot-konti, og Actions-tokens har aldrig admin-rettigheder. Forslagene passer ikke til opsætningen.
- **Min egen tilføjelse (ikke fra modellen):** et billigt skadebegrænsende skridt er en hurtig tilbagerulning af udgivelsen hos hosting-udbyderen. Skriv i kravets ikke-mål eller accept, at Jonas ved, hvordan man ruller tilbage ét klik, så en ondsindet commit kan fjernes fra siden på få minutter. Det kræver ingen kode.

### Foreslået ændring af kravet N2
Tilføj: "Rulesettet beskytter historikken, ikke indholdet; mod en ny ondsindet commit beskytter N1/H2. `bypass_actors` er tom. Accept (3): Jonas har prøvet tilbagerulning af seneste udgivelse hos hosting-udbyderen og ved, hvor knappen er."

## Samlet
Modellen fandt ét konkret hul (`GITHUB_TOKEN`-rettigheder) og to rigtige præciseringer (dynamisk import i kontrollen, tom bypass-liste); resten var enten allerede dækket, forkert for opsætningen eller direkte i modstrid med kravets egne betingelser. Ikke set eller kørt: ingen workflowfiler er læst i denne kørsel, så om der findes artefakter eller cache i dag er ikke tjekket.

Nyttigt: delvist
