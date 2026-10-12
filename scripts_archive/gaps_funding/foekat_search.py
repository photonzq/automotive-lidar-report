"""Search the German federal funding catalogue (Foerderkatalog, foerderportal.bund.de/foekat).

Usage:  python foekat_search.py OUTDIR field=value [field=value ...]
  field is one of: thema (project title words), verbund (joint-project title),
  ze (recipient name), fkz (funding code), schnell (quick search over title, code,
  recipient and executing body). Values are wrapped in the catalogue's % wildcard.
Example: python foekat_search.py povos thema=POVOS
         python foekat_search.py povos verbund=POVOS
         python foekat_search.py povos ze=Scantinel

The catalogue's public search form is driven by GET/POST parameters; this script opens a
session, submits the form, pages through the result list and saves each result page as
HTML, then prints the rows (funding code, ministry, recipient, project title, period,
amount). Detail pages are saved for every funding code found. No login or personal data
is sent.
"""
import os
import re
import sys
import time
from html import unescape

import requests

BASE = "https://foerderportal.bund.de/foekat/jsp/"
HEADERS = {"User-Agent": "research-script/1.0"}
FIELD = {"thema": "suche.themaSuche[0]", "verbund": "suche.verbundSuche[0]",
         "ze": "suche.nameZeStSuche", "fkz": "suche.fkzSuche[0]",
         "schnell": "suche.schnellSuche"}
# The catalogue matches whole field values; % and _ are its wildcards, so values are
# wrapped in % unless they already contain one.


def clean(html):
    txt = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", txt)
    return re.sub(r"\s+", " ", unescape(txt)).strip()


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    params = {}
    for arg in sys.argv[2:]:
        k, v = arg.split("=", 1)
        params[FIELD[k]] = v if "%" in v else f"%{v}%"
    tag = "_".join(f"{k}-{re.sub(r'[^A-Za-z0-9]', '', v)}" for k, v in
                   (a.split("=", 1) for a in sys.argv[2:]))
    s = requests.Session()
    s.headers.update(HEADERS)
    s.get(BASE + "SucheAction.do?actionMode=searchreset", timeout=60)
    quick = "suche.schnellSuche" in params
    data = {"actionMode": "searchlist", "suche.detailSuche": "false" if quick else "true",
            "submitAction": "Schnellsuche starten" if quick else "Suche starten"}
    data.update(params)
    data = {k: v.encode("iso-8859-15") for k, v in data.items()}
    r = s.post(BASE + "SucheAction.do?actionMode=searchlist" if quick else BASE + "SucheAction.do",
               data=data, timeout=120)
    pages = [r.text]
    # The result list shows 10 rows per page; paging is a POST of suche.listrowfrom
    # within the same session. Read the total hit count and request 50 rows at a time.
    m = re.search(r"(\d+)\s*Treffer insgesamt", r.text)
    total = int(m.group(1)) if m else 0
    if total > 10:
        pages = []
        for start in range(1, total + 1, 50):
            time.sleep(1)
            rr = s.post(BASE + "SucheAction.do",
                        data={"suche.listrowfrom": str(start), "suche.listrowpersite": "50",
                              "suche.orderby": "1", "suche.order": "asc"}, timeout=120)
            pages.append(rr.text)
    print(f"total hits reported: {total}")
    for i, p in enumerate(pages):
        with open(os.path.join(out, f"foekat_{tag}_p{i + 1}.html"), "w", encoding="utf-8") as f:
            f.write(p)
    fkzs = []
    for p in pages:
        fkzs += re.findall(r"actionMode=view&(?:amp;)?fkz=([A-Z0-9]+)", p)
    fkzs = list(dict.fromkeys(fkzs))
    print(f"{tag}: {len(pages)} result page(s), {len(fkzs)} funding codes: {fkzs}")
    for fkz in fkzs:
        time.sleep(1)
        d = s.get(BASE + f"SucheAction.do?actionMode=view&fkz={fkz}", timeout=120).text
        with open(os.path.join(out, f"foekat_detail_{fkz}.html"), "w", encoding="utf-8") as f:
            f.write(d)
        txt = clean(d)
        i = txt.find("Förderkennzeichen")
        print(f"\n--- {fkz} ---\n{txt[i:i + 1600] if i >= 0 else txt[:1600]}")


if __name__ == "__main__":
    main()
