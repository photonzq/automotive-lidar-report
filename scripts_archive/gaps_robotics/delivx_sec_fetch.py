"""Download SEC EDGAR filings for one company and search them for keywords.

Used for the "Delivery robots outside China" open item of the automotive
perception report (Appendix 1; section B4a, subsection 4): Serve Robotics'
lidars per robot, fleet counts and lidar purchase commitments, and any
Ouster disclosure about the Serve supply agreement.

How it works
------------
1. ``list``: reads ``https://data.sec.gov/submissions/CIK##########.json``
   and prints the filings (date, form, accession number, primary document,
   8-K items) from a start date onwards, optionally filtered by form type.
2. ``get``: for each accession number given, reads the filing index
   (``https://www.sec.gov/Archives/edgar/data/<cik>/<acc>/index.json``) and
   downloads every ``.htm``/``.txt`` document (the main filing and its
   exhibits, e.g. the earnings press release filed as Exhibit 99.1) into
   ``<out>/<accession>/``.
3. ``grep``: strips the HTML of every downloaded document under ``<out>``
   and prints each keyword hit with surrounding context, so that the
   paragraph can then be read in full at the source.

SEC asks automated clients to identify themselves in the User-Agent header
and to stay under 10 requests per second. Set the environment variable
``SEC_UA`` to a generic tool name plus a placeholder contact at the reserved
example domain (never a real address); the built-in default is only a
generic tool name. No personal data is sent.

Usage
-----
    python delivx_sec_fetch.py list 1832483 --since 2024-01-01 --forms 10-K,10-Q,8-K
    python delivx_sec_fetch.py get 1832483 0001832483-26-000010 0001832483-26-000035 --out sec_serv
    python delivx_sec_fetch.py grep --out sec_serv --pattern "lidar|Ouster|purchase obligation" --context 400

CIKs used for this item: Serve Robotics 1832483; Ouster 1816581.
"""
import argparse
import html
import json
import os
import re
import sys
import time
import urllib.request

UA = {"User-Agent": os.environ.get("SEC_UA", "research-script")}


def fetch(url, binary=False, tries=3):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=90) as r:
                data = r.read()
            time.sleep(0.15)  # stay well below SEC's 10 requests/s limit
            return data if binary else data.decode("utf-8", errors="replace")
        except Exception as e:  # noqa: BLE001
            if k == tries - 1:
                raise
            time.sleep(2 + 2 * k)


def cmd_list(a):
    cik10 = str(int(a.cik)).zfill(10)
    d = json.loads(fetch(f"https://data.sec.gov/submissions/CIK{cik10}.json"))
    rec = d["filings"]["recent"]
    forms = set(a.forms.split(",")) if a.forms else None
    print(d.get("name"))
    for i in range(len(rec["form"])):
        if rec["filingDate"][i] < a.since:
            continue
        if forms and rec["form"][i] not in forms:
            continue
        print(rec["filingDate"][i], rec["form"][i], rec["accessionNumber"][i],
              rec["primaryDocument"][i], rec.get("items", [""] * len(rec["form"]))[i])


def cmd_get(a):
    cik = str(int(a.cik))
    for acc in a.accessions:
        accn = acc.replace("-", "")
        folder = os.path.join(a.out, acc)
        os.makedirs(folder, exist_ok=True)
        idx = json.loads(fetch(f"https://www.sec.gov/Archives/edgar/data/{cik}/{accn}/index.json"))
        for item in idx["directory"]["item"]:
            name = item["name"]
            if not re.search(r"\.(htm|html|txt)$", name, re.I):
                continue
            if name.endswith("-index.html") or name.endswith("-index-headers.html"):
                continue
            if a.skip_full_txt and re.fullmatch(r"\d{10}-\d{2}-\d{6}\.txt", name):
                continue
            if re.fullmatch(r"R\d+\.htm", name):  # XBRL viewer fragments; the main document has the same text
                continue
            dest = os.path.join(folder, name)
            if os.path.exists(dest):
                continue
            url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accn}/{name}"
            try:
                data = fetch(url, binary=True)
            except Exception as e:  # noqa: BLE001
                print("FAILED", url, e)
                continue
            with open(dest, "wb") as f:
                f.write(data)
            print("saved", dest, len(data))


def strip_html(raw):
    raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
    raw = re.sub(r"(?is)<ix:header>.*?</ix:header>", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    return re.sub(r"\s+", " ", raw)


def cmd_grep(a):
    pat = re.compile(a.pattern, re.I)
    for root, _, files in os.walk(a.out):
        for fn in sorted(files):
            if not re.search(r"\.(htm|html|txt)$", fn, re.I) or re.fullmatch(r"R\d+\.htm", fn):
                continue
            path = os.path.join(root, fn)
            with open(path, "rb") as f:
                text = strip_html(f.read().decode("utf-8", errors="replace"))
            hits = list(pat.finditer(text))
            if not hits:
                continue
            print(f"\n===== {os.path.relpath(path, a.out)}  ({len(hits)} hits)")
            last_end = -1
            for m in hits:
                s = max(0, m.start() - a.context)
                e = min(len(text), m.end() + a.context)
                if s < last_end:  # merge overlapping windows
                    continue
                print("...", text[s:e], "...\n")
                last_end = e


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    pl = sub.add_parser("list")
    pl.add_argument("cik")
    pl.add_argument("--since", default="2024-01-01")
    pl.add_argument("--forms", default="")
    pg = sub.add_parser("get")
    pg.add_argument("cik")
    pg.add_argument("accessions", nargs="+")
    pg.add_argument("--out", default="sec_filings")
    pg.add_argument("--skip-full-txt", action="store_true", default=True)
    pr = sub.add_parser("grep")
    pr.add_argument("--out", default="sec_filings")
    pr.add_argument("--pattern", required=True)
    pr.add_argument("--context", type=int, default=300)
    a = p.parse_args()
    {"list": cmd_list, "get": cmd_get, "grep": cmd_grep}[a.cmd](a)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
