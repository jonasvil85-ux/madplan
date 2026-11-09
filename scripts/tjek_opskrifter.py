"""Automatiske tjek af opskrifterne (retter.json + opskrifter.json): finder de grove fejl, før nogen laver maden.

Tjek:
  RAA          råt kød/fisk/kylling nævnes aldrig i et trin med tilberedning (steg/bag/kog …)
  OVN          ovn eller bagning uden temperatur ("grader")
  TID          et enkelt trin varer længere end hele retten (tid_minutter), eller tiden er meget lavere end summen af trinnene
  NAVN         retnavnet nævner en ingrediens (en vare, der findes i andre retter), som ikke står på ingredienslisten
  IKKE_BRUGT   en ingrediens (ikke basisvare) nævnes aldrig i trinnene
  TRIN_MANGLER trinnene nævner en vare, der ikke står på ingredienslisten
  MAENGDE      urealistisk mængde til 4 personer (kød, pasta/ris, kartofler, brød i stk)
  KORT         under 3 trin

Brug:  python -I scripts/tjek_opskrifter.py [--alle]     (uden --alle vises kun de alvorligste: RAA, OVN, TID, NAVN, MAENGDE)
Afslutter med kode 1, hvis der er RAA-fejl (kan bruges som sikkerhedsnet i rutinen)."""
import collections, json, os, re, sys

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAA = re.compile(r'flæskesteg|ribbensteg|kamsteg|oksesteg|svinekam|lammekølle|kylling|kalkun|hakket|kotelet|mørbrad|nakkefilet|nakkesteg|bøf|flanksteak|culotte|entrecote|'
                 r'oksekød|gullasch|andebryst|andelår|hel and|\blam(?!mefjord)|medister|spareribs|frikadelle|svinekød|svinebov|tyndsteg|torsk|laks|\bsej|rødspætte|fiskefilet|'
                 r'rejer|kalv|krondyr|fasan|ribben|flæsk|steak|schnitzel', re.I)
RAA_SKIP = re.compile(r'bouillon|fond|pålæg|røget|gravad|tun\b|dåse|sauce|sovs|kokos|pølse|bacon|skinke|roastbeef|kødsauce|chips|salat\b', re.I)
VERBUM = re.compile(r'steg|bag|bages|bagt|kog|grill|simre|brun|rist|ovn|pande|gryde|sauter|wok|damp|fritter|pochér|braiser|varm|smelt', re.I)
BASIS = re.compile(r'^(salt|sort peber|peber|vand|olie|olivenolie|rapsolie|smør|sukker|eddike|mel|hvedemel|bouillon|fond|krydderi)|salt og peber|efter smag', re.I)
STOP = {'dansk', 'græsk', 'økologiske', 'økologisk', 'ungarsk', 'spansk', 'spanske', 'italiensk', 'asiatisk', 'mexicansk', 'amerikansk', 'franske', 'med', 'og', 'fra', 'af', 'til', 'på', 'i', 'den', 'det', 'uden', 'eller', 'lun', 'lune', 'varm', 'kold', 'kolde', 'hjemmelavet', 'hjemmelavede', 'klassisk', 'bagt', 'bagte',
        'stegt', 'stegte', 'ovnbagt', 'ovnbagte', 'ovnstegt', 'ovnstegte', 'sprød', 'sprøde', 'cremet', 'cremede', 'frisk', 'friske', 'hurtig', 'nem', 'små', 'store', 'fyldte', 'fyldt'}
