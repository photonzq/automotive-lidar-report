"""Convert downloaded SEC filing HTML documents (and press-release HTML) to plain text.

Walks ./sec/ and ./press/ (relative to the aeva_oem folder), and for every main
document or exhibit (.htm/.html, excluding EDGAR index pages and XBRL R*.htm
viewer pages) writes a sibling .txt file with whitespace-normalised text.
Inline-XBRL hidden headers are dropped. Tables are flattened row by row with
' | ' between cells so that numeric tables stay readable.

Usage (run from the aeva_oem folder):
    python scripts/html_to_text.py
"""
import os
import re

from bs4 import BeautifulSoup

SKIP = re.compile(r"(-index(-headers)?\.html$)|(^R\d+\.htm$)", re.I)


def convert(path):
    raw = open(path, "rb").read().decode("utf-8", errors="replace")
    soup = BeautifulSoup(raw, "lxml")
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    for t in soup.find_all(["ix:header"]):
        t.decompose()
    for tr in soup.find_all("tr"):
        cells = [c.get_text(" ", strip=True) for c in tr.find_all(["td", "th"])]
        cells = [c for c in cells if c]
        tr.replace_with(soup.new_string("\n" + " | ".join(cells) + "\n"))
    for br in soup.find_all(["br"]):
        br.replace_with("\n")
    for blk in soup.find_all(["p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6"]):
        blk.insert_after("\n")
    text = soup.get_text("")
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def main():
    for root in ("sec", "press"):
        if not os.path.isdir(root):
            continue
        for dirpath, _, files in os.walk(root):
            for f in files:
                if not f.lower().endswith((".htm", ".html")) or SKIP.search(f):
                    continue
                p = os.path.join(dirpath, f)
                out = os.path.splitext(p)[0] + ".txt"
                try:
                    txt = convert(p)
                except Exception as e:  # noqa: BLE001
                    print("fail", p, e)
                    continue
                open(out, "w", encoding="utf-8").write(txt)
                print(out, len(txt))


if __name__ == "__main__":
    main()
