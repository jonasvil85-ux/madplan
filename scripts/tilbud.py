"""Henter ugens tilbudsaviser fra Tjek og giver tilbuddene korte id'er (N1, M1, B1 …).

Brug:
  python -I scripts/tilbud.py bilka rema > tilbud.txt   (kun de nævnte butikker – fx dem med ny avis)
  python -I scripts/tilbud.py alle > tilbud.txt          (alle butikker)

  - opdaterer scripts/tilbud_snapshot.json for de nævnte butikker (de andre røres ikke)
  - skriver tilbudslisten for de nævnte butikker til stdout (til at skrive retter ud fra)

Tjek leverer ikke tilbuddene i fast rækkefølge, så id'erne gælder KUN for det gemte
øjebliksbillede. Hent derfor ikke en butik igen mellem at dens retter skrives og bygges.
"""
import json, os, re, sys, urllib.request
from datetime import datetime, timezone

API = 'https://squid-api.tjek.com/v2'
BUTIKKER = {
    'netto':        {'navn': 'Netto',        'dealerId': '9ba51',  'prefix': 'N'},
    'meny':         {'navn': 'MENY',         'dealerId': '267e1m', 'prefix': 'M'},
    'bilka':        {'navn': 'Bilka',        'dealerId': '93f13',  'prefix': 'B'},
    'rema':         {'navn': 'REMA 1000',    'dealerId': '11deC',  'prefix': 'R'},
    # Kvickly og SuperBrugsen (Coop) har næsten samme avis: én samlet butik med de tilbud, der gælder begge steder (samme tekst og pris)
    'kvickly':      {'navn': 'Kvickly / SuperBrugsen', 'dealerId': 'c1edq', 'prefix': 'K', 'sammen_med': '0b1e8'},
    'lidl':         {'navn': 'Lidl',         'dealerId': '71c90',  'prefix': 'L'},
    '365':          {'navn': '365discount',  'dealerId': 'DWZE1w', 'prefix': 'D'},
    'spar':         {'navn': 'SPAR',         'dealerId': '88ddE',  'prefix': 'P'},
    'minkoebmand':  {'navn': 'Min Købmand',  'dealerId': '603dfL', 'prefix': 'X'},
}
# Aviser med mad: ugeavisen ("Uge 46", "Netto AU46", "Lidl avis (uge 46)" …) PLUS alle andre aviser, der indeholder mad (fx Lidls "Fast lav pris i Lidl" og Bilkas "Salling Princip").
# Ugeavisen kendes på et ugenummer (1-53) i navnet – uanset præfiks. Årstal (2026) passerer ikke.
UGEAVIS = re.compile(r'(?<!\d)(?:[1-9]|[1-4]\d|5[0-3])(?!\d)')


def er_ugeavis(label):
    """Butikkens ugeavis – den, retterne skrives efter. Lidls "Weekendavis (uge 46)" har et ugenummer, men er et uddrag af ugeavisen, ikke en ny avis."""
    return bool(UGEAVIS.search(label or '')) and not re.search(r'weekend', label or '', re.I)


def _norm(navn):
    return re.sub(r'[^a-z0-9æøå]', '', navn.lower())


def _ord(navn):
    return set(re.findall(r'[a-z0-9æøå]+', navn.lower()))


def _grundmaengde(m, e):
    """Mængden i grundenhed (g, ml eller stk), så 0,5 kg og 500 g er ens – None hvis ukendt."""
    if m is None or e is None:
        return None
    try:
        v = float(str(m).split('-')[0])
    except ValueError:
        return None
    faktor = {'kg': 1000, 'g': 1, 'l': 1000, 'cl': 10, 'ml': 1, 'stk': 1}.get(e)
    if faktor is None:
        return None
    return (v * faktor, 'g' if e in ('kg', 'g') else 'ml' if e in ('l', 'cl', 'ml') else 'stk')


def samme_tilbud(a, b):
    """Er det den samme vare i to af butikkens aviser? Samme pris og samme navn (med eller uden mærke, bindestreg og mellemrum) og samme
    mængde i grundenhed. Er navnet ordret ens og prisen ens, er det samme vare, selv om mængden er tastet forskelligt i de to aviser
    (Lidls weekendavis gentager ugeavisen med den slags småforskelle: 'SILVERCREST Gryder' / 'Gryder', '0.5 kg' / '500 g')."""
    if a['pris'] != b['pris']:
        return False
    if _norm(a['navn']) == _norm(b['navn']):
        return True
    oa, ob = _ord(a['navn']), _ord(b['navn'])
    if not oa or not ob or not (oa <= ob or ob <= oa):
        return False
    ga, gb = _grundmaengde(a['maengde'], a['enhed']), _grundmaengde(b['maengde'], b['enhed'])
    return ga is None or gb is None or ga == gb
