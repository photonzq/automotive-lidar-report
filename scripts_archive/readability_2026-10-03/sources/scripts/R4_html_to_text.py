"""Strip a saved HTML page to readable text (Round 4, group R4_C7-C7b_F6).

Usage:
  python R4_html_to_text.py <page.htm> <out.txt> [regex]

Drops <script> and <style> blocks, keeps one line per block element, collapses
whitespace, and writes UTF-8 text. With [regex], also prints each matching line
with one line of context (for locating passages; the full text is then read).
Paths come from the command line (e.g. <scratch>/r4). No network access.
"""
import html
import re
import sys
from html.parser import HTMLParser

BLOCK = {"p", "div", "br", "tr", "li", "h1", "h2", "h3", "h4", "h5", "h6",
         "table", "section", "article", "td", "th", "dd", "dt"}


class Stripper(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.skip += 1
        elif tag in BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self.skip:
            self.skip -= 1
        elif tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def main(src, dst, pattern=None):
    raw = open(src, "rb").read().decode("utf-8", errors="replace")
    p = Stripper()
    p.feed(raw)
    text = html.unescape("".join(p.out))
    lines = [" ".join(l.split()) for l in text.splitlines()]
    lines = [l for l in lines if l]
    with open(dst, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"wrote {dst}: {len(lines)} lines")
    if pattern:
        rx = re.compile(pattern, re.I)
        for i, l in enumerate(lines):
            if rx.search(l):
                ctx = " / ".join(lines[max(0, i - 1):i + 2])
                print(f"[{i}] {ctx[:700]}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
