"""Search the Federal Register API for documents on a term and grep their full text for sensor counts.

Purpose: find NHTSA notices on Zoox's exemption petition (49 CFR Part 555) or other Zoox
documents that state how many lidars, cameras and radars the robotaxi carries (Appendix 1, Zoox).
Usage:   python robotaxi_zoox_federal_register.py [TERM] [OUTDIR]   (defaults: Zoox, ./fr)
Inputs:  public Federal Register API (https://www.federalregister.gov/api/v1), no key needed.
Outputs: document list printed; raw text of each document saved in OUTDIR; context printed
         around every match of lidar/LiDAR/camera/radar counts.
Date:    2026-10-03
"""
import os
import re
import sys

import requests

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"
API = "https://www.federalregister.gov/api/v1/documents.json"
PAT = re.compile(r"(?i)(\b(?:one|two|three|four|five|six|seven|eight|nine|ten|twelve|\d+)\s+(?:\w+\s+){0,3}?"
                 r"(?:lidar|lidars|cameras?|radars?|sensors?)\b|lidar)")


def main():
    term = sys.argv[1] if len(sys.argv) > 1 else "Zoox"
    outdir = sys.argv[2] if len(sys.argv) > 2 else "fr"
    os.makedirs(outdir, exist_ok=True)
    params = {"conditions[term]": term, "per_page": 100, "order": "newest",
              "fields[]": ["title", "publication_date", "document_number", "raw_text_url", "html_url", "agencies"]}
    d = requests.get(API, params=params, headers={"User-Agent": UA}, timeout=60).json()
    print("count", d.get("count"))
    for doc in d.get("results", []):
        print(doc["publication_date"], doc["document_number"], doc["title"][:110], doc["html_url"])
        fn = os.path.join(outdir, doc["document_number"] + ".txt")
        if not os.path.exists(fn) and doc.get("raw_text_url"):
            r = requests.get(doc["raw_text_url"], headers={"User-Agent": UA}, timeout=60)
            open(fn, "w", encoding="utf-8").write(r.text)
        if os.path.exists(fn):
            t = re.sub(r"\s+", " ", open(fn, encoding="utf-8").read())
            if term.lower() not in t.lower():
                continue
            for m in PAT.finditer(t):
                print("    ...", t[max(0, m.start() - 250): m.end() + 250], "...")


if __name__ == "__main__":
    main()
