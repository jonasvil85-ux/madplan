# Anden mening 2026-11-24 (kørsel 2)

Udløst af ændringen i `ai/design/` (commit cc2586e): ny designfil `ai/design/2026-11-24-soeg-ental-flertal.md`. Der var ingen ændringer i `ai/BACKLOG.md`. Rolle: UX Designer (emne 1). Ingen `[SIKKERHED]`-krav. Kald: 3 af 3 (1 kreativ som gav svar; 2 kritiske kald gav begge "tomt svar fra modellen" og er dermed spildt). Modellen: gpt-oss-120b. Modellen er rådgiver; intet er ændret i backlog eller design.

## Emne 1: Søg i "Vælg selv": stamme-regel for ental/flertal

**Spørgsmål:** hvilke huller og falske træffere har stamme-reglen som tillæg til den eksisterende søgning, og findes en enklere løsning?

**Idéer (kreativ runde; modellen gav ét samlet svar, ikke fem adskilte idéer):**
1. "Kar" → "kartoffel" som falsk træffer: **afvist**. Det er den eksisterende ordstart-regel (under 4 tegn), ikke stamme-reglen; stamme-reglen sammenligner kun hele ord. Modellen misforstod designet.
2. "-et" og verbalformer ("stege/steger"): **afvist** som irrelevant. Søgning er på ingrediens- og retnavne, ikke verber; "-et" findes via trin 1 (indeholder), hvis søgeordet er mindst 4 tegn.
3. "mos" ↔ "majsmos"/"smudge": **afvist**, vrøvl (ingen sådan ret, og under 4 tegn er det kun ordstart).
4. Flere uregelmæssige flertal ("ankler", "honningkager"): **afvist**, findes ikke som ingredienser. Dog korrekt generelt, at tabellen er kort og skal vedligeholdes (det står allerede i designet).
5. **Forhåndsberegnet lemma-indeks** (dansk lemmatizer som spaCy/Snowball, nøgleordsliste pr. ret, kun eksakt match): **afvist.** Kræver en ekstern NLP-afhængighed og et build-trin i H-scripts (`scripts/byg_*.py`), gør siden tungere og bryder klasse A. Reglen med en kort tabel er langt enklere og lige så forudsigelig. Eneste gode kerne: sammenhængen mellem søgeord og retternes egne ord kan testes automatisk (se tilføjelsen nedenfor).

**Modellens kritik (kritisk runde):** ingen. Begge kald gav tomt svar (`content: null`, kun intern tankekæde). Ingen kritik fra modellen er derfor med; vurderingen nedenfor er min egen gennemgang af reglen og er **ikke** valideret af en anden model.

## Min vurdering (egen gennemgang, ikke modellens)
Reglen er i hovedsagen god og beholder "aldrig færre træffere". Jeg fandt dog tre konkrete huller ved at følge reglen på papiret (ikke kørt mod `retter.json`):
- **Bestemte former af uregelmæssige ord falder igennem tabellen.** "kartoflerne" → fjern "erne" → "kartofl", og "gulerødderne" → "gulerødd"; begge er forskellige fra tabellens "kartoffel"/"gulerod". Tabellen skal slås op efter at *bestemt-endelsen* er fjernet, eller indeholde både "kartofler/kartoflerne" og "gulerødder/gulerødderne".
- **Ental med -e og kort stamme matcher ikke sit flertal.** "pære" (4 tegn) stammes ikke (e kræver ≥5 tilbage), men "pærer" → "pær". De er forskellige, så "pære" ≠ "pærer". Samme for "lime/limer" og "nudel/nudler" ("nudler" → "nudl", "nudel" uændret). Disse er præcis den type ental/flertal-par, designet vil løse. Løsning: samme tabel, eller sammenlign også stamme(s) med w direkte og stamme(w) med s (to-vejs, stadig hele ord).
- **"rejer" ↔ "reje"** stammes forskelligt ("rej" ≠ "reje"); dækkes kun af trin 1 i den ene retning (søger man "reje", findes "rejer" ved indeholder; søger man "rejer" finder man ikke en ret, der kun har "reje"). Skal med i de samme to-vejs-tests.
Falske træffere mellem to hele ord fandt jeg ikke i de kendte ord: mindstelængderne (3/5) beskytter "hvide", "sorte", "peber", "olie" og "smør".

**Foreslået ændring af designet (tekst til UX Designer/Ejer):**
> Tilføj til regel, trin 3: "Opslag i tabellen sker efter, at bestemt-endelsen (-erne, -ene, -en) er fjernet, så 'kartoflerne' og 'gulerødderne' ender på samme stamme som 'kartofler'/'gulerødder'. Hel-ords-sammenligningen er to-vejs: ordet er fundet, hvis stamme(s) == w, s == stamme(w) eller stamme(s) == stamme(w)."
> Tilføj til Acceptkriterier (1): "ental og flertal giver samme antal også for 'pære/pærer', 'lime/limer', 'nudel/nudler', 'reje/rejer' og for de bestemte former 'kartoflerne', 'gulerødderne'."
> Tilføj til punkt 6: "Testen kører over alle ord i retterne for alle 9 butikker og lister de par af hele ord, som den nye stamme-regel forener (men som ikke er ental/flertal af hinanden), i rapporten, så falske par ses, før udviklingen afsluttes."

## Oversigt
- Emner: 1 (UX Designer). Kald brugt: 3 af 3; kun ét gav indhold.
- Taget med: kun min egen gennemgang (tre konkrete huller i tabellen og ental med -e) og testen af forenede ordpar. Fra modellen intet brugbart ud over bekræftelsen af, at tabellen er kort og skal vedligeholdes.
- Afvist: alle modellens fem punkter (misforståelser af ordstart-reglen, irrelevante bøjninger, ekstern lemmatizer).
- Ikke tjekket: jeg har ikke kørt reglen mod `retter.json` eller `index.html`; hullerne er fundet ved at følge reglen på papiret. De to kritiske kald fejlede ("tomt svar"), og et tredje forsøg var ikke muligt. Uenighed: modellens forslag om en lemmatizer er afvist (se punkt 5).

Nyttigt: nej (modellens svar byggede på en misforståelse, og den kritiske runde gav intet; de konkrete forslag her stammer fra min egen gennemgang).
