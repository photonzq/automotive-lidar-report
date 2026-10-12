"""For a govinfo Federal Register HTML/text file, report the Federal Register
page (from the [[Page NNNNN]] markers) on which each regex match occurs.

Usage:
    python fr_page_locator.py <file> <context_chars> <pattern1> [<pattern2> ...]
"""
import html
import re
import sys


def load(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        raw = fh.read()
    if path.lower().endswith((".htm", ".html")):
        raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
        raw = re.sub(r"(?s)<[^>]+>", " ", raw)
        raw = html.unescape(raw)
    return raw


def main():
    path, ctx = sys.argv[1], int(sys.argv[2])
    txt = load(path)
    marks = [(m.start(), m.group(1)) for m in re.finditer(r"\[\[Page (\d+)\]\]", txt)]
    for pat in sys.argv[3:]:
        hits = list(re.finditer(pat, txt, flags=re.I))
        print("=" * 100)
        print(f"PATTERN {pat!r}: {len(hits)} hit(s)")
        for m in hits:
            page = None
            for pos, pg in marks:
                if pos <= m.start():
                    page = pg
                else:
                    break
            a, b = max(0, m.start() - ctx), min(len(txt), m.end() + ctx)
            snippet = re.sub(r"\s+", " ", txt[a:b])
            print(f"--- @ {m.start()}  (on FR page {page if page else 'first page of document'})")
            print(snippet)


if __name__ == "__main__":
    main()
