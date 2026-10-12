"""Download a URL to a local file with a generic browser User-Agent.

Usage:
    python fetch.py URL OUTFILE [--referer URL]

No e-mail address or personal identifier is sent in any header.
Prints the HTTP status, final URL, content type and byte count.
"""
import argparse
import sys

import requests

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("outfile")
    ap.add_argument("--referer", default=None)
    args = ap.parse_args()

    headers = {
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                  "application/pdf,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    }
    if args.referer:
        headers["Referer"] = args.referer
    try:
        r = requests.get(args.url, headers=headers, timeout=60,
                         allow_redirects=True)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR {exc}")
        sys.exit(1)
    with open(args.outfile, "wb") as fh:
        fh.write(r.content)
    print(f"status={r.status_code} final={r.url} "
          f"type={r.headers.get('Content-Type')} bytes={len(r.content)}")


if __name__ == "__main__":
    main()
