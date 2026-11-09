"""Bygger retter.json (det siden viser) ud fra scripts/retter/<butik>.json + ugens tilbud.

Ugentlig rutine (pr. butik, når dens avis skifter):
  1. python -I scripts/tilbud.py <butik> > tilbud.txt   (henter avisen og viser tilbud med id'er)
  2. Skriv scripts/retter/<butik>.json                   (30 retter, kun den avis' tilbuds-id'er)
  3. python -I scripts/byg_retter.py                     (validerer og skriver retter.json)
  4. git commit + push  -> Vercel deployer automatisk

Format for scripts/retter/<butik>.json:
  {"avis": "<katalog-id>", "retter": [ <ret>, ... ]}
  <ret> er enten en fuld opskrift:
    {"navn", "beskrivelse", "niveau", "kategori", "tid_minutter", "spis_tidligt",
     "ingredienser": [[navn, mængde (4 pers.), enhed, basisvare 0/1, [tilbuds-id'er]], ...],
     "fremgangsmaade": [...]}
  eller en genbrugt opskrift fra en anden butiks fil:
    {"som": "<navn på opskrift>", "tilbud": {"<ingrediensnavn>": ["R12"], ...}}
    Værdien kan også være {"tilbud": [...], "navn": "nyt navn", "maengde": 500, "enhed": "g"} for at tilpasse
    ingrediensen. Øvrige felter (fx "niveau", "beskrivelse") overskriver opskriftens.
"""
import copy, glob, json, math, os, re, sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tilbud import BUTIKKER, SNAPSHOT  # noqa: E402
from billeder import slug  # noqa: E402

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FELTER = ['navn', 'maengde', 'enhed', 'basisvare', 'tilbud']
NIVEAUER = {'student', 'familie', 'weekend'}
KOEKKENER = ['dansk', 'italiensk', 'amerikansk', 'asiatisk', 'middelhav', 'vegetar']
MIN_PR_KOEKKEN = 4
# FÆRDIGVARER – tre niveauer:
#  1) Altid OK: basale halvfabrikata (rødkål/rødbeder på glas, bouillon, ketchup/sennep/remoulade, pasta, ris, brød, wraps,
#     pizzadej, pesto og pastasauce på glas, konserves, frosne grøntsager, rå kebab-/gullaschkød osv.)
#  2) I ny og næ (SJAELDEN): frysepizza, paneret fisk/schnitzel, pommes frites – højst MAX_SJAELDEN retter pr. butik
#  3) Aldrig (FORARBEJDET): ultra-forarbejdede færdigretter og færdigt tilbehør – fx færdige kødboller i karry, lasagne,
#     middagsretter, nuggets, dinner kits, kopsupper, færdige flødekartofler/gratin, laktosefri, smørbart, plantebaseret
FORARBEJDET = re.compile(
    r'færdigret|middagsret|dinner kit|kopsuppe|cup a soup|snackpot|instant|nuggets|cordon|minischnitzel|schnitzelmaker|'
    r'forårsruller|spring rolls|fyldt pasta|tex ?mex(?![ -]*tortilla)|kødboller|melboller|frikadeller|lasagne|moussaka|gryderet|boller i karry|'
    r'komplet suppe|specialsuppe|hamburger|færdig|'
    r'flødekartofler|brunede kartofler|kartoffelgratin|duchesse|glaskartofler|kartofler i glas|kålsalat|'
    r'æbleskiver|risalamande|confit|smørrebrød|menu|mortensaften|andesauce|kyllingemarked|wok-?mix|indbagt|kebabbrød|toast|wienerbrød|tærte(?!dej)|'
    r'lactofree|laktosefri|smørbar|naturli|margarine|^kærgården', re.I)
