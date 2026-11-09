// Kategorier i "Vælg retter" (Budget, Fitness, Fast food, Kokken, Vegetar), ugeplanen under dem og Fitness-kortene med energifordeling.
// Næringstal pr. portion står i naering.json (bygges af scripts/naering/byg_naering.py og hentes i start() i index.html som window.NAERING).
// Fitness: mindst 30 % af energien fra protein, højst 40 % fra fedt, 350-850 kcal pr. portion, og tallene skal være sikre (dækning >= 90 %).
function naeringFor(id) {
  const n = window.NAERING && window.NAERING[id];
  if (!n) return null;
  const p = n.protein * 4, k = n.kulhydrat * 4, f = n.fedt * 9, s = (p + k + f) || 1;
  const pP = Math.round(p / s * 100), fP = Math.round(f / s * 100);
  return { ...n, pP, fP, kP: Math.max(0, 100 - pP - fP), fit: n.daekning >= 0.9 && p / s * 100 >= 30 && f / s * 100 <= 40 && n.kcal >= 350 && n.kcal <= 850 };
}
const erFitness = id => !!(naeringFor(id) || {}).fit;
const fitProtein = id => (naeringFor(id) || { protein: 0 }).protein;
const FITNESS_INFO = '<p class="fitinfo">Mindst 30 % af energien fra protein, højst 40 % fra fedt, 350-850 kcal pr. portion. Mest protein først.</p>';

// ===== Kombination: handler man i flere butikker, vælges hver ingrediens i den butik, hvor den er billigst på tilbud =====
// En ret hører til Kombination, hvis den bruger tilbud fra mindst to af butikkerne og enten KUN kan laves sådan, eller bliver mærkbart billigere end i den billigste enkeltbutik.
const KOMBI_MIN_SPAR = 5;  // kr. for hele retten (4 personer)
const KOMBI_HUKOMMELSE = new Map();
function kombiInfo(r) {
  const S = aktivS();
  if (!r.mix || S.length < 2) return null;
  const nk = sNoegle(S);
  let m = KOMBI_HUKOMMELSE.get(nk);
  if (!m) KOMBI_HUKOMMELSE.set(nk, m = new Map());
  if (m.has(r.id)) return m.get(r.id);
  let enkelt = Infinity;  // billigste pris, hvis man kun handlede i én af butikkerne
  for (const k of S) { const x = mixFor([k]).map.get(r.id); if (x && x.ok) enkelt = Math.min(enkelt, x.pris_i_alt); }
  const butikker = S.filter(k => r.ingredienser.some(i => i.tilbud.some(id => ALLE_TILBUD[id] && ALLE_TILBUD[id].butik === k)));
  const spar = enkelt === Infinity ? null : Math.round(enkelt - r.pris_i_alt);  // null = kan ikke laves i nogen enkelt butik
  const info = butikker.length >= 2 && (spar === null || spar >= KOMBI_MIN_SPAR) ? { butikker, spar } : null;
  m.set(r.id, info);
  return info;
}
const kombiLinje = r => {
  const k = kombiInfo(r);
  if (!k) return '';
  const navne = k.butikker.map(b => data.butikker[b].navn).join(' + ');
  return `<div class="kombi-linje" title="Ingredienserne købes, hvor de er billigst på tilbud: ${esc(navne)}">${ikon('refresh')}<span>${esc(navne)} · ${k.spar === null ? 'kun mulig som kombination' : 'spar ca. ' + k.spar + ' kr'}</span></div>`;
};

