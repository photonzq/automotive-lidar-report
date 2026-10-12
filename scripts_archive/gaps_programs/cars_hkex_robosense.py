"""List RoboSense (HKEX 2498) filings, download the results announcements and grep customer descriptions.

Purpose: trace RoboSense's unnamed-customer wording ("emerging global electric pickup truck
brand", "leading global manufacturer of SUVs and trucks", the European and Japanese JV
wins) behind the Rivian supplier question and the VW/Toyota/Nissan JV items.
Usage:   python cars_hkex_robosense.py [LANG]   (LANG = E for English, ZH for Chinese; default E)
Outputs: PDFs saved in ./robosense/, matches printed with page numbers.
Date:    2026-10-03
HKEX internal stock id for 02498 is 1000211551 (from the HKEX prefix lookup).
"""
import json
import os
import re
import sys

import pymupdf
import requests

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"
KEYS_E = r"(North Americ|SUVs and trucks|pickup|global top|top-tier|Top 3 OEMs|largest Europe|joint venture)"
KEYS_ZH = r"(SUV|皮卡|北美|日本|歐洲|合資)"


def list_filings(lang):
    p = {"sortDir": "0", "sortByOptions": "DateTime", "category": "0", "market": "SEHK",
         "stockId": "1000211551", "documentType": "-1", "fromDate": "20250101", "toDate": "20261003",
         "title": "", "searchType": "0", "t1code": "-2", "t2Gcode": "-2", "t2code": "-2",
         "rowRange": "200", "lang": lang}
    r = requests.get("https://www1.hkexnews.hk/search/titleSearchServlet.do", params=p,
                     headers={"User-Agent": UA}, timeout=30)
    return json.loads(r.json()["result"])


def main():
    lang = sys.argv[1] if len(sys.argv) > 1 else "E"
    os.makedirs("robosense", exist_ok=True)
    pat = re.compile(KEYS_ZH if lang == "ZH" else KEYS_E, re.I)
    for x in list_filings(lang):
        title = re.sub(r"<[^>]+>", " ", x["TITLE"])
        if not re.search(r"RESULT|BUSINESS UPDATE|業績|業務更新", title, re.I):
            continue
        url = "https://www1.hkexnews.hk" + x["FILE_LINK"]
        fn = os.path.join("robosense", os.path.basename(url))
        if not os.path.exists(fn):
            open(fn, "wb").write(requests.get(url, headers={"User-Agent": UA}, timeout=60).content)
        print("=====", x["DATE_TIME"], title.strip()[:80], url)
        for i, page in enumerate(pymupdf.open(fn)):
            t = re.sub(r"\s+", " ", page.get_text())
            for m in pat.finditer(t):
                print(f"  p{i + 1}: ...{t[max(0, m.start() - 250): m.end() + 250]}...")


if __name__ == "__main__":
    main()
