"""Fletter kok-gennemgangens resultater (resultat_N.json) ind i scripts/rettelser.json og skriver en læseliste.

Brug:  python -I scripts/flet_gennemgang.py <mappe med resultat_*.json> [--alvor fejl,tvivl,forbedring]
Kun felter, der er tilladt i rettelser.json, tages med; ingen ingrediens-udskiftning. Eksisterende rettelser for samme ret overskrives felt for felt.
Skriver også <mappe>/laeseliste.md: retter, hvor gennemgangen er i tvivl (bruger_skal_laese) eller alvor = fejl/tvivl – til en menneskelig kok."""
import glob, json, os, sys

HER = os.path.dirname(os.path.abspath(__file__))
TILLADT = ('fremgangsmaade', 'tid_minutter', 'beskrivelse', 'niveau', 'koekken', 'maengder', 'tilfoej_basis', 'tilfoej_vare')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    mappe = sys.argv[1]
    alvor = set((sys.argv[sys.argv.index('--alvor') + 1] if '--alvor' in sys.argv else 'fejl,tvivl,forbedring').split(','))
    sti = os.path.join(HER, 'rettelser.json')
    rk = json.load(open(sti, encoding='utf-8')) if os.path.exists(sti) else {}
    antal = {'fejl': 0, 'tvivl': 0, 'forbedring': 0}
    laes = []
    for f in sorted(glob.glob(os.path.join(mappe, 'resultat_*.json'))):
        for x in json.load(open(f, encoding='utf-8')):
            antal[x['alvor']] = antal.get(x['alvor'], 0) + 1
            if x['alvor'] not in alvor:
                continue
            r = {k: v for k, v in (x.get('rettelse') or {}).items() if k in TILLADT and v}
            if r:
                rk.setdefault(x['navn'], {}).update(r)
            if x['alvor'] in ('fejl', 'tvivl') or x.get('bruger_skal_laese'):
                laes.append(x)
    json.dump(rk, open(sti, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    with open(os.path.join(mappe, 'laeseliste.md'), 'w', encoding='utf-8') as o:
        o.write('# Retter til gennemlæsning\n\n')
        for x in laes:
            o.write(f"## {x['navn']}  ({x['alvor']}{', bør læses' if x.get('bruger_skal_laese') else ''})\n")
            for p in x.get('problemer', []):
                o.write(f'- {p}\n')
            r = x.get('rettelse') or {}
            if r.get('fremgangsmaade'):
                o.write('Ny fremgangsmåde:\n' + ''.join(f'  {i}. {t}\n' for i, t in enumerate(r['fremgangsmaade'], 1)))
            if r.get('maengder'):
                o.write('Mængder: ' + ', '.join(f"{m['ingrediens']} → {m['maengde']:g} {m['enhed']}" for m in r['maengder']) + '\n')
            o.write('\n')
    print('fund:', antal, '| rettelser i rettelser.json:', len(rk), '| på læselisten:', len(laes))


if __name__ == '__main__':
    main()
