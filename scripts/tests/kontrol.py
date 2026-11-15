"""Faste kontroller af Måltidsjagten – skal bestå, før noget må på main (kører uden netværk og uden browser, så de også virker i skyen).

Kør:  python -I scripts/tests/kontrol.py
Afslutter med kode 1 ved FEJL (blokerer udgivelse). ADVARSEL blokerer ikke, men skal nævnes i rapporten.
Hver kontrol er skrevet ud fra en fejl, vi faktisk har haft – tilføj en ny kontrol, hver gang en fejl opdages (se ai/regler.md).
"""
import glob, json, os, re, shutil, subprocess, sys

sys.stdout.reconfigure(encoding='utf-8')
ROD = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
fejl, advarsler, ok = [], [], []


def laes(sti):
    with open(os.path.join(ROD, sti), encoding='utf-8') as f:
        return f.read()


def json_fil(sti):
    try:
        return json.loads(laes(sti))
    except Exception as e:  # noqa: BLE001
        fejl.append(f'{sti} kan ikke læses som JSON: {e}')
        return None


# ---------- 1. JSON-filer og tegn ----------
data = {}
for fil in ['retter.json', 'opskrifter.json', 'naering.json', 'tilbudsliste.json', 'scripts/tilbud_snapshot.json', 'scripts/billedprompts.json', 'scripts/rettelser.json']:
    data[fil] = json_fil(fil)
    if data[fil] is not None and '�' in laes(fil):
        fejl.append(f'{fil} indeholder ødelagte tegn (U+FFFD) – tegnsæt gik galt')
retter, opskr = data['retter.json'], data['opskrifter.json']

# ---------- 2. Butikkernes retter ----------
SOED = re.compile(r'(skyr|hytteost|banan|havre)pandekage|pandekager? med (æble|bær|syltetøj|kanel|banan|sirup|sukker)|dessert|æblekage|trifli|vafl|smoothie|müsli|grød(?!en)', re.I)
FROKOST = re.compile(r'(rejesalat|sild|røget laks|tunsalat|æggesalat).*(rugbrød|madder)|^rugbrød|smørrebrød|^toast|brunch', re.I)
if retter:
    antal_vt = laes('retter.json').count('"vt"')
    if antal_vt < 150:
        fejl.append(f'retter.json har kun {antal_vt} "vt"-felter (forventet ca. 250) – blev byg_opskrifter.py sprunget over? Kør ALTID byg_retter.py -> byg_opskrifter.py')
    else:
        ok.append(f'{antal_vt} vt-felter')
    tot = 0
    uden_billede, uden_ty = {}, {}
    for kode, b in retter['butikker'].items():
        L = b['retter']; tot += len(L)
        if len(L) < 40:
            fejl.append(f'{kode}: kun {len(L)} retter (mål: mindst 40)')
        navne = [r['navn'] for r in L]
        for n in {n for n in navne if navne.count(n) > 1}:
            fejl.append(f'{kode}: retten "{n}" findes to gange')
        for r in L:
            h = f"{kode}: '{r['navn']}'"
            if SOED.search(r['navn']): fejl.append(f'{h} er en sød ret/dessert – kun rigtig aftensmad')
            if FROKOST.search(r['navn']): fejl.append(f'{h} er frokost/morgenmad – kun rigtig aftensmad')
            if not r.get('billede') or not os.path.exists(os.path.join(ROD, r['billede'])): uden_billede.setdefault(kode, []).append(r['navn'])
            if len(r.get('fremgangsmaade', [])) < 2: fejl.append(f'{h} har under 2 trin i fremgangsmåden')
            if not r.get('ingredienser'): fejl.append(f'{h} har ingen ingredienser'); continue
            if not (15 <= r.get('pris_i_alt', 0) <= 450): advarsler.append(f"{h} har mærkelig pris: {r.get('pris_i_alt')} kr (hele retten)")
            ikke_basis = [i for i in r['ingredienser'] if not i.get('basisvare')]
            if not any(i.get('tilbud') for i in ikke_basis): fejl.append(f'{h} bruger ikke ét eneste tilbud')
            for i in r['ingredienser']:
                for t in i.get('tilbud') or []:
                    if t not in b['tilbud']: fejl.append(f"{h}: ingrediensen '{i['navn']}' peger på et tilbud ({t}), der ikke findes i butikkens aviser")
                if i.get('tilbud') and not (i.get('ty') or i.get('typ')): uden_ty.setdefault(kode, set()).add(i['navn'])
            # navnet må ikke love en hovedingrediens, retten ikke har
            ing_tekst = ' '.join(i['navn'].lower() for i in r['ingredienser'])
            for ord_ in ('svinemørbrad', 'andebryst', 'laks', 'torsk', 'kylling', 'hakket'):
                if ord_ in r['navn'].lower() and ord_ not in ing_tekst and not (ord_ == 'hakket' and 'hak' in ing_tekst):
                    advarsler.append(f"{h}: navnet nævner '{ord_}', men det står ikke på ingredienslisten")
    # Billeder kan ikke laves i skyen (nøglen findes kun på ejerens pc) – derfor en advarsel, ikke en fejl. Den, der laver billeder lokalt, skal rydde den.
    for kode, L in uden_billede.items():
        advarsler.append(f"{kode}: {len(L)} retter mangler billede (kræver lokal billeder.py): " + '; '.join(L[:3]) + (' …' if len(L) > 3 else ''))
    for kode, S in uden_ty.items():
        if len(S) > 15: advarsler.append(f"{kode}: {len(S)} ingredienser med tilbud mangler typeoplysning (ty) – indkøbslisten kan vise hele tilbudsgruppen: " + ', '.join(sorted(S)[:5]) + ' …')
    ok.append(f'{tot} butiksretter tjekket')

