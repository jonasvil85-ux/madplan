"""Bygger statiske opskriftssider til søgemaskiner: /opskrift/<navn>/index.html for hver biblioteksopskrift,
oversigten /opskrifter/index.html og sitemap.xml.

Siderne har billede, ingredienser til 4, trin, tid, næring og Recipe-struktureret data (schema.org). De indeholder bevidst ingen priser eller datoer,
fordi tilbud skifter hver uge og siderne ellers ville blive forældede. Knappen fører til appen, hvor ugens tilbud står.
Kør EFTER byg_opskrifter.py:   python -I scripts/byg_sider.py
"""
import html, json, os, re, shutil, sys

sys.stdout.reconfigure(encoding='utf-8')
ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://www.xn--mltidsjagten-tcb.dk'
KOEKKEN = {'dansk': 'Dansk', 'italiensk': 'Italiensk', 'amerikansk': 'Amerikansk', 'asiatisk': 'Asiatisk', 'middelhav': 'Middelhav', 'vegetar': 'Vegetar'}
NIVEAU = {'student': 'Nem hverdagsmad', 'familie': 'Familiemad', 'weekend': 'Weekendmad'}
ENHEDER_FLERTAL = {'dåse': 'dåser', 'pakke': 'pakker', 'bundt': 'bundter', 'glas': 'glas'}


def slug(navn):
    s = navn.lower().replace('æ', 'ae').replace('ø', 'oe').replace('å', 'aa')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')[:90]


def tal(m):
    s = ('%g' % m).replace('.', ',')
    return s


def ingrediens(i):
    n, m, e = i['navn'], i['maengde'], i['enhed']
    if e == 'efter smag' or not m:
        return n
    if e == 'stk':
        return f'{tal(m)} {n}'
    enh = ENHEDER_FLERTAL.get(e, e) if m > 1 else e
    return f'{tal(m)} {enh} {n}'


def esc(t):
    return html.escape(str(t), quote=True)


STIL = """
:root { --bg:#F8F5F0; --surface:#fff; --surface2:#F1ECE4; --border:rgba(60,45,30,.14); --t1:#1F1A16; --t2:#40372F; --t3:#6B6055; --knap:#C9561E; --knap-tekst:#fff; }
@media (prefers-color-scheme: dark) { :root { --bg:#15100C; --surface:#1F1813; --surface2:#2B211A; --border:rgba(255,226,190,.13); --t1:#fff; --t2:#E8DFD4; --t3:#B8AA9A; } }
* { box-sizing: border-box; }
body { margin:0; background:var(--bg); color:var(--t2); font:16px/1.6 Inter,system-ui,sans-serif; }
a { color: inherit; }
.top { max-width: 860px; margin: 0 auto; padding: 14px 16px; display:flex; align-items:center; justify-content:space-between; gap:12px; }
.logo { display:flex; align-items:center; gap:8px; font-weight:700; font-size:18px; color:var(--t1); text-decoration:none; }
.logo img { width:28px; height:28px; }
.top a.link { color:var(--t3); font-size:14px; text-decoration:none; padding:10px 4px; }
main { max-width: 860px; margin: 0 auto; padding: 0 16px 48px; }
.spor { font-size:13px; color:var(--t3); margin:4px 0 14px; }
.spor a { text-decoration:none; padding:6px 0; display:inline-block; }
h1 { color:var(--t1); font-size:clamp(1.7rem,4vw,2.3rem); line-height:1.15; margin:0 0 10px; letter-spacing:-.02em; }
h2 { color:var(--t1); font-size:1.2rem; margin:28px 0 10px; }
.hero { width:100%; aspect-ratio:4/3; object-fit:cover; border-radius:14px; display:block; background:var(--surface2); }
.meta { display:flex; flex-wrap:wrap; gap:8px; margin:14px 0; padding:0; list-style:none; }
.meta li { background:var(--surface); border:1px solid var(--border); border-radius:99px; padding:4px 12px; font-size:14px; }
.kort { background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:6px 18px 16px; }
ul.ing { margin:0; padding:0; list-style:none; }
ul.ing li { padding:9px 0; border-bottom:1px solid var(--border); }
ul.ing li:last-child { border-bottom:0; }
ol.trin { margin:0; padding-left:22px; }
ol.trin li { padding:6px 0; }
.knap { display:inline-block; background:var(--knap); color:var(--knap-tekst); font-weight:600; border-radius:12px; padding:14px 22px; text-decoration:none; min-height:48px; margin:6px 0; }
.lille { font-size:14px; color:var(--t3); }
.net { display:grid; grid-template-columns:repeat(auto-fill,minmax(180px,1fr)); gap:12px; padding:0; list-style:none; }
.net a { display:block; background:var(--surface); border:1px solid var(--border); border-radius:12px; overflow:hidden; text-decoration:none; height:100%; }
.net img { width:100%; aspect-ratio:4/3; object-fit:cover; display:block; background:var(--surface2); }
.net span { display:block; padding:10px 12px; font-size:14.5px; color:var(--t1); font-weight:500; }
footer { max-width:860px; margin:0 auto; padding:24px 16px 40px; font-size:14px; color:var(--t3); display:flex; flex-wrap:wrap; gap:6px 18px; }
footer a { padding:8px 0; }
"""


