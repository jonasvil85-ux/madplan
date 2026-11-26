"""Måling: bliver ugeforslaget dyrere, når der kommer en billig ret til? (advarsel, aldrig fejl)

Kører monotoni.js (sidens egen JavaScript i node, gemt datakopi, uden net) og skriver en tabel for 9 butikker x 3 husstande
(2+0, 2+2, 6+4): ugepris før, ugepris efter at en konstrueret billig ret (kopi af butikkens billigste og mest børnevenlige
retter til 25 % og 50 % af prisen) er lagt til, og forskellen. Pr. felt vises det VÆRSTE udfald; en stigning er en advarsel.
Ændrer intet i ugeforslagets algoritme eller i data.

  python -I scripts/tests/monotoni.py          tabel + advarsler (exit 0; exit 2 kun hvis målingen selv fejler)
  python -I scripts/tests/monotoni.py --stille kun slutlinjen (bruges af kontrol.py)
  python -I scripts/tests/monotoni.py --selvtest  tester målerens egen logik uden node
"""
import json, os, shutil, subprocess, sys

ROD = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
TEST = os.path.join(ROD, 'scripts', 'tests')
TOLERANCE = 0.005  # kr; afrundingsstøj tæller ikke


def maal():
    node = shutil.which('node')
    if not node:
        return None, 'node findes ikke her'
    p = subprocess.run([node, os.path.join(TEST, 'monotoni.js'), ROD, os.path.join(TEST, 'fixtur')], capture_output=True, text=True, encoding='utf-8', timeout=600)
    if p.returncode:
        return None, 'monotoni.js fejlede: ' + (p.stderr.strip().splitlines() or ['?'])[0][:300]
    return json.loads(p.stdout)['raekker'], None


def stigninger(raekker):
    """De felter, hvor ugen blev dyrere (mere end afrundingsstøj), størst først."""
    return sorted((r for r in raekker if r["diff"] > TOLERANCE), key=lambda r: -r['diff'])


def ustabile(raekker):
    """Felter hvor samme uge ikke kan genskabes (målingen er så ikke til at stole på)."""
    return [r for r in raekker if not r['gentagelig']]


def tabel(raekker):
    ud = [f"{'butik':<12}{'husstand':<9}{'før (kr)':>10}{'efter (kr)':>12}{'forskel':>9}  værste tilføjelse"]
    for r in raekker:
        ud.append(f"{r['butik']:<12}{r['husstand']:<9}{r['for']:>10.2f}{r['efter']:>12.2f}{r['diff']:>+9.2f}  {r['donor']} til {int(r['faktor'] * 100)} % af prisen{' (brugt i ugen)' if r['brugt'] else ''}")
    return '\n'.join(ud)


def slutlinje(raekker):
    st = stigninger(raekker)
    if not st:
        return 'MONOTONI: INGEN STIGNING (%d felter)' % len(raekker)
    top = st[0]
    return 'MONOTONI: ADVARSEL – %d af %d felter bliver dyrere, når en billig ret kommer til (størst: %s %s +%.2f kr, %.2f → %.2f)' % (
        len(st), len(raekker), top['butik'], top['husstand'], top['diff'], top['for'], top['efter'])


def selvtest():
    """Måleren selv: en konstrueret stigning skal fanges, et fald og afrundingsstøj ikke."""
    r = lambda d, g=True: {'butik': 'x', 'husstand': '2+2', 'for': 100.0, 'efter': 100.0 + d, 'diff': d, 'donor': 'x-1', 'faktor': 0.25, 'brugt': True, 'gentagelig': g}
    fejl = []
    if [x['diff'] for x in stigninger([r(-5), r(0), r(0.004), r(12), r(3)])] != [12, 3]: fejl.append('stigninger() fanger ikke præcis stigningerne')
    if 'ADVARSEL' not in slutlinje([r(12)]): fejl.append('en stigning giver ingen advarsel')
    if 'INGEN STIGNING' not in slutlinje([r(-5), r(0)]): fejl.append('et fald giver en advarsel')
    if len(ustabile([r(0, False), r(0)])) != 1: fejl.append('ustabil måling opdages ikke')
    return fejl


def main(args):
    if '--selvtest' in args:
        f = selvtest()
        print('MONOTONI-SELVTEST: ' + ('FEJLET – ' + '; '.join(f) if f else 'BESTÅET'))
        return 1 if f else 0
    raekker, fejl = maal()
    if fejl:
        print('MONOTONI: IKKE MÅLT – ' + fejl)
        return 2
    if ustabile(raekker):
        print('MONOTONI: IKKE MÅLT – samme uge kan ikke genskabes i ' + ', '.join(r['butik'] + ' ' + r['husstand'] for r in ustabile(raekker)))
        return 2
    if '--stille' not in args:
        print(tabel(raekker))
        print()
    print(slutlinje(raekker))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
