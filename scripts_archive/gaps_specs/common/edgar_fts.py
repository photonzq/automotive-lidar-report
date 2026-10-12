"""Query the SEC EDGAR full-text search index for phrases in one company's filings.

Endpoint: https://efts.sec.gov/LATEST/search-index (public JSON). The SEC asks
automated clients to identify themselves; this script deliberately sends only a
generic User-Agent without any personal name or e-mail address. The full-text
index answered such requests; the document archive (www.sec.gov/Archives) did
not, so the documents themselves were read through a web browser fetch.

CIKs used: Hesai 0001861737, Aeva 0001789029, Aurora 0001828108,
Innoviz 0001835591.

Usage : python edgar_fts.py <cik> "<phrase>" ["<phrase>" ...]
Output: for each phrase, filing date, form and document id of up to 15 hits.
"""
import sys

import requests

UA = {"User-Agent": "research-script/1.0"}


def search(cik, phrase):
    r = requests.get("https://efts.sec.gov/LATEST/search-index",
                     params={"q": f'"{phrase}"', "ciks": cik}, headers=UA, timeout=60)
    r.raise_for_status()
    return r.json().get("hits", {}).get("hits", [])


def main():
    cik, phrases = sys.argv[1], sys.argv[2:]
    for ph in phrases:
        hits = search(cik, ph)
        print(f"## {ph}: {len(hits)} hit(s)")
        for h in hits[:15]:
            s = h["_source"]
            print("   ", s.get("file_date"), s.get("form"), h["_id"])


if __name__ == "__main__":
    main()
