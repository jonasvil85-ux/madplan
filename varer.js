// Varegrupper til indkøbssedlen + katalog over almindelige varer man kan tilføje.
// Rækkefølgen af VAREGRUPPER er rækkefølgen på indkøbssedlen (nogenlunde som en typisk butiksrunde).

const VAREGRUPPER = [
  { navn: 'Frugt & grønt', ikon: '🥕' },
  { navn: 'Brød & bagværk', ikon: '🍞' },
  { navn: 'Kød & fjerkræ', ikon: '🥩' },
  { navn: 'Fisk & skaldyr', ikon: '🐟' },
  { navn: 'Pålæg & delikatesse', ikon: '🥓' },
  { navn: 'Mejeri, æg & ost', ikon: '🧀' },
  { navn: 'Kolonial', ikon: '🍝' },
  { navn: 'Konserves', ikon: '🥫' },
  { navn: 'Krydderier & bagning', ikon: '🧂' },
  { navn: 'Frost', ikon: '🧊' },
  { navn: 'Drikkevarer', ikon: '🥤' },
  { navn: 'Snacks & slik', ikon: '🍫' },
  { navn: 'Husholdning', ikon: '🧻' },
  { navn: 'Personlig pleje', ikon: '🧴' },
  { navn: 'Baby & børn', ikon: '🍼' },
  { navn: 'Dyr', ikon: '🐾' },
  { navn: 'Andet', ikon: '📦' },
];

