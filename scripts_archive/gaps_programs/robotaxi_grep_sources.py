"""robotaxi_grep_sources.py

Purpose
    Extract the visible text of downloaded sources (HTML, PDF, JSON, TXT) and print
    keyword-in-context snippets, to locate sentences about lidar counts and
    suppliers (e.g. "lidar", "LiDAR", "Hesai", "激光雷达") before reading the page
    in full. For PDFs it reports the 0-based page index of each hit so that the
    page can then be rendered and read as an image.

Inputs
    --dir DIR          folder with downloaded files (from robotaxi_fetch_sources.py)
    --glob PATTERN     file-name filter (default "*")
    --kw K1 K2 ...     keywords (case-insensitive regular expressions)
    --width N          characters of context on each side (default 160)
    --dump             also write DIR/text/<file>.txt with the extracted text

Outputs
    Snippets on stdout; optional plain-text dumps under DIR/text/.

Date: 2026-10-03
"""
import argparse
import fnmatch
import json
import os
import re
import sys

from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def html_text(raw):
    soup = BeautifulSoup(raw, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    text = soup.get_text(" ")
    return re.sub(r"\s+", " ", text)


def pdf_pages(path):
    import pymupdf
    doc = pymupdf.open(path)
    return [re.sub(r"\s+", " ", doc[i].get_text()) for i in range(doc.page_count)]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", required=True)
    ap.add_argument("--glob", default="*")
    ap.add_argument("--kw", nargs="+", required=True)
    ap.add_argument("--width", type=int, default=160)
    ap.add_argument("--dump", action="store_true")
    args = ap.parse_args()
    pats = [re.compile(k, re.I) for k in args.kw]
    if args.dump:
        os.makedirs(os.path.join(args.dir, "text"), exist_ok=True)
    for name in sorted(os.listdir(args.dir)):
        path = os.path.join(args.dir, name)
        if not os.path.isfile(path) or not fnmatch.fnmatch(name, args.glob):
            continue
        ext = name.rsplit(".", 1)[-1].lower()
        try:
            if ext == "pdf":
                pages = pdf_pages(path)
            elif ext in ("html", "htm", "xml"):
                with open(path, "rb") as fh:
                    pages = [html_text(fh.read())]
            elif ext == "json":
                with open(path, encoding="utf-8", errors="replace") as fh:
                    pages = [json.dumps(json.load(fh), ensure_ascii=False)]
            elif ext == "txt":
                with open(path, encoding="utf-8", errors="replace") as fh:
                    pages = [fh.read()]
            else:
                continue
        except Exception as exc:
            print(f"## {name}: could not parse ({exc!r})")
            continue
        if args.dump:
            with open(os.path.join(args.dir, "text", name + ".txt"), "w",
                      encoding="utf-8") as out:
                for i, p in enumerate(pages):
                    out.write(f"\n===== page {i} =====\n{p}\n")
        hits = 0
        for i, p in enumerate(pages):
            for pat in pats:
                for m in pat.finditer(p):
                    a, b = max(0, m.start() - args.width), m.end() + args.width
                    if hits == 0:
                        print(f"\n## {name}")
                    where = f"p{i}" if ext == "pdf" else ""
                    print(f"  [{pat.pattern}] {where} ...{p[a:b]}...")
                    hits += 1
        if hits == 0:
            print(f"## {name}: no hits")


if __name__ == "__main__":
    main()
