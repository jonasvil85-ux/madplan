"""Bygger tilbudsliste.json til "Gode tilbud i dine butikker" nederst på indkøbslisten.

Det er IKKE varer til aftensmaden (dem har madplanen allerede taget stilling til), men ting man ofte køber alligevel: sodavand, kaffe, smør, mælk, pålæg,
brød, vaskepulver, toiletpapir, shampoo, tandpasta, bleer, dyremad …
Pr. kategori gemmes hver butiks BILLIGSTE tilbud (med kr/kg, kr/l eller kr/stk, hvis den kan regnes). Siden vælger selv de bedste for brugerens butikker og
sammenligner tilbud med tilbud (ikke med en normalpris, som vi ikke kender).

Bruger scripts/tilbud_snapshot.json – kør scripts/tilbud.py først.

Brug:  python -I scripts/byg_tilbudsliste.py
"""
import datetime, json, os, re, sys

HER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HER)
from tilbud import laes_snapshot  # noqa: E402
from sammenlign import enhedspris  # noqa: E402

UD = os.path.join(os.path.dirname(HER), 'tilbudsliste.json')

# kategori: (regex der skal matche det FØRSTE produkt i tilbuddets navn, regex der udelukker (hele navnet), enhed for pris pr. enhed)
KATEGORIER = {
    'Sodavand':         (r'sodavand|coca-cola|cola zero|pepsi|faxe kondi|fanta|sprite|schweppes|nestea|ice tea|danskvand|mineralvand|squash|cult\b|mountain dew', r'julekalender|booster|energy|monster|capri|\bis\b|ice cream', 'l'),
    'Juice':            (r'juice|smoothie', r'shot|julekalender', 'l'),
    'Kaffe':            (r'kaffe|merrild|gevalia|bki|lavazza|café noir', r'kapsl|filter|instant|nescafé|dolce|kop\b|mælk', 'kg'),
    'Smør':             (r'\bsmør\b|kærgården|lurpak', r'smørrebrød|pålæg|flydende|naturli|becel|cookies', 'kg'),
    'Mælk':             (r'mælk\b|letmælk|minimælk|sødmælk|kærnemælk', r'kokos|chokolade|kakao|mælkeris|shake|cocio|karamel|jordbær|vanilje|mælkechokolade', 'l'),
    'Yoghurt og skyr':  (r'yoghurt|skyr|tykmælk|kefir', r'is\b|dessert|müsli', 'kg'),
    'Ost':              (r'skæreost|riberhus|danbo|havarti|mammen|klovborg|cheddar|emmentaler|cheasy (skæreost|ost)', r'burger|boost|hakket|smelte|yoghurt|skyr', 'kg'),
    'Pålæg':            (r'leverpostej|rullepølse|hamburgerryg|spegepølse|salami|pålæg|kyllingepålæg', r'chokolade|rullepølsekrydderi', 'kg'),
    'Brød':             (r'rugbrød|franskbrød|toastbrød|knækbrød|schulstad|det gode brød|wasa|rundstykker', r'kiks|oreo|julekage', 'kg'),
    'Morgenmad':        (r'havregryn|müsli|cornflakes|granola|morgenmad|cheerios', r'bar\b|barer|yoghurt|skyr', 'kg'),
    'Chips og snacks':  (r'chips|popcorn|peanuts|saltstænger|nødder', r'julekalender', 'kg'),
    'Vaskemiddel':      (r'vaskepulver|vaskemiddel|skyllemiddel|\bomo\b|ariel|persil|\bvia\b|bamseline', r'opvask', 'stk'),
    'Opvask':           (r'opvasketabs|opvaskemiddel|fairy|finish|maskinopvask', r'capri', 'stk'),
    'Toiletpapir':      (r'toiletpapir|lotus|lambi|serla|køkkenrulle', r'holder|børste|rensebørste', 'stk'),
    'Rengøring':        (r'cillit|ajax|allrent|rengøring|glasrens|toiletrens|\bvim\b|mr muscle', r'artikler', 'stk'),
    'Shampoo':          (r'shampoo|balsam|conditioner|head & shoulders|pantene|elvital', r'hundeshampoo', 'stk'),
    'Tandpleje':        (r'tandpasta|mundskyl|zendium|colgate|oral-b|tandbørste|tandtråd|tandcreme', r'', 'stk'),
    'Sæbe og deodorant': (r'håndsæbe|showergel|shower gel|deodorant|\bdeo\b|nivea|dove', r'solcreme', 'stk'),
    'Bleer':            (r'bleer|libero|pampers|vådservietter', r'', 'stk'),
    'Dyremad':          (r'kattemad|hundemad|whiskas|pedigree|frolic|dreamies|perfect fit|kattegrus|hundesnacks', r'', 'kg'),
}


