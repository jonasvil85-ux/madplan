"""Bygger retter.json (det siden viser) ud fra scripts/retter/<butik>.json + ugens tilbud.

Ugentlig rutine (pr. butik, når dens avis skifter):
  1. python -I scripts/tilbud.py <butik> > tilbud.txt   (henter avisen og viser tilbud med id'er)
  2. Skriv scripts/retter/<butik>.json                   (30 retter, kun den avis' tilbuds-id'er)
  3. python -I scripts/byg_retter.py                     (validerer og skriver retter.json)
  4. git commit + push  -> Vercel deployer automatisk

Format for scripts/retter/<butik>.json:
  {"avis": "<katalog-id>", "retter": [ <ret>, ... ]}
  <ret> er enten en fuld opskrift:
    {"navn", "beskrivelse", "niveau", "kategori", "tid_minutter", "spis_tidligt",
     "ingredienser": [[navn, mængde (4 pers.), enhed, basisvare 0/1, [tilbuds-id'er]], ...],
     "fremgangsmaade": [...]}
  eller en genbrugt opskrift fra en anden butiks fil:
    {"som": "<navn på opskrift>", "tilbud": {"<ingrediensnavn>": ["R12"], ...}}
    Værdien kan også være {"tilbud": [...], "navn": "nyt navn", "maengde": 500, "enhed": "g"} for at tilpasse
    ingrediensen. Øvrige felter (fx "niveau", "beskrivelse") overskriver opskriftens.
"""
import copy, glob, json, math, os, re, sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tilbud import BUTIKKER, SNAPSHOT  # noqa: E402

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FELTER = ['navn', 'maengde', 'enhed', 'basisvare', 'tilbud']
NIVEAUER = {'student', 'familie', 'weekend'}
# Retterne skal være hjemmelavede: ingen færdigretter, færdigtilbehør eller færdige saucer/deje
FORARBEJDET = re.compile(r'flødekartofler|herregårds|kødboller|melboller|panering|paneret|eriks sauce|færdigret|middagsret|'
                         r'dinner kit|pizzadej|pesto|pastasauce|kopsuppe|snackpot|ristorante|rustica|surdejspizza|'
                         r'italiensk pizza|æbleskiver|kyllingemarked|kebab|confit|smørrebrød|menu|mortensaften|'
                         r'frikadeller|lasagne|nuggets|cordon|wok-?mix|færdig|brunede kartofler|kartoffelgratin|kålsalat|'
                         r'andesauce|risalamande|forårsruller|spring rolls|fyldt pasta|pizzatopping|grande pizza|'
                         r'tex mex|indbagt|minifrikadeller|kebabbrød|toast|wienerbrød|tærte', re.I)
OMREGN = {'g': ('g', 1), 'kg': ('g', 1000), 'ml': ('ml', 1), 'cl': ('ml', 10), 'l': ('ml', 1000), 'stk': ('stk', 1)}
# Groft skøn (kr pr. enhed) for ingredienser der IKKE er på tilbud, så retter med få tilbudsvarer
# ikke ser kunstigt billige ud i prissammenligningen. Basisvarer (salt, olie, mel …) tælles ikke.
NORMALPRIS = {'g': 0.06, 'ml': 0.025, 'dl': 2.5, 'stk': 6, 'dåse': 9, 'pakke': 20, 'bundt': 15,
              'fed': 1, 'spsk': 2, 'tsk': 1, 'efter smag': 0}


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


def laes_kilder():
    kilder = {}
    for sti in sorted(glob.glob(os.path.join(ROD, 'scripts', 'retter', '*.json'))):
        butik = os.path.splitext(os.path.basename(sti))[0]
        with open(sti, encoding='utf-8') as f:
            kilder[butik] = json.load(f)
    return kilder


