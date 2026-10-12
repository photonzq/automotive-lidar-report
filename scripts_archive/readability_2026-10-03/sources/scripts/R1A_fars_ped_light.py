"""R1_partA_E2-E5: US pedestrian deaths by light condition, land use and road class, from FARS.

Usage (Anaconda interpreter):
  python R1A_fars_ped_light.py <FARSyyyyNationalCSV.zip> [<another zip> ...]

Inputs: NHTSA FARS national CSV archives, e.g.
  https://static.nhtsa.gov/nhtsa/downloads/FARS/2024/National/FARS2024NationalCSV.zip
(downloaded with a generic User-Agent; no e-mail or credentials sent).

Definitions (FARS Analytical User's Manual):
  person.csv  PER_TYP = 5 pedestrian; INJ_SEV = 4 fatal injury (K)
  accident.csv LGT_COND: 1 daylight, 2 dark-not lighted, 3 dark-lighted, 4 dawn, 5 dusk,
               6 dark-unknown lighting, 7 other, 8 not reported, 9 reported as unknown
  accident.csv RUR_URB: 1 rural, 2 urban (others: not in inventory / unknown)
  accident.csv FUNC_SYS: 1 interstate, 2 other freeways and expressways, 3 other principal
               arterial, 4 minor arterial, 5 major collector, 6 minor collector, 7 local
The NAME columns shipped in the CSVs are printed alongside the codes as a check.
"""
import sys
import zipfile

import pandas as pd


def load(zpath, name):
    z = zipfile.ZipFile(zpath)
    member = [n for n in z.namelist() if n.lower().endswith("/" + name)][0]
    with z.open(member) as f:
        return pd.read_csv(f, low_memory=False, encoding="latin-1")


def pct(n, d):
    return f"{n} ({100.0 * n / d:.1f}%)"


for zpath in sys.argv[1:]:
    acc = load(zpath, "accident.csv")
    per = load(zpath, "person.csv")
    ped = per[(per["PER_TYP"] == 5) & (per["INJ_SEV"] == 4)]
    keep = ["ST_CASE", "LGT_COND", "RUR_URB", "FUNC_SYS"]
    names = [c for c in ["LGT_CONDNAME", "RUR_URBNAME", "FUNC_SYSNAME"] if c in acc.columns]
    m = ped[["ST_CASE"]].merge(acc[keep + names], on="ST_CASE", how="left")
    n = len(m)
    print("=" * 70)
    print(zpath)
    print("pedestrians killed:", n)
    if names:
        print(m.groupby(["LGT_COND", "LGT_CONDNAME"]).size().to_string())
    dark_nl = m[m["LGT_COND"] == 2]
    dark_l = m[m["LGT_COND"] == 3]
    dark_u = m[m["LGT_COND"] == 6]
    dark_all = len(dark_nl) + len(dark_l) + len(dark_u)
    print("dark (not lighted + lighted + unknown lighting):", pct(dark_all, n))
    print("dark - not lighted:", pct(len(dark_nl), n))
    print("dark - lighted:", pct(len(dark_l), n))
    print("dark - unknown lighting:", pct(len(dark_u), n))
    print("dark - not lighted as share of all dark:", pct(len(dark_nl), dark_all))
    for label, sub in [("all", m), ("dark-not-lighted", dark_nl)]:
        rur = (sub["RUR_URB"] == 1).sum()
        urb = (sub["RUR_URB"] == 2).sum()
        fw = sub["FUNC_SYS"].isin([1, 2]).sum()
        art = sub["FUNC_SYS"].isin([3, 4]).sum()
        col_loc = sub["FUNC_SYS"].isin([5, 6, 7]).sum()
        k = len(sub)
        print(f"[{label}] rural {pct(rur, k)}; urban {pct(urb, k)}; "
              f"interstate+freeway {pct(fw, k)}; other arterial {pct(art, k)}; collector/local {pct(col_loc, k)}")
    rural_or_fw = dark_nl[(dark_nl["RUR_URB"] == 1) | dark_nl["FUNC_SYS"].isin([1, 2])]
    print("dark-not-lighted AND (rural OR interstate/freeway):", pct(len(rural_or_fw), n), "of all pedestrian deaths")
