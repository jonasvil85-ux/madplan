# Dagsrapport 2026-11-21
**Siden i dag:** Sund med advarsler. Udgivet side grøn (Vagtpost 07:00 UTC, begge domæner), kontrol bestået med 0 fejl og 9 advarsler.
## Ændret på siden (slået sammen)
- Gode tilbud-grupperne (ai/2026-11-21-ux, klasse H, forsøg 3, 10e1bd7): korte titler ved helt ord, foldet til 4 rækker, "Vis færre" virker med afkrydset vare. Godkendt af kontrollanten 06:59 UTC efter skærpet validering; main BESTÅET før og efter, inkl. regression, budget, sammenlign og Chromium-testene.
- Nye tilbudsaviser fra Netto, uge 48 (065e06f, 05:12 UTC) og billeder til nye retter (automatisk).
## Afvist eller rullet tilbage
- ai/2026-11-21-backend (datafejl, H): afvist af kontrollanten, kun proceduremæssigt (forkert forklaring i rapporten, 6 slettede retter ikke 5, før/efter-tabel ufuldstændig). Indholdet bestod alle tjek; tæller ikke som forsøg. Se ai/rapporter/2026-11-21-kontrol.md.
- ai/2026-11-20-datafejl: afvist 20/11 (ny type hakket_kod rammer rent kød), ét forsøg tilbage. Ingen tilbagerulning i dag.
## Data
- Retter (568 i alt): Meny 73, Bilka 83, Kvickly 88, Spar 73, Netto 60, Rema 50, Lidl 50, 365discount 50, minkøbmand 41. `retter.json` genereret 2026-11-21 05:11 UTC.
- Uden billede: 34 (alle Netto, nye retter; kræver lokal billedkørsel). 252 billeder bruges ikke.
- Feedback fra brugerne: ingen nye beskeder siden 17/11 (to testbeskeder, 0 brugbare). Ingen HASTER.
## Sundhed
- Kontrol: RESULTAT: BESTÅET (0 fejl, 9 advarsler), regression, budget, sammenlign og tilbudsgrupper bestået. Udgivet side: nået, matcher main (HELBRED, 568 retter). Browser-QA GRØN: 0 JS-fejl, intet vandret scroll, 30 små tryk-flader på mobil og 31 på desktop.
- Advarsler af betydning: 5 retter over ca. 490 kr (andelår og helstegt and hos Bilka, Spar og minkøbmand); Meny-svinemørbrad mangler ingrediens; 34 Netto-retter uden billede; sidefodens Chromium-test kunne ikke køres i min session (Playwright mangler).
- Ikke tjekket af mig: udseende i browser, kontrast, tastatur, iOS Safari.
## I morgen
- Øverste krav: ret kendte datafejl (Backend/data-udvikleren, H, sidste forsøg), derefter "Ét kort: Hvor handler du?" og "Én regel for to butikker".
## Til prøve hos Jonas
- Intet nyt som UX: Gode tilbud-grupperne er ændret i udseende (kortere titler, foldet til 4 rækker). Ejerens rapport har dog ikke meldt den som prøve-klar; kan kigges på, hvis du alligevel har lyst.
## Til Jonas
- Intet nyt. Sikkerhedspunkter H2, L2/L3, M4/M5 afventer stadig dig (jf. Ejeren).
