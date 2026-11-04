"""Bygger tilbudsliste.json til "Værd at overveje" på forsiden.

Pr. kategori (sodavand, fløde, smør, kød, kartofler …) gemmes hver butiks BILLIGSTE tilbud med kr/kg, kr/l eller kr/stk. Siden regner selv ud,
hvilken af de valgte butikker der er billigst, og hvor meget under de andre butikkers tilbud den ligger. Der sammenlignes altså tilbud med tilbud
(ikke med en normalpris, som vi ikke kender).

Bruger scripts/tilbud_snapshot.json – kør scripts/tilbud.py først. Kategorierne ligger i scripts/sammenlign.py.

Brug:  python -I scripts/byg_tilbudsliste.py
"""
import datetime, json, os, re, sys

HER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HER)
from tilbud import laes_snapshot  # noqa: E402
from sammenlign import KATEGORIER, enhedspris  # noqa: E402

UD = os.path.join(os.path.dirname(HER), 'tilbudsliste.json')
MIN_BUTIKKER = 3  # en sammenligning kræver mindst tre butikker med et tilbud i kategorien


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    data = laes_snapshot()
    kategorier = []
    for kat, (med, uden, enhed) in KATEGORIER.items():
        bedst = {}
        for t in data['tilbud']:
            tekst = f"{t['navn']} {t.get('beskrivelse', '')[:60]}"
            # Kun det første produkt i navnet tæller ('Fiskefilet, skalrejer, … laks' er ikke laks; 'Merrild eller Gevalia kaffe' er kaffe)
            forste = re.split(r',| eller | og ', t['navn'])[0]
            if re.search(med, forste, re.I) and not (uden and re.search(uden, tekst, re.I)):
                p = enhedspris(t, enhed)
                if p and (t['butik'] not in bedst or p < bedst[t['butik']][0]):
                    bedst[t['butik']] = (p, t)
        if len(bedst) < MIN_BUTIKKER:
            continue
        kategorier.append({
            'navn': kat, 'enhed': enhed,
            'tilbud': [{'butik': t['butik'], 'navn': t['navn'], 'pris': t['pris'], 'maengde': t.get('maengde'), 'enhed': t.get('enhed'),
                        'ep': round(p, 2), 'billede': t.get('billede'), 'gyldigTil': t.get('gyldigTil')}
                       for p, t in sorted(bedst.values(), key=lambda x: x[0])],
        })
    ud = {'genereret': datetime.datetime.now().astimezone().isoformat(timespec='seconds'), 'kategorier': kategorier}
    with open(UD, 'w', encoding='utf-8') as f:
        json.dump(ud, f, ensure_ascii=False, separators=(',', ':'))
    print(f'tilbudsliste.json skrevet: {len(kategorier)} kategorier')
    for k in kategorier:
        a, b = k['tilbud'][0], k['tilbud'][1:]
        median = sorted(x['ep'] for x in b)[len(b) // 2]
        print(f"  {k['navn']:18} billigst {a['butik']:12} {a['ep']:7.2f} kr/{k['enhed']}  ({round((1 - a['ep'] / median) * 100):3d} % under de andres midte)  {a['navn'][:40]}")


if __name__ == '__main__':
    main()