def side(titel, beskrivelse, kanon, indhold, jsonld, billede=None):
    og = f'<meta property="og:image" content="{esc(BASE + billede)}">' if billede else f'<meta property="og:image" content="{BASE}/og-image.jpg?v=2">'
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False, separators=(",", ":"))}</script>' for x in jsonld)
    return f"""<!doctype html>
<html lang="da">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(titel)}</title>
<meta name="description" content="{esc(beskrivelse)}">
<link rel="canonical" href="{esc(BASE + kanon)}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(titel)}">
<meta property="og:description" content="{esc(beskrivelse)}">
<meta property="og:url" content="{esc(BASE + kanon)}">
{og}
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F8F5F0">
<link rel="icon" type="image/svg+xml" href="/favicon.svg?v=2">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v=3">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{STIL}</style>
{ld}
</head>
<body>
<header class="top"><a class="logo" href="/"><img src="/favicon.svg?v=2" alt="" width="28" height="28">Måltidsjagten</a><a class="link" href="/opskrifter/">Alle opskrifter</a></header>
<main>
{indhold}
</main>
<footer><a href="/">Ugens madplan</a><a href="/opskrifter/">Alle opskrifter</a><a href="/privatlivspolitik.html">Privatlivspolitik</a></footer>
</body>
</html>
"""


