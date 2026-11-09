"""Opskriftsbibliotek del 7: ugens nye retter, hentet som INSPIRATION fra åbne opskrifter (idéen til en ret, ikke teksten) og skrevet om med egne ord, egne mængder
og egne trin, så de passer til de varer, der er på tilbud. Kopiér aldrig tekst, ingredienslister eller billeder fra andre sider.
Samme format som bibliotek_1: (navn, mængde, enhed, basis 0/1, type, nøgle 0/1). Mængder er til 4 personer. EN = engelsk billedbeskrivelse.

Pilot (uge 46, 2026): idéer fra valdemarsro.dk (stegte fyldte pitabrød, linsedhal, pasta med squash), gastromand.dk (fish and chips med ærtemos)
og opskrifter.dk (bønnegryde med pølser, bøfsalat)."""
from bibliotek_1 import R, SALT, OLIE
from bibliotek_4 import PEBER

EN = {}


def r(navn, beskr, niveau, kat, koekken, tid, ing, trin, en, tidligt=False):
    EN[navn] = en
    return R(navn, beskr, niveau, kat, koekken, tid, ing, trin, tidligt)


HVIDLOEG = ('hvidløg', 2, 'fed', 0, '', 0)
LOEG = ('løg', 1, 'stk', 0, 'loeg', 0)
CITRON = ('citron', 1, 'stk', 0, 'citron', 0)

