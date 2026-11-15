"""Browser-QA: åbner den UDGIVNE side i en rigtig browser (Playwright/Chromium), måler og tager skærmbilleder.

Kører i GitHub Actions (der er en browser og internet; rutinerne i skyen har ingen af delene).
Skriver:
  ai/BROWSER.md            kort tekstrapport (uden tidsstempel og millisekunder, så den kun ændres, når noget faktisk ændres)
  skaermbilleder/*.png     skærmbilleder af forsiden og flowet (lægges på grenen "skaermbilleder" af handlingen)
Afslutter med kode 1 ved fejl (vandret scroll, JavaScript-fejl, ødelagte billeder, side der ikke kan åbnes).
Kør:  python -I scripts/tests/browser_tjek.py [url]
"""
import datetime, os, sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
ROD = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
URL = sys.argv[1] if len(sys.argv) > 1 else 'https://madplan-blue.vercel.app/'
UD = os.path.join(ROD, 'skaermbilleder')
os.makedirs(UD, exist_ok=True)

MAAL = """() => {
  const W = document.documentElement.clientWidth, sw = document.documentElement.scrollWidth;
  const smaa = [...document.querySelectorAll('button, a, [role=button], input, select')].filter(e => {
    const b = e.getBoundingClientRect(), cs = getComputedStyle(e);
    return b.width > 0 && b.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && (b.height < 40 || b.width < 40);
  }).map(e => (e.getAttribute('aria-label') || e.textContent || e.className || e.tagName).toString().trim().replace(/\\s+/g, ' ').slice(0, 28));
  const billeder = [...document.querySelectorAll('img')].filter(i => i.complete && i.naturalWidth === 0).map(i => (i.getAttribute('src') || '').slice(0, 60));
  const ualt = [...document.querySelectorAll('img')].filter(i => !i.hasAttribute('alt')).length;
  return { W, sw, overflow: sw > W + 1, smaa, billeder, ualt, antalBilleder: document.querySelectorAll('img').length, titel: document.title,
           h1: document.querySelectorAll('h1').length, lcp: window.__lcp || 0, trin: (typeof state !== 'undefined' && state.trin) || '' };
}"""

LCP = "() => { window.__lcp = 0; new PerformanceObserver(l => { for (const e of l.getEntries()) window.__lcp = Math.round(e.startTime); }).observe({ type: 'largest-contentful-paint', buffered: true }); }"


def spand(ms):
    return 'under 1 s' if ms < 1000 else ('1–3 s' if ms <= 3000 else 'over 3 s')


