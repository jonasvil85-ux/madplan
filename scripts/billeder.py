"""Lav illustrationsbilleder til retterne med Cloudflare Workers AI (Flux Schnell, gratis grænse pr. dag).

Brug:  python -I scripts/billeder.py            (retter i retter.json der mangler billede – højst 60 pr. kørsel som standard)
       python -I scripts/billeder.py --maks 20  (højst 20 nye billeder i denne kørsel)
       python -I scripts/billeder.py --koekken dansk --maks 130 [--aeldre-end "2026-11-05 14:00"]  (lav alle retter i et køkken om med den nye stil)
Kræver miljøvariablen CLOUDFLARE_API_TOKEN (nøgle med Workers AI-adgang) – den må ikke stå i koden eller sendes i chatten.
Billeder gemmes som billeder/<navn-som-slug>.jpg (720×540, ca. 50 KB). Eksisterende billeder genbruges, så kørslen kan
gentages: den stopper pænt, når dagens gratis grænse er nået, og fortsætter næste dag.
Kør derefter scripts/byg_retter.py, som sætter feltet "billede" på de retter der har et billede.
"""
import base64, io, json, os, re, sys, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPPE = os.path.join(ROD, 'billeder')
KONTO = os.environ.get('CLOUDFLARE_ACCOUNT_ID', '38253a60db8406866eb2a255247002d5')
MODEL = '@cf/black-forest-labs/flux-1-schnell'
# Stilen er neutral: beskrivelsen af retten angiver selv kar, tilbehør og køkken (fad, tallerken, skål, dansk, asiatisk …)
STIL = 'Appetizing food photography, freshly cooked homemade dish, natural daylight, rustic table, realistic, high detail, no text'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from billedstil import byg_prompt  # noqa: E402
BESKRIVELSER = os.path.join(ROD, 'scripts', 'billedprompts.json')  # {rettens navn: engelsk beskrivelse af den færdige ret}


def beskrivelser():
    if os.path.exists(BESKRIVELSER):
        return json.load(open(BESKRIVELSER, encoding='utf-8'))
    return {}


def slug(navn):
    s = navn.lower().replace('æ', 'ae').replace('ø', 'oe').replace('å', 'aa')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')[:90]


def sti(navn):
    return os.path.join(MAPPE, slug(navn) + '.jpg')


def prompt(r, besk=None):
    """Faglig beskrivelse af retten (billedstil.py: hvordan fx stegt flæsk, medister og frikadeller ser ud) + køkkenstil + nordisk fotostil.
    Uden beskrivelse bruges retnavn + hovedingredienser, men det giver oftere skæve billeder."""
    if besk and r['navn'] in besk:
        return byg_prompt(r['navn'], r.get('koekken'), besk[r['navn']])
    hoved = [i['navn'] for i in r['ingredienser'] if not i.get('basisvare')][:5]
    return byg_prompt(r['navn'], r.get('koekken'), f"{r['navn']}. Main ingredients: {', '.join(hoved)}")


class GraenseNaaet(Exception):
    pass


