"""Beder en anden AI-model (Cloudflare Workers AI) om en kritisk vurdering af et krav eller et design. Bruges af agenterne i GitHub-handlingen anden-mening.yml.

Brug:   python3 scripts/second_opinion.py spoergsmaal.txt        (teksten i filen sendes; svaret skrives til skærmen)
        python3 scripts/second_opinion.py --proev                (afprøver forbindelsen med ét kort spørgsmål)

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
SYSTEM = ('Du er en kritisk, ærlig sparringspartner for et lille dansk produkthold. Du får et krav eller et design til en hjemmeside, der laver ugens madplan '
          'og indkøbsseddel ud fra supermarkedernes tilbud. Svar på dansk og kort (højst 250 ord) i netop disse fire punkter: '
          '1) Hvad er svagt eller uklart? 2) Hvad er glemt? 3) Hvilke risici er der for brugerne (fx forvirring, forkerte priser, tillid)? '
          '4) Hvad ville du gøre anderledes? Er kravet godt, så sig det kort og nævn kun det vigtigste. Du ser kun den tekst, du har fået; gæt ikke på mere, og opfind ikke fakta.')


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


def spoerg(tekst):
    nøgle = os.environ.get('CLOUDFLARE_API_TOKEN')
    if not nøgle:
        stop('Mangler CLOUDFLARE_API_TOKEN', 2)
    tjek_tekst(tekst)
    nr = tael()
    krop = {'messages': [{'role': 'system', 'content': SYSTEM}, {'role': 'user', 'content': tekst}], 'max_tokens': 700}
    req = urllib.request.Request(f'https://api.cloudflare.com/client/v4/accounts/{KONTO}/ai/run/{MODEL}', data=json.dumps(krop).encode(),
                                 headers={'Authorization': 'Bearer ' + nøgle, 'Content-Type': 'application/json', 'User-Agent': 'madplan-anden-mening'})
    try:
        svar = json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e:
        stop(f'FEJL fra Cloudflare (HTTP {e.code}): ' + e.read().decode()[:300].replace(nøgle, '***'), 2)
    except Exception as e:  # noqa: BLE001
        stop(f'FEJL: {type(e).__name__}', 2)
    res = svar.get('result') or {}
    tekst_svar = res.get('response')
    if tekst_svar is None and res.get('choices'):
        tekst_svar = res['choices'][0].get('message', {}).get('content')
    if not tekst_svar:
        stop('FEJL: tomt svar fra modellen: ' + json.dumps(svar)[:300], 2)
    print(f'[Svar fra {MODEL} – kald {nr} af {MAKS}]')
    print(tekst_svar if isinstance(tekst_svar, str) else json.dumps(tekst_svar, ensure_ascii=False))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        stop(__doc__, 2)
    if sys.argv[1] == '--proev':
        spoerg('Krav: Brugeren skal kunne vælge flere butikker med ét tryk, og prisen skal vise den billigste uge. Accept: prisen ændrer sig, når man vælger en butik mere.')
    else:
        spoerg(open(sys.argv[1], encoding='utf-8').read())
