"""Download USAspending.gov prime transactions whose text matches lidar terms.

Purpose
    Requests the Advanced Search transaction download (POST /api/v2/download/transactions/)
    for one keyword set and a fiscal-year window, polls the status endpoint until the zip
    file is ready, then downloads and unpacks it. The zip holds full FPDS (contracts) and
    FABS (assistance) columns, including the FPDS "research" field that marks SBIR/STTR
    phases (SR1/SR2/SR3/ST1/ST2/ST3), product/service codes and action dates.

    The keyword filter is USAspending's full-text "keywords" filter (any listed string,
    searched over the transaction's text fields such as descriptions and recipient names).
    The API needs no key. No personal identifier is sent with any request.

Inputs
    out_dir   : directory for the zip and unpacked CSVs
    tag       : short label for the run, used in file names (e.g. lidar)
    keywords  : one or more search strings (quote multi-word strings)
Options
    --start YYYY-MM-DD (default 2007-10-01), --end YYYY-MM-DD (default 2026-09-30)

Outputs
    <out_dir>/<tag>.zip and its unpacked CSV files under <out_dir>/<tag>/

Usage:
    python usasp_lidar_download.py <out_dir> <tag> lidar ladar "laser radar" [--start 2007-10-01] [--end 2026-09-30]
"""
import json
import os
import sys
import time
import zipfile

import requests

API = "https://api.usaspending.gov"
HEAD = {"User-Agent": "research-script/1.0", "Content-Type": "application/json"}


def main(argv):
    if len(argv) < 4:
        sys.exit(__doc__)
    args = list(argv[1:])
    start, end = "2007-10-01", "2026-09-30"
    if "--start" in args:
        i = args.index("--start"); start = args[i + 1]; del args[i:i + 2]
    if "--end" in args:
        i = args.index("--end"); end = args[i + 1]; del args[i:i + 2]
    out_dir, tag, keywords = args[0], args[1], args[2:]
    os.makedirs(out_dir, exist_ok=True)
    body = {"filters": {"keywords": keywords,
                        "time_period": [{"start_date": start, "end_date": end}]},
            "file_format": "csv"}
    r = requests.post(API + "/api/v2/download/transactions/", headers=HEAD, data=json.dumps(body), timeout=120)
    r.raise_for_status()
    job = r.json()
    print("requested", job.get("file_name"))
    status_url = job["status_url"]
    if status_url.startswith("/"):
        status_url = API + status_url
    while True:
        s = requests.get(status_url, headers=HEAD, timeout=120).json()
        print(s.get("status"), s.get("total_rows"), s.get("seconds_elapsed"))
        if s.get("status") == "finished":
            url = s["file_url"]
            break
        if s.get("status") == "failed":
            sys.exit("download failed: " + str(s.get("message")))
        time.sleep(15)
    zpath = os.path.join(out_dir, tag + ".zip")
    with requests.get(url, headers={"User-Agent": HEAD["User-Agent"]}, stream=True, timeout=600) as g:
        g.raise_for_status()
        with open(zpath, "wb") as f:
            for chunk in g.iter_content(1 << 20):
                f.write(chunk)
    with zipfile.ZipFile(zpath) as z:
        z.extractall(os.path.join(out_dir, tag))
        for n in z.namelist():
            print(n, z.getinfo(n).file_size)
    with open(os.path.join(out_dir, tag + "_request.json"), "w") as f:
        json.dump({"request": body, "status": s}, f, indent=1)


if __name__ == "__main__":
    main(sys.argv)
