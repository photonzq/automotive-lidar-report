"""List the public docket of NHTSA defect investigations (e.g. EA26002, AQ26002).

Queries NHTSA's public "safety issues" API,
    https://api.nhtsa.gov/safetyIssues/byNhtsaId?nhtsaId=<ID>&name=investigations
and prints, for each investigation ID given on the command line: the opening
and closing dates, any linked recall campaigns, and every associated document
(load date, file name, NHTSA's one-line summary and URL) in date order.

Document-name prefixes seen in the dockets:
  INOA / INOV  opening resume and ODI report numbers
  INIM         information request or special order to the manufacturer
  INRE         memo granting a response-time extension
  INCCS        placeholder: documents responsive to question Qn are the subject
               of a confidential-business-information (CBI) request
  INRL         manufacturer's response letter (public version)

Optionally (--flat FLAT_INV.zip) it also prints the matching rows of ODI's
investigation flat file (https://static.nhtsa.gov/odi/ffdd/inv/FLAT_INV.zip),
whose field 8 is the closing date and field 9 the recall campaign number.

Usage:
    python nhtsa_investigation_docket.py EA26002 AQ26002 [--flat FLAT_INV.zip]

No credentials or contact details are sent; a generic User-Agent is used.
"""
import io
import json
import sys
import urllib.request
import zipfile

API = "https://api.nhtsa.gov/safetyIssues/byNhtsaId?nhtsaId={}&name=investigations"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"


def fetch(nhtsa_id):
    """Return the parsed API response for one investigation."""
    req = urllib.request.Request(API.format(nhtsa_id), headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def show(nhtsa_id):
    """Print dates, recalls and the document list of one investigation."""
    d = fetch(nhtsa_id)
    res = d["results"][0]
    inv = res["investigations"][0]
    print(f"== {inv['nhtsaActionNumber']}: {inv['subject']}")
    print(f"   opened {inv['dateOpened']}, closed {inv['dateClosed']}, "
          f"recalls {[r.get('nhtsaCampaignNumber') for r in res.get('recalls', [])]}")
    for doc in sorted(inv["associatedDocuments"], key=lambda x: x["loadDate"]):
        print(f"   {doc['loadDate'][:10]}  {doc['fileName']:<28} {doc['summary']}  {doc['url']}")


def flat_rows(path, ids):
    """Print the flat-file rows (first 10 fields) for the given IDs."""
    with zipfile.ZipFile(path) as z, z.open("FLAT_INV.txt") as f:
        seen = set()
        for line in io.TextIOWrapper(f, encoding="latin-1"):
            parts = line.rstrip("\n").split("\t")
            if parts[0] in ids and parts[0] not in seen:
                seen.add(parts[0])
                print("   flat file:", " | ".join(parts[:10]))


def main(argv):
    flat = None
    if "--flat" in argv:
        i = argv.index("--flat")
        flat = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    ids = argv or ["EA26002"]
    for nid in ids:
        show(nid)
    if flat:
        flat_rows(flat, set(ids))


if __name__ == "__main__":
    main(sys.argv[1:])
