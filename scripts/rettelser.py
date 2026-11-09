"""Redaktionelle rettelser til opskrifter: scripts/rettelser.json (navn -> felter), anvendt hver gang retterne bygges.

Så bliver en rettelse (fx stegetrin til en flæskesteg) ved med at gælde, selv om retten bygges forfra hver uge, og den gælder både biblioteksopskriften
og butikkernes egne kopier. Felter i rettelser.json (alle valgfrie):
  "fremgangsmaade": [trin ...]      erstatter alle trin
  "tid_minutter": 90
  "beskrivelse": "…"
  "niveau": "familie"
  "maengder": [{"ingrediens": "ris", "maengde": 300, "enhed": "g"}]     ændrer mængde/enhed på en eksisterende ingrediens (navnet må være en del af ingrediensnavnet)
  "tilfoej_basis": [{"ingrediens": "salt", "maengde": 1, "enhed": "tsk"}] tilføjer en basisvare (uden tilbud), hvis den ikke findes
  "tilfoej_vare": [{"ingrediens": "majskolber", "maengde": 4, "enhed": "stk"}]   tilføjer en almindelig vare til normalpris (ikke basisvare, ikke koblet til tilbud)
  "koekken": "dansk"
Bruges af bibliotek.py (opskriftsbiblioteket) og byg_retter.py (butikkernes egne, fuldt skrevne retter)."""
import json, os

STI = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rettelser.json')


def _laes():
    if not os.path.exists(STI):
        return {}
    with open(STI, encoding='utf-8') as f:
        return {k: v for k, v in json.load(f).items() if not k.startswith('_')}


def _find(ings, navn, navn_ved):
    n = navn.lower()
    ens = [i for i in ings if navn_ved(i).lower() == n]
    if ens:
        return ens[0]
    dele = [i for i in ings if n in navn_ved(i).lower()]
    return dele[0] if len(dele) == 1 else None


def anvend_bibliotek(retter):
    """retter: biblioteksopskrifter (dict med ingredienser som tuples (navn, mængde, enhed, basis, type, nøgle)). Ændrer dem på stedet; returnerer antal rettede."""
    rk, antal = _laes(), 0
    for r in retter:
        x = rk.get(r['navn'])
        if not x:
            continue
        antal += 1
        for f in ('fremgangsmaade', 'tid_minutter', 'beskrivelse', 'niveau', 'koekken'):
            if f in x:
                r[f] = list(x[f]) if f == 'fremgangsmaade' else x[f]
        ings = [list(i) for i in r['ingredienser']]
        for m in x.get('maengder', []):
            i = _find(ings, m['ingrediens'], lambda i: i[0])
            if i is None:
                print(f"ADVARSEL rettelser: '{r['navn']}': ingen ingrediens '{m['ingrediens']}'")
                continue
            i[1], i[2] = m['maengde'], m['enhed']
        for b in x.get('tilfoej_basis', []):
            if not any(i[0].lower() == b['ingrediens'].lower() for i in ings):
                ings.append([b['ingrediens'], b['maengde'], b['enhed'], 1, '', 0])
        for b in x.get('tilfoej_vare', []):
            if not any(i[0].lower() == b['ingrediens'].lower() for i in ings):
                ings.append([b['ingrediens'], b['maengde'], b['enhed'], 0, '', 0])
        r['ingredienser'] = [tuple(i) for i in ings]
    return antal


def anvend_kilde(r):
    """r: en fuldt skrevet butiksret fra scripts/retter/*.json (ingredienser som lister [navn, mængde, enhed, basis, [tilbud-id'er]]). Ændrer på stedet."""
    x = _laes().get(r.get('navn'))
    if not x:
        return False
    for f in ('fremgangsmaade', 'tid_minutter', 'beskrivelse', 'niveau', 'koekken'):
        if f in x:
            r[f] = list(x[f]) if f == 'fremgangsmaade' else x[f]
    ings = r['ingredienser']
    for m in x.get('maengder', []):
        i = _find(ings, m['ingrediens'], lambda i: i[0])
        if i is None:
            print(f"ADVARSEL rettelser: '{r['navn']}': ingen ingrediens '{m['ingrediens']}'")
            continue
        i[1], i[2] = m['maengde'], m['enhed']
    for b in x.get('tilfoej_basis', []):
        if not any(i[0].lower() == b['ingrediens'].lower() for i in ings):
            ings.append([b['ingrediens'], b['maengde'], b['enhed'], 1, []])
    for b in x.get('tilfoej_vare', []):
        if not any(i[0].lower() == b['ingrediens'].lower() for i in ings):
            ings.append([b['ingrediens'], b['maengde'], b['enhed'], 0, []])
    return True