SJAELDEN = re.compile(r'panering|paneret|ristorante|rustica|surdejspizza|italiensk.*pizza|grande pizza|pizzatopping|pizza|pommes', re.I)
MAX_SJAELDEN = 2  # retter pr. butik med frysepizza, paneret fisk eller pommes frites
OMREGN = {'g': ('g', 1), 'kg': ('g', 1000), 'ml': ('ml', 1), 'cl': ('ml', 10), 'l': ('ml', 1000), 'stk': ('stk', 1)}
# Groft skøn (kr pr. enhed) for ingredienser der IKKE er på tilbud, så retter med få tilbudsvarer
# ikke ser kunstigt billige ud i prissammenligningen. Basisvarer (salt, olie, mel …) tælles ikke.
# Mere præcise skøn for almindelige varer (nøgleord i ingrediensnavnet -> kr pr. enhed)
NORMALPRIS_VARE = [
    (r'syltede', {'g': 0.04}),  # syltede rødbeder/agurker på glas
    (r'kartof', {'g': 0.015}), (r'gulerød|pastinak|rødbede', {'g': 0.015, 'stk': 1.5}),
    (r'hvidløg', {'fed': 0.8, 'stk': 5}), (r'skalotte|løg\b', {'stk': 2}),
    (r'\bæg\b', {'stk': 2.5}), (r'mælk', {'ml': 0.013}), (r'fløde|creme fraiche', {'ml': 0.04, 'g': 0.05}),
    (r'citron|lime', {'stk': 4}), (r'agurk', {'stk': 9}), (r'porre', {'stk': 6}), (r'rødkål|hvidkål|spidskål', {'stk': 15}),
    (r'ærter|bønner', {'g': 0.03, 'dåse': 8}), (r'champignon|svampe', {'g': 0.06}), (r'pasta|spaghetti|lasagne', {'g': 0.02}),
    (r'\bris\b|jasminris', {'g': 0.025}), (r'rasp|hvedemel', {'g': 0.02}), (r'salat', {'stk': 12}),
    (r'ingefær', {'g': 0.06}), (r'dild|persille|purløg|rosmarin|timian|koriander|estragon', {'bundt': 12}),
]
NORMALPRIS = {'g': 0.06, 'ml': 0.025, 'dl': 2.5, 'stk': 6, 'dåse': 9, 'glas': 14, 'pakke': 20, 'bundt': 15,
              'fed': 1, 'spsk': 2, 'tsk': 1, 'efter smag': 0}


def normalpris(ing):
    """Skønnet pris pr. enhed for en ingrediens der ikke er på tilbud."""
    for moenster, priser in NORMALPRIS_VARE:
        if re.search(moenster, ing['navn'], re.I) and ing['enhed'] in priser:
            return priser[ing['enhed']]
    return NORMALPRIS.get(ing['enhed'], 5)


def enhedspris(t):
    """'76,67 kr/kg', '6,67 kr/l' eller '1,80 kr/stk' ud fra pris og (midten af) mængde."""
    try:
        dele = [float(x) for x in str(t.get('maengde') or '').split('-')]
        str_ = sum(dele) / len(dele)
    except ValueError:
        return None
    enhed, gange = OMREGN.get(t.get('enhed'), (None, None))
    if not str_ or not enhed or not t.get('pris'):
        return None
    str_ *= t.get('stk') or 1  # multipakker: mængden er pr. stk (fx 33 cl pr. dåse)
    if enhed == 'stk':
        if str_ <= 1:
            return None
        pris, label = t['pris'] / str_, 'stk'
    else:
        pris, label = t['pris'] / (str_ * gange) * 1000, 'kg' if enhed == 'g' else 'l'
    return f"{pris:.2f}".replace('.', ',') + f" kr/{label}"


STUDENT_LOFT_PR_PERSON = 35  # kr pr. person (indkøb) – Studentermad over dette giver en advarsel


def forbrugs_andel(t, behov):
    """Hvor stor en del af EN pakke retten bruger (0-1+). Bruges til forbrugspris = det retten reelt bruger."""
    try:
        dele = [float(x) for x in str(t.get('maengde') or '').split('-')]
        stoerrelse = sum(dele) / len(dele)
    except ValueError:
        return float(antal_pakker(t, behov))
    enhed, gange = OMREGN.get(t.get('enhed'), (None, None))
    andele = [behov.get('dåse', 0) + behov.get('glas', 0) + behov.get('pakke', 0)]
    if stoerrelse and enhed and behov.get(enhed):
        andele.append(behov[enhed] / (stoerrelse * gange))
    return max(max(andele), 0.05)


def antal_pakker(t, behov):
    """Samme logik som antalPakker() i index.html."""
    try:
        # Interval (fx "100-400 g" i "rejer eller fiskefileter") -> brug midten
        dele = [float(x) for x in str(t.get('maengde') or '').split('-')]
        stoerrelse = sum(dele) / len(dele)
    except ValueError:
        stoerrelse = 0
    enhed, gange = OMREGN.get(t.get('enhed'), (None, None))
    n = math.ceil(behov.get('dåse', 0) + behov.get('glas', 0) + behov.get('pakke', 0))
    if stoerrelse and enhed and behov.get(enhed):
        n = max(n, math.ceil(behov[enhed] / (stoerrelse * gange) - 0.15))  # samme 15 % tolerance som index.html
    return max(1, n)


