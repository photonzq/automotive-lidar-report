"""Download one or more URLs to local files with a generic browser User-Agent.

Usage:
    python fetch.py <url> <output_path> [<url> <output_path> ...]

Notes:
- No e-mail address or personal identifier is sent; only a generic browser UA.
- Prints HTTP status, final URL, content type and byte count for each download.
"""
import sys
import urllib.request
import ssl

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def fetch(url, out_path):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    })
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
            data = r.read()
            ctype = r.headers.get("Content-Type", "")
            final = r.geturl()
            status = r.status
    except Exception as e:  # report and continue
        print(f"FAIL {url} -> {e}")
        return False
    with open(out_path, "wb") as f:
        f.write(data)
    print(f"OK {status} {len(data)} bytes {ctype} final={final} -> {out_path}")
    return True


def main(argv):
    if len(argv) < 3 or (len(argv) - 1) % 2:
        print(__doc__)
        return 1
    pairs = list(zip(argv[1::2], argv[2::2]))
    for url, out in pairs:
        fetch(url, out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
