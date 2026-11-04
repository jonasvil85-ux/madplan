// Prisskøn for varer der ikke er på tilbud (normalpriser, groft gennemsnit i danske supermarkeder).
// Skønnet regner i hele pakker – som når man står i butikken: 2 fed hvidløg = 1 hvidløg, 250 g pasta = 1 pakke.
// Format: [regex på varenavn, pakkestørrelse, enhed, pris for én pakke]

const PRISSKOEN = [
  // Specifikke først (ellers rammes de af bredere regler længere nede)
  [/hakkede tomater|flåede tomater/i, 1, 'dåse', 8], [/tomatpuré/i, 1, 'stk', 8], [/kokosmælk/i, 400, 'ml', 12],
  [/kikærter|kidneybønner|hvide bønner/i, 1, 'dåse', 9], [/frosne ærter|frosne grøntsager/i, 1, 'pakke', 20],
  [/sukkerærter/i, 150, 'g', 15], [/fløde ?ost|flødeost/i, 200, 'g', 15], [/chilisauce/i, 1, 'stk', 15],
  [/bouillon|fond|sovsejævner/i, 1, 'pakke', 15],
  // Frugt & grønt
  [/hvidløg/i, 10, 'fed', 5], [/skalotte|rødløg|\bløg\b|^løg/i, 1, 'stk', 2],
  [/kartof/i, 1000, 'g', 15], [/gulerød/i, 1000, 'g', 12], [/pastinak|persillerod|rodfrugt/i, 500, 'g', 15],
  [/knoldselleri|selleri/i, 1, 'stk', 15], [/rødbede/i, 500, 'g', 12],
  [/citron|lime/i, 1, 'stk', 4], [/agurk/i, 1, 'stk', 9], [/porre/i, 1, 'stk', 6],
  [/kål/i, 1, 'stk', 15], [/salat|rucola|iceberg/i, 1, 'stk', 15], [/peberfrugt|rød peber/i, 1, 'stk', 8],
  [/cherrytomat|tomat(?!puré|er på dåse)|^tomater/i, 250, 'g', 15], [/champignon|svampe|portobello/i, 250, 'g', 15],
  [/spinat/i, 250, 'g', 15], [/squash|aubergine/i, 1, 'stk', 8], [/broccoli|blomkål/i, 1, 'stk', 15],
  [/græskar|hokkaido/i, 1, 'stk', 20], [/avocado/i, 1, 'stk', 8], [/ingefær/i, 100, 'g', 8], [/chili\b/i, 1, 'stk', 5],
  [/dild|persille|purløg|koriander|basilikum|estragon|rosmarin|mynte|frisk timian|krydderurt/i, 1, 'bundt', 12],
  [/æble|pære|appelsin|klementin|banan/i, 1000, 'g', 18], [/druer|bær/i, 250, 'g', 20], [/mango|ananas|melon/i, 1, 'stk', 15],
  [/grønne bønner|bønner(?!.*dåse)/i, 400, 'g', 20], [/ærter/i, 500, 'g', 15],
  // Mejeri & æg
  [/(?<!kokos)mælk|kærnemælk|havredrik/i, 1000, 'ml', 13], [/piskefløde|madlavningsfløde|fløde/i, 250, 'ml', 15],
  [/creme fraiche/i, 200, 'g', 13], [/skyr|yoghurt|ymer/i, 1000, 'g', 25], [/hytteost/i, 250, 'g', 15],
  [/smør|kærgården|margarine/i, 250, 'g', 25], [/(?<![a-zæøå])æg(?![a-zæøå])|frilandsæg|skrabeæg/i, 10, 'stk', 30],
  [/flødeost|philadelphia/i, 200, 'g', 15], [/feta|halloumi|mozzarella|brie/i, 200, 'g', 20],
  [/parmesan|grana|cheddar|revet ost|skiveost|ost\b/i, 200, 'g', 25],
  // Kød & fisk
  [/kylling/i, 1000, 'g', 80], [/hakket oksekød|okse|kalv|bøf|entrecote/i, 1000, 'g', 110],
  [/hakket grise|gris|svin|flæsk|bacon|medister|pølse|kotelet|mørbrad/i, 1000, 'g', 70],
  [/\band\b|ande/i, 1000, 'g', 90], [/laks/i, 1000, 'g', 180], [/rejer/i, 300, 'g', 50],
  [/torsk|\bsej\b|mørksej|rødspætte|fisk/i, 1000, 'g', 140], [/tun\b/i, 1, 'dåse', 12], [/makrel|sild/i, 1, 'stk', 15],
  [/leverpostej|pålæg|skinke|salami|rullepølse|spegepølse/i, 1, 'pakke', 20],
  // Kolonial & konserves
  [/lasagne|pasta|spaghetti|penne|fettuccine|nudler|makaroni/i, 500, 'g', 12], [/\bris\b|jasminris|basmati/i, 1000, 'g', 20],
  [/couscous|bulgur|quinoa/i, 500, 'g', 18], [/havregryn|müsli|cornflakes|granola/i, 1, 'pakke', 25],
  [/hakkede tomater|flåede tomater/i, 1, 'dåse', 8], [/tomatpuré/i, 1, 'stk', 8], [/kokosmælk/i, 400, 'ml', 12],
  [/kikærter|kidneybønner|hvide bønner|majs/i, 1, 'dåse', 9], [/kapers|oliven|ansjoser|syltede/i, 1, 'stk', 18],
  [/bouillon|fond/i, 1, 'pakke', 15], [/sojasauce|worcester/i, 1, 'stk', 20],
  [/sennep|ketchup|remoulade|mayonnaise|dressing|pesto|pastasauce/i, 1, 'stk', 20],
  [/olivenolie|rapsolie|\bolie\b/i, 1, 'stk', 30], [/eddike/i, 1, 'stk', 12], [/honning|marmelade|nutella|peanutbutter/i, 1, 'stk', 30],
  [/rasp/i, 1, 'pakke', 10], [/nødder|mandler|kerner|rosiner|svesker/i, 1, 'pakke', 25],
  // Krydderier & bagning
  [/hvedemel|\bmel\b/i, 1, 'pakke', 15], [/sukker|flormelis/i, 1, 'pakke', 12], [/gær\b/i, 1, 'pakke', 2],
  [/bagepulver|natron|vaniljesukker|kakao|maizena|kulør/i, 1, 'pakke', 12], [/\bsalt\b|^salt/i, 1, 'pakke', 8],
  [/peber\b|karry|paprika|spidskommen|oregano|kanel|muskat|laurbær|krydderi|tørret|chiliflager/i, 1, 'pakke', 15],
  // Brød
  [/rugbrød|brød|pita|tortilla|wraps|boller|baguette|knækbrød|toast|rundstykker/i, 1, 'pakke', 20],
  // Frost
  [/pommes frites|frosne|frossen|\bis\b/i, 1, 'pakke', 25],
  // Drikkevarer
  [/kaffe/i, 1, 'pakke', 50], [/\bte\b/i, 1, 'pakke', 20], [/juice|saft|most/i, 1, 'stk', 20],
  [/sodavand|cola|danskvand|mineralvand/i, 1, 'stk', 15], [/\bøl\b/i, 1, 'stk', 60], [/vin\b|rødvin|hvidvin/i, 750, 'ml', 60],
  // Snacks
  [/chips|popcorn|chokolade|slik|vingummi|lakrids|kiks|småkager|saltstænger|peanuts/i, 1, 'stk', 20],
  // Husholdning
  [/toiletpapir/i, 1, 'stk', 45], [/køkkenrulle/i, 1, 'stk', 30], [/opvasketabs|maskinopvask/i, 1, 'stk', 60],
  [/opvaskemiddel/i, 1, 'stk', 20], [/vaskemiddel|skyllemiddel/i, 1, 'stk', 55], [/bagepapir|alufolie|husholdningsfilm|madpapir/i, 1, 'stk', 18],
  [/fryseposer|affaldsposer|plastikposer/i, 1, 'stk', 20], [/rengøring|toiletrens|glasrens/i, 1, 'stk', 25],
  [/karklude|svampe til opvask|opvaskebørste/i, 1, 'stk', 15], [/stearinlys|fyrfadslys/i, 1, 'stk', 30],
  [/batterier/i, 1, 'stk', 40], [/servietter|tændstikker/i, 1, 'stk', 15], [/pærer/i, 1, 'stk', 30], [/støvsugerposer/i, 1, 'stk', 50],
  // Personlig pleje
  [/shampoo|balsam|showergel|bodylotion/i, 1, 'stk', 30], [/håndsæbe|håndcreme/i, 1, 'stk', 20],
  [/tandpasta|tandtråd/i, 1, 'stk', 20], [/tandbørste/i, 1, 'stk', 25], [/deodorant/i, 1, 'stk', 30],
  [/barber/i, 1, 'stk', 40], [/bind|tampon/i, 1, 'stk', 30], [/vatpinde|vatrondeller|plaster|læbepomade/i, 1, 'stk', 15],
  [/solcreme/i, 1, 'stk', 80], [/hårvoks/i, 1, 'stk', 40], [/panodil|smertestillende/i, 1, 'stk', 25],
  // Baby & dyr
  [/bleer/i, 1, 'stk', 90], [/vådservietter/i, 1, 'stk', 20], [/babymad|klemmeposer|grødpulver/i, 1, 'stk', 15],
  [/modermælk/i, 1, 'stk', 90], [/kattegrus/i, 1, 'stk', 50], [/kattemad|hundemad/i, 1, 'stk', 45], [/snacks/i, 1, 'stk', 25],
];

