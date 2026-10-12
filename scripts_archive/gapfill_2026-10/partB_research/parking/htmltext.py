"""Convert saved HTML files to plain text lines and optionally grep them.

Usage:
    python htmltext.py <file.html> [--grep REGEX [--ctx N]] [--head N]

- Strips <script>/<style>, converts tags to newlines, unescapes entities,
  and drops empty lines.
- With --grep, prints matching lines with N lines of context (default 2).
- With --head, prints only the first N lines of the text.
"""
import html
import re
import sys


def to_lines(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        t = f.read()
    t = re.sub(r"<script.*?</script>", "", t, flags=re.S | re.I)
    t = re.sub(r"<style.*?</style>", "", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", "\n", t)
    t = html.unescape(t)
    return [ln.strip() for ln in t.splitlines() if ln.strip()]


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    if len(argv) < 2:
        print(__doc__)
        return 1
    lines = to_lines(argv[1])
    args = argv[2:]
    if "--grep" in args:
        pat = re.compile(args[args.index("--grep") + 1], re.I)
        ctx = int(args[args.index("--ctx") + 1]) if "--ctx" in args else 2
        shown = set()
        for i, ln in enumerate(lines):
            if pat.search(ln):
                for j in range(max(0, i - ctx), min(len(lines), i + ctx + 1)):
                    if j not in shown:
                        print(f"{j}: {lines[j]}")
                        shown.add(j)
                print("--")
        return 0
    n = int(args[args.index("--head") + 1]) if "--head" in args else len(lines)
    for ln in lines[:n]:
        print(ln)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
