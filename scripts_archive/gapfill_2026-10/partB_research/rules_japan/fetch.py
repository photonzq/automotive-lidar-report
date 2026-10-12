"""Download one or more URLs to local files with a generic browser User-Agent.

Usage:
    python fetch.py URL OUTFILE [URL OUTFILE ...]

No credentials, no contact details are sent. Output paths are taken as given
(relative paths resolve against the current working directory).
"""
import sys
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def fetch(url, out):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.8,ja;q=0.6",
    })
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
        ctype = r.headers.get("Content-Type", "")
    with open(out, "wb") as f:
        f.write(data)
    print(f"{url} -> {out} ({len(data)} bytes, {ctype})")


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 2 or len(args) % 2:
        sys.exit(__doc__)
    for i in range(0, len(args), 2):
        try:
            fetch(args[i], args[i + 1])
        except Exception as e:  # report and continue with the rest
            print(f"FAILED {args[i]}: {e}")
