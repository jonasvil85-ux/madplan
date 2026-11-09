"""Tilføjer til retter.json og opskrifter.json de oplysninger, indkøbssedlen skal bruge for at vise den RIGTIGE vare i et tilbud med flere:
"Coop koteletter, stegeflæsk, nakkekoteletter eller filet a la mørbrad med gyros" skal stå som "nakkekoteletter", når retten skal bruge nakkekoteletter.

  tilbud[id]['vt'] = {type: [numre på de dele af overskriften, der passer til typen]}   (delene: overskriften delt ved komma og "eller", som i index.html)
  ingrediens['ty'] = [typer, ingrediensnavnet passer til]                                  (kun butikkernes egne retter; opskrifterne har allerede 'typ')

Køres automatisk sidst i byg_opskrifter.py (efter byg_retter.py). Mangler felterne, bruger siden bare ordsammenligning som før.
Brug:  python -I scripts/tilfoej_varianter.py"""
import json, os, re, sys

HER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HER)
from bibliotek_typer import TYPER  # noqa: E402
from udvid_retter import varer_i, BESKRIVELSE_EKSKL, BR, IKKE_MAD  # noqa: E402

ROD = os.path.dirname(HER)


def passer(typ, tekst):
    inkl, ekskl = TYPER[typ]
    return bool(re.search(inkl, tekst)) and not (ekskl and re.search(ekskl, tekst))


def tilbuds_vt(t):
    """{type: [delnumre]} for et tilbud (samme regler som kandidater() i udvid_retter.py)."""
    dele = varer_i(t.get('navn') or '')
    beskr = ((t.get('beskrivelse') or '').split('.')[0]).lower()
    ud = {}
    for typ in TYPER:
        if typ in BESKRIVELSE_EKSKL and re.search(BESKRIVELSE_EKSKL[typ], beskr):
            continue
        idx = [i for i, f in enumerate(dele) if not (BR.FORARBEJDET.search(f) or IKKE_MAD.search(f)) and passer(typ, f)]
        if idx:
            ud[typ] = idx
    return ud


def ingrediens_typer(navn):
    n = navn.lower()
    return [typ for typ in TYPER if passer(typ, n)]


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    sti_r, sti_o = os.path.join(ROD, 'retter.json'), os.path.join(ROD, 'opskrifter.json')
    r = json.load(open(sti_r, encoding='utf-8'))
    antal_vt = antal_ty = 0
    for b in r['butikker'].values():
        for t in b['tilbud'].values():
            vt = tilbuds_vt(t)
            if vt: t['vt'] = vt; antal_vt += 1
            else: t.pop('vt', None)
        for ret in b['retter']:
            for i in ret['ingredienser']:
                ty = ingrediens_typer(i['navn'])
                if ty: i['ty'] = ty; antal_ty += 1
                else: i.pop('ty', None)
    json.dump(r, open(sti_r, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    o = json.load(open(sti_o, encoding='utf-8'))
    antal_o = 0
    for t in o['tilbud'].values():
        vt = tilbuds_vt(t)
        if vt: t['vt'] = vt; antal_o += 1
        else: t.pop('vt', None)
    json.dump(o, open(sti_o, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print(f'varianter: {antal_vt} tilbud i retter.json, {antal_o} i opskrifter.json, {antal_ty} ingredienser med typer')


if __name__ == '__main__':
    main()
