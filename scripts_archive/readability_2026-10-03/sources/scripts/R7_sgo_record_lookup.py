"""R7 item 03: print every version of selected NHTSA SGO ADAS (Level 2) incident reports.

Usage: python R7_sgo_record_lookup.py <csv> [<csv> ...] -- <report_id> [<report_id> ...]
CSV sources (public, no login):
  https://static.nhtsa.gov/odi/ffdd/sgo-2021-01/Archive-2021-2025/SGO-2021-01_Incident_Reports_ADAS.csv
  https://static.nhtsa.gov/odi/ffdd/sgo-2021-01/SGO-2021-01_Incident_Reports_ADAS.csv
Prints date/time/location/weather/speed/narrative-redaction fields for each version.
"""
import sys

import pandas as pd

args = sys.argv[1:]
cut = args.index("--")
files, ids = args[:cut], args[cut + 1:]

for f in files:
    df = pd.read_csv(f, dtype=str, encoding="latin-1", low_memory=False)
    print(f"\n=== {f}: {len(df)} rows, {len(df.columns)} columns")
    idcol = [c for c in df.columns if c.strip().lower() == "report id"][0]
    sub = df[df[idcol].isin(ids)]
    keys = [c for c in df.columns if any(s in c.lower() for s in (
        "report id", "report version", "report submission", "report month", "report year",
        "incident date", "incident time", "city", "state", "roadway type", "roadway description",
        "weather", "lighting", "crash with", "sv precrash speed", "highest injury", "model",
        "make", "notice received", "narrative", "same incident", "source", "investigating",
        "adas/ads system version", "automation system engaged", "engagement"))]
    for _, row in sub.iterrows():
        print("-" * 60)
        for k in keys:
            v = row[k]
            if isinstance(v, str) and len(v) > 160:
                v = v[:160] + "..."
            if pd.notna(v) and str(v).strip() != "":
                print(f"{k}: {v}")