def lav(navn, tekst, nøgle):
    req = urllib.request.Request(
        f'https://api.cloudflare.com/client/v4/accounts/{KONTO}/ai/run/{MODEL}',
        data=json.dumps({'prompt': tekst, 'steps': 6}).encode(),
        headers={'Authorization': 'Bearer ' + nøgle, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        besked = e.read().decode(errors='replace')
        if e.code == 429 or '4006' in besked or 'daily' in besked.lower() or 'allocation' in besked.lower():
            raise GraenseNaaet(besked[:200])
        raise RuntimeError(f'HTTP {e.code}: {besked[:200]}')
    if not d.get('success'):
        raise RuntimeError(json.dumps(d.get('errors'))[:200])
    from PIL import Image
    img = Image.open(io.BytesIO(base64.b64decode(d['result']['image']))).convert('RGB')
    b, h = img.size
    ny_h = int(b * 3 / 4)  # beskær til 4:3 fra midten
    top = max(0, (h - ny_h) // 2)
    img = img.crop((0, top, b, top + ny_h)).resize((720, 540), Image.LANCZOS)
    os.makedirs(MAPPE, exist_ok=True)
    img.save(sti(navn), 'JPEG', quality=78, optimize=True, progressive=True)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    nøgle = os.environ.get('CLOUDFLARE_API_TOKEN', '')
    if not nøgle:
        sys.exit('Mangler miljøvariablen CLOUDFLARE_API_TOKEN')
    # Sikkerhedsgrænse mod uventet forbrug: højst 60 nye billeder pr. kørsel, medmindre --maks er angivet (bevidst valg)
    maks = int(sys.argv[sys.argv.index('--maks') + 1]) if '--maks' in sys.argv else 60
    forfra = '--forfra' in sys.argv  # lav alle billeder om (også dem der findes)
    kun = [x.strip().lower() for x in sys.argv[sys.argv.index('--kun') + 1].split(';')] if '--kun' in sys.argv else None  # kun retter hvis navn indeholder en af disse tekster (laves altid forfra)
    koekken = sys.argv[sys.argv.index('--koekken') + 1].lower() if '--koekken' in sys.argv else None  # lav alle retter i dette køkken om
    aeldre = None
    if '--aeldre-end' in sys.argv:  # kun billeder, der er ældre end dette tidspunkt (ÅÅÅÅ-MM-DD TT:MM) – så en afbrudt kørsel kan genoptages
        import datetime
        aeldre = datetime.datetime.fromisoformat(sys.argv[sys.argv.index('--aeldre-end') + 1]).timestamp()
    besk = beskrivelser()
    d = json.load(open(os.path.join(ROD, 'retter.json'), encoding='utf-8'))
    unikke = {}
    for b in d['butikker'].values():
        for r in b['retter']:
            unikke.setdefault(r['navn'], r)
    opskr = os.path.join(ROD, 'opskrifter.json')  # biblioteksopskrifterne (kan vælges i madplanen, også selv om ingen butik har dem som egen ret)
    if os.path.exists(opskr):
        for r in json.load(open(opskr, encoding='utf-8'))['opskrifter']:
            unikke.setdefault(r['navn'], r)
    def skal_laves(n, r):
        if koekken:
            return r.get('koekken') == koekken and (aeldre is None or not os.path.exists(sti(n)) or os.path.getmtime(sti(n)) < aeldre)
        if kun:
            return any(k in n.lower() for k in kun)
        return forfra or not os.path.exists(sti(n))
    mangler = [r for n, r in unikke.items() if skal_laves(n, r)][:maks]
    uden = [n for n in unikke if n not in besk]
    if uden:
        print(f'ADVARSEL: {len(uden)} retter mangler beskrivelse i scripts/billedprompts.json (billedet bliver dårligere): ' + '; '.join(uden[:8]))
    print(f'{len(unikke)} forskellige retter, {len(unikke) - len([n for n in unikke if not os.path.exists(sti(n))])} har billede, laver {len(mangler)} nye')
    stop = {'graense': False}
    lavet = fejl = 0

    def arbejd(r):
        if stop['graense']:
            return None
        try:
            lav(r['navn'], prompt(r, besk), nøgle)
            return 'ok'
        except GraenseNaaet as e:
            stop['graense'] = True
            return 'graense: ' + str(e)
        except Exception as e:
            return 'fejl: ' + str(e)

    with ThreadPoolExecutor(3) as ex:
        for r, res in zip(mangler, ex.map(arbejd, mangler)):
            if res == 'ok':
                lavet += 1
                print(f'  ✓ {r["navn"]}')
            elif res and res.startswith('graense'):
                print(f'  Dagens gratis grænse er nået – stopper. ({res[8:]})')
            elif res:
                fejl += 1
                print(f'  ✗ {r["navn"]}: {res}')
    print(f'Færdig: {lavet} nye billeder, {fejl} fejl. {"Kør igen i morgen for resten." if stop["graense"] else ""}')


if __name__ == '__main__':
    main()
