"""Download US patent/application PDFs from the USPTO public print service and
grep their text for keywords.

Usage:
    python item5b_fetch_uspto.py OUTDIR NUMBER [NUMBER ...] [--kw word1,word2,...]

NUMBER is a granted patent number (e.g. 11422238) or an 11-digit application
publication number (e.g. 20240302648). PDFs are saved as OUTDIR/US<NUMBER>.pdf.
For each PDF the script prints the page count, the first-page text (title,
assignee, priority data) and every line that contains one of the keywords,
with its page index (0-based), so that the relevant pages can be rendered.
Uses a generic User-Agent; sends no personal data.
"""
import os
import sys
import time
import urllib.request

import pymupdf

BASE = "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/"
UA = {"User-Agent": "research-script/1.0"}


def fetch(num, outdir):
    path = os.path.join(outdir, f"US{num}.pdf")
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        return path
    req = urllib.request.Request(BASE + num, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    with open(path, "wb") as f:
        f.write(data)
    time.sleep(1.0)
    return path


def main():
    args = sys.argv[1:]
    kws = []
    if "--kw" in args:
        i = args.index("--kw")
        kws = [k.strip().lower() for k in args[i + 1].split(",") if k.strip()]
        args = args[:i] + args[i + 2:]
    outdir, nums = args[0], args[1:]
    os.makedirs(outdir, exist_ok=True)
    for num in nums:
        try:
            path = fetch(num, outdir)
        except Exception as e:  # network or HTTP error
            print(f"== US{num}: download failed: {e}")
            continue
        try:
            d = pymupdf.open(path)
        except Exception as e:
            print(f"== US{num}: not a readable PDF: {e}")
            continue
        print(f"\n== US{num}: {d.page_count} pages")
        first = d[0].get_text()
        print(first[:1800])
        if kws:
            for pi in range(d.page_count):
                for line in d[pi].get_text().splitlines():
                    low = line.lower()
                    if any(k in low for k in kws):
                        print(f"  p{pi}: {line.strip()[:220]}")


if __name__ == "__main__":
    main()
