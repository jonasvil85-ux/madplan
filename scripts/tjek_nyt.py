"""Tjekker om der er kommet en NY tilbudsavis hos nogen butikker – uden at røre øjebliksbilledet eller retterne.

Brug:  python -I scripts/tjek_nyt.py
Skriver én linje pr. butik og til sidst "NYE: netto meny …" (eller "NYE: ingen"). Afslutter altid med kode 0,
medmindre Tjek ikke kan nås for nogen af butikkerne (kode 2).
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tilbud import BUTIKKER, find_aviser, laes_snapshot  # noqa: E402


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    snap = laes_snapshot()['butikker']
    nye, fejl = [], 0
    for key in BUTIKKER:
        gemt = {a['id'] for a in snap.get(key, {}).get('aviser', [])}
        try:
            nu = find_aviser(key)
        except Exception as e:  # netværk, Tjek nede …
            fejl += 1
            print(f"{key}: kunne ikke hente ({type(e).__name__}: {e})")
            continue
        nu_ids = {a['id'] for a in nu}
        ny = bool(nu_ids) and nu_ids != gemt
        print(f"{key}: gemt {sorted(gemt)} / nu {sorted(nu_ids)}" + ('  -> NY AVIS' if ny else ''))
        if ny:
            nye.append(key)
    print('NYE: ' + (' '.join(nye) if nye else 'ingen'))
    if fejl == len(BUTIKKER):
        sys.exit(2)


if __name__ == '__main__':
    main()
