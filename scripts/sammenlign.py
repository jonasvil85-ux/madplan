"""Sammenligner ugens tilbud på tværs af butikker i populære kategorier (kr/kg, kr/l eller kr/stk).

Bruges til at vælge hver butiks top 3 ("værd at køre efter") ud fra data i stedet for øjemål.

Brug:  python -I scripts/sammenlign.py            (alle kategorier, 8 billigste i hver)
       python -I scripts/sammenlign.py sodavand   (kun kategorier der matcher)
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tilbud import BUTIKKER, laes_snapshot  # noqa: E402

# kategori: (regex der skal matche, regex der udelukker, enhed)
KATEGORIER = {
    'Sodavand':          (r'sodavand|coca-cola|cola\b|pepsi|faxe kondi|fanta|squash|sprite|jolly|schweppes|nestea', r'booster|monster|energy|julekalender|klasse|\bis\b|\bice\b', 'l'),
    'Øl':                (r'\bøl\b|pilsner|carlsberg|tuborg|heineken|royal export|classic', r'alkoholfri|0[,.]0|julekalender|sodavand|squash|cola|fanta', 'l'),
    'Kaffe':             (r'kaffe|merrild|gevalia|bki|lavazza|café noir|l.or\b', r'kapsl|kaffefilter|instant|nescafé|dolce|kop', 'kg'),
    'Piskefløde':        (r'piskefløde|fløde 36', r'', 'l'),
    'Smør':              (r'\bsmør\b|kærgården|lurpak', r'smørbar|smørrebrød|pålæg|flydende|lactofree|laktosefri|naturli|kærgården|becel', 'kg'),
    'Mælk':              (r'mælk\b|letmælk|minimælk|sødmælk|græsmælk', r'kokos|chokolade|kakao|drik|mælkeris|shake|lactofree|laktosefri', 'l'),
    'Æg':                (r'\bæg\b|skrabeæg|frilandsæg', r'påske|æggesalat|kinder', 'stk'),
    'Hakket oksekød':    (r'hakket.*okse|okse.*hakket', r'grise|kalv|kylling', 'kg'),
    'Hakket grisekød':   (r'hakket.*gris|gris.*hakket', r'kalv|okse', 'kg'),
    'Hakket kylling':    (r'hakket.*kylling|kylling.*hakket', r'', 'kg'),
    'Kyllingebryst':     (r'kyllingebryst|kyllingeinderfilet|brystfilet', r'pålæg|and|bbq|lage', 'kg'),
    'Hel kylling':       (r'hel kylling|hel dansk kylling|frilands kylling|frilandskylling', r'', 'kg'),
    'Kyllingelår':       (r'kyllingelår|kyllingeover|kyllingeunder|overlår', r'', 'kg'),
    'Flæskesteg/ribben': (r'flæskesteg|ribbensteg', r'tilbehør|menu|sauce', 'kg'),
    'Bacon':             (r'bacon', r'kalkun|chips|hamburger', 'kg'),
    'Laks (fersk)':      (r'laks', r'røget|gravad|snitter|pålæg|vildlaks|varmrøget', 'kg'),
    'Kartofler':         (r'kartofler', r'flødekartofler|brunede|glas|chips|gratin|pommes|duchesse|søde', 'kg'),
    'Skæreost':          (r'skæreost|danbo|havarti|riberhus|klovborg|mammen|cheasy.*ost', r'skiver|revet|smelte|yoghurt|skyr|hytteost', 'kg'),
}
OMREGN = {'g': ('kg', 1000), 'kg': ('kg', 1), 'ml': ('l', 1000), 'cl': ('l', 100), 'l': ('l', 1), 'stk': ('stk', 1)}


def stk_i_pakke(t):
    """Antal i pakken: fra Tjek (t['stk']) eller fra beskrivelsen ('24 x 33 cl')."""
    if (t.get('stk') or 1) > 1:
        return t['stk']
    m = re.search(r'(\d+)\s*[x×]\s*\d', t.get('beskrivelse') or '', re.I)
    return int(m.group(1)) if m else 1


def enhedspris(t, enhed):
    try:
        dele = [float(x) for x in str(t.get('maengde') or '').split('-')]
    except ValueError:
        return None
    if not dele or not t.get('pris'):
        return None
    maal, deler = OMREGN.get(t.get('enhed'), (None, None))
    if maal != enhed:
        return None
    mængde = sum(dele) / len(dele) / deler * stk_i_pakke(t)
    return t['pris'] / mængde if mængde else None


def main(filter_=None):
    sys.stdout.reconfigure(encoding='utf-8')
    data = laes_snapshot()
    for kat, (med, uden, enhed) in KATEGORIER.items():
        if filter_ and filter_.lower() not in kat.lower():
            continue
        fund = []
        for t in data['tilbud']:
            tekst = f"{t['navn']} {t.get('beskrivelse', '')[:60]}"
            if re.search(med, t['navn'], re.I) and not (uden and re.search(uden, tekst, re.I)):
                p = enhedspris(t, enhed)
                if p:
                    fund.append((p, t))
        fund.sort(key=lambda x: x[0])
        print(f"\n## {kat} (kr/{enhed})")
        for p, t in fund[:8]:
            print(f"  {p:8.2f}  {BUTIKKER[t['butik']]['navn']:13} {t['kort']:6} {t['pris']:>7} kr  {t['navn'][:55]}")


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
