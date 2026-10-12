"""Search the USPTO Assignment Center (public, no login) for recorded patent
assignments by assignor or assignee name, and list the patents in each one.

It uses the same public JSON endpoints as the Assignment Center web page
(https://assignmentcenter.uspto.gov/search/patent):
  POST /ipas/search/api/v3/public/search/patent
    - name search:  {"searchCriteria": [{"property": NAME, "searchBy":
                     "assignorName"|"assigneeName", "matchType": "Contains", ...}],
                     "dataFilter": {...}}
    - reel/frame:   {"reelNumber": R, "frameNumber": F, "searchBy": "reelFrame", ...}
    - one patent:   {"property": NUMBER, "searchBy": "patentNumber"|"publicationNumber"
                     |"applicationNumber", ...}
It was used to check whether the patents of failed lidar companies (Baraja,
LeddarTech, TetraVue, Scantinel, Ibeo and others) were transferred, to whom and
when.

Usage:
    python uspto_assignment_search.py --out DIR --assignor "BARAJA" --assignor "LEDDARTECH"
    python uspto_assignment_search.py --out DIR --assignee "NLIGHT" --details
    python uspto_assignment_search.py --out DIR --patent 12510751

Writes DIR/assignments_<tag>.json (raw) and prints one line per assignment:
recorded date | reel/frame | conveyance | assignors -> assignees | properties.
Requests are spaced by --sleep seconds; no personal data is sent.
"""
import argparse
import json
import os
import re
import time
import urllib.request

BASE = "https://assignmentcenter.uspto.gov/ipas/search/api/v3/public/search/patent"
HDRS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/json", "Accept": "application/json",
        "Origin": "https://assignmentcenter.uspto.gov"}


def post(body, tries=3):
    data = json.dumps(body).encode("utf-8")
    for k in range(tries):
        try:
            req = urllib.request.Request(BASE, data=data, headers=HDRS, method="POST")
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode("utf-8", errors="replace"))
        except Exception:  # transient errors: back off and retry
            if k == tries - 1:
                raise
            time.sleep(5 * (k + 1))


def name_search(name, field, rows=100, sleep=1.5):
    """All assignment summaries whose assignor/assignee name contains `name`."""
    out, page = [], 1
    while True:
        body = {"searchCriteria": [{"property": name, "searchBy": field, "matchType": "Contains",
                                    "order": 1, "relation": ""}],
                "dataFilter": {"rowsPerPage": rows, "currentPage": page}}
        d = post(body)["successResponse"]
        data = d.get("data") or []
        out += data
        total = d.get("totalRows") or 0
        if len(out) >= total or not data:
            break
        page += 1
        time.sleep(sleep)
    return out


def reel_frame_details(reel, frame):
    body = {"reelNumber": str(reel), "frameNumber": str(frame), "searchBy": "reelFrame",
            "dataFilter": {"rowsPerPage": 100, "currentPage": 1}}
    return post(body)["successResponse"]


def property_search(number, field):
    body = {"property": str(number), "searchBy": field,
            "dataFilter": {"rowsPerPage": 50, "currentPage": 1}}
    return post(body)["successResponse"]


def props_of(details):
    """Return a list of 'patent/publication/application: title' strings."""
    out = []
    data = details.get("data") or {}
    props = data.get("properties") if isinstance(data, dict) else None
    if isinstance(props, dict):
        props = [props]
    for p in props or []:
        num = p.get("patentNumber") or p.get("publicationNumber") or p.get("applicationNumber")
        out.append("%s (%s): %s" % (num, p.get("applicationNumber"), (p.get("inventionTitle") or "")[:70]))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=".")
    ap.add_argument("--assignor", action="append", default=[])
    ap.add_argument("--assignee", action="append", default=[])
    ap.add_argument("--patent", action="append", default=[])
    ap.add_argument("--details", action="store_true", help="also list the patents in each assignment")
    ap.add_argument("--sleep", type=float, default=1.5)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    jobs = [(n, "assignorName") for n in a.assignor] + [(n, "assigneeName") for n in a.assignee]
    for name, field in jobs:
        rows = name_search(name, field, sleep=a.sleep)
        rows.sort(key=lambda r: (r.get("recorded") or "")[-4:] + (r.get("recorded") or ""))
        print("\n#### %s contains %r: %d assignments" % (field, name, len(rows)))
        for r in rows:
            ors = "; ".join(x.get("assignorName", "") for x in r.get("assignors") or [])
            ees = "; ".join(r.get("assignees") or [])
            line = "%s | %s/%s | %s | %s -> %s" % (r.get("recorded"), r.get("reelNumber"), r.get("frameNumber"),
                                                 (r.get("conveyance") or "").strip()[:60], ors[:120], ees[:120])
            if a.details:
                time.sleep(a.sleep)
                try:
                    r["details"] = reel_frame_details(r["reelNumber"], r["frameNumber"])
                    line += " | " + " || ".join(props_of(r["details"]))
                except Exception as e:
                    line += " | details failed: %s" % e
            print(line)
        tag = re.sub(r"\W+", "_", field + "_" + name).strip("_")
        with open(os.path.join(a.out, "assignments_%s.json" % tag), "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=1, ensure_ascii=False)
        time.sleep(a.sleep)
    for num in a.patent:
        field = "publicationNumber" if len(num) > 8 else "patentNumber"
        d = property_search(num, field)
        with open(os.path.join(a.out, "patent_%s.json" % num), "w", encoding="utf-8") as f:
            json.dump(d, f, indent=1, ensure_ascii=False)
        data = d.get("data") or {}
        print("\n#### %s %s: %s assignments" % (field, num, data.get("noOfAssignments")))
        for asg in data.get("assignment") or []:
            print("%s | %s | %s | %s -> %s" % (asg.get("recordationDate"), asg.get("reelFrame"),
                                               (asg.get("conveyance") or "")[:60],
                                               "; ".join(x.get("assignorName", "") for x in asg.get("assignors") or []),
                                               "; ".join(x.get("assigneeName", "") for x in asg.get("assignees") or [])))
        time.sleep(a.sleep)


if __name__ == "__main__":
    main()
