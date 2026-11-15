"""Regressionstest af pris, indkøbsliste og ugeforslag.

Kører sidens egen JavaScript i node (regression.js, uden browser og uden net) på en GEMT kopi af data
(scripts/tests/fixtur/*.json.gz) og sammenligner med facitlisten (scripts/tests/facit.json).
Data ændrer sig hver dag; fixturen gør, at testen kun fanger ændringer i KODEN (prisregler, pakker, ugeforslag, indkøbsliste).

  python -I scripts/tests/regression.py                  kør og sammenlign (exit 1 ved forskel)
  python -I scripts/tests/regression.py --opdater-facit  gem nyt facit (når en ændring er tilsigtet)
  python -I scripts/tests/regression.py --opdater-fixtur tag nyt udsnit af de rigtige datafiler og gem nyt facit
"""
import gzip, json, os, shutil, subprocess, sys, time

ROD = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
TEST = os.path.join(ROD, 'scripts', 'tests')
FACIT = os.path.join(TEST, 'facit.json')
FIXTUR = os.path.join(TEST, 'fixtur')
DATA = ['retter', 'opskrifter', 'tilbudsliste', 'naering']


def regn():
    node = shutil.which('node')
    if not node:
        return None, 'node findes ikke her'
    p = subprocess.run([node, os.path.join(TEST, 'regression.js'), ROD, FIXTUR], capture_output=True, text=True, encoding='utf-8', timeout=300)
    if p.returncode:
        return None, 'regression.js fejlede: ' + (p.stderr.strip().splitlines() or ['?'])[-1][:300]
    return json.loads(p.stdout), None


def forskelle(a, b, sti=''):
    """Liste af (sti, facit, nu)."""
    ud = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            ud += forskelle(a.get(k, '<mangler>'), b.get(k, '<mangler>'), f'{sti}/{k}')
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            ud += forskelle(x, y, f'{sti}[{i}]')
    elif a != b:
        ud.append((sti, a, b))
    return ud


def gem_json(sti, obj):
    with open(sti, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write('\n')


def main(args):
    if '--opdater-fixtur' in args:
        os.makedirs(FIXTUR, exist_ok=True)
        for n in DATA:
            with open(os.path.join(ROD, n + '.json'), 'rb') as f, open(os.path.join(FIXTUR, n + '.json.gz'), 'wb') as raw:
                with gzip.GzipFile(fileobj=raw, mode='wb', compresslevel=9, mtime=0) as g:  # mtime=0: samme indhold giver samme fil
                    g.write(f.read())
        print('Fixtur opdateret fra de rigtige datafiler.')
    t = time.time()
    nu, fejl = regn()
    if fejl:
        print('REGRESSION: FEJL –', fejl)
        return 2
    sek = time.time() - t
    if '--opdater-facit' in args or '--opdater-fixtur' in args:
        gem_json(FACIT, nu)
        print(f'Facit gemt ({os.path.relpath(FACIT, ROD)}, {sek:.1f} s). Husk at forklare i rapporten, hvorfor tallene ændrede sig.')
        return 0
    if not os.path.exists(FACIT):
        print('REGRESSION: FEJL – facit.json mangler (kør med --opdater-facit)')
        return 2
    with open(FACIT, encoding='utf-8') as f:
        facit = json.load(f)
    nu = json.loads(json.dumps(nu, ensure_ascii=False))  # samme afrunding/typer som den gemte fil
    d = forskelle(facit, nu)
    if not d:
        print(f'REGRESSION: BESTÅET ({sek:.1f} s, ingen forskel mod facit)')
        return 0
    print(f'REGRESSION: FEJLET – {len(d)} forskelle mod facit (viser de første 25):')
    for sti, a, b in d[:25]:
        print(f'  {sti}: facit={json.dumps(a, ensure_ascii=False)[:90]}  nu={json.dumps(b, ensure_ascii=False)[:90]}')
    print('Er ændringen tilsigtet: kør `python -I scripts/tests/regression.py --opdater-facit` og beskriv før/efter i rapporten.')
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
