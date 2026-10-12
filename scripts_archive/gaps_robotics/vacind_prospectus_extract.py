"""Download robot-vacuum and industrial-lidar filings and print the key passages.

Used for the Appendix 1 items "Robot vacuums" and "Industrial-lidar market size"
of the automotive perception report. The documents are:

* LDROBOT (Shenzhen LDROBOT Co., HKEX 01236): application proof of 1 Dec 2025
  (which carries the "over 720,000 units of DTOF LiDAR" claim for 2024), the
  prospectus of 30 Apr 2026 (which replaces it with "over 4,000,000 units" for
  2025) and the H1 2026 interim results;
* Camsense (HKEX 06802): prospectus of 22 Sep 2026 (CIC market tables, the
  "approximately 80%" lidar share of robot vacuums, unit volumes and average
  prices by product line);
* Vanjee Technology (SZSE 300552): 2025 annual report (lidar revenue and units).

Usage
-----
    python vacind_prospectus_extract.py OUTDIR

Each file is downloaded once into OUTDIR (relative to the working directory),
then sentences matching the keyword patterns are printed with page numbers.
Read the pages themselves (render to PNG) before quoting any figure: text
extraction loses chart labels and table alignment.

Only a generic browser User-Agent is sent; no cookies, logins or personal data.
"""
import os
import re
import sys
import time

import pymupdf
import requests

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124 Safari/537.36"}
HK = "https://www1.hkexnews.hk"
DOCS = {
    "ldrobot_application_proof.pdf": HK + "/listedco/listconews/sehk/2026/0511/sehk25120104096.pdf",
    "ldrobot_prospectus.pdf": HK + "/listedco/listconews/sehk/2026/0430/2026043000099.pdf",
    "ldrobot_h1_2026_results.pdf": HK + "/listedco/listconews/sehk/2026/0824/2026082400450.pdf",
    "camsense_prospectus.pdf": HK + "/listedco/listconews/sehk/2026/0922/2026092200005.pdf",
    "vanjee_annual_report_2025.pdf": "http://static.cninfo.com.cn/finalpage/2026-03-31/1225062787.PDF",
}
PATTERNS = [
    r"[^.]{0,250}units of DTOF LiDAR[^.]{0,200}\.",
    r"[^.]{0,250}DTOF LiDAR products accounted for[^.]{0,200}\.",
    r"[^.]{0,250}equipped with LiDAR technology[^.]{0,200}\.",
    r"[^.]{0,250}robotic vacuum LiDAR market size[^.]{0,250}\.",
    r"[^.]{0,250}Triangulation LiDAR \. \.[^.]{0,250}",
    r".{0,80}激光雷达 销售量 套.{0,120}",
    r".{0,40}分产品.{0,40}激光雷达 [\d,\.]+ [\d\.]+%.{0,60}",
]


def fetch(name: str, url: str, out: str) -> str:
    os.makedirs(out, exist_ok=True)
    fn = os.path.join(out, name)
    if not os.path.exists(fn):
        r = requests.get(url, headers=UA, timeout=240)
        r.raise_for_status()
        with open(fn, "wb") as f:
            f.write(r.content)
        time.sleep(1.0)
    return fn


def main() -> None:
    out = sys.argv[1] if len(sys.argv) > 1 else "vacind_docs"
    for name, url in DOCS.items():
        fn = fetch(name, url, out)
        doc = pymupdf.open(fn)
        print(f"===== {name}: {doc.page_count} pages")
        for i, page in enumerate(doc):
            text = re.sub(r"\s+", " ", page.get_text())
            for pat in PATTERNS:
                for m in re.finditer(pat, text):
                    print(f"p{i + 1}: {m.group(0).strip()[:500]}")


if __name__ == "__main__":
    main()
