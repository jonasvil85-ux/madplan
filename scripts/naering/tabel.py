"""Opslagstabel til næringsberegning (DEMO): danske ingrediensnavne -> fødevare i foedevarer.json + omregning til gram.

Næringsværdier pr. 100 g RÅ vare kommer fra USDA FoodData Central (SR Legacy, offentligt frit tilgængelig). Posterne er valgt i hånden
(fdc_id står i foedevarer.json). Tallene er amerikanske, så de kan afvige fra danske varer – derfor skal de på sigt skiftes til Frida (DTU).

Hver regel: (regex på ingrediensnavn i små bogstaver, fødevare-nøgle, omregning)
  omregning er en dict med gram pr. enhed ('stk', 'spsk', 'tsk', 'fed', 'dåse', 'glas', 'pakke', 'bundt', 'skive'), evt. 'ml' (gram pr. ml, standard 1.0),
  'spild' (spiselig andel, fx 0.65 for kød med ben) og 'faktor' (gang alle værdier, fx 0.55 for remoulade i forhold til mayonnaise).
Første regel der matcher vinder. Ingredienser uden regel tælles som "ukendt"; krydderier og lignende ignoreres (IGNORER)."""
import re

IGNORER = re.compile(
    r'^(salt|sort peber|peber|vand)\b|groft salt|garam masala|salt og peber|krydder|oregano|timian|spidskommen|^paprika|karry|kanel|laurbær|muskat|bouillon|fond\b|kulør|'
    r'asia cubes|terning|dild|persille|purløg|koriander|mynte|basilikum|rosmarin|eddike|chili|cayenne|gurkemeje|worcester|laurbær|sennepsfrø|'
    r'safran|vanille|bagepulver|gær|lakrids|sesam', re.I)

FOEDEVARE_ID = {
    'loeg': '170000', 'hvidloeg': '169230', 'smoer': '173410', 'olie': '171413', 'hvedemel': '168894', 'majsstivelse': '169698',
    'kartoffel': '170026', 'soed_kartoffel': '168482', 'gulerod': '170393', 'aeg': '171287', 'tomat_knust': '170501', 'tomat': '170457', 'tomatpure': '170459',
    'maelk': '171265', 'kokosmaelk': '170173', 'piskeflode': '170859', 'flode_let': '171255', 'cremefraiche': '171257', 'skyr': '170894', 'yoghurt': '171284',
    'kyllingebryst': '171077', 'kyllingelaar': '173619', 'hel_kylling': '171447', 'hakket_okse_95': '171790', 'hakket_okse_85': '171796', 'hakket_okse_90': '174030',
    'hakket_gris': ('167902', '169190'), 'moerbrad': '168312', 'koteletter': '167839', 'nakke': '167843', 'flaesk': '167812', 'bacon': '168277', 'polse': '172964',
    'oksebof': '171804', 'laks': '175167', 'roeget_laks': '173687', 'rejer': '175179', 'torsk': '171955', 'sild': '175118', 'tun': '175158',
    'and': '172408', 'hakket_kalv': '175290', 'lam': '172486',
    'ris': '168877', 'pasta': '169736', 'nudler': '169731', 'couscous': '169699', 'hvedebroed': '172686', 'rugbroed': '172684', 'pita': '174915', 'tortilla': '167535',
    'cheddar': '170899', 'parmesan': '170848', 'mozzarella': '170847', 'feta': '173420', 'floedeost': '173418', 'gouda': '171241', 'hytteost': '172182',
    'agurk': '168409', 'broccoli': '170379', 'squash': '169291', 'peberfrugt': '170108', 'porre': '169246', 'kaal': '169975', 'roedkaal': '169977', 'champignon': '169251',
    'spinat': '168462', 'salat': '169249', 'groenkaal': '168421', 'pastinak': '170417', 'roedbede': '170480', 'selleri': '169988', 'graeskar': '168448', 'aeble': '171688',
    'avocado': '171705', 'havregryn': '172989', 'kikaerter': '175206', 'citron': '167746', 'aerter': '170016', 'majs': '169216', 'oliven': '169094', 'kidney': '174285', 'linser': '172420', 'ingefaer': '169231',
    'sukker': '169655', 'honning': '169640', 'ketchup': '168556', 'sennep': '172234', 'mayo': '171009', 'soja': '174277',
}

U = lambda **k: k  # noqa: E731

