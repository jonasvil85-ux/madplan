"""Bygger retter.json (det siden viser) ud fra scripts/retter_kilde.json + ugens tilbud.

Ugentlig rutine:
  1. python scripts/tilbud.py > tilbud.txt        (se ugens tilbud med id'er)
  2. Skriv/opdater scripts/retter_kilde.json      (20 retter pr. butik)
  3. python scripts/byg_retter.py                 (validerer og skriver retter.json)
  4. git commit + push  -> Vercel deployer automatisk
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tilbud import BUTIKKER, hent_tilbud  # noqa: E402

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FELTER = ['navn', 'maengde', 'enhed', 'basisvare', 'tilbud']


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    with open(os.path.join(ROD, 'scripts', 'retter_kilde.json'), encoding='utf-8') as f:
        kilde = json.load(f)
    data = hent_tilbud()
    alle = {t['kort']: t for t in data['tilbud']}
    fejl, ud = [], {}

    for butik, numre in kilde['butikker'].items():
        info = data['butikker'][butik]
        avis_ids = [a['id'] for a in info['aviser']]
        if kilde['aviser'][butik] not in avis_ids:
            fejl.append(f"{butik}: retter_kilde er lavet til avis {kilde['aviser'][butik]}, men aktuel avis er {avis_ids} - id'er passer ikke længere")
            continue
        prefix = BUTIKKER[butik]['prefix']
        retter, brugte = [], {}
        for nr in numre:
            r = kilde['retter'][nr - 1]
            ingredienser = []
            for ing in r['ingredienser']:
                d = dict(zip(FELTER, ing))
                d['basisvare'] = bool(d['basisvare'])
                for tid in d['tilbud']:
                    if tid not in alle:
                        fejl.append(f"{r['navn']}: ukendt tilbuds-id {tid}")
                d['tilbud'] = [t for t in d['tilbud'] if t.startswith(prefix) and t in alle]
                for t in d['tilbud']:
                    brugte[t] = alle[t]
                ingredienser.append(d)
            if not any(i['tilbud'] for i in ingredienser):
                fejl.append(f"{butik}: '{r['navn']}' har ingen tilbudsvarer i {info['navn']}")
            retter.append({**r, 'id': f"{butik}-{nr}", 'ingredienser': ingredienser})
        ud[butik] = {**info, 'retter': retter, 'tilbud': brugte}
        print(f"{info['navn']}: {len(retter)} retter, {len(brugte)} forskellige tilbudsvarer")

    if fejl:
        print('\nFEJL:\n- ' + '\n- '.join(fejl))
        sys.exit(1)

    from datetime import datetime, timezone
    with open(os.path.join(ROD, 'retter.json'), 'w', encoding='utf-8') as f:
        json.dump({'genereret': datetime.now(timezone.utc).isoformat(timespec='seconds'), 'butikker': ud},
                  f, ensure_ascii=False, indent=1)
    print('\nretter.json skrevet')


if __name__ == '__main__':
    main()
