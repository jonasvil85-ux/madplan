// Fælles modul (ikke en route — filer med _ eksponeres ikke af Vercel)
// Henter aktuelle tilbudsaviser fra Tjek (samme data som etilbudsavis.dk).
// Ingen API-nøgle. Uofficielt API — kan ændre sig uden varsel.
const API = 'https://squid-api.tjek.com/v2';

const BUTIKKER = {
  netto: { navn: 'Netto', dealerId: '9ba51',  prefix: 'N' },
  meny:  { navn: 'MENY',  dealerId: '267e1m', prefix: 'M' },
};

// Aviser uden dagligvarer (Netto Nonfood, MENY Vin, magasiner)
const IKKE_MAD = /nonfood|vin|spisetid|magasin/i;

const ENHEDER = { pcs: 'stk', g: 'g', kg: 'kg', ml: 'ml', cl: 'cl', l: 'l' };

// Tjek bruger "+0000" uden kolon — gør datoen ISO-gyldig
const tid = s => new Date(String(s).replace(/([+-]\d\d)(\d\d)$/, '$1:$2')).getTime();

async function hent(url) {
  const r = await fetch(url, { headers: { Accept: 'application/json' } });
  if (!r.ok) throw new Error(`Tjek HTTP ${r.status} for ${url}`);
  return r.json();
}

async function hentButik(key) {
  const b = BUTIKKER[key];
  const nu = Date.now();
  const kataloger = (await hent(`${API}/catalogs?dealer_ids=${b.dealerId}&limit=24`))
    .filter(c => c.offer_count > 0 && !IKKE_MAD.test(c.label || '') && tid(c.run_till) >= nu);

  // Foretræk aviser der gælder nu; ellers den næste der starter (fx dagen før avisskifte)
  let aviser = kataloger.filter(c => tid(c.run_from) <= nu);
  if (!aviser.length) aviser = kataloger.sort((a, z) => tid(a.run_from) - tid(z.run_from)).slice(0, 1);

  const tilbud = [];
  for (const avis of aviser) {
    for (let offset = 0; offset < 1500; offset += 100) {
      const side = await hent(`${API}/offers?catalog_id=${avis.id}&limit=100&offset=${offset}`);
      tilbud.push(...side.map(o => normaliser(o, key)));
      if (side.length < 100) break;
    }
  }

  return {
    info: {
      navn: b.navn,
      aviser: aviser.map(a => ({ id: a.id, navn: a.label, fra: a.run_from, til: a.run_till })),
    },
    tilbud,
  };
}

function normaliser(o, butik) {
  const q = o.quantity || {};
  const s = q.size || {};
  const sym = q.unit?.symbol;
  return {
    id: o.id,
    butik,
    navn: (o.heading || '').trim(),
    beskrivelse: (o.description || '').trim(),
    pris: o.pricing?.price ?? null,
    forPris: o.pricing?.pre_price ?? null,
    maengde: s.from == null ? null : (s.from === s.to ? `${s.from}` : `${s.from}-${s.to}`),
    enhed: ENHEDER[sym] || sym || null,
    billede: o.images?.thumb || null,
    gyldigTil: o.run_till,
  };
}

// Simpel cache i den varme serverless-instans
let cache = null;
const CACHE_MS = 30 * 60 * 1000;

async function hentTilbud() {
  if (cache && Date.now() - cache.hentet < CACHE_MS) return cache.data;

  const keys = Object.keys(BUTIKKER);
  const resultater = await Promise.all(keys.map(hentButik));

  const butikker = {};
  const tilbud = [];
  keys.forEach((k, i) => {
    butikker[k] = resultater[i].info;
    // Korte id'er (N1, N2 … / M1, M2 …) — bruges af Claude og frontend
    resultater[i].tilbud.forEach((t, n) => tilbud.push({ ...t, kort: `${BUTIKKER[k].prefix}${n + 1}` }));
  });

  // Nøgle der skifter når en ny avis udkommer — bruges som cache-nøgle for retter
  const noegle = keys.flatMap(k => butikker[k].aviser.map(a => a.id)).sort().join('-');

  const data = { noegle, hentet: new Date().toISOString(), butikker, tilbud };
  cache = { hentet: Date.now(), data };
  return data;
}

module.exports = { BUTIKKER, hentTilbud };
