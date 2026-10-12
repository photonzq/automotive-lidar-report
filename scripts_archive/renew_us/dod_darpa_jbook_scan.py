"""DARPA RDT&E justification books: lidar mentions per book and named lidar/photonic beam-steering lines.

Purpose
    (1) Downloads DARPA's RDT&E master justification books (Volume 1, Defense-Wide 0400) for a
        set of budget years from the DoD Comptroller site, unless already present.
    (2) Counts lidar terms (lidar, ladar, laser radar, light detection and ranging) per book,
        with pages and mentions per 1,000 pages, and lists the pages naming the programmes
        SWEEPER, E-PHI, DODOS, MOABB, LUMOS, HALOE and optical phased arrays. Page text is used
        only to locate and count; the amounts below were read from pages rendered at 160 dpi.
    (3) Writes the programme amounts read from the rendered pages (FY, $M, book, page) to CSV.

Inputs
    out_dir : folder for the PDFs, rendered pages and CSVs
Outputs
    dod_darpa_jbook_lidar_mentions.csv, dod_darpa_programme_lines.csv, png/<book>_p<N>.png

Usage:
    python dod_darpa_jbook_scan.py <out_dir>
"""
import csv
import os
import re
import sys

import pymupdf
import requests

BASE = "https://comptroller.war.gov/Portals/45/Documents/defbudget"
BOOKS = {  # budget year -> path under BASE (file names differ by year)
    2014: "fy2014/budget_justification/pdf/03_RDT_and_E/Defense_Advanced_Research_Projects_Agency_PB_2014.pdf",
    2016: "fy2016/budget_justification/pdfs/03_RDT_and_E/DARPA_0400D_RDTE_MasterJustificationBook_Defense_Advanced_Research_Project.pdf",
    2018: "FY2018/budget_justification/pdfs/03_RDT_and_E/DARPA_0400D_FY18PB_FINAL.pdf",
    2020: "FY2020/budget_justification/pdfs/03_RDT_and_E/RDTE_Vol1_DARPA_MasterJustificationBook_PB_2020.pdf",
    2022: "FY2022/budget_justification/pdfs/03_RDT_and_E/RDTE_Vol1_DARPA_MasterJustificationBook_PB_2022.pdf",
    2024: "FY2024/budget_justification/pdfs/03_RDT_and_E/RDTE_Vol1_DARPA_MasterJustificationBook_PB_2024.pdf",
    2026: "FY2026/budget_justification/pdfs/03_RDT_and_E/RDTE_Vol1_DARPA_MasterJustificationBook_PB_2026.pdf",
    2027: "FY2027/budget_justification/pdfs/03_RDT_and_E/RDTE_Vol1_DARPA_MasterJustificationBook_PB_2027.pdf",
}
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
LIDAR = re.compile(r"lidar|ladar|laser radar|light detection and ranging", re.I)
PROGS = re.compile(r"SWEEPER|Electronic-Photonic Heterogeneous|DODOS|Direct On-chip Digital Optical|MOABB|"
                   r"Modular Optical Aperture|LUMOS|Lasers for Universal Microscale|HALOE|optical phased array", re.I)

# Amounts read from rendered pages; $M; "book" is the budget year of the justification book.
LINES = [
    ("SWEEPER", "PE 0602716E", 2012, 7.466, "actual", 2014, 214, "final year; chip-scale phased-array emitter/receiver"),
    ("DODOS", "PE 0602716E", 2015, 3.000, "estimate", 2016, 198, "chip-scale optical frequency synthesis; lists coherent synthesized-aperture lidar"),
    ("DODOS", "PE 0602716E", 2016, 8.000, "request", 2016, 198, ""),
    ("MOABB", "PE 0602716E ELT-01", 2016, 12.000, "actual", 2018, 179, "optical phased arrays; lidar named first among applications"),
    ("MOABB", "PE 0602716E ELT-01", 2017, 16.911, "estimate", 2018, 179, ""),
    ("MOABB", "PE 0602716E ELT-01", 2018, 21.000, "actual", 2020, 167, "request in PB2018 was 22.000"),
    ("MOABB", "PE 0602716E ELT-01", 2019, 20.000, "estimate", 2020, 167, "actual not read (PB2021 not used)"),
    ("MOABB", "PE 0602716E ELT-01", 2020, 19.000, "actual", 2022, 163, ""),
    ("MOABB", "PE 0602716E ELT-01", 2021, 13.141, "estimate", 2022, 163, "no FY2022 funding"),
    ("LUMOS", "PE 0602716E ELT-02", 2020, 8.000, "actual", 2022, 172, "lasers on silicon photonics; lidar not named"),
    ("LUMOS", "PE 0602716E ELT-02", 2021, 21.000, "estimate", 2022, 172, ""),
    ("LUMOS", "PE 0602716E ELT-02", 2022, 23.000, "actual", 2024, 169, ""),
    ("LUMOS", "PE 0602716E ELT-02", 2023, 18.000, "estimate", 2024, 169, ""),
    ("LUMOS", "PE 0602716E ELT-02", 2024, 8.000, "request", 2024, 169, ""),
    ("LUMOS", "PE 0602716E ELT-02", 2025, 9.000, "actual", 2027, 248, ""),
    ("LUMOS", "PE 0602025E MSL-02", 2026, 1.903, "estimate", 2027, 150, "moved to PE 0602025E; nothing for FY2027"),
]


def main(out_dir):
    os.makedirs(os.path.join(out_dir, "png"), exist_ok=True)
    rows = []
    for year, path in BOOKS.items():
        fn = os.path.join(out_dir, f"DARPA_PB{year}.pdf")
        if not os.path.exists(fn):
            r = requests.get(f"{BASE}/{path}", headers=UA, timeout=300)
            if r.status_code != 200 or not r.content.startswith(b"%PDF"):
                print(year, "download failed", r.status_code)
                continue
            open(fn, "wb").write(r.content)
        d = pymupdf.open(fn)
        hits, pages, progs = 0, [], {}
        for i in range(d.page_count):
            t = d[i].get_text()
            n = len(LIDAR.findall(t))
            if n:
                hits += n
                pages.append(i + 1)
            for m in PROGS.finditer(t):
                progs.setdefault(m.group(0).upper(), set()).add(i + 1)
        rows.append((year, d.page_count, hits, round(1000 * hits / d.page_count, 1), ";".join(map(str, pages)),
                     "; ".join(f"{k}:{sorted(v)[:6]}" for k, v in progs.items())))
        print(rows[-1][:4])
    with open(os.path.join(out_dir, "dod_darpa_jbook_lidar_mentions.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["budget_year", "pages", "lidar_mentions", "per_1000_pages", "pages_with_mentions", "programme_pages"])
        w.writerows(rows)
    with open(os.path.join(out_dir, "dod_darpa_programme_lines.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["programme", "line", "fiscal_year", "usd_million", "status", "book_budget_year", "pdf_page", "note"])
        w.writerows(LINES)
    for prog, _, fy, usd, _, book, page, _ in LINES:
        png = os.path.join(out_dir, "png", f"DARPA_PB{book}_p{page}.png")
        fn = os.path.join(out_dir, f"DARPA_PB{book}.pdf")
        if os.path.exists(fn) and not os.path.exists(png):
            pymupdf.open(fn)[page - 1].get_pixmap(dpi=160).save(png)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
