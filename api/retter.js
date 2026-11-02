// Vercel API route — Claude foreslår 15-20 aftensmadsretter ud fra ugens tilbud
// Env: ANTHROPIC_API_KEY
// Svaret caches på Vercels CDN pr. tilbudsavis (?noegle=...), så Claude kun kaldes ca. én gang om ugen.
const { Anthropic } = require('@anthropic-ai/sdk');
const { BUTIKKER, hentTilbud } = require('./_tjek');

const ENHEDER = ['g', 'ml', 'stk', 'spsk', 'tsk', 'fed', 'dåse', 'pakke', 'bundt', 'efter smag'];

const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['retter'],
  properties: {
    retter: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['navn', 'beskrivelse', 'kategori', 'tid_minutter', 'spis_tidligt', 'ingredienser', 'fremgangsmaade'],
        properties: {
          navn: { type: 'string' },
          beskrivelse: { type: 'string' },
          kategori: { type: 'string', enum: ['kylling', 'okse', 'svin', 'fisk', 'vegetar', 'andet'] },
          tid_minutter: { type: 'integer' },
          spis_tidligt: { type: 'boolean' },
          ingredienser: {
            type: 'array',
            items: {
              type: 'object',
              additionalProperties: false,
              required: ['navn', 'maengde', 'enhed', 'basisvare', 'tilbud'],
              properties: {
                navn: { type: 'string' },
                maengde: { type: 'number' },
                enhed: { type: 'string', enum: ENHEDER },
                basisvare: { type: 'boolean' },
                tilbud: { type: 'array', items: { type: 'string' } },
              },
            },
          },
          fremgangsmaade: { type: 'array', items: { type: 'string' } },
        },
      },
    },
  },
};

const SYSTEM = `Du er en dansk madplanlægger. Du foreslår varierede, realistiske hverdagsretter til aftensmad for en dansk husstand, og du bygger dem så vidt muligt op omkring varer der er på tilbud i denne uges tilbudsaviser. Skriv på dansk.`;

function byggePrompt(data) {
  const sektioner = Object.keys(BUTIKKER).map(k => {
    const linjer = data.tilbud
      .filter(t => t.butik === k)
      .map(t => {
        const maengde = t.maengde ? ` | ${t.maengde} ${t.enhed || ''}`.trimEnd() : '';
        const besk = t.beskrivelse ? ` | ${t.beskrivelse.replace(/\s*\n\s*/g, '; ').slice(0, 140)}` : '';
        return `${t.kort} | ${t.navn} | ${t.pris} kr${maengde}${besk}`;
      });
    return `## ${BUTIKKER[k].navn} (id-præfiks ${BUTIKKER[k].prefix})\n${linjer.join('\n')}`;
  });

  return `Her er ugens tilbud. Format: id | vare | pris | mængde | beskrivelse.

${sektioner.join('\n\n')}

Foreslå 18 aftensmadsretter til 4 personer:
- Hver ret skal bruge mindst én tilbudsvare som en central ingrediens (typisk proteinen eller hovedgrøntsagen).
- Varier mellem kylling, okse, svin, fisk og vegetar, og mellem hurtige hverdagsretter (under 30 min) og lidt større retter. Gerne både klassisk dansk og internationalt.
- Ingredienser: angiv mængde for 4 personer. Brug g og ml (aldrig kg eller liter). Brug "stk" for løg, æg, peberfrugter o.l.
- "basisvare": true for ting de fleste har i skabet: salt, peber, olie, smør, mel, sukker, tørrede krydderier, bouillonterning, eddike, sojasauce o.l.
- "tilbud": id'er på tilbud der faktisk er denne ingrediens (fx N12, M7). Tag gerne et id fra begge butikker hvis begge har varen. Tom liste hvis ingen tilbud passer. Brug kun id'er fra listen ovenfor.
- "spis_tidligt": true hvis retten indeholder frisk fisk, skaldyr eller andet der bør spises tidligt i ugen.
- "fremgangsmaade": 4-8 korte, konkrete trin.
- Ignorer non-food, alkohol, slik, sodavand og kaffe.`;
}

module.exports = async function (req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  res.setHeader('Cache-Control', 'no-store');
  if (!process.env.ANTHROPIC_API_KEY) return res.status(503).json({ error: 'CLAUDE_NOT_CONFIGURED' });

  try {
    const data = await hentTilbud();
    const client = new Anthropic();

    // Streaming + finalMessage undgår HTTP-timeouts ved lange svar.
    // fallbacks: "default" — hvis modellen afviser, kører API'et automatisk forespørgslen videre på en fallback-model.
    const msg = await client.beta.messages.stream({
      model: 'claude-opus-5-5',
      max_tokens: 32000,
      betas: ['server-side-fallback-2026-07-01'],
      fallbacks: 'default',
      output_config: { effort: 'medium', format: { type: 'json_schema', schema: SCHEMA } },
      system: SYSTEM,
      messages: [{ role: 'user', content: byggePrompt(data) }],
    }).finalMessage();

    if (msg.stop_reason === 'refusal') return res.status(502).json({ error: 'Claude afviste forespørgslen' });
    if (msg.stop_reason === 'max_tokens') return res.status(502).json({ error: 'Svaret fra Claude blev afkortet' });

    const tekst = msg.content.filter(b => b.type === 'text').map(b => b.text).join('');
    const { retter } = JSON.parse(tekst);

    // Kun de tilbud retterne refererer til — og drop id'er Claude har fundet på
    const alle = new Map(data.tilbud.map(t => [t.kort, t]));
    const tilbud = {};
    retter.forEach((r, i) => {
      r.id = `r${i + 1}`;
      r.ingredienser.forEach(ing => {
        ing.tilbud = ing.tilbud.filter(id => alle.has(id));
        ing.tilbud.forEach(id => { tilbud[id] = alle.get(id); });
      });
    });

    res.setHeader('Cache-Control', 'public, s-maxage=604800, stale-while-revalidate=86400');
    return res.status(200).json({
      noegle: data.noegle,
      genereret: new Date().toISOString(),
      butikker: data.butikker,
      retter,
      tilbud,
    });
  } catch (e) {
    return res.status(502).json({ error: `Kunne ikke lave retter: ${e.message}` });
  }
};
