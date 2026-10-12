"""List Google Patents results for a query via the public xhr endpoint.

Usage:
  python gpatents.py "<url-query>" [maxpages]
     e.g. python gpatents.py "assignee=Fortsense&q=(high+reflectivity)"
Saves raw JSON pages under gp_json/ and prints one line per result:
  publication_number | priority | publication date | assignee | title
"""
import sys
import os
import json
import time
import html
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
HERE = os.path.dirname(os.path.abspath(__file__))


def fetch(qs):
    url = "https://patents.google.com/xhr/query?url=" + urllib.parse.quote(qs, safe="") + "&exp="
    for k in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            last = e
            time.sleep(4 * (k + 1))
    raise last


def main():
    base = sys.argv[1]
    maxpages = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    os.makedirs(os.path.join(HERE, "gp_json"), exist_ok=True)
    seen = set()
    total = None
    for page in range(maxpages):
        qs = f"{base}&num=100&page={page}"
        data = fetch(qs)
        tag = urllib.parse.quote(base, safe="")[:80]
        with open(os.path.join(HERE, "gp_json", f"{tag}_p{page}.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        res = data.get("results", {})
        total = res.get("total_num_results")
        n = 0
        for cl in res.get("cluster", []):
            for item in cl.get("result", []):
                p = item["patent"]
                pn = p.get("publication_number")
                if pn in seen:
                    continue
                seen.add(pn)
                n += 1
                title = html.unescape(p.get("title", "")).strip()
                print(f"{pn} | prio {p.get('priority_date')} | pub {p.get('publication_date')} | "
                      f"{html.unescape(p.get('assignee', ''))} | {title}")
        if n == 0 or page + 1 >= res.get("total_num_pages", 0):
            break
        time.sleep(2)
    print(f"# total_num_results={total}, listed={len(seen)}")


if __name__ == "__main__":
    main()
