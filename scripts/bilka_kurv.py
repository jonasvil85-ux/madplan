"""Lægger din indkøbsseddel i kurven på Bilka To Go – ved at åbne en synlig Edge og trykke "Læg i kurv"
på hver vare, som du ville gøre det selv. Kører på din egen computer.

Brug:
  1. Tryk "Kopiér seddel" på indkøbssedlen på madplan-siden.
  2. python -I scripts/bilka_kurv.py            (læser fra udklipsholderen)
     python -I scripts/bilka_kurv.py liste.txt (eller fra en fil med én vare pr. linje)

Første gang: vælg cookies og afhentning/levering i browservinduet – scriptet venter på dig.
Browseren forbliver åben bagefter, så du selv kan logge ind og gennemføre købet.
Der vælges altid det FØRSTE søgeresultat – tjek kurven til sidst.
"""
import asyncio, json, os, re, subprocess, sys, time, urllib.parse, urllib.request

try:
    from websockets.asyncio.client import connect
except ImportError:  # ældre websockets
    from websockets import connect

EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
PORT = 9333
PROFIL = os.path.join(os.environ.get('LOCALAPPDATA', '.'), 'madplan-bilka-profil')
SOEG = 'https://www.bilkatogo.dk/s/?query='


def soegeord(navn):
    """Samme logik som soegeord() i index.html: kort, søgbart navn uden mængder og 'eller …'."""
    n = re.split(r' eller |,| – | - ', navn, flags=re.I)[0]
    n = re.sub(r'\(.*?\)', '', n)
    n = re.sub(r'\s(marked|storkøb|xxl)\b', '', n, flags=re.I)
    n = re.sub(r'\d+([,.]\d+)?(-\d+([,.]\d+)?)?\s*(%|g|kg|ml|l|dl|stk|fed|dåser?|pakker?|bundt)\b', '', n, flags=re.I)
    return re.sub(r'\s+', ' ', n).strip()


def laes_varer(tekst):
    """Fra den kopierede seddel: '☐ 2 × Danske kartofler (25 kr)' -> (2, 'Danske kartofler')."""
    varer = []
    for linje in tekst.splitlines():
        if not linje.strip().startswith('☐'):
            continue
        navn = re.sub(r'\s*\((ca\. )?[\d.,]+ kr\)\s*$', '', linje.strip().lstrip('☐').strip())
        m = re.match(r'(\d+)\s*×\s*(.+)', navn)
        antal, navn = (int(m.group(1)), m.group(2)) if m else (1, navn)
        s = soegeord(navn)
        if s:
            varer.append((antal, s))
    return varer


def start_edge():
    try:
        urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json/version', timeout=2)
        return  # en Edge fra tidligere kørsel er stadig åben – genbrug den (og dens kurv)
    except Exception:
        pass
    os.makedirs(PROFIL, exist_ok=True)
    subprocess.Popen([EDGE, f'--remote-debugging-port={PORT}', '--remote-allow-origins=*', f'--user-data-dir={PROFIL}',
                      '--no-first-run', '--no-default-browser-check', 'https://www.bilkatogo.dk/'],
                     creationflags=0x00000008 | 0x00000200)  # DETACHED_PROCESS | NEW_PROCESS_GROUP
    for _ in range(40):
        try:
            urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json/version', timeout=1)
            return
        except Exception:
            time.sleep(0.5)
    sys.exit('Kunne ikke starte Edge.')


class Side:
    def __init__(self, ws):
        self.ws, self.n = ws, 0

    async def kald(self, metode, **params):
        self.n += 1
        await self.ws.send(json.dumps({'id': self.n, 'method': metode, 'params': params}))
        while True:
            svar = json.loads(await self.ws.recv())
            if svar.get('id') == self.n:
                return svar.get('result', {})

    async def js(self, kode):
        r = await self.kald('Runtime.evaluate', expression=kode, returnByValue=True, awaitPromise=True)
        return r.get('result', {}).get('value')


# Finder det første synlige "Læg i kurv" i selve søgeresultaterne og trykker på det (antal-1 gange ekstra "+")
TRYK = """(async (antal) => {
  const knapper = () => [...document.querySelectorAll('button[data-testid="addToBasketBtn"][aria-label="Læg i kurv"]')]
    .filter(b => b.offsetParent !== null && !b.closest('[class*="autocomplete"],[class*="Autocomplete"]'));
  const k = knapper()[0];
  if (!k) return null;
  const kort = k.closest('li,article,[class*="product"],[class*="Product"]') || k.parentElement.parentElement;
  const navn = (kort?.innerText || '').split('\\n').map(s => s.trim()).filter(Boolean).slice(0, 3).join(' | ').slice(0, 110);
  k.click();
  for (let i = 1; i < antal; i++) { await new Promise(r => setTimeout(r, 700)); (kort.querySelector('.add-to-basket-increment') || k).click(); }
  await new Promise(r => setTimeout(r, 900));
  return navn;
})(%d)"""


async def kør(varer):
    start_edge()
    mål = [t for t in json.load(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json')) if t.get('type') == 'page'][0]
    async with connect(mål['webSocketDebuggerUrl'], max_size=None) as ws:
        side = Side(ws)
        await side.kald('Page.enable')
        print(f'Lægger {len(varer)} varer i kurven på Bilka To Go …\n')
        mangler = []
        for nr, (antal, navn) in enumerate(varer, 1):
            await side.kald('Page.navigate', url=SOEG + urllib.parse.quote(navn))
            fundet, ventet = None, 0
            while ventet < (180 if nr == 1 else 12):  # første gang: giv tid til cookies/butiksvalg
                await asyncio.sleep(1.5); ventet += 1.5
                fundet = await side.js(TRYK % antal)
                if fundet:
                    break
                if nr == 1 and ventet == 6:
                    print('  (Hvis Bilka To Go spørger om cookies eller afhentning/levering, så vælg det i browservinduet – jeg venter.)')
            if fundet:
                print(f'  ✓ {antal} × {navn:28} → {fundet}')
            else:
                print(f'  ✗ {navn:28} → ingen resultater')
                mangler.append(navn)
        print(f'\nFærdig: {len(varer) - len(mangler)} af {len(varer)} varer lagt i kurven.')
        if mangler:
            print('Mangler (søg selv): ' + ', '.join(mangler))
        await side.kald('Page.navigate', url='https://www.bilkatogo.dk/kurv')
        print('Browservinduet er åbent på kurven – tjek varerne, log ind og gennemfør købet. Husk at kontrollere, at hvert produkt er det rigtige.')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) > 1:
        tekst = open(sys.argv[1], encoding='utf-8').read()
    else:
        tekst = subprocess.run(['powershell', '-NoProfile', '-Command', 'Get-Clipboard -Raw'], capture_output=True,
                               text=True, encoding='utf-8').stdout
    varer = laes_varer(tekst)
    if not varer:
        sys.exit('Fandt ingen varer. Tryk "Kopiér seddel" på indkøbssedlen først (eller giv en fil med linjer som "☐ Danske kartofler").')
    asyncio.run(kør(varer))


if __name__ == '__main__':
    main()
