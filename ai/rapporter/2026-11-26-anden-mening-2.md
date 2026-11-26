# Anden mening 2026-11-26 (kørsel 2)

Udløst af: `ai/BACKLOG.md` (to nye krav tilføjet fra SEO/vækst, uge 48). Ingen ændringer i `ai/design/`.

## Resultat: intet nyt at validere – modellen er ikke kaldt (0 af 3 kald)
De to nye krav er:
1. "Forside: Nye tilbud siden dit sidste besøg" ([UX] [A], hypotese)
2. "Opskriftsside: tydelig overgang til ugens tilbud" ([UX] [A], hypotese)

Begge står som krav nr. ca. 15 og 16 i backloggen (fra linje 105), langt under de 5 øverste krav (linje 31-64). Instruksen i `ai/agenter/anden-mening.md` giver kun Product Owner anden mening på de nye eller ændrede af de **5 øverste** krav, og ingen af dem er mærket `[SIKKERHED]`. De er derfor uden for kørslens omfang. Der er ingen designfiler at validere. Jeg har ikke kaldt modellen, for at undgå spildte kald.

## Til Ejer (ingen ændring foreslået)
- Når de to krav rykker op blandt de 5 øverste, får de anden mening i en senere kørsel.
- Observation fra første læsning (ikke modelsvar): krav 1 henter tallet fra `retter.json` og gemmer kun i `localStorage`, hvilket er rimeligt for privatlivet. Krav 2 bør ved bygning sikre, at knappens nye tekst ikke lover tilbud til den enkelte ret, når der ingen er den uge. "Se hvilke butikker der har tilbud til denne ret" kan skuffe, hvis svaret er "ingen". Det er en egen vurdering og ikke valideret af anden model.

Nyttigt: nej (intet kaldt, intet at validere).
