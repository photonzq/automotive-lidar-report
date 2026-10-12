"""Explore the public EIC Data Hub data files (datahub.eismea.eu).

The Data Hub web app loads two JSON files listed in /app/config/config.json:
    /app/assets/json/data/eic-data-core.json
    /app/assets/json/data/eic-data-extend.json
(saved by fetch.py as raw/datahub_eic-data-core.json and
raw/datahub_eic-data-extend.json). This script prints the structure of both
files (top-level keys, record counts, the field names of each record type),
then prints every record that mentions the search terms (default: voxel,
hybrid lidar) together with all linked project / equity records, so that the
grant and any disclosed equity investment can be read directly.

Run from the eic_fund folder:  python scripts/datahub_explore.py [term ...]
"""
import json
import sys
from pathlib import Path


def load(name):
    return json.loads(Path("raw") / name if False else (Path("raw") / name).read_text(encoding="utf-8"))


def describe(obj, path="", depth=0, maxdepth=3):
    pad = "  " * depth
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, list):
                kinds = type(v[0]).__name__ if v else "empty"
                print(f"{pad}{path}{k}: list[{len(v)}] of {kinds}")
                if v and isinstance(v[0], dict) and depth < maxdepth:
                    print(f"{pad}   fields: {list(v[0].keys())}")
                    print(f"{pad}   example: {json.dumps(v[0], ensure_ascii=False)[:400]}")
            elif isinstance(v, dict):
                print(f"{pad}{path}{k}: dict[{len(v)}]")
                if depth < maxdepth:
                    describe(v, "", depth + 1, maxdepth)
            else:
                print(f"{pad}{path}{k}: {str(v)[:120]}")


def main(terms):
    core = load("datahub_eic-data-core.json")
    ext = load("datahub_eic-data-extend.json")
    print("=== core ===")
    describe(core)
    print("=== extend ===")
    describe(ext)
    # generic search: any record (dict inside any list) whose JSON mentions a term
    hits = {}
    for label, blob in (("core", core), ("extend", ext)):
        for k, v in blob["content"].items():
            if not isinstance(v, list):
                continue
            for rec in v:
                s = json.dumps(rec, ensure_ascii=False).lower()
                if any(t in s for t in terms):
                    print(f"\nHIT [{label}.{k}]: {json.dumps(rec, ensure_ascii=False)[:1500]}")
                    if isinstance(rec, dict) and "id" in rec:
                        hits[rec["id"]] = rec
    # follow ids found above into every other list
    print("\n=== records linked to hit ids ===")
    ids = set(hits)
    for label, blob in (("core", core), ("extend", ext)):
        for k, v in blob["content"].items():
            if not isinstance(v, list):
                continue
            for rec in v:
                s = json.dumps(rec)
                if any(str(i) in s for i in ids) and (not isinstance(rec, dict) or rec.get("id") not in ids):
                    print(f"LINK [{label}.{k}]: {json.dumps(rec, ensure_ascii=False)[:1500]}")


if __name__ == "__main__":
    main([t.lower() for t in (sys.argv[1:] or ["voxel", "hybrid lidar"])])
