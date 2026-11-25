# Anden mening 2026-11-25 (kørsel 1)

Udløst af: `ai/BACKLOG.md` (ny linje "Skærpet 2026-11-25" under kravet "Søg i Vælg selv: ental/flertal og småfejl"). Ingen ændringer i `ai/design/`. Kun ét emne; det øvrige i diffen var Ejerens rapport. Rolle: Product Owner. Kald brugt: 2 af 3 (kreativ + kritisk).

## Emne 1: Søg i "Vælg selv" – ental/flertal uden falske træffere (sidste forsøg 3)
**Spørgsmål:** Hvordan matcher man ental/flertal begge veje i dansk uden falske træffere midt i ord ("ris"/"tomatris"), og uden at miste "rejer" → "kutterrejer"?

### Idéer (runde 1, kreativ)
Modellen gav ét samlet forslag i stedet for fem adskilte idéer (svaret blev i øvrigt skåret af i slutningen).
- **Token-indeks over normaliserede ordstammer (ét opslag pr. stamme):** AFVIST. Det er et præcist ordopslag og ville ødelægge "rejer" → "kutterrejer" og al delstrengs-søgning, som kravet netop kræver bevaret. Der er desuden en ny datastruktur at holde ved lige.
- **Normalisér både søgeord og tekst med få suffiksregler + kort liste over uregelmæssige par:** DELVIST VALGT. Listen over uregelmæssige par er brugbar (kartoffel/kartofler, gulerod/gulerødder m.fl.). Men modellens suffiksregel er farlig: den fjerner bare "-e/-en/-er" og ville gøre "køber" til "køb" og "hønen" til "høn". Vi udvider derfor kun søgeordet til en mængde former og normaliserer ikke teksten.
- Fjernelse af diakritik via NFD: AFVIST. Den rører ikke æ/ø/å og er uden betydning; "aa → å" er ikke en brugerønske.

### Modellens kritik (runde 2, kritisk; svaret blev også skåret af)
- Korte søgeord (2-3 bogstaver: ris, ost, æg, mel, bær) får ingen beskyttelse mod at ramme ord, de bare er starten på: "risotto", "ægte", "mellem", "bæredygtig".
- Match i slutningen af sammensatte ord (kutterrejer) findes ikke i "helt ord eller ordstart"-reglen, hvis man ikke udtrykkeligt tillader det.
- Der kom ingen konkret regel for, hvornår slut-match er tilladt.

### Min vurdering
- **Enig** i, at korte ord er farlige. Mel/mellem, æg/ægte er reelle risici i en ret-liste. Eksemplerne med "bæredygtig" og "melodi" er irrelevante for madretter; "oste" som falsk træffer er ikke falsk (det er flertal af ost).
- **Delvist enig** om "risotto" for "ris": en risotto er en risret, så en træffer er næppe forkert. Det er et spørgsmål til Jonas som bruger, ikke noget, holdet skal gætte.
- **Enig** i, at slut-match mangler en klar regel, og modellen leverede den ikke. Forslaget herunder er mit eget, ikke modellens.
- **Uenig** i modellens tokeniserede indeks og suffiksfjernelse på begge sider (se ovenfor).

### Foreslået ændring af kravet (konkret tekst til punkt 7-8)
Tilføj til de skærpede acceptkriterier:
- (10) Søgeordet udvides til en mængde former (selv + ental/flertal/bestemt form via få suffiksregler og en kort liste over uregelmæssige par: kartoffel/kartofler, gulerod/gulerødder, pære/pærer, lime/limer, nudel/nudler, reje/rejer). Teksten ændres ikke.
- (11) Hver form matcher som helt ord eller ordstart. **Match i slutningen af et sammensat ord ("kutterrejer") kræver, at formen er mindst 5 bogstaver.** Så finder "rejer" "kutterrejer", mens "ris" (3) aldrig finder "tomatris".
- (12) Former på højst 3 bogstaver (ris, ost, æg, mel, løg, bær, ål) matcher kun som hele ord eller bøjninger af hele ord, så "mel" ikke rammer "mellem" og "æg" ikke "ægte".
- (13) Test med negative eksempler: "ris" ↔ "tomatris"/"risotto" (aftales: ja/nej), "mel" ↔ "mellem", "æg" ↔ "ægte", "hvide bønner" ↔ "hvidløg"; og positive: "rejer" ↔ "kutterrejer", "kartoflerne" ↔ "kartoffel", "løgene" ↔ "løg".
- (14) Hver ret kommer højst med én gang, og antallet for ental og flertal er ens (testes for alle ordpar).
Spørgsmål til Jonas (som bruger, i almindeligt sprog): Skal en søgning på "ris" også finde retten "Risotto"?

### Begrænsninger
Svarene var skåret af, så en del af modellens tabeller mangler. Tredje kald blev ikke brugt. Forslagene er ikke afprøvet i kode eller browser.

**Nyttigt: delvist** – modellen bekræftede kun risikoen ved korte søgeord og kom ikke med en brugbar regel for slut-match; reglen om mindst 5 bogstaver og de korte ords særregel er mine egne.
