"""Genbruger de HÅNDSKREVNE opskrifter (scripts/retter_skabeloner.json) til en butik, så butikken får mange håndskrevne retter fra start.

For hver skabelon finder scriptet butikkens egne tilbud til opskriftens ingredienser (typerne i bibliotek_typer.py), kasserer retten, hvis hovedvaren
(kød/fisk/kylling/grønt, som var på tilbud i originalen) ikke er på tilbud i butikken, og skriver den som en "som"-reference i scripts/retter/<butik>.json
(se docstringen i byg_retter.py). Retter, butikken allerede har, springes over. Kør derefter udvid_retter.py, som fylder op til 50 med biblioteksretter.

Brug:  python -I scripts/genbrug_retter.py <butik> [--op-til 45] [--min-andel 0.6]
  --op-til N     antal håndskrevne retter butikken højst skal have i alt (standard 45)
  --min-andel X  mindst denne andel af de ingredienser, der var på tilbud i originalen, skal også være på tilbud i butikken (standard 0.6)
Rutinen kan bruge det som start på trin 2 i RUTINE.md, når en butiks avis er skiftet."""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tilbud import BUTIKKER, laes_snapshot  # noqa: E402
import byg_retter as BR  # noqa: E402
from bibliotek_typer import TYPER  # noqa: E402
import udvid_retter as UV  # noqa: E402

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKABELONER = os.path.join(ROD, 'scripts', 'retter_skabeloner.json')
# Typer, der er hovedvarer (kød, fisk, kylling …): mindst én af dem skal være på tilbud, hvis originalen havde en på tilbud
HOVED = {'hakket_okse', 'hakket_gris', 'hakket_kylling', 'kyllingebryst', 'kyllingelaar', 'hel_kylling', 'bacon', 'flaesk', 'flaeskesteg', 'medister', 'polser',
         'spareribs', 'svinekoteletter', 'moerbrad', 'oksebof', 'okse_tern', 'laks', 'hvid_fisk', 'tun', 'rejer', 'chorizo'}


def type_for(navn):
    n = navn.lower()
    for typ, (inkl, ekskl) in TYPER.items():
        if re.search(inkl, n) and not (ekskl and re.search(ekskl, n)):
            return typ
    return None


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    args = sys.argv[1:]
    butik = next((a for a in args if a in BUTIKKER), None)
    if not butik:
        sys.exit(f"Angiv en butik: {', '.join(BUTIKKER)}")
    op_til = int(args[args.index('--op-til') + 1]) if '--op-til' in args else 45
    min_andel = float(args[args.index('--min-andel') + 1]) if '--min-andel' in args else 0.6
    tilbud = [t for t in laes_snapshot()['tilbud'] if t['butik'] == butik]
    d, navne, antal = UV.eksisterende(butik)
    haandskrevne = [r for r in d['retter'] if not r.get('auto')]
    plads = op_til - len(haandskrevne)
    if plads <= 0:
        print(f"{BUTIKKER[butik]['navn']}: har allerede {len(haandskrevne)} håndskrevne retter"); return
    skabeloner = json.load(open(SKABELONER, encoding='utf-8'))
    kandid = []
    for s in skabeloner:
        if s['navn'] in navne or any((r.get('navn') or r.get('som')) == s['navn'] for r in haandskrevne):
            continue
        match, med_tilbud, hoved_orig, hoved_ok, tilpas = 0, 0, False, False, {}
        for navn, m, e, basis, ids in s['ingredienser']:
            if basis:
                continue
            typ = type_for(navn)
            if ids:                                   # originalen havde et tilbud på denne ingrediens
                med_tilbud += 1
                hoved_orig = hoved_orig or typ in HOVED
            kand = UV.kandidater(tilbud, typ) if typ else []
            if ids and kand:
                b = UV.vaelg_bedste(kand, m, e)
                tilpas[navn] = [b['kort']]
                match += 1
                hoved_ok = hoved_ok or typ in HOVED
        if not med_tilbud or match / med_tilbud < min_andel or (hoved_orig and not hoved_ok):
            continue
        kandid.append((match / med_tilbud, match, s, tilpas))
    kandid.sort(key=lambda x: (-x[0], -x[1]))
    per_koekken, valgt = {}, []
    for andel, match, s, tilpas in kandid:
        if len(valgt) >= plads:
            break
        k = s['koekken']
        if per_koekken.get(k, 0) >= (22 if k == 'dansk' else 10):
            continue
        per_koekken[k] = per_koekken.get(k, 0) + 1
        valgt.append({'som': s['navn'], 'tilbud': tilpas})
    d['retter'] = haandskrevne + valgt + [r for r in d['retter'] if r.get('auto')]
    with open(os.path.join(UV.RETTER_MAPPE, f'{butik}.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
    print(f"{BUTIKKER[butik]['navn']}: {len(haandskrevne)} håndskrevne + {len(valgt)} genbrugte = {len(haandskrevne) + len(valgt)} (kandidater: {len(kandid)}) | "
          + ', '.join(f'{k} {n}' for k, n in sorted(per_koekken.items())))


if __name__ == '__main__':
    main()
