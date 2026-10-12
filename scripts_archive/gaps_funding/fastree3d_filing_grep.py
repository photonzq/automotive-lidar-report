"""Locate Fastree3D-related passages in Hesai's annual and interim filings (PDF).

Usage:  python fastree3d_filing_grep.py PDF_DIR [OUT_DIR]
Scans every PDF in PDF_DIR page by page (PyMuPDF text layer, used only to locate pages)
for the acquisition and deal-term keywords below, prints file, 1-based page number and a
snippet for every hit, and writes the hit list to OUT_DIR/fastree3d_hits.txt. The pages
found are then rendered to PNG at 160 dpi into OUT_DIR/png/ so they can be read as
images (text extraction alone loses tables and layout).
"""
import os
import re
import sys

import pymupdf

KEYWORDS = [r"fastree", r"switzerland", r"swiss", r"lausanne", r"contingent consideration",
            r"earn[- ]?out", r"business combination", r"acquisition of (?:a )?subsidiar",
            r"patent rights?", r"\bCHF\b", r"image sensors for spatial",
            r"bargain purchase", r"goodwill"]
PAT = re.compile("|".join(KEYWORDS), re.I)


def main():
    pdf_dir = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "fastree3d_out"
    os.makedirs(os.path.join(out, "png"), exist_ok=True)
    lines, pages = [], {}
    for fn in sorted(os.listdir(pdf_dir)):
        if not fn.lower().endswith(".pdf"):
            continue
        doc = pymupdf.open(os.path.join(pdf_dir, fn))
        for i, page in enumerate(doc):
            txt = re.sub(r"\s+", " ", page.get_text())
            hits = {m.group(0).lower() for m in PAT.finditer(txt)}
            strong = {h for h in hits if not h.startswith(("goodwill", "patent"))}
            if not strong:
                continue
            for m in PAT.finditer(txt):
                if m.group(0).lower().startswith(("goodwill", "patent")):
                    continue
                s = txt[max(0, m.start() - 160): m.end() + 200]
                lines.append(f"{fn} p{i + 1} [{m.group(0)}] ...{s}...")
            pages.setdefault(fn, set()).add(i)
    with open(os.path.join(out, "fastree3d_hits.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    for fn, idx in pages.items():
        doc = pymupdf.open(os.path.join(pdf_dir, fn))
        for i in sorted(idx):
            doc[i].get_pixmap(dpi=160).save(os.path.join(out, "png", f"{fn[:-4]}_p{i + 1}.png"))
        print(fn, "pages:", [i + 1 for i in sorted(idx)])


if __name__ == "__main__":
    main()
