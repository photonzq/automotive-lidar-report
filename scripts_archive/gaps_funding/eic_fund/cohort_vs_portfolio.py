"""Cross-match an EIC Accelerator cut-off results table against the EIC Fund
portfolio list scraped by eic_fund_portfolio_scrape.py.

Usage (run from the eic_fund folder):
    python scripts/cohort_vs_portfolio.py raw/<cutoff>.pdf  LABEL
Extracts the one-page table (company, acronym, description, recommended
financing type, website, country) with PyMuPDF's table finder, then checks for
each company whether a fuzzy-normalised name occurs in eic_fund_portfolio.json.
Writes cohort_<LABEL>.csv and prints a summary by financing type. Name
matching is approximate: every 'no' should be spot-checked by hand.
"""
import csv
import json
import re
import sys
from pathlib import Path

import pymupdf

STOP = {"gmbh", "ltd", "limited", "ab", "bv", "b.v.", "sl", "s.l.", "sas", "sa", "oy",
        "aps", "nv", "srl", "s.r.l.", "ag", "as", "lda", "lda.", "ad", "spa", "sarl",
        "technologies", "technology", "the", "systems", "sp", "z", "o.o.", "inc"}


def norm(s: str) -> str:
    s = s.lower().replace("\n", " ")
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    toks = [t for t in s.split() if t not in STOP]
    return " ".join(toks)


def main(pdf, label):
    port = json.loads(Path("eic_fund_portfolio.json").read_text(encoding="utf-8"))
    pnames = [(norm(p["name"]), p) for p in port]
    doc = pymupdf.open(pdf)
    rows = []
    for page in doc:
        for tab in page.find_tables().tables:
            for r in tab.extract():
                if not r or not r[0] or r[0].strip().lower().startswith("company"):
                    continue
                cells = [(c or "").replace("\n", " ").strip() for c in r]
                rows.append(cells)
    out = []
    for c in rows:
        name = c[0]
        ftype = c[3] if len(c) > 3 else ""
        site = c[4] if len(c) > 4 else ""
        country = c[5] if len(c) > 5 else ""
        n = norm(name)
        hit = None
        for pn, p in pnames:
            if not pn or not n:
                continue
            if pn == n or (len(n) > 4 and (n in pn or pn in n)) or n.split()[0] == pn.split()[0] and len(n.split()[0]) > 4:
                hit = p
                break
        out.append({"company": name, "acronym": c[1], "financing_type": ftype,
                    "website": site, "country": country,
                    "in_eic_fund_portfolio": "yes" if hit else "no",
                    "portfolio_name": hit["name"] if hit else "",
                    "portfolio_href": hit["href"] if hit else ""})
    with open(f"cohort_{label}.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    from collections import defaultdict
    agg = defaultdict(lambda: [0, 0])
    for o in out:
        agg[o["financing_type"]][0] += 1
        agg[o["financing_type"]][1] += o["in_eic_fund_portfolio"] == "yes"
    print(f"{label}: {len(out)} companies")
    for k, (n, y) in agg.items():
        print(f"  {k:20s} total {n:3d}  listed in EIC Fund portfolio {y:3d}")
    for o in out:
        print(f"  {o['in_eic_fund_portfolio']:3s} | {o['financing_type']:15s} | {o['country']:14s} | {o['company']} -> {o['portfolio_name']}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
