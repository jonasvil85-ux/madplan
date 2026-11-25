"""Test af selve byggeren: byg_retter.py skal stoppe (exit 1, ingen retter.json), når en kobling dækker under 20 %.

Kører en KOPI af byggeren i en midlertidig mappe med en lille konstrueret kilde, så de rigtige filer
(retter.json, opskrifter.json, scripts/retter/*) aldrig røres.

  python -I scripts/tests/byggertest.py   (exit 1 ved fejl)

Rød-hold i selve testen: samme kilde med 20 %-tjekket slået fra i kopien SKAL bygge (exit 0) – ellers
måler testen ikke, at byggeren kalder tjekket.
"""
import json, os, re, shutil, subprocess, sys, tempfile

ROD = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.stdout.reconfigure(encoding='utf-8')
TJEK = 'if dk is not None and dk < MIN_DAEKNING:'

fejl = []
def tjek(navn, ok, info=''):
    if not ok:
        fejl.append(navn + (' – ' + info if info else ''))

def tilbud(kort, navn, maengde):
    return {'id': 'x' + kort, 'side': 1, 'butik': 'rema', 'navn': navn, 'beskrivelse': '', 'pris': 20, 'forPris': None,
            'stk': 1, 'maengde': maengde, 'enhed': 'g', 'billede': '', 'gyldigTil': '2099-01-01T00:00:00+0000', 'kort': kort}

def ret(navn, maengde, tid):
    return {'navn': navn, 'beskrivelse': 'Test', 'niveau': 'familie', 'koekken': 'dansk', 'kategori': 'kylling',
            'tid_minutter': 30, 'spis_tidligt': False, 'fremgangsmaade': ['Tilbered.'],
            'ingredienser': [['kyllingebryst', maengde, 'g', 0, [tid]]]}

def kor(mappe, maengde, tilbudsmaengde, uden_tjek=False):
    """Bygger en frisk sandkasse og kører byggeren; returnerer (exit, output, retter.json findes)."""
    if os.path.exists(mappe):
        shutil.rmtree(mappe)
    os.makedirs(os.path.join(mappe, 'scripts', 'retter'))
    for f in os.listdir(os.path.join(ROD, 'scripts')):
        if f.endswith('.py') or f == 'rettelser.json':
            shutil.copy(os.path.join(ROD, 'scripts', f), os.path.join(mappe, 'scripts', f))
    kopi = os.path.join(mappe, 'scripts', 'byg_retter.py')
    kode = open(kopi, encoding='utf-8').read()
    if uden_tjek:
        tjek('rød-hold kan udføres (tjekket står i byg_retter.py)', kode.count(TJEK) == 1, 'ændret tjek? opdatér TJEK i byggertest.py')
        kode = kode.replace(TJEK, 'if False:')
    open(kopi, 'w', encoding='utf-8').write(kode)
    snap = {'butikker': {'rema': {'navn': 'REMA 1000', 'logo': '', 'logo2': None, 'farve': '#014693',
                                  'aviser': [{'fast': False, 'id': 'TESTAVIS', 'navn': 'Uge 1', 'fra': '', 'til': ''}]}},
            'tilbud': [tilbud('R1', 'Kyllingebryst', tilbudsmaengde)]}
    json.dump(snap, open(os.path.join(mappe, 'scripts', 'tilbud_snapshot.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump({'avis': 'TESTAVIS', 'retter': [ret('Testret æøå', maengde, 'R1')]},
              open(os.path.join(mappe, 'scripts', 'retter', 'rema.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    p = subprocess.run([sys.executable, '-I', kopi], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=120, cwd=mappe)
    return p.returncode, p.stdout + p.stderr, os.path.exists(os.path.join(mappe, 'retter.json'))

foer = {f: (os.path.getmtime(os.path.join(ROD, f)), os.path.getsize(os.path.join(ROD, f))) for f in ('retter.json', 'opskrifter.json') if os.path.exists(os.path.join(ROD, f))}
tmp = tempfile.mkdtemp(prefix='byggertest-')
try:
    m = os.path.join(tmp, 'sandkasse')
    # 1. Kontrol af kilden: fuld dækning (500 g mod 500 g) bygger, og retter.json skrives
    kode, ud, skrevet = kor(m, 500, '500')
    tjek('fuld dækning bygger (exit 0)', kode == 0, ud[-300:])
    tjek('fuld dækning skriver retter.json', skrevet)
    # 2. 10 % dækning (500 g mod 50 g) skal stoppe: exit 1, fejlteksten nævner dækningen, ingen retter.json
    kode, ud, skrevet = kor(m, 500, '50')
    tjek('10 % dækning giver exit 1', kode == 1, f'exit {kode}: {ud[-200:]}')
    tjek('fejlteksten nævner 10 % og 20 %', bool(re.search(r'dækker 10 % \(under 20 %\)', ud)), ud[-300:])
    tjek('10 % dækning skriver ingen retter.json', not skrevet)
    # 3. Grænsen: 19 % stopper, 20 % bygger
    tjek('19 % stopper', kor(m, 500, '95')[0] == 1)
    tjek('20 % bygger', kor(m, 500, '100')[0] == 0)
    # 4. Rød-hold: uden tjekket i kopien bygger 10 %-koblingen – beviser, at tjekket er det, der stopper bygget
    kode, ud, skrevet = kor(m, 500, '50', uden_tjek=True)
    tjek('rød-hold: uden tjek bygges 10 % (exit 0)', kode == 0, ud[-200:])
    tjek('rød-hold: uden tjek skrives retter.json', skrevet)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# 5. De rigtige filer er urørte
for f, (mt, sz) in foer.items():
    nu = os.path.join(ROD, f)
    tjek(f'{f} urørt', os.path.getmtime(nu) == mt and os.path.getsize(nu) == sz)

if fejl:
    print('FEJL i byggertest:\n- ' + '\n- '.join(fejl))
    sys.exit(1)
print('byggertest bestået (10 % stopper bygget, 20 % bygger, rød-hold virker, retter.json urørt)')
