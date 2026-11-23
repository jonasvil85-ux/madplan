"""Browsertest af søgningen i "Vælg selv" i Chromium (Python-Playwright) mod en LOKAL kopi af repoet.

Dækker det, der skal kunne køres, hvor kun Python-Playwright findes (som de øvrige Chromium-tests):
ental/flertal giver samme retter, "ris"/"ost" matcher ikke midt i ord, kun én synlig "Din uge"-overskrift under søgning,
og at søgningen ikke ændrer de valgte retter. Den fulde test (felt, tom-tilstand, ×, Escape) er soeg_browser.js (node).
Kør:  python -I scripts/tests/soeg_browser.py [rodmappe]
Afslutter med 0 (bestået), 1 (fejl) eller 3 (Playwright/Chromium findes ikke her: testen er IKKE kørt).
"""
import functools, http.server, os, sys, threading

sys.stdout.reconfigure(encoding='utf-8')
ROD = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print('IKKE KØRT: Playwright findes ikke her (pip install playwright && playwright install chromium)')
    sys.exit(3)

class Stille(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

JS_PAR = """() => {
  const R = pool(aktivS()), n = s => { const x = soegRetter(R, s); return x ? x.size : -1; };
  const falsk = [{ id: 'a', navn: 'Tomatris', ingredienser: [{ navn: 'tomatris' }] }, { id: 'b', navn: 'Risotto', ingredienser: [{ navn: 'ris' }] },
    { id: 'c', navn: 'Ostesovs', ingredienser: [{ navn: 'smeltet cheddar' }] }, { id: 'd', navn: 'Suppe', ingredienser: [{ navn: 'løgene' }, { navn: 'kartofler' }] }];
  const ids = s => [...soegRetter(falsk, s)].join('');
  return { par: [['kartoffel', 'kartofler'], ['gulerod', 'gulerødder'], ['tomat', 'tomater'], ['pølse', 'pølser'], ['løg', 'løgene']].map(([a, b]) => [a, b, n(a), n(b)]),
    ris: ids('ris'), ost: ids('ost'), logene: ids('løg'), kartofler: ids('kartoffel'), kartoffel: ids('kartofler'),
    risRetter: R.filter(r => !soegOrd([r.navn, ...r.ingredienser.map(i => i.navn)].join(' ')).some(w => w.startsWith('ris')) && soegRetter([r], 'ris').size).length }; }"""
JS_UGE = """() => [...document.querySelectorAll('#ret-indhold *')].filter(e => e.children.length === 0 && /^Din uge\\b/.test(e.textContent.trim()) && e.getBoundingClientRect().height > 0).length"""

srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Stille, directory=ROD))
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f'http://127.0.0.1:{srv.server_address[1]}/'
fejl, js_fejl = [], []
try:
    with sync_playwright() as p:
        try:
            b = p.chromium.launch()
        except Exception as e:
            print('IKKE KØRT: Chromium kunne ikke startes:', str(e).splitlines()[0])
            sys.exit(3)
        for bredde in (390, 360):
            ctx = b.new_context(viewport={'width': bredde, 'height': 844}, has_touch=True, is_mobile=True)
            side = ctx.new_page()
            side.on('pageerror', lambda e: js_fejl.append(str(e)[:200]))
            side.route('**/*', lambda r: r.continue_() if r.request.url.startswith(url) else r.abort())
            side.goto(url)
            side.wait_for_function("typeof data !== 'undefined' && data && data.butikker && typeof renderRetter === 'function'", timeout=60000)
            side.evaluate("() => { localStorage.clear(); document.querySelector('[data-intro-luk]')?.click(); }")
            side.evaluate("() => { const k = Object.keys(data.butikker)[0]; state.butikker = [k]; state.butik = k; state.butikValgt = true; state.trin = 'retter'; render(); }")
            side.wait_for_selector('#ret-soeg', timeout=10000)
            m = f'{bredde} px: '
            r = side.evaluate(JS_PAR)
            for a, c, x, y in r['par']:
                if not (x > 0 and x == y): fejl.append(f'{m}"{a}" ({x}) og "{c}" ({y}) skal give samme antal retter')
            if r['ris'] != 'b': fejl.append(m + '"ris" skal kun finde ordet ris: ' + r['ris'])
            if r['ost'] != 'c': fejl.append(m + '"ost" skal kun finde ordstart: ' + r['ost'])
            if not (r['logene'] == 'd' and r['kartofler'] == 'd' and r['kartoffel'] == 'd'): fejl.append(m + 'ental/flertal på prøveretter: ' + str(r))
            if r['risRetter']: fejl.append(m + '"ris" matcher midt i ord i rigtige retter')
            side.click('#ret-indhold .grid .ret h3')
            foer = side.evaluate("() => JSON.stringify([state.valgte, state.dagPlads])")
            side.fill('#ret-soeg', 'kartofler')
            antal = side.evaluate("() => document.querySelectorAll('#ret-indhold .grid .ret').length")
            side.fill('#ret-soeg', 'kartoffel')
            antal2 = side.evaluate("() => document.querySelectorAll('#ret-indhold .grid .ret').length")
            if not (antal > 0 and antal == antal2): fejl.append(f'{m}kort på siden: "kartofler" {antal} mod "kartoffel" {antal2}')
            uge = side.evaluate(JS_UGE)
            if uge != 1: fejl.append(f'{m}der skal være én synlig "Din uge"-overskrift under søgning, ikke {uge}')
            if side.evaluate("() => JSON.stringify([state.valgte, state.dagPlads])") != foer: fejl.append(m + 'søgningen ændrede de valgte retter')
            ctx.close()
        b.close()
finally:
    srv.shutdown()
for e in js_fejl: fejl.append('JavaScript-fejl: ' + e)
for f in fejl[:30]: print('FEJL:', f)
print('SØGNING (PYTHON) I BROWSER:', f'FEJLET ({len(fejl)} fejl)' if fejl else 'BESTÅET')
sys.exit(1 if fejl else 0)
