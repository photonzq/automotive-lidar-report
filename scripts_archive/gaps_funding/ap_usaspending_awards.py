"""Analog Photonics LLC (UEI EA5NMDFQBNF4) in USAspending.gov: prime awards and subawards.

Pulls, through the public USAspending API (no key needed):
  1. every subaward whose sub-recipient matches "Analog Photonics" (contract and
     grant subawards), from the Advanced Search endpoint;
  2. every prime award to the UEI (contracts, IDVs, grants, other assistance);
  3. the recipient profile (prime totals).
Writes JSON files and a flat CSV of subawards to the output folder (default ./raw,
or the first command-line argument). Run from the folder that should hold the data.
No personal identifiers are sent with the requests.
"""
import csv
import json
import os
import sys
import time

import requests

API = "https://api.usaspending.gov/api/v2"
UEI = "EA5NMDFQBNF4"
HEADERS = {"Content-Type": "application/json", "User-Agent": "research-script/1.0"}
OUT = sys.argv[1] if len(sys.argv) > 1 else "raw"
os.makedirs(OUT, exist_ok=True)

SUB_FIELDS = ["Sub-Award ID", "Sub-Awardee Name", "Sub-Award Date", "Sub-Award Amount",
              "Awarding Agency", "Awarding Sub Agency", "Prime Award ID", "Prime Recipient Name",
              "prime_award_recipient_id", "Sub-Award Description", "Sub-Recipient UEI",
              "Prime Award Recipient UEI", "Sub-Award Primary Place of Performance",
              "Sub-Award Type"]
PRIME_FIELDS = ["Award ID", "Recipient Name", "Start Date", "End Date", "Award Amount",
                "Total Outlays", "Awarding Agency", "Awarding Sub Agency", "Award Type",
                "Description", "recipient_id", "generated_internal_id", "Recipient UEI"]

CONTRACT_CODES = ["A", "B", "C", "D"]
IDV_CODES = ["IDV_A", "IDV_B", "IDV_B_A", "IDV_B_B", "IDV_B_C", "IDV_C", "IDV_D", "IDV_E"]
GRANT_CODES = ["02", "03", "04", "05", "F001", "F002"]
LOAN_CODES = ["07", "08", "F003", "F004"]
OTHER_FA_CODES = ["06", "10", "F006", "F007"]
DIRECT_CODES = ["09", "F005", "11", "-1", "F008", "F009", "F010"]


def post(path, payload, tries=4):
    for k in range(tries):
        r = requests.post(API + path, headers=HEADERS, data=json.dumps(payload), timeout=120)
        if r.status_code == 200:
            return r.json()
        time.sleep(3 * (k + 1))
    raise RuntimeError(f"{path} -> {r.status_code}: {r.text[:500]}")


def search_all(filters, fields, subawards, sort):
    rows, page = [], 1
    while True:
        js = post("/search/spending_by_award/", {
            "filters": filters, "fields": fields, "subawards": subawards,
            "limit": 100, "page": page, "sort": sort, "order": "desc"})
        rows += js.get("results", [])
        if not js.get("page_metadata", {}).get("hasNext"):
            break
        page += 1
    return rows


def main():
    period = [{"start_date": "2007-10-01", "end_date": "2026-09-30"}]
    subs = []
    for label, codes in (("contract", CONTRACT_CODES), ("grant", GRANT_CODES)):
        for text in ("ANALOG PHOTONICS", "ANALOGPHOTONICS", UEI):
            rows = search_all({"recipient_search_text": [text], "award_type_codes": codes,
                               "time_period": period}, SUB_FIELDS, True, "Sub-Award Amount")
            for r in rows:
                r["_query"] = f"{label}:{text}"
            subs += rows
    # de-duplicate identical internal records returned by both queries
    seen, uniq = set(), []
    for r in subs:
        key = r.get("internal_id")
        if key in seen:
            continue
        seen.add(key)
        uniq.append(r)
    with open(os.path.join(OUT, "ap_subawards_search.json"), "w", encoding="utf-8") as f:
        json.dump(uniq, f, indent=1)
    with open(os.path.join(OUT, "ap_subawards_search.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        cols = ["internal_id", "_query"] + SUB_FIELDS
        w.writerow(cols)
        for r in uniq:
            w.writerow([str(r.get(c, "")).replace("\r", " ").replace("\n", " ") for c in cols])
    print(f"subaward records (unique internal_id): {len(uniq)}")

    primes = []
    for label, codes in (("contract", CONTRACT_CODES), ("idv", IDV_CODES),
                         ("grant", GRANT_CODES), ("loan", LOAN_CODES),
                         ("other_fa", OTHER_FA_CODES), ("direct", DIRECT_CODES)):
        try:
            rows = search_all({"recipient_search_text": [UEI], "award_type_codes": codes,
                               "time_period": period}, PRIME_FIELDS, False, "Award Amount")
        except RuntimeError as exc:
            print(label, "failed:", str(exc)[:200])
            continue
        for r in rows:
            r["_group"] = label
        primes += rows
    with open(os.path.join(OUT, "ap_prime_awards.json"), "w", encoding="utf-8") as f:
        json.dump(primes, f, indent=1)
    print(f"prime awards: {len(primes)}")

    # recipient profile(s): look up the recipient hash(es) for the UEI
    js = post("/recipient/", {"keyword": UEI, "limit": 50})
    with open(os.path.join(OUT, "ap_recipient_list.json"), "w", encoding="utf-8") as f:
        json.dump(js, f, indent=1)
    for rec in js.get("results", []):
        rid = rec.get("id")
        r = requests.get(f"{API}/recipient/{rid}/", params={"year": "all"}, headers=HEADERS,
                         timeout=120)
        if r.status_code == 200:
            with open(os.path.join(OUT, f"ap_recipient_{rid}.json"), "w", encoding="utf-8") as f:
                json.dump(r.json(), f, indent=1)
            print(rid, rec.get("recipient_level"), r.json().get("total_transaction_amount"))


if __name__ == "__main__":
    main()
