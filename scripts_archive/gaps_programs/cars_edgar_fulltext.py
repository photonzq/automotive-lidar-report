"""Query the SEC EDGAR full-text search for a phrase, optionally limited by CIK, form and dates.

Purpose: check whether Rivian (CIK 1874178), GM (1467858), Ford (37996), MicroVision (65770)
and Luminar (1758057) filings mention lidar suppliers or Nissan (Appendix 1 passenger-car items).
Usage:   python cars_edgar_fulltext.py "QUERY" [CIKS] [FORMS] [START YYYY-MM-DD] [END YYYY-MM-DD]
         e.g. python cars_edgar_fulltext.py '"lidar"' 0001874178 "" 2025-06-01 2026-10-03
Outputs: prints total hits and, per hit, filing date, form, filer and document URL.
Date:    2026-10-03
The request carries a generic User-Agent only (no name or contact address).
"""
import sys

import requests

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) research-script"


def main():
    params = {"q": sys.argv[1]}
    if len(sys.argv) > 2 and sys.argv[2]:
        params["ciks"] = sys.argv[2]
    if len(sys.argv) > 3 and sys.argv[3]:
        params["forms"] = sys.argv[3]
    if len(sys.argv) > 5:
        params.update({"dateRange": "custom", "startdt": sys.argv[4], "enddt": sys.argv[5]})
    d = requests.get("https://efts.sec.gov/LATEST/search-index", params=params,
                     headers={"User-Agent": UA}, timeout=60).json()
    hits = d.get("hits", {}).get("hits", [])
    print("total", d.get("hits", {}).get("total"))
    for h in hits[:100]:
        s = h["_source"]
        adsh, fn = h["_id"].split(":")
        cik = s["ciks"][0].lstrip("0")
        url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{adsh.replace('-', '')}/{fn}"
        print(s.get("file_date"), s.get("form"), s.get("display_names", [""])[0][:50], url)


if __name__ == "__main__":
    main()
