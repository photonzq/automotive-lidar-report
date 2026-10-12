"""Convert a saved HTML file to plain text and print keyword-in-context snippets.

Usage:
    python html2txt_grep.py <file.html> <context_chars> <pattern1> [<pattern2> ...]

Patterns are case-insensitive regular expressions. The plain-text version is
also written next to the input as <file>.txt for later inspection.
"""
import html
import re
import sys


def html_to_text(raw):
    raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>", "\n", raw)
    raw = re.sub(r"(?i)</(p|div|li|tr|h[1-6]|section|heading)>", "\n", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    txt = html.unescape(raw)
    txt = re.sub(r"[ \t\r\f\v]+", " ", txt)
    txt = re.sub(r"\n\s*\n+", "\n", txt)
    return txt


def main():
    path = sys.argv[1]
    ctx = int(sys.argv[2])
    pats = sys.argv[3:]
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        raw = fh.read()
    txt = html_to_text(raw) if path.lower().endswith((".html", ".htm")) else raw
    if path.lower().endswith((".html", ".htm")):
        with open(path + ".txt", "w", encoding="utf-8") as fh:
            fh.write(txt)
    for pat in pats:
        hits = list(re.finditer(pat, txt, flags=re.I))
        print("=" * 100)
        print(f"PATTERN {pat!r}: {len(hits)} hit(s)")
        for k, m in enumerate(hits):
            a = max(0, m.start() - ctx)
            b = min(len(txt), m.end() + ctx)
            snippet = txt[a:b].replace("\n", " | ")
            print(f"--- hit {k + 1} @ {m.start()}")
            print(snippet)


if __name__ == "__main__":
    main()
