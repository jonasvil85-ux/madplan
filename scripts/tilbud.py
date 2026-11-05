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
# Kun den ugentlige madavis ("Uge 45", "Netto uge 45", "Lidl avis (uge 45)" …)
UGEAVIS = re.compile(r'uge\s*\d+', re.I)
IKKE_MAD = re.compile(r'nonfood|vin|søndag|magasin|katalog', re.I)
SNAPSHOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tilbud_snapshot.json')
ENHEDER = {'pcs': 'stk', 'g': 'g', 'kg': 'kg', 'ml': 'ml', 'cl': 'cl', 'l': 'l'}


def hent(url):
    req = urllib.request.Request(url, headers={'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def tid(s):
    return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S%z')


def fmt(v):
    return str(int(v)) if float(v).is_integer() else str(v)


def find_aviser_dealer(dealer_id):
    nu = datetime.now(timezone.utc)
    kat = [c for c in hent(f"{API}/catalogs?dealer_ids={dealer_id}&limit=24")
           if c['offer_count'] > 0 and UGEAVIS.search(c.get('label') or '')
           and not IKKE_MAD.search(c.get('label') or '') and tid(c['run_till']) >= nu]
    return [c for c in kat if tid(c['run_from']) <= nu] or sorted(kat, key=lambda c: tid(c['run_from']))[:1]


def find_aviser(key):
    """De ugeaviser der gælder nu for butikken (eller den næste der starter) – uden at hente selve tilbuddene."""
    b = BUTIKKER[key]
    nu = datetime.now(timezone.utc)
    kat = [c for c in hent(f"{API}/catalogs?dealer_ids={b['dealerId']}&limit=24")
           if c['offer_count'] > 0 and UGEAVIS.search(c.get('label') or '')
           and not IKKE_MAD.search(c.get('label') or '') and tid(c['run_till']) >= nu]
    # Foretræk avisen der gælder nu; ellers den næste der starter
    return [c for c in kat if tid(c['run_from']) <= nu] or sorted(kat, key=lambda c: tid(c['run_from']))[:1]


def hent_butik(key):
    b = BUTIKKER[key]
    aviser = find_aviser(key)
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
    info = {'navn': b['navn'], 'logo': dealer.get('logo'), 'logo2': logo2, 'farve': '#' + (dealer.get('color') or '10B981'), 'aviser': [{'id': a['id'], 'navn': a['label'], 'fra': a['run_from'], 'til': a['run_till']} for a in aviser]}
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