# ---------- 3. Biblioteksopskrifter ----------
if opskr:
    ider = [o['id'] for o in opskr['opskrifter']]
    if len(ider) != len(set(ider)): fejl.append('opskrifter.json har dobbelte id')
    for o in opskr['opskrifter']:
        if SOED.search(o['navn']) or FROKOST.search(o['navn']): fejl.append(f"opskrift '{o['navn']}' er ikke aftensmad")
        if not o.get('billede') or not os.path.exists(os.path.join(ROD, o['billede'])): fejl.append(f"opskrift '{o['navn']}' mangler billede")
    ok.append(f'{len(ider)} biblioteksopskrifter tjekket')

# ---------- 3b. Opskriftssider (SEO): hver opskrift skal have en side, gyldig Recipe-JSON-LD og stå i sitemap ----------
if opskr:
    try:
        sitemap = laes('sitemap.xml')
        mangler_side, mangler_sitemap, ugyldig = [], [], []
        for o in opskr['opskrifter']:
            sl = re.sub(r'[^a-z0-9]+', '-', o['navn'].lower().replace('æ', 'ae').replace('ø', 'oe').replace('å', 'aa')).strip('-')[:90]
            sti = f'opskrift/{sl}/index.html'
            if not os.path.exists(os.path.join(ROD, sti)): mangler_side.append(o['navn']); continue
            if f'/opskrift/{sl}/' not in sitemap: mangler_sitemap.append(o['navn'])
            blokke = re.findall(r'<script type="application/ld\+json">(.*?)</script>', laes(sti), re.S)
            try:
                r = [json.loads(b) for b in blokke if '"Recipe"' in b][0]
                if not (r.get('recipeIngredient') and r.get('recipeInstructions') and r.get('name')): ugyldig.append(o['navn'])
            except Exception:  # noqa: BLE001
                ugyldig.append(o['navn'])
        if mangler_side: fejl.append(f'{len(mangler_side)} opskrifter mangler opskriftsside (kør scripts/byg_sider.py): ' + '; '.join(mangler_side[:3]))
        if mangler_sitemap: fejl.append(f'{len(mangler_sitemap)} opskriftssider mangler i sitemap.xml: ' + '; '.join(mangler_sitemap[:3]))
        if ugyldig: fejl.append(f'{len(ugyldig)} opskriftssider har ugyldig Recipe-JSON-LD: ' + '; '.join(ugyldig[:3]))
        if not (mangler_side or mangler_sitemap or ugyldig): ok.append(f'{len(opskr["opskrifter"])} opskriftssider i orden')
    except FileNotFoundError:
        fejl.append('sitemap.xml mangler')

# ---------- 4. Næring og tilbudsliste skal høre til de aktuelle retter ----------
if retter and data['naering.json']:
    n = data['naering.json']
    manglende = [r['id'] for b in retter['butikker'].values() for r in b['retter'] if r['id'] not in n]
    if len(manglende) > 5: advarsler.append(f'naering.json mangler tal for {len(manglende)} retter – kør byg_opskrifter.py')
if data['tilbudsliste.json'] and not data['tilbudsliste.json'].get('grupper'): fejl.append('tilbudsliste.json har ingen grupper')

# ---------- 5. Billeder: størrelse og forladte filer ----------
brugt = set()
for b in (retter or {}).get('butikker', {}).values():
    brugt |= {os.path.basename(r.get('billede', '')) for r in b['retter']}
