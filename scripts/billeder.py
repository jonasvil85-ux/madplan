"""Lav illustrationsbilleder til retterne med Cloudflare Workers AI (Flux Schnell, gratis grænse pr. dag).

Brug:  python -I scripts/billeder.py            (alle retter i retter.json der mangler billede)
       python -I scripts/billeder.py --maks 20  (højst 20 nye billeder i denne kørsel)
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
STIL = ('Appetizing food photography of homemade Danish home cooking, served on a plate, natural daylight, '
        'rustic table, realistic, high detail, no text')


def slug(navn):
    s = navn.lower().replace('æ', 'ae').replace('ø', 'oe').replace('å', 'aa')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')[:90]


def sti(navn):
    return os.path.join(MAPPE, slug(navn) + '.jpg')


def prompt(r):
    hoved = [i['navn'] for i in r['ingredienser'] if not i.get('basisvare')][:5]
    return f"{r['navn']}. Main ingredients: {', '.join(hoved)}. {STIL}"


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
    maks = int(sys.argv[sys.argv.index('--maks') + 1]) if '--maks' in sys.argv else 10 ** 6
    d = json.load(open(os.path.join(ROD, 'retter.json'), encoding='utf-8'))
    unikke = {}
    for b in d['butikker'].values():
        for r in b['retter']:
            unikke.setdefault(r['navn'], r)
    mangler = [r for n, r in unikke.items() if not os.path.exists(sti(n))][:maks]
    print(f'{len(unikke)} forskellige retter, {len(unikke) - len([n for n in unikke if not os.path.exists(sti(n))])} har billede, laver {len(mangler)} nye')
    stop = {'graense': False}
    lavet = fejl = 0

    def arbejd(r):
        if stop['graense']:
            return None
        try:
            lav(r['navn'], prompt(r), nøgle)
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
