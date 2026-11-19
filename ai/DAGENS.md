# Dagsrapport 2026-11-19
**Siden i dag:** Sund med advarsler. Udgivet side grøn (Vagtpost 07:03 UTC, Browser-QA), kontrol bestået (0 fejl, 11 advarsler); udseendet er kun målt af Browser-QA, ikke set af mig.
## Ændret på siden (slået sammen)
- Data: tilbudsrutinen (6b05f36, 05:13 UTC) hentede nye aviser (365discount uge 47, Lidl suppleret med weekendavis). 483 retter, op fra 479. Kontrollant: main grøn, regression bestået. Ingen kodeændring i dag.
## Afvist eller rullet tilbage
- ai/2026-11-19-gode-tilbud-grupper (H, forsøg 1): afvist. Titlen er første led i "A, B eller C", så varetypen forsvinder på sedlen ("Daim (18 kr)", "Kartofler (15 kr)"); før/efter-tal for 9 butikker mangler.
- ai/2026-11-19-datafejl (H): afvist igen, tæller ikke som nyt forsøg. Koden i scripts/ er uændret; stadig 16 Netto-ingredienser uden type (accept 1).
- Stadig rullet tilbage fra 17/11: "Hvor handler du?" (090801b). Ingen ny tilbagerulning i dag.
## Data
- Retter pr. butik: netto 64, bilka 58, kvickly 60, meny 53, spar 53, rema 50, lidl 50, 365 50, minkoebmand 45 (i alt 483). Retter uden billede: 30, alle hos 365 (nye retter; kræver lokal billeder.py). Ubrugte billeder: 214 (188 i går).
- Feedback fra brugerne: 0 nye beskeder (FEEDBACK.md: seneste 17/11, 2 testbeskeder, 0 brugbare). Ingen HASTER.
## Sundhed
- Kontrol: RESULTAT: BESTÅET (0 fejl, 11 advarsler). Udgivet side: nået, matcher main ja (begge domæner OK, 8/8 billeder; Browser-QA GRØN, 0 JS-fejl, intet vandret scroll, 30 små tryk-flader på mobil). Advarsler af betydning: 5 dyre andretter (496–759 kr for hele retten), Kvickly svinemørbrad mangler på ingrediensliste, 25 Netto-ingredienser uden ty, 30 retter uden billede (365), 214 ubrugte billeder. Ikke tjekket: sidefodens Chromium-test i min session (Playwright mangler; kontrollanten kørte den i Actions), farvekontrast, tastatur, login.
## I morgen
- Øverst: "Ret kendte datafejl" (DATA, H, backend-udvikleren – skal rette de 16 ty-mangler); derefter "Ét kort: Hvor handler du?" genindsendes (frontend), og gode-tilbud-grupper skal rettes.
- SEO-rapport uge 47 er læst: 171 af 193 opskriftstitler er over 60 tegn; "10 supermarkeder" i tekster mod 9 butikker; 5 sider med over 1000 kcal pr. portion. Ejeren tager det op i backloggen (ikke målt mod rigtige søgedata).
## Til prøve hos Jonas
- Intet nyt udgivet siden sidefoden på mobil (spørgsmålene står i dagsrapporten 2026-11-18).
## Til Jonas
- Grundlovs-punkter fra Sikkerhedsagentens uge 47 afventer dig: H2, L2/L3, M4/M5 (se ai/rapporter/2026-uge-47-sikkerhed.md). Ejeren har ingen nye forslag.
