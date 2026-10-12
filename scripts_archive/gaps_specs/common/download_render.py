"""Download public PDFs and render every page (or selected pages) to PNG.

Used for open documents only: arXiv and open-access papers, conference
programmes, distributor-hosted datasheets, regulatory filings and preprints.
No login, no paywall circumvention, no contact details; a generic browser
User-Agent is used and TLS certificates are verified (a site with an expired
certificate is skipped, not bypassed).

Usage : python download_render.py <url> <out_name.pdf> [--pages 1-4] [--dpi 160]
Output: <out_name.pdf> and <out_name>_p<k>.png in the folder given by
        GAPS_SPECS_RAW (default ".").
"""
import argparse
import os

import pymupdf
import requests

OUT = os.environ.get("GAPS_SPECS_RAW", ".")
UA = {"User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                     "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")}


def page_list(spec, n):
    if not spec:
        return list(range(n))
    a, _, b = spec.partition("-")
    return list(range(int(a) - 1, min(n, int(b or a))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("name")
    ap.add_argument("--pages", default="")
    ap.add_argument("--dpi", type=int, default=160)
    a = ap.parse_args()
    r = requests.get(a.url, headers=UA, timeout=300)
    r.raise_for_status()
    pdf_path = os.path.join(OUT, a.name)
    with open(pdf_path, "wb") as fh:
        fh.write(r.content)
    doc = pymupdf.open(pdf_path)
    stem = os.path.splitext(a.name)[0]
    print(pdf_path, len(r.content), "bytes,", doc.page_count, "pages")
    for i in page_list(a.pages, doc.page_count):
        fn = os.path.join(OUT, f"{stem}_p{i + 1}.png")
        doc[i].get_pixmap(dpi=a.dpi).save(fn)
        print("rendered", fn)


if __name__ == "__main__":
    main()
