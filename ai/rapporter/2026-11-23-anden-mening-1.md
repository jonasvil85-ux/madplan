# Anden mening 2026-11-23 (kørsel 1)

Udløst af ændring i `ai/BACKLOG.md` (commit 8525360): tre nye krav fra Ejeren. Tre emner, ét kritisk kald pr. emne (3 af 3 kald). Kreativ runde er ikke brugt: tre emner kunne ikke få både kreativ og kritisk runde inden for 3 kald, så jeg valgte at dække alle tre kritisk. Ingen persondata er sendt.

## Emne 1 – [UX] Søg i "Vælg selv": ental/flertal

**Spørgsmål:** Hvad er svagt ved ental/flertal-matching i dansk søgning, og hvad er den enkleste robuste løsning uden stemmerbibliotek?

**Idéer:** ingen (ingen kreativ runde).

**Modellens kritik (omskrevet):** Kravet nævner kun få eksempelord. Det er uklart, om reglen gælder alle ingredienser. Glemt: -e/-er/-r/-ene, bortfald af e, omlyd, sammensatte ord og genitiv-s. Foreslår en lille regelbaseret normalisering plus ordliste, der laver både ental og flertal for hvert indeksord, og matching på hele ord med `\b`.

**Min vurdering:**
- Delvist enig. Reglen bør være et lille, eksplicit sæt endelser og undtagelser, ikke en ordliste over håndplukkede ord, og testen skal dække mønstrene (e-bortfald: kartoffel/kartofler; omlyd: gulerod/gulerødder; -er: pølse/pølser; -ene/-en).
- Uenig i `\b`: `ai/regler.md` forbyder det med æøå (virker ikke korrekt på æ, ø, å). Brug `(?<![a-zæøå])…(?![a-zæøå])`.
- Afvist: ordliste over "hyppige ingredienser" som whitelist (vedligeholdelsesbyrde; kan glemme ord). Bedre: udled formerne fra ingrediensord i `retter.json` og retternes titler.
- Modellen så ikke, at kravet allerede kræver, at "ris"/"ost" ikke matcher midt i ord. Sammensatte ord (kartoffelmos) er en reel åben beslutning, som kravet ikke afklarer.

**Foreslået ændring af kravet (tekst til accept):**
- Tilføj: "Normaliseringen er en lille regel (fjern -ene/-erne/-en/-er/-e/-r/-s i slutningen, plus e-bortfald og omlyd i en kort, eksplicit undtagelsesliste), anvendt på både søgeord og de ord, der søges i."
- Tilføj: "Tag stilling til sammensatte ord: søgning på 'kartoffel' må finde 'kartoffelmos' (ordstart), men ikke 'tomatris' ved 'ris'. Skriv beslutningen i rapporten."
- Tilføj test for mindst tre mønstre (e-bortfald, omlyd, -er) og et negativt tilfælde for hvert (ris/tomatris, ost/…).
- Regex uden `\b`.

## Emne 2 – [BACKEND][H] 20 %-regel og tjek før udgivelse

**Spørgsmål:** Hvad er svagt ved en fast 20 %-tærskel for koblinger, og er 450 kr og 40 retter gode grænser?

**Idéer:** ingen.

**Modellens kritik (omskrevet):** Tærsklen ignorerer måleenhed (vægt/stk.), og små mængder af olie/krydderier fra store pakker kan give falske afvisninger. Hel and kan slippe igennem mod andebryst, hvis 200 g af 1 kg er 20 %. 450 kr og 40 retter kan gøre en butik "rød" og udelukke den. Foreslår 5 %/10 % afhængigt af enhed, pro-rata-pris, maks. pris pr. ret og en reserveavis.