// Hvis intet nøgleord passer: typisk pris for én vare i gruppen
const GRUPPE_PRIS = {
  'Frugt & grønt': 15, 'Brød & bagværk': 20, 'Kød & fjerkræ': 60, 'Fisk & skaldyr': 50, 'Pålæg & delikatesse': 20,
  'Mejeri, æg & ost': 15, 'Kolonial': 20, 'Konserves': 10, 'Krydderier & bagning': 15, 'Frost': 25, 'Drikkevarer': 25,
  'Snacks & slik': 20, 'Husholdning': 30, 'Personlig pleje': 30, 'Baby & børn': 40, 'Dyr': 40, 'Andet': 25,
};
const OMREGN_SKOEN = { g: ['g', 1], kg: ['g', 1000], ml: ['ml', 1], dl: ['ml', 100], l: ['ml', 1000] };

// Skønnet pris i kr for at købe varen (hele pakker). maengde/enhed kan udelades (= én pakke).
const SKOEN_OPSLAG = new Map();  // navn -> prisregel (opslaget kører mange gange, når madplanen simuleres)
function skoenPris(navn, maengde, enhed, gruppe) {
  if (!SKOEN_OPSLAG.has(navn)) SKOEN_OPSLAG.set(navn, PRISSKOEN.find(([r]) => r.test(navn)) || null);
  const regel = SKOEN_OPSLAG.get(navn);
  if (!regel) return GRUPPE_PRIS[gruppe || varegruppe(navn)] ?? 25;
  const [, str, pEnhed, pris] = regel;
  if (!maengde || !enhed || enhed === 'efter smag') return pris;
  // Samme slags enhed (g/ml) -> antal pakker; stk/fed/dåse/bundt -> tæl direkte; ellers 1 pakke
  const [a, fa] = OMREGN_SKOEN[enhed] || [enhed, 1];
  const [b, fb] = OMREGN_SKOEN[pEnhed] || [pEnhed, 1];
  if (a !== b) return pris;
  return Math.max(1, Math.ceil((maengde * fa) / (str * fb) - 1e-9)) * pris;
}