def udfold(r, bibliotek, fejl, butik):
    """Gør en "som"-reference til en fuld opskrift med denne butiks tilbud."""
    if 'som' not in r:
        return r
    if r['som'] not in bibliotek:
        fejl.append(f"{butik}: 'som' peger på ukendt opskrift '{r['som']}'")
        return None
    ret = copy.deepcopy(bibliotek[r['som']])
    tilpas = r.get('tilbud', {})
    navne = {ing[0] for ing in ret['ingredienser']}
    for navn in tilpas:
        if navn not in navne:
            fejl.append(f"{butik}: '{r['som']}' har ingen ingrediens '{navn}'")
    for ing in ret['ingredienser']:
        v = tilpas.get(ing[0], [])
        if isinstance(v, dict):
            ing[0] = v.get('navn', ing[0])
            ing[1] = v.get('maengde', ing[1])
            ing[2] = v.get('enhed', ing[2])
            v = v.get('tilbud', [])
        ing[4] = v
    ret.update({k: v for k, v in r.items() if k not in ('som', 'tilbud')})
    return ret


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    kilder = laes_kilder()
    # Brug det gemte øjebliksbillede – Tjeks rækkefølge (og dermed id'erne) skifter mellem kald
    with open(SNAPSHOT, encoding='utf-8') as f:
        data = json.load(f)
    alle = {t['kort']: t for t in data['tilbud']}
    fejl, ud = [], {}
    bibliotek = {r['navn']: r for k in kilder.values() for r in k['retter'] if 'som' not in r}

    for butik, b in BUTIKKER.items():
        if butik not in kilder:
            continue
        info = data['butikker'].get(butik)
        if not info:
            fejl.append(f"{butik}: ingen tilbud i øjebliksbilledet – kør scripts/tilbud.py {butik}")
            continue
        avis_ids = [a['id'] for a in info['aviser']]
        if kilder[butik]['avis'] not in avis_ids:
            fejl.append(f"{butik}: retterne er lavet til avis {kilder[butik]['avis']}, men øjebliksbilledet har {avis_ids}")
            continue
        retter, brugte, navne = [], {}, set()
        for nr, kilderet in enumerate(kilder[butik]['retter'], 1):
            r = udfold(kilderet, bibliotek, fejl, butik)
            if r is None:
                continue
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
            oevrigt = sum(i['maengde'] * NORMALPRIS.get(i['enhed'], 5) for i in ikke_basis if not i['tilbud'])
            andel = sum(1 for i in ikke_basis if i['tilbud']) / max(1, len(ikke_basis))
            if not behov:
                fejl.append(f"{butik}: '{r['navn']}' har ingen tilbudsvarer")
            retter.append({**r, 'id': f'{butik}-{nr}', 'ingredienser': ingredienser,
                           'pris_tilbud': round(pris, 2), 'pris_oevrigt': round(oevrigt, 2),
                           'pris_i_alt': round(pris + oevrigt, 2), 'andel_tilbud': round(andel, 2)})
        ud[butik] = {**info, 'retter': retter, 'tilbud': brugte}

        print(f"\n{info['navn']}: {len(retter)} retter, {len(brugte)} forskellige tilbudsvarer, "
              f"gns. {round(sum(r['andel_tilbud'] for r in retter) / max(1, len(retter)) * 100)}% tilbud")
        for niv in ('student', 'familie', 'weekend'):
            rr = [r for r in retter if r['niveau'] == niv]
            print(f"  {niv:8} {len(rr):2} retter")
            for r in rr:
                print(f"    {r['pris_i_alt']:7.2f} kr (tilbud {r['pris_tilbud']:6.2f})  {round(r['andel_tilbud'] * 100):3d}% tilbud  {r['navn']}")

    if fejl:
        print('\nFEJL:\n- ' + '\n- '.join(fejl))
        sys.exit(1)

    with open(os.path.join(ROD, 'retter.json'), 'w', encoding='utf-8') as f:
        json.dump({'genereret': datetime.now(timezone.utc).isoformat(timespec='seconds'), 'butikker': ud},
                  f, ensure_ascii=False, separators=(',', ':'))
    print(f"\nretter.json skrevet ({os.path.getsize(os.path.join(ROD, 'retter.json')) // 1024} KB)")


if __name__ == '__main__':
    main()
