"""R2 helper snippets run inline during the R2_C0_C4 research, collected here for the archive.

Usage (Anaconda interpreter):
  python R2_inline_snippets.py html <file.html> <regex> [<regex> ...]   # keyword windows in a saved page
  python R2_inline_snippets.py jats <file.xml> <regex> [<regex> ...]    # keyword windows in a JATS full text
  python R2_inline_snippets.py settembrini                              # dB ratios from Extended Data Table 2
  python R2_inline_snippets.py arxiv <id> [<id> ...]                    # title/authors/DOI from arXiv abstract pages
  python R2_inline_snippets.py crossref <doi> [<doi> ...]               # title/authors/journal from Crossref
  python R2_inline_snippets.py epmc <query>                             # Europe PMC search (e.g. DOI:..., PMCID:...)
  python R2_inline_snippets.py c7 <wavelength_nm>                       # IEC 60825-1:2014 C7 and CW small-source AEL

Notes:
  - Network requests send a generic browser User-Agent only: no e-mail address, no mailto parameter,
    no cookies or credentials. Crossref is queried without the "polite pool" e-mail parameter.
  - Saved pages are read from paths given on the command line (<scratch> stands for a temporary folder).
"""
import html
import json
import math
import re
import sys
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0 Safari/537.36")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def page_text(raw):
    t = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t)


def windows(text, patterns, width=250, limit=6):
    for p in patterns:
        for m in list(re.finditer(p, text))[:limit]:
            print(f"[{p}] ...{text[max(0, m.start() - width):m.end() + width]}...\n")


def settembrini():
    # Extended Data Table 2 of Settembrini et al. (Nature 2026), SNR per target at 7.2 m.
    rows = {1: {"retro": 113715, "50%": 74.7, "10%": 31.2, "5%": 19.4},
            4: {"retro": 433565, "50%": 264, "10%": 90.2, "5%": 41.7}}
    for navg, r in rows.items():
        for ref in ("50%", "10%", "5%"):
            print(f"N_avg={navg}: retro/{ref} = {10 * math.log10(r['retro'] / r[ref]):.2f} dB")
        print(f"N_avg={navg}: 50%/5% = {10 * math.log10(r['50%'] / r['5%']):.2f} dB")
    for ref, rho in (("50%", 0.5), ("10%", 0.1), ("5%", 0.05)):
        print(f"rho_eq from {ref}: {rho * rows[1]['retro'] / rows[1][ref]:.0f}")


def arxiv(ids):
    for i in ids:
        s = get(f"https://arxiv.org/abs/{i}")
        meta = lambda n: [html.unescape(m) for m in re.findall(r'<meta name="%s" content="([^"]*)"' % n, s)]
        print(i, "|", meta("citation_title")[:1], "|", meta("citation_author")[:6], "|",
              meta("citation_date")[:1], "| doi", meta("citation_doi")[:1])


def crossref(dois):
    for d in dois:
        m = json.loads(get("https://api.crossref.org/works/" + urllib.parse.quote(d)))["message"]
        au = ", ".join(a.get("family", "") for a in m.get("author", [])[:4])
        print(d, "|", (m.get("title") or [""])[0], "|", au, "|", (m.get("container-title") or [""])[0],
              m.get("volume"), m.get("page"), "|", m.get("issued", {}).get("date-parts"))


def epmc(query):
    url = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json&resultType=core&query="
           + urllib.parse.quote(query))
    for r in json.loads(get(url))["resultList"]["result"]:
        print(r.get("pmcid"), "|", r.get("title"), "|", r.get("authorString", "")[:120], "|",
              r.get("journalInfo", {}).get("journal", {}).get("title"), r.get("pubYear"), "|", r.get("doi"))


def c7(lam):
    # IEC 60825-1:2014 Table 9: C4 = 5 (1050-1400 nm); C7 = 10**(0.018(l-1150)) (1150-1200 nm),
    # 8 + 10**(0.04(l-1250)) (1200-1400 nm). Small-source Class 1 CW AEL = 3.9e-4 * C4 * C7 W.
    if 1150 <= lam < 1200:
        c = 10 ** (0.018 * (lam - 1150))
    elif 1200 <= lam <= 1400:
        c = 8 + 10 ** (0.04 * (lam - 1250))
    else:
        c = 1.0
    c4 = 5.0 if 1050 <= lam <= 1400 else 10 ** (0.002 * (lam - 700))
    print(f"lambda={lam} nm: C4={c4:.3f}, C7={c:.1f}, AEL={3.9e-4 * c4 * c:.4f} W (Class 3B cap 0.5 W)")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    cmd = sys.argv[1]
    if cmd == "html":
        windows(page_text(open(sys.argv[2], encoding="utf-8", errors="replace").read()), sys.argv[3:])
    elif cmd == "jats":
        raw = open(sys.argv[2], encoding="utf-8").read()
        windows(re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw))), sys.argv[3:], width=400)
    elif cmd == "settembrini":
        settembrini()
    elif cmd == "arxiv":
        arxiv(sys.argv[2:])
    elif cmd == "crossref":
        crossref(sys.argv[2:])
    elif cmd == "epmc":
        epmc(sys.argv[2])
    elif cmd == "c7":
        c7(float(sys.argv[2]))
    else:
        raise SystemExit(__doc__)
