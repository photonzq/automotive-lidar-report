"""Independent re-check of the EIC Fund's public list of invested companies.

Usage:  python eic_fund_portfolio_check.py [OUT_DIR] [term ...]
Pages through https://eic.ec.europa.eu/eic-fund/eic-fund-invested-companies_en until no
new entries appear, saves each page, and counts case-insensitive matches of each term
across all pages (default terms: two lidar companies plus three companies known to be on
the list as positive controls). No personal data is sent.
"""
import glob
import html
import os
import re
import sys
import time

import requests

BASE = "https://eic.ec.europa.eu/eic-fund/eic-fund-invested-companies_en"
HEADERS = {"User-Agent": "research-script/1.0"}
DEFAULT_TERMS = ["voxel", "hybrid lidar", "lidar", "LiSSA", "Swave", "iPronics", "Vitestro"]


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "eic_fund_check"
    terms = sys.argv[2:] or DEFAULT_TERMS
    os.makedirs(out, exist_ok=True)
    names = []
    for p in range(0, 40):
        r = requests.get(BASE, params={"page": p}, headers=HEADERS, timeout=60)
        if r.status_code != 200:
            print("page", p, "HTTP", r.status_code)
            break
        with open(os.path.join(out, f"eicfund_page_{p:02d}.html"), "w", encoding="utf-8") as f:
            f.write(r.text)
        items = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", x))).strip()
                 for x in re.findall(r'<a[^>]+href="/eic-fund/[^"]+"[^>]*>(.*?)</a>', r.text,
                                     flags=re.S)]
        new = [x for x in items if x and x not in names]
        if not new:
            break
        names += new
        time.sleep(1)
    txt = " ".join(open(f, encoding="utf-8").read()
                   for f in glob.glob(os.path.join(out, "eicfund_page_*.html")))
    print(f"pages read: {p}; link entries collected (incl. navigation): {len(names)}")
    for k in terms:
        print(f"{k!r}: {len(re.findall(re.escape(k), txt, re.I))} matches")


if __name__ == "__main__":
    main()
