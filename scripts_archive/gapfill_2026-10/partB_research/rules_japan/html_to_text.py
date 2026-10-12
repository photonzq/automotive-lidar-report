"""Strip an HTML file to readable text lines and write them as UTF-8.

Usage:
    python html_to_text.py INPUT.html OUTPUT.txt [MIN_LINE_LENGTH]

Scripts and styles are removed; tags become line breaks; lines shorter than
MIN_LINE_LENGTH (default 1) are dropped.
"""
import html
import re
import sys


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    minlen = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    raw = open(sys.argv[1], "rb").read()
    for enc in ("utf-8", "cp932", "euc-jp", "latin-1"):
        try:
            t = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    t = re.sub(r"(?is)<script.*?</script>|<style.*?</style>|<!--.*?-->", "", t)
    t = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</h\d>|</tr>|</div>", "\n", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    lines = [" ".join(l.split()) for l in t.split("\n")]
    lines = [l for l in lines if len(l) >= minlen]
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {len(lines)} lines to {sys.argv[2]}")


if __name__ == "__main__":
    main()
