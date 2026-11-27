# Dagsrapport 2026-11-27
**Siden i dag:** Advarsel: main er RØD (kontrol.py FEJLET, 4 fejl). Fire retter koster over 450 kr efter tilbudsrutinens uge 49-aviser. Den udgivne side er grøn og identisk med main, så de fire retter vises nu for brugerne.
## Ændret på siden (slået sammen)
- Nye tilbudsaviser uge 49: meny, bilka, kvickly, spar, minkoebmand (dc0d0ec, tilbudsrutinen, 05:11 UTC). Ingen kontrollant-sammenlægninger de sidste 24 timer.
## Afvist eller rullet tilbage
- ai/2026-11-27-dyre-retter (klasse H, forsøg 1): afvist. Spar-andelårsretterne er stadig koblet til en andebryststeg (P29), så indkøbslisten viser forkert vare. Rettelse: fjern de to spar-retter.
- ai/2026-11-27-nye-tilbud (klasse A, forsøg 1): afvist. Linjen "nye tilbud siden sidst" kommer med på udskriften af indkøbssedlen. Logikken er ellers solid.
- ai/2026-11-26-monotoni: uændret efter afvisning (forsøg 1; målefejl). Ingen tilbagerulning, da fejlen kommer fra data.
## Data
- Retter pr. butik: netto 60, meny 93, bilka 82, rema 56, kvickly 94, lidl 49, 365 50, spar 92, minkoebmand 77 (653 i alt). Retter uden billede: 3 (365). 336 billeder bruges ikke (advarsel).
- Feedback fra brugerne: ingen nye beskeder siden 2026-11-25 (ai/FEEDBACK.md). Ingen HASTER-punkter.
## Sundhed
- Kontrol (kørt af mig): RESULTAT: FEJLET (4 fejl, 5 advarsler). Udgivet side: nået, retter.json matcher main (HELBRED GRØN 07:01 UTC; BROWSER GRØN, 0 JS-fejl, intet vandret scroll). Advarsler: rema og lidl har 18 tilbudsingredienser uden typeoplysning; 30 (mobil) / 31 (desktop) små tryk-flader; sidefodens Chromium-test kunne ikke køres her.
## I morgen
- Øverst: HASTER, ret de fire dyre retter (DATA, H): fjern de to spar-andelårsretter og ret bilka. Tager Backend-udvikleren (forsøg 2).
## Til prøve hos Jonas
- Intet nyt udgivet siden sidste rapport (søgning i "Vælg selv" fra i går kan stadig prøves).
## Til Jonas
- Ejerens afventende forslag til grundloven: tilbudsrutinen bør køre byg_retter.py og kontrol.py før commit; det ville have forhindret dagens røde main. Sikkerhedspunkterne H2, N1, N2, M4, M5, L2/L3 afventer også dig.
- Ikke tjekket af mig: udseende i browser, skærmbilleder, mørkt tema, siden live.