SYN = {'spaghetti': ['spaghetti', 'pasta'], 'wraps': ['wrap', 'tortilla'], 'remoulade': ['remoulade', 'mayonnaise'], 'svinekød': ['svinekød', 'gris', 'svine', 'hakket', 'mørbrad', 'nakke', 'kotelet'], 'flødeost': ['flødeost', 'philadelphia'], 'pasta': ['spaghetti', 'penne', 'fusilli', 'fettuccine', 'tagliatelle', 'farfalle', 'rigatoni', 'makaroni', 'lasagne', 'pasta'], 'kød': ['kød'], 'brød': ['brød', 'bolle', 'baguette', 'ciabatta', 'tortilla', 'wrap', 'pita', 'toast'],
       'kartofler': ['kartof'], 'pølser': ['pølse'], 'grønt': ['grønt', 'broccoli', 'squash'], 'suppe': ['bouillon', 'suppe'], 'sovs': ['sovs', 'sauce', 'fløde', 'mælk'], 'sauce': ['sovs', 'sauce', 'fløde'],
       'gratin': ['ost', 'fløde'], 'tærte': ['dej', 'mel'], 'pizza': ['pizza', 'dej'], 'salat': ['salat', 'agurk', 'tomat', 'rucola'], 'gryde': ['gryde'], 'wok': ['wok', 'nudler', 'ris'],
       'lasagne': ['lasagne'], 'burger': ['burger', 'bøf', 'hakket'], 'burgere': ['burger', 'bøf', 'hakket'], 'frikadeller': ['frikadelle', 'hakket', 'kød'], 'kødboller': ['hakket', 'kød', 'kødbolle'],
       'bøffer': ['bøf', 'hakket', 'okse', 'kød'], 'kyllingelår': ['kyllingelår', 'kylling'], 'grøntsager': ['grønt', 'gulerød', 'broccoli', 'squash', 'løg', 'kål', 'peber'], 'rodfrugter': ['gulerød', 'pastinak', 'selleri', 'kartof', 'rod'],
       'nudler': ['nudler', 'mie'], 'ris': ['ris'], 'omelet': ['æg'], 'æggekage': ['æg'], 'pandekager': ['mel', 'æg'], 'sandwich': ['bolle', 'brød', 'ciabatta', 'baguette']}
DUR = re.compile(r'(\d+(?:,\d+)?)(?:\s*[-–]\s*(\d+(?:,\d+)?))?\s*(minutter|min\b|timer|time\b|timers)', re.I)


def laes():
    d = json.load(open(os.path.join(ROD, 'retter.json'), encoding='utf-8'))
    o = json.load(open(os.path.join(ROD, 'opskrifter.json'), encoding='utf-8'))
    uni = {}
    for r in o['opskrifter']:
        uni.setdefault(r['navn'], (r, 'bibliotek'))
    for k, b in d['butikker'].items():
        for r in b['retter']:
            uni.setdefault(r['navn'], (r, k))
    return uni


def trinvarighed(t):
    m = DUR.search(t)
    if not m:
        return 0
    a = float(m.group(1).replace(',', '.'))
    return round(a * 60) if m.group(3).lower().startswith('time') else round(a)