// Regler til at placere en vare i en gruppe ud fra navnet. Første match vinder, så rækkefølgen betyder noget.
const GRUPPE_REGLER = [
  ['Personlig pleje', /shampoo|balsam|sæbe|tandpasta|tandbørst|tandtråd|deodorant|deo\b|bodylotion|hudcreme|barber|skraber|bind\b|tampon|trusseindlæg|vatpinde|vatrondel|plaster|solcreme|læbepomade|hårspray|hårvoks|neglefil|mundskyl|håndcreme|shower/i],
  ['Husholdning', /toiletpapir|køkkenrulle|opvask|vaskemiddel|skyllemiddel|bagepapir|alufolie|husholdningsfilm|frysepose|affaldspose|skraldepose|rengøring|universalrengøring|karklud|klude|svampeklud|opvaskebørste|stearinlys|fyrfadslys|batteri|servietter|tændstik|pærer|lightere|wc-rens|kalkfjern|glasrens|støvsugerpose|madpapir|plastikposer|engangs/i],
  ['Baby & børn', /bleer|vådservietter|babymad|modermælk|grødpose|sutteflaske|klemmeposer/i],
  ['Dyr', /kattemad|hundemad|kattegrus|hundesnack|kattesnack|dyrefoder|fuglefrø/i],
  ['Frost', /frosne|frost|\bis\b|isvafler|ispinde|pommes frites|\bærter\b|frossen/i],
  ['Drikkevarer', /sodavand|danskvand|mineralvand|kildevand|juice|saft\b|most\b|\bøl\b|\bvin\b|rødvin|hvidvin(?!seddike)|côtes|capolavoro|cola|kaffe|\bte\b|tebreve|kakao|energidrik|smoothie/i],
  ['Snacks & slik', /chips|slik|chokolade|vingummi|lakrids|popcorn|kiks|småkager|cookies|marcipan|peanuts|saltstænger|müslibar/i],
  ['Konserves', /hakkede tomater|flåede tomater|tomatpuré|kikærter|kidneybønner|hvide bønner|linser på dåse|majs|dåse|kokosmælk|oliven|kapers|syltede|rødbeder på glas|ananas i|tun\b|makrel i|ansjoser|asier|agurkesalat på glas/i],
  ['Kolonial', /honning|marmelade|sauce/i],
  ['Krydderier & bagning', /tørret|krydderi|salt og peber|groft salt|muskat/i],
  ['Fisk & skaldyr', /laks|rejer|torsk|sej\b|mørksej|rødspætte|fisk|makrel|sild|blæksprutte|muslinger|kuller|ørred|hellefisk|krabbe/i],
  ['Pålæg & delikatesse', /pålæg|leverpostej|postej|spegepølse|salami|rullepølse|hamburgerryg|skinke(?!strimler)|chorizo|serrano|pepperoni|hummus|pålægssalat/i],
  ['Kød & fjerkræ', /kylling|okse|landand|pekingand|berberi|\bgris|grise|svine|svin\b|kalv|\blam\b|lamme|\band\b|ande|\bgås|bacon|flæsk|medister|pølse|kotelet|mørbrad|steg\b|stegeben|ribbensteg|flæskesteg|hakket|gullasch|entrecote|culotte|bøf|kød|skinkestrimler|spareribs|kæber|schnitzel|roastbeef|porchetta|kalkun|tyndstegsfilet|medaljon|klump|inderlår|lår\b|bryst/i],
  ['Mejeri, æg & ost', /mælk|fløde|creme fraiche|cremefraiche|skyr|yoghurt|ymer|kefir|smør|kærgården|\bost\b|ost\b|ostehaps|mozzarella|cheddar|grana|parmesan|halloumi|feta|hytteost|philadelphia|flødeost|saint agur|blåskimmel|brie|camembert|havarti|danbo|\bæg\b|æg \(|frilandsæg|skrabeæg|madlavningsjævner|ama madlavning|madlavningsfløde|piskefløde|kærnemælk/i],
  ['Brød & bagværk', /brød|pita|tortilla|wraps|boller|baguette|rugbrød|madbrød|burgerboller|hotdog|knækbrød|toast|rundstykker|croissant|tærtebund|levebrød|signaturbrød/i],
  ['Frugt & grønt', /peberfrugt|rød peber|chili\b|kartof|\bløg|rødløg|skalotte|hvidløg|gulerød|porre|kål\b|hvidkål|rødkål|spidskål|grønkål|rosenkål|blomkål|broccoli|salat|agurk|tomat|squash|græskar|hokkaido|aubergine|spinat|svampe|champignon|portobello|selleri|pastinak|persillerod|rødbede|majskolbe|avocado|æble|pære|banan|citron|lime|appelsin|klementin|clementin|mandarin|mango|ananas|druer|granatæble|kiwi|blommer|bær|jordbær|blåbær|hindbær|dild|persille|purløg|timian|rosmarin|basilikum|koriander|estragon|mynte|krydderurter|ingefær|bønner|sukkerærter|asparges|radiser|frugt|grønt/i],
  ['Kolonial', /pasta|penne|fettuccine|spaghetti|lasagne|nudler|\bris\b|jasminris|basmati|bulgur|couscous|quinoa|havregryn|müsli|cornflakes|granola|honning|marmelade|nutella|peanutbutter|bouillon|fond|sovsejævner|sauce|soja|ketchup|sennep|remoulade|mayonnaise|dressing|eddike|\bolie\b|olivenolie|rapsolie|svesker|rosiner|nødder|mandler|kerner|frø\b|tørret frugt|knækbrød|rasp/i],
  ['Krydderier & bagning', /salt|peber\b|karry|paprika|spidskommen|oregano|kanel|muskat|laurbær|krydderi|chilipulver|chiliflager|tørret timian|hvedemel|\bmel\b|sukker|flormelis|gær\b|bagepulver|natron|vaniljesukker|kakaopulver|kulør|maizena|worcestershire/i],
];

// JavaScripts \b kender ikke æ/ø/å (så "kikærter" ville matche \bærter\b). Erstat med dansk-sikre grænser:
// \b foran et bogstav = "intet bogstav før", ellers = "intet bogstav efter".
const DANSK_GRAENSE = src => src
  .replace(/\\b(?=[a-zæøå(])/gi, '(?<![a-zæøå])')
  .replace(/\\b/g, '(?![a-zæøå])');
const REGLER = GRUPPE_REGLER.map(([g, r]) => [g, new RegExp(DANSK_GRAENSE(r.source), 'i')]);

function varegruppe(navn) {
  for (const [gruppe, regel] of REGLER) if (regel.test(navn)) return gruppe;
  return 'Andet';
}

// Katalog med almindelige varer – brugeren kan søge og tilføje dem til indkøbssedlen.
const KATALOG = {
  'Frugt & grønt': ['Kartofler', 'Bagekartofler', 'Søde kartofler', 'Løg', 'Rødløg', 'Skalotteløg', 'Hvidløg', 'Gulerødder', 'Porrer', 'Agurk', 'Tomater', 'Cherrytomater', 'Peberfrugt', 'Squash', 'Broccoli', 'Blomkål', 'Hvidkål', 'Rødkål', 'Spidskål', 'Grønkål', 'Rosenkål', 'Iceberg', 'Hjertesalat', 'Rucola', 'Babyspinat', 'Champignon', 'Selleri', 'Pastinak', 'Rødbeder', 'Majskolber', 'Avocado', 'Ingefær', 'Chili', 'Forårsløg', 'Radiser', 'Sukkerærter', 'Grønne bønner', 'Æbler', 'Pærer', 'Bananer', 'Appelsiner', 'Klementiner', 'Citroner', 'Lime', 'Druer', 'Kiwi', 'Mango', 'Ananas', 'Melon', 'Jordbær', 'Blåbær', 'Hindbær', 'Persille', 'Dild', 'Purløg', 'Basilikum', 'Koriander', 'Timian', 'Rosmarin', 'Mynte'],
  'Brød & bagværk': ['Rugbrød', 'Franskbrød', 'Fuldkornsbrød', 'Toastbrød', 'Boller', 'Rundstykker', 'Baguette', 'Knækbrød', 'Tortilla wraps', 'Pitabrød', 'Burgerboller', 'Hotdogbrød', 'Croissanter', 'Wienerbrød', 'Kiks til ost'],
  'Kød & fjerkræ': ['Hakket oksekød', 'Hakket grisekød', 'Hakket kyllingekød', 'Kyllingebryst', 'Kyllingelår', 'Hel kylling', 'Bacon', 'Medister', 'Pølser', 'Koteletter', 'Mørbrad', 'Flæsk i skiver', 'Oksebøffer', 'Gullasch', 'Kalkunbryst'],
  'Fisk & skaldyr': ['Laks', 'Torsk', 'Rødspætte', 'Rejer', 'Røget laks', 'Makrel i tomat', 'Tun på dåse', 'Marinerede sild', 'Fiskefrikadeller'],
  'Pålæg & delikatesse': ['Leverpostej', 'Rullepølse', 'Hamburgerryg', 'Skinke', 'Spegepølse', 'Salami', 'Kyllingepålæg', 'Kalkunpålæg', 'Hummus', 'Æggesalat', 'Hønsesalat', 'Tunsalat', 'Rejesalat', 'Pålægschokolade'],
  'Mejeri, æg & ost': ['Letmælk', 'Sødmælk', 'Minimælk', 'Skummetmælk', 'Kærnemælk', 'Havredrik', 'Piskefløde', 'Madlavningsfløde', 'Creme fraiche', 'Yoghurt naturel', 'Græsk yoghurt', 'Skyr', 'Ymer', 'Smør', 'Smørbar', 'Margarine', 'Æg', 'Skiveost', 'Revet ost', 'Mozzarella', 'Parmesan', 'Feta', 'Hytteost', 'Flødeost', 'Brie', 'Halloumi', 'Smøreost'],
  'Kolonial': ['Pasta', 'Spaghetti', 'Lasagneplader', 'Nudler', 'Ris', 'Basmatiris', 'Bulgur', 'Couscous', 'Havregryn', 'Müsli', 'Cornflakes', 'Honning', 'Marmelade', 'Nutella', 'Peanutbutter', 'Bouillonterninger', 'Fond', 'Sojasauce', 'Ketchup', 'Sennep', 'Remoulade', 'Mayonnaise', 'Dressing', 'Eddike', 'Olivenolie', 'Rapsolie', 'Rosiner', 'Nødder', 'Mandler', 'Solsikkekerner', 'Rasp', 'Tomatketchup', 'Pastasauce', 'Pesto', 'Kaffefilter'],
  'Konserves': ['Hakkede tomater', 'Flåede tomater', 'Tomatpuré', 'Kikærter', 'Kidneybønner', 'Hvide bønner', 'Majs', 'Kokosmælk', 'Oliven', 'Kapers', 'Syltede agurker', 'Rødbeder på glas', 'Ananas på dåse', 'Fersken på dåse'],
  'Krydderier & bagning': ['Salt', 'Peber', 'Karry', 'Paprika', 'Spidskommen', 'Oregano', 'Timian (tørret)', 'Kanel', 'Muskatnød', 'Laurbærblade', 'Chiliflager', 'Hvedemel', 'Sukker', 'Flormelis', 'Rørsukker', 'Gær', 'Bagepulver', 'Natron', 'Vaniljesukker', 'Kakaopulver', 'Maizena', 'Kulør'],
  'Frost': ['Frosne ærter', 'Frosne grøntsager', 'Frossen spinat', 'Frosne bær', 'Pommes frites', 'Is', 'Frossen fisk', 'Frosne rejer', 'Frossen pizza', 'Frosne boller'],
  'Drikkevarer': ['Kaffe', 'Te', 'Kakao', 'Appelsinjuice', 'Æblejuice', 'Saft', 'Danskvand', 'Mineralvand', 'Sodavand', 'Cola', 'Øl', 'Rødvin', 'Hvidvin', 'Energidrik'],
  'Snacks & slik': ['Chips', 'Popcorn', 'Saltstænger', 'Peanuts', 'Chokolade', 'Slik', 'Vingummi', 'Lakrids', 'Kiks', 'Småkager', 'Müslibarer', 'Riskiks'],
  'Husholdning': ['Toiletpapir', 'Køkkenrulle', 'Opvaskemiddel', 'Opvasketabs', 'Vaskemiddel', 'Skyllemiddel', 'Bagepapir', 'Alufolie', 'Husholdningsfilm', 'Fryseposer', 'Affaldsposer', 'Universalrengøring', 'Toiletrens', 'Glasrens', 'Karklude', 'Opvaskebørste', 'Svampe til opvask', 'Stearinlys', 'Fyrfadslys', 'Batterier', 'Servietter', 'Madpapir', 'Pærer', 'Tændstikker', 'Støvsugerposer'],
  'Personlig pleje': ['Shampoo', 'Balsam', 'Håndsæbe', 'Showergel', 'Tandpasta', 'Tandbørste', 'Tandtråd', 'Deodorant', 'Bodylotion', 'Håndcreme', 'Barberskrabere', 'Barberskum', 'Bind', 'Tamponer', 'Vatpinde', 'Vatrondeller', 'Plaster', 'Solcreme', 'Læbepomade', 'Hårvoks', 'Panodil'],
  'Baby & børn': ['Bleer', 'Vådservietter', 'Babymad', 'Grødpulver', 'Klemmeposer', 'Modermælkserstatning'],
  'Dyr': ['Kattemad', 'Hundemad', 'Kattegrus', 'Hundesnacks', 'Kattesnacks'],
};
