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
  "skift": [{"fra": "rugbrød", "til": "baguette", "type": "baguette", "maengde": 1, "enhed": "stk"}]   skifter en ingrediens ud (navn, type, mængde); tilbudskoblingen fjernes; ordet rettes også i trin og beskrivelse
Bruges af bibliotek.py (opskriftsbiblioteket) og byg_retter.py (butikkernes egne, fuldt skrevne retter)."""
import json, os, re

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


def _tekst_skift(tekst, fra, til):
    """Retter ordet i en tekst (rugbrød/rugbrødet -> baguette/baguetten)."""
    tekst = re.sub(re.escape(fra) + r'et', til + 'n' if til.endswith('e') is False else til + 'n', tekst, flags=re.I)
    return re.sub(re.escape(fra), til, tekst, flags=re.I)


SPROEJTET = set()


UDEN = {'økologisk', 'økologiske', 'dansk', 'danske', 'frisk', 'friske', 'fersk', 'ferske', 'hakket', 'røget', 'røgede', 'på', 'med', 'af', 'eller', 'i', 'top', 'glas', 'dåse', 'fryst', 'frosne'}


def _stamme(navn):
    ord_ = [o for o in re.findall(r'[a-zæøå]+', navn.lower()) if o not in UDEN and len(o) > 2] or [navn.lower()]
    return max(ord_, key=len)[:5]


def _kompatibel(x, ings):
    """Gennemlæseren så en bestemt liste af ingredienser ("_ref"). Butiksudgaver (skabeloner) kan have andre ingredienser; en rettelse anvendes kun, hvis listerne i det store hele er ens."""
    ref = {_stamme(n) for n in x.get('_ref', [])}
    if not ref:
        return True
    her = {_stamme(i[0]) for i in ings if not i[3]}
    return len(ref & her) / max(1, len(ref | her)) >= 0.5


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
        for s in x.get('skift', []):
            i = _find(ings, s['fra'], lambda i: i[0])
            if i is not None:
                i[0], i[1], i[2], i[4] = s['til'], s['maengde'], s['enhed'], s.get('type', '')
            elif _find(ings, s['til'], lambda i: i[0]) is None:
                print(f"ADVARSEL rettelser: '{r['navn']}': ingen ingrediens '{s['fra']}' at skifte")
                continue
            r['fremgangsmaade'] = [_tekst_skift(t, s['fra'], s['til']) for t in r['fremgangsmaade']]
            r['beskrivelse'] = _tekst_skift(r['beskrivelse'], s['fra'], s['til'])
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
    if not _kompatibel(x, r['ingredienser']):
        if r['navn'] not in SPROEJTET:
            SPROEJTET.add(r['navn'])
            print(f"NOTE rettelser: '{r['navn']}' har andre ingredienser end den gennemgåede udgave – kun brødskift anvendes for denne butiksudgave")
        x = {'skift': x['skift']} if x.get('skift') else None  # et ingrediensskift (rugbrød -> baguette) gælder altid; resten springes over
        if not x:
            return False
    for f in ('fremgangsmaade', 'tid_minutter', 'beskrivelse', 'niveau', 'koekken'):
        if f in x:
            r[f] = list(x[f]) if f == 'fremgangsmaade' else x[f]
    ings = r['ingredienser']
    for s in x.get('skift', []):
        i = _find(ings, s['fra'], lambda i: i[0])
        if i is not None:
            i[0], i[1], i[2], i[4] = s['til'], s['maengde'], s['enhed'], []
        elif _find(ings, s['til'], lambda i: i[0]) is None:
            print(f"ADVARSEL rettelser: '{r['navn']}': ingen ingrediens '{s['fra']}' at skifte")
            continue
        r['fremgangsmaade'] = [_tekst_skift(t, s['fra'], s['til']) for t in r['fremgangsmaade']]
        r['beskrivelse'] = _tekst_skift(r['beskrivelse'], s['fra'], s['til'])
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
