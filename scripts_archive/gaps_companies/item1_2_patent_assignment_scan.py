"""Scan Google Patents for a company's patents and list their assignment history.

For each search term (an assignee name, optionally an inventor), the script
queries the public Google Patents search endpoint, then opens every result page
and extracts the original and current assignee and every recorded assignment
("AS") legal event: date, new owner, conveyance text, reel/frame and effective
date. It was used to trace where the patents of TetraVue (to nLIGHT, via a
Chapter 7 trustee) and LeddarTech went after each company failed.

Usage:
    python item1_2_patent_assignment_scan.py --assignee TetraVue --out out_dir
    python item1_2_patent_assignment_scan.py --assignee LeddarTech --out out_dir
    python item1_2_patent_assignment_scan.py --assignee "VayaVision" --out out_dir

Outputs (in --out): <tag>_results.json and <tag>_assignments.csv.
Only public pages are read; requests are spaced by --sleep seconds.
"""
import argparse
import csv
import html
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"


def get(url, timeout=60, tries=4):
    """GET with a simple backoff on HTTP 429/503 (the endpoint rate-limits)."""
    for k in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and k < tries - 1:
                time.sleep(10 * (k + 1))
                continue
            raise


def search(assignee, inventor=None, sleep=1.5):
    """Return a list of result dicts from the Google Patents search endpoint."""
    out, page = [], 0
    while True:
        q = "assignee=" + assignee
        if inventor:
            q += "&inventor=" + inventor
        q += "&num=100" + ("&page=%d" % page if page else "")
        url = "https://patents.google.com/xhr/query?url=" + urllib.parse.quote(q, safe="") + "&exp="
        d = json.loads(get(url))
        res = d.get("results", {})
        for c in res.get("cluster", []):
            for x in c.get("result", []):
                p = x["patent"]
                out.append({
                    "publication_number": p.get("publication_number"),
                    "title": html.unescape(re.sub("<[^>]+>", "", p.get("title", ""))).strip(),
                    "priority_date": p.get("priority_date"),
                    "filing_date": p.get("filing_date"),
                    "publication_date": p.get("publication_date"),
                    "assignee_listed": html.unescape(re.sub("<[^>]+>", "", p.get("assignee", ""))),
                })
        page += 1
        if page >= res.get("total_num_pages", 1):
            break
        time.sleep(sleep)
    return out


def parse_page(s):
    """Extract current/original assignee (of this patent only) and AS legal events."""
    # The page lists assignees of cited/similar documents too; the patent's own
    # assignees appear in the header <dl> before the first 'Info' section.
    head = s.split('itemprop="citations"')[0] if 'itemprop="citations"' in s else s
    cur = [html.unescape(m).strip() for m in re.findall(r'itemprop="assigneeCurrent"[^>]*>\s*([^<]+)', head)]
    orig = [html.unescape(m).strip() for m in re.findall(r'itemprop="assigneeOriginal"[^>]*>\s*([^<]+)', head)]
    status = re.findall(r'itemprop="legalStatusIfi"[^>]*>(.*?)</', s, flags=re.S)
    events = []
    for m in re.finditer(r'<tr itemprop="legalEvents"[^>]*>(.*?)</tr>', s, flags=re.S):
        row = html.unescape(re.sub(r"<[^>]+>", " | ", m.group(1)))
        row = re.sub(r"\s+", " ", row)
        row = re.sub(r"(\|\s*)+", "| ", row).strip(" |")
        if re.search(r"\|\s*AS\s*\|", "| " + row + " |") or "Assignment" in row or "ASSIGNMENT" in row:
            events.append(row)
    return {"assignee_current": cur[:3], "assignee_original": orig[:3],
            "legal_status": [html.unescape(re.sub("<[^>]+>", "", x)).strip() for x in status][:1],
            "assignment_events": events}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--assignee", required=True)
    ap.add_argument("--inventor", default=None)
    ap.add_argument("--out", default=".")
    ap.add_argument("--sleep", type=float, default=1.5)
    ap.add_argument("--us-only", action="store_true", help="open only US documents")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tag = re.sub(r"\W+", "_", a.assignee + ("_" + a.inventor if a.inventor else "")).strip("_")
    results = search(a.assignee, a.inventor, a.sleep)
    for r in results:
        pn = r["publication_number"]
        if a.us_only and not pn.startswith("US"):
            continue
        try:
            s = get("https://patents.google.com/patent/%s/en" % pn)
            r.update(parse_page(s))
        except Exception as e:  # keep going on a single failure
            r["error"] = str(e)
        time.sleep(a.sleep)
    with open(os.path.join(a.out, tag + "_results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1, ensure_ascii=False)
    with open(os.path.join(a.out, tag + "_assignments.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["publication_number", "title", "priority_date", "filing_date", "publication_date",
                    "assignee_listed", "assignee_current", "assignment_event"])
        for r in results:
            evs = r.get("assignment_events") or [""]
            for ev in evs:
                w.writerow([r["publication_number"], r["title"], r["priority_date"], r["filing_date"],
                            r["publication_date"], r["assignee_listed"],
                            "; ".join(r.get("assignee_current", [])), ev])
    print("%d documents; written to %s" % (len(results), a.out))


if __name__ == "__main__":
    main()
