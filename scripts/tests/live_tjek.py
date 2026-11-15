"""Vagtposten: tjekker den UDGIVNE side mod main og skriver resultatet til ai/HELBRED.md.

Kører i GitHub Actions (som har internet; rutinerne i skyen kan ikke nå siden). Afslutter med kode 1, hvis siden er rød.
Kør:  python -I scripts/tests/live_tjek.py [--ingen-fil]
"""
import datetime, hashlib, json, os, re, sys, urllib.request

sys.stdout.reconfigure(encoding='utf-8')
ROD = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SIDER = ['https://madplan-blue.vercel.app', 'https://www.xn--mltidsjagten-tcb.dk']
UA = 'Maaltidsjagten-vagtpost/1.0 (+https://xn--mltidsjagten-tcb.dk)'


def hent(url, bytes_=False):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Cache-Control': 'no-cache'})
    with urllib.request.urlopen(req, timeout=30) as r:
        d = r.read()
        return d if bytes_ else d.decode('utf-8')


def lokal(sti):
    with open(os.path.join(ROD, sti), 'rb') as f:
        return f.read()


def norm(b):  # Windows/Unix-linjeskift ligegyldige
    return b.replace(b'\r\n', b'\n')


linjer, fejl, advarsler = [], [], []
lokal_retter = json.loads(lokal('retter.json').decode('utf-8'))
antal_lokal = sum(len(b['retter']) for b in lokal_retter['butikker'].values())
lokal_version = re.search(r"const VERSION = '(v\d+)'", lokal('sw.js').decode('utf-8')).group(1)
billeder = [r['billede'] for b in lokal_retter['butikker'].values() for r in b['retter'] if r.get('billede')]

for side in SIDER:
    try:
        sw = hent(side + '/sw.js')
        v = re.search(r"const VERSION = '(v\d+)'", sw)
        v = v.group(1) if v else '?'
        r = json.loads(hent(side + '/retter.json'))
        antal = sum(len(b['retter']) for b in r['butikker'].values())
        same = hashlib.sha1(norm(hent(side + '/retter.json', True))).hexdigest() == hashlib.sha1(norm(lokal('retter.json'))).hexdigest()
        html = hent(side + '/')
        har_app = 'kategorier.js' in html and 'sw.js' in html
        stikprove = billeder[:: max(1, len(billeder) // 8)][:8]
        mangler = []
        for b in stikprove:
            try:
                hent(side + '/' + b, True)
            except Exception:  # noqa: BLE001
                mangler.append(b)
        status = 'OK'
        if v != lokal_version: status = 'AFVIGER'; fejl.append(f'{side}: sw.js VERSION er {v}, main har {lokal_version} (deploy ikke færdig, eller fejlet)')
        if not same: status = 'AFVIGER'; fejl.append(f'{side}: retter.json er ikke identisk med main ({antal} mod {antal_lokal} retter)')
        if not har_app: status = 'FEJL'; fejl.append(f'{side}: forsiden mangler scripts')
        if mangler: status = 'FEJL'; fejl.append(f'{side}: {len(mangler)} af {len(stikprove)} stikprøve-billeder kan ikke hentes: {mangler[:2]}')
        linjer.append(f'- {side}: **{status}** (sw.js {v}, {antal} retter, retter.json {"identisk" if same else "AFVIGER"} med main, {len(stikprove) - len(mangler)}/{len(stikprove)} billeder hentet)')
    except Exception as e:  # noqa: BLE001
        fejl.append(f'{side}: kan ikke nås ({e})')
        linjer.append(f'- {side}: **KAN IKKE NÅS** ({e})')

tid = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
rod = os.popen(f'git -C "{ROD}" rev-parse --short HEAD').read().strip()
tekst = f'# Helbred for den udgivne side\n\nSidst tjekket: {tid} · main: {rod}\n\n**Resultat: {"RØD" if fejl else "GRØN"}**\n\n' + '\n'.join(linjer) + '\n'
if fejl:
    tekst += '\n## Fejl\n' + '\n'.join('- ' + f for f in fejl) + '\n'
tekst += '\nFilen skrives af GitHub-handlingen "Vagtpost" (scripts/tests/live_tjek.py). Rutinerne i skyen kan ikke selv nå siden, så de læser denne fil.\n'
print(tekst)
if '--ingen-fil' not in sys.argv:
    with open(os.path.join(ROD, 'ai', 'HELBRED.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(tekst)
sys.exit(1 if fejl else 0)
