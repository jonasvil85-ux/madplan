# Ejerens ugerapport, uge 47 (søndag 2026-11-22)

## Hvad gik godt
- Kontrollen er grøn på main hver dag (0 fejl); Vagtpost og Browser-QA er grønne. Browsertest af sammenlign og sidefod kører nu i GitHub med Chromium.
- Sidefodens tryk-flader og "Gode tilbud-grupperne" er udgivet efter tre forsøg og valideret med før/efter-tal for 9 butikker.
- Nye tilbudsaviser for alle butikker er hentet automatisk i ugens løb (uge 48 for netto, rema og lidl).

## Hvad gik galt (fakta)
- Samme tre store UX-ting ("Ét kort", "Én regel for to butikker", datafejl) har stået fast hele ugen: "Ét kort" blev rullet tilbage 17/11 og er ikke genindsendt; datafejl-grenen er afvist tre gange (to indholdsfejl, én rapportfejl). Det betyder, at ugens synlige forbedringer for brugeren kun er små (indkøbslistens grupper, sidefod).
- 30–31 små tryk-flader (under 40 px) på mobil ifølge Browser-QA; det er stort set uændret siden sidste søndag.
- 5 retter over 450 kr (andelår/and hos bilka, spar og minkoebmand); 18 ingredienser uden `ty` hos hver af rema og lidl; 313 ubrugte billeder; rema 32 og lidl 36 retter uden billede.
- Skærpet kontrol (over 450 kr er en FEJL) kan gøre main rød ved en ny avis; tilbudsrutinen fanger det ikke selv endnu (krav tilføjet).

## Gennemgang af 10 retter (tilfældigt udvalg, læst ned til ingredienser)
Oksemedaljoner med bacon og flødekartofler (bilka), Mørbradgryde med porrer og ris (rema), Pasta med ovnbagte grøntsager og mozzarella (netto), Karbonader med løgsovs (365), Kyllingefrikadeller med tzatziki (bilka), Bradepande-kyllingelår med farverige grøntsager (meny), BBQ-kyllingelår med coleslaw (kvickly), Tykstegsbøffer med portobello og pastinakmos (meny), Tunpasta med cherrytomater og oliven (rema), Kylling- og græskarsuppe med lunt brød (kvickly).
- Alle er aftensmad; køkkenerne varierer (dansk, amerikansk, middelhav, græsk). Farverige: bradepande-kylling, BBQ med coleslaw, tunpasta, græskarsuppe.
- Svagt: Karbonader og Mørbradgryde er brune uden friskt tilbehør; Pasta med grøntsager og Tunpasta har ingen tydelig mættende protein til 4 (tun 1 dåse? ikke tjekket i mængde); Tykstegsbøffer og Mørbradgryde har kun smør/fløde som sauce og få grøntsager.
- Mærkeligt: **rødvin som ingrediens (Morel Côtes-du-Rhône) i Tykstegsbøffer hos meny og bilka** – en vin til ca. 60–80 kr i en hverdagsret gør prisen urealistisk og giver et alkoholkøb i børnefamiliens indkøbsliste; "Kylling i rødvin" (spar) og "Rødvinsbraiserede oksekæber" (minkoebmand) har samme mønster. Skrevet som idé til næste datakrav (vin valgfri/udgår som ingrediens).
- Fordeling af kategorier: svin fylder 26 af 88 retter hos kvickly og 19 af 73 hos meny; vegetar kun 5 hos netto, rema, lidl og 365 (11 hos minkoebmand). "Kødfri uge" er stadig ikke mulig hos de fleste.

## Konkurrenter
`scripts/konkurrenter/` findes ikke, og skyen har intet internet, så konkurrentgennemgangen er udeladt. Det jeg ved fra tidligere revision: konkurrenter fremhæver budget, fravalg og gemte planer, og de to første har vi nu.

## Hvad brugerne sandsynligvis mangler (antagelse – ingen brugerdata)
Søgning i den lange retliste, favoritter/gemte planer, og et enkelt butiksvalg. Ingen nye feedbackbeskeder siden 17/11 (kun testbeskeder), så det er en antagelse.

## ROADMAP
Status fra revisionen 15/11: 1 (rækker), 2 (tryk-flader, delvist), 3 (fravalg: ikke udgivet), 4 (budget, udgivet), 7 (opskriftssider), 8 og 5 venter. Jeg har ikke ændret ROADMAP.md (ligger uden for mit mandat i denne kørsel); næste prioriteter er i backloggen: genindsend "Ét kort", søgning (10), derefter favoritter (5) og fravalg (3).

## Tre mål til næste uge
1. Få "Ét kort" og "Én regel for to butikker" ud igen med grøn Chromium-test (forsiden på én skærm på telefon).
2. Datafejl-grenen sluttes (kun rapportrettelse), og fejlkoblings-reglen i byg_retter.py laves.
3. Søg i "Vælg selv" designes og bygges; tryk-flader under 40 px på mobil ned fra 30 til under 15.

## Forslag til grundloven
Ingen nye. Påmindelse til Jonas: sikkerhedspunkter H2 (token i grenens kontrol), M4/M5 (politiktekst og workflow-tjek) og L2/L3 kræver hans hånd.
