// Måltidsjagten – service worker: gør siden hurtig og lader indkøbssedlen virke uden dækning (fx inde i butikken).
// Principper:
//  - Data (retter.json osv.) og siden selv hentes ALTID fra nettet først, så ugens nye tilbud aldrig er forældede; kun uden net bruges den sidste gemte kopi.
//  - Billeder og grafik hentes fra gemmen først (de ændrer sig sjældent) og opdateres i baggrunden.
//  - Kun adresser på samme domæne gemmes. Login (Supabase) og andre eksterne kald røres aldrig.
const VERSION = 'v1';
const SKAL = `maaltidsjagten-skal-${VERSION}`;      // siden og scripts
const DATA = `maaltidsjagten-data-${VERSION}`;      // JSON-filer
const BILLEDER = `maaltidsjagten-billeder-${VERSION}`;

const FORUD = ['/', '/ikoner.js', '/varer.js', '/pris.js', '/auth.js', '/feedback.js', '/manifest.webmanifest', '/ikoner/icon-192.png', '/favicon.svg'];

const FORUD_DATA = ['/retter.json', '/opskrifter.json', '/tilbudsliste.json'];  // hentes med det samme, så appen kan åbnes uden net allerede efter første besøg

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const skal = await caches.open(SKAL), data = await caches.open(DATA);
    await Promise.allSettled([...FORUD.map(u => skal.add(u)), ...FORUD_DATA.map(u => data.add(new Request(u, { cache: 'no-cache' })))]);
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    for (const n of await caches.keys()) if (![SKAL, DATA, BILLEDER].includes(n)) await caches.delete(n);  // gamle versioner ryddes væk
    await self.clients.claim();
  })());
});

const netFoerst = async (req, gem) => {
  const kopi = await caches.match(req, { ignoreSearch: req.mode === 'navigate' });
  try {
    // Findes en gemt kopi, ventes højst 5 sekunder på nettet (dårlig dækning i butikken): derefter bruges kopien
    const hent = fetch(req).then(svar => { if (svar.ok) { const ekstra = svar.clone(); caches.open(gem).then(c => c.put(req, ekstra)); } return svar; });
    return kopi ? await Promise.race([hent, new Promise((_, afvis) => setTimeout(() => afvis(new Error('langsomt net')), 5000))]) : await hent;
  } catch (fejl) {
    if (kopi) return kopi;
    if (req.mode === 'navigate') { const forside = await caches.match('/'); if (forside) return forside; }
    throw fejl;
  }
};

const gemFoerst = async (req, gem) => {
  const c = await caches.open(gem), kopi = await c.match(req);
  const hent = fetch(req).then(svar => { if (svar.ok) c.put(req, svar.clone()); return svar; }).catch(() => null);  // (klonen laves med det samme, før svaret bruges)
  return kopi || (await hent) || Response.error();
};

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;                 // eksterne kald (login, billeder fra Tjek m.m.) røres ikke
  if (url.pathname === '/sw.js' || url.pathname.startsWith('/admin')) return;
  if (req.mode === 'navigate') return void e.respondWith(netFoerst(req, SKAL));
  if (url.pathname.endsWith('.json') || url.pathname.endsWith('.js') || url.pathname.endsWith('.webmanifest')) return void e.respondWith(netFoerst(req, url.pathname.endsWith('.json') ? DATA : SKAL));
  if (/\.(jpg|jpeg|png|webp|svg|ico)$/.test(url.pathname)) return void e.respondWith(gemFoerst(req, BILLEDER));
});
