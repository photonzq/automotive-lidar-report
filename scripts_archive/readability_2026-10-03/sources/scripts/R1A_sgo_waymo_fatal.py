"""R1_partA_E2-E5: list NHTSA Standing General Order (SGO) ADS crash reports from Waymo
that record a fatality, and the date range the file covers.

Usage (Anaconda interpreter):
  python R1A_sgo_waymo_fatal.py <sgo_ads.csv>

Input: the public SGO ADS incident file, e.g.
  https://static.nhtsa.gov/odi/ffdd/sgo-2021-01/SGO-2021-01_Incident_Reports_ADS.csv
(downloaded with a generic User-Agent; no e-mail or credentials sent).
"""
import sys

import pandas as pd

path = sys.argv[1]
df = pd.read_csv(path, low_memory=False, encoding_errors="replace")
print("rows:", len(df))
cols = list(df.columns)
sev_cols = [c for c in cols if "Severity" in c or "Injury" in c]
print("severity-like columns:", sev_cols[:12])
ent = df["Reporting Entity"].astype(str)
w = df[ent.str.contains("Waymo", case=False, na=False)].copy()
print("Waymo rows:", len(w))
for c in ["Report Month", "Report Year", "Incident Date", "Incident Time (24:00)"]:
    if c in df.columns:
        print(c, "range:", df[c].dropna().astype(str).min(), "->", df[c].dropna().astype(str).max())

mask = pd.Series(False, index=w.index)
for c in sev_cols:
    mask |= w[c].astype(str).str.contains("Fatal", case=False, na=False)
f = w[mask]
show = [c for c in ["Report ID", "Report Version", "Incident Date", "Incident Time (24:00)", "City", "State",
                    "Crash With", "Highest Injury Severity Alleged", "SV Pre-Crash Movement",
                    "CP Pre-Crash Movement", "Driver / Operator Type", "Narrative"] if c in w.columns]
pd.set_option("display.max_colwidth", 400)
pd.set_option("display.width", 250)
print("Waymo rows mentioning a fatality:", len(f))
print(f[show].to_string())
