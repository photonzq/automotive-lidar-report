"""china_hkex.py -- list, download and keyword-search HKEX filings of RoboSense (2498) and Hesai (2525).

Purpose
    Pull the HKEXnews filing list for a stock code over a date window, download the
    filings whose titles match a regular expression, and search their text (page by
    page, with PyMuPDF) for keywords such as joint-venture customers, carmaker names
    or model names. Used to look for primary statements about which foreign-brand
    China joint ventures buy RoboSense or Hesai lidar.

Inputs (command line)
    code            HKEX stock code, e.g. 02498 (RoboSense) or 02525 (Hesai)
    --from YYYYMMDD / --to YYYYMMDD   date window for the filing list
    --title REGEX   only download filings whose title matches (case-insensitive)
    --keys K1;K2    semicolon-separated regular expressions (case-insensitive; use (?-i:...)
                    for case-sensitive parts); hits printed with page numbers
    --data DIR      data folder (default ./data_hkex)

Outputs
    DIR/hkex_list_<code>.json   raw filing list returned by HKEXnews
    DIR/<code>_<file>.pdf       downloaded filings
    stdout: page-numbered keyword hits (about 160 characters around each hit)

Notes
    Uses the public HKEXnews title-search endpoints; no login. A generic browser
    User-Agent is sent; no contact details.

Date: 2026-10-03
"""
import argparse
import json
import os
import re
import sys
import time

import pymupdf
import requests

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
H = {"User-Agent": UA}
BASE = "https://www1.hkexnews.hk"


def stock_id(code):
    r = requests.get(f"{BASE}/search/prefix.do?&callback=callback&lang=EN&type=A&name={code}&market=SEHK",
                     headers=H, timeout=30)
    j = json.loads(r.text[r.text.index("(") + 1:r.text.rindex(")")])
    for s in j["stockInfo"]:
        if s["code"] == code:
            return s["stockId"]
    raise SystemExit(f"stock {code} not found")


def filing_list(sid, d0, d1):
    url = (f"{BASE}/search/titleSearchServlet.do?sortDir=0&sortByOptions=DateTime&category=0&market=SEHK"
           f"&stockId={sid}&documentType=-1&fromDate={d0}&toDate={d1}&title=&searchType=0"
           "&t1code=-2&t2Gcode=-2&t2code=-2&rowRange=300&lang=E")
    r = requests.get(url, headers=H, timeout=60)
    j = json.loads(r.text)
    res = json.loads(j["result"]) if isinstance(j.get("result"), str) else (j.get("result") or [])
    return r.text, res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("code")
    ap.add_argument("--from", dest="d0", default="20250101")
    ap.add_argument("--to", dest="d1", default="20261003")
    ap.add_argument("--title", default="RESULTS|REPORT|BUSINESS UPDATE|GLOBAL OFFERING")
    ap.add_argument("--keys", default="joint venture;Volkswagen;European")
    ap.add_argument("--data", default="data_hkex")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    os.makedirs(a.data, exist_ok=True)
    sid = stock_id(a.code)
    raw, res = filing_list(sid, a.d0, a.d1)
    with open(os.path.join(a.data, f"hkex_list_{a.code}.json"), "w", encoding="utf-8") as f:
        f.write(raw)
    keys = [k.strip() for k in a.keys.split(";") if k.strip()]
    for x in res:
        title = re.sub(r"<[^>]+>", "", x.get("TITLE", "")).replace("\n", " ")
        link = x.get("FILE_LINK", "")
        if not link.lower().endswith(".pdf") or not re.search(a.title, title, re.I):
            continue
        fn = os.path.join(a.data, f"{a.code}_{os.path.basename(link)}")
        if not os.path.exists(fn):
            r = requests.get(BASE + link, headers=H, timeout=120)
            with open(fn, "wb") as f:
                f.write(r.content)
            time.sleep(1.0)
        print(f"\n### {x.get('DATE_TIME')} | {title} | {BASE + link}")
        try:
            doc = pymupdf.open(fn)
        except Exception as e:  # noqa: BLE001
            print("   cannot open:", e)
            continue
        for pno in range(doc.page_count):
            t = doc[pno].get_text()
            flat = re.sub(r"\s+", " ", t)
            for k in keys:
                for m in re.finditer(k, flat, re.I):
                    s = max(0, m.start() - 160)
                    print(f"   p{pno + 1} [{k}] ...{flat[s:m.end() + 160]}...")


if __name__ == "__main__":
    main()
