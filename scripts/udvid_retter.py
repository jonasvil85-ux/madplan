"""Udvider en butiks retter til 50 ved at parre opskriftsbiblioteket (bibliotek.py) med butikkens tilbud.

For hver opskrift finder scriptet butikkens billigste tilbud til hver ingredienstype (bibliotek_typer.py), kasserer
retter hvor hovedingrediensen ikke er på tilbud, og vælger de bedste (flest tilbud, lavest pris pr. person), så hvert
køkken får mindst 5 retter. Valgte retter skrives ind i scripts/retter/<butik>.json med "auto": true.
Kør igen for at genskabe dem (tidligere auto-retter fjernes først).

Brug:  python -I scripts/udvid_retter.py netto [--til 50] [--min-koekken 5] [--min-tilbud 0.5] [--max-noegle 5] [--max-dansk 26]  (min. andel af retters pris der er tilbudsvarer)
       python -I scripts/udvid_retter.py alle        (alle butikker undtagen superbrugsen, som kopieres fra kvickly)
GENNEMGÅ altid udskriften: hvert tilbud skal give mening i retten (ingen sød yoghurt i suppe osv.).
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tilbud import BUTIKKER, laes_snapshot  # noqa: E402
import byg_retter as BR  # noqa: E402
from bibliotek import RETTER as BIB  # noqa: E402
from bibliotek_typer import TYPER  # noqa: E402

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RETTER_MAPPE = os.path.join(ROD, 'scripts', 'retter')
MAX_PR_KOEKKEN = {'dansk': 26}
STANDARD_MAX = 13
MAX_PR_NOEGLETILBUD = 5
MAX_VARIANTER = 4   # en opskrift kan komme i op til så mange udgaver med hver sit tilbud som nøgle-ingrediens (kun én udgave vælges)
VARIANT_PRIS = 1.8  # en udgave må koste højst så meget mere end den billigste (+ 15 kr)
NYE_TILBUD_BONUS = 0.05  # pr. tilbud, retten bruger, som ingen valgt ret bruger endnu (højst 4 tæller): flest mulige af ugens tilbud kommer i brug


# Ikke-mad (og drikkevarer), som aldrig må kobles til en ingrediens, selv om navnet ligner en madvare
IKKE_MAD = re.compile(r"test|maske|mask|collagen|shampoo|vitamin|lotion|parfume|spejl|massage|trimmer|batteri|vaskemiddel|opvask|"
                      r"toilet|legetøj|dukke|julekalender|pude|plaid|sengetøj|krus|glas|gryde|kniv|lampe|pærer|kapsel|vodka|whisky|"
                      r"gin|likør|champagne|prosecco|rødvin|hvidvin|vin|øl|pilsner|sodavand|cola|energidrik|hundemad|kattemad|"
                      r"foder|gel|creme|serum|plaster|tablet|medicin|pastel|pastis", re.I)


# Typer, hvor tilbuddets BESKRIVELSE (ikke kun navnet) afgør, om det passer (navnet er fx bare "Rana Pasta" eller "Arla Yoghurt")
# Skyr og yoghurt må kun bruges i madretter, hvis avisen UDTRYKKELIGT siger, at den er naturel/græsk/tyrkisk. Står der ingenting (fx "Cheasy skyr"), er det ofte en sødet udgave med frugt eller vanilje,
# og så er det bedre at bruge normalpris end at anbefale det forkerte produkt.
KRAEV_BESKRIVELSE = {'skyr': r'natur|græsk|tyrkisk|islandsk', 'yoghurt': r'natur|græsk|tyrkisk'}
def uden_krav(typ, t):
    """True, hvis typen kræver en bekræftelse i avisen (naturel …), og tilbuddet ikke har den."""
    return typ in KRAEV_BESKRIVELSE and not re.search(KRAEV_BESKRIVELSE[typ], ((t.get('navn') or '') + ' ' + (t.get('beskrivelse') or '')).lower())


BESKRIVELSE_EKSKL = {'yoghurt': r'pære|banan|jordbær|blåbær|vanilje|mango|fersken|skovbær|frugt', 'pasta': r'tortell|ravioli|fyldt|gnocchi'}


def varer_i(navn):
    """Alle varer i en tilbudsoverskrift: \"Grønlandske rejer, kold- eller varmrøget laks\" er både rejer og laks."""
    dele = [d.strip() for d in re.split(r'\s*,\s*|\s+eller\s+', navn.lower()) if d.strip()]
    return dele or [navn.lower()]


