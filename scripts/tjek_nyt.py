"""Tjekker om der er kommet en NY tilbudsavis hos nogen butikker – uden at røre øjebliksbilledet eller retterne.

Brug:  python -I scripts/tjek_nyt.py
Skriver én linje pr. butik og til sidst "NYE: netto meny …" (ny ugeavis -> nye retter) og "SUPPLERET: lidl …" (samme ugeavis, men en
ekstra avis er kommet til eller udløbet -> tilbud.py + remap_ider.py, ingen nye retter); "ingen" når der ikke er nogen. Afslutter altid med kode 0,
medmindre Tjek ikke kan nås for nogen af butikkerne (kode 2).
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tilbud import BUTIKKER, er_ugeavis, find_aviser, laes_snapshot  # noqa: E402


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    snap = laes_snapshot()['butikker']
    nye, suppleret, fejl = [], [], 0
    for key in BUTIKKER:
        gemt_aviser = snap.get(key, {}).get('aviser', [])
        gemt = {a['id'] for a in gemt_aviser}
        gemt_uge = {a['id'] for a in gemt_aviser if not a.get('fast')}
        try:
            nu = find_aviser(key)
        except Exception as e:  # netværk, Tjek nede …
            fejl += 1
            print(f"{key}: kunne ikke hente ({type(e).__name__}: {e})")
            continue
        nu_ids = {a['id'] for a in nu}
        nu_uge = {a['id'] for a in nu if er_ugeavis(a['label'])}
        ny = bool(nu_uge) and nu_uge != gemt_uge  # ny ugeavis -> nye retter
        suppl = not ny and bool(nu_ids) and nu_ids != gemt  # samme ugeavis, men en ekstra avis er kommet til eller udløbet -> samme retter, nye id'er
        ekstra = ', '.join(a['label'] for a in nu if a['id'] not in gemt)
        print(f"{key}: gemt {sorted(gemt)} / nu {sorted(nu_ids)}" + ('  -> NY AVIS' if ny else f'  -> SUPPLERET ({ekstra or "en avis er udløbet"})' if suppl else ''))
        if ny:
            nye.append(key)
        elif suppl:
            suppleret.append(key)
    print('NYE: ' + (' '.join(nye) if nye else 'ingen'))
    print('SUPPLERET: ' + (' '.join(suppleret) if suppleret else 'ingen'))
    if fejl == len(BUTIKKER):
        sys.exit(2)


if __name__ == '__main__':
    main()
