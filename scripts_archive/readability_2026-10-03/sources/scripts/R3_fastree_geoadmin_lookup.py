# -*- coding: utf-8 -*-
"""
Look up Swiss official addresses and the federal Register of Buildings and
Dwellings (GWR / RegBL) through the public swisstopo API (api3.geo.admin.ch),
to establish in which MUNICIPALITY a building lies, its postal code/locality
and its building name (e.g. 'PSE-E' = Parc Scientifique d'Ecublens, bldg E).

For each search text: SearchServer (origin=address) -> coordinates ->
MapServer/identify on layer ch.bfs.gebaeude_wohnungs_register.
Prints EGID, street + number, building name (gbez), municipality (ggdename,
BFS no.), postcode + locality, construction year.

No login, no key, no email; generic browser User-Agent only.
Usage:  python R3_fastree_geoadmin_lookup.py "<search text>" ["<search text>" ...]
        e.g. "Chemin Erna Hamburger 1c" "Dent d'Oche 1b Ecublens"
"""
import json
import sys
import time

import requests

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
SEARCH = "https://api3.geo.admin.ch/rest/services/api/SearchServer"
IDENT = "https://api3.geo.admin.ch/rest/services/api/MapServer/identify"
KEEP = ("egid", "strname_deinr", "gbez", "ggdename", "ggdenr", "gdekt",
        "dplz4", "dplzname", "gbauj", "lparz")


def gwr_at(s, lon, lat, tol=8):
    p = {"geometry": f"{lon},{lat}", "geometryType": "esriGeometryPoint",
         "sr": "4326", "layers": "all:ch.bfs.gebaeude_wohnungs_register",
         "tolerance": str(tol),
         "mapExtent": f"{lon - 0.01},{lat - 0.01},{lon + 0.01},{lat + 0.01}",
         "imageDisplay": "1000,1000,96", "returnGeometry": "false",
         "lang": "fr"}
    r = s.get(IDENT, params=p, timeout=60)
    r.raise_for_status()
    out = []
    for res in r.json().get("results", []):
        a = res.get("attributes", {})
        out.append({k: a.get(k) for k in KEEP})
    return out


def main(queries):
    s = requests.Session()
    s.headers["User-Agent"] = UA
    for q in queries:
        print("=== search:", q)
        r = s.get(SEARCH, params={"searchText": q, "type": "locations",
                                  "origins": "address", "sr": "4326",
                                  "limit": "5"}, timeout=60)
        r.raise_for_status()
        for hit in r.json().get("results", [])[:3]:
            a = hit["attrs"]
            print(" address hit:", a.get("label"), "|", a.get("detail"))
            for g in gwr_at(s, a["lon"], a["lat"]):
                print("   GWR:", json.dumps(g, ensure_ascii=False))
            time.sleep(0.5)


if __name__ == "__main__":
    main(sys.argv[1:])
