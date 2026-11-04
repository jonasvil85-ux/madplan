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
    ud = {'genereret': datetime.datetime.now().astimezone().isoformat(timespec='seconds'), 'kategorier': kategorier}
    with open(UD, 'w', encoding='utf-8') as f:
        json.dump(ud, f, ensure_ascii=False, separators=(',', ':'))
    print(f'tilbudsliste.json skrevet: {len(kategorier)} kategorier')
    for k in kategorier:
        a = k['tilbud'][0]
        print(f"  {k['navn']:18} {len(k['tilbud'])} butikker, billigst {a['butik']:12} {a['pris']:g} kr  {a['navn'][:46]}")


if __name__ == '__main__':
    main()
