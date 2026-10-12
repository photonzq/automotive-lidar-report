"""robotaxi_fetch_sources.py

Purpose
    Download a list of public web sources (HTML pages, PDFs, JSON API responses)
    used to check robotaxi lidar counts and suppliers (Nuro/Lucid/Uber, Zoox,
    Mercedes-Benz/Momenta/Lumo), and keep an auditable index of what was fetched.

Inputs
    --urls FILE   text file, one source per line: "<label><TAB><url>" or just "<url>".
                  Lines starting with '#' are ignored.
    --out DIR     output data folder (relative path recommended), created if absent.
    --delay S     seconds to wait between requests (default 1.5).

Outputs
    DIR/<label>.<ext>    raw response body (html / pdf / json / txt by content type)
    DIR/fetch_index.csv  one row per request: utc time, label, url, final url,
                         HTTP status, content type, bytes, sha256, saved file name

Notes
    - Uses a generic browser-like User-Agent only; no contact details, e-mail
      addresses or names are sent in any header or parameter.
    - No logins, no cookies carried between sites, no paywall circumvention.

Date: 2026-10-03
"""
import argparse
import csv
import datetime as dt
import hashlib
import os
import re
import time

import requests

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
HEADERS = {"User-Agent": UA,
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                     "application/pdf,application/json;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,de;q=0.4,ja;q=0.3"}


def safe_label(text, maxlen=80):
    text = re.sub(r"^https?://", "", text)
    text = re.sub(r"[^A-Za-z0-9._-]+", "_", text).strip("_")
    return text[:maxlen] or "page"


def ext_for(ctype, url):
    ctype = (ctype or "").lower()
    if "pdf" in ctype or url.lower().endswith(".pdf"):
        return "pdf"
    if "json" in ctype:
        return "json"
    if "html" in ctype or "xml" in ctype:
        return "html"
    if "image/png" in ctype:
        return "png"
    if "image/jpeg" in ctype:
        return "jpg"
    if "image/webp" in ctype:
        return "webp"
    return "txt"


def read_list(path):
    items = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "\t" in line:
                label, url = line.split("\t", 1)
            else:
                label, url = safe_label(line), line
            items.append((safe_label(label), url.strip()))
    return items


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--urls", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--delay", type=float, default=1.5)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    index_path = os.path.join(args.out, "fetch_index.csv")
    new_file = not os.path.exists(index_path)
    with open(index_path, "a", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh)
        if new_file:
            wr.writerow(["utc", "label", "url", "final_url", "status",
                         "content_type", "bytes", "sha256", "saved_as"])
        for label, url in read_list(args.urls):
            t = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            try:
                r = requests.get(url, headers=HEADERS, timeout=60,
                                 allow_redirects=True)
                body = r.content
                ext = ext_for(r.headers.get("Content-Type"), r.url)
                name = f"{label}.{ext}"
                with open(os.path.join(args.out, name), "wb") as out:
                    out.write(body)
                wr.writerow([t, label, url, r.url, r.status_code,
                             r.headers.get("Content-Type", ""), len(body),
                             hashlib.sha256(body).hexdigest(), name])
                print(f"{r.status_code}  {len(body):>9d}  {name}")
            except Exception as exc:  # keep going; record the failure
                wr.writerow([t, label, url, "", "ERR", repr(exc)[:200], 0, "", ""])
                print(f"ERR  {label}  {exc!r}"[:200])
            fh.flush()
            time.sleep(args.delay)


if __name__ == "__main__":
    main()
