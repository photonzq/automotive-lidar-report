"""Fetch public metadata of IEEE Xplore documents (title, authors, affiliations,
abstract, open-access flag, publication details) from the JSON block that the
public document page embeds (xplGlobal.document.metadata).

No login is used and no contact details are sent; a generic browser
User-Agent is used. Only the public landing page is read.

Usage : python ieee_meta.py <arnumber> [<arnumber> ...]
Output: prints a summary per document and writes ieee_<arnumber>.json to the
        folder given by GAPS_SPECS_RAW (default ".").
"""
import json
import os
import re
import sys

import requests

OUT = os.environ.get("GAPS_SPECS_RAW", ".")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def fetch(arnumber):
    url = f"https://ieeexplore.ieee.org/document/{arnumber}"
    r = requests.get(url, headers={"User-Agent": UA}, timeout=60)
    r.raise_for_status()
    m = re.search(r"xplGlobal\.document\.metadata\s*=\s*(\{.*?\});\s*\n", r.text, re.S)
    if not m:
        raise RuntimeError(f"no metadata block found for {arnumber}")
    meta = json.loads(m.group(1))
    with open(os.path.join(OUT, f"ieee_{arnumber}.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    return meta


def summary(meta):
    keys = ("title", "publicationTitle", "volume", "issue", "startPage", "endPage",
            "publicationDate", "doi", "isOpenAccess", "isFreeDocument", "accessType")
    for k in keys:
        if k in meta:
            print(f"{k}: {meta[k]}")
    for a in meta.get("authors", []):
        print("author:", a.get("name"), "|", "; ".join(a.get("affiliation", []) or []))
    print("abstract:", meta.get("abstract"))


if __name__ == "__main__":
    for arn in sys.argv[1:]:
        print("=" * 20, arn)
        try:
            summary(fetch(arn))
        except Exception as exc:  # report and continue with the next number
            print("failed:", exc)
