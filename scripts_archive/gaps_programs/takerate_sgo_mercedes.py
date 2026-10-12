"""Download NHTSA Standing General Order (SGO 2021-01) incident-report CSVs and count reports by make.

Purpose: look for Mercedes-Benz Drive Pilot (SAE Level 3, reported as an automated driving
system, ADS) crash reports, and BMW, Lucid or other L3 entries, as an indirect sign of fleet
activity for the take-rate item of Appendix 1. The SGO files hold crash reports, not fleet sizes.
Usage:   python takerate_sgo_mercedes.py [OUTDIR]    (default ./sgo)
Inputs:  public CSVs on static.nhtsa.gov (current file and the 2021-2025 archive); no key needed.
Outputs: the CSVs in OUTDIR; printed counts of ADS and ADAS reports per make, and every
         Mercedes-Benz / BMW / Lucid row of the ADS files with date, model, state and ADS version.
Date:    2026-10-03
"""
import csv
import io
import os
import sys
from collections import Counter

import requests

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"
BASE = "https://static.nhtsa.gov/odi/ffdd/sgo-2021-01/"
FILES = ["SGO-2021-01_Incident_Reports_ADS.csv",
         "Archive-2021-2025/SGO-2021-01_Incident_Reports_ADS.csv",
         "SGO-2021-01_Incident_Reports_ADAS.csv",
         "Archive-2021-2025/SGO-2021-01_Incident_Reports_ADAS.csv"]


def fetch(outdir, name):
    fn = os.path.join(outdir, name.replace("/", "__"))
    if not os.path.exists(fn):
        r = requests.get(BASE + name, headers={"User-Agent": UA}, timeout=120)
        print(name, "HTTP", r.status_code, len(r.content))
        if r.status_code != 200:
            return None
        open(fn, "wb").write(r.content)
    return fn


def rows(fn):
    raw = open(fn, "rb").read()
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            txt = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    return list(csv.DictReader(io.StringIO(txt)))


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else "sgo"
    os.makedirs(outdir, exist_ok=True)
    for name in FILES:
        fn = fetch(outdir, name)
        if not fn:
            continue
        data = rows(fn)
        print("=====", name, "rows", len(data))
        if not data:
            continue
        cols = list(data[0].keys())
        make_col = next((c for c in cols if c.strip().lower() == "make"), None)
        ent_col = next((c for c in cols if "reporting entity" in c.lower()), None)
        print("columns:", make_col, ent_col)
        cnt = Counter((r.get(make_col) or "").strip().upper() for r in data)
        print("top makes:", cnt.most_common(25))
        if "ADS" in name and "ADAS" not in name:
            for r in data:
                mk = (r.get(make_col) or "").upper()
                if any(k in mk for k in ("MERCEDES", "BMW", "LUCID", "HONDA", "LEXUS")):
                    keep = {c: r[c] for c in cols if any(k in c.lower() for k in (
                        "report id", "reporting entity", "make", "model", "model year",
                        "incident date", "incident time", "state", "city", "roadway type",
                        "posted speed", "ads equipped", "automation system engaged",
                        "driver / operator type", "sv pre-crash speed", "crash with", "report version"))}
                    print(keep)


if __name__ == "__main__":
    main()
