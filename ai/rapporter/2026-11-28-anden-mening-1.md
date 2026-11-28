# Anden mening 2026-11-28 (kørsel 1)

Udløst af ændring i `ai/BACKLOG.md` (Ejeren præciserede kravet "Forside: Nye tilbud siden dit sidste besøg"). Ét emne; ingen nye designfiler. Modellen: gpt-oss-120b, 2 af 3 kald brugt (kreativ, kritisk).

## Emne: Forside "Nye tilbud siden dit sidste besøg" [UX] [A]
Spørgsmålet: hvordan ser en tilbagevendende bruger roligt og hurtigt, hvad der er nyt i ugens tilbud, uden at madplanen skubbes eller linjen kommer på udskriften?

### Idéer (kreativ runde)
1. **Sammenklappelig nyhedsbjælke med kort liste** – VALGT (uden "pulserende" animation, som strider mod "rolig side"). Giver svar på "hvilke retter?", ikke kun "hvor mange?".
2. Mini-preview-kort med foto, der forsvinder efter 5 sek. – AFVIST: pop-up og tidsstyring er uroligt, og kort der forsvinder af sig selv kan overses.
3. Tidslinje med prikker pr. butik – AFVIST: kræver scroll og forklaring, ingen klar værdi for en travl forælder.
4. AR-nyhedssky via kamera – AFVIST: kamera-tilladelse, langt uden for målgruppe og pris.
5. "Tilbud forsvandt siden sidst" + genopliv-knap – AFVIST: tilbud udløber ugentligt, så tabte tilbud kan ikke købes; "genopliv" ville vise tilbud, der ikke gælder, og er uærligt. Kun en kort tanke tages ikke med.

### Modellens kritik (kritisk runde, omskrevet)
- "Ny" defineret på navn tæller en omdøbt ret som ny.
- Hvad sker der ved mere end ca. 8 nye retter?
- Hvis `localStorage` er blokeret/fuld: skal linjen skjules helt; ellers kan "0" eller "?" vises.
- Linjen skal skjules i print (`@media print`).
- Tilgængelighed (ARIA, tastatur).
- Foreslog hash af ingredienser/version-ID i stedet for navn.

### Min vurdering
- **Omdøbte retter: delvist enig.** Navn er den eneste stabile nøgle, vi har (id'er er positionelle, jf. kontrollantens afvisning). Hash af ingredienser er ikke bedre: små ændringer i mængder ville give falske "nye". Jeg tager: sammenlign på normaliseret navn (småt, trimmet mellemrum), og kald det "nye retter", ikke "nye tilbud".
- **Mere end 8: enig.** Vis de første 8 og "+ N flere" (ingen scroll i listen).
- **localStorage blokeret/fuld: enig.** Kravet siger "virker uændret", men præciser: ingen linje vises, ingen fejl. Samme når tallet er 0: ingen linje.
- **Print: uenig i, at det mangler.** Det står allerede som accept (7) med test i `nyt_browser.js`; modellen så kun mit korte resumé. Ingen ændring.
- **Tilgængelighed: delvist enig.** Den generelle formulering er tom, men konkret: linjen er en rigtig `<button>` med `aria-expanded`, og lukkeknappen har tekst-label. Det er billigt og testbart.
- Udvidelsen (liste ved tryk) er min egen tilføjelse fra idé 1; den øger omfanget lidt. Hvis kontrollanten finder det for stort til ét trin, så del i trin 1 (linje + tal) og trin 2 (liste).

### Foreslået ændring af kravet (tekst til Ejeren)
Tilføj til Krav: "Et tryk på linjen folder en liste ud med ret-navn og butik (højst 8, derefter '+ N flere'); listen skubber ikke madplanen i lukket tilstand og har ingen animation. Linjen er en `<button>` med `aria-expanded`. Sammenligningen bruger normaliseret retnavn pr. butik; teksten siger 'nye retter'."
Tilføj til Accept: "(8) blokeret eller fuld `localStorage` samt tallet 0 giver ingen linje og ingen fejl; (9) mere end 8 nye retter viser 8 og '+ N flere'; (10) linjen kan betjenes med tastatur."
Ikke-mål: "tilbud der er forsvundet", billeder i listen.

Ikke tjekket: om `retter.json` indeholder nok til at vise butik pr. ret uden ekstra data (kontrolleres af udvikleren).

Nyttigt: delvist (liste ved tryk, "+ N flere" og blokeret-localStorage-præciseringen var nyttige; resten kendte vi).