**Min vurdering:**
- Uenig i den vigtigste påstand om falske afvisninger: reglen afviser, når tilbuddets mængde er under 20 % af *ingrediensens* mængde. Krydderier og olie i små mængder fra en stor pakke har tilbudsmængde langt over 100 % af behovet og afvises ikke. Modellen har vendt forholdet om.
- Enig i, at stykvarer og vægt kan blandes: hvis mængderne ikke har samme enhed, skal reglen ikke gætte, men enten springe over eller være eksplicit. Kravet bør sige, hvad der sker ved enhedsmismatch (stk. mod gram).
- Enig i, at en hel and mod andebryst kan slippe igennem, hvis tallene tilfældigvis ligger over 20 %. Derfor skal bilka-15 rettes konkret (allerede i kravet), og reglen er et sikkerhedsnet, ikke en garanti.
- Delvist enig om grænserne: 450 kr og 40 retter er forslag fra data; kravet bør sige, om et brud på tjekket stopper hele udgivelsen eller kun beholder den forrige avis for den ene butik. Afvist: "dynamisk 5 %/10 %": uden data fra de tre tidligere fejl er det opfundne tal; hold 20 % og mål, hvor mange koblinger den rammer pr. butik (før/efter-tal findes allerede i accept).
- Afvist: pro-rata-priser og "standard-avis uden pris": ændrer pris-logikken (klasse H, ud over kravet) og vil vise tal, vi ikke kan stå inde for.

**Foreslået ændring af kravet:**
- Tilføj i accept (1): "Ved forskellig enhed (stk. mod vægt) afvises ikke på tal, men koblingen markeres og tælles i rapporten."
- Tilføj i accept (3): "Fejler tjekket for én butik, beholdes den forrige avis for den butik, og siden går aldrig rød; det beskrives i rapporten, og brugeren ser ikke en tom butik."
- Tilføj i accept: "Rapportér antal koblinger, 20 %-reglen afviser pr. butik, så tærsklen kan vurderes mod data."

## Emne 3 – [TEST] Måling af dyrere ugeforslag ved flere retter

**Spørgsmål:** Hvordan designes målingen, hvilken "ny billig ret" testes, og hvad er en rimelig advarselstærskel?

**Idéer:** ingen.

**Modellens kritik (omskrevet):** "Ny billig ret" er udefineret, og advarsel-tærsklen mangler. Glemt: en baseline-kørsel uden ny ret og kontrol for andre faktorer. Foreslår en syntetisk kontrolret med fast pris og portion, kørsel pr. butik og husstand med sammensætningen gemt, advarsel ved over 3 % eller over 30 kr (det højeste), og rå tal plus procent.

**Min vurdering:**
- Enig i en fast syntetisk kontrolret (reproducerbar, uafhængig af data). Kravet siger allerede "konstrueret billig ret" i accept (2), men ikke hvordan den vælges; skriv det.
- Enig i baseline og i at gemme sammensætningen (hvilke retter blev valgt før/efter), så en stigning kan forklares.
- Uenig i tærsklen "3 % eller 30 kr": tallet er opfundet. Eksemplet fra kontrollanten (+147 kr, ca. 12,7 %) ville fanges af alt realistisk. Start med at vise alle stigninger over 0 kr i tabellen og kun markere som advarsel over fx 10 kr; justér, når første måling findes.
- Modellens risiko om "vænner sig til advarsler" er rimelig; derfor tæller kun antal tilfælde og største stigning i rapporten, ikke hver enkelt linje.
- Ikke svaret: hvordan variationsregler (køkkener) skelnes fra en fejl. Det kan målingen ikke afgøre; den skal vise sammensætningen, så et menneske kan se det.

**Foreslået ændring af kravet:**
- Tilføj: "Den nye ret er en fast, syntetisk ret (kendt pris, portion til 4, dagligvarer), lagt til for hver butik; kørsel uden den (baseline) er med."
- Tilføj: "Tabellen viser rå ugepris før/efter, forskel i kr og %, samt hvilke retter der blev valgt før og efter. Advarsel ved forskel over 10 kr (forslag; justér efter første måling)."
- Tilføj: "Rapporten tæller tilfælde og største stigning pr. husstand."

## Samlet

Modellen gav få nye idéer og misforstod emne 2 (vendte 20 %-reglens retning). Det værdifulde var enhedsmismatch, baseline-kørsel, den faste kontrolret og behovet for at afgøre, hvad der sker for brugeren, når et tjek fejler. Ikke afklaret af nogen af os: om sammensatte ord skal findes ved søgning.

Nyttigt: delvist
