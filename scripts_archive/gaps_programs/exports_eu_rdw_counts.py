"""Count Dutch first registrations of Chinese-brand passenger cars by make and model (RDW open data).

Purpose
    Part of the 2026-10-03 check of how many lidar-equipped Chinese-brand cars were sold
    outside China. Queries the RDW "Gekentekende_voertuigen" dataset (Socrata id m9d7-ebf2)
    and counts passenger cars (voertuigsoort = 'Personenauto') by merk + handelsbenaming,
    for first admission (datum_eerste_toelating) in 2024, 2025 and 2026 to date.
    A second count uses the first Dutch registration date for cars first admitted abroad
    (possible grey or used imports, e.g. Li Auto, Xiaomi, Aito).

Inputs
    None besides network access to https://opendata.rdw.nl (no key needed).
    Optional command-line argument: output folder (default: ./data_rdw).

Outputs
    <out>/rdw_merk_discovery.json   make spellings found for each brand pattern
    <out>/rdw_counts.json           counts per make/model/period
    Printed tables.

Caveats
    The dataset is a live register: cars that were exported or scrapped since registration can
    drop out, so counts are lower bounds for registrations in each period.

Date: 2026-10-03
"""
import json
import os
import sys
import requests

BASE = "https://opendata.rdw.nl/resource/m9d7-ebf2.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
PATTERNS = ["NIO", "FIREFLY", "ZEEKR", "LYNK", "LOTUS", "POLESTAR", "XPENG", "BYD", "DENZA",
            "LEAPMOTOR", "SMART", "VOYAH", "HONGQI", "AVATR", "AITO", "SERES", "LI AUTO",
            "LIXIANG", "LI XIANG", "XIAOMI", "YANGWANG", "EXEED", "GEELY", "DEEPAL", "CHANGAN",
            "JETOUR", "HYPTEC", "AION", "GAC", "WEY", "GWM", "ORA", "TANK", "LUXEED", "STELATO",
            "MAEXTRO", "IM ", "MG"]
PERIODS = {"2024": ("20240101", "20241231"),
           "2025": ("20250101", "20251231"),
           "2026ytd": ("20260101", "20261231")}


def soql(params):
    r = requests.get(BASE, params=params, headers=HEADERS, timeout=120)
    r.raise_for_status()
    return r.json()


def discover():
    found = {}
    for p in PATTERNS:
        rows = soql({"$select": "merk, count(*) as n",
                     "$where": f"voertuigsoort='Personenauto' AND upper(merk) like '%{p.strip()}%'",
                     "$group": "merk", "$order": "n DESC", "$limit": 50})
        found[p] = [(row["merk"], int(row["n"])) for row in rows]
    return found


def counts_for(merk, field="datum_eerste_toelating"):
    out = {}
    for label, (a, b) in PERIODS.items():
        where = (f"voertuigsoort='Personenauto' AND merk='{merk}' AND "
                 f"{field} >= '{a}' AND {field} <= '{b}'")
        rows = soql({"$select": "handelsbenaming, count(*) as n", "$where": where,
                     "$group": "handelsbenaming", "$order": "n DESC", "$limit": 500})
        out[label] = {row.get("handelsbenaming", "?"): int(row["n"]) for row in rows}
    return out


def imports_for(merk):
    """Cars first registered in NL in the period but first admitted abroad earlier."""
    out = {}
    for label, (a, b) in PERIODS.items():
        where = (f"voertuigsoort='Personenauto' AND merk='{merk}' AND "
                 f"datum_eerste_tenaamstelling_in_nederland >= '{a}' AND "
                 f"datum_eerste_tenaamstelling_in_nederland <= '{b}' AND "
                 f"datum_eerste_toelating < datum_eerste_tenaamstelling_in_nederland")
        rows = soql({"$select": "handelsbenaming, count(*) as n", "$where": where,
                     "$group": "handelsbenaming", "$order": "n DESC", "$limit": 500})
        out[label] = {row.get("handelsbenaming", "?"): int(row["n"]) for row in rows}
    return out


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else "data_rdw"
    os.makedirs(outdir, exist_ok=True)
    found = discover()
    json.dump(found, open(os.path.join(outdir, "rdw_merk_discovery.json"), "w"), indent=1)
    makes = sorted({m for v in found.values() for m, n in v})
    # MG is large and mostly not relevant; keep it but only report IM models below.
    results = {}
    for m in makes:
        results[m] = {"first_admission": counts_for(m), "imported_used": imports_for(m)}
    json.dump(results, open(os.path.join(outdir, "rdw_counts.json"), "w"), indent=1)
    for m in makes:
        fa = results[m]["first_admission"]
        tot = {k: sum(v.values()) for k, v in fa.items()}
        print(f"\n== {m}: totals {tot}")
        for label in PERIODS:
            items = fa[label]
            if m.upper().startswith("MG"):
                items = {k: v for k, v in items.items() if "IM" in k.upper()}
            if items:
                print(f"  {label}: " + "; ".join(f"{k} {v}" for k, v in items.items()))
        imp = {k: sum(v.values()) for k, v in results[m]["imported_used"].items()}
        if any(imp.values()):
            print(f"  imported (first admitted abroad): {imp}")


if __name__ == "__main__":
    main()
