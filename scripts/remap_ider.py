"""Flytter en butiks retter over på nye tilbuds-id'er, når id'erne er skiftet, uden at avisen er ny.

Hvornår: tilbud.py giver tilbuddene id'er efter side og navn. Kommer der en ekstra madavis med (eller en avis forsvinder), flytter ALLE id'er sig, og retterne i
scripts/retter/<butik>.json peger på forkerte varer. Dette script finder hvert gammelt tilbud i den nye liste (samme navn, pris og mængde – ellers samme vare efter `samme_tilbud` i tilbud.py) og retter id'erne.

Brug:
  1. gem det gamle øjebliksbillede (git har det: det er filen, som scriptet bruger som standard)
  2. python -I scripts/tilbud.py <butik> > tilbud.txt         (nye id'er)
  3. python -I scripts/remap_ider.py <butik> [gammelt_snapshot.json]
  Uden filnavn bruges scripts/tilbud_snapshot.json, som den står i git (HEAD). Tilbud, der ikke længere findes, fjernes fra retterne og udskrives.
Kør derefter udvid_retter.py (hvis der skal flere retter til), byg_retter.py, byg_opskrifter.py og byg_tilbudsliste.py."""
import json, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tilbud import samme_tilbud  # noqa: E402

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP = os.path.join(ROD, 'scripts', 'tilbud_snapshot.json')


def noegle(t):
    return (t['navn'].strip().lower(), t['pris'], t['maengde'], t['enhed'])


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    butik = sys.argv[1]
    if len(sys.argv) > 2:
        gammel = json.load(open(sys.argv[2], encoding='utf-8'))
    else:
        gammel = json.loads(subprocess.run(['git', 'show', 'HEAD:scripts/tilbud_snapshot.json'], capture_output=True, cwd=ROD, check=True).stdout.decode('utf-8'))
    ny = json.load(open(SNAP, encoding='utf-8'))
    g = {t['kort']: t for t in gammel['tilbud'] if t['butik'] == butik}
    n = {}
    for t in ny['tilbud']:
        if t['butik'] == butik:
            n.setdefault(noegle(t), t['kort'])
    n_navnpris = {}
    for t in ny['tilbud']:
        if t['butik'] == butik:
            n_navnpris.setdefault((t['navn'].strip().lower(), t['pris']), t['kort'])
    nye = [t for t in ny['tilbud'] if t['butik'] == butik]
    kort = {}
    for k, t in g.items():
        ny_k = n.get(noegle(t)) or n_navnpris.get((t['navn'].strip().lower(), t['pris']))
        if not ny_k:  # samme vare, men navn eller mængde skrevet lidt anderledes (fx slået sammen med et kombi-tilbud til samme pris)
            ny_k = next((x['kort'] for x in nye if samme_tilbud(x, t)), None)
        if ny_k:
            kort[k] = ny_k
    sti = os.path.join(ROD, 'scripts', 'retter', f'{butik}.json')
    d = json.load(open(sti, encoding='utf-8'))
    manglede, flyttet = [], 0

    def flyt(ids, ret, ing):
        nonlocal flyttet
        ud = []
        for i in ids:
            if i in kort:
                ud.append(kort[i]); flyttet += 1
            else:
                manglede.append((ret, ing, g.get(i, {}).get('navn', i)))
        return ud

    for r in d['retter']:
        navn = r.get('navn') or r.get('som')
        for ing in r.get('ingredienser', []):
            ing[4] = flyt(ing[4], navn, ing[0])
        for ing_navn, v in (r.get('tilbud') or {}).items():
            if isinstance(v, list):
                r['tilbud'][ing_navn] = flyt(v, navn, ing_navn)
            else:
                v['tilbud'] = flyt(v.get('tilbud', []), navn, ing_navn)
    for t in d.get('top', []):
        if t.get('id') in kort:
            t['id'] = kort[t['id']]
    d['top'] = [t for t in d.get('top', []) if t.get('id') in set(kort.values())]
    nye_avis = [a['id'] for a in ny['butikker'][butik]['aviser'] if not a.get('fast')]
    if nye_avis:
        d['avis'] = nye_avis[0]
    open(sti, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
    print(f"{butik}: {flyttet} koblinger flyttet; {len(g)} gamle tilbud, {len(kort)} fundet i den nye liste, {len(g) - len(kort)} findes ikke mere")
    for ret, ing, tilb in manglede:
        print(f"  fjernet: {ing}  x  {tilb[:60]}  (ret: {ret})")


if __name__ == '__main__':
    main()
