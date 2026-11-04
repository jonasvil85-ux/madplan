"""Laver stemningsbilleder til siden (toppen og prisniveau-kortene) med Cloudflare Workers AI (Flux Schnell).

Brug:  python -I scripts/grafik.py [navn ...]     (uden navne laves alle; findes billedet allerede, springes det over medmindre --forfra)
Kræver miljøvariablen CLOUDFLARE_API_TOKEN. Billederne gemmes som grafik/<navn>.jpg (800×800, ca. 60-90 KB).
"""
import base64, io, json, os, sys, urllib.error, urllib.request

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPPE = os.path.join(ROD, 'grafik')
KONTO = os.environ.get('CLOUDFLARE_ACCOUNT_ID', '38253a60db8406866eb2a255247002d5')
MODEL = '@cf/black-forest-labs/flux-1-schnell'
STIL = 'Warm natural light, rich appetizing colours, shallow depth of field, realistic photograph, high detail, no text, empty room, nobody visible'

BILLEDER = {
    # Toppen: fra indkøb til madlavning til det dækkede bord
    'hero-indkoeb': 'Fresh vegetables, bread and groceries in a wicker shopping basket on a wooden kitchen counter, seen from above at an angle',
    'hero-madlavning': 'Close-up of a homemade dinner being cooked in a pan on a stove with steam rising, a wooden spoon and fresh herbs, cosy rustic kitchen',
    'hero-bord': 'Overhead view of an empty rustic wooden dinner table set with several homemade dishes in ceramic bowls and empty plates, cutlery and linen napkins, nobody at the table',
    # Prisniveauer
    'niveau-student': 'A simple cosy dinner for one: a bowl of pasta with tomato sauce and a fork, a glass of water, on a small wooden table next to a window',
    'niveau-familie': 'Close-up of a big baking dish of oven roasted chicken with potatoes and vegetables in the middle of a set table with empty plates and glasses, nobody at the table',
    'niveau-weekend': 'Elegant weekend dinner: a plated beef steak with sauce and roasted vegetables, a glass of red wine and a lit candle on a dark wooden table',
}


# Husstandsikoner (vælger på forsiden): samme stil på tværs, mørk varm baggrund som siden
STIL_IKON = ('Minimal flat vector illustration, bold simple shapes, only orange and cream colours, '
             'plain solid near-black charcoal background, the scene fills most of the frame and is centered, clean edges, no text, no letters')
IKONER = {
    'husstand-enlig': 'One adult person sitting at a small table eating a bowl of pasta, a steaming mug beside the bowl',
    'husstand-par': 'Two adults sitting opposite each other at a small round table with one shared pot of food and two plates',
    'husstand-familie': 'A family of two adults and two small children sitting around a dinner table with a big dish of food in the middle',
    'husstand-stor': 'A large group of six people, adults and children, seated around a long table full of dishes, lively dinner',
}
BILLEDER.update(IKONER)


def lav(navn, nøgle):
    from PIL import Image
    body = json.dumps({'prompt': f'{BILLEDER[navn]}. {STIL_IKON if navn in IKONER else STIL}', 'steps': 6}).encode()
    req = urllib.request.Request(f'https://api.cloudflare.com/client/v4/accounts/{KONTO}/ai/run/{MODEL}', data=body,
                                 headers={'Authorization': 'Bearer ' + nøgle, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.load(r)
    if not d.get('success'):
        raise RuntimeError(json.dumps(d.get('errors'))[:200])
    img = Image.open(io.BytesIO(base64.b64decode(d['result']['image']))).convert('RGB').resize((320, 320) if navn in IKONER else (800, 800), Image.LANCZOS)
    os.makedirs(MAPPE, exist_ok=True)
    img.save(os.path.join(MAPPE, navn + '.jpg'), 'JPEG', quality=80, optimize=True, progressive=True)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    nøgle = os.environ.get('CLOUDFLARE_API_TOKEN', '')
    if not nøgle:
        sys.exit('Mangler miljøvariablen CLOUDFLARE_API_TOKEN')
    forfra = '--forfra' in sys.argv
    valgt = [a for a in sys.argv[1:] if not a.startswith('--')] or [n for n in BILLEDER if n not in IKONER]
    for n in valgt:
        if os.path.exists(os.path.join(MAPPE, n + '.jpg')) and not forfra:
            print(f'  – {n} findes (brug --forfra for at lave den om)')
            continue
        try:
            lav(n, nøgle)
            print(f'  ✓ {n}')
        except (urllib.error.HTTPError, RuntimeError) as e:
            print(f'  ✗ {n}: {e}')


if __name__ == '__main__':
    main()
