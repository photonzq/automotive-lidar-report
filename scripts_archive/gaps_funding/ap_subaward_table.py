"""Tabulate Analog Photonics' subaward records award by award and total them by funder.

Reads raw/ap_subaward_detail.json (from ap_subaward_detail.py) and prints one line per
FSRS/SAM.gov subaward record: prime award, prime recipient, funding agency, subaward
number, action date, amount and a short purpose. It then gives:
  * the total of all records (each record treated as a separate funding action);
  * a lower bound that keeps only the largest record per subaward number, i.e. the
    total if every repeated number were a cumulative restatement;
  * a flag for records whose description repeats an earlier record of the same number
    (the only candidates for double counting);
  * totals by programme family.
Writes raw/ap_subaward_table.csv.
"""
import csv
import json
import os
import re
import sys
from collections import defaultdict

RAW = sys.argv[1] if len(sys.argv) > 1 else "raw"

FAMILY = {
    "ASST_NON_FA86501525220_097": "AIM Photonics 1.0 (AFRL coop. agreement, RF SUNY)",
    "ASST_NON_FA86502121000_097": "AIM Photonics 2.0 (AFRL coop. agreement, RF SUNY)",
    "ASST_NON_HQ00342020007_097": "NCMS CTMA (DoD sustainment coop. agreement)",
    "ASST_NON_HQ00342420001_097": "NCMS CTMA (DoD sustainment coop. agreement)",
    "ASST_NON_HQ00342420008_097": "NCMS CTMA (DoD sustainment coop. agreement)",
    "CONT_AWD_HR001113C0071_9700_-NONE-_-NONE-": "DARPA DiSARMER via Rockwell Collins",
    "CONT_AWD_HR001116C0105_9700_-NONE-_-NONE-": "DARPA MOABB via Teledyne",
    "CONT_AWD_HR001119C0083_9700_-NONE-_-NONE-": "DARPA PIPES via UC Santa Barbara",
    "CONT_AWD_N0003015C0003_9700_-NONE-_-NONE-": "Navy SSP via Draper",
    "CONT_AWD_N0003023C6008_9700_-NONE-_-NONE-": "Navy SSP via Draper",
    "CONT_AWD_N0003024C6001_9700_-NONE-_-NONE-": "Navy SSP via Draper",
}


def norm(text):
    return re.sub(r"[^A-Z]", "", (text or "").upper())[:300]


def main():
    d = json.load(open(os.path.join(RAW, "ap_subaward_detail.json"), encoding="utf-8"))
    rows = []
    for pid, v in d["primes"].items():
        s = v["summary"]
        prime = (s.get("recipient") or {}).get("recipient_name")
        fund = ((s.get("funding_agency") or {}).get("subtier_agency") or {}).get("name")
        for x in v["ap_subawards"]:
            rows.append({"prime_award": pid, "family": FAMILY.get(pid, "?"),
                         "prime_recipient": prime, "funding_subtier": fund,
                         "subaward_number": x.get("subaward_number"),
                         "action_date": x.get("action_date"), "amount": x.get("amount") or 0.0,
                         "description": re.sub(r"\s+", " ", x.get("description") or "")})
    rows.sort(key=lambda r: (r["family"], r["action_date"]))
    seen_desc = defaultdict(list)
    for r in rows:
        key = (r["subaward_number"], norm(r["description"]))
        r["repeat_of_same_text"] = bool(seen_desc[key])
        seen_desc[key].append(r["action_date"])
    total = sum(r["amount"] for r in rows)
    best = defaultdict(float)
    for r in rows:
        best[(r["prime_award"], r["subaward_number"])] = max(
            best[(r["prime_award"], r["subaward_number"])], r["amount"])
    lower = sum(best.values())
    flagged = sum(r["amount"] for r in rows if r["repeat_of_same_text"])
    fam = defaultdict(float)
    for r in rows:
        fam[r["family"]] += r["amount"]
    for r in rows:
        print(f"{r['family'][:44]:44s} {r['subaward_number']:20s} {r['action_date']} "
              f"{r['amount']:>14,.2f} {'REPEAT-TEXT' if r['repeat_of_same_text'] else '':11s} "
              f"{r['description'][:60]}")
    print(f"\nrecords: {len(rows)}; distinct subaward numbers: {len(best)}")
    print(f"total of all records: {total:,.2f}")
    print(f"lower bound (largest record per number): {lower:,.2f}")
    print(f"records repeating the text of an earlier record of the same number: {flagged:,.2f}")
    for k, v in sorted(fam.items(), key=lambda kv: -kv[1]):
        print(f"  {k:52s} {v:>14,.2f}  ({100 * v / total:4.1f}%)")
    with open(os.path.join(RAW, "ap_subaward_table.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
