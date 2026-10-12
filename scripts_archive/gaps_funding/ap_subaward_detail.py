"""Award-by-award check of the subawards Analog Photonics LLC received (USAspending.gov).

For every prime award that ap_usaspending_awards.py found with an Analog Photonics
subaward, this script:
  * pages through /api/v2/subawards/ (all subawards reported under that prime) and keeps
    those whose sub-recipient name contains "ANALOG PHOTONICS";
  * downloads the prime award summary (/api/v2/awards/<id>/): agency, programme
    description, period, obligations and the prime's reported subaward total;
  * repeats the Advanced Search with the old DUNS (079091194) and the second UEI
    (DG68H2G8MNC6) listed as a parent in the recipient profile, to catch records
    the name search might miss.
Input: raw/ap_subawards_search.json (from ap_usaspending_awards.py).
Output: raw/ap_subaward_detail.json and a printed table.
"""
import json
import os
import sys
import time

import requests

API = "https://api.usaspending.gov/api/v2"
HEADERS = {"Content-Type": "application/json", "User-Agent": "research-script/1.0"}
RAW = sys.argv[1] if len(sys.argv) > 1 else "raw"


def post(path, payload, tries=4):
    for k in range(tries):
        r = requests.post(API + path, headers=HEADERS, data=json.dumps(payload), timeout=120)
        if r.status_code == 200:
            return r.json()
        time.sleep(3 * (k + 1))
    raise RuntimeError(f"{path} -> {r.status_code}: {r.text[:400]}")


def get(path):
    r = requests.get(API + path, headers=HEADERS, timeout=120)
    r.raise_for_status()
    return r.json()


def all_subawards(award_id):
    rows, page = [], 1
    while True:
        js = post("/subawards/", {"award_id": award_id, "limit": 100, "page": page,
                                  "sort": "action_date", "order": "asc"})
        rows += js.get("results", [])
        if not js.get("page_metadata", {}).get("hasNext"):
            break
        page += 1
    return rows


def main():
    found = json.load(open(os.path.join(RAW, "ap_subawards_search.json"), encoding="utf-8"))
    primes = sorted({r["prime_award_generated_internal_id"] for r in found})
    out = {"primes": {}, "extra_searches": {}}
    for pid in primes:
        summ = get(f"/awards/{pid}/")
        subs = all_subawards(pid)
        ap = [s for s in subs if "ANALOG PHOTONICS" in (s.get("recipient_name") or "").upper()]
        out["primes"][pid] = {
            "summary": {k: summ.get(k) for k in (
                "piid", "fain", "category", "type_description", "description",
                "total_obligation", "base_and_all_options_value", "subaward_count",
                "total_subaward_amount", "period_of_performance", "awarding_agency",
                "funding_agency", "recipient", "cfda_info", "parent_award")},
            "n_subawards_all": len(subs),
            "ap_subawards": ap}
        rec = summ.get("recipient") or {}
        print(f"\n== {pid}  prime={rec.get('recipient_name')}  "
              f"oblig={summ.get('total_obligation')}  subaward_total={summ.get('total_subaward_amount')}"
              f"  n_sub={summ.get('subaward_count')}")
        print("   ", (summ.get("description") or "")[:160])
        for s in ap:
            print(f"   AP sub {s.get('subaward_number')} {s.get('action_date')} "
                  f"{s.get('amount'):,.2f}  {(s.get('description') or '')[:70]!r}")
    # extra searches by DUNS and the second UEI
    period = [{"start_date": "2007-10-01", "end_date": "2026-09-30"}]
    fields = ["Sub-Award ID", "Sub-Awardee Name", "Sub-Award Date", "Sub-Award Amount",
              "Prime Award ID", "Prime Recipient Name", "Sub-Recipient UEI"]
    for text in ("079091194", "DG68H2G8MNC6"):
        for codes in (["A", "B", "C", "D"], ["02", "03", "04", "05", "F001", "F002"]):
            js = post("/search/spending_by_award/", {
                "filters": {"recipient_search_text": [text], "award_type_codes": codes,
                            "time_period": period},
                "fields": fields, "subawards": True, "limit": 100, "page": 1})
            out["extra_searches"][f"sub:{text}:{codes[0]}"] = js.get("results", [])
            print(f"\nsubaward search {text} {codes[0]}: {len(js.get('results', []))} rows")
            for r in js.get("results", []):
                print("   ", r.get("Sub-Award ID"), r.get("Sub-Award Date"),
                      r.get("Sub-Award Amount"), r.get("Prime Award ID"),
                      r.get("Prime Recipient Name"), r.get("Sub-Awardee Name"))
        for codes in (["A", "B", "C", "D"], ["02", "03", "04", "05", "F001", "F002"],
                      ["IDV_A", "IDV_B", "IDV_B_A", "IDV_B_B", "IDV_B_C", "IDV_C", "IDV_D",
                       "IDV_E"]):
            js = post("/search/spending_by_award/", {
                "filters": {"recipient_search_text": [text], "award_type_codes": codes,
                            "time_period": period},
                "fields": ["Award ID", "Recipient Name", "Award Amount", "Start Date",
                           "Awarding Sub Agency", "Description", "Recipient UEI"],
                "subawards": False, "limit": 100, "page": 1})
            out["extra_searches"][f"prime:{text}:{codes[0]}"] = js.get("results", [])
            print(f"prime search {text} {codes[0]}: {len(js.get('results', []))} rows")
            for r in js.get("results", []):
                print("   ", r.get("Award ID"), r.get("Start Date"), r.get("Award Amount"),
                      r.get("Recipient Name"), r.get("Recipient UEI"),
                      (r.get("Description") or "")[:60])
    with open(os.path.join(RAW, "ap_subaward_detail.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