RETTER = [
    r("Stegte pitabrød fyldt med krydret hakket kød", "Sprøde pitabrød fyldt med krydret hakket oksekød og løg, serveret med frisk tzatziki og tomatsalat.", 'familie', 'okse', 'middelhav', 40,
      [('hakket oksekød', 500, 'g', 0, 'hakket_okse', 1), ('pitabrød', 4, 'stk', 0, 'pita', 0), LOEG, ('persille', 1, 'bundt', 0, '', 0), ('spidskommen', 1, 'tsk', 1, '', 0),
       ('paprika', 1, 'tsk', 1, '', 0), ('skyr', 250, 'g', 0, 'skyr', 0), ('agurk', 1, 'stk', 0, 'agurk', 0), ('cherrytomater', 250, 'g', 0, 'tomater', 0), HVIDLOEG, OLIE, SALT],
      ["Riv løget fint, og hak persillen. Ælt hakket kød med løg, persille, spidskommen, paprika, 1 tsk salt og peber.",
       "Skær hver pita over på midten, så du får to lommer. Fyld hver lomme med et tyndt lag kødfars, og tryk den flad.",
       "Steg pitaerne i lidt olie på en pande ved middel varme, 4-5 minutter på hver side, til kødet er gennemstegt (ingen rosa) og brødet er sprødt.",
       "Rør skyr med revet agurk (pres væden fra), knust hvidløg og lidt salt til tzatziki. Skær tomaterne i både, og vend dem med salt og olie.",
       "Server de varme pitabrød med tzatziki og tomatsalat."],
      "Crispy pan-fried pita breads filled with spiced minced beef, cut in halves on a plate with tzatziki and tomato salad"),
    r("Ovnbagt fish and chips med ærtemos og remoulade", "Sprød ovnbagt fisk i rasp med kartoffelbåde, cremet ærtemos og remoulade.", 'familie', 'fisk', 'amerikansk', 45,
      [('torskefilet', 700, 'g', 0, 'hvid_fisk', 1), ('kartofler', 1000, 'g', 0, 'kartofler', 0), ('ærter', 400, 'g', 0, '', 0), ('rasp', 100, 'g', 0, '', 0), ('æg', 2, 'stk', 0, 'aeg', 0),
       ('hvedemel', 3, 'spsk', 1, '', 0), ('remoulade', 6, 'spsk', 0, '', 0), CITRON, OLIE, SALT],
      ["Tænd ovnen på 220 grader. Skær kartoflerne i både, vend dem med 3 spsk olie og salt, og bag dem i 35-40 minutter, til de er gyldne og møre. Vend dem halvvejs.",
       "Skær fisken i 4 stykker, og krydr med salt og peber. Vend dem i mel, derefter i sammenpisket æg, og til sidst i rasp blandet med 2 spsk olie.",
       "Læg fisken på en bageplade med bagepapir, og bag den de sidste 12-15 minutter, til den er gylden og kan skilles i flager.",
       "Kog ærterne 3 minutter i letsaltet vand. Mos dem groft med 1 spsk olie, citronsaft, salt og peber.",
       "Server fisk og kartoffelbåde med ærtemos, remoulade og citronbåde."],
      "Oven-baked crispy breadcrumb coated white fish fillets with potato wedges, mushy peas and remoulade on a plate with lemon wedges"),
    r("Gryde med pølser og hvide bønner", "Mættende vintergryde med pølser, hvide bønner, gulerødder og tomat – serveres med godt brød.", 'student', 'svin', 'dansk', 45,
      [('pølser', 500, 'g', 0, 'polser', 1), ('hvide bønner', 2, 'dåse', 0, 'kidneyboenner', 0), ('hakkede tomater', 1, 'dåse', 0, 'hakkede_tomater', 0), ('gulerødder', 3, 'stk', 0, 'gulerod', 0),
       LOEG, HVIDLOEG, ('tørret timian', 1, 'tsk', 1, '', 0), ('bouillon', 1, 'stk', 1, '', 0), ('brød', 1, 'stk', 0, 'braed', 0), OLIE, SALT],
      ["Skær løg og gulerødder i tern, og skær pølserne i skiver. Svits løg og gulerødder 5 minutter i olie i en gryde.",
       "Tilsæt pølser og knust hvidløg, og brun dem let i 4-5 minutter.",
       "Tilsæt hakkede tomater, skyllede bønner, timian, bouillonterning og 3 dl vand. Kog op, og lad det simre under låg i 20 minutter.",
       "Smag til med salt og peber. Server med brødet."],
      "Hearty sausage and white bean stew with carrots and tomato in a bowl with a slice of crusty bread"),
    r("Bøfsalat med bagte tomater og sennepsdressing", "Lun salat med medium-stegte bøffer i skiver, bagte tomater og en frisk sennepsdressing.", 'familie', 'okse', 'dansk', 35,
      [('oksebøffer', 600, 'g', 0, 'oksebof', 1), ('cherrytomater', 400, 'g', 0, 'tomater', 0), ('rucola', 100, 'g', 0, '', 0), ('rødløg', 1, 'stk', 0, '', 0), ('kartofler', 600, 'g', 0, 'kartofler', 0),
       ('sennep', 1, 'spsk', 1, '', 0), ('eddike', 2, 'spsk', 1, '', 0), ('honning', 1, 'tsk', 0, '', 0), OLIE, SALT],
      ["Tænd ovnen på 200 grader. Skær kartoflerne i både, og vend dem med 2 spsk olie og salt. Bag dem i 30-35 minutter.",
       "Læg cherrytomater på en bageplade med 1 spsk olie og salt, og bag dem de sidste 15 minutter, til de begynder at falde sammen.",
       "Tag bøfferne ud af køleskabet 20 minutter før. Krydr dem med salt og peber, og steg dem i en meget varm pande med olie, 3-4 minutter på hver side til medium (kernetemperatur ca. 55 grader). Lad dem hvile 5 minutter, og skær dem i tynde skiver.",
       "Rør sennep, eddike, honning og 3 spsk olie til dressing. Skær rødløget i tynde ringe.",
       "Læg rucola, kartofler, tomater og bøfskiver på fade, og dryp dressing over."],
      "Warm steak salad with sliced medium-rare beef, roasted cherry tomatoes, arugula, potato wedges and mustard dressing on a plate"),
    r("Linsedhal med kokosmælk og ris", "Cremet indisk linsegryde med kokosmælk, tomat og ingefær – vegetarisk og mættende.", 'student', 'vegetar', 'asiatisk', 40,
      [('røde linser', 300, 'g', 0, '', 0), ('kokosmælk', 400, 'ml', 0, 'kokosmaelk', 1), ('hakkede tomater', 1, 'dåse', 0, 'hakkede_tomater', 0), ('ris', 280, 'g', 0, 'ris', 0), LOEG, HVIDLOEG,
       ('ingefær', 1, 'spsk', 1, '', 0), ('karry', 2, 'tsk', 1, '', 0), ('gurkemeje', 1, 'tsk', 1, '', 0), ('spinat', 150, 'g', 0, 'spinat', 0), CITRON, OLIE, SALT],
      ["Skyl linserne. Svits hakket løg, hvidløg og ingefær i olie i en gryde i 4 minutter, og rør karry og gurkemeje i.",
       "Tilsæt linser, hakkede tomater, kokosmælk og 4 dl vand. Kog op, og lad det simre under låg i 20-25 minutter, til linserne er helt møre. Rør jævnligt, og tilsæt lidt vand, hvis den bliver for tyk.",
       "Kog risene efter anvisningen på posen.",
       "Vend spinat i dhalen, til den falder sammen. Smag til med salt og citronsaft.",
       "Server dhalen over ris."],
      "Creamy red lentil dal with coconut milk and spinach served over rice in a bowl with a lemon wedge"),
    r("Pasta med squash, parmesan og citron", "Cremet pasta med smørstegt squash, parmesan og citron – klar på 25 minutter.", 'student', 'vegetar', 'italiensk', 25,
      [('squash', 3, 'stk', 0, 'squash', 1), ('pasta', 400, 'g', 0, 'pasta', 0), ('parmesan', 80, 'g', 0, 'parmesan', 0), ('smør', 40, 'g', 0, 'smor', 0), HVIDLOEG, CITRON,
       ('basilikum', 1, 'bundt', 0, '', 0), OLIE, SALT],
      ["Riv squashen groft, drys med 1 tsk salt, og lad den stå 10 minutter. Pres væden fra i et rent viskestykke.",
       "Kog pastaen i saltet vand, og gem 2 dl af kogevandet.",
       "Steg squashen i smør og olie i en stor pande ved middel varme i 8-10 minutter, til den er gylden. Tilsæt knust hvidløg de sidste 2 minutter.",
       "Vend pastaen i panden sammen med halvdelen af parmesanen, citronskal, citronsaft og kogevand efter behov, til sovsen er cremet.",
       "Server med resten af parmesanen, basilikum og peber."],
      "Pasta with golden grated zucchini, parmesan and lemon zest in a white bowl with fresh basil"),
]
