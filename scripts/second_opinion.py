"""Beder en anden AI-model (Cloudflare Workers AI) om en kritisk vurdering af et krav eller et design. Bruges af agenterne i GitHub-handlingen anden-mening.yml.

Brug:   python3 scripts/second_opinion.py spoergsmaal.txt                      (kritisk rolle: finder huller; svaret skrives til skærmen)
        python3 scripts/second_opinion.py --rolle kreativ spoergsmaal.txt      (kreativ rolle: kommer med 5 forskellige idéer, høj temperatur)
        python3 scripts/second_opinion.py --proev [--rolle kreativ|kritisk]    (afprøver forbindelsen med ét kort spørgsmål)
Model: SECOND_OPINION_MODEL (standard Llama 3.3 70B). Stærkere gratis modeller på Cloudflare kan prøves, fx @cf/openai/gpt-oss-120b.

Kræver miljøvariablen CLOUDFLARE_API_TOKEN (samme nøgle som billederne; den må ikke stå i koden eller sendes i chatten).
Modellen er en RÅDGIVER: den ser kun den tekst, du sender, og kan tage fejl. Den ændrer ingenting.

Sikkerhedsgrænser (scriptet afviser selv, hvis de brydes):
  - højst SECOND_OPINION_MAKS kald pr. kørsel (standard 3), talt i filen SECOND_OPINION_TAELLER
  - højst 12000 tegn pr. spørgsmål
  - ingen e-mailadresser og ingen nøgle-lignende tekster (lange tilfældige tegnfølger, "Bearer", "api_key" osv.) i det, der sendes
"""
import json, os, re, sys, urllib.error, urllib.request

ROD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KONTO = os.environ.get('CLOUDFLARE_ACCOUNT_ID', '38253a60db8406866eb2a255247002d5')
MODEL = os.environ.get('SECOND_OPINION_MODEL', '@cf/meta/llama-3.3-70b-instruct-fp8-fast')
MAKS = int(os.environ.get('SECOND_OPINION_MAKS', '3'))
TAELLER = os.environ.get('SECOND_OPINION_TAELLER', os.path.join(ROD, '.second_opinion_taeller'))
MAKS_TEGN = 12000
PRODUKT = 'en hjemmeside, der laver ugens madplan og indkøbsseddel ud fra supermarkedernes tilbud (danske familier, lav pris, ærlige tal)'
ROLLER = {
    # kritisk = konvergerer: finder huller. Lav temperatur, så den holder sig til sagen.
    'kritisk': ('Du er en kritisk, ærlig sparringspartner for et lille dansk produkthold. Du får et krav eller et design til ' + PRODUKT + '. '
                'Svar på dansk og kort (højst 250 ord) i netop disse fire punkter: 1) Hvad er svagt eller uklart? 2) Hvad er glemt? '
                '3) Hvilke risici er der for brugerne (fx forvirring, forkerte priser, tillid)? 4) Hvad ville du gøre anderledes? '
                'Er kravet godt, så sig det kort og nævn kun det vigtigste. Du ser kun den tekst, du har fået; gæt ikke på mere, og opfind ikke fakta.', 0.3, 700),
    # kreativ = divergerer: kommer med flere, forskellige idéer. Høj temperatur. Agenten vælger bagefter, hvad der passer til produktets mål.
    'kreativ': ('Du er en meget kreativ produkttænker og en uforudsigelig sparringspartner for et lille dansk produkthold. Du får et krav eller et design til ' + PRODUKT + '. '
                'Din opgave er IKKE at kritisere, men at udvide mulighederne. Kom med 5 forskellige, konkrete idéer til, hvordan kravet kan løses eller tænkes helt anderledes, '
                'fra sikre til dristige. Mindst én skal være "skør, men tænkbar", mindst én skal vende problemet på hovedet, og mindst én skal være en radikalt enklere løsning. '
                'Hent inspiration fra andre brancher (spil, abonnementer, sociale apps, opskriftsapps, butikkernes egne apps), og tænk både som en travl forælder og som en konkurrent. '
                'Svar på dansk. For hver idé: en kort titel og 1-2 sætninger om, hvad brugeren oplever, og hvorfor det er værdifuldt. Ingen forbehold og ingen kritik. Højst 350 ord. '
                'Du ser kun den tekst, du har fået; opfind ikke fakta om produktet.', 1.0, 900),
}


