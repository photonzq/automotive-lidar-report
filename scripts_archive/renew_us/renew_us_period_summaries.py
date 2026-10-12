"""Period averages across the non-SBIR lidar series (USAspending, NSF, NASA TechPort/ESTO).

Purpose
    Reads the result CSVs written by usasp_lidar_analysis.py, nsf_lidar_awards.py and
    nasa_techport_lidar.py and prints per-year averages for the periods used in the report
    (FY2008-09 or FY2005-09, FY2010-14, FY2015-19, FY2020-22, FY2023-25, FY2026 partial), so the
    non-SBIR channels can be compared with the SBIR/STTR series on the same periods.
    Also writes the NASA ESTO (IIP, ACT, Decadal Survey Incubation, ESTO Innovation Fund)
    lidar project list from the TechPort extract.

Inputs
    usasp_dir    : folder with usasp_lidar_by_fy.csv and usasp_lidar_agency_fy.csv
    nsf_nasa_dir : folder with nsf_lidar_awards.csv and techport_lidar_projects.csv
Outputs
    printed tables; <nsf_nasa_dir>/techport_esto_lidar.csv; <usasp_dir>/usasp_lidar_period_means.csv

Usage:
    python renew_us_period_summaries.py <usasp_dir> <nsf_nasa_dir>
"""
import os
import sys

import pandas as pd

PERIODS = ((2005, 2009, "2005-09"), (2010, 2014, "2010-14"), (2015, 2019, "2015-19"),
           (2020, 2022, "2020-22"), (2023, 2025, "2023-25"), (2026, 2026, "2026p"))


def per(y):
    for lo, hi, lab in PERIODS:
        if lo <= y <= hi:
            return lab
    return None


def main(usasp_dir, nsf_nasa_dir):
    pd.set_option("display.width", 250)
    t = pd.read_csv(os.path.join(usasp_dir, "usasp_lidar_by_fy.csv"), index_col=0)
    g = t.groupby(t.index.map(per)).mean()  # USAspending starts FY2008, so the first period is FY2008-09
    g.to_csv(os.path.join(usasp_dir, "usasp_lidar_period_means.csv"))
    print(g.round(1).T.to_string())
    a = pd.read_csv(os.path.join(usasp_dir, "usasp_lidar_agency_fy.csv"), index_col=0)
    a.columns = a.columns.astype(float).astype(int)
    print((a.T.groupby(a.columns.map(per)).mean().T).round(1).to_string())

    n = pd.read_csv(os.path.join(nsf_nasa_dir, "nsf_lidar_awards.csv"))
    n = n[n["start_fy"].between(2005, 2026) & ~n["sbir"]]
    years = {lab: hi - lo + 1 for lo, hi, lab in PERIODS}
    n = n.assign(p=n["start_fy"].map(per))
    s = n.groupby("p").agg(awards=("id", "size"), obligated=("fundsObligatedAmt", "sum"),
                           estimated=("estimatedTotalAmt", "sum"))
    s = s.div(s.index.map(years), axis=0)
    s[["obligated", "estimated"]] /= 1e6
    print("NSF non-SBIR lidar awards per year (count, $M):")
    print(s.round(2).to_string())
    k = n.pivot_table(index="klass", columns="p", values="fundsObligatedAmt", aggfunc="sum", fill_value=0)
    print((k / k.columns.map(years) / 1e6).round(2).to_string())

    tp = pd.read_csv(os.path.join(nsf_nasa_dir, "techport_lidar_projects.csv"))
    esto = tp[tp["program"].fillna("").str.contains(
        "Instrument Incubator|Advanced Component|Decadal Survey Incubation|ESTO", regex=True)]
    esto.to_csv(os.path.join(nsf_nasa_dir, "techport_esto_lidar.csv"), index=False)
    print(pd.crosstab(esto["start_year"], esto["program"]).to_string())


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
