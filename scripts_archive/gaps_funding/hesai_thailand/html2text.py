"""Convert a saved HTML file to plain text and optionally print context around keywords.

Usage:
    python scripts/html2text.py <file.html> [keyword1 keyword2 ...] [--window N] [--full]

Writes <file>.txt next to the HTML file. With keywords, prints +/- N characters
(default 800) of context around every case-insensitive hit. With --full, prints
the whole text.
"""
import html
import re
import sys


def to_text(path):
    raw = open(path, encoding="utf-8", errors="ignore").read()
    raw = re.sub(r"(?is)<(script|style|noscript).*?</\1>", "", raw)
    raw = re.sub(r"(?i)<br\s*/?>", "\n", raw)
    raw = re.sub(r"(?i)</(p|div|li|h\d|tr|td|th|section|article)>", "\n", raw)
    txt = re.sub(r"(?s)<[^>]+>", " ", raw)
    txt = html.unescape(txt)
    lines = [re.sub(r"[ \t ]+", " ", l).strip() for l in txt.split("\n")]
    lines = [l for l in lines if l]
    return "\n".join(lines)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    path = args[0]
    window = 800
    full = False
    kws = []
    i = 1
    while i < len(args):
        a = args[i]
        if a == "--window":
            window = int(args[i + 1])
            i += 2
            continue
        if a == "--full":
            full = True
            i += 1
            continue
        kws.append(a)
        i += 1
    txt = to_text(path)
    out = re.sub(r"\.html?$", "", path) + ".txt"
    open(out, "w", encoding="utf-8").write(txt)
    print(f"[saved {out}, {len(txt)} chars]")
    if full:
        print(txt)
        return
    for kw in kws:
        hits = [m.start() for m in re.finditer(re.escape(kw), txt, flags=re.I)]
        print(f"\n===== '{kw}': {len(hits)} hits =====")
        last_end = -1
        for h in hits:
            a, b = max(0, h - window), min(len(txt), h + window)
            if a < last_end:
                continue
            print(f"--- @{h} ---")
            print(txt[a:b])
            last_end = b


if __name__ == "__main__":
    main()
