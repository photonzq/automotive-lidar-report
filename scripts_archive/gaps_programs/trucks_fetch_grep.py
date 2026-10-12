"""Fetch web pages or PDFs, keep the raw copy, and print keyword-in-context snippets.

Purpose
    Support the autonomous-truck and robotaxi lidar gap research (report Appendix 1,
    items on Aurora, Kodiak, Waabi, PlusAI, Gatik, Bot Auto, Avride, May Mobility).
    Each URL is downloaded with a generic browser-like User-Agent (no contact details),
    the raw bytes are saved, visible text is extracted (HTML via BeautifulSoup, PDF via
    PyMuPDF), and every case-insensitive keyword hit is printed with surrounding context
    so that verbatim quotes can be checked against the source.

Inputs (command line)
    --out DIR        data folder for raw downloads and extracted text (default: ./data)
    --kw  WORD ...   keywords or regular expressions to locate (default: lidar terms)
    --ctx N          characters of context on each side of a hit (default: 220)
    URL ...          one or more URLs

Outputs
    DIR/<slug>.html or .pdf   raw download
    DIR/<slug>.txt            extracted visible text
    stdout                    HTTP status, final URL, size, and keyword-in-context lines

Date: 2026-10-03
"""
import argparse
import hashlib
import os
import re
import sys

import requests

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
DEFAULT_KW = [r"lidar", r"LiDAR", r"FirstLight", r"Hesai", r"Luminar", r"Ouster",
              r"Aeva", r"Innoviz", r"Velodyne", r"sensor"]


def slug_for(url):
    base = re.sub(r"[^A-Za-z0-9]+", "_", url.split("://", 1)[-1])[:80].strip("_")
    return base + "_" + hashlib.md5(url.encode()).hexdigest()[:6]


def html_to_text(raw):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(raw, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    text = soup.get_text(" ")
    return re.sub(r"\s+", " ", text)


def pdf_to_text(path):
    import pymupdf
    doc = pymupdf.open(path)
    parts = []
    for i, page in enumerate(doc):
        parts.append(f" [[page {i + 1}]] " + page.get_text())
    return re.sub(r"\s+", " ", " ".join(parts))


def main():
    try:  # avoid console code-page errors on Windows
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data")
    ap.add_argument("--kw", nargs="*", default=DEFAULT_KW)
    ap.add_argument("--ctx", type=int, default=220)
    ap.add_argument("--maxhits", type=int, default=60)
    ap.add_argument("urls", nargs="+")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    sess = requests.Session()
    sess.headers.update({"User-Agent": UA,
                         "Accept": "text/html,application/xhtml+xml,application/pdf,*/*;q=0.8",
                         "Accept-Language": "en-US,en;q=0.9"})
    for url in a.urls:
        print("=" * 100)
        print("URL:", url)
        try:
            r = sess.get(url, timeout=60, allow_redirects=True)
        except Exception as exc:  # network errors are reported, not raised
            print("  ERROR:", exc)
            continue
        ctype = r.headers.get("Content-Type", "")
        print(f"  status={r.status_code} final={r.url} type={ctype} bytes={len(r.content)}")
        slug = slug_for(url)
        is_pdf = "pdf" in ctype.lower() or r.content[:5] == b"%PDF-"
        raw_path = os.path.join(a.out, slug + (".pdf" if is_pdf else ".html"))
        with open(raw_path, "wb") as fh:
            fh.write(r.content)
        try:
            text = pdf_to_text(raw_path) if is_pdf else html_to_text(r.content)
        except Exception as exc:
            print("  text extraction failed:", exc)
            continue
        with open(os.path.join(a.out, slug + ".txt"), "w", encoding="utf-8") as fh:
            fh.write(text)
        print("  saved:", raw_path, " text chars:", len(text))
        title = re.search(r"<title[^>]*>(.*?)</title>", r.text if not is_pdf else "", re.S | re.I)
        if title:
            print("  title:", re.sub(r"\s+", " ", title.group(1)).strip()[:200])
        nhits = 0
        seen = []
        for kw in a.kw:
            for m in re.finditer(kw, text, re.I):
                s, e = max(0, m.start() - a.ctx), min(len(text), m.end() + a.ctx)
                if any(abs(s - p) < a.ctx for p in seen):
                    continue
                seen.append(s)
                print(f"  [{kw}] ...{text[s:e]}...")
                nhits += 1
                if nhits >= a.maxhits:
                    break
            if nhits >= a.maxhits:
                print("  (hit limit reached)")
                break
        print("  total hits shown:", nhits)


if __name__ == "__main__":
    sys.exit(main())
