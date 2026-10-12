"""Run Google Patents search queries (public xhr endpoint) and print a compact
table: publication number, priority date, title, assignee, inventor.

Usage:
    python item5a_gpatents_query.py OUTDIR "QUERY_URL_PART" [MAXPAGES]

QUERY_URL_PART is the part after '?' in a patents.google.com search URL,
unencoded, e.g. 'assignee=Strobe Inc&num=100' or
'inventor=Lutfollah Maleki&assignee=GM Global Technology Operations&num=100'.
Results (raw JSON per page) are saved in OUTDIR as query_<n>_p<page>.json.
"""
import html
import json
import os
import re
import sys
import time
import urllib.parse

import requests

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def clean(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    return html.unescape(s).strip()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    outdir, q = sys.argv[1], sys.argv[2]
    maxpages = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    os.makedirs(outdir, exist_ok=True)
    tag = re.sub(r"[^A-Za-z0-9]+", "_", q)[:60]
    seen = set()
    for page in range(maxpages):
        part = q + ("&page=%d" % page if page else "")
        url = "https://patents.google.com/xhr/query?url=" + urllib.parse.quote(part, safe="") + "&exp="
        r = requests.get(url, headers=UA, timeout=60)
        if r.status_code != 200:
            print("HTTP", r.status_code)
            break
        data = r.json()
        with open(os.path.join(outdir, "query_%s_p%d.json" % (tag, page)), "w", encoding="utf-8") as f:
            json.dump(data, f)
        res = data.get("results", {})
        if page == 0:
            print("TOTAL:", res.get("total_num_results"), "PAGES:", res.get("total_num_pages"))
        n = 0
        for cl in res.get("cluster", []):
            for it in cl.get("result", []):
                p = it.get("patent", {})
                pn = p.get("publication_number")
                if pn in seen:
                    continue
                seen.add(pn)
                n += 1
                print("%-16s | pri %s | pub %s | %s | A: %s | I: %s" % (
                    pn, p.get("priority_date"), p.get("publication_date"),
                    clean(p.get("title"))[:110], clean(p.get("assignee"))[:50],
                    clean(p.get("inventor"))[:60]))
        if n == 0 or page + 1 >= (res.get("total_num_pages") or 1):
            break
        time.sleep(1.0)


if __name__ == "__main__":
    main()