def tjek(r):
    fund = []
    ings = [i for i in r['ingredienser']]
    navne = [i['navn'].lower() for i in ings]
    ingtekst = ' '.join(navne)
    trin = r['fremgangsmaade']
    tekst = ' '.join(trin).lower()
    # RAA
    for i in ings:
        n = i['navn']
        if RAA.search(n) and not RAA_SKIP.search(n):
            if not any(VERBUM.search(t) for t in trin):
                fund.append(('RAA', f"'{n}' tilberedes ikke i trinnene"))
            elif re.search(r'flæskesteg|ribbensteg|kamsteg|oksesteg|lammekølle|hel and|hel kylling|andelår', n.lower()) and not re.search(r'ovn|grader|°|gryde|pande|simre', tekst):
                fund.append(('RAA', f"'{n}' er en stor steg, men trinnene har hverken ovn, temperatur eller gryde/pande"))
    # OVN
    if re.search(r'\bovn|bag\b|bages|bagt', tekst) and not re.search(r'grader|°|\d+\s*c\b|grill', tekst):
        fund.append(('OVN', 'ovn/bagning uden temperatur'))
    # TID
    tider = [trinvarighed(t) for t in trin]
    if tider and max(tider) > r['tid_minutter'] + 5:
        fund.append(('TID', f"et trin varer {max(tider)} min, men retten er sat til {r['tid_minutter']} min"))
    elif sum(tider) > 1.6 * r['tid_minutter'] + 15:
        fund.append(('TID', f"trinnene summer til {sum(tider)} min (kan overlappe), retten er sat til {r['tid_minutter']} min"))
    # NAVN (kun varer, der findes som ingredienser i andre retter)
    for ord_ in re.findall(r'[a-zæøåA-ZÆØÅ]+', r['navn']):
        w = ord_.lower()
        if w in STOP or len(w) < 5:
            continue
        if w in VOKAB:
            kandidater = SYN.get(w, [w[:6]])
            if not any(k in ingtekst for k in kandidater) and not any(k in tekst for k in kandidater if len(k) > 4 and False):
                fund.append(('NAVN', f"navnet nævner '{w}', men det står ikke på ingredienslisten"))
    # IKKE_BRUGT
    for i in ings:
        if i.get('basisvare') or BASIS.search(i['navn']):
            continue
        ord_ = [w for w in re.findall(r'[a-zæøå]+', i['navn'].lower()) if len(w) >= 4]
        if ord_ and not any(w[:5] in tekst for w in ord_):
            fund.append(('IKKE_BRUGT', f"'{i['navn']}' nævnes ikke i trinnene"))
    # TRIN_MANGLER
    for v in sorted(VOKAB_TRIN):
        if v in tekst and v[:5] not in ingtekst and not any(v[:5] in n for n in navne):
            fund.append(('TRIN_MANGLER', f"trinnene nævner '{v}', men det står ikke på listen"))
    # MAENGDE
    kg = lambda i: i['maengde'] * (1000 if i['enhed'] == 'kg' else 1) if i['enhed'] in ('g', 'kg') else None
    koed = sum(kg(i) or 0 for i in ings if RAA.search(i['navn']) and not RAA_SKIP.search(i['navn']) and not re.search(r'hel |kylling$', i['navn'].lower()))
    if 0 < koed < 350:
        fund.append(('MAENGDE', f'kun {koed:g} g kød/fisk i alt til 4 personer'))
    if koed > 1700:
        fund.append(('MAENGDE', f'{koed:g} g kød/fisk til 4 personer er meget'))
    for i in ings:
        g = kg(i)
        n = i['navn'].lower()
        if g is None:
            if i['enhed'] == 'stk' and re.search(r'rugbrød|^brød$|franskbrød', n) and i['maengde'] >= 3:
                fund.append(('MAENGDE', f"{i['maengde']:g} stk {i['navn']} (hele brød?)"))
            continue
        if re.search(r'pasta|spaghetti|penne|fusilli|tagliatelle|nudler', n) and not (150 <= g <= 600):
            fund.append(('MAENGDE', f"{g:g} g {i['navn']} til 4 personer"))
        if re.search(r'^ris$|jasminris|basmati|grødris', n) and not (150 <= g <= 450):
            fund.append(('MAENGDE', f"{g:g} g {i['navn']} til 4 personer"))
        if re.search(r'kartof', n) and not re.search(r'søde|chips|mos', n) and not re.search(r'suppe', r['navn'].lower()) and not (400 <= g <= 1600):
            fund.append(('MAENGDE', f"{g:g} g {i['navn']} til 4 personer"))
    if len(trin) < 3:
        fund.append(('KORT', f'kun {len(trin)} trin'))
    return fund


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    global VOKAB, VOKAB_TRIN
    uni = laes()
    ordtael = collections.Counter()
    for r, _ in uni.values():
        for i in r['ingredienser']:
            for w in set(re.findall(r'[a-zæøå]{5,}', i['navn'].lower())):
                ordtael[w] += 1
    VOKAB = {w for w, n in ordtael.items() if n >= 2 and w not in STOP}
    VOKAB_TRIN = {w for w in ('flæskesteg', 'rødkål', 'agurk', 'ost', 'fløde', 'mælk', 'æg', 'kartoffel', 'løg', 'hvidløg', 'tomat', 'smør', 'ris', 'pasta', 'broccoli', 'spinat', 'creme fraiche', 'bacon', 'remoulade', 'sennep', 'ketchup', 'citron', 'avocado', 'feta', 'mozzarella', 'persille', 'purløg', 'dild')
                  if len(w) > 2}
    # korte ord, der ofte er del af andre ord, undgås i TRIN_MANGLER
    VOKAB_TRIN -= {'ost', 'æg', 'ris', 'løg', 'smør', 'tomat', 'fløde', 'mælk', 'agurk', 'dild', 'pasta'}
    alle = '--alle' in sys.argv
    gruppe = collections.defaultdict(list)
    for navn, (r, kilde) in sorted(uni.items()):
        for kode, tekst in tjek(r):
            gruppe[kode].append((navn, kilde, tekst))
    vigtige = ['RAA', 'OVN', 'TID', 'NAVN', 'MAENGDE'] + (['IKKE_BRUGT', 'TRIN_MANGLER', 'KORT'] if alle else [])
    print(f'{len(uni)} unikke retter tjekket.')
    for kode in vigtige:
        liste = gruppe.get(kode, [])
        print(f'\n== {kode}: {len(liste)}')
        for navn, kilde, tekst in liste:
            print(f'  {navn[:58]:58} [{kilde}] {tekst}')
    antal = {k: len(v) for k, v in gruppe.items()}
    print('\nI alt:', antal or 'ingen fund')
    json.dump({k: [{'navn': n, 'kilde': ki, 'tekst': t} for n, ki, t in v] for k, v in gruppe.items()},
              open(os.path.join(ROD, 'scripts', '_tjek_fund.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    sys.exit(1 if gruppe.get('RAA') else 0)


if __name__ == '__main__':
    main()
