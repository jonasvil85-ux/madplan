"""Bygger opskrifter.json: opskriftsbiblioteket (bibliotek_1..3) med ugens tilbud fra ALLE butikker koblet på hver ingrediens.

Hver ingrediens med en type (fx 'hakket_okse', 'kartofler') får en liste af tilbud-id'er: den billigste vare af typen i hver butiks avis.
Siden vælger så selv det billigste tilbud blandt de butikker, brugeren har valgt – også inden for samme ret
(kartofler fra Bilka, hakket kød fra Netto …). Retter, hvor en nøgle-ingrediens ikke er på tilbud i nogen af de valgte butikker, vises ikke.

Bruger scripts/tilbud_snapshot.json – kør scripts/tilbud.py først. Skal køres hver gang aviser er hentet (står i RUTINE.md).

Brug:  python -I scripts/byg_opskrifter.py
"""
import datetime, json, os, sys

HER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HER)
from tilbud import BUTIKKER, laes_snapshot  # noqa: E402
import byg_retter as BR  # noqa: E402
from bibliotek import RETTER as BIB  # noqa: E402
from billeder import slug  # noqa: E402
from udvid_retter import kandidater, vaelg_bedste  # noqa: E402

ROD = os.path.dirname(HER)
UD = os.path.join(ROD, 'opskrifter.json')
TILBUDSFELTER = ('navn', 'pris', 'forPris', 'maengde', 'enhed', 'billede', 'gyldigTil', 'stk')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    data = laes_snapshot()
    nu = datetime.datetime.now(datetime.timezone.utc)

    def gyldig(t):
        try:
            return datetime.datetime.strptime(t['gyldigTil'], '%Y-%m-%dT%H:%M:%S%z') >= nu
        except (KeyError, ValueError, TypeError):
            return True

    pr_butik = {b: [t for t in data['tilbud'] if t['butik'] == b and gyldig(t)] for b in BUTIKKER}
    udvalgte = {}
    typer = {}  # ingrediens-type -> tilbud-id'er (pr. butik de billigste til små og store mængder), så siden kan vælge billigst for hele ugens mængde
    opskrifter = []
    for nr, o in enumerate(BIB, 1):
        ings = []
        for navn, m, e, basis, typ, noegle in o['ingredienser']:
            ids = []
            if typ:
                fund = []
                for b, tilbud in pr_butik.items():
                    kand = kandidater(tilbud, typ)
                    if kand:
                        t = vaelg_bedste(kand, m, e)
                        fund.append((t['pris'] * BR.antal_pakker(t, {e: m}), t))
                        for faktor in (0.3, 1, 2.5, 5):  # den bedste pakke afhænger af mængden (1 voksen eller en stor familie)
                            tt = vaelg_bedste(kand, m * faktor, e)
                            typer.setdefault(typ, [])
                            if tt['kort'] not in typer[typ]:
                                typer[typ].append(tt['kort'])
                            udvalgte[tt['kort']] = {'butik': tt['butik'], 'kort': tt['kort'], **{f: tt.get(f) for f in TILBUDSFELTER if tt.get(f) is not None}}
                for _, t in sorted(fund, key=lambda x: x[0]):
                    ids.append(t['kort'])
                    udvalgte[t['kort']] = {'butik': t['butik'], 'kort': t['kort'], **{f: t.get(f) for f in TILBUDSFELTER if t.get(f) is not None}}
            ings.append({'navn': navn, 'maengde': m, 'enhed': e, 'basisvare': bool(basis), 'noegle': bool(noegle), 'typ': typ or None, 'tilbud': ids})
        billede = f"billeder/{slug(o['navn'])}.jpg"
        r = {'id': f'mix-{nr}', **{k: o[k] for k in ('navn', 'beskrivelse', 'niveau', 'kategori', 'koekken', 'tid_minutter', 'spis_tidligt', 'fremgangsmaade')},
             'ingredienser': ings}
        if os.path.exists(os.path.join(ROD, billede)):
            r['billede'] = billede
        opskrifter.append(r)
    ud = {'genereret': datetime.datetime.now().astimezone().isoformat(timespec='seconds'), 'tilbud': udvalgte, 'typer': typer, 'opskrifter': opskrifter}
    with open(UD, 'w', encoding='utf-8') as f:
        json.dump(ud, f, ensure_ascii=False, separators=(',', ':'))
    print(f"opskrifter.json skrevet: {len(opskrifter)} opskrifter, {len(udvalgte)} tilbud ({os.path.getsize(UD) // 1024} KB)")
    # Overblik: hvor mange opskrifter har alle nøgle-ingredienser på tilbud, hvis man kun bruger én butik / alle butikker?
    for navn, butikker in [(BUTIKKER[b]['navn'], [b]) for b in BUTIKKER] + [('ALLE butikker', list(BUTIKKER))]:
        ok = sum(1 for r in opskrifter if all(any(udvalgte[i]['butik'] in butikker for i in ing['tilbud']) for ing in r['ingredienser'] if ing['noegle']))
        print(f'  {navn:14} {ok:3d} af {len(opskrifter)} opskrifter har alle nøgle-ingredienser på tilbud')


if __name__ == '__main__':
    main()