// Nederste linje på et retkort: tid og pris pr. person til venstre, antal tilbudsvarer til højre
function liniePris(r, kp, tilbudsvarer) {
  return liniePris0(r, kp, tilbudsvarer) + kombiLinje(r);
}
function liniePris0(r, kp, tilbudsvarer) {
  return `<div class="rolig"><span class="pris">${r.tid_minutter} min · ${kr(Math.round(kp.indkoeb / kp.pers))}/pers.${r.spis_tidligt ? ' · spis tidligt' : ''}</span>${tilbudsvarer.length ? `<span class="tilb"><i></i>${tilbudsvarer.length} på tilbud</span>` : ''}</div>`;
}
// Almindeligt retkort: kort beskrivelse (højst to linjer) og én linje med tid, pris og tilbud. Ingen mærkater eller lister
function retKortHtml(r, kp, tilbudsvarer) {
  return `<p class="besk">${esc(r.beskrivelse)}</p>${liniePris(r, kp, tilbudsvarer)}`;
}
// Fitness-kort: protein i gram, kcal og energifordeling som farvet søjle med korte navne
function fitnessKortHtml(r, kp, tilbudsvarer) {
  const n = naeringFor(r.id);
  if (!n) return '';
  return `<div class="fithoved"><span class="stor">${Math.round(n.protein)}<small> g protein</small></span><span class="kcal">${n.kcal} kcal</span></div>
    <div class="energi" title="Energifordeling"><i class="p" style="width:${n.pP}%"></i><i class="k" style="width:${n.kP}%"></i><i class="f" style="width:${n.fP}%"></i></div>
    <div class="forklar"><span class="p">Protein <b>${n.pP}%</b></span><span class="k">Kulhydrat <b>${n.kP}%</b></span><span class="f">Fedt <b>${n.fP}%</b></span></div>
    ${liniePris(r, kp, tilbudsvarer)}`;
}

// ===== Kategorier i "Vælg retter" (erstatter niveau-, køkken- og type-rækkerne) =====
// En ret kan høre til flere kategorier. Retter, der ikke passer i nogen, ses, når intet kort er valgt.
const FAST_FOOD = /burger|pizza|taco|wrap|kebab|gyros|shawarma|hotdog|nugget|quesadilla|burrito|fajita|sandwich|pommes|spareribs|sticky ribs/i;
const BUDGET_GRAENSE = 20;  // kr. pr. person (indkøb)
const KATEGORIER_VALG = [
  { k: 'kombi', navn: 'Kombination', kort: 'Billigst på tværs', ikon: 'refresh', bil: 'grafik/niveau-familie.jpg', kunFlere: true },
  { k: 'budget', navn: 'Budget', kort: 'Højst ' + BUDGET_GRAENSE + ' kr. pr. person', ikon: 'cart', bil: 'grafik/niveau-student.jpg' },
  { k: 'fitness', navn: 'Fitness', kort: 'Mest protein', ikon: 'flame', bil: 'billeder/kyllingebryst-i-fad-med-roed-peber-og-kartofler.jpg' },
  { k: 'fastfood', navn: 'Fast food', kort: 'Burgere, pizza, wraps', ikon: 'utensils', bil: 'billeder/burgere-med-hjemmelavede-boeffer.jpg' },
  { k: 'kokken', navn: 'Kokken', kort: 'Lidt ekstra', ikon: 'wine', bil: 'grafik/niveau-weekend.jpg' },
  { k: 'vegetar', navn: 'Vegetar', kort: 'Uden kød', ikon: 'blad', bil: 'billeder/kikaertecurry-med-kokos-og-ris.jpg' },
];
function katIKat(r, k, prPers) {
  switch (k) {
    case 'kombi': return !!kombiInfo(r);
    case 'budget': return prPers.get(r.id) <= BUDGET_GRAENSE;
    case 'fitness': return erFitness(r.id);
    case 'fastfood': return FAST_FOOD.test(r.navn);
    case 'kokken': return r.niveau === 'weekend';
    case 'vegetar': return r.kategori === 'vegetar';
    default: return true;
  }
}
function katSort(k, prPers) {
  if (k === 'kombi') return (a, b) => ((kombiInfo(b) || {}).spar ?? 999) - ((kombiInfo(a) || {}).spar ?? 999);  // størst besparelse først (kun mulig som kombination øverst)
  return k === 'fitness' ? (a, b) => fitProtein(b.id) - fitProtein(a.id) : (a, b) => prPers.get(a.id) - prPers.get(b.id);  // ellers billigste først
}
function katRaekke(retter, prPers, valgt) {
  const harTal = !!window.NAERING && Object.keys(window.NAERING).length > 0;  // uden næringstal findes Fitness ikke
  const kort = KATEGORIER_VALG.filter(c => (c.k !== 'fitness' || harTal) && (!c.kunFlere || aktivS().length > 1)).map(c => {
    const n = retter.filter(r => katIKat(r, c.k, prPers)).length, aktiv = valgt === c.k;
    return `<button class="niveau kat ${aktiv ? 'aktiv' : ''}" data-koekken="${aktiv ? 'alle' : c.k}" style="--bg:url('${c.bil}')" aria-pressed="${aktiv}">
      <span class="ikon">${ikon(c.ikon)}</span><strong>${c.navn}</strong><small>${c.kort}</small><em class="antal-pille">${n}</em></button>`;
  }).join('');
  return `<div class="niveauer katraekke">${kort}</div>`;  // intet kort valgt = alle retter; tryk på det valgte kort for at gå tilbage
}

