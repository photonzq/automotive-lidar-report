# -*- coding: utf-8 -*-
"""
Download Swiss Official Gazette of Commerce (SOGC / FOSC / SHAB) publications
from the public SHAB archive servlet by publication id (DOCID), then
locate the page(s) mentioning a search word with page.get_text() and render
those pages to PNG at 160 dpi with PyMuPDF (pages must be READ as images;
get_text() is only used to find them).

Also fetches the Zefix public firm record (JSON) that carries the post-2016
SOGC message texts.

No login, no email, no key; generic browser User-Agent only.
Usage:
  python R3_fastree_sogc_fetch.py <OUTDIR> <WORD> <DOCID> [<DOCID> ...]
  e.g. <scratch>/r3/fastree Fastree 974895 7225834 1805463
Optional env ZEFIX_EHRAID=<id> to also save zefix_firm_<id>.json.
"""
import os
import re
import sys
import time

import pymupdf
import requests

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
ARCHIVE = "https://www.shab.ch/shabforms/servlet/Search?EID=7&DOCID={}"
ZEFIX = "https://www.zefix.ch/ZefixREST/api/v1/firm/{}.json"


def main(outdir, word, docids):
    os.makedirs(os.path.join(outdir, "png"), exist_ok=True)
    s = requests.Session()
    s.headers["User-Agent"] = UA
    eh = os.environ.get("ZEFIX_EHRAID")
    if eh:
        r = s.get(ZEFIX.format(eh), headers={"Accept": "application/json"},
                  timeout=60)
        print("zefix", r.status_code, len(r.content))
        with open(os.path.join(outdir, f"zefix_firm_{eh}.json"), "wb") as f:
            f.write(r.content)
    pat = re.compile(word, re.I)
    for did in docids:
        fn = os.path.join(outdir, f"sogc_{did}.pdf")
        if not os.path.exists(fn):
            r = s.get(ARCHIVE.format(did), timeout=120)
            print(did, r.status_code, r.headers.get("Content-Type"),
                  len(r.content))
            if r.status_code != 200 or r.content[:4] != b"%PDF":
                with open(fn + ".err.txt", "wb") as f:
                    f.write(r.content[:20000])
                continue
            with open(fn, "wb") as f:
                f.write(r.content)
            time.sleep(1.5)
        d = pymupdf.open(fn)
        hits = [i for i in range(d.page_count) if pat.search(d[i].get_text())]
        print(did, "pages", d.page_count, "hits", hits,
              "created", d.metadata.get("creationDate"))
        for i in (hits or range(min(d.page_count, 2))):
            d[i].get_pixmap(dpi=160).save(
                os.path.join(outdir, "png", f"sogc_{did}_p{i + 1}.png"))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
