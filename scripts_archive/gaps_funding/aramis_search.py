"""ARAMIS, the Swiss federal research-project database (aramis.admin.ch): project details.

Usage:  python aramis_search.py OUTDIR --ids ID [ID ...]
        python aramis_search.py OUTDIR term [term ...]      (see the caveat below)

--ids mode (the one used for the report): for each ARAMIS ProjectID, saves the "Basic
data" (Grunddaten), "Participants" (Beteiligte) and "Texts" (Texte) pages and prints
project number, title, status, dates, granted total costs, research partner and
implementation partner. E-mail addresses in the pages are masked in the printout.
ProjectIDs used: 35043 and 37602 (Fastree3D's CTI projects 16607.1 and 18345.1),
58359 (Innosuisse 128.726, Chirp Light AG) and 57060 (SERI 24.00114, RETINA).

Caveat on term search: ARAMIS's search runs through an ASP.NET AJAX update panel on
/Projektsuche/. A plain form post of the header search box returns the home page
without results (Oct 2026), so term searches ("Pointcloud", "Nicolaescu", "Fastree3D",
"FMCW", "lidar") were run in a browser on https://www.aramis.admin.ch/Projektsuche/ and
the ProjectIDs taken from the result links. The term mode below is kept for reference.
"""
import os
import re
import sys
import time
from html import unescape

import requests

BASE = "https://www.aramis.admin.ch"
HEADERS = {"User-Agent": "research-script/1.0"}


def text(html):
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    txt = re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", html))).strip()
    return re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "[email]", txt)


def details(s, out, pid):
    parts = {}
    for kind in ("Grunddaten", "Beteiligte", "Texte"):
        h = s.get(f"{BASE}/{kind}/?ProjectID={pid}&Sprache=en-US", timeout=60).text
        with open(os.path.join(out, f"aramis_{pid}_{kind}.html"), "w", encoding="utf-8") as f:
            f.write(h)
        t = text(h)
        i = t.find("Project number")
        parts[kind] = t[i:i + 1500] if i >= 0 else t[:800]
        time.sleep(1)
    print(f"\n=== ProjectID {pid}")
    for kind, t in parts.items():
        print(f"  [{kind}] {t}")


def term_search(s, out, term):
    home = s.get(BASE + "/Projektsuche/?Sprache=en-US", timeout=60).text
    data = {m.group(1): unescape(m.group(2)) for m in re.finditer(
        r'<input type="hidden" name="([^"]+)" id="[^"]*" value="([^"]*)"', home)}
    data.update({"ctl00$cphContent$txtSearch": term, "ctl00$cphContent$cmdSearch.x": "1",
                 "ctl00$cphContent$cmdSearch.y": "1"})
    r = s.post(BASE + "/Projektsuche/?Sprache=en-US", data=data, timeout=120)
    ids = list(dict.fromkeys(re.findall(r"ProjectID=(\d+)", r.text)))
    with open(os.path.join(out, f"aramis_search_{re.sub(r'[^A-Za-z0-9]', '_', term)}.html"),
              "w", encoding="utf-8") as f:
        f.write(r.text)
    print(f"'{term}': {len(ids)} ProjectIDs in the response {ids[:30]}")


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    s = requests.Session()
    s.headers.update(HEADERS)
    if len(sys.argv) > 2 and sys.argv[2] == "--ids":
        for pid in sys.argv[3:]:
            details(s, out, pid)
    else:
        for term in sys.argv[2:]:
            term_search(s, out, term)


if __name__ == "__main__":
    main()
