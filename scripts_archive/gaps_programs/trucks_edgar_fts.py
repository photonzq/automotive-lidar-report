"""Query the SEC EDGAR full-text search index and list matching filings.

Purpose
    Locate SEC filings (10-K, 10-Q, 8-K exhibits, S-4, proxy, 20-F, 6-K, ARS) that mention
    lidar suppliers or autonomous-truck operators, for the report's Appendix 1 items on
    Aurora, Kodiak, PlusAI/Churchill IX, Hesai, Ouster, Aeva, Luminar, MicroVision, Gatik,
    Avride, May Mobility, Waabi and Bot Auto. Only the public search index is queried; the
    documents themselves are opened separately.

Inputs (command line)
    --q "QUERY"            EDGAR full-text query (quote phrases inside, e.g. '"lidar" Gatik')
    --ciks CIK [CIK ...]   optional filer CIKs (10 digits or shorter; zero-padded here)
    --forms F [F ...]      optional form filter, e.g. 10-K 10-Q 8-K S-4
    --start / --end        optional date range YYYY-MM-DD
    --out DIR              folder for the raw JSON responses (default: ./data)
    --pages N              result pages to fetch, 100 hits per page (default 1)

Outputs
    DIR/edgar_fts_<hash>.json   raw JSON response(s)
    stdout                      one line per hit: file date, form, filer, accession,
                                document name and the Archives URL of the document

Notes
    A generic browser-like User-Agent is used; no contact details are sent.
Date: 2026-10-03
"""
import argparse
import hashlib
import json
import os
import sys
import time
import urllib.parse

import requests

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
BASE = "https://efts.sec.gov/LATEST/search-index"


def main():
    try:  # avoid console code-page errors on Windows
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", required=True)
    ap.add_argument("--ciks", nargs="*", default=[])
    ap.add_argument("--forms", nargs="*", default=[])
    ap.add_argument("--start")
    ap.add_argument("--end")
    ap.add_argument("--out", default="data")
    ap.add_argument("--pages", type=int, default=1)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    params = {"q": a.q}
    if a.ciks:
        params["ciks"] = ",".join(c.zfill(10) for c in a.ciks)
    if a.forms:
        params["forms"] = ",".join(a.forms)
    if a.start or a.end:
        params["dateRange"] = "custom"
        params["startdt"] = a.start or "2001-01-01"
        params["enddt"] = a.end or time.strftime("%Y-%m-%d")
    total_seen = 0
    for page in range(a.pages):
        if page:
            params["from"] = str(page * 100)
        url = BASE + "?" + urllib.parse.urlencode(params)
        r = requests.get(url, headers={"User-Agent": UA, "Accept": "application/json"}, timeout=60)
        if r.status_code != 200:
            print("HTTP", r.status_code, url)
            print(r.text[:300])
            return 1
        js = r.json()
        tag = hashlib.md5(url.encode()).hexdigest()[:8]
        with open(os.path.join(a.out, f"edgar_fts_{tag}.json"), "w", encoding="utf-8") as fh:
            json.dump(js, fh, indent=1)
        hits = js.get("hits", {}).get("hits", [])
        total = js.get("hits", {}).get("total", {}).get("value")
        if page == 0:
            print(f"query={a.q!r} ciks={params.get('ciks', '-')} forms={params.get('forms', '-')} "
                  f"total={total}")
        for h in hits:
            src = h.get("_source", {})
            adsh, _, doc = h.get("_id", "").partition(":")
            cik = (src.get("ciks") or ["?"])[0].lstrip("0")
            link = (f"https://www.sec.gov/Archives/edgar/data/{cik}/"
                    f"{adsh.replace('-', '')}/{doc}")
            name = (src.get("display_names") or ["?"])[0][:60]
            print(f"{src.get('file_date')} {src.get('form'):8s} {name:60s} {adsh} {doc}\n    {link}")
            total_seen += 1
        if len(hits) < 100:
            break
        time.sleep(0.5)
    print("hits listed:", total_seen)
    return 0


if __name__ == "__main__":
    sys.exit(main())
