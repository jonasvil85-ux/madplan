# Status for AI-holdet

**2026-11-17: "Hvor handler du?" (090801b) og flueben-CSS'en (4211735) er RULLET TILBAGE** – main var rød (kontrol.py FEJLET i Chromium: sammenlign_browser.py går ned på de nye målinger fra sammenlign_side.js). Siden er tilbage på butiksvalget fra før 2026-11-16 kl. 14.

HELBRED.md: GRØN (2026-11-20 05:16 UTC, begge domæner OK, main 9eac79c). BROWSER.md: GRØN (2026-11-20, 0 JS-fejl, intet vandret scroll). Egen måling 2026-11-20: madplan-blue.vercel.app 200, sw.js v6, retter.json identisk med main.

Sidst kontrolleret: 2026-11-20, kørsel 3 (planlagt). Main BESTÅET (0 fejl, 10 advarsler) inkl. regression og sammenlign i Chromium; sidefodens Chromium-test ikke kørt (Python-Playwright mangler). HELBRED/BROWSER GRØN. Ingen tilbagerulning. Intet slået sammen – ingen gren ændret siden kørsel 2.
I dag: ai/2026-11-19-gode-tilbud-grupper AFVIST (forsøg 2, H: "Vis færre" virker ikke med afkrydset vare). ai/2026-11-20-datafejl AFVIST (forsøg 2, H: ny type hakket_kod rammer også rent okse-/grisekød → hele gruppeteksten i indkøbslisten). Øvrige grene uændrede. Se ai/rapporter/2026-11-20-kontrol.md (kørsel 1 og 2).

## Udgivet uden forudgående kontrol – SKAL efterprøves ved næste kørsel
(ingen – 090801b og 4211735 efterprøvet og rullet tilbage 2026-11-17)

## Afvist – udvikleren retter
- ai/2026-11-20-datafejl (881b85f, forsøg 2 – udvikleren kalder det 3, men 2026-11-19 talte ikke; klasse H): AFVIST 2026-11-20 – ét forsøg tilbage. Indholdsfejl (rød-hold): `bibliotek_typer.py` hakket_kod (`hakket (?:dansk )?(?:okse|gris|svine)[a-zæøå -]*kød`) rammer også rent kød; "hakket oksekød" får ty [hakket_okse, hakket_kod], og overskriften "Dansk hakket oksekød 4-7% eller dansk hakket grise- og oksekød 8-12%" vises i hele sin længde (main: kun oksekødet). Bestået: kontrol (0 fejl, 3 adv.), regression, budget, sammenlign, Chromium, genbygning, før/efter genskabt (meny −3, lidl +4,9, minkoebmand −47,5 kr i 2+2; øvrige uændrede), accept (1) og (2), alle 1499 eksisterende listevisninger uændrede. Afløser ai/2026-11-19-datafejl og ai/2026-11-16-datafejl.
- ai/2026-11-19-gode-tilbud-grupper (8ca3ab7, forsøg 2, klasse H): AFVIST 2026-11-20 – ét forsøg tilbage. Forsøg 1's fejl er rettet (titlen er avisens egen tekst, afkortet). Indholdsfejl: index.html renderListe, `aaben = ekstraAaben.has(id) || linjer.some(valgt)` – fold en gruppe ud, afkryds en vare, tryk "Vis færre": intet sker (gentaget i Chromium). Bemærkning: afkortningen springer et ord over, der passer før et komma ("Dan Cake juleromkugler…" i stedet for "…, havregrynskugler…"). Bestået: kontrol, regression, før/efter (kun titeltekst i ekstra-grupperne, 9 butikker), 400 px målt af kontrollanten. Forsøg 1 (8b91af3) afvist 2026-11-19: titlen var første alternativ ("Daim (18 kr)").
- ai/2026-11-17-sidefod-tryk-flader (8fa5c7d, forsøg 1, klasse A) – AFLØST: forsøg 2 (ai/2026-11-18-sidefod-tryk-flader) slået sammen 2026-11-18.
- ai/2026-11-17-browsertest-sky (0b558ff, forsøg 1, klasse A) – AFLØST: forsøg 2 (ai/2026-11-18-browsertest-sky) slået sammen 2026-11-18. Oprindelig afvisning: node-reserven gør enhver fejl efter opstart (timeout, side der ikke bliver klar, undtagelse i testen) til "IKKE KØRT" exit 3, som kontrol.py kun giver en advarsel for – en ødelagt forside giver BESTÅET i skyen. Gentaget: `SAMM` omdøbt i en kopi → exit 3 (Python-Playwright: exit 1). Kun manglende playwright/Chromium må give exit 3. Resten bestået (kontrol BESTÅET, accept 1–3, tekstmutation fanges).
- "Hvor handler du?" (090801b + 4661112, forsøg 1, klasse H): rullet tilbage, se øverst. Selve sidens tjek gav fejl = []; ret runneren (eller tag den med fra browsertest-sky, når den er rettet) og indsend som gren. Kontrol.py skal være BESTÅET med Playwright.
- ai/2026-11-19-datafejl (24ca7f3, klasse H) – AFVIST 2026-11-19, tæller IKKE som nyt forsøg (stadig forsøg 1 brugt): koden i scripts/ er byte-identisk med 4f2dd38; kun data genbygget og før/efter-tal tilføjet (H-punkt 2 nu opfyldt – før/efter genskabt af kontrollanten, identiske priser og linjer i 9 butikker). Mangler: accept (1) – 16 ty-advarsler hos Netto (mayonnaise, remoulade, risottoris, tacoskaller, pizzasauce, sild m.fl.). Rød-hold: "Jalapeño ost", "Mayonnaise med mango" og "Hakket svinekød og kalv" får forkert type. Afløser grenen nedenfor.
- ai/2026-11-16-datafejl (4f2dd38, forsøg 1, klasse H; uændret også 2026-11-17 – intet nyt forsøg): før/efter-tal mangler ugepris og indkøbslinjer for de 9 butikker (H-punkt 2); dagens H-plads var brugt (H-punkt 5); accept (1) kun delvist (16 ty-advarsler tilbage). Bygget korrekt (kun tidsstempel ændres ved genbygning).