def laes_kilder():
    kilder = {}
    for sti in sorted(glob.glob(os.path.join(ROD, 'scripts', 'retter', '*.json'))):
        butik = os.path.splitext(os.path.basename(sti))[0]
        with open(sti, encoding='utf-8') as f:
            kilder[butik] = json.load(f)
    return kilder


def udfold(r, bibliotek, fejl, butik):
    """Gør en "som"-reference til en fuld opskrift med denne butiks tilbud."""
    if 'som' not in r:
        return r
    if r['som'] not in bibliotek:
        fejl.append(f"{butik}: 'som' peger på ukendt opskrift '{r['som']}'")
        return None
    ret = copy.deepcopy(bibliotek[r['som']])
    tilpas = r.get('tilbud', {})
    navne = {ing[0] for ing in ret['ingredienser']}
    for navn in tilpas:
        if navn not in navne:
            fejl.append(f"{butik}: '{r['som']}' har ingen ingrediens '{navn}'")
    for ing in ret['ingredienser']:
        v = tilpas.get(ing[0], [])
        if isinstance(v, dict):
            ing[0] = v.get('navn', ing[0])
            ing[1] = v.get('maengde', ing[1])
            ing[2] = v.get('enhed', ing[2])
            v = v.get('tilbud', [])
        ing[4] = v
    # "erstat": {"hvidkål": "gulerødder"} retter ordene i fremgangsmåde og beskrivelse,
    # når en ingrediens er skiftet ud (store/små forbogstaver bevares)
    def erstat(tekst):
        for gammel, ny in r.get('erstat', {}).items():
            # Stort forbogstav kun i starten af en sætning
            tekst = re.sub(re.escape(gammel),
                           lambda m: ny[0].upper() + ny[1:] if (m.start() == 0 or m.string[:m.start()].rstrip().endswith('.')) else ny,
                           tekst, flags=re.I)
        return tekst
    ret['fremgangsmaade'] = [erstat(t) for t in ret['fremgangsmaade']]
    ret['beskrivelse'] = erstat(ret['beskrivelse'])
    ret.update({k: v for k, v in r.items() if k not in ('som', 'tilbud', 'erstat')})

    # Advar hvis en udskiftet ingrediens stadig nævnes i fremgangsmåden
    tekst = ' '.join(ret['fremgangsmaade']).lower()
    originale = {ing[0]: ing for ing in bibliotek[r['som']]['ingredienser']}
    for gammel, v in tilpas.items():
        if isinstance(v, dict) and 'navn' in v and gammel in originale:
            ord_ = [o for o in re.findall(r'[a-zæøå]{4,}', gammel.lower()) if o not in v['navn'].lower()
                    and o not in ('økologisk', 'økologiske', 'dansk', 'danske', 'frisk', 'ferske', 'fersk')]
            for o in ord_:
                if any(o.startswith(a) and b in v['navn'].lower() for a, b in SYNONYMER):
                    continue
                stamme = o[:-2] if len(o) > 6 else o
                if stamme in tekst:
                    advarsler.append(f"{butik}: '{ret['navn']}' – '{gammel}' er skiftet til '{v['navn']}', men '{o}' står stadig i fremgangsmåden (brug \"erstat\")")
                    break
    return ret


