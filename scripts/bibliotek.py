"""Samler opskriftsbiblioteket (bibliotek_1..5)."""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from bibliotek_1 import RETTER as _1
from bibliotek_2 import RETTER as _2
from bibliotek_3 import RETTER as _3
from bibliotek_4 import RETTER as _4
from bibliotek_5 import RETTER as _5
from bibliotek_typer import TYPER

RETTER = _1 + _2 + _3 + _4 + _5
# Smør til sovs, mos og stegning (mindst 30 g) er en rigtig vare, der kan være på tilbud (fx Lurpak) – kun mindre klatter er basisvarer
SMOER_MIN = 30
for _r in RETTER:
    _r['ingredienser'] = [(n, m, e, 0, t, k) if n == 'smør' and t == 'smor' and m >= SMOER_MIN and b else (n, m, e, b, t, k)
                          for (n, m, e, b, t, k) in _r['ingredienser']]
ENHEDER = {'g', 'ml', 'stk', 'spsk', 'tsk', 'fed', 'dåse', 'glas', 'pakke', 'bundt', 'efter smag'}
if __name__ == '__main__':
    import collections, sys
    sys.stdout.reconfigure(encoding='utf-8')
    fejl = []
    navne = collections.Counter(r['navn'] for r in RETTER)
    for r in RETTER:
        if navne[r['navn']] > 1: fejl.append('dublet: ' + r['navn'])
        if not any(i[5] for i in r['ingredienser']): fejl.append('ingen nøgle-ingrediens: ' + r['navn'])
        for navn, m, e, b, t, k in r['ingredienser']:
            if e not in ENHEDER: fejl.append(f"{r['navn']}: ukendt enhed {e} ({navn})")
            if t and t not in TYPER: fejl.append(f"{r['navn']}: ukendt type {t} ({navn})")
    print(len(RETTER), 'opskrifter', dict(collections.Counter(r['koekken'] for r in RETTER)))
    print('FEJL:', fejl or 'ingen')
