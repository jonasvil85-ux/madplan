"""Henter ugens tilbud fra Tjek med samme korte id'er (N1, M1 …) som api/_tjek.js.

Brug:  python scripts/tilbud.py            -> skriver tilbudsliste til stdout (til at lave retter ud fra)
Bruges også af scripts/byg_retter.py.
"""
import json, re, sys, urllib.request
from datetime import datetime, timezone

API = 'https://squid-api.tjek.com/v2'
BUTIKKER = {
    'netto': {'navn': 'Netto', 'dealerId': '9ba51', 'prefix': 'N'},
    'meny':  {'navn': 'MENY',  'dealerId': '267e1m', 'prefix': 'M'},
}
IKKE_MAD = re.compile(r'nonfood|vin|spisetid|magasin', re.I)
ENHEDER = {'pcs': 'stk', 'g': 'g', 'kg': 'kg', 'ml': 'ml', 'cl': 'cl', 'l': 'l'}


def hent(url):
    req = urllib.request.Request(url, headers={'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def tid(s):
    return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S%z')


def fmt(v):
    return str(int(v)) if float(v).is_integer() else str(v)


def hent_butik(key):
    b = BUTIKKER[key]
    nu = datetime.now(timezone.utc)
    kat = [c for c in hent(f"{API}/catalogs?dealer_ids={b['dealerId']}&limit=24")
           if c['offer_count'] > 0 and not IKKE_MAD.search(c.get('label') or '') and tid(c['run_till']) >= nu]
    aviser = [c for c in kat if tid(c['run_from']) <= nu] or sorted(kat, key=lambda c: tid(c['run_from']))[:1]
    tilbud = []
    for avis in aviser:
        for offset in range(0, 1500, 100):
            side = hent(f"{API}/offers?catalog_id={avis['id']}&limit=100&offset={offset}")
            for o in side:
                q = o.get('quantity') or {}
                s = q.get('size') or {}
                sym = (q.get('unit') or {}).get('symbol')
                tilbud.append({
                    'id': o['id'], 'butik': key, 'navn': (o.get('heading') or '').strip(),
                    'beskrivelse': (o.get('description') or '').strip(),
                    'pris': (o.get('pricing') or {}).get('price'),
                    'forPris': (o.get('pricing') or {}).get('pre_price'),
                    'maengde': None if s.get('from') is None else (fmt(s['from']) if s['from'] == s['to'] else f"{fmt(s['from'])}-{fmt(s['to'])}"),
                    'enhed': ENHEDER.get(sym, sym),
                    'billede': (o.get('images') or {}).get('thumb'),
                    'gyldigTil': o.get('run_till'),
                })
            if len(side) < 100:
                break
    info = {'navn': b['navn'], 'aviser': [{'id': a['id'], 'navn': a['label'], 'fra': a['run_from'], 'til': a['run_till']} for a in aviser]}
    return info, tilbud


def hent_tilbud():
    butikker, tilbud = {}, []
    for k in BUTIKKER:
        info, t = hent_butik(k)
        butikker[k] = info
        tilbud += [{**x, 'kort': f"{BUTIKKER[k]['prefix']}{n + 1}"} for n, x in enumerate(t)]
    noegle = '-'.join(sorted(a['id'] for k in BUTIKKER for a in butikker[k]['aviser']))
    return {'noegle': noegle, 'butikker': butikker, 'tilbud': tilbud}


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    d = hent_tilbud()
    print('noegle:', d['noegle'])
    for t in d['tilbud']:
        besk = re.sub(r'\s*\n\s*', '; ', t['beskrivelse'])[:110]
        print(f"{t['kort']} | {t['navn']} | {t['pris']} kr | {t['maengde'] or ''} {t['enhed'] or ''} | {besk}")
