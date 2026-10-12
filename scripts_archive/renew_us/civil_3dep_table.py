"""USGS 3D Elevation Program (3DEP) expenditures FY2015-FY2024, transcribed from the USGS chart.

Purpose
    Writes the 3DEP expenditure series by source, as printed on the USGS figure
    "3D Elevation Program Fiscal Year 2015-2024 Expenditures" (image dated 2024-10-09,
    https://www.usgs.gov/media/images/3d-elevation-program-fiscal-year-2015-2024-expenditures),
    and derives the federal (USGS plus supplemental) and partner totals. 3DEP buys lidar
    elevation data (IfSAR in Alaska), so this is data acquisition, not lidar technology R&D.
    Partners include other federal agencies as well as states and local governments.

Inputs
    out_dir : output folder
Outputs
    usgs_3dep_expenditures_fy2015_2024.csv

Usage:
    python civil_3dep_table.py <out_dir>
"""
import os
import sys

import pandas as pd

SRC = "https://www.usgs.gov/media/images/3d-elevation-program-fiscal-year-2015-2024-expenditures"
# columns: FY, USGS NGP programme management + processing, USGS NGP acquisition, partners' acquisition,
#          supplemental acquisition, supplemental management/processing, chart total ($M)
ROWS = [
    (2015, 16.6, 9.3, 36.2, 0.0, 0.0, 62.3),
    (2016, 17.4, 12.7, 47.3, 0.0, 0.0, 77.5),
    (2017, 17.7, 17.0, 67.3, 0.0, 0.0, 101.9),
    (2018, 17.7, 18.5, 86.6, 17.6, 0.0, 140.3),
    (2019, 17.7, 19.2, 116.2, 2.8, 0.9, 156.7),
    (2020, 17.7, 18.0, 83.3, 7.7, 1.0, 127.7),
    (2021, 17.7, 18.0, 48.2, 0.0, 1.2, 85.1),
    (2022, 18.1, 21.8, 56.6, 9.7, 0.0, 106.1),
    (2023, 18.4, 24.5, 64.6, 17.3, 1.1, 125.9),
    (2024, 21.0, 17.3, 69.0, 8.4, 3.2, 118.9),
]


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    d = pd.DataFrame(ROWS, columns=["fy", "usgs_mgmt_processing", "usgs_acquisition", "partners_acquisition",
                                    "supplemental_acquisition", "supplemental_mgmt", "chart_total"])
    d["usgs_base_total"] = d["usgs_mgmt_processing"] + d["usgs_acquisition"]
    d["supplemental_total"] = d["supplemental_acquisition"] + d["supplemental_mgmt"]
    d["sum_check"] = d[["usgs_base_total", "partners_acquisition", "supplemental_total"]].sum(axis=1).round(1)
    d["source"] = SRC
    d.to_csv(os.path.join(out_dir, "usgs_3dep_expenditures_fy2015_2024.csv"), index=False)
    print(d.drop(columns="source").to_string(index=False))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
