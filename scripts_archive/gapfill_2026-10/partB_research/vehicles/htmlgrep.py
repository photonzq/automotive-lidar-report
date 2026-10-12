"""Strip an HTML file to plain text and print context around regex hits.

Usage:
    python htmlgrep.py HTMLFILE REGEX [REGEX ...] [--ctx N] [--dump OUT.txt]

Case-insensitive. --ctx sets characters of context (default 300).
--dump writes the whole stripped text to OUT.txt (UTF-8).
"""
import html
import re
import sys


def strip(s):
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<style.*?</style>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    args = sys.argv[1:]
    ctx = 300
    dump = None
    if "--ctx" in args:
        i = args.index("--ctx")
        ctx = int(args[i + 1])
        del args[i:i + 2]
    if "--dump" in args:
        i = args.index("--dump")
        dump = args[i + 1]
        del args[i:i + 2]
    path, pats = args[0], args[1:]
    raw = open(path, "rb").read()
    for enc in ("utf-8", "gb18030", "latin-1"):
        try:
            s = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    t = strip(s)
    if dump:
        with open(dump, "w", encoding="utf-8") as fh:
            fh.write(t)
    for p in pats:
        for m in re.finditer(p, t, re.I):
            a = max(0, m.start() - ctx)
            b = min(len(t), m.end() + ctx)
            print(f"/{p}/ ... {t[a:b]} ...\n")


if __name__ == "__main__":
    main()
