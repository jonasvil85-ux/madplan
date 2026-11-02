"""Bygger retter.json (det siden viser) ud fra scripts/retter_kilde.json + ugens tilbud.

Ugentlig rutine:
  1. python -I scripts/tilbud.py > tilbud.txt     (se ugens tilbud med id'er)
  2. Skriv scripts/retter_kilde.json              (20 retter pr. avis, kun den avis' tilbuds-id'er)
  3. python -I scripts/byg_retter.py              (validerer og skriver retter.json)
  4. git commit + push  -> Vercel deployer automatisk
"""
import json, math, os, re, sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tilbud import BUTIKKER, SNAPSHOT  # noqa: E402

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FELTER = ['navn', 'maengde', 'enhed', 'basisvare', 'tilbud']
NIVEAUER = {'student', 'familie', 'weekend'}
# Retterne skal være hjemmelavede: ingen færdigretter, færdigtilbehør eller færdige saucer/deje
FORARBEJDET = re.compile(r'flødekartofler|herregårds|kødboller|melboller|panering|eriks sauce|færdigret|middagsret|'
                         r'dinner kit|pizzadej|pesto|pastasauce|kopsuppe|snackpot|ristorante|rustica|surdejspizza|'
                         r'italiensk pizza|æbleskiver|kyllingemarked|kebab|confit|smørrebrød|menu|mortensaften', re.I)
OMREGN = {'g': ('g', 1), 'kg': ('g', 1000), 'ml': ('ml', 1), 'cl': ('ml', 10), 'l': ('ml', 1000), 'stk': ('stk', 1)}


def antal_pakker(t, behov):
    """Samme logik som antalPakker() i index.html."""
    try:
        stoerrelse = float(str(t.get('maengde') or '').split('-')[0])
    except ValueError:
        stoerrelse = 0
    enhed, gange = OMREGN.get(t.get('enhed'), (None, None))
    n = math.ceil(behov.get('dåse', 0) + behov.get('pakke', 0))
    if stoerrelse and enhed and behov.get(enhed):
        n = max(n, math.ceil(behov[enhed] / (stoerrelse * gange) - 1e-9))
    return max(1, n)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    with open(os.path.join(ROD, 'scripts', 'retter_kilde.json'), encoding='utf-8') as f:
        kilde = json.load(f)
    # Brug det gemte øjebliksbillede – Tjeks rækkefølge (og dermed id'erne) skifter mellem kald
    with open(SNAPSHOT, encoding='utf-8') as f:
        data = json.load(f)
    alle = {t['kort']: t for t in data['tilbud']}
    fejl, ud = [], {}

    for butik, b in BUTIKKER.items():
        info = data['butikker'][butik]
        avis_ids = [a['id'] for a in info['aviser']]
        if kilde['aviser'][butik] not in avis_ids:
            fejl.append(f"{butik}: retter_kilde er lavet til avis {kilde['aviser'][butik]}, men aktuel avis er {avis_ids}")
            continue
        retter, brugte, navne = [], {}, set()
        for nr, r in enumerate(kilde[butik], 1):
            if r['niveau'] not in NIVEAUER:
                fejl.append(f"{r['navn']}: ukendt niveau {r['niveau']}")
            if r['navn'] in navne:
                fejl.append(f"{butik}: '{r['navn']}' findes to gange")
            navne.add(r['navn'])
            ingredienser, behov = [], {}
            for ing in r['ingredienser']:
                d = dict(zip(FELTER, ing))
                d['basisvare'] = bool(d['basisvare'])
                for tid in d['tilbud']:
                    if not tid.startswith(b['prefix']) or tid not in alle:
                        fejl.append(f"{butik}: '{r['navn']}' bruger ugyldigt tilbuds-id {tid}")
                d['tilbud'] = [t for t in d['tilbud'] if t.startswith(b['prefix']) and t in alle]
                for t in d['tilbud']:
                    if FORARBEJDET.search(alle[t]['navn']):
                        fejl.append(f"{butik}: '{r['navn']}' bruger færdigvare {t} ({alle[t]['navn'][:40]})")
                if d['tilbud']:
                    t = d['tilbud'][0]
                    brugte[t] = alle[t]
                    behov.setdefault(t, {})
                    behov[t][d['enhed']] = behov[t].get(d['enhed'], 0) + d['maengde']
                ingredienser.append(d)
            pris = sum(alle[t]['pris'] * antal_pakker(alle[t], bh) for t, bh in behov.items())
            ikke_basis = [i for i in ingredienser if not i['basisvare']]
            andel = sum(1 for i in ikke_basis if i['tilbud']) / max(1, len(ikke_basis))
            if not behov:
                fejl.append(f"{butik}: '{r['navn']}' har ingen tilbudsvarer")
            retter.append({**r, 'id': f'{butik}-{nr}', 'ingredienser': ingredienser,
                           'pris_tilbud': round(pris, 2), 'andel_tilbud': round(andel, 2)})
        ud[butik] = {**info, 'retter': retter, 'tilbud': brugte}

        print(f"\n{info['navn']}: {len(retter)} retter, {len(brugte)} forskellige tilbudsvarer")
        for niv in ('student', 'familie', 'weekend'):
            rr = [r for r in retter if r['niveau'] == niv]
            print(f"  {niv:8} {len(rr):2} retter")
            for r in rr:
                print(f"    {r['pris_tilbud']:7.2f} kr  {round(r['andel_tilbud'] * 100):3d}% tilbud  {r['navn']}")

    if fejl:
        print('\nFEJL:\n- ' + '\n- '.join(fejl))
        sys.exit(1)

    with open(os.path.join(ROD, 'retter.json'), 'w', encoding='utf-8') as f:
        json.dump({'genereret': datetime.now(timezone.utc).isoformat(timespec='seconds'), 'butikker': ud},
                  f, ensure_ascii=False, indent=1)
    print('\nretter.json skrevet')


if __name__ == '__main__':
    main()