# Aviser, der aldrig er mad: nonfood, vin/alkohol, magasiner, kataloger, legetøj, gaver, elektronik, menuer – og Premium, som kun gentager tilbud fra hovedavisen
IKKE_MAD = re.compile(r'nonfood|(?<![a-zæøå])vin(?![a-zæøå])|vinkatalog|søndag|magasin|katalog|premium|trend|gave|indstik|legetøj|beauty|prosonic|elektronik|ud af huset|madskole|opskrift|princip', re.I)  # Salling Princip er en produktkatalog med almindelige priser, ikke tilbud
# En avis, der ikke er en ugeavis, skal mindst have denne andel mad i sine tilbud (de første 100 tjekkes), før den tages med
MADORD = re.compile(
    r'kød|kylling|okse|gris|svin|flæsk|bacon|pølse|medister|skinke|laks|fisk|rejer|sild|torsk|ørred|\bost\b|ost\b|mælk|yoghurt|skyr|fløde|smør|\bæg\b|brød|rundstykk|bolle|pasta|spaghetti|ris\b|nudler|mel\b|sukker|'
    r'kaffe|juice|saft|sodavand|cola|chips|slik|chokolade|kiks|kage|pizza|suppe|sauce|ketchup|sennep|mayo|olie|eddike|grønt|frugt|æble|appelsin|banan|kartof|løg|gulerod|tomat|agurk|salat|avocado|bønner|'
    r'nødder|mandler|müsli|havre|marmelade|honning|pålæg|and\b|confit|pancetta|guanciale|parmigiano|salsiccia|grød|dej|tærte|burger|wrap|pita|sirup|dadler|figner|asparges|pommes|is\b', re.I)
MIN_MADANDEL = 0.35
_MADAVIS = {}  # katalog-id -> er mad (så en avis kun tjekkes én gang pr. kørsel)


def er_madavis(c):
    """Ugeaviser tages altid med; andre aviser kun hvis navnet ikke afslører nonfood, og de mindst MIN_MADANDEL af tilbuddene ligner mad."""
    label = c.get('label') or ''
    if IKKE_MAD.search(label):
        return False
    if UGEAVIS.search(label):
        return True
    if c['id'] not in _MADAVIS:
        side = hent(f"{API}/offers?catalog_id={c['id']}&limit=100")
        mad = sum(1 for o in side if MADORD.search(o.get('heading') or ''))
        _MADAVIS[c['id']] = bool(side) and mad / len(side) >= MIN_MADANDEL
    return _MADAVIS[c['id']]


SNAPSHOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tilbud_snapshot.json')
ENHEDER = {'pcs': 'stk', 'g': 'g', 'kg': 'kg', 'ml': 'ml', 'cl': 'cl', 'l': 'l'}


