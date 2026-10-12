"""Round 2, agent R2F_C9: fetches the three sources read for sections C9-C9a and renders the pages used.

- SICK LMS511-10100 PRO data sheet (p. 2: 190 deg field, 25-100 Hz, 0.2-80 m working range, 11.9 mrad).
- Kim, Eom, Choi & Park, IEMEK J. Embed. Sys. Appl. 12(1):43-62 (2017), open access (p. 48 Table 1;
  p. 50 Tables 2-3; p. 53 Tables 4-5; pp. 56-58 power analysis).
- Popko, "Signal interactions between lidar scanners", MS thesis, Georgia Tech (2019), open access
  (printed pp. 100-101 Table 8; pp. 104-112 Tables 9-13; pp. 113-121 direct-interference angular extent).
No e-mail address or identity is sent; a plain browser user agent is used. Usage:
  <anaconda python> R2F_C9_fetch_sources.py <output folder>
"""
import sys
import urllib.request
from pathlib import Path

import pymupdf

SOURCES = {
    "sick_lms511_pro.pdf": ("https://www.sick.com/media/pdf/1/41/941/dataSheet_LMS511-10100-PRO_1046135_en.pdf", [1]),
    "kim_2017_iemek.pdf": ("https://koreascience.kr/article/JAKO201711437355484.pdf", [5, 7, 10, 13, 14, 15]),
    "popko_2019_thesis.pdf": ("https://repository.gatech.edu/server/api/core/bitstreams/"
                              "12d8d33b-3af4-47d8-91b2-cedb80d8f728/content",
                              [120, 121, 125, 126, 129, 131, 132, 134, 135, 140, 141]),
}

out = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
out.mkdir(parents=True, exist_ok=True)
for name, (url, pages) in SOURCES.items():
    dest = out / name
    if not dest.exists():
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            dest.write_bytes(r.read())
    doc = pymupdf.open(dest)
    print(name, doc.page_count, "pages")
    for i in pages:                       # 0-based page indices
        doc[i].get_pixmap(dpi=160).save(out / f"{dest.stem}_p{i + 1:03d}.png")
