"""Kopierer en butiks retter til en anden butik med samme tilbudsavis (fx Kvickly -> SuperBrugsen).

Tilbuds-id'erne oversættes ved at matche varerne på navn, pris og mængde i øjebliksbilledet.

Brug:  python -I scripts/kopier_retter.py kvickly superbrugsen
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tilbud import BUTIKKER, laes_snapshot  # noqa: E402

RETTER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'retter')


def main(fra, til):
    sys.stdout.reconfigure(encoding='utf-8')
    data = laes_snapshot()
    noegle = lambda t: (t['navn'].lower(), t['pris'], t['maengde'], t['enhed'])
    fra_tilbud = {t['kort']: t for t in data['tilbud'] if t['butik'] == fra}
    til_efter_noegle = {noegle(t): t['kort'] for t in data['tilbud'] if t['butik'] == til}
    # Navne sammenlignes uden mellemrum/tegn, så "kyllinge lårfilet" = "kyllingelårfilet"
    norm = lambda s: re.sub(r'[^a-zæøå0-9]', '', s.lower())
    til_efter_navn = {norm(t['navn']): t['kort'] for t in data['tilbud'] if t['butik'] == til}

    def oversaet(kort):
        t = fra_tilbud[kort]
        return til_efter_noegle.get(noegle(t)) or til_efter_navn.get(norm(t['navn']))

    with open(os.path.join(RETTER, f'{fra}.json'), encoding='utf-8') as f:
        tekst = f.read()
    mangler = set()

    def erstat(m):
        ny = oversaet(m.group(1))
        if not ny:
            mangler.add(f"{m.group(1)} ({fra_tilbud[m.group(1)]['navn']})")
            return '"__MANGLER__"'
        return f'"{ny}"'

    prefix = re.escape(BUTIKKER[fra]['prefix'])
    tekst = re.sub(rf'"({prefix}\d+)"', erstat, tekst)
    d = json.loads(tekst)
    d['avis'] = data['butikker'][til]['aviser'][0]['id']
    # Fjern id'er der ikke kunne oversættes (ingrediensen bliver så til normalpris; top 5-linjen udgår)
    def rens(x):
        if isinstance(x, list):
            return [rens(v) for v in x if v != '__MANGLER__' and not (isinstance(v, dict) and v.get('id') == '__MANGLER__')]
        if isinstance(x, dict):
            return {k: rens(v) for k, v in x.items()}
        return x
    tekst = json.dumps(rens(d), ensure_ascii=False, indent=2)
    with open(os.path.join(RETTER, f'{til}.json'), 'w', encoding='utf-8') as f:
        f.write(tekst + '\n')
    print(f"Skrev scripts/retter/{til}.json fra {fra}.json")
    if mangler:
        print('Kunne ikke oversætte (bliver normalpris):\n- ' + '\n- '.join(sorted(mangler)))


if __name__ == '__main__':
    main(*sys.argv[1:3])
