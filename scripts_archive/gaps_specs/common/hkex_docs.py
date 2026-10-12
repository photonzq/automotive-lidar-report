"""List and download HKEX filings (prospectuses, annual reports) for a listed company.

Uses the public HKEXnews endpoints that the title-search web page calls:
  1. prefix.do          -> maps a stock code (e.g. 2525 Hesai, 2498 RoboSense)
                           to the internal stockId;
  2. titleSearchServlet -> lists documents for a date window.
Matching documents can then be downloaded as PDF.

No login and no contact details are sent; a generic browser User-Agent is used.

Usage : python hkex_docs.py <stock_code> <from YYYYMMDD> <to YYYYMMDD>
            [--match "GLOBAL OFFERING,ANNUAL REPORT"] [--download]
Output: prints date | title | link | size; with --download, saves the PDFs
        to the folder given by GAPS_SPECS_RAW (default ".").
"""
import argparse
import json
import os
import re

import requests

BASE = "https://www1.hkexnews.hk"
UA = {"User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                     "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")}
OUT = os.environ.get("GAPS_SPECS_RAW", ".")


def stock_id(code):
    r = requests.get(f"{BASE}/search/prefix.do",
                     params={"callback": "callback", "lang": "EN", "type": "A",
                             "name": code, "market": "SEHK"},
                     headers=UA, timeout=30)
    m = re.search(r'"stockId":(\d+),"code":"0*%s"' % re.escape(code.lstrip("0")), r.text)
    if not m:
        m = re.search(r'"stockId":(\d+)', r.text)
    return m.group(1) if m else None


def list_docs(sid, date_from, date_to):
    params = {"sortDir": "0", "sortByOptions": "DateTime", "category": "0", "market": "SEHK",
              "stockId": sid, "documentType": "-1", "fromDate": date_from, "toDate": date_to,
              "title": "", "searchType": "0", "t1code": "-2", "t2Gcode": "-2", "t2code": "-2",
              "rowRange": "200", "lang": "E"}
    r = requests.get(f"{BASE}/search/titleSearchServlet.do", params=params, headers=UA, timeout=60)
    res = r.json().get("result")
    return json.loads(res) if res else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("code")
    ap.add_argument("date_from")
    ap.add_argument("date_to")
    ap.add_argument("--match", default="")
    ap.add_argument("--download", action="store_true")
    a = ap.parse_args()
    sid = stock_id(a.code)
    print("stockId:", sid)
    keys = [k.strip().upper() for k in a.match.split(",") if k.strip()]
    for it in list_docs(sid, a.date_from, a.date_to):
        title = it.get("TITLE", "").replace("\n", " ")
        if keys and not any(k in title.upper() for k in keys):
            continue
        link = it.get("FILE_LINK")
        print(it.get("DATE_TIME"), "|", title[:110], "|", link, "|", it.get("FILE_INFO"))
        if a.download and link and link.lower().endswith(".pdf"):
            pdf = requests.get(BASE + link, headers=UA, timeout=400)
            fn = os.path.join(OUT, f"hkex_{a.code}_{os.path.basename(link)}")
            with open(fn, "wb") as fh:
                fh.write(pdf.content)
            print("   saved", fn, len(pdf.content), "bytes")


if __name__ == "__main__":
    main()
