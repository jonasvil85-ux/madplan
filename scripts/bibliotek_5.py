"""Opskriftsbibliotek del 5: retter til de varer, der ofte er på tilbud, men som biblioteket manglede opskrifter til
(and, kalv, roastbeef, nakkefilet, røget laks, kalkun, kyllingespyd, vildt, lam, søde kartofler og camembert).
Samme format som bibliotek_1: (navn, mængde, enhed, basisvare 0/1, type, nøgle 0/1). nøgle=1: retten medtages kun, hvis ingrediensen er på tilbud.
Mængder er til 4 personer. EN = engelsk billedbeskrivelse (til billedmodellen), skrives ind i billedprompts.json af scripts/byg_bibliotek4.py."""
from bibliotek_1 import R, SALT, OLIE
from bibliotek_4 import PEBER, SMOER, BOUILLON, MEL

EN = {}  # navn -> engelsk beskrivelse af den færdige ret


def r(navn, beskr, niveau, kat, koekken, tid, ing, trin, en, tidligt=False):
    EN[navn] = en
    return R(navn, beskr, niveau, kat, koekken, tid, ing, trin, tidligt)


HVIDLOEG = ('hvidløg', 2, 'fed', 0, '', 0)
LOEG = ('løg', 1, 'stk', 0, 'loeg', 0)