// ===== Ugeplan under kategorierne: de valgte retter lagt på ugens dage (i den rækkefølge, de er valgt), fra i dag =====
// Dage, hvor man ikke er hjemme, springes over: retterne rykker til de næste dage, der er hjemme.
let UGE_UDE = new Set();  // dagsindeks (0 = i dag) – gemmes i browseren
try { UGE_UDE = new Set(JSON.parse(localStorage.getItem('madplan-ude') || '[]')); } catch (e) { /* uden lager */ }
document.addEventListener('click', e => {
  const b = e.target.closest('[data-ude]');
  if (!b) return;
  const i = +b.dataset.ude;
  UGE_UDE.has(i) ? UGE_UDE.delete(i) : UGE_UDE.add(i);
  try { localStorage.setItem('madplan-ude', JSON.stringify([...UGE_UDE])); } catch (err) { /* uden lager */ }
  const y = window.scrollY; render(); window.scrollTo(0, y);
});
function ugeplanValg(retter) {
  const valgte = state.valgte.map(id => retter.find(r => r.id === id)).filter(Boolean);
  const dage = Array.from({ length: 7 }, (_, i) => { const d = new Date(); d.setDate(d.getDate() + i); return d; });
  const hjemme = 7 - UGE_UDE.size;
  let n = 0;  // næste valgte ret
  const kort = dage.map((d, i) => {
    const hoved = `<div class="dag-top"><b>${DAGE[d.getDay()]}</b><small>${d.getDate()}/${d.getMonth() + 1}</small></div>`;
    const ude = `<button type="button" class="ude-knap" data-ude="${i}" title="Ikke hjemme">${ikon('ude')}<span>Ikke hjemme</span></button>`;
    if (UGE_UDE.has(i)) {
      return `<div class="dag-kort fravalgt">${hoved}<div class="dag-fra"><span class="ude-ikon">${ikon('ude')}</span><span class="ude-tekst">Ikke hjemme</span>
        <button type="button" class="byt-knap udvidet" data-ude="${i}" title="Hjemme igen">${ikon('plus')}<span>Hjemme igen</span></button></div></div>`;
    }
    const r = valgte[n++];
    if (!r) return `<div class="dag-kort fravalgt">${hoved}<div class="dag-fra"><span class="tom-tekst">Ingen ret</span>${ude}</div></div>`;
    return `<div class="dag-kort">${hoved}<span class="dag-knapper"><button type="button" class="byt-knap" data-ret="${esc(r.id)}" title="Fjern retten" aria-label="Fjern ${esc(r.navn)}">${ikon('minus')}</button></span>
      <div class="dag-bil-sim ${r.billede ? '' : 'ingen'}">${r.billede ? `<img src="${esc(r.billede)}" alt="" loading="lazy" width="360" height="270">` : ikon('utensils')}</div>
      <div class="dag-ret" title="${esc(r.navn)}">${esc(r.navn)}</div>
      <div class="dag-ude">${ude}</div>
    </div>`;
  }).join('');
  const rest = valgte.slice(hjemme);  // retter ud over ugen: små billeder, tryk for at fjerne
  return `<div class="panel ugeplan-valg">
    <div class="panel-hoved"><h2>Din uge</h2><span class="ugetal">${Math.min(valgte.length, hjemme)} af ${hjemme} dage</span></div>
    <div class="kalender">${kort}</div>
    ${rest.length ? `<div class="rest-raekke"><span class="rest-tekst">Ud over ugen:</span>${rest.map(r => `<button type="button" class="rest-ret" data-ret="${esc(r.id)}" title="${esc(r.navn)} – tryk for at fjerne">${r.billede ? `<img src="${esc(r.billede)}" alt="">` : ''}<span>×</span></button>`).join('')}</div>` : ''}
  </div>`;
}
