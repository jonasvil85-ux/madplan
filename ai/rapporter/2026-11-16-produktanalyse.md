# Produktanalyse 2026-11-16 (CTO)

## Hvorfor skulle nogen vælge Måltidsjagten?
Ærligt svar i dag: fordi den er gratis, uden login og regner på ni kæders aviser på én gang. Det er det eneste, vi har, som de andre ikke har samlet.

**Konkurrenter** (kilde: app-butikssider og én reklamepræget artikel, ikke afprøvet af os):
- **Goma**: gratis, priser fra næsten alle butikker hver nat, madplaner ud fra ugens billigste ingredienser, delt indkøbsliste. Den farligste konkurrent: samme løfte som os, men som app.
- **Mambeno**: madplan ud fra REMA 1000's tilbud, allergier, diæt og fravalg, levering. Abonnement efter 30 dage.
- **Valdemarsro, Hofretter, Maddie, Nem Madplan, Madopskrifter.nu**: madplaner og indkøbslister, men ikke bygget på tilbud (eller kun delvist).
- **eTilbudsavis**: aviser og liste, ingen madplan.

## Største svagheder (kritisk)
1. **Brugeren skal selv finde ud af, hvor det er billigst.** Forsiden viser én butik ad gangen (standard: den billigste). Hvad ugen koster i de otte andre, skal man klikke sig frem til. Det er netop det spørgsmål, en tilbudsside skal besvare på første skærm, og det Goma reklamerer med.
2. **Forslaget passer ikke til alle familier.** Ingen fravalg (svin, fisk, laktose …) og intet budget. Mambeno har fravalg. Vores gren er bygget, men parkeret efter rød-hold-fund.
3. **Ingen grund til at komme tilbage.** Ingen gemt uge, ingen favoritter, ingen påmindelse, når nye aviser kommer.
4. **Vælg selv er en endeløs liste** (171 retter, 63.000 px på mobil, ingen søgning).
5. **Vi ved ikke, hvad brugerne gør.** Ingen måling af frafald.

## De fem vigtigste forbedringer (efter brugerværdi)

### 1. Sammenlign alle butikker på forsiden
- **Problem:** "Hvor skal jeg handle i denne uge?" kræver i dag mange klik.
- **Løsning:** en rangeret liste over alle 9 butikker med ugens pris for netop din husstand, besparelsen mod normalpris og andel på tilbud; den billigste markeret; tryk vælger butikken. Under listen: den bedste kombination af to butikker, hvis den sparer mindst 30 kr. Tallene regnes i baggrunden, butik for butik, og vises efterhånden.
- **Værdi:** besvarer kernespørgsmålet på første skærm; synliggør besparelsen (kan være 200+ kr om ugen mellem dyreste og billigste butik).
- **Størrelse:** M (frontend; genbruger den eksisterende beregning, ingen ændring af priser).
- **Måling:** andel af besøg, hvor brugeren vælger en anden butik end standarden; tid til "Brug forslaget"; fejlfri visning i Browser-QA.

### 2. Fravalg og budget (færdiggøres)
- **Problem:** forslaget er ubrugeligt for familier, der ikke spiser svin/fisk/laktose, og ingen kan sige "højst 600 kr".
- **Løsning:** findes på grenen `ai/2026-11-15-fravalg-budget`; budgetdelen er godkendt i indhold, fravalg mangler mayonnaise/remoulade (æg), pesto (mejeri) og blandet fars.
- **Størrelse:** S (rettelser) + ny gren for budget alene.
- **Måling:** andel med mindst ét fravalg; 0 brud i testen over hele puljen.

### 3. Gem min uge og favoritter
- **Problem:** næste uge starter man forfra.
- **Løsning:** "Gem ugen" (lokalt, og på konto hvis logget ind), stjerne på retter, favoritter vises først i "Vælg selv" og vægtes op i forslaget.
- **Størrelse:** M–L (rører konto/Supabase: sikkerhedsagenten først).
- **Måling:** andel tilbagevendende brugere inden for 14 dage.

### 4. Søg og filtrér i "Vælg selv"
- **Problem:** 171 retter uden søgning.
- **Løsning:** søgefelt (ret og ingrediens), filtre (tid under 30 min, børnevenlig, billigst først), "Vis 24 flere".
- **Størrelse:** M. **Måling:** sidelængde, tid til at vælge 7 retter.

### 5. Måling af frafald (privatlivsvenlig)
- **Problem:** vi prioriterer i blinde.
- **Løsning:** tæl anonymt fem hændelser (butik valgt, Brug forslaget, liste åbnet, seddel åbnet, delt) uden cookies eller persondata.
- **Størrelse:** S–M (rører privatliv: grundlov og sikkerhed).
- **Måling:** tragt fra forside til seddel.

## Valgt: nr. 1, Sammenlign alle butikker
Den største værdi, fordi den gør det, en tilbudsside er til: viser hvor pengene spares, med det samme. Den kræver ingen ny data, ingen konto og ingen ændring af prisberegningen, så den kan bygges og valideres nu. Fravalg/budget (nr. 2) færdiggøres parallelt som små rettelser.

Holdet: Ejeren (krav, se BACKLOG), UX-designeren (designfil), frontend-udvikleren (bygger på gren), kontrollanten (uafhængig test, må afvise), SEO/vækst (vurderer på torsdag, om sammenligningen kan blive en søgbar side "billigste supermarked i denne uge").