brugt |= {os.path.basename(o.get('billede', '')) for o in (opskr or {}).get('opskrifter', [])}
store = [f for f in glob.glob(os.path.join(ROD, 'billeder', '*.jpg')) if os.path.getsize(f) > 160_000]
if store: advarsler.append(f'{len(store)} billeder er over 160 KB (langsom mobil): ' + ', '.join(os.path.basename(f) for f in store[:3]))
forladte = [os.path.basename(f) for f in glob.glob(os.path.join(ROD, 'billeder', '*.jpg')) if os.path.basename(f) not in brugt]
if len(forladte) > 60: advarsler.append(f'{len(forladte)} billeder bruges ikke af nogen ret (kan ryddes)')

# ---------- 6. Sitens filer ----------
sw = laes('sw.js')
if not re.search(r"const VERSION = 'v\d+'", sw): fejl.append('sw.js mangler VERSION')
for fil in ['index.html', 'kategorier.js', 'pris.js', 'varer.js', 'sw.js', 'manifest.webmanifest', 'robots.txt', 'sitemap.xml']:
    if not os.path.exists(os.path.join(ROD, fil)): fejl.append(f'{fil} mangler')
if os.path.getsize(os.path.join(ROD, 'retter.json')) > 3_000_000: advarsler.append('retter.json er over 3 MB (langsom første indlæsning)')

# JavaScript-syntaks (kun hvis node findes – i skyen kan det mangle)
node = shutil.which('node')
if node:
    import tempfile
    html = laes('index.html')
    # kun rigtig JavaScript: spring JSON-LD og andre data-blokke (type=application/ld+json mv.) over
    scripts = [s for attr, s in re.findall(r'<script(?![^>]*\bsrc=)([^>]*)>(.*?)</script>', html, re.S)
               if not re.search(r'type\s*=\s*["\']?(?!module|text/javascript|application/javascript)[^"\'\s>]+', attr)]
    with tempfile.TemporaryDirectory() as tmp:
        emner = [(f'index.html #{i + 1}', s) for i, s in enumerate(scripts) if s.strip()] + [(f, laes(f)) for f in ['kategorier.js', 'pris.js', 'varer.js', 'sw.js']]
        for navn, kode in emner:
            sti = os.path.join(tmp, 'x.js')
            open(sti, 'w', encoding='utf-8').write(kode)
            p = subprocess.run([node, '--check', sti], capture_output=True, text=True)
            if p.returncode: fejl.append(f'JavaScript-fejl i {navn}: {p.stderr.strip().splitlines()[0] if p.stderr.strip() else "?"}')
    ok.append('JavaScript-syntaks tjekket med node')
else:
    advarsler.append('node findes ikke her – JavaScript-syntaksen er IKKE tjekket (kør kontrollen lokalt før udgivelse af kodeændringer)')

# ---------- 7. Opskrifternes egne tjek (rå kød uden tilberedning mv.) ----------
p = subprocess.run([sys.executable, '-I', os.path.join(ROD, 'scripts', 'tjek_opskrifter.py')], capture_output=True, text=True, encoding='utf-8', errors='replace')
if p.returncode: fejl.append('tjek_opskrifter.py fandt rå-fejl:\n' + '\n'.join(p.stdout.strip().splitlines()[-12:]))
else: ok.append('tjek_opskrifter.py bestået')

# ---------- 8. Regressionstest af pris, indkøbsliste og ugeforslag (node, gemt datakopi, se scripts/tests/regression.py) ----------
if shutil.which('node'):
    p = subprocess.run([sys.executable, '-I', os.path.join(ROD, 'scripts', 'tests', 'regression.py')], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if p.returncode: fejl.append('Regressionstesten (regression.py) fejlede:\n' + '\n'.join(p.stdout.strip().splitlines()[:12]))
    else: ok.append('regressionstest bestået (pris, indkøbsliste, ugeforslag)')
else:
    advarsler.append('node findes ikke her – regressionstesten er IKKE kørt')

print('OK:      ' + '; '.join(ok))
for a in advarsler[:40]: print('ADVARSEL:', a)
if len(advarsler) > 40: print(f'… og {len(advarsler) - 40} flere advarsler')
for f in fejl[:60]: print('FEJL:    ', f)
if len(fejl) > 60: print(f'… og {len(fejl) - 60} flere fejl')
print(f'\nRESULTAT: {"BESTÅET" if not fejl else "FEJLET"} ({len(fejl)} fejl, {len(advarsler)} advarsler)')
sys.exit(1 if fejl else 0)
