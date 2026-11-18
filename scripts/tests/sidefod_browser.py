"""Browsertest af sidefoden i Chromium (Playwright) mod en LOKAL kopi af repoet.

Måler: på 360 og 390 px er alle synlige sidefodselementer (Om Måltidsjagten, Rundvisning, links, knapper) mindst 44 px
høje, lukket og åben, uden vandret scroll; sidefodens opacity er 1 (også åben/fokus); på 1280 px står +/– lige efter
"Om Måltidsjagten" (ikke løsrevet til højre).
Kør:  python -I scripts/tests/sidefod_browser.py [rodmappe]
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

JS = """() => { const f = [];
  if (document.documentElement.scrollWidth > innerWidth) f.push('vandret scroll');
  const fod = document.querySelector('.fod'); if (!fod) return ['.fod findes ikke'];
  fod.scrollIntoView();
  const els = fod.querySelectorAll('summary, a, .fod-knap');
  let set = 0;
  els.forEach(e => { if (e.getBoundingClientRect().height === 0) return; set++;
    const h = e.getBoundingClientRect().height;
    if (innerWidth <= 600 && h < 44) f.push(e.textContent.trim() + ': ' + h + ' px');
    if (innerWidth <= 600 && Math.round(e.getBoundingClientRect().width) < innerWidth - 40) f.push(e.textContent.trim() + ' er ikke fuld bredde'); });
  if (set < 3) f.push('for få synlige sidefodselementer: ' + set);
  if (getComputedStyle(fod).opacity !== '1') f.push('opacity ' + getComputedStyle(fod).opacity);
  return f; }"""
JS_IKON = """() => { const s = document.querySelector('.fod summary'); const r = document.createRange(); r.selectNodeContents(s);
  const tekst = r.getBoundingClientRect(); const ikon = getComputedStyle(s, '::after');
  return {tekstHoejre: tekst.right, summaryHoejre: s.getBoundingClientRect().right, float: ikon.float, indhold: ikon.content}; }"""

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
        for bredde in (360, 390, 1280):
            side = b.new_page(viewport={'width': bredde, 'height': 844}, has_touch=bredde < 600, is_mobile=bredde < 600)
            side.on('pageerror', lambda e: js_fejl.append(str(e)[:200]))
            side.route('**/*', lambda r: r.abort() if not r.request.url.startswith(url) else r.continue_())
            side.add_init_script("localStorage.setItem('madplan-intro','1')")
            side.goto(url)
            side.wait_for_selector('.fod summary', state='attached', timeout=60000)
            side.wait_for_timeout(800)
            for tilstand in ('lukket', 'åben'):
                if tilstand == 'åben':
                    side.evaluate("() => { document.querySelector('.fod details').open = true; }")
                    side.evaluate("() => { document.querySelector('.fod summary').focus(); }")
                for f in side.evaluate(JS): fejl.append(f'{bredde} px, {tilstand}: {f}')
            ikon = side.evaluate(JS_IKON)
            if ikon['float'] != 'none': fejl.append(f'{bredde} px: +/– er løsrevet (float {ikon["float"]})')
            if bredde > 600 and ikon['summaryHoejre'] - ikon['tekstHoejre'] > 60:
                fejl.append(f'{bredde} px: +/– står langt fra teksten ({round(ikon["summaryHoejre"] - ikon["tekstHoejre"])} px)')
            side.close()
        b.close()
finally:
    srv.shutdown()
fejl += [f'JavaScript-fejl: {e}' for e in js_fejl]
for f in fejl[:30]: print('FEJL:', f)
print('SIDEFOD I BROWSER:', 'BESTÅET' if not fejl else f'FEJLET ({len(fejl)} fejl)')
sys.exit(1 if fejl else 0)
