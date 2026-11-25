# Dagsrapport 2026-11-25
**Siden i dag:** Sund. Vagtpost og Browser-QA er GRØNNE, og kontrol.py består (0 fejl, 4 advarsler).
## Ændret på siden (slået sammen)
- Test af selve byggeren (70dd54e, klasse A, kun test): bygget stopper nu, hvis en ret kun er koblet til tilbud med 10 % dækning. Kontrollanten slog den sammen (9c31d33) efter kontrol.py, regression og 8 rød-hold-forsøg. Brugeren ser ingen forskel.
## Afvist eller rullet tilbage
- ai/2026-11-25-ux ("Søg i Vælg selv: ental/flertal", forsøg 3): afvist to gange i dag. Indholdet består alle kontroller; rapporten mangler ugepris og indkøbslinjer pr. butik (accept 9). Ingen tilbagerulning.
## Data
- Ingen nye aviser eller retter fundet i dagens commits. Retter pr. butik: netto 60, meny 73, bilka 80, rema 56, kvickly 88, lidl 49, 365 49, spar 71, minkoebmand 40. Retter uden billede: 0. 313 billeder bruges ikke (advarsel).
- Feedback fra brugerne: ingen nye beskeder siden 2026-11-23 (ai/FEEDBACK.md uændret; ikke selv genkørt i dag). Ingen HASTER-punkter.
## Sundhed
- Kontrol: RESULTAT: BESTÅET (0 fejl, 4 advarsler). Udgivet side: nået, matcher main (HELBRED GRØN 08:45 UTC). Browser-QA GRØN (0 JS-fejl, intet vandret scroll).
- Advarsler: rema og lidl har 18 tilbudsingredienser uden typeoplysning (ty); 313 ubrugte billeder; sidefodens Chromium-test blev ikke kørt her (ingen Playwright).
## I morgen
- Øverst: søgning i Vælg selv (UX, forsøg 3, det sidste). Frontend-udvikleren skal kun rette rapporten med ugepris og indkøbslinjer.
## Til prøve hos Jonas
- Intet.
## Til Jonas
- Intet nyt. Uændret afventende: sikkerhedspunkterne H2, M4, M5, L2/L3 og forslaget om, at tilbudsrutinen kører byg_retter.py og kontrol.py før commit.
- Ikke tjekket af mig: udseende i browser, skærmbilleder, mørkt tema.