linjer, fejl = [], []
with sync_playwright() as p:
    b = p.chromium.launch()
    for navn, w, h, mobil in [('mob', 390, 844, True), ('desk', 1280, 800, False)]:
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, is_mobile=mobil, has_touch=mobil, locale='da-DK')
        side = ctx.new_page()
        konsol = []
        side.on('console', lambda m, k=konsol: k.append(m.text[:140]) if m.type == 'error' else None)
        side.on('pageerror', lambda e, k=konsol: k.append('pageerror: ' + str(e)[:140]))
        try:
            side.goto(URL, wait_until='load', timeout=45000)
            side.evaluate(LCP)
            side.wait_for_selector('.dag-kort', timeout=20000)
            side.wait_for_timeout(2500)
        except Exception as e:  # noqa: BLE001
            fejl.append(f'{navn}: siden kunne ikke åbnes eller viste ikke madplanen ({str(e)[:100]})')
            linjer.append(f'### {navn} ({w} px)\n- Kunne ikke åbnes: {str(e)[:100]}\n')
            ctx.close(); continue
        # luk rundvisningen, hvis den er der
        try:
            side.click('[data-intro-luk]', timeout=1500)
        except Exception:  # noqa: BLE001
            pass
        side.wait_for_timeout(400)
        m = side.evaluate(MAAL)
        navigation = side.evaluate("() => Math.round(performance.getEntriesByType('navigation')[0]?.loadEventEnd || 0)")
        side.screenshot(path=os.path.join(UD, f'{navn}_1_forside.png'))
        # flowet: brug forslaget -> hvert trin
        trin_set = [m['trin']]
        skridt = []
        try:
            side.click('[data-sim-indkoeb]', timeout=4000)
            side.wait_for_timeout(1800)
            side.screenshot(path=os.path.join(UD, f'{navn}_2_efter_brug_forslaget.png'))
            skridt.append('brug forslaget: ok')
            knapper = side.query_selector_all('nav.trin button')
            for i, kn in enumerate(knapper[1:5], start=2):
                try:
                    if kn.is_enabled():
                        kn.click(timeout=2500)
                        side.wait_for_timeout(1500)
                        side.screenshot(path=os.path.join(UD, f'{navn}_{i + 1}_trin_{i}.png'))
                        skridt.append(f'trin {i}: ok')
                        trin_set.append(side.evaluate("() => (typeof state !== 'undefined' && state.trin) || ''"))
                    else:
                        skridt.append(f'trin {i}: låst')
                except Exception as e:  # noqa: BLE001
                    skridt.append(f'trin {i}: kunne ikke åbnes ({str(e)[:50]})')
        except Exception as e:  # noqa: BLE001
            skridt.append(f'brug forslaget: kunne ikke klikkes ({str(e)[:60]})')
        m2 = side.evaluate(MAAL)
        if m['overflow'] or m2['overflow']: fejl.append(f'{navn}: vandret scroll (bredde {m["sw"]} mod {m["W"]})')
        if konsol: fejl.append(f'{navn}: {len(konsol)} JavaScript-fejl i konsollen, fx: {konsol[0]}')
        if m['billeder'] or m2['billeder']: fejl.append(f'{navn}: ødelagte billeder: {(m["billeder"] + m2["billeder"])[:2]}')
        smaa = sorted(set(m['smaa'] + m2['smaa']))
        linjer.append(f'''### {navn} ({w} px)
- Indlæsning (load-hændelsen): {spand(navigation)} · største indhold vist: {spand(m['lcp'])}
- Vandret scroll: {'JA' if (m['overflow'] or m2['overflow']) else 'nej'} · JavaScript-fejl: {len(konsol)} · ødelagte billeder: {len(m['billeder'] + m2['billeder'])} · billeder uden alt: {m['ualt']}
- Små tryk-flader (under 40 px): {len(smaa)}{(' – fx ' + '; '.join(smaa[:8])) if smaa else ''}
- Flow: {', '.join(skridt) if skridt else 'ikke afprøvet'}
- Trin set: {', '.join(t for t in trin_set if t)}
''')
        ctx.close()
    b.close()

dato = datetime.date.today().isoformat()
tekst = f'''# Browser-QA af den udgivne side

Sidst kørt: {dato} · {URL}

**Resultat: {"RØD" if fejl else "GRØN"}**

Skrevet af GitHub-handlingen "Browser-QA" (`scripts/tests/browser_tjek.py`) med Chromium. Skærmbillederne ligger på grenen `skaermbilleder` (hent dem med `git fetch origin skaermbilleder` og `git show origin/skaermbilleder:mob_1_forside.png > /tmp/x.png`, og åbn filen med Read). Rutinerne i skyen har ingen browser, så de læser denne fil og billederne.

''' + '\n'.join(linjer) + ('\n## Fejl\n' + '\n'.join('- ' + f for f in fejl) + '\n' if fejl else '') + '''
Målt: vandret scroll, JavaScript-fejl, ødelagte billeder, tryk-flader under 40 px, indlæsningstid (i grove intervaller) og et flow gennem trinene. Ikke målt: farvekontrast, tastaturbrug, andre husstande end standard, login.
'''
open(os.path.join(ROD, 'ai', 'BROWSER.md'), 'w', encoding='utf-8', newline='\n').write(tekst)
print(tekst)
sys.exit(1 if fejl else 0)