# ---- Fire grupper til indkøbslisten: weekenden, madpakken, morgenmad og frokost (hver vare i højst én gruppe) ----
# (gruppe, underkategori, regex på tilbuddets navn). Første match vinder, så en vare aldrig står i to grupper. Alkohol og ikke-mad udelukkes.
ALKOHOL = re.compile(r'(?<![a-zæøå])(vin|rødvin|hvidvin|rosé|øl|pilsner|cider|vodka|gin|whisky|rom|likør|baileys|aquavit|bitter|spiritus|champagne|prosecco|gløgg|hvidtøl|julebryg|påskebryg)(?![a-zæøå])|'
                     r'heineken|carlsberg|tuborg classic|royal export|jacobsen|grimbergen|1664|cuvée|shiraz|chardonnay|riesling|appassi|moscato|zinfandel|sauvignon|ripasso|merlot|gammel dansk|underberg|beefeater|absolut|ballantine|captain morgan|o\.p\. anderson|sælges kun i hele rammer|aus\b|today.s special|tendida', re.I)
IKKE_MAD_LISTE = re.compile(r'vask|toilet|køkkenrulle|opvask|duracell|batteri|lyskæde|bloklys|fyrfadslys|stearin|kalenderlys|\bled\b|tena\b|libresse|bleer|tandpasta|colgate|shampoo|hundemad|kattemad|sheba|cesar|'
                         r'julekalender|nivea|deodorant|energi|red bull|monster|ikke egnet til børn|biotex|ajax|klorin|fairy|libero|dun-let|kaffemaskine|gave|legetøj|naturli|lactofree|laktosefri|pizzadej|dejli', re.I)
GRUPPER = [
    ('weekend', 'Slik', r'slik|haribo|lakrids|vingummi|bolsjer|skumfidus|mentos|snebolde|julepose|spangsberg|nørregade|(?<![a-zæøå])toms|marabou|ritter sport|kinder|guldæske|anthon berg|konfekt|marcipan|karamel|bland selv|fazer|cloetta|chokolade(?!mælk)'),
    ('weekend', 'Sodavand', r'sodavand|cola|pepsi|fanta|sprite|faxe kondi|schweppes|tuborg squash|ramlösa|fuze|mirinda|ribena|saftevand|ice tea|nestea|limonade|(?<![a-zæøå])squash|fun eller scoop'),
    ('weekend', 'Chips og snacks', r'chips|snacks(?! pot)|popcorn|peanuts|saltstænger|(?<![a-zæøå])nødder|nachos|ostepops|kims|tortilla chips'),
    ('weekend', 'Is og kager', r'(?<![a-zæøå])is(?![a-zæøå])|ice cream|magnum|ben & jerry|hansens|risalamande|dessert|budding|kage(?![a-zæøå])|kager|cookies|kiks|småkager|donuts|muffin|æbleskiver|wienerbrød|brownie'),
    ('madpakke', 'Pålæg', r'pålæg|leverpostej|rullepølse|hamburgerryg|spegepølse|salami|skinke(?!steg)|postej|k-salat|pålægssalat|pålægschokolade|kødpølse|kalkunbacon|den grønne slagter'),
    ('madpakke', 'Brød', r'rugbrød|franskbrød|toastbrød|(?<![a-zæøå])brød(?![a-zæøå])|boller|rundstykker|knækbrød|wasa|baguette|pitabrød|hvedebrød|levain|limpan|schulstad|pågen|kohberg'),
    ('madpakke', 'Ost', r'skiveost|skæreost|smørbar|danbo|havarti|castello|philadelphia|klovborg|cheasy|mammen|riberhus|osteskiver|flødeost|first price skiveost'),
    ('madpakke', 'Frugt og drikke', r'æble|banan|appelsin|clementin|mandarin|druer|pærer|kiwi|blåbær|figner|rosiner|juice|smoothie|kakaomælk|cocio|matilde|müslibar|corny|granolabar'),
    ('morgenmad', 'Morgenmad', r'havregryn|müsli|granola|cornflakes|cheerios|grød|(?<![a-zæøå])havre|morgenmad|rice krispies|crunchy|kellogg'),
    ('morgenmad', 'Mejeri', r'yoghurt|skyr|ymer|(?<![a-zæøå])mælk|letmælk|minimælk|kærnemælk|tykmælk|kefir|hytteost|cultura|yoggi|a38'),
    ('morgenmad', 'Smør og smørepålæg', r'(?<![a-zæøå])smør(?![a-zæøå])|lurpak|kærgården|marmelade|syltetøj|honning|nutella|nougat|peanutbutter|nøddesmør'),
    ('morgenmad', 'Kaffe og te', r'kaffe|nescafé|(?<![a-zæøå])bki|karat|merrild|gevalia|lavazza|(?<![a-zæøå])te(?![a-zæøå])|pickwick|lipton'),
    ('morgenmad', 'Æg', r'(?<![a-zæøå])æg(?![a-zæøå])|frilandsæg|skrabeæg'),
    ('frokost', 'Suppe', r'suppe'),
    ('frokost', 'Hurtig frokost', r'nudler|snack pot|noodles|spaghetteria|middagsret|færdigret|knorr retter|steff houlberg maxi|indbagt|tarteletter|wraps|sandwich|bagel|pizza|ristorante|tærte|quiche'),
    ('frokost', 'Fisk og salat', r'(?<![a-zæøå])tun(?![a-zæøå])|makrel|sild|rejesalat|hønsesalat|salat(?![a-zæøå])|dressing|mayonnaise|remoulade'),
]
TITLER = {'weekend': 'Weekenden', 'madpakke': 'Madpakken', 'morgenmad': 'Morgenmad', 'frokost': 'Frokost'}