def main():
    opskr = json.load(open(os.path.join(ROD, 'opskrifter.json'), encoding='utf-8'))['opskrifter']
    naering = json.load(open(os.path.join(ROD, 'naering.json'), encoding='utf-8'))
    navne = [o['navn'] for o in opskr]
    assert len(navne) == len(set(navne)), 'dobbelte opskriftsnavne'
    slugs = {o['navn']: slug(o['navn']) for o in opskr}
    assert len(set(slugs.values())) == len(slugs), 'dobbelte slugs'
    for mappe in ('opskrift', 'opskrifter'):
        shutil.rmtree(os.path.join(ROD, mappe), ignore_errors=True)
    sorteret = sorted(opskr, key=lambda o: o['navn'].lower())
    urls = [BASE + '/', BASE + '/opskrifter/', BASE + '/privatlivspolitik.html']
    for o in sorteret:
        s = slugs[o['navn']]
        kanon = f'/opskrift/{s}/'
        urls.append(BASE + kanon)
        img = '/' + o['billede'] if o.get('billede') else None
        koek = KOEKKEN.get(o['koekken'], o['koekken'].capitalize())
        niv = NIVEAU.get(o['niveau'], '')
        n = naering.get(o['id'])
        lignende = [x for x in sorteret if x['navn'] != o['navn'] and x['koekken'] == o['koekken']]
        # de fire næste i alfabetisk rækkefølge (rundt), så alle sider får og giver interne links
        idx = [x['navn'] for x in lignende]
        start = sum(1 for x in idx if x.lower() < o['navn'].lower())
        valgte = [lignende[(start + k) % len(lignende)] for k in range(min(4, len(lignende)))]
        ings = [ingrediens(i) for i in o['ingredienser']]
        beskr = f"{o['beskrivelse']} {o['tid_minutter']} min. til 4 personer."
        ld_recipe = {'@context': 'https://schema.org', '@type': 'Recipe', 'name': o['navn'], 'description': o['beskrivelse'], 'inLanguage': 'da',
                     'author': {'@type': 'Organization', 'name': 'Måltidsjagten', 'url': BASE + '/'}, 'recipeYield': '4 portioner',
                     'totalTime': f"PT{o['tid_minutter']}M", 'recipeCategory': 'Aftensmad', 'recipeCuisine': koek,
                     'recipeIngredient': ings, 'recipeInstructions': [{'@type': 'HowToStep', 'text': t} for t in o['fremgangsmaade']]}
        if img: ld_recipe['image'] = [BASE + img]
        if n and n.get('kcal'):
            ld_recipe['nutrition'] = {'@type': 'NutritionInformation', 'calories': f"{round(n['kcal'])} kcal", 'proteinContent': f"{n['protein']} g", 'fatContent': f"{n['fedt']} g", 'carbohydrateContent': f"{n['kulhydrat']} g", 'servingSize': '1 portion (gennemsnit af 4)'}
        if o['kategori'] == 'vegetar': ld_recipe['suitableForDiet'] = 'https://schema.org/VegetarianDiet'
        bread = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Måltidsjagten', 'item': BASE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Opskrifter', 'item': BASE + '/opskrifter/'},
            {'@type': 'ListItem', 'position': 3, 'name': o['navn'], 'item': BASE + kanon}]}
        meta = [f"{o['tid_minutter']} min.", '4 personer', koek] + ([niv] if niv else []) + (['Vegetar'] if o['kategori'] == 'vegetar' else [])
        naer = (f'<h2>Næring</h2><p class="lille">Cirka {round(n["kcal"])} kcal, {tal(n["protein"])} g protein, {tal(n["fedt"])} g fedt og {tal(n["kulhydrat"])} g kulhydrat pr. portion (gennemsnit af de fire portioner, beregnet ud fra ingredienserne).</p>' if n and n.get('kcal') else '')
        indhold = f"""<nav class="spor" aria-label="Brødkrumme"><a href="/">Måltidsjagten</a> › <a href="/opskrifter/">Opskrifter</a> › {esc(o['navn'])}</nav>
<h1>{esc(o['navn'])}</h1>
<p>{esc(o['beskrivelse'])}</p>
{f'<img class="hero" src="{esc(img)}" alt="{esc(o["navn"])}" width="720" height="540" fetchpriority="high">' if img else ''}
<ul class="meta">{''.join(f'<li>{esc(m)}</li>' for m in meta)}</ul>
<h2>Ingredienser til 4 personer</h2>
<div class="kort"><ul class="ing">{''.join(f'<li>{esc(i)}</li>' for i in ings)}</ul></div>
<h2>Sådan gør du</h2>
<ol class="trin">{''.join(f'<li>{esc(t)}</li>' for t in o['fremgangsmaade'])}</ol>
{naer}
<h2>Hvad koster den i denne uge?</h2>
<p>Måltidsjagten finder ugens tilbud i Netto, MENY, Bilka, REMA 1000, Kvickly, SuperBrugsen, Lidl, 365discount, SPAR og Min Købmand og viser, hvad retten koster i den butik, du handler i.</p>
<p><a class="knap" href="/">Se ugens tilbud og lav din madplan</a></p>
<h2>Flere opskrifter i samme stil</h2>
<ul class="net">{''.join(f'<li><a href="/opskrift/{slugs[x["navn"]]}/">' + (f'<img src="/{esc(x["billede"])}" alt="" loading="lazy" width="720" height="540">' if x.get('billede') else '') + f'<span>{esc(x["navn"])}</span></a></li>' for x in valgte)}</ul>"""
        ud = os.path.join(ROD, 'opskrift', s)
        os.makedirs(ud, exist_ok=True)
        open(os.path.join(ud, 'index.html'), 'w', encoding='utf-8', newline='\n').write(side(f"{o['navn']} – opskrift til 4 | Måltidsjagten", beskr, kanon, indhold, [ld_recipe, bread], img))
    # oversigten
    grupper = {}
    for o in sorteret:
        grupper.setdefault(o['koekken'], []).append(o)
    sektioner = []
    for k in ['dansk', 'italiensk', 'amerikansk', 'asiatisk', 'middelhav', 'vegetar']:
        if k not in grupper: continue
        sektioner.append(f'<h2>{esc(KOEKKEN[k])} ({len(grupper[k])})</h2><ul class="net">' + ''.join(
            f'<li><a href="/opskrift/{slugs[x["navn"]]}/">' + (f'<img src="/{esc(x["billede"])}" alt="" loading="lazy" width="720" height="540">' if x.get('billede') else '') + f'<span>{esc(x["navn"])}</span></a></li>' for x in grupper[k]) + '</ul>')
    liste = {'@context': 'https://schema.org', '@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': f'{BASE}/opskrift/{slugs[o["navn"]]}/', 'name': o['navn']} for i, o in enumerate(sorteret)]}
    indhold = f"""<nav class="spor" aria-label="Brødkrumme"><a href="/">Måltidsjagten</a> › Opskrifter</nav>
<h1>Opskrifter til aftensmad</h1>
<p>{len(sorteret)} hjemmelavede aftensretter til en familie på fire, sorteret efter køkken. Alle er bygget, så de kan laves af ugens tilbud i de danske supermarkeder.</p>
<p><a class="knap" href="/">Se ugens tilbud og lav din madplan</a></p>
{''.join(sektioner)}"""
    os.makedirs(os.path.join(ROD, 'opskrifter'), exist_ok=True)
    open(os.path.join(ROD, 'opskrifter', 'index.html'), 'w', encoding='utf-8', newline='\n').write(
        side('Opskrifter til aftensmad | Måltidsjagten', f'{len(sorteret)} hjemmelavede aftensretter til 4 personer, sorteret efter køkken, bygget til ugens tilbud i danske supermarkeder.', '/opskrifter/', indhold, [liste]))
    # sitemap
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        fr = 'daily' if u.endswith('.dk/') else ('yearly' if 'privatliv' in u else 'monthly')
        xml += f'  <url><loc>{u}</loc><changefreq>{fr}</changefreq></url>\n'
    xml += '</urlset>\n'
    open(os.path.join(ROD, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write(xml)
    print(f'{len(sorteret)} opskriftssider + oversigt, sitemap med {len(urls)} adresser')


if __name__ == '__main__':
    main()