advarsler = []
rest_tips = []
# Udskiftninger der betyder det samme, så der ikke advares (gammelt ord, ord i det nye navn)
SYNONYMER = [('smør', 'kærgården'), ('smør', 'smør'), ('græskar', 'hokkaido'), ('burger', 'oksekød'),
             ('hakkede', 'tomater'), ('madlavningsjævner', 'madlavningsjævner')]


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    kilder = laes_kilder()
    # Brug det gemte øjebliksbillede – Tjeks rækkefølge (og dermed id'erne) skifter mellem kald
    with open(SNAPSHOT, encoding='utf-8') as f:
        data = json.load(f)
    alle = {t['kort']: t for t in data['tilbud']}
    fejl, ud = [], {}
    bibliotek = {r['navn']: r for k in kilder.values() for r in k['retter'] if 'som' not in r}
    # Faste skabeloner (originale ingrediensnavne), så "som"-henvisninger ikke brydes, når en butiks retter skiftes ud
    skab = os.path.join(ROD, 'scripts', 'retter_skabeloner.json')
    if os.path.exists(skab):
        with open(skab, encoding='utf-8') as f:
            bibliotek.update({r['navn']: r for r in json.load(f)})

    for butik, b in BUTIKKER.items():
        if butik not in kilder:
            continue
        info = data['butikker'].get(butik)
        if not info:
            fejl.append(f"{butik}: ingen tilbud i øjebliksbilledet – kør scripts/tilbud.py {butik}")
            continue
        avis_ids = [a['id'] for a in info['aviser']]
        if kilder[butik]['avis'] not in avis_ids:
            fejl.append(f"{butik}: retterne er lavet til avis {kilder[butik]['avis']}, men øjebliksbilledet har {avis_ids}")
            continue
        retter, brugte, navne = [], {}, set()
        sjaeldne = set()
        for nr, kilderet in enumerate(kilder[butik]['retter'], 1):
            r = udfold(kilderet, bibliotek, fejl, butik)
            if r is None:
                continue
            if r.get('koekken') not in KOEKKENER:
                fejl.append(f"{r['navn']}: mangler køkken ({KOEKKENER})")
            if r['niveau'] not in NIVEAUER:
                fejl.append(f"{r['navn']}: ukendt niveau {r['niveau']}")
            if r['navn'] in navne:
                fejl.append(f"{butik}: '{r['navn']}' findes to gange")
            navne.add(r['navn'])
            ingredienser, behov = [], {}
            for ing in r['ingredienser']:
                d = dict(zip(FELTER, ing))
                d['basisvare'] = bool(d['basisvare'])
                for tid in d['tilbud']:
                    if not tid.startswith(b['prefix']) or tid not in alle:
                        fejl.append(f"{butik}: '{r['navn']}' bruger ugyldigt tilbuds-id {tid}")
                d['tilbud'] = [t for t in d['tilbud'] if t.startswith(b['prefix']) and t in alle]
                for t in d['tilbud']:
                    alt = [a.strip() for a in re.split(r'\s*,\s*| eller ', alle[t]['navn']) if a.strip()] or [alle[t]['navn']]
                    if all(FORARBEJDET.search(a) for a in alt):  # først når ALLE varer i tilbuddet er færdigvarer (et tilbud kan have flere varer; retten bruger én af dem)
                        fejl.append(f"{butik}: '{r['navn']}' bruger færdigvare {t} ({alle[t]['navn'][:40]})")
                    if all(SJAELDEN.search(a) for a in alt):
                        sjaeldne.add(r['navn'])
                if d['tilbud']:
                    t = d['tilbud'][0]
                    brugte[t] = alle[t]
                    behov.setdefault(t, {})
                    behov[t][d['enhed']] = behov[t].get(d['enhed'], 0) + d['maengde']
                ingredienser.append(d)
            pris = sum(alle[t]['pris'] * antal_pakker(alle[t], bh) for t, bh in behov.items())
            ikke_basis = [i for i in ingredienser if not i['basisvare']]
            oevrigt = sum(i['maengde'] * normalpris(i) for i in ikke_basis if not i['tilbud'])
            forbrug = sum(alle[t]['pris'] * forbrugs_andel(alle[t], bh) for t, bh in behov.items()) + oevrigt
            if r['niveau'] == 'student' and (pris + oevrigt) / 4 > STUDENT_LOFT_PR_PERSON:
                advarsler.append(f"{butik}: Studentermad '{r['navn']}' koster ca. {round((pris + oevrigt) / 4)} kr/pers. (loft {STUDENT_LOFT_PR_PERSON}) – gør den billigere eller flyt til Familiemad")
            andel = sum(1 for i in ikke_basis if i['tilbud']) / max(1, len(ikke_basis))
            if not behov:
                fejl.append(f"{butik}: '{r['navn']}' har ingen tilbudsvarer")
            billede = f"billeder/{slug(r['navn'])}.jpg"
            if os.path.exists(os.path.join(ROD, billede)):
                r = {**r, 'billede': billede}
            retter.append({**r, 'id': f'{butik}-{nr}', 'ingredienser': ingredienser,
                           'pris_tilbud': round(pris, 2), 'pris_oevrigt': round(oevrigt, 2),
                           'pris_i_alt': round(pris + oevrigt, 2), 'pris_forbrug': round(forbrug, 2),
                           'andel_tilbud': round(andel, 2)})
        if len(sjaeldne) > MAX_SJAELDEN:
            advarsler.append(f"{butik}: {len(sjaeldne)} retter bruger frysepizza/paneret/pommes (højst {MAX_SJAELDEN} 'i ny og næ'): {', '.join(sorted(sjaeldne))}")
        # Rest-tip: store pakker (efter 4 personers behov bliver >=30 % tilbage) som kun få retter bruger,
        # så brugeren ikke kan bruge resten i en anden ret
        brug = {}
        for r in retter:
            for i in r['ingredienser']:
                if i['tilbud'][:1] and not i['basisvare']:
                    o = alle[i['tilbud'][0]]
                    try:
                        dele = [float(x) for x in str(o.get('maengde') or '').split('-')]
                    except ValueError:
                        continue
                    grund, gange = OMREGN.get(o.get('enhed'), (None, None))
                    if grund and OMREGN.get(i['enhed'], (None,))[0] == grund and (sum(dele) / len(dele)):
                        pakke = sum(dele) / len(dele) * gange * (o.get('stk') or 1)
                        brug.setdefault(i['tilbud'][0], {'pakke': pakke, 'enhed': grund, 'retter': []})['retter'].append(
                            (r['navn'], i['maengde'] * OMREGN[i['enhed']][1]))
        for k, v in brug.items():
            behov = sorted(m for _, m in v['retter'])
            stoerste = behov[-1]
            # findes der to forskellige retter, der TILSAMMEN passer til én pakke (+15 %)?
            par = any(behov[x] + behov[y] <= v['pakke'] * 1.15 for x in range(len(behov)) for y in range(x + 1, len(behov)))
            if v['pakke'] - stoerste >= 0.3 * v['pakke'] and not par and alle[k]['pris'] >= 30:
                brugt = ', '.join(f"'{n[:28]}' {m:g}" for n, m in v['retter'])
                rest_tips.append(f"{info['navn']}: {alle[k]['navn'][:40]} ({alle[k]['pris']:g} kr, {v['pakke']:g} {v['enhed']}) – ingen to retter passer til én pakke. Bruges af: {brugt} {v['enhed']}")

        # Ugens 3 bedste tilbud ("værd at køre efter") – vælges i hånden i butikkens fil
        top = []
        for t in kilder[butik].get('top', []):
            o = alle.get(t['id'])
            if not o or not t['id'].startswith(b['prefix']):
                fejl.append(f"{butik}: top bruger ugyldigt tilbuds-id {t['id']}")
                continue
            top.append({'navn': o['navn'], 'pris': o['pris'], 'maengde': o['maengde'], 'enhed': o['enhed'],
                         'billede': o['billede'], 'enhedspris': t.get('enhedspris', enhedspris(o)), 'hvorfor': t['hvorfor']})
        ud[butik] = {**info, 'top': top, 'retter': retter, 'tilbud': brugte}

        antal_k = {k: sum(1 for r in retter if r.get('koekken') == k) for k in KOEKKENER}
        mangler_k = [f"{k} ({n})" for k, n in antal_k.items() if n < MIN_PR_KOEKKEN]
        if mangler_k:
            rest_tips.append(f"{info['navn']}: for få retter i køkken (min {MIN_PR_KOEKKEN}): {', '.join(mangler_k)}")
        print(f"\n{info['navn']}: {len(retter)} retter, {len(brugte)} forskellige tilbudsvarer, "
              f"gns. {round(sum(r['andel_tilbud'] for r in retter) / max(1, len(retter)) * 100)}% tilbud")
        print('  køkkener: ' + ', '.join(f'{k} {n}' for k, n in antal_k.items()))
        for niv in ('student', 'familie', 'weekend'):
            rr = [r for r in retter if r['niveau'] == niv]
            print(f"  {niv:8} {len(rr):2} retter")
            for r in rr:
                print(f"    {r['pris_i_alt']:7.2f} kr (tilbud {r['pris_tilbud']:6.2f})  {round(r['andel_tilbud'] * 100):3d}% tilbud  {r['navn']}")

    if rest_tips:
        print(f'\nREST-TIP ({len(rest_tips)}): store tilbudspakker, hvor ingen to retter tilsammen passer til én pakke – tilføj en lille ret:\n- ' + '\n- '.join(rest_tips))
    if advarsler:
        print('\nADVARSLER:\n- ' + '\n- '.join(advarsler))
    if fejl:
        print('\nFEJL:\n- ' + '\n- '.join(fejl))
        sys.exit(1)

    with open(os.path.join(ROD, 'retter.json'), 'w', encoding='utf-8') as f:
        json.dump({'genereret': datetime.now(timezone.utc).isoformat(timespec='seconds'), 'butikker': ud},
                  f, ensure_ascii=False, separators=(',', ':'))
    print(f"\nretter.json skrevet ({os.path.getsize(os.path.join(ROD, 'retter.json')) // 1024} KB)")


if __name__ == '__main__':
    main()