def stop(tekst, kode=1):
    print(tekst)
    sys.exit(kode)


def tjek_tekst(t):
    if len(t) > MAKS_TEGN:
        stop(f'AFVIST: spørgsmålet er for langt ({len(t)} tegn, højst {MAKS_TEGN}). Opsummér.')
    if re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', t):
        stop('AFVIST: der står en e-mailadresse i teksten. Fjern den.')
    if re.search(r'(?i)bearer\s|api[_ -]?key|secret', t):
        stop('AFVIST: teksten nævner en nøgle eller hemmelighed. Send aldrig den slags.')
    if re.search(r'[A-Za-z0-9_\-]{32,}', t):
        stop('AFVIST: teksten indeholder en lang tegnfølge, der ligner en nøgle. Fjern den.')


def tael():
    n = 0
    try:
        n = int(open(TAELLER).read().strip() or 0)
    except Exception:
        pass
    if n >= MAKS:
        stop(f'STOP: grænsen på {MAKS} kald i denne kørsel er nået. Skriv rapporten med det, du har.', 3)
    open(TAELLER, 'w').write(str(n + 1))
    return n + 1


def uddrag_tekst(res):
    """Finder svarteksten, uanset hvilken form modellen svarer i."""
    if isinstance(res.get('response'), str) and res['response'].strip():
        return res['response']
    if res.get('choices'):
        t = res['choices'][0].get('message', {}).get('content')
        if t:
            return t
    dele = []
    for blok in res.get('output') or []:
        for del_ in (blok.get('content') or []) if isinstance(blok, dict) else []:
            if isinstance(del_, dict) and del_.get('type') in ('output_text', 'text') and del_.get('text'):
                dele.append(del_['text'])
    return '\n'.join(dele) or None


def spoerg(tekst, rolle='kritisk'):
    nøgle = os.environ.get('CLOUDFLARE_API_TOKEN')
    if not nøgle:
        stop('Mangler CLOUDFLARE_API_TOKEN', 2)
    if rolle not in ROLLER:
        stop('Ukendt rolle: ' + rolle + ' (brug kritisk eller kreativ)', 2)
    system, temperatur, maks_tokens = ROLLER[rolle]
    tjek_tekst(tekst)
    nr = tael()
    krop = {'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': tekst}], 'max_tokens': maks_tokens, 'temperature': temperatur}
    req = urllib.request.Request(f'https://api.cloudflare.com/client/v4/accounts/{KONTO}/ai/run/{MODEL}', data=json.dumps(krop).encode(),
                                 headers={'Authorization': 'Bearer ' + nøgle, 'Content-Type': 'application/json', 'User-Agent': 'madplan-anden-mening'})
    try:
        svar = json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e:
        stop(f'FEJL fra Cloudflare (HTTP {e.code}): ' + e.read().decode()[:300].replace(nøgle, '***'), 2)
    except Exception as e:  # noqa: BLE001
        stop(f'FEJL: {type(e).__name__}', 2)
    tekst_svar = uddrag_tekst(svar.get('result') or {})
    if not tekst_svar:
        stop('FEJL: tomt svar fra modellen: ' + json.dumps(svar, ensure_ascii=False)[:400], 2)
    print(f'[Svar fra {MODEL} som {rolle} – kald {nr} af {MAKS}]')
    print(tekst_svar)


if __name__ == '__main__':
    args = sys.argv[1:]
    rolle = 'kritisk'
    if '--rolle' in args:
        i = args.index('--rolle')
        rolle = args[i + 1] if i + 1 < len(args) else ''
        del args[i:i + 2]
    if not args:
        stop(__doc__, 2)
    if args[0] == '--proev':
        spoerg('Krav: Brugeren skal kunne vælge flere butikker med ét tryk, og prisen skal vise den billigste uge. Accept: prisen ændrer sig, når man vælger en butik mere.', rolle)
    else:
        spoerg(open(args[0], encoding='utf-8').read(), rolle)
