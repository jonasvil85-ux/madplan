"""Udtrækker de udvalgte fødevarer (tabel.FOEDEVARE_ID) fra USDA FoodData Central SR Legacy (CSV) til foedevarer.json.

Brug:  python -I scripts/naering/hent_usda.py <mappe med sr_legacy CSV-filerne>
Datasættet hentes fra https://fdc.nal.usda.gov/download-datasets (SR Legacy, CSV). Kun den lille foedevarer.json skal i repoet."""
import csv, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tabel import FOEDEVARE_ID  # noqa: E402

NID = {'1008': 'kcal', '1003': 'protein', '1004': 'fedt', '1005': 'kulhydrat'}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    d = sys.argv[1]
    enkelt = {k: v for k, v in FOEDEVARE_ID.items() if isinstance(v, str)}
    blandinger = {k: v for k, v in FOEDEVARE_ID.items() if not isinstance(v, str)}  # nøgle -> (id, id): middelværdi af to USDA-poster
    for ids in blandinger.values():
        for i in ids:
            enkelt.setdefault('_' + i, i)
    onsket = {v: k for k, v in enkelt.items()}
    navn = {r['fdc_id']: r['description'] for r in csv.DictReader(open(os.path.join(d, 'food.csv'), encoding='utf-8')) if r['fdc_id'] in onsket}
    ud = {k: {'fdc_id': i, 'beskrivelse': navn[i]} for i, k in onsket.items() if i in navn}
    for r in csv.DictReader(open(os.path.join(d, 'food_nutrient.csv'), encoding='utf-8')):
        if r['fdc_id'] in onsket and r['nutrient_id'] in NID:
            ud[onsket[r['fdc_id']]][NID[r['nutrient_id']]] = float(r['amount'])
    for k, ids in blandinger.items():
        poster = [ud['_' + i] for i in ids]
        ud[k] = {'fdc_id': '+'.join(ids), 'beskrivelse': ' + '.join(p['beskrivelse'] for p in poster) + ' (middelværdi)'}
        for n in ('kcal', 'protein', 'fedt', 'kulhydrat'):
            ud[k][n] = round(sum(p[n] for p in poster) / len(poster), 2)
    ud = {k: v for k, v in ud.items() if not k.startswith('_')}
    mangler = [k for k in FOEDEVARE_ID if k not in ud or len(ud[k]) < 6]
    if mangler:
        sys.exit('Mangler data for: ' + ', '.join(mangler))
    sti = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'foedevarer.json')
    json.dump({'kilde': 'USDA FoodData Central, SR Legacy (2018), pr. 100 g rå vare', 'foedevarer': ud}, open(sti, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(ud), 'fødevarer skrevet til', sti)


if __name__ == '__main__':
    main()
