"""Browsertest af "Sammenlign butikker" i Chromium (Playwright) mod en LOKAL kopi af repoet (ingen net nødvendigt).

Måler BACKLOG accept (1), (2), (3), (4), (5), (9) og (11) på 390 px med touch: kortet køres rigtigt, og priserne i DOM
sammenlignes med sidens egne prisfunktioner. Selve testen står i scripts/tests/sammenlign_side.js.
Kør:  python -I scripts/tests/sammenlign_browser.py [rodmappe]
Afslutter med 0 (bestået), 1 (fejl) eller 3 (Playwright/Chromium findes ikke her: testen er IKKE kørt).
Tidsmålingen (lange opgaver) afhænger af maskinen; kravet er højst 200 ms.
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

srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Stille, directory=ROD))
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f'http://127.0.0.1:{srv.server_address[1]}/'
test = open(os.path.join(ROD, 'scripts', 'tests', 'sammenlign_side.js'), encoding='utf-8').read()
js_fejl = []
try:
    with sync_playwright() as p:
        try:
            b = p.chromium.launch()
        except Exception as e:
            print('IKKE KØRT: Chromium kunne ikke startes:', str(e).splitlines()[0])
            sys.exit(3)
        side = b.new_page(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True)
        side.on('pageerror', lambda e: js_fejl.append(str(e)[:200]))
        side.route('**/*', lambda r: r.abort() if not r.request.url.startswith(url) else r.continue_())  # kun den lokale kopi (logoer udefra blokeres)
        side.goto(url)
        side.wait_for_function("typeof data !== 'undefined' && data && data.butikker && typeof SAMM !== 'undefined'", timeout=60000)
        side.evaluate("() => { localStorage.clear(); document.querySelector('[data-intro-luk]')?.click(); }")
        ud = side.evaluate(test)
        b.close()
finally:
    srv.shutdown()
import json
d = json.loads(ud)
for h, m in d['maal'].items(): print(f"{h}: længste opgave {m['laengsteOpgaveMs']} ms; to butikker: {m.get('kombi')}")
fejl = d['fejl'] + [f'JavaScript-fejl: {e}' for e in js_fejl]
for f in fejl[:30]: print('FEJL:', f)
print('SAMMENLIGN I BROWSER:', 'BESTÅET' if not fejl else f'FEJLET ({len(fejl)} fejl)')
sys.exit(1 if fejl else 0)
