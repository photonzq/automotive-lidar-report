"""List and download HKEX (Hong Kong Stock Exchange) filings for a listed company.

Used for the robotics-lidar open items of the automotive perception report
(Appendix 1: robotics revenue, robot lidar by type, robotics-lidar prices).

How it works
------------
1. ``prefix.do`` maps a stock code (e.g. ``02498`` for RoboSense) to HKEX's
   internal ``stockId``.
2. ``titleSearchServlet.do`` returns the filing list (date, title, PDF link,
   document category) for that ``stockId`` and a date range.
3. Selected PDFs are downloaded into the output folder given on the command
   line (default: ``./hkex_pdfs`` relative to the working directory).

Usage
-----
    python hkex_fetch.py 02498 --from 20250101 --to 20261003 --list
    python hkex_fetch.py 02498 --from 20250101 --to 20261003 \
        --match "ANNUAL REPORT|INTERIM REPORT|RESULTS|BUSINESS UPDATE" --out hkex_pdfs

For companies that have only filed an application proof (no stock code yet),
HKEX's "Application Proofs and PHIPs" pages must be used instead; this script
does not cover them.

No login, cookie or personal data is sent; only a generic browser User-Agent.
"""
import argparse
import json
import os
import re
import sys
import time

import requests

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124 Safari/537.36"}
BASE = "https://www1.hkexnews.hk"


def stock_id(code: str) -> int:
    """Return HKEX's internal stockId for a 5-digit stock code (active equities)."""
    url = f"{BASE}/search/prefix.do?&callback=callback&lang=EN&type=A&name={code}&market=SEHK"
    txt = requests.get(url, headers=UA, timeout=30).text
    payload = json.loads(re.search(r"callback\((.*)\);?", txt, re.S).group(1))
    for s in payload.get("stockInfo", []):
        if s["code"].lstrip("0") == code.lstrip("0"):
            return int(s["stockId"])
    raise SystemExit(f"stock code {code} not found: {payload}")


def filings(sid: int, date_from: str, date_to: str, lang: str = "E") -> list:
    """Return the HKEX filing list (newest first) for one stockId."""
    url = (f"{BASE}/search/titleSearchServlet.do?sortDir=0&sortByOptions=DateTime&category=0"
           f"&market=SEHK&stockId={sid}&documentType=-1&fromDate={date_from}&toDate={date_to}"
           f"&title=&searchType=0&t1code=-2&t2Gcode=-2&t2code=-2&rowRange=500&lang={lang}")
    d = requests.get(url, headers=UA, timeout=60).json()
    res = d.get("result")
    return json.loads(res) if isinstance(res, str) else (res or [])


def download(link: str, out_dir: str) -> str:
    """Download one filing PDF (skips files already present)."""
    os.makedirs(out_dir, exist_ok=True)
    fn = os.path.join(out_dir, link.rsplit("/", 1)[-1])
    if not os.path.exists(fn):
        r = requests.get(BASE + link, headers=UA, timeout=180)
        r.raise_for_status()
        with open(fn, "wb") as f:
            f.write(r.content)
        time.sleep(1.0)
    return fn


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("code", help="HKEX stock code, e.g. 02498")
    ap.add_argument("--from", dest="dfrom", default="20240101")
    ap.add_argument("--to", dest="dto", default="20261231")
    ap.add_argument("--lang", default="E", help="E (English) or C (Chinese) titles")
    ap.add_argument("--list", action="store_true", help="only print the filing list")
    ap.add_argument("--match", default="", help="regex on titles to download")
    ap.add_argument("--out", default="hkex_pdfs")
    a = ap.parse_args()

    sid = stock_id(a.code)
    rows = filings(sid, a.dfrom, a.dto, a.lang)
    print(f"stockId {sid}: {len(rows)} filings")
    for x in rows:
        title = re.sub(r"\s+", " ", x["TITLE"])
        print(x["DATE_TIME"], "|", title[:140], "|", x["FILE_LINK"])
    if a.list or not a.match:
        return
    pat = re.compile(a.match, re.I)
    for x in rows:
        if pat.search(x["TITLE"]):
            fn = download(x["FILE_LINK"], a.out)
            print("saved", fn, file=sys.stderr)


if __name__ == "__main__":
    main()
