# Design: "Gode tilbud"-grupperne nederst på indkøbslisten

Set på siden: `index.html` bygger grupperne Weekenden / Madpakken / Morgenmad / Frokost (`EKSTRA_TITLER`, `ekstraTilbud`, `kortNavn`). De bruger de samme rækker som tilbudsvarerne (`mob_4_trin_3.png`: afkrydsningsfelt, lille avisbillede, fed titel, grå linje, pris), men er ikke afkrydset som standard og står efter basisvarerne, dvs. langt nede.

## Problemet set fra brugeren
Tilbudsteksterne kommer fra avisen og er rå gruppetekster, fx "HØJER Røget bacon" er fint, men "COMBINO Fusilli eller penne rigate" og lignende "A, B eller C" fylder to linjer på 390 px, og man ved ikke, hvad man egentlig får. Hver gruppe har op til 10 rækker, så den nederste del af listen er en lang mur af tekst, som er svær at skimme i butikken.

## To meget forskellige løsninger
**A. Kompakt tæt liste:** én linje pr. vare (navn til venstre, pris til højre), uden billede og uden "Detaljer". Meget skimbar, men mister avisbilledet, som hjælper med at finde varen på hylden, og ligner ikke resten af listen.
**B. Samme række, kortere tekst og indrykket gruppe (valgt):** rækkens udseende er uændret, men titlen er kort og tydelig (ét varenavn, højst to linjer, aldrig afskåret midt i et ord), og hver gruppe er foldet sammen til 4 rækker med "Vis 6 flere".

**Valg: B.** Rækkerne er allerede godkendt som tryk-flader (44 px) og kendt af brugeren; problemet er teksten og længden, ikke formen. A fjerner billedet, som er det vigtigste hjælpemiddel i butikken.

## Detaljer
### Tekst pr. vare (ord for ord)
- **Titel (`.navn`):** varens eget navn, højst 40 tegn. Indeholder tilbuddet alternativer ("A, B eller C"), vises det **første** (billigste) alternativ som titel, og resten står på linjen under: "eller 2 andre slags". Opfind aldrig nye navne; brug kun de ord, avisen har.
- Afkortning sker ved sidste hele ord før 40 tegn plus "…" (i dag skæres ved tegn 40 uanset ord).
- **Linjen under (`.detalje`):** størrelse/mængde, butik: fx "500 g · Lidl". Ingen "Til …"-tekst (de er ikke til en ret).
- Pris til højre som i dag (`prisCelle`), forbrugspris vs. indkøbspris uændret; en tilbudspris er indkøbspris.

### Gruppen
- Overskrift 16 px fed + lille antal: "Weekenden – slik, sodavand og snacks · 10". Titlerne er uændrede.
- Vis de første **4** rækker; knap "Vis 6 flere" (min-højde 44 px, fuld bredde, sekundær stil, `--text-2`), derefter "Vis færre". Gruppen er lukket som udgangspunkt, hvis intet i den er afkrydset.
- Rækker i grupperne afkrydses ikke automatisk (uændret), så summen "24 varer valgt · ca. 421 kr" ikke ændres af, at man bare ruller forbi.
- Afstand: 24 px mellem grupper, 0 mellem rækker (1 px `--border` som nu). Farver: kun eksisterende tokens, prisen i `--text`; "gode-pct" (grøn) må kun bruges til en sand besparelse mod andre butikkers tilbud.

### Tilstande
- **Tom gruppe:** vises slet ikke (som i dag). **Én til fire varer:** ingen "Vis flere"-knap.
- **Indlæser/fejl:** tilbudslisten er ikke indlæst: grupperne skjules, resten af listen virker.
- **Mange:** maks 10 pr. gruppe (uændret).
- Animation: ingen (lav højde-skift uden overgang, så man ikke mister sin plads); respekterer `prefers-reduced-motion`.

### Tilgængelighed
Knappen har `aria-expanded` og `aria-controls`; rækkerne er stadig `label` + afkrydsning; fokusring 2 px `--valgt`; kontrast ≥ 4,5:1 på alle tekster; 400 px uden vandret scroll (lange ord ombrydes: `overflow-wrap: anywhere`).

## Sådan opfyldes acceptkriterierne
1. **Ingen vare over 45 tegn:** titlen er højst 40 (+ "…"), og linjen under er kortere end 45. Testes over alle varer i `tilbudsliste.grupper` for alle 9 butikker.
2. **400 px uden vandret scroll:** ombrydning og `width:100%`; testes i Chromium.
3. **Designfil med valgt løsning:** denne.

## Indvending til Ejeren
- **Accept (1) er allerede opfyldt i kode:** `kortNavn` afkorter i forvejen til 42 tegn (40 + "…"), så "ingen vare over 45 tegn" består uden, at brugeren ser nogen forbedring. Det rigtige mål er læsbarhed. Forslag til formulering: *"(1) ingen titel afkortes midt i et ord; (2) en vare med alternativer ('A eller B') viser ét navn som titel og højst én kort linje om resten; (3) hver gruppe viser højst 4 rækker, før man trykker 'Vis flere'; (4) 390–400 px uden vandret scroll; (5) summen på listen er uændret af, hvilke grupper der er foldet ud."*
- Kravet står som [A], men ændrer, hvad der vises på indkøbslisten (tekst/layout, ikke priser eller summer) – det er rigtigt som A, så længe `prisSum`, `listeLinjer` og afkrydsning ikke røres. Skriv det som Ikke-mål.
- "Motoren i trin" (næste [UX]-krav) har ingen synlig brugerflade og kræver derfor ingen designfil.