def hent(url):
    # Tjek afviser kald uden User-Agent (401 siden 12/11-2026); vi identificerer os ærligt som siden
    req = urllib.request.Request(url, headers={'Accept': 'application/json', 'User-Agent': 'Maaltidsjagten/1.0 (+https://xn--mltidsjagten-tcb.dk)'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def tid(s):
    return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S%z')


def fmt(v):
    return str(int(v)) if float(v).is_integer() else str(v)


def find_aviser_dealer(dealer_id):
    """De aviser med mad, der gælder nu for en kæde – eller den næste ugeavis, der starter, hvis ingen gælder endnu."""
    nu = datetime.now(timezone.utc)
    kat = [c for c in hent(f"{API}/catalogs?dealer_ids={dealer_id}&limit=48")
           if c['offer_count'] > 0 and tid(c['run_till']) >= nu and er_madavis(c)]
    gaelder = [c for c in kat if tid(c['run_from']) <= nu]
    return gaelder or sorted(kat, key=lambda c: tid(c['run_from']))[:1]


def find_aviser(key):
    """De aviser med mad, der gælder nu for butikken (ugeavisen og evt. faste madaviser) – uden at hente selve tilbuddene."""
    return find_aviser_dealer(BUTIKKER[key]['dealerId'])


def hent_butik(key):
    b = BUTIKKER[key]
    aviser = sorted(find_aviser(key), key=lambda a: not er_ugeavis(a['label']))  # ugeavisen først, så dens navne og mængder vinder ved dubletter
    tilbud = []
    for avis in aviser:
        for offset in range(0, 1500, 100):
            side = hent(f"{API}/offers?catalog_id={avis['id']}&limit=100&offset={offset}")
            for o in side:
                q = o.get('quantity') or {}
                s = q.get('size') or {}
                sym = (q.get('unit') or {}).get('symbol')
                tilbud.append({
                    'id': o['id'], 'side': o.get('catalog_page') or 0, 'butik': key, 'navn': (o.get('heading') or '').strip(),
                    'beskrivelse': (o.get('description') or '').strip(),
                    'pris': (o.get('pricing') or {}).get('price'),
                    'forPris': (o.get('pricing') or {}).get('pre_price'),
                    'stk': ((q.get('pieces') or {}).get('from') or 1),  # antal i pakken (fx 20 dåser i en ramme)
                    'maengde': None if s.get('from') is None else (fmt(s['from']) if s['from'] == s['to'] else f"{fmt(s['from'])}-{fmt(s['to'])}"),
                    'enhed': ENHEDER.get(sym, sym),
                    'billede': (o.get('images') or {}).get('thumb'),
                    'gyldigTil': o.get('run_till'),
                })
            if len(side) < 100:
                break
    unikke = []  # samme vare til samme pris i flere aviser (fx ugeavis, weekendavis og fast-lav-pris-avis) vises kun én gang – se samme_tilbud
    for t in tilbud:
        if not any(samme_tilbud(t, u) for u in unikke):
            unikke.append(t)
    if len(unikke) != len(tilbud):
        print(f"{b['navn']}: {len(tilbud) - len(unikke)} dubletter mellem aviserne fjernet", file=sys.stderr)
    tilbud = unikke
    if b.get('sammen_med'):  # behold kun tilbud, der også findes (samme tekst og pris) i den anden kædes avis
        andre = set()
        for avis in find_aviser_dealer(b['sammen_med']):
            for offset in range(0, 1500, 100):
                side = hent(f"{API}/offers?catalog_id={avis['id']}&limit=100&offset={offset}")
                andre |= {((o.get('heading') or '').strip().lower(), (o.get('pricing') or {}).get('price')) for o in side}
                if len(side) < 100:
                    break
        faelles = [t for t in tilbud if (t['navn'].lower(), t['pris']) in andre]
        if andre and len(faelles) >= 0.5 * len(tilbud):
            print(f"{b['navn']}: {len(faelles)} af {len(tilbud)} tilbud gælder begge kæder", file=sys.stderr)
            tilbud = faelles
        else:
            print(f"ADVARSEL {b['navn']}: den anden kædes avis passer ikke (fælles {len(faelles)} af {len(tilbud)}) – bruger alle tilbud", file=sys.stderr)
    tilbud.sort(key=lambda t: (t['side'], t['navn'], t['id']))  # så stabilt som muligt
    tilbud = [{**t, 'kort': f"{b['prefix']}{n + 1}"} for n, t in enumerate(tilbud)]
    dealer = hent(f"{API}/dealers/{b['dealerId']}")
    logo2 = hent(f"{API}/dealers/{b['sammen_med']}").get('logo') if b.get('sammen_med') else None
    info = {'navn': b['navn'], 'logo': dealer.get('logo'), 'logo2': logo2, 'farve': '#' + (dealer.get('color') or '10B981'), 'aviser': [{'fast': not er_ugeavis(a['label']), 'id': a['id'], 'navn': a['label'], 'fra': a['run_from'], 'til': a['run_till']} for a in aviser]}
    return info, tilbud


def laes_snapshot():
    if os.path.exists(SNAPSHOT):
        with open(SNAPSHOT, encoding='utf-8') as f:
            return json.load(f)
    return {'butikker': {}, 'tilbud': []}


def opdater_snapshot(keys):
    """Henter de nævnte butikker og erstatter kun dem i øjebliksbilledet."""
    d = laes_snapshot()
    for k in keys:
        info, t = hent_butik(k)
        d['butikker'][k] = info
        d['tilbud'] = [x for x in d['tilbud'] if x['butik'] != k] + t
    d.pop('noegle', None)
    with open(SNAPSHOT, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    return d


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    valgt = sys.argv[1:] or ['alle']
    keys = list(BUTIKKER) if valgt == ['alle'] else valgt
    ukendte = [k for k in keys if k not in BUTIKKER]
    if ukendte:
        sys.exit(f"Ukendt butik: {ukendte}. Vælg blandt: {', '.join(BUTIKKER)} eller 'alle'")
    d = opdater_snapshot(keys)
    for k in keys:
        info = d['butikker'][k]
        print(f"\n## {info['navn']} – " + ', '.join(f"{a['navn']} ({a['id']}, {a['fra'][:10]}–{a['til'][:10]})" for a in info['aviser']))
        for t in d['tilbud']:
            if t['butik'] == k:
                besk = re.sub(r'\s*\n\s*', '; ', t['beskrivelse'])[:90]
                print(f"{t['kort']} | {t['navn'][:70]} | {t['pris']} kr | {t['maengde'] or ''} {t['enhed'] or ''} | {besk}")