def kandidater(tilbud, typ):
    inkl, ekskl = TYPER[typ]
    ud = []
    for t in tilbud:
        if not t.get('pris'):
            continue
        if uden_krav(typ, t):
            continue  # skyr/yoghurt uden "naturel" i avisen kan være sødet
        if typ in BESKRIVELSE_EKSKL and re.search(BESKRIVELSE_EKSKL[typ], (t.get('beskrivelse') or '').split('.')[0].lower()):
            continue  # fx sød yoghurt (pære/banan) til naturel-yoghurt, eller fyldt pasta (tortellini) til pasta
        for f in varer_i(t['navn']):  # tilbuddet kan bruges, hvis NOGEN af varerne i overskriften passer til typen (siden viser den vare, retten bruger)
            if BR.FORARBEJDET.search(f) or IKKE_MAD.search(f):
                continue
            if re.search(inkl, f) and not (ekskl and re.search(ekskl, f)):
                ud.append(t)
                break
    return ud


def vaelg_bedste(kand, maengde, enhed):
    """Det tilbud der er billigst for det behov, retten har (hele pakker)."""
    def pris(t):
        return t['pris'] * BR.antal_pakker(t, {enhed: maengde})
    return min(kand, key=lambda t: (pris(t), t['pris']))


def lav_ret(butik, tilbud, opskrift, rang=0):
    """rang 0: nøgle-ingrediensen får butikkens billigste tilbud. rang 1, 2 …: det næstbilligste osv. (højst VARIANT_PRIS gange så dyrt),
    så en vare med mange tilbud (fx 10 andetilbud) ikke kun bruger det billigste."""
    prefix = BUTIKKER[butik]['prefix']
    ings, behov, matchet, ialt, noegler = [], {}, 0, 0, set()
    for navn, m, e, basis, typ, noegle in opskrift['ingredienser']:
        ids = []
        if typ:
            kand = kandidater(tilbud, typ)
            if kand:
                if noegle and rang:
                    pr = lambda t: t['pris'] * BR.antal_pakker(t, {e: m})
                    rk = sorted(kand, key=lambda t: (pr(t), t['pris']))
                    rk = [t for t in rk if pr(t) <= VARIANT_PRIS * pr(rk[0]) + 15]
                    if rang >= len(rk):
                        return None
                    b = rk[rang]
                else:
                    b = vaelg_bedste(kand, m, e)
                ids = [b['kort']]
                if noegle:
                    noegler.add(b['kort'])
                behov.setdefault(b['kort'], {})
                behov[b['kort']][e] = behov[b['kort']].get(e, 0) + m
            elif noegle:
                return None
        if not basis:
            ialt += 1
            matchet += 1 if ids else 0
        ings.append([navn, m, e, basis, ids])
    alle = {t['kort']: t for t in tilbud}
    pris = sum(alle[k]['pris'] * BR.antal_pakker(alle[k], bh) for k, bh in behov.items())
    oevrigt = sum(i[1] * BR.normalpris({'navn': i[0], 'enhed': i[2]}) for i in ings if not i[3] and not i[4])
    pr_person = (pris + oevrigt) / 4
    niveau = opskrift['niveau']
    if niveau == 'student' and pr_person > BR.STUDENT_LOFT_PR_PERSON:
        niveau = 'familie'
    ret = {k: opskrift[k] for k in ('navn', 'beskrivelse', 'kategori', 'koekken', 'tid_minutter', 'spis_tidligt', 'fremgangsmaade')}
    ret.update(niveau=niveau, ingredienser=ings, auto=True)
    return dict(ret=ret, andel=matchet / max(1, ialt), andel_pris=pris / max(1, pris + oevrigt), pr_person=pr_person, noegler=noegler,
                koekken=opskrift['koekken'], navn=opskrift['navn'], behov=behov)


def eksisterende(butik):
    """(navne, antal pr. køkken) for butikkens retter UDEN tidligere auto-retter."""
    fuld = {}
    for sti in os.listdir(RETTER_MAPPE):
        for r in json.load(open(os.path.join(RETTER_MAPPE, sti), encoding='utf-8'))['retter']:
            if 'som' not in r:
                fuld[r['navn']] = r
    navne, antal = set(), {k: 0 for k in BR.KOEKKENER}
    d = json.load(open(os.path.join(RETTER_MAPPE, f'{butik}.json'), encoding='utf-8'))
    for r in d['retter']:
        if r.get('auto'):
            continue
        base = fuld.get(r.get('som')) if 'som' in r else r
        navne.add(r.get('navn') or r.get('som'))
        k = r.get('koekken') or (base or {}).get('koekken')
        if k in antal:
            antal[k] += 1
    return d, navne, antal