RETTER = [
    # ---------------- AND ----------------
    r("Andebryst med appelsinsauce og kartoffelmos", "Sprødstegt andebryst med frisk appelsinsauce og blød kartoffelmos.", 'weekend', 'and', 'dansk', 45,
      [('andebryst', 700, 'g', 0, 'and', 1), ('kartofler', 1000, 'g', 0, 'kartofler', 0), ('appelsiner', 2, 'stk', 0, '', 0), ('smør', 50, 'g', 0, 'smor', 0),
       ('mælk', 100, 'ml', 0, 'maelk', 0), SALT],
      ["Rids skindet på andebrystene, og steg dem 8 minutter på skindsiden og 4 minutter på den anden side. Lad dem hvile.",
       "Kog de skrællede kartofler møre, og most dem med smør og mælk.", "Kog appelsinjuice med lidt af stegefedtet ind til en sauce.",
       "Skær andebrystet i skiver, og server med mos og sauce."],
      "Sliced pan-seared duck breast with crispy skin, orange sauce and smooth mashed potatoes on a plate"),
    r("Andelår i ovn med rødkål og kartofler", "Mørt andelår fra ovnen med sprød skind, rødkål og kartofler.", 'weekend', 'and', 'dansk', 110,
      [('andelår', 800, 'g', 0, 'and', 1), ('rødkål', 600, 'g', 0, 'rodkaal', 0), ('kartofler', 1000, 'g', 0, 'kartofler', 0), ('æbler', 1, 'stk', 0, 'aeble', 0),
       ('eddike', 2, 'spsk', 1, '', 0), SALT],
      ["Gnid andelårene med salt, og steg dem i ovnen ved 160 grader i 1,5 time. Skru til sidst op på 220 grader, så skindet bliver sprødt.",
       "Snit rødkålen fint, og kog den langsomt med æble i tern, eddike og lidt vand i 45 minutter.", "Kog kartoflerne, og server med and og rødkål."],
      "Roasted duck legs with crisp golden skin, braised red cabbage and boiled potatoes on a plate"),
    r("Helstegt and med æbler og svesker", "Søndagsmad: en hel and fyldt med æbler og svesker, med rødkål og kartofler.", 'weekend', 'and', 'dansk', 150,
      [('hel and', 2500, 'g', 0, 'and', 1), ('æbler', 4, 'stk', 0, 'aeble', 0), ('svesker', 100, 'g', 0, '', 0), ('rødkål', 500, 'g', 0, 'rodkaal', 0),
       ('kartofler', 1000, 'g', 0, 'kartofler', 0), SALT],
      ["Salt anden, og fyld den med skårne æbler og svesker.", "Steg den ved 175 grader i ca. 2 timer, og øs fedtet af undervejs.",
       "Varm rødkålen, og kog kartoflerne.", "Skær anden i stykker, og server med rødkål, kartofler og sauce af stegefonden."],
      "Whole roasted duck with golden skin, baked apples and prunes on a platter with red cabbage and potatoes", tidligt=False),
    r("Wok med andebryst, broccoli og nudler", "Hurtig wok med tynde skiver andebryst, grønt og nudler i sojasauce.", 'familie', 'and', 'asiatisk', 30,
      [('andebryst', 500, 'g', 0, 'and', 1), ('broccoli', 300, 'g', 0, 'broccoli', 0), ('nudler', 250, 'g', 0, 'nudler', 0), ('frisk ingefær', 15, 'g', 0, '', 0),
       ('sojasauce', 3, 'spsk', 1, '', 0), HVIDLOEG, OLIE],
      ["Skær andebrystet i tynde skiver, og steg dem sprøde i en tør wok, til fedtet er stegt ud. Tag dem op.", "Kog nudlerne efter pakken.",
       "Steg broccoli, hvidløg og ingefær i lidt af andefedtet i 4 minutter.", "Vend nudler og and i, og smag til med sojasauce."],
      "Stir-fried sliced duck breast with broccoli and egg noodles in a glossy soy glaze in a bowl"),

    # ---------------- KALV ----------------
    r("Osso buco med tomat og ris", "Møre kalveskanker simret i tomat og grøntsager, serveret med ris.", 'weekend', 'okse', 'italiensk', 130,
      [('osso buco', 1000, 'g', 0, 'osso_buco', 1), ('hakkede tomater', 1, 'dåse', 0, 'hakkede_tomater', 0), ('gulerødder', 2, 'stk', 0, 'gulerod', 0),
       LOEG, ('selleri', 1, 'stk', 0, 'selleri', 0), ('ris', 300, 'g', 0, 'ris', 0), BOUILLON, MEL, OLIE, SALT, PEBER],
      ["Vend skiverne i mel, og brun dem i olie i en gryde. Tag dem op.", "Svits hakket løg, gulerod og selleri, og tilsæt tomater, bouillon og 2 dl vand.",
       "Læg kødet tilbage, og lad det simre under låg i 1,5-2 timer, til det er mørt.", "Kog ris, og server med kødet og sovsen."],
      "Italian osso buco veal shanks in a rich tomato and vegetable sauce served with white rice in a shallow bowl"),
    r("Kalvegryde med svampe og kartofler", "Mør kalvegryde med champignon og fløde, serveret med kartofler.", 'weekend', 'okse', 'dansk', 100,
      [('kalvekød i tern', 800, 'g', 0, 'kalvegryde', 1), ('champignon', 300, 'g', 0, 'champignon', 0), ('kartofler', 800, 'g', 0, 'kartofler', 0), LOEG,
       ('madlavningsfløde', 200, 'ml', 0, 'madlavningsflode', 0), BOUILLON, MEL, SMOER, SALT, PEBER],
      ["Brun kødet i smør i en gryde, og tilsæt hakket løg og skårne svampe.", "Drys med mel, og rør bouillon og 4 dl vand i. Lad det simre under låg i 1 time.",
       "Tilsæt fløden, og lad det småkoge 15 minutter. Kog kartoflerne.", "Smag til med salt og peber, og server."],
      "Creamy veal stew with mushrooms and boiled potatoes on a white plate"),
    r("Kalvekoteletter med smørstegte kartofler og salat", "Saftige kalvekoteletter med smørstegte kartofler og frisk agurkesalat.", 'weekend', 'okse', 'dansk', 40,
      [('kalvekoteletter', 800, 'g', 0, 'kalvekotelet', 1), ('kartofler', 800, 'g', 0, 'kartofler', 0), ('agurk', 1, 'stk', 0, 'agurk', 0), SMOER, ('eddike', 1, 'spsk', 1, '', 0), SALT, PEBER],
      ["Kog kartoflerne næsten møre, og steg dem gyldne i smør.", "Krydr koteletterne, og steg dem 3-4 minutter på hver side. Lad dem hvile.",
       "Rør agurk i skiver med eddike og lidt salt.", "Server koteletterne med kartofler og agurkesalat."],
      "Pan-fried veal chops with golden butter-fried potatoes and fresh cucumber salad on a plate"),

    # ---------------- ROASTBEEF / OKSEMØRBRAD ----------------
    r("Roastbeef med kartoffelsalat og remoulade", "Kold roastbeef i skiver med hjemmelavet kartoffelsalat og remoulade.", 'familie', 'okse', 'dansk', 35,
      [('roastbeef', 700, 'g', 0, 'roastbeef', 1), ('kartofler', 1000, 'g', 0, 'kartofler', 0), ('creme fraiche', 200, 'g', 0, 'creme_fraiche', 0), LOEG,
       ('remoulade', 4, 'spsk', 0, '', 0), ('purløg', 1, 'bundt', 0, '', 0), SALT],
      ["Kog kartoflerne, lad dem køle, og skær dem i tern.", "Rør creme fraiche med fintsnittet løg og purløg, og vend den med kartoflerne.",
       "Skær roastbeefen i tynde skiver, og server med kartoffelsalat og remoulade."],
      "Thin slices of pink roast beef with potato salad and a spoon of remoulade on a plate"),
    r("Mørbrad af okse med flødesauce og ovnkartofler", "Mør oksemørbrad med flødesauce og ovnbagte kartofler.", 'weekend', 'okse', 'dansk', 50,
      [('mørbrad af okse', 700, 'g', 0, 'roastbeef', 1), ('kartofler', 1000, 'g', 0, 'kartofler', 0), ('piskefløde', 200, 'ml', 0, 'piskeflode', 0),
       ('champignon', 200, 'g', 0, 'champignon', 0), SMOER, BOUILLON, SALT, PEBER],
      ["Skær kartoflerne i både, og bag dem i ovnen ved 220 grader i 35 minutter.", "Brun mørbraden i smør på alle sider, og steg den videre i ovnen til den er rosa (kerne 55 grader).",
       "Svits svampene i panden, og kog dem med fløde og bouillon til en sauce.", "Lad kødet hvile, skær det i skiver, og server med sauce og kartofler."],
      "Sliced beef tenderloin medium-rare with creamy mushroom sauce and roasted potato wedges on a plate"),
    r("Wraps med roastbeef, avocado og creme fraiche", "Hurtige wraps med tynde skiver roastbeef, avocado og cremet fyld.", 'student', 'okse', 'amerikansk', 20,
      [('roastbeef', 400, 'g', 0, 'roastbeef', 1), ('tortillas', 8, 'stk', 0, 'wraps', 0), ('avocado', 2, 'stk', 0, 'avocado', 0), ('creme fraiche', 150, 'g', 0, 'creme_fraiche', 0),
       ('agurk', 1, 'stk', 0, 'agurk', 0), SALT],
      ["Skær roastbeef i strimler, avocado i skiver og agurk i stave.", "Smør tortillaerne med creme fraiche.", "Fyld med roastbeef, avocado og agurk, og rul dem sammen."],
      "Tortilla wraps filled with thin roast beef slices, avocado and cucumber, cut in half on a wooden board"),

    # ---------------- NAKKEFILET ----------------
    r("Nakkefilet i fad med sennepssauce og kartofler", "Mør svinenakke i cremet sennepssauce, bagt i fad med kartofler.", 'familie', 'svin', 'dansk', 60,
      [('nakkefilet', 1000, 'g', 0, 'nakkefilet', 1), ('kartofler', 1200, 'g', 0, 'kartofler', 0), ('madlavningsfløde', 200, 'ml', 0, 'madlavningsflode', 0), LOEG,
       ('grov sennep', 2, 'spsk', 1, '', 0), SMOER, SALT, PEBER],
      ["Skær nakkefileten i skiver, og brun dem hurtigt i smør. Læg dem i et ildfast fad med skiveskåret løg og halverede kartofler.",
       "Rør fløde med sennep, og hæld over.", "Bag ved 200 grader i 40 minutter."],
      "Baked pork neck slices in a creamy mustard sauce with onions and potatoes in an oven dish"),
    r("Nakkesteaks med coleslaw og ovnkartofler", "Saftige nakkesteaks med cremet coleslaw og krydrede ovnkartofler.", 'familie', 'svin', 'amerikansk', 45,
      [('nakkefilet', 800, 'g', 0, 'nakkefilet', 1), ('hvidkål', 400, 'g', 0, 'hvidkaal', 0), ('gulerødder', 2, 'stk', 0, 'gulerod', 0), ('creme fraiche', 100, 'g', 0, 'creme_fraiche', 0),
       ('kartofler', 1000, 'g', 0, 'kartofler', 0), ('paprika', 1, 'tsk', 1, '', 0), OLIE, SALT],
      ["Skær kartoflerne i både, vend dem med olie og paprika, og bag dem ved 220 grader i 35 minutter.", "Riv kål og gulerødder, og vend dem med creme fraiche og salt til coleslaw.",
       "Skær nakken i tykke steaks, krydr, og steg dem 4 minutter på hver side.", "Server steaks med coleslaw og kartofler."],
      "Grilled pork neck steaks with creamy coleslaw and roasted potato wedges on a wooden board"),
    r("Nakkefilet med rødkål og kartofler", "Mør nakkefilet med rødkål og kartofler – klassisk hverdagsmad med fylde.", 'familie', 'svin', 'dansk', 55,
      [('nakkefilet', 900, 'g', 0, 'nakkefilet', 1), ('rødkål', 500, 'g', 0, 'rodkaal', 0), ('kartofler', 1000, 'g', 0, 'kartofler', 0), BOUILLON, SMOER, MEL, SALT, PEBER],
      ["Brun nakkefileten i smør, og steg den videre i ovnen ved 180 grader i 35 minutter.", "Varm rødkålen op, og kog kartoflerne.",
       "Lav sovs af stegefonden, mel, bouillon og lidt vand.", "Skær kødet i skiver, og server med rødkål, kartofler og sovs."],
      "Sliced roast pork neck with braised red cabbage, boiled potatoes and brown gravy on a plate"),

    # ---------------- RØGET LAKS ----------------
    r("Pasta med røget laks, creme fraiche og citron", "Cremet pasta med røget laks og citron – klar på 20 minutter.", 'student', 'fisk', 'italiensk', 20,
      [('røget laks', 200, 'g', 0, 'roeget_laks', 1), ('pasta', 400, 'g', 0, 'pasta', 0), ('creme fraiche', 200, 'g', 0, 'creme_fraiche', 0), ('citron', 1, 'stk', 0, 'citron', 0),
       ('frisk spinat', 100, 'g', 0, 'spinat', 0), SALT, PEBER],
      ["Kog pastaen i saltet vand.", "Rør creme fraiche med saft og revet skal fra citronen.", "Vend pastaen med saucen, spinat og røget laks i strimler. Smag til med peber."],
      "Pasta in a creamy lemon sauce with ribbons of smoked salmon and spinach in a rustic bowl"),
    r("Rugbrød med røget laks og rørt æggesalat", "Klassisk lun frokost eller let aftensmad: rugbrød, røget laks og æggesalat.", 'student', 'fisk', 'dansk', 20,
      [('røget laks', 200, 'g', 0, 'roeget_laks', 1), ('rugbrød', 8, 'stk', 0, 'rugbroed', 0), ('æg', 6, 'stk', 0, 'aeg', 0), ('creme fraiche', 100, 'g', 0, 'creme_fraiche', 0),
       ('citron', 1, 'stk', 0, 'citron', 0), ('purløg', 1, 'bundt', 0, '', 0), SALT],
      ["Hårdkog æggene i 9 minutter, og hak dem groft.", "Rør æggene med creme fraiche, purløg og salt.", "Læg æggesalat og røget laks på rugbrødet, og pynt med citron."],
      "Danish open-faced sandwiches on dark rye bread with smoked salmon, egg salad, chives and lemon on a plate"),
    r("Laksewraps med avocado og agurk", "Hurtige wraps med røget laks, avocado og cremet fyld.", 'student', 'fisk', 'amerikansk', 15,
      [('røget laks', 200, 'g', 0, 'roeget_laks', 1), ('tortillas', 8, 'stk', 0, 'wraps', 0), ('avocado', 2, 'stk', 0, 'avocado', 0), ('agurk', 1, 'stk', 0, 'agurk', 0),
       ('creme fraiche', 150, 'g', 0, 'creme_fraiche', 0), ('citron', 1, 'stk', 0, 'citron', 0), SALT],
      ["Rør creme fraiche med citronsaft og salt.", "Smør den på tortillaerne, og læg laks, avocadoskiver og agurk på.", "Rul dem sammen, og skær dem over."],
      "Tortilla wraps with smoked salmon, avocado slices and cucumber with a creamy filling cut in half"),
    r("Kartoffelsalat med røget laks og æg", "Lun kartoffelsalat med røget laks, æg og dild.", 'familie', 'fisk', 'dansk', 30,
      [('røget laks', 250, 'g', 0, 'roeget_laks', 1), ('kartofler', 800, 'g', 0, 'kartofler', 0), ('æg', 4, 'stk', 0, 'aeg', 0), ('creme fraiche', 200, 'g', 0, 'creme_fraiche', 0),
       ('dild', 1, 'bundt', 0, '', 0), ('citron', 1, 'stk', 0, 'citron', 0), SALT, PEBER],
      ["Kog kartoflerne, og skær dem i tern. Hårdkog æggene.", "Rør creme fraiche med dild, citronsaft, salt og peber.",
       "Vend kartoflerne med dressingen, og læg laks og æg i både ovenpå."],
      "Warm potato salad with smoked salmon, halved boiled eggs and fresh dill on a white plate"),

    # ---------------- KALKUN ----------------
    r("Kalkunstroganoff med ris", "Cremet stroganoff på kalkunbryst og champignon, serveret med ris.", 'familie', 'andet', 'dansk', 30,
      [('kalkunbryst', 600, 'g', 0, 'kalkun', 1), ('ris', 300, 'g', 0, 'ris', 0), ('champignon', 250, 'g', 0, 'champignon', 0), ('creme fraiche', 200, 'g', 0, 'creme_fraiche', 0),
       LOEG, ('paprika', 1, 'tsk', 1, '', 0), SMOER, SALT, PEBER],
      ["Skær kalkunen i strimler, og brun den i smør. Tag den op.", "Svits løg og svampe, og drys med paprika.",
       "Tilsæt creme fraiche og kødet, og lad det varme igennem. Kog imens ris.", "Smag til, og server over ris."],
      "Creamy turkey stroganoff with mushrooms served over white rice in a shallow bowl"),
    r("Kalkunburgere med coleslaw", "Saftige burgere af hakket kalkun med cremet coleslaw.", 'familie', 'andet', 'amerikansk', 30,
      [('hakket kalkunkød', 600, 'g', 0, 'kalkun', 1), ('burgerboller', 4, 'stk', 0, 'burgerboller', 0), ('hvidkål', 300, 'g', 0, 'hvidkaal', 0), ('gulerødder', 1, 'stk', 0, 'gulerod', 0),
       ('creme fraiche', 100, 'g', 0, 'creme_fraiche', 0), ('æg', 1, 'stk', 0, 'aeg', 0), SALT, PEBER, OLIE],
      ["Ælt kalkun med æg, salt og peber, og form 4 bøffer. Steg dem 5 minutter på hver side.", "Riv kål og gulerod, og vend dem med creme fraiche til coleslaw.",
       "Rist bollerne, og fyld dem med bøf og coleslaw."],
      "Juicy turkey burgers in toasted buns with creamy coleslaw served on a wooden board"),
    r("Kalkunbryst i fad med broccoli og ris", "Mør kalkunbryst bagt med broccoli i cremet sauce, serveret med ris.", 'familie', 'andet', 'dansk', 40,
      [('kalkunbrystfilet', 700, 'g', 0, 'kalkun', 1), ('broccoli', 400, 'g', 0, 'broccoli', 0), ('ris', 300, 'g', 0, 'ris', 0), ('madlavningsfløde', 200, 'ml', 0, 'madlavningsflode', 0),
       ('revet ost', 100, 'g', 0, 'revet_ost', 0), SALT, PEBER],
      ["Skær kalkunen i skiver, og læg den i et ildfast fad med broccolibuketter.", "Hæld fløde over, drys med ost, og bag ved 200 grader i 25 minutter.", "Kog ris, og server."],
      "Baked turkey breast slices with broccoli in a creamy cheese sauce in an oven dish with rice"),

    # ---------------- KYLLINGESPYD ----------------
    r("Kyllingespyd med ris og agurkesalat", "Grillede kyllingespyd med ris og kølig agurkesalat med skyr.", 'familie', 'kylling', 'middelhav', 30,
      [('kyllingespyd', 600, 'g', 0, 'kyllingespyd', 1), ('ris', 300, 'g', 0, 'ris', 0), ('agurk', 1, 'stk', 0, 'agurk', 0), ('skyr', 200, 'g', 0, 'skyr', 0), ('citron', 1, 'stk', 0, 'citron', 0), SALT],
      ["Steg eller grill spyddene gennemstegte, ca. 12-15 minutter.", "Kog ris. Rør agurk i tern med skyr, citronsaft og salt.", "Server spyd med ris og agurkesalat."],
      "Grilled chicken skewers with white rice and cucumber yoghurt salad on a plate"),
    r("Kyllingespyd i pita med tzatziki", "Kyllingespyd i varmt pitabrød med grønt og tzatziki.", 'familie', 'kylling', 'middelhav', 25,
      [('kyllingespyd', 600, 'g', 0, 'kyllingespyd', 1), ('pitabrød', 8, 'stk', 0, 'pita', 0), ('skyr', 250, 'g', 0, 'skyr', 0), ('agurk', 1, 'stk', 0, 'agurk', 0),
       ('tomater', 2, 'stk', 0, 'tomater', 0), HVIDLOEG, SALT],
      ["Steg spyddene gennemstegte, og tag kødet af.", "Rør skyr med revet agurk, hvidløg og salt til tzatziki.", "Varm pitabrødene, og fyld dem med kød, tomat og tzatziki."],
      "Warm pita bread filled with grilled chicken pieces, tomato and tzatziki on a plate"),

    # ---------------- VILDT ----------------
    r("Fasanbryst med æbler og fløde", "Mør fasanbryst med æbler og fløde – efterårsmad til weekenden.", 'weekend', 'andet', 'dansk', 40,
      [('fasanbryst', 600, 'g', 0, 'fasan', 1), ('kartofler', 800, 'g', 0, 'kartofler', 0), ('æbler', 2, 'stk', 0, 'aeble', 0), ('piskefløde', 150, 'ml', 0, 'piskeflode', 0), SMOER, BOUILLON, SALT, PEBER],
      ["Brun fasanbrystene i smør, og steg dem færdige i ovnen ved 180 grader i 15 minutter.", "Steg æbleskiver i panden, og tilsæt fløde og bouillon. Kog ind til en sauce.",
       "Kog kartoflerne, og server med fasan og sauce."],
      "Roasted pheasant breast with apples and a cream sauce and boiled potatoes on a plate"),
    r("Krondyrgryde med rodfrugter", "Langtidsstegt gryde af krondyr med rodfrugter – rigtig efterårsmad.", 'weekend', 'andet', 'dansk', 130,
      [('krondyrkød i tern', 800, 'g', 0, 'krondyr', 1), ('pastinakker', 300, 'g', 0, 'pastinak', 0), ('gulerødder', 3, 'stk', 0, 'gulerod', 0), LOEG, ('kartofler', 600, 'g', 0, 'kartofler', 0),
       BOUILLON, MEL, SMOER, SALT, PEBER],
      ["Vend kødet i mel, og brun det i smør i en gryde.", "Tilsæt hakket løg, rodfrugter i stykker, bouillon og 5 dl vand.", "Lad det simre under låg i 1,5 time.", "Kog kartoflerne, og server."],
      "Rich venison stew with root vegetables and potatoes in a deep bowl"),

    # ---------------- LAM ----------------
    r("Lammekølle med rosmarin og ovnkartofler", "Helstegt lammekølle med hvidløg og rosmarin og ovnbagte kartofler.", 'weekend', 'andet', 'middelhav', 150,
      [('lammekølle', 1500, 'g', 0, 'lam', 1), ('kartofler', 1000, 'g', 0, 'kartofler', 0), ('hvidløg', 4, 'fed', 0, '', 0), ('rosmarin', 1, 'bundt', 0, '', 0), OLIE, SALT, PEBER],
      ["Stik huller i kødet, og fyld dem med hvidløg og rosmarin. Gnid med salt, peber og olie.", "Steg ved 160 grader i 1,5-2 timer, til kernetemperaturen er 65-70 grader.",
       "Bag kartofler i både i ovnen sammen med kødet den sidste time.", "Lad kødet hvile, og skær det i skiver."],
      "Roast leg of lamb with rosemary and garlic served with roasted potatoes on a platter"),
    r("Lammegryde med bønner og tomat", "Mør lammegryde med hvide bønner og tomat – middelhavsmad med fylde.", 'weekend', 'andet', 'middelhav', 110,
      [('lammekød', 800, 'g', 0, 'lam', 1), ('hakkede tomater', 2, 'dåse', 0, 'hakkede_tomater', 0), ('kikærter', 1, 'dåse', 0, 'kikaerter', 0), LOEG, HVIDLOEG, BOUILLON, OLIE, SALT, PEBER],
      ["Brun kødet i olie i en gryde. Tilsæt hakket løg og hvidløg.", "Tilsæt tomater, bouillon og 2 dl vand, og lad det simre under låg i 1,5 time.",
       "Tilsæt kikærter, og lad det koge 10 minutter. Server med brød eller ris."],
      "Slow-cooked lamb stew with chickpeas and tomato sauce in a rustic bowl"),

    # ---------------- SØDE KARTOFLER ----------------
    r("Sødkartoffelcurry med kokosmælk og kikærter", "Vegetarisk curry med søde kartofler, kikærter og kokosmælk, serveret med ris.", 'student', 'vegetar', 'asiatisk', 35,
      [('søde kartofler', 800, 'g', 0, 'soede_kartofler', 1), ('kokosmælk', 400, 'ml', 0, 'kokosmaelk', 0), ('kikærter', 1, 'dåse', 0, 'kikaerter', 0), LOEG, ('ris', 300, 'g', 0, 'ris', 0),
       ('karry', 2, 'spsk', 1, '', 0), HVIDLOEG, OLIE, SALT],
      ["Svits hakket løg og hvidløg med karry i olie.", "Tilsæt søde kartofler i tern, kokosmælk, kikærter og lidt vand, og lad det simre i 20 minutter.", "Kog ris, og server."],
      "Sweet potato and chickpea curry in coconut milk served with white rice in a bowl"),
    r("Fyldte søde kartofler med bønner og avocado", "Bagte søde kartofler fyldt med varme bønner, avocado og skyr.", 'student', 'vegetar', 'amerikansk', 50,
      [('søde kartofler', 1000, 'g', 0, 'soede_kartofler', 1), ('kidneybønner', 1, 'dåse', 0, 'kidneyboenner', 0), ('avocado', 2, 'stk', 0, 'avocado', 0), ('skyr', 150, 'g', 0, 'skyr', 0),
       ('spidskommen', 1, 'tsk', 1, '', 0), SALT],
      ["Bag de hele søde kartofler ved 200 grader i 40 minutter.", "Varm bønnerne med spidskommen.", "Skær kartoflerne op, og fyld dem med bønner, avocado og skyr."],
      "Baked sweet potato halves topped with beans, sliced avocado and a spoon of yoghurt on a plate"),
    r("Ovnbagte søde kartofler med feta og spinat", "Søde kartofler fra ovnen med salt feta og friske spinatblade.", 'student', 'vegetar', 'middelhav', 45,
      [('søde kartofler', 1000, 'g', 0, 'soede_kartofler', 1), ('feta', 150, 'g', 0, 'feta', 0), ('frisk spinat', 150, 'g', 0, 'spinat', 0), ('rødløg', 1, 'stk', 0, '', 0), OLIE, SALT],
      ["Skær søde kartofler i både, vend dem med olie og salt, og bag dem ved 220 grader i 30 minutter.", "Kom spinat og rødløg i skiver på, og smuldr feta ovenpå."],
      "Roasted sweet potato wedges topped with feta cheese, fresh spinach and red onion on a tray"),
    r("Sødkartoffelsuppe med kokosmælk", "Fløjlsblød suppe af søde kartofler og kokosmælk med ingefær.", 'student', 'vegetar', 'vegetar', 35,
      [('søde kartofler', 800, 'g', 0, 'soede_kartofler', 1), ('kokosmælk', 400, 'ml', 0, 'kokosmaelk', 0), LOEG, ('frisk ingefær', 15, 'g', 0, '', 0), BOUILLON, ('brød', 1, 'stk', 0, 'braed', 0), SALT],
      ["Svits løg og ingefær i en gryde. Tilsæt søde kartofler i tern og 1 liter vand med bouillon, og kog dem møre.", "Blend suppen med kokosmælken, og smag til med salt. Server med brød."],
      "Smooth orange sweet potato and coconut soup in a bowl with bread on the side"),

    # ---------------- CAMEMBERT / BRIE ----------------
    r("Bagt camembert med æbler og rugbrød", "Varm, flydende camembert med bagte æbler og honning, serveret med rugbrød.", 'student', 'vegetar', 'dansk', 25,
      [('camembert', 500, 'g', 0, 'camembert', 1), ('æbler', 2, 'stk', 0, 'aeble', 0), ('honning', 2, 'spsk', 1, '', 0), ('rugbrød', 8, 'stk', 0, 'rugbroed', 0), ('valnødder', 50, 'g', 0, '', 0)],
      ["Læg camembert i et ildfast fad, og bag den ved 200 grader i 15 minutter.", "Steg æbleskiver i panden med honning, til de er bløde.",
       "Server den varme ost med æbler, valnødder og rugbrød."],
      "Baked camembert with caramelised apple slices, walnuts and dark rye bread on a wooden board"),
]
