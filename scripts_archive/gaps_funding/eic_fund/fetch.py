"""Fetch one or more URLs and save the raw response bodies under ../raw/.

Usage (run from the eic_fund folder):
    python scripts/fetch.py URL [URL ...]
    python scripts/fetch.py --name custom_name.html URL

Each body is saved as raw/<sanitised-name>; a JSON log line (url, status,
final url, content-type, bytes, saved file) is appended to raw/fetch_log.jsonl.
A generic browser User-Agent is sent; no personal data, e-mail address or
credential is put in any header, URL or parameter.
"""
import json
import re
import sys
import time
from pathlib import Path

import requests

RAW = Path("raw")
RAW.mkdir(exist_ok=True)
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
HEADERS = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.8,de;q=0.6,fr;q=0.5,nl;q=0.4"}


def safe_name(url: str) -> str:
    name = re.sub(r"^https?://", "", url)
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_")
    return name[:150]


def fetch(url: str, name: str | None = None) -> None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=60, allow_redirects=True)
    except Exception as exc:  # network errors are logged, not raised
        print(f"ERR {url}: {exc}")
        with open(RAW / "fetch_log.jsonl", "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"url": url, "error": str(exc), "t": time.time()}) + "\n")
        return
    ctype = r.headers.get("Content-Type", "")
    fname = name or safe_name(url)
    if "pdf" in ctype.lower() and not fname.lower().endswith(".pdf"):
        fname += ".pdf"
    elif "html" in ctype.lower() and not re.search(r"\.html?$", fname, re.I):
        fname += ".html"
    elif "json" in ctype.lower() and not fname.lower().endswith(".json"):
        fname += ".json"
    (RAW / fname).write_bytes(r.content)
    rec = {"url": url, "status": r.status_code, "final_url": r.url,
           "content_type": ctype, "bytes": len(r.content), "file": fname,
           "t": time.time()}
    with open(RAW / "fetch_log.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(f"{r.status_code} {len(r.content):>9} {ctype[:30]:<30} {fname}")


if __name__ == "__main__":
    args = sys.argv[1:]
    custom = None
    if args and args[0] == "--name":
        custom = args[1]
        args = args[2:]
    for u in args:
        fetch(u, custom)
        time.sleep(1.0)