def kor(butik, til=50, min_k=5, min_tilbud=0.5):
    data = laes_snapshot()
    tilbud = [t for t in data['tilbud'] if t['butik'] == butik]
    d, navne, antal = eksisterende(butik)
    nuvaerende = sum(antal.values())
    kandid = []
    for o in BIB:
        if o['navn'] in navne:
            continue
        for rang in range(MAX_VARIANTER):
            c = lav_ret(butik, tilbud, o, rang)
            if not c:
                break
            if c['andel_pris'] >= min_tilbud and c['andel'] >= 0.2:
                kandid.append(c)
    kandid.sort(key=lambda c: (-c['andel_pris'], c['pr_person']))
    valgt, brugt_noegle = [], {}
    brugt_tilbud = set()  # alle tilbud, de valgte retter bruger – nye retter belønnes for at bringe flere af ugens tilbud i brug

    def max_k(k):
        return MAX_PR_KOEKKEN.get(k, STANDARD_MAX)

    def antal_k(k):
        return antal[k] + sum(1 for c in valgt if c['koekken'] == k)

    def kan(c):
        return c not in valgt and all(c['navn'] != v['navn'] for v in valgt) and antal_k(c['koekken']) < max_k(c['koekken']) and \
            all(brugt_noegle.get(n, 0) < MAX_PR_NOEGLETILBUD for n in c['noegler'])

    def tag(c):
        valgt.append(c)
        brugt_tilbud.update(c['behov'])
        for n in c['noegler']:
            brugt_noegle[n] = brugt_noegle.get(n, 0) + 1

    # Fase 1: mindst min_k i hvert køkken
    while True:
        mangler = [k for k in BR.KOEKKENER if antal_k(k) < min_k and any(kan(c) and c['koekken'] == k for c in kandid)]
        if not mangler:
            break
        k = min(mangler, key=antal_k)
        tag(next(c for c in kandid if kan(c) and c['koekken'] == k))
    # Fase 2: fyld op til målet – bedste retter, men fordel køkkenerne
    while nuvaerende + len(valgt) < til:
        raest = [c for c in kandid if kan(c)]
        if not raest:
            break
        tag(min(raest, key=lambda c: (-(c['andel_pris'] - 0.03 * antal_k(c['koekken']) + NYE_TILBUD_BONUS * min(4, len(set(c['behov']) - brugt_tilbud))), c['pr_person'])))

    d['retter'] = [r for r in d['retter'] if not r.get('auto')] + [c['ret'] for c in valgt]
    open(os.path.join(RETTER_MAPPE, f'{butik}.json'), 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')

    alle = {t['kort']: t for t in tilbud}
    print(f"\n## {BUTIKKER[butik]['navn']}: {nuvaerende} eksisterende + {len(valgt)} nye = {nuvaerende + len(valgt)} "
          f"| køkkener: " + ', '.join(f'{k} {antal_k(k)}' for k in BR.KOEKKENER) + f" | kandidater: {len(kandid)}")
    for c in valgt:
        r = c['ret']
        print(f"- [{r['niveau'][:3]}/{r['koekken'][:4]}] {r['navn']} ({c['pr_person']:.0f} kr/pers, {c['andel_pris']:.0%} af prisen er tilbud)")
        print('    ' + ' | '.join(f"{i[0]} → {alle[i[4][0]]['navn'][:34]} {alle[i[4][0]]['pris']:g}kr" for i in r['ingredienser'] if i[4]))


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    args = sys.argv[1:]
    til = int(args[args.index('--til') + 1]) if '--til' in args else 50
    min_k = int(args[args.index('--min-koekken') + 1]) if '--min-koekken' in args else 5
    min_t = float(args[args.index('--min-tilbud') + 1]) if '--min-tilbud' in args else 0.5
    global MAX_PR_NOEGLETILBUD, MAX_PR_KOEKKEN
    if '--max-dansk' in args: MAX_PR_KOEKKEN = {'dansk': int(args[args.index('--max-dansk') + 1])}  # tynde aviser: flere danske retter
    if '--max-noegle' in args: MAX_PR_NOEGLETILBUD = int(args[args.index('--max-noegle') + 1])  # tynde aviser: lad ét tilbud (fx kyllingebryst) indgå i flere retter
    butikker = [a for a in args if a in BUTIKKER or a == 'alle']
    if butikker == ['alle'] or not butikker:
        butikker = [b for b in BUTIKKER if b != 'superbrugsen']
    for b in butikker:
        kor(b, til, min_k, min_t)


if __name__ == '__main__':
    main()
