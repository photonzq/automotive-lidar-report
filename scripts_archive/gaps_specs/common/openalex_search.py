"""Search OpenAlex for works by free text and print DOI, title, venue, year and
the abstract rebuilt from OpenAlex's inverted index.

Used to find coherent-lidar receiver papers and semiconductor-optical-amplifier
(SOA) and CW-laser efficiency-versus-temperature papers. No contact details are
sent (no mailto parameter, generic User-Agent).

Usage : python openalex_search.py "<query>" [--from 2021-01-01] [--n 8]
Output: printed list of works with abstracts (UTF-8).
"""
import argparse
import sys

import requests

UA = {"User-Agent": "Mozilla/5.0 research-script/1.0"}
sys.stdout.reconfigure(encoding="utf-8")


def abstract(inv):
    if not inv:
        return ""
    pos = {i: w for w, ids in inv.items() for i in ids}
    return " ".join(pos[i] for i in sorted(pos))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--from", dest="date_from", default="2021-01-01")
    ap.add_argument("--n", type=int, default=8)
    a = ap.parse_args()
    r = requests.get("https://api.openalex.org/works",
                     params={"search": a.query, "per-page": a.n,
                             "filter": f"from_publication_date:{a.date_from}"},
                     headers=UA, timeout=60)
    for w in r.json().get("results", []):
        src = ((w.get("primary_location") or {}).get("source") or {}).get("display_name")
        print(w.get("doi"), "|", w.get("title"), "|", src, "|", w.get("publication_year"))
        ab = abstract(w.get("abstract_inverted_index"))
        if ab:
            print("    ABS:", ab[:1200])


if __name__ == "__main__":
    main()
