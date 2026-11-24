"""Test af 20 %-reglen i byg_retter.py: et tilbud, hvis pakke dækker under 20 % af ingrediensens mængde, er en fejlkobling.

  python -I scripts/tests/daekning.py   (exit 1 ved fejl)
"""
import os, sys

ROD = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(ROD, 'scripts'))
sys.stdout.reconfigure(encoding='utf-8')
import byg_retter as b  # noqa: E402

def til(maengde, enhed, stk=1):
    return {'maengde': maengde, 'enhed': enhed, 'stk': stk}

def afvist(t, m, e):
    dk = b.daekning(t, m, e)
    return dk is not None and dk < b.MIN_DAEKNING

fejl, antal = [], [0]
def tjek(navn, ok):
    antal[0] += 1
    if not ok: fejl.append(navn)

# 1. Grænsen: 19 % afvises, 20 % og 21 % accepteres (500 g ingrediens)
tjek('19 % afvises', afvist(til('95', 'g'), 500, 'g'))
tjek('20 % accepteres', not afvist(til('100', 'g'), 500, 'g'))
tjek('21 % accepteres', not afvist(til('105', 'g'), 500, 'g'))
# 2. Enhedsomregning: 0,25 kg-pakke mod 2500 g (10 %) afvises; 0,5 kg mod 2500 g (20 %) accepteres; cl/l/ml
tjek('kg mod g: 10 % afvises', afvist(til('0.25', 'kg'), 2500, 'g'))
tjek('kg mod g: 20 % accepteres', not afvist(til('0.5', 'kg'), 2500, 'g'))
tjek('ml mod dl-uvist enhed: ikke sammenlignelig', b.daekning(til('250', 'ml'), 2, 'dl') is None)
tjek('l mod ml: 19 % afvises', afvist(til('0.19', 'l'), 1000, 'ml'))
# 3. Interval (650-750 g) bruger midten, og multipakke ganges med antal
tjek('interval: 700 g mod 2500 g = 28 % accepteres', not afvist(til('650-750', 'g'), 2500, 'g'))
tjek('multipakke 6 x 33 cl mod 1 l accepteres', not afvist(til('33', 'cl', 6), 1000, 'ml'))
tjek('multipakke 2 x 10 g mod 500 g afvises', afvist(til('10', 'g', 2), 500, 'g'))
# 4. Kantsager der ikke må give falsk alarm eller crash: stk mod g, mængde 0 ("efter smag"), tom/ugyldig pakkemængde, ukendt enhed
tjek('stk mod g er ikke sammenlignelig', b.daekning(til('1', 'stk'), 2500, 'g') is None)
tjek('mængde 0 (efter smag)', b.daekning(til('250', 'g'), 0, 'g') is None)
tjek('tom pakkemængde', b.daekning({'maengde': '', 'enhed': 'g'}, 500, 'g') is None)
tjek('ugyldig pakkemængde (æøå)', b.daekning({'maengde': 'æøå', 'enhed': 'g'}, 500, 'g') is None)
tjek('ukendt enhed (pakke)', b.daekning(til('1', 'pakke'), 1, 'pakke') is None)
tjek('stk mod stk: 1 mod 6 = 17 % afvises', afvist(til('1', 'stk'), 6, 'stk'))
# 5. De tre kendte fejlkoblinger: hel and 2500 g mod andebryst 250 g (10 %), laks 600 g mod 115 g (19 %)
tjek('365: hel and mod andebryst 250 g', afvist(til('250', 'g'), 2500, 'g'))
tjek('rema: laksestykke 600 g mod fintskåret laks 115 g', afvist(til('115', 'g'), 600, 'g'))
tjek('kvickly: laks 600 g mod laksefilet 600 g er fint', not afvist(til('600', 'g'), 600, 'g'))

# 6. Forbudte par (ris -> kiks): hele ord/ordslutning, æøå-sikkert, ingen falske alarmer
R101 = 'Nordthy Mini ris- eller majskiks'
tjek('ris mod riskiks afvises', b.forbudt_par('ris', R101) == ('ris', 'kiks'))
tjek('jasminris mod riskiks afvises', b.forbudt_par('jasminris', R101) is not None)
tjek('basmatiris (gule ris) mod kiks afvises', b.forbudt_par('gule ris', R101) is not None)
tjek('ris (gerne kogt dagen før) afvises', b.forbudt_par('ris (gerne kogt dagen før)', R101) is not None)
tjek('RIS med stort afvises', b.forbudt_par('RIS', 'RISKIKS 100 g') is not None)
tjek('basmatiris mod rigtig risvare accepteres', b.forbudt_par('basmatiris', 'Tilda basmatiris 1 kg') is None)
tjek('grisekød rammes ikke', b.forbudt_par('grisekød', R101) is None)
tjek('hakket gris rammes ikke', b.forbudt_par('hakket gris', 'Cheasy kiks') is None)
tjek('frilandsgris rammes ikke', b.forbudt_par('frilandsgris', R101) is None)
tjek('tomatris/risotto: risotto rammes ikke', b.forbudt_par('risottoris', R101) is not None and b.forbudt_par('risotto', R101) is None)
tjek('riskiks mod riskiks accepteres (ingrediensen er selv kiks)', b.forbudt_par('riskiks', R101) is None)
tjek('æøå i navne giver ikke crash', b.forbudt_par('ærter og løg', 'Grønne ærter åben æske') is None)
tjek('tom ingrediens', b.forbudt_par('', R101) is None)
# 7. Ingen ingrediens i den byggede retter.json er koblet til et forbudt par (tjekker de rigtige data)
import json
sti = os.path.join(ROD, 'retter.json')
if os.path.exists(sti):
    with open(sti, encoding='utf-8') as f:
        rj = json.load(f)
    for bk, bd in rj['butikker'].items():
        for r in bd['retter']:
            for i in r['ingredienser']:
                for t in i['tilbud']:
                    fp = b.forbudt_par(i['navn'], bd['tilbud'][t]['navn']) if t in bd['tilbud'] else None
                    tjek(f"{bk}: '{r['navn']}' kobler '{i['navn']}' til {t} – forbudt par", fp is None)

if fejl:
    print('DÆKNING: FEJLET – ' + '; '.join(fejl)); sys.exit(1)
print('DÆKNING: BESTÅET (20 %-reglen, ' + str(antal[0]) + ' tjek)')
