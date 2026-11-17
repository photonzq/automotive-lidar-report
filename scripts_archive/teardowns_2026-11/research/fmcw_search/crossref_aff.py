"""Query Crossref for works with an affiliation string: python -I crossref_aff.py "Aeva" [extra query]"""
import sys, json, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
aff = sys.argv[1]
q = sys.argv[2] if len(sys.argv) > 2 else ""
params = {"query.affiliation": aff, "rows": "40", "select": "DOI,title,author,container-title,issued,type"}
if q:
    params["query.bibliographic"] = q
url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
req = urllib.request.Request(url, headers={"User-Agent": "report-check/1.0 (research)"})
js = json.load(urllib.request.urlopen(req, timeout=60))
for it in js["message"]["items"]:
    affs = set()
    for a in it.get("author", []):
        for x in a.get("affiliation", []):
            affs.add(x.get("name", ""))
    hit = [x for x in affs if aff.lower() in x.lower()]
    if not hit:
        continue
    t = (it.get("title") or [""])[0]
    ct = (it.get("container-title") or [""])[0]
    yr = it.get("issued", {}).get("date-parts", [[None]])[0][0]
    names = ", ".join((a.get("given", "") + " " + a.get("family", "")).strip() for a in it.get("author", [])[:6])
    print(yr, "|", it["DOI"], "|", t[:120], "|", ct[:60], "|", names[:120], "|", "; ".join(hit)[:100])
