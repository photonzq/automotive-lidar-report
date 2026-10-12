"""Helpers used for group R3 (Fastree3D register history, exchange rates, saved-page searches).

No credentials and no email address are used anywhere; requests carry a generic browser User-Agent.
Paths are passed on the command line (e.g. <scratch>/r3/fastree), never hard-coded.

Usage:
  python R3_registry_fx_snippets.py zefix-search <name>             # Zefix public web API: firm list (ehraid, UID)
  python R3_registry_fx_snippets.py zefix-firm <ehraid> <out.json>   # firm record incl. SOGC publication texts
  python R3_registry_fx_snippets.py sogc-texts <firm.json>           # print each SOGC notice (date, ID, journal, text)
  python R3_registry_fx_snippets.py sogc-pdf <sogc_id> <out.pdf>     # pre-2020 SOGC notice as a one-page PDF
  python R3_registry_fx_snippets.py snb <cube> <from> <to> [dimSel]  # SNB data portal CSV, e.g. devkum 2023-12 2023-12 "D0(M0,M1),D1(USD1,CNY100)"
  python R3_registry_fx_snippets.py page-grep <file.html> <regex>... # tag-stripped text search of a saved web page

Notes on the sources:
  * Zefix firm records list SOGC (FOSC/SHAB) notices with their full text; older notices (before about 2016)
    are fetched one by one from the SOGC archive by their publication ID and read as PDFs (render with PyMuPDF).
  * The cantonal (Vaud) extract shows struck entries only after its "Afficher les radiations" switch is set;
    that was done in a browser, not by this script.
"""
import html
import json
import re
import sys
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def _get(url, data=None, headers=None, timeout=60):
    h = {"User-Agent": UA, "Accept": "*/*"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def zefix_search(name):
    body = json.dumps({"name": name, "languageKey": "fr", "maxEntries": 10, "offset": 0}).encode()
    raw = _get("https://www.zefix.admin.ch/ZefixREST/api/v1/firm/search.json", data=body,
               headers={"Content-Type": "application/json", "Accept": "application/json"})
    for f in json.loads(raw).get("list", []):
        print(f.get("name"), f.get("ehraid"), f.get("uidFormatted"), f.get("legalSeat"), f.get("status"))


def zefix_firm(ehraid, out):
    raw = _get(f"https://www.zefix.admin.ch/ZefixREST/api/v1/firm/{ehraid}.json",
               headers={"Accept": "application/json"})
    open(out, "wb").write(raw)
    print("saved", len(raw), "bytes")


def sogc_texts(path):
    d = json.load(open(path, encoding="utf-8"))
    for p in d.get("shabPub", []):
        msg = re.sub(r"<[^>]+>", "", html.unescape(p.get("message", "")))
        print("----", p.get("shabDate"), "ID", p.get("shabId"), "journal", p.get("registryOfficeJournalId"),
              p.get("registryOfficeJournalDate"))
        print(msg)


def sogc_pdf(sogc_id, out):
    raw = _get(f"https://www.shab.ch/shabforms/servlet/Search?EID=7&DOCID={sogc_id}")
    open(out, "wb").write(raw)
    print("saved", len(raw), "bytes, starts", raw[:8])


def snb(cube, frm, to, dimsel=None):
    q = {"fromDate": frm, "toDate": to}
    if dimsel:
        q["dimSel"] = dimsel
    url = f"https://data.snb.ch/api/cube/{cube}/data/csv/en?" + urllib.parse.urlencode(q)
    print(_get(url).decode("utf-8-sig", "replace"))


def page_grep(path, patterns, width=200):
    raw = open(path, "rb").read()
    for enc in ("utf-8", "gb18030"):
        try:
            t = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    s = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))
    for p in patterns:
        for m in list(re.finditer(p, s))[:3]:
            print(f"[{p}] ...{s[max(0, m.start() - width):m.end() + width]}...")


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "zefix-search":
        zefix_search(args[0])
    elif cmd == "zefix-firm":
        zefix_firm(args[0], args[1])
    elif cmd == "sogc-texts":
        sogc_texts(args[0])
    elif cmd == "sogc-pdf":
        sogc_pdf(args[0], args[1])
    elif cmd == "snb":
        snb(args[0], args[1], args[2], args[3] if len(args) > 3 else None)
    elif cmd == "page-grep":
        page_grep(args[0], args[1:])