REGLER = [
    # krydderurter m.m. ignoreres i IGNORER; her kun varer med næring
    (r'søde kartofler|sød kartoffel', 'soed_kartoffel', U(stk=200)),
    (r'kartof|bagekartof', 'kartoffel', U(stk=150)),
    (r'skalotte|rødløg|forårsløg|\bløg\b|^løg', 'loeg', U(stk=110)),
    (r'hvidløg', 'hvidloeg', U(fed=3, stk=40)),
    (r'smør\b|kærgården', 'smoer', U()),
    (r'olivenolie|rapsolie|olie', 'olie', U(spsk=13.5, tsk=4.5, ml=0.92)),
    (r'hvedemel|rasp|mel\b', 'hvedemel', U(spsk=8, tsk=3)),
    (r'maizena', 'majsstivelse', U(spsk=8)),
    (r'gulerød|gulerod', 'gulerod', U(stk=80)),
    (r'^æg\b|økologiske æg|frilandsæg|^æg', 'aeg', U(stk=55)),
    (r'hakkede tomater|flåede tomater|tomater på dåse|hakket tomat', 'tomat_knust', U(dåse=400)),
    (r'tomatpuré', 'tomatpure', U(spsk=16, tsk=5)),
    (r'cherrytomater|tomat', 'tomat', U(stk=120)),
    (r'kokosmælk', 'kokosmaelk', U(ml=0.97)),
    (r'(?<!kokos)mælk|kærnemælk|havredrik', 'maelk', U(ml=1.03)),
    (r'piskefløde', 'piskeflode', U(ml=0.99)),
    (r'madlavningsfløde|madlavningsjævner|milbona|fløde(?!ost)', 'flode_let', U(ml=1.0)),
    (r'creme fraiche', 'cremefraiche', U(ml=1.0, spsk=15)),
    (r'skyr|græsk yoghurt|græsk(?!ar)', 'skyr', U(spsk=15)),
    (r'yoghurt', 'yoghurt', U(spsk=15, ml=1.03)),
    (r'kyllingebryst|kyllingebrystfilet|kylling i tern|kyllingestrimler|kyllingespyd|kyllingefilet', 'kyllingebryst', U()),
    (r'kyllingelårfilet|kyllingeinderfilet|hakket kylling|hakket dansk kylling|kyllingekød|kyllingefilet', 'kyllingelaar', U()),
    (r'kyllingeover|kyllingeunder|kyllingelår|stegeben|kyllingeben|kyllingevinger', 'kyllingelaar', U(spild=0.65)),
    (r'hel kylling|helstegt kylling', 'hel_kylling', U(spild=0.65, stk=1200)),
    (r'hakket oksekød.*(4-7|5)\s*%|hakket oksekød 4-7', 'hakket_okse_95', U()),
    (r'hakket oksekød.*(15|18)', 'hakket_okse_85', U()),
    (r'hakket oksekød|hakket okse|oksekød hakket', 'hakket_okse_90', U()),
    (r'hakket kalv|kalvekød', 'hakket_kalv', U()),
    (r'hakket gris|hakket svin|grisekød|svinekød|salsiccia|medister|pulled pork|chorizo|spareribs', 'hakket_gris', U()),
    (r'svinemørbrad|mørbrad', 'moerbrad', U()),
    (r'kotelet|svinekam|kamsteg', 'koteletter', U()),
    (r'nakkefilet|nakkesteg|(?<![a-zæøå])nakke', 'nakke', U()),
    (r'flæskesteg|ribbensteg|ribben|skinkesteg|krogmodnet', 'nakke', U(spild=0.9)),
    (r'flæsk i skiver|stegeflæsk|^flæsk|flæsk', 'flaesk', U()),
    (r'bacon', 'bacon', U()),
    (r'pølse|pølser|frankfurter|hotdog(?!brød)', 'polse', U()),
    (r'oksebøf|oksefilet|flanksteak|flap meat|entrecote|steak|culotte|oksekød|oksemørbrad|tyndsteg|roastbeef|okse(?!bouillon)', 'oksebof', U()),
    (r'røget laks|gravad laks|koldrøget|varmrøget', 'roeget_laks', U()),
    (r'laks', 'laks', U()),
    (r'rejer', 'rejer', U()),
    (r'torsk|fiskefilet|hvid fisk|sej\b|mørksej|sejfilet|rødspætte|kuller|hellefisk|fisk', 'torsk', U()),
    (r'sild', 'sild', U()),
    (r'tun\b|tunfisk', 'tun', U(dåse=150)),
    (r'andebryst|andelår|^and\b|fritgående and|\band\b|and$|ferske and', 'and', U(spild=0.55, stk=2500, faktor=0.75)),
    (r'lam\b|lammekølle|lammekotelet|lammeculotte|lamme', 'lam', U(spild=0.8)),
    (r'jasminris|grødris|risengrød|\bris\b|basmati|^ris', 'ris', U()),
    (r'lasagneplader|spaghetti|penne|fettuccine|makaroni|macaroni|pasta|tagliatelle|fusilli|farfalle|rigatoni', 'pasta', U()),
    (r'nudler|mie', 'nudler', U()),
    (r'couscous', 'couscous', U()),
    (r'pizzadej|butterdej|dej\b', 'hvedebroed', U(g=1)),
    (r'havregryn', 'havregryn', U(spsk=8)),
    (r'rugbrød', 'rugbroed', U(skive=40, stk=40, pakke=500)),
    (r'pitabrød|pita', 'pita', U(pakke=330, stk=60)),
    (r'tortilla|wrap', 'tortilla', U(pakke=320, stk=40)),
    (r'burgerboller|boller|rundstykke', 'hvedebroed', U(stk=70)),
    (r'baguette', 'hvedebroed', U(stk=250)),
    (r'brød|toast|brioche|sandwich', 'hvedebroed', U(stk=40, skive=40, pakke=500)),
    (r'revet ost|cheddar|skæreost|emmentaler|danbo|havarti', 'cheddar', U()),
    (r'grana padano|parmesan|parmigiano', 'parmesan', U()),
    (r'mozzarella', 'mozzarella', U()),
    (r'feta', 'feta', U()),
    (r'flødeost|philadelphia|smelteost', 'floedeost', U()),
    (r'halloumi|paneer|saint agur|blåskimmel', 'feta', U()),
    (r'brie|camembert|gouda|(?<![a-zæøå])ost\b', 'gouda', U()),
    (r'hytteost', 'hytteost', U()),
    (r'agurk', 'agurk', U(stk=300)),
    (r'broccoli', 'broccoli', U(stk=350)),
    (r'squash', 'squash', U(stk=250)),
    (r'peberfrugt|rød peber|snackpebre|spidspeber|peber(?!frugt)', 'peberfrugt', U(stk=160)),
    (r'porre', 'porre', U(stk=150)),
    (r'rødkål|rødkål \(frisk\)', 'roedkaal', U(stk=800, glas=450, pakke=450)),
    (r'grønkål', 'groenkaal', U()),
    (r'hvidkål|spidskål|kål\b|kål', 'kaal', U(stk=800)),
    (r'champignon|svampe|portobello', 'champignon', U()),
    (r'spinat', 'spinat', U()),
    (r'rucola|salat|iceberg', 'salat', U(stk=150)),
    (r'grønkål', 'groenkaal', U()),
    (r'pastinak', 'pastinak', U(stk=100)),
    (r'rødbede|syltede rødbeder', 'roedbede', U()),
    (r'selleri', 'selleri', U(stk=60)),
    (r'græskar|hokkaido|butternut', 'graeskar', U(stk=800)),
    (r'æble', 'aeble', U(stk=150)),
    (r'avocado', 'avocado', U(stk=150)),
    (r'citron|lime', 'citron', U(stk=60)),
    (r'(?<![a-zæøå])ærter', 'aerter', U()),
    (r'majs', 'majs', U(dåse=285)),
    (r'oliven', 'oliven', U()),
    (r'kikærter', 'kikaerter', U(dåse=240)),
    (r'svesker|dadler|figner|rosiner', 'sukker', U(faktor=0.8)),
    (r'pak choi|grøntsagsblanding|wokmix', 'broccoli', U(stk=200)),
    (r'appelsin|clementin|mandarin', 'aeble', U(stk=150)),
    (r'kidney|bønner', 'kidney', U(dåse=240)),
    (r'linser', 'linser', U()),
    (r'ingefær', 'ingefaer', U(spsk=6, tsk=2)),
    (r'honning', 'honning', U(spsk=21)),
    (r'peanutbutter|jordnøddesmør', 'smoer', U(spsk=16, faktor=0.9)),
    (r'sukker', 'sukker', U(spsk=12, tsk=4)),
    (r'ketchup', 'ketchup', U(spsk=17)),
    (r'sennep', 'sennep', U(spsk=15)),
    (r'remoulade', 'mayo', U(spsk=14, ml=0.9, faktor=0.55)),
    (r'mayonnaise', 'mayo', U(spsk=14, ml=0.9)),
    (r'soja', 'soja', U(spsk=16)),
]
REGLER = [(re.compile(r, re.I), n, o) for r, n, o in REGLER]

DEFAULT_ENHED = {'g': 1.0, 'kg': 1000.0, 'ml': 1.0, 'dl': 100.0, 'l': 1000.0, 'cl': 10.0}


def gram(navn, maengde, enhed, regel_omregning):
    """Antal gram for en ingrediens, eller None hvis enheden ikke kan omregnes."""
    o = regel_omregning
    if enhed in ('g', 'kg'):
        return maengde * DEFAULT_ENHED[enhed]
    if enhed in ('ml', 'dl', 'l', 'cl'):
        return maengde * DEFAULT_ENHED[enhed] * o.get('ml', 1.0)
    if enhed in o:
        return maengde * o[enhed]
    return None


def find_regel(navn):
    n = navn.lower()
    if IGNORER.search(n):
        return 'ignorer', None, None
    for rx, noegle, om in REGLER:
        if rx.search(n):
            return 'ok', noegle, om
    return 'ukendt', None, None
