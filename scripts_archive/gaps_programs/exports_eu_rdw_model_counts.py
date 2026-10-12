"""Targeted RDW (Netherlands) counts of Chinese-brand passenger cars by model, 2024, 2025 and 2026 to date.

Purpose
    Faster, targeted successor of exports_eu_rdw_counts.py (whose make-discovery step with broad
    LIKE patterns was too slow and was stopped). Counts passenger cars (voertuigsoort =
    'Personenauto') in the RDW "Gekentekende_voertuigen" dataset (Socrata id m9d7-ebf2) by
    merk + handelsbenaming, using the make spellings found by the discovery step
    (e.g. 'LYNK&CO', 'LI AUTO'), for:
      (a) first admission anywhere (datum_eerste_toelating) in the period, and
      (b) first Dutch registration in the period for cars first admitted abroad earlier
          (used or grey imports).
    Used on 2026-10-03 for the estimate of lidar-equipped Chinese-brand cars sold outside China.

Inputs
    Network access to https://opendata.rdw.nl (no key needed).
    Optional command-line argument: output folder (default: ./data_rdw).

Outputs
    <out>/rdw_model_counts.json and printed tables.

Caveats
    Live register: exported or scrapped cars drop out, so counts are lower bounds.
    Model names are the registrant's trade names (handelsbenaming) and can vary in spelling.

Date: 2026-10-03
"""
import json
import os
import sys
import requests

BASE = "https://opendata.rdw.nl/resource/m9d7-ebf2.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
MAKES = ["NIO", "ZEEKR", "LYNK&CO", "LOTUS", "POLESTAR", "XPENG", "DENZA", "LEAPMOTOR",
         "VOYAH", "SERES", "LI AUTO", "XIAOMI", "BYD", "MG", "AION", "DEEPAL", "GEELY"]
PERIODS = {"2024": ("20240101", "20241231"),
           "2025": ("20250101", "20251231"),
           "2026ytd": ("20260101", "20261231")}


def soql(params):
    r = requests.get(BASE, params=params, headers=HEADERS, timeout=180)
    r.raise_for_status()
    return r.json()


def by_model(merk, a, b, imported=False):
    if imported:
        where = (f"voertuigsoort='Personenauto' AND merk='{merk}' AND "
                 f"datum_eerste_tenaamstelling_in_nederland between '{a}' and '{b}' AND "
                 f"datum_eerste_toelating < '{a}'")
    else:
        where = (f"voertuigsoort='Personenauto' AND merk='{merk}' AND "
                 f"datum_eerste_toelating between '{a}' and '{b}'")
    rows = soql({"$select": "handelsbenaming, count(*) as n", "$where": where,
                 "$group": "handelsbenaming", "$order": "n DESC", "$limit": 500})
    return {row.get("handelsbenaming", "?"): int(row["n"]) for row in rows}


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else "data_rdw"
    os.makedirs(outdir, exist_ok=True)
    res = {}
    for m in MAKES:
        res[m] = {}
        for label, (a, b) in PERIODS.items():
            new = by_model(m, a, b)
            imp = by_model(m, a, b, imported=True) if m not in ("MG", "BYD", "POLESTAR") else {}
            if m == "MG":
                new = {k: v for k, v in new.items() if k.upper().startswith("IM")}
            res[m][label] = {"new": new, "imported_older": imp}
            tot = sum(new.values())
            print(f"{m:10s} {label:8s} total {tot:6d} | " +
                  "; ".join(f"{k} {v}" for k, v in list(new.items())[:12]) +
                  (f" || imported older: {sum(imp.values())} " +
                   "; ".join(f"{k} {v}" for k, v in list(imp.items())[:6]) if imp else ""),
                  flush=True)
        json.dump(res, open(os.path.join(outdir, "rdw_model_counts.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