def noegle(navn):
    """Samme vare i flere butikker får samme nøgle (ordene i det første produkt, sorteret)."""
    forste = re.split(r',| eller | og ', navn)[0].lower()
    return ' '.join(sorted(set(re.findall(r'[a-zæøå]{3,}', forste))))


def byg_grupper(data):
    grupper = {g: [] for g in TITLER}
    pr_butik = {}
    for t in sorted(data['tilbud'], key=lambda x: x['pris'] or 0):
        if not t.get('pris') or ALKOHOL.search(t['navn']) or IKKE_MAD_LISTE.search(t['navn']):
            continue
        for g, under, mønster in GRUPPER:
            if re.search(mønster, t['navn'], re.I):
                n = pr_butik[(t['butik'], g)] = pr_butik.get((t['butik'], g), 0) + 1
                if n <= 30:
                    grupper[g].append({'butik': t['butik'], 'kort': t['kort'], 'navn': t['navn'], 'pris': t['pris'], 'forPris': t.get('forPris'), 'maengde': t.get('maengde'),
                                       'enhed': t.get('enhed'), 'billede': t.get('billede'), 'gyldigTil': t.get('gyldigTil'), 'under': under, 'noegle': noegle(t['navn']),
                                       'note': (re.search(r'pr\. (100 g|kg|stk|liter|l)', t.get('beskrivelse') or '', re.I) or [None])[0]})
                break  # højst én gruppe pr. vare
    return grupper


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    data = laes_snapshot()
    kategorier = []
    for kat, (med, uden, enhed) in KATEGORIER.items():
        bedst = {}
        for t in data['tilbud']:
            if not t.get('pris') or not t.get('billede'):
                continue
            forste = re.split(r',| eller | og ', t['navn'])[0]
            if not re.search(med, forste, re.I) or (uden and re.search(uden, t['navn'], re.I)):
                continue
            ep = enhedspris(t, enhed)
            # billigste pr. enhed hvis den kan regnes, ellers billigste pris
            noegle = (0, ep) if ep else (1, t['pris'])
            if t['butik'] not in bedst or noegle < bedst[t['butik']][0]:
                bedst[t['butik']] = (noegle, ep, t)
        if not bedst:
            continue
        kategorier.append({
            'navn': kat, 'enhed': enhed,
            'tilbud': [{'butik': t['butik'], 'kort': t['kort'], 'navn': t['navn'], 'pris': t['pris'], 'forPris': t.get('forPris'), 'maengde': t.get('maengde'),
                        'enhed': t.get('enhed'), 'ep': round(ep, 2) if ep else None, 'billede': t.get('billede'), 'gyldigTil': t.get('gyldigTil')}
                       for _, ep, t in sorted(bedst.values(), key=lambda x: x[0])],
        })
    grupper = byg_grupper(data)
    ud = {'genereret': datetime.datetime.now().astimezone().isoformat(timespec='seconds'), 'kategorier': kategorier, 'grupper': grupper}
    with open(UD, 'w', encoding='utf-8') as f:
        json.dump(ud, f, ensure_ascii=False, separators=(',', ':'))
    print(f'tilbudsliste.json skrevet: {len(kategorier)} kategorier og grupperne ' + ', '.join(f'{TITLER[g]} {len(v)}' for g, v in grupper.items()))
    for k in kategorier:
        a = k['tilbud'][0]
        print(f"  {k['navn']:18} {len(k['tilbud'])} butikker, billigst {a['butik']:12} {a['pris']:g} kr  {a['navn'][:46]}")


if __name__ == '__main__':
    main()
