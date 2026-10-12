"""Scrape the full EIC Fund 'invested companies' portfolio list.

Source: https://eic.ec.europa.eu/eic-fund/eic-fund-invested-companies_en
(paginated, 20 entries per page, ?page=0..N-1). Also downloads the page's RSS
feed (/node/688/rss_en). Saves every page under raw/eic_fund_portfolio/ and a
combined list (name, profile link, one-line description, country, sector) to
eic_fund_portfolio.json and eic_fund_portfolio.csv; then prints any entry whose
name or description matches the search terms given on the command line
(default: voxel, hybrid, lidar).

Run from the eic_fund folder:  python scripts/eic_fund_portfolio_scrape.py
"""
import csv
import json
import re
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE = "https://eic.ec.europa.eu"
LIST = BASE + "/eic-fund/eic-fund-invested-companies_en"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
OUT = Path("raw/eic_fund_portfolio")
OUT.mkdir(parents=True, exist_ok=True)


def parse_page(html: bytes):
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    # each result is an article/card; the company link is an <a> inside a heading
    for card in soup.select("article, div.ecl-content-item"):
        a = card.find("a")
        if not a or not a.get("href"):
            continue
        name = a.get_text(" ", strip=True)
        text = card.get_text("\n", strip=True).split("\n")
        country = sector = desc = ""
        for i, t in enumerate(text):
            if t == "Country" and i + 1 < len(text):
                country = text[i + 1]
            if t == "Sector" and i + 1 < len(text):
                sector = text[i + 1]
        try:
            idx = text.index(name)
            desc = text[idx + 1] if idx + 1 < len(text) and text[idx + 1] != "Country" else ""
        except ValueError:
            pass
        rows.append({"name": name, "href": a["href"], "description": desc,
                     "country": country, "sector": sector})
    return soup, rows


def main(terms):
    s = requests.Session()
    s.headers.update({"User-Agent": UA})
    r = s.get(LIST, timeout=60)
    (OUT / "page_00.html").write_bytes(r.content)
    soup, rows = parse_page(r.content)
    total_txt = soup.find(string=re.compile(r"Showing results"))
    last = 0
    for a in soup.select("a[href*='?page=']"):
        m = re.search(r"page=(\d+)", a["href"])
        if m:
            last = max(last, int(m.group(1)))
    print("first page rows:", len(rows), "| last page index:", last, "|", total_txt)
    allrows = list(rows)
    for p in range(1, last + 1):
        time.sleep(1.0)
        rp = s.get(LIST + f"?page={p}", timeout=60)
        (OUT / f"page_{p:02d}.html").write_bytes(rp.content)
        _, rr = parse_page(rp.content)
        print(f"page {p}: {len(rr)} rows")
        allrows.extend(rr)
    # de-duplicate on href
    seen, uniq = set(), []
    for row in allrows:
        if row["href"] in seen:
            continue
        seen.add(row["href"])
        uniq.append(row)
    Path("eic_fund_portfolio.json").write_text(json.dumps(uniq, indent=1, ensure_ascii=False), encoding="utf-8")
    with open("eic_fund_portfolio.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["name", "href", "description", "country", "sector"])
        w.writeheader()
        w.writerows(uniq)
    print("unique entries:", len(uniq))
    rss = s.get(BASE + "/node/688/rss_en", timeout=60)
    (OUT / "rss.xml").write_bytes(rss.content)
    print("rss bytes:", len(rss.content), rss.headers.get("Content-Type"))
    for row in uniq:
        blob = (row["name"] + " " + row["description"]).lower()
        if any(t in blob for t in terms):
            print("MATCH:", row)
    for c in ("Belgium", "Germany"):
        print(f"--- {c} entries ---")
        for row in uniq:
            if row["country"] == c:
                print("  ", row["name"], "|", row["sector"], "|", row["description"][:90])


if __name__ == "__main__":
    main([t.lower() for t in (sys.argv[1:] or ["voxel", "hybrid", "lidar"])])
