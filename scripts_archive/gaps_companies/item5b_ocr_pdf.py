"""OCR image-only PDFs (e.g. USPTO patent prints) with the Windows built-in OCR
engine, via the companion PowerShell script item5b_winocr.ps1.

Usage:
    python item5b_ocr_pdf.py PDF [PDF ...] [--outdir DIR] [--pages a-b] [--lang en-US]
                                   [--dpi 200]

For each PDF, pages are rendered with PyMuPDF to PNG (default 200 dpi) in
DIR/png_<stem>/, then OCR'd; the text is written to DIR/<stem>.txt with a
'===== page N' header per page (N is 1-based). Pages that already carry a text
layer are extracted directly instead of OCR'd. Requires Windows PowerShell 5.1
(powershell.exe) for the WinRT OCR API.
"""
import argparse
import os
import subprocess

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
PS1 = os.path.join(HERE, "item5b_winocr.ps1")


def ocr_pngs(pngs, lang):
    cmd = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", PS1,
           "-Lang", lang, "-PathList", "|".join(pngs)]
    out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                         errors="replace")
    return out.stdout + (("\n[stderr] " + out.stderr) if out.stderr.strip() else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdfs", nargs="+")
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--pages", default=None, help="1-based inclusive range, e.g. 1-12")
    ap.add_argument("--lang", default="en-US")
    ap.add_argument("--dpi", type=int, default=200)
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    for pdf in a.pdfs:
        stem = os.path.splitext(os.path.basename(pdf))[0]
        d = pymupdf.open(pdf)
        lo, hi = 1, d.page_count
        if a.pages:
            s, e = a.pages.split("-")
            lo, hi = max(1, int(s)), min(d.page_count, int(e))
        pngdir = os.path.join(a.outdir, f"png_{stem}")
        os.makedirs(pngdir, exist_ok=True)
        chunks = []
        batch = []
        for n in range(lo, hi + 1):
            txt = d[n - 1].get_text().strip()
            if len(txt) > 200:
                chunks.append((n, txt))
                continue
            p = os.path.join(pngdir, f"p{n:03d}.png")
            if not os.path.exists(p):
                d[n - 1].get_pixmap(dpi=a.dpi).save(p)
            batch.append((n, p))
        # OCR in groups of 10 pages per PowerShell call
        for i in range(0, len(batch), 10):
            grp = batch[i:i + 10]
            raw = ocr_pngs([p for _, p in grp], a.lang)
            parts = raw.split("===== ")
            for part in parts[1:]:
                head, _, body = part.partition("\n")
                base = os.path.basename(head.strip())
                try:
                    n = int(base[1:4])
                except ValueError:
                    n = -1
                chunks.append((n, body))
        chunks.sort(key=lambda t: t[0])
        outp = os.path.join(a.outdir, f"{stem}.txt")
        with open(outp, "w", encoding="utf-8") as f:
            for n, body in chunks:
                f.write(f"===== page {n}\n{body}\n")
        print(f"{pdf}: pages {lo}-{hi} -> {outp}")


if __name__ == "__main__":
    main()
