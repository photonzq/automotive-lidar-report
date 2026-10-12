"""List and download file formats of regulations.gov documents.

Usage:
    python regs_docket.py OUTDIR DOC_ID [DOC_ID ...]

Uses the public regulations.gov v4 API with the generic api.data.gov
DEMO_KEY (rate limited). For each document id it prints the main file and
attachment URLs and downloads every PDF into OUTDIR/<DOC_ID>_<name>.pdf.
No e-mail address or personal identifier is sent.
"""
import json
import os
import sys
import time

import requests

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
API = "https://api.regulations.gov/v4/documents/{}?include=attachments&api_key=DEMO_KEY"


def get(url):
    return requests.get(url, headers={"User-Agent": UA}, timeout=90)


def main():
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for doc_id in sys.argv[2:]:
        r = get(API.format(doc_id))
        if r.status_code != 200:
            print(doc_id, "API status", r.status_code, r.text[:200])
            continue
        d = r.json()
        attrs = d["data"]["attributes"]
        print(f"== {doc_id} | {attrs.get('title')} | posted {attrs.get('postedDate')}")
        files = []
        for ff in attrs.get("fileFormats") or []:
            files.append(("content", ff.get("fileUrl")))
        for inc in d.get("included", []) or []:
            ia = inc.get("attributes", {})
            for ff in ia.get("fileFormats") or []:
                files.append((ia.get("title", "att"), ff.get("fileUrl")))
        for title, url in files:
            if not url:
                continue
            name = url.rstrip("/").split("/")[-1]
            out = os.path.join(outdir, f"{doc_id}_{name}")
            print(f"   [{title}] {url}")
            if url.lower().endswith(".pdf") and not os.path.exists(out):
                fr = get(url)
                with open(out, "wb") as fh:
                    fh.write(fr.content)
                print(f"      saved {out} ({len(fr.content)} bytes, {fr.status_code})")
        time.sleep(1.0)


if __name__ == "__main__":
    main()