## Parkeret – Ejeren har dem (to forsøg brugt)
- ai/2026-11-15-fravalg-budget (7ad8866, klasse H): fravalg lader stadig igennem: mayonnaise/remoulade under "Æg" (6 butikker), pesto under "Mælkeprodukter", "hakket kød 8-12%" (svin+kalv) under "Okse og kalv". Budgetdelen er i orden (8/9 under 600 kr) – foreslås bygget som egen gren.
- ai/2026-11-16-mobil-tryk-flader (cccb0f6, klasse A): forsiden 36 → 1 element under 40 px, men "Om Måltidsjagten" i sidefoden er 95 × 14 px, og accept (4) (madplan-hero.png 405 KB) er ikke gjort. Forslag: flyt (4) til eget H-krav. Erstatter ai/2026-11-15-mobil-tryk-flader.

## Rullet tilbage
- 2026-11-17: 4211735 (flueben, e202c61) og 090801b "Hvor handler du?" (4aab106), udgivet 2026-11-16 uden forudgående kontrol. Årsag: kontrol.py FEJLET på main (TypeError i sammenlign_browser.py linje 46; før 090801b bestået). Efter tilbagerulning: BESTÅET. Se ai/rapporter/2026-11-17-kontrol.md.

## Seneste sammenlægninger
- 2026-11-18: ai/2026-11-18-sidefod-tryk-flader (A, merge 3104489, forsøg 2): sidefoden på mobil er en rolig liste med 48 px rækker, 15 px tekst, uden opacity; +/– ved teksten på desktop; ny Chromium-test sidefod_browser.py i kontrol.py. Accept (3) "færre end 23" vurderet efter hensigt (basis forsvandt med tilbagerulningen; 33 → 30) – Ejeren bør omformulere. Opfølgning: "Om" 39 px på desktop, ubetingede hover-regler, testen har ingen node-reserve. Til brugerprøve: ja. Se ai/rapporter/2026-11-18-kontrol.md, kørsel 2.
- 2026-11-18: ai/2026-11-18-browsertest-sky (A, 3b28eb5, forsøg 2; lineær – se rapporten): browsertesten kører i skyen med node-Playwright som reserve; kun manglende Playwright/Chromium giver IKKE KØRT, sidefejl giver FEJLET. 6 rød-hold-forsøg, revert-prøve. Se ai/rapporter/2026-11-18-kontrol.md.
- 2026-11-16: ai/2026-11-16-budget (H, f1c3024, forsøg 3): budget for ugens aftensmad i Dine valg. Skærpet validering bestået (før/efter identisk uden budget for 9 butikker × 3 husstande, 7/9 under 600 kr, 5 rød-hold-forsøg, revert-prøve). Dagens 3. H. Opfølgning: "600 kr – 1 kr over 600 kr"-beskeden, afvigelse fra designfilens chips, "højt budget ændrer intet" gælder kun én butik.
- 2026-11-16: ai/2026-11-16-sammenlign-butikker (H, 25d3cb7, forsøg 2): rangeret liste over 9 butikker og ærligt to-butiks-forslag. Skærpet validering bestået (før/efter byte-identisk for 9 butikker × 3 husstande, 6 rød-hold-forsøg, revert-prøve). Dagens 2. H.
- 2026-11-16: ai/2026-11-15-indkoebsliste-raekker (H, 8c2e4a7): korte rækker med Detaljer-link. Skærpet validering bestået (linjer og summer uændrede i alle 9 butikker, rød-hold, revert-prøve).
- 2026-11-15: ai/2026-11-15-opskriftssider (H, 384f5d1): 193 opskriftssider, oversigt og sitemap. Skærpet validering bestået (før/efter byte-identisk for alle 9 butikker, rød-hold, revert-prøve).
- 2026-11-15: ai/2026-11-15-regressionstest (A, kun test): regression.py/.js + facit + frossen datakopi; kaldes af kontrol.py. Klasse H kan nu valideres efter den skærpede proces.
- 2026-11-15: ai/2026-11-15-kontrol-jsonld (A, kun test): kontrol.py springer JSON-LD-blokke over i JS-tjekket.

## Kendte begrænsninger
- Kontrollantens sky-session har lokal Chromium (Playwright via node) og kan måle en gren mod en lokal server; eksterne billeder (butikslogoer, tilbudsbilleder) blokeres dér.
- Skyen har ingen browser. Browser-QA (GitHub) måler og tager skærmbilleder af siden (`ai/BROWSER.md`, grenen `skaermbilleder`), men klikker kun et fast flow.
- Regressionstesten dækker ikke DOM/udseende, simByt, andre husstande end 2+2/2+0 eller live-data (se udviklerrapporten 2026-11-15).
- Brugerfeedback (Supabase) kan holdet ikke læse.
- Skyrutinerne kan ikke hente den udgivne side (netværkspolitikken afviser den). Vagtposten er derfor flyttet til GitHub-handlingen "Vagtpost", som skriver `ai/HELBRED.md`; rutinerne læser den fil.
- Skyrutinerne kan ikke slette grene på GitHub; Vagtposten rydder sammenlagte `ai/*`-grene.
