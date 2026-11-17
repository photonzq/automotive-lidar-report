"""Search Wikimedia Commons files and print licence, size and URL.

Usage: python -I commons_search.py "query one" "query two" ...
Uses the public MediaWiki API with a generic User-Agent; no personal data sent.
"""
import json
import re
import sys
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
UA = "report-check/1.0 (research)"
API = "https://commons.wikimedia.org/w/api.php"


def get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def strip(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


for q in sys.argv[1:]:
    print("=" * 20, q, "=" * 20)
    res = get({"action": "query", "list": "search", "srsearch": q, "srnamespace": 6,
               "srlimit": 25, "format": "json"})
    titles = [h["title"] for h in res.get("query", {}).get("search", [])]
    if not titles:
        print("  (no results)")
        continue
    for i in range(0, len(titles), 20):
        chunk = titles[i:i + 20]
        info = get({"action": "query", "titles": "|".join(chunk), "prop": "imageinfo",
                    "iiprop": "url|size|extmetadata", "format": "json"})
        for page in info.get("query", {}).get("pages", {}).values():
            ii = (page.get("imageinfo") or [{}])[0]
            md = ii.get("extmetadata", {})
            lic = strip(md.get("LicenseShortName", {}).get("value"))
            art = strip(md.get("Artist", {}).get("value"))[:60]
            desc = strip(md.get("ImageDescription", {}).get("value"))[:140]
            date = strip(md.get("DateTimeOriginal", {}).get("value"))[:20]
            print(f"- {page.get('title')} | {ii.get('width')}x{ii.get('height')} | {lic} | {art} | {date}")
            print(f"    url: {ii.get('url')}")
            print(f"    page: {ii.get('descriptionurl')}")
            if desc:
                print(f"    desc: {desc}")
