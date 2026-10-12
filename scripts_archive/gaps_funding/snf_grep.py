"""Search the Swiss National Science Foundation's open datasets for a company or person.

Usage:  python snf_grep.py OUTDIR pattern [pattern ...]
Downloads (once) the SNSF Data Portal exports listed in FILES (grants with abstracts,
persons, and the output datasets on collaborations, use-inspired outputs and knowledge
transfer, which name non-academic partners), then prints every row in which any pattern
(case-insensitive regular expression) occurs, with the file name and the grant number.
For grant rows it also prints title, period, approved amount and institution.
No login or personal data is sent.
"""
import csv
import os
import re
import sys

import requests

BASE = "https://data.snf.ch/datasets/"
FILES = ["grants_with_abstracts.csv", "persons.csv", "output_data_collaborations.csv",
         "output_data_useinspired.csv", "output_data_knowledgetransfer.csv"]
HEADERS = {"User-Agent": "research-script/1.0"}


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    pat = re.compile("|".join(sys.argv[2:]), re.I)
    csv.field_size_limit(10 ** 9)
    for fn in FILES:
        path = os.path.join(out, fn)
        if not os.path.exists(path):
            r = requests.get(BASE + fn, headers=HEADERS, timeout=600)
            r.raise_for_status()
            with open(path, "wb") as f:
                f.write(r.content)
        with open(path, encoding="utf-8-sig", errors="replace", newline="") as f:
            sample = f.read(4096)
            f.seek(0)
            delim = ";" if sample.count(";") > sample.count(",") else ","
            rows = list(csv.DictReader(f, delimiter=delim))
        hits = [r for r in rows if pat.search(" | ".join(str(v) for v in r.values()))]
        print(f"\n=== {fn}: {len(rows)} rows, {len(hits)} hits")
        for r in hits[:50]:
            keys = [k for k in r if k and re.search(r"Grant|Title|Start|End|Amount|Institution"
                                                    r"|Partner|Organisation|Name|Type", k)]
            print("  ", {k: (r[k] or "")[:160] for k in keys[:14]})


if __name__ == "__main__":
    main()
