"""Download the annual accounts filed with the National Bank of Belgium's
Central Balance Sheet Office (public 'Consult' service, consult.cbso.nbb.be)
for one Belgian enterprise number.

Usage (run from the eic_fund folder):
    python scripts/nbb_cbso_download.py 0745364628 voxelsensors
Lists the published deposit ids (/api/rs-consult/published-deposits/ids),
then saves each deposit's PDF (/api/external/broker/public/deposits/pdf/<id>)
and, where available, the CSV extract (/consult/csv/<id>) under
raw/nbb_<label>/. No login is needed; nothing personal is sent.
"""
import json
import sys
import time
from pathlib import Path

import requests

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
BASE = "https://consult.cbso.nbb.be/api"


def main(num, label):
    out = Path(f"raw/nbb_{label}")
    out.mkdir(parents=True, exist_ok=True)
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept": "application/json, text/plain, */*",
                      "Referer": f"https://consult.cbso.nbb.be/consult-enterprise/{num}"})
    r = s.get(f"{BASE}/rs-consult/published-deposits/ids", params={"enterpriseNumber": num}, timeout=60)
    r.raise_for_status()
    ids = r.json()
    (out / "deposit_ids.json").write_text(json.dumps(ids, indent=1), encoding="utf-8")
    print(len(ids), "deposits")
    for d in ids:
        did = d["id"]
        for kind, path, ext in (("pdf", f"/external/broker/public/deposits/pdf/{did}", "pdf"),
                                ("csv", f"/external/broker/public/deposits/consult/csv/{did}", "csv")):
            time.sleep(0.8)
            rr = s.get(BASE + path, timeout=120)
            ctype = rr.headers.get("Content-Type", "")
            print(did, kind, rr.status_code, ctype, len(rr.content))
            if rr.ok and len(rr.content) > 200:
                (out / f"{did}.{ext}").write_bytes(rr.content)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
