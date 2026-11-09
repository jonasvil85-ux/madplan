"""Regner kcal, protein, fedt og kulhydrat pr. portion ud for alle retter (retter.json) og biblioteksopskrifter (opskrifter.json) og skriver naering.json
(id -> værdier), som siden bruger til kategorien Fitness og til energifordelingen på retkortene.

Brug:  python -I scripts/naering/byg_naering.py      (kør efter byg_retter.py og byg_opskrifter.py – id'erne ændrer sig, når retterne bygges)
Mængderne i opskrifterne er til 4 personer, så alt deles med 4. Næringsværdierne pr. 100 g står i foedevarer.json (USDA FoodData Central, SR Legacy);
tabel.py slår ingredienserne op og omregner til gram. Skriptet udskriver dækningen og de hyppigste ingredienser uden opslag, så tabellen kan udvides."""
import collections, json, os, sys

HER = os.path.dirname(os.path.abspath(__file__))
ROD = os.path.dirname(os.path.dirname(HER))
sys.path.insert(0, HER)
from tabel import find_regel, gram  # noqa: E402

PERSONER = 4


def regn(ings, mad):
    sum_ = dict(kcal=0.0, protein=0.0, fedt=0.0, kulhydrat=0.0)
    ok = ukendt = 0
    mangler = []
    for i in ings:
        if i['enhed'] == 'efter smag':
            continue
        status, noegle, om = find_regel(i['navn'])
        if status == 'ignorer':
            continue
        g = gram(i['navn'], i['maengde'], i['enhed'], om) if status == 'ok' else None
        if g is None:
            ukendt += 1
            mangler.append(f"{i['navn']} ({i['maengde']:g} {i['enhed']})")
            continue
        ok += 1
        g *= om.get('spild', 1.0)
        f = mad[noegle]
        for k in sum_:
            sum_[k] += f[k] * g / 100 * om.get('faktor', 1.0)
    d = {k: round(v / PERSONER, 1) for k, v in sum_.items()}
    d['kcal'] = round(d['kcal'])
    d['daekning'] = round(ok / max(1, ok + ukendt), 2)
    return d, mangler


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    mad = json.load(open(os.path.join(HER, 'foedevarer.json'), encoding='utf-8'))['foedevarer']
    retter = json.load(open(os.path.join(ROD, 'retter.json'), encoding='utf-8'))
    opskr = json.load(open(os.path.join(ROD, 'opskrifter.json'), encoding='utf-8'))
    ud, ukendte = {'_genereret': retter['genereret']}, collections.Counter()  # siden bruger kun tallene, hvis stemplet passer til retter.json
    for b in retter['butikker'].values():
        for r in b['retter']:
            ud[r['id']], mangler = regn(r['ingredienser'], mad)
            ukendte.update(x.split(' (')[0].lower() for x in mangler)
    for r in opskr['opskrifter']:
        ings = [dict(navn=i['navn'], maengde=i['maengde'], enhed=i['enhed']) for i in r['ingredienser']]
        ud[r['id']], mangler = regn(ings, mad)
        ukendte.update(x.split(' (')[0].lower() for x in mangler)
    json.dump(ud, open(os.path.join(ROD, 'naering.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    dk = [v['daekning'] for k, v in ud.items() if k != '_genereret']
    print(f"naering.json skrevet: {len(dk)} retter; dækning gns. {sum(dk) / len(dk):.0%}; ≥90 %: {sum(1 for d in dk if d >= .9)}; <70 %: {sum(1 for d in dk if d < .7)}")
    print('Hyppigste ingredienser uden opslag:', ', '.join(f'{k} ({v})' for k, v in ukendte.most_common(15)))


if __name__ == '__main__':
    main()
