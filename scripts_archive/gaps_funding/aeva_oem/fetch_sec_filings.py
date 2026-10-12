"""Download selected SEC EDGAR filings (all documents in each filing) for one issuer.

Reads ./sec_submissions.json (the data.sec.gov submissions JSON for the issuer),
selects filings by form type and date window, then for each filing downloads the
EDGAR folder index (index.json) and every .htm/.html/.txt/.pdf/.xml document into
./sec/<filingDate>_<form>_<accession>/ . A plain, contact-free User-Agent is used.
Requests are throttled to stay well under the EDGAR fair-access rate limit.

Usage (run from the aeva_oem folder):
    python scripts/fetch_sec_filings.py
"""
import json
import os
import time
import urllib.request

UA = "research-script/1.0"
CIK = "1789029"
FORMS = {"10-K", "10-Q", "8-K", "S-3ASR", "424B5", "DEF 14A", "DEFA14A",
         "SCHEDULE 13D/A", "25-NSE", "SD", "S-8"}
DATE_MIN = "2025-10-01"
EXTS = (".htm", ".html", ".txt", ".pdf", ".xml", ".jpg", ".png", ".gif")


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    time.sleep(0.25)
    return data if binary else data.decode("utf-8", errors="replace")


def main():
    sub = json.load(open("sec_submissions.json", encoding="utf-8"))
    rec = sub["filings"]["recent"]
    os.makedirs("sec", exist_ok=True)
    for i in range(len(rec["form"])):
        form, fdate, acc = rec["form"][i], rec["filingDate"][i], rec["accessionNumber"][i]
        if fdate < DATE_MIN or form not in FORMS:
            continue
        accnd = acc.replace("-", "")
        folder = os.path.join("sec", f"{fdate}_{form.replace(' ', '_').replace('/', '-')}_{acc}")
        os.makedirs(folder, exist_ok=True)
        base = f"https://www.sec.gov/Archives/edgar/data/{CIK}/{accnd}/"
        try:
            idx = json.loads(get(base + "index.json"))
        except Exception as e:  # noqa: BLE001
            print("index fail", acc, e)
            continue
        json.dump(idx, open(os.path.join(folder, "index.json"), "w"), indent=1)
        for item in idx["directory"]["item"]:
            name = item["name"]
            if not name.lower().endswith(EXTS):
                continue
            out = os.path.join(folder, name)
            if os.path.exists(out) and os.path.getsize(out) > 0:
                continue
            try:
                data = get(base + name, binary=True)
                open(out, "wb").write(data)
                print(fdate, form, name, len(data))
            except Exception as e:  # noqa: BLE001
                print("doc fail", acc, name, e)


if __name__ == "__main__":
    main()
