"""R8_C9a_inband: strip a saved HTML page (script and style removed) to UTF-8
text, one line per block element, and print either all lines or the lines that
match a regex, with N lines of context; no network access.

Usage: python R8_html_text.py <saved.html> [regex] [context_lines] [max_lines]
"""
import html as htmllib
import re
import sys


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raw = open(sys.argv[1], encoding="utf-8", errors="replace").read()
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", "", raw, flags=re.S | re.I)
    raw = re.sub(r"<(br|p|div|li|tr|h[1-6]|section|table)[^>]*>", "\n", raw, flags=re.I)
    txt = re.sub(r"<[^>]+>", "", raw)
    txt = htmllib.unescape(txt)
    lines = [l.strip() for l in txt.split("\n") if l.strip()]
    rx = re.compile(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] else None
    ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    mx = int(sys.argv[4]) if len(sys.argv) > 4 else 100000
    out = 0
    if rx is None:
        for l in lines[:mx]:
            print(l)
        return
    for i, l in enumerate(lines):
        if rx.search(l):
            for j in range(max(0, i - ctx), min(len(lines), i + ctx + 1)):
                print(f"{j}: {lines[j][:600]}")
            print("--")
            out += 1
            if out >= mx:
                break


if __name__ == "__main__":
    main()
